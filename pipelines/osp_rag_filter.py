"""
OSP RAG Filter Pipeline
========================

Filter Pipeline die RAG-Kontext zu Anfragen hinzufügt.
Arbeitet mit jedem Modell (z.B. osp-claude-45) zusammen.

Embedding-Modell: intfloat/multilingual-e5-large (1024 dim)

WICHTIG: Verwendet Modul-Level Singleton für Ressourcen,
da Open WebUI Filter bei jedem Request neu instanziiert.

Autor: AL
Stand: 2025-12-15
"""

import logging
import threading
from typing import List, Optional
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("osp_rag_filter")

# ============================================================================
# MODUL-LEVEL SINGLETON (wird nur EINMAL beim Import geladen)
# ============================================================================

_GLOBAL_RESOURCES = {
    "chroma_client": None,
    "embedding_model": None,
    "initialized": False,
    "init_lock": threading.Lock(),
    "init_error": None
}


def _initialize_resources():
    """
    Initialisiert globale Ressourcen (Thread-safe Singleton).

    Wird nur einmal ausgeführt, auch bei mehreren Filter-Instanzen.
    """
    global _GLOBAL_RESOURCES

    # Double-check locking pattern
    if _GLOBAL_RESOURCES["initialized"]:
        return

    with _GLOBAL_RESOURCES["init_lock"]:
        # Nochmal prüfen nach Lock-Erwerb
        if _GLOBAL_RESOURCES["initialized"]:
            return

        logger.info("=" * 60)
        logger.info("OSP RAG Filter - Modul-Level Initialisierung")
        logger.info("=" * 60)

        # 1. E5-large Embedding-Modell laden
        try:
            logger.info("Lade E5-large Embedding-Modell...")
            from sentence_transformers import SentenceTransformer

            _GLOBAL_RESOURCES["embedding_model"] = SentenceTransformer(
                'intfloat/multilingual-e5-large',
                device='cpu'
            )
            dim = _GLOBAL_RESOURCES["embedding_model"].get_sentence_embedding_dimension()
            logger.info(f"E5-large geladen (Dimension: {dim})")
        except Exception as e:
            logger.error(f"E5-large Fehler: {e}")
            _GLOBAL_RESOURCES["init_error"] = str(e)
            _GLOBAL_RESOURCES["initialized"] = True
            return

        # 2. ChromaDB verbinden
        try:
            logger.info("Verbinde mit ChromaDB...")
            import chromadb
            from chromadb.config import Settings

            _GLOBAL_RESOURCES["chroma_client"] = chromadb.HttpClient(
                host="chromadb",
                port=8000,
                settings=Settings(anonymized_telemetry=False)
            )

            collections = _GLOBAL_RESOURCES["chroma_client"].list_collections()
            logger.info(f"ChromaDB verbunden: {len(collections)} Collections")
            for col in collections:
                try:
                    count = col.count()
                    logger.info(f"  - {col.name}: {count} Dokumente")
                except:
                    logger.info(f"  - {col.name}: (count n/a)")
        except Exception as e:
            logger.error(f"ChromaDB Fehler: {e}")
            _GLOBAL_RESOURCES["init_error"] = str(e)
            _GLOBAL_RESOURCES["initialized"] = True
            return

        _GLOBAL_RESOURCES["initialized"] = True
        logger.info("=" * 60)
        logger.info("OSP RAG Filter READY")
        logger.info("=" * 60)


# ============================================================================
# FILTER KLASSE
# ============================================================================

class Filter:
    """
    OSP RAG Filter.

    Fügt RAG-Kontext aus ChromaDB zur Anfrage hinzu,
    bevor sie an das ausgewählte Modell weitergeleitet wird.
    """

    class Valves(BaseModel):
        """Filter-Konfiguration"""
        CHROMADB_HOST: str = Field(default="chromadb", description="ChromaDB Host")
        CHROMADB_PORT: int = Field(default=8000, description="ChromaDB Port")
        MAX_CONTEXT_LENGTH: int = Field(default=16000, description="Max Context-Länge")
        TOP_K: int = Field(default=15, description="Anzahl der RAG-Ergebnisse pro Collection")
        PRIORITY_PIPELINES: List[str] = Field(
            default=["*"],
            description="Modelle für die dieser Filter gilt (* = alle)"
        )

    def __init__(self):
        """Initialize Filter - nutzt globale Ressourcen."""
        self.name = "OSP RAG Filter"
        self.valves = self.Valves()

        # Initialisierung beim ersten Instanz-Erstellen triggern
        _initialize_resources()

    @property
    def chroma_client(self):
        """Zugriff auf globalen ChromaDB Client."""
        return _GLOBAL_RESOURCES["chroma_client"]

    @property
    def embedding_model(self):
        """Zugriff auf globales Embedding-Modell."""
        return _GLOBAL_RESOURCES["embedding_model"]

    @property
    def is_ready(self):
        """Prüft ob alle Ressourcen verfügbar sind."""
        return (
            _GLOBAL_RESOURCES["initialized"] and
            _GLOBAL_RESOURCES["chroma_client"] is not None and
            _GLOBAL_RESOURCES["embedding_model"] is not None
        )

    async def on_startup(self):
        """Wird von Open WebUI beim Start aufgerufen (falls implementiert)."""
        logger.info("on_startup aufgerufen")
        _initialize_resources()

    async def on_shutdown(self):
        """Cleanup beim Shutdown."""
        logger.info("OSP RAG Filter Shutdown")

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """
        INLET: Verarbeitet eingehende Anfragen VOR dem Modell.

        Fügt RAG-Kontext zum System-Prompt hinzu.
        """
        logger.info("INLET aufgerufen")

        # Sicherstellen, dass Ressourcen initialisiert sind
        _initialize_resources()

        # Prüfen ob RAG verfügbar
        if not self.is_ready:
            error = _GLOBAL_RESOURCES.get("init_error", "Unbekannter Fehler")
            logger.warning(f"RAG nicht verfügbar: {error}")
            return body

        # Letzte User-Nachricht extrahieren
        messages = body.get("messages", [])
        if not messages:
            logger.info("Keine Messages im Body")
            return body

        user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str):
                    user_message = content
                elif isinstance(content, list):
                    # Multi-modal content
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            user_message = item.get("text", "")
                            break
                        elif isinstance(item, str):
                            user_message = item
                            break
                break

        if not user_message:
            logger.info("Keine User-Nachricht gefunden")
            return body

        logger.info(f"RAG-Query: '{user_message[:80]}...'")

        # RAG-Kontext abrufen
        context = self._retrieve_context(user_message)

        if not context:
            logger.info("Kein RAG-Kontext gefunden")
            return body

        # System-Prompt mit Kontext erstellen/erweitern
        osp_system_prompt = f"""Du bist der OSP-Assistent für Rainer Schneider Kabelsatzbau GmbH & Co. KG.

WICHTIGE REGELN:
1. Antworte NUR basierend auf dem bereitgestellten Kontext
2. Gib Confidence-Level an: (C: XX%)
3. Bei Unsicherheit: Nachfragen statt raten
4. Kennzeichne Antworten mit [OSP]
5. NULL-FEHLER-POLITIK: Keine erfundenen Daten!

═══════════════════════════════════════════════════════════
KONTEXT AUS DER WISSENSDATENBANK:
═══════════════════════════════════════════════════════════
{context}
═══════════════════════════════════════════════════════════
"""

        # Bestehenden System-Prompt prüfen und erweitern
        if messages and messages[0].get("role") == "system":
            original_system = messages[0].get("content", "")
            messages[0]["content"] = f"{osp_system_prompt}\n\n--- URSPRÜNGLICHER SYSTEM-PROMPT ---\n{original_system}"
            logger.info("System-Prompt erweitert")
        else:
            messages.insert(0, {
                "role": "system",
                "content": osp_system_prompt
            })
            logger.info("System-Prompt hinzugefügt")

        body["messages"] = messages
        logger.info(f"RAG-Kontext injiziert ({len(context)} Zeichen)")

        return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """
        OUTLET: Verarbeitet Antworten NACH dem Modell.
        """
        return body

    def _expand_person_query(self, query: str) -> str:
        """
        Erweitert Personen-Anfragen für besseres Ranking.

        "wer ist AL" -> "wer ist AL Mitarbeiter Kürzel Personalstamm"
        """
        import re

        # Pattern für Personen-Anfragen
        person_patterns = [
            r'wer ist (\w{2,4})\b',
            r'was macht (\w{2,4})\b',
            r'kontakt (\w{2,4})\b',
            r'email (\w{2,4})\b',
            r'telefon (\w{2,4})\b',
            r'personalnummer (\w{2,4})\b',
        ]

        query_lower = query.lower()
        for pattern in person_patterns:
            match = re.search(pattern, query_lower)
            if match:
                kuerzel = match.group(1).upper()
                # Query erweitern für besseres HR_CORE Ranking
                expanded = f"{query} Mitarbeiter Kürzel {kuerzel} Personalstamm HR_CORE"
                logger.info(f"Query erweitert: '{query}' -> '{expanded}'")
                return expanded

        return query

    def _retrieve_context(self, query: str) -> str:
        """
        Ruft relevanten Kontext aus ChromaDB ab.

        Multi-Layer Strategie:
        1. OSP_KERN (Priorität 1)
        2. OSP_KPL (Priorität 2)
        3. OSP_ERWEITERT (Priorität 3)
        """
        try:
            # Query für Personen-Anfragen erweitern
            expanded_query = self._expand_person_query(query)

            # E5 Query-Embedding berechnen
            query_with_prefix = f"query: {expanded_query}"
            query_embedding = self.embedding_model.encode(
                [query_with_prefix],
                normalize_embeddings=True
            ).tolist()

            # Multi-Layer Suche
            collections_priority = ["osp_kern", "osp_kpl", "osp_erweitert"]
            all_results = []
            top_k = self.valves.TOP_K

            for collection_name in collections_priority:
                try:
                    collection = self.chroma_client.get_collection(collection_name)

                    results = collection.query(
                        query_embeddings=query_embedding,
                        n_results=top_k,
                        include=["documents", "metadatas", "distances"]
                    )

                    if results and results.get('documents') and results['documents'][0]:
                        for doc, meta, dist in zip(
                            results['documents'][0],
                            results['metadatas'][0],
                            results['distances'][0]
                        ):
                            all_results.append({
                                'document': doc,
                                'metadata': meta,
                                'distance': dist,
                                'source': collection_name,
                                'filename': meta.get('filename', 'unbekannt')
                            })
                        logger.info(f"  {collection_name}: {len(results['documents'][0])} Treffer")
                except Exception as e:
                    logger.warning(f"Collection {collection_name} nicht verfügbar: {e}")
                    continue

            logger.info(f"Gesamt: {len(all_results)} Ergebnisse aus {len(collections_priority)} Collections")

            # Nach Distanz sortieren (kleinere = besser)
            all_results.sort(key=lambda x: x['distance'])

            # Kontext zusammenstellen
            context_parts = []
            max_length = self.valves.MAX_CONTEXT_LENGTH
            current_length = 0

            for result in all_results[:top_k]:
                doc = result['document']
                filename = result['filename']
                score = 1 - result['distance']

                if doc is None or len(doc) == 0:
                    continue
                if current_length + len(doc) > max_length:
                    if current_length == 0:
                        truncated = doc[:max_length - 200] + "\n...[TRUNCATED]..."
                        context_parts.append(f"[Quelle: {filename} | Score: {score:.2f}]\n{truncated}")
                        current_length = len(truncated)
                    break

                context_parts.append(f"[Quelle: {filename} | Score: {score:.2f}]\n{doc}")
                current_length += len(doc)

            logger.info(f"{len(context_parts)} Kontextblöcke ({current_length} Zeichen)")

            return "\n\n---\n\n".join(context_parts)

        except Exception as e:
            logger.error(f"Context Retrieval Error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return ""
