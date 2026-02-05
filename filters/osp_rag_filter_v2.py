"""
OSP RAG Filter v2.0 - Mit Modul-Level Singleton für Lazy Loading
================================================================

Löst das Problem dass on_startup() bei Filtern nicht aufgerufen wird.
Nutzt Thread-safe Lazy Loading auf Modul-Ebene.

Autor: AL
Stand: 2025-12-15
"""

from typing import Optional
import logging
import re
import threading

logger = logging.getLogger(__name__)

# ============================================================
# MODUL-LEVEL SINGLETON - Wird NUR EINMAL initialisiert
# ============================================================
_initialized = False
_init_lock = threading.Lock()
_chroma_client = None
_embedding_model = None
_collections = {}


def _ensure_initialized():
    """
    Thread-safe Lazy Loading auf Modul-Ebene.
    Wird beim ersten Request aufgerufen, danach gecached.
    """
    global _initialized, _chroma_client, _embedding_model, _collections

    if _initialized:
        return True

    with _init_lock:
        # Double-check nach Lock
        if _initialized:
            return True

        try:
            logger.info("🚀 OSP RAG Filter - Initialisierung startet...")

            # 1. ChromaDB verbinden
            import chromadb
            from chromadb.config import Settings
            _chroma_client = chromadb.HttpClient(
                host="chromadb",
                port=8000,
                settings=Settings(anonymized_telemetry=False)
            )
            logger.info("✅ ChromaDB verbunden")

            # 2. Collections laden
            collection_names = ["osp_kern", "osp_kpl", "osp_erweitert"]
            for name in collection_names:
                try:
                    _collections[name] = _chroma_client.get_collection(name)
                    count = _collections[name].count()
                    logger.info(f"  📚 {name}: {count} Dokumente")
                except Exception as e:
                    logger.warning(f"  ⚠️ Collection {name} nicht gefunden: {e}")

            # 3. Embedding Model laden (optional - für bessere Suche)
            try:
                from sentence_transformers import SentenceTransformer
                _embedding_model = SentenceTransformer("intfloat/multilingual-e5-large")
                logger.info("✅ Embedding Model geladen (E5-large)")
            except Exception as e:
                logger.warning(f"⚠️ Embedding Model nicht geladen: {e}")
                logger.info("   → Fallback auf ChromaDB Default-Embeddings")

            _initialized = True
            logger.info("✅ OSP RAG Filter READY")
            return True

        except Exception as e:
            logger.error(f"❌ Initialisierung fehlgeschlagen: {e}")
            return False


class Filter:
    """
    OSP RAG Filter - Injiziert Kontext aus ChromaDB vor dem LLM-Aufruf.
    """

    class Valves:
        """Konfigurierbare Parameter"""
        def __init__(self):
            self.TOP_K = 15
            self.MIN_RELEVANCE = 0.25
            self.ENABLE_QUERY_EXPANSION = True
            self.DEBUG_MODE = False

    def __init__(self):
        self.name = "OSP RAG Filter"
        self.valves = self.Valves()

    def _expand_query(self, query: str) -> str:
        """
        Erweitert Queries für besseres RAG-Ranking.
        z.B. "wer ist AL" → "wer ist AL Mitarbeiter Kürzel AL Personalstamm HR_CORE"
        """
        query_lower = query.lower()
        expanded = query

        # MA-Kürzel Pattern (2-3 Großbuchstaben)
        ma_pattern = r'\b([A-Z]{2,3})\b'
        ma_matches = re.findall(ma_pattern, query)

        if ma_matches or "wer ist" in query_lower or "mitarbeiter" in query_lower:
            expanded = f"{query} Mitarbeiter Kürzel Personalstamm HR_CORE"

        # Maschinen-Keywords
        if any(kw in query_lower for kw in ["maschine", "anlage", "inventar", "komax", "schleuniger"]):
            expanded = f"{query} Maschinen Anlagen TM_CORE Inventar"

        # Werkzeug-Keywords
        if any(kw in query_lower for kw in ["werkzeug", "wkz", "kontakt"]):
            expanded = f"{query} Werkzeug WKZ TM_WKZ"

        # Qualitäts-Keywords
        if any(kw in query_lower for kw in ["null-fehler", "qualität", "reklamation", "8d"]):
            expanded = f"{query} Qualität QM_CORE NULL-FEHLER"

        return expanded

    def _query_chromadb(self, query: str) -> str:
        """
        Multi-Layer ChromaDB Query.
        Priorisiert OSP_KERN, ergänzt mit OSP_ERWEITERT bei Bedarf.

        WICHTIG: Collections nutzen E5-large (1024 dim).
        query_texts nutzt Default-Model (384 dim) → Dimension Mismatch!
        Daher MUSS query_embeddings verwendet werden.
        """
        global _collections, _embedding_model

        if not _collections:
            logger.warning("Keine Collections verfügbar")
            return ""

        # E5-large ist PFLICHT - ohne funktioniert es nicht!
        if not _embedding_model:
            logger.error("E5-large Embedding Model nicht verfügbar - RAG kann nicht funktionieren!")
            return ""

        context_parts = []
        expanded_query = self._expand_query(query) if self.valves.ENABLE_QUERY_EXPANSION else query

        if self.valves.DEBUG_MODE:
            logger.info(f"🔍 Query: {query}")
            logger.info(f"🔍 Expanded: {expanded_query}")

        # Embedding berechnen - PFLICHT für 1024-dim Collections
        try:
            query_with_prefix = f"query: {expanded_query}"
            query_embedding = _embedding_model.encode(
                [query_with_prefix],
                normalize_embeddings=True
            ).tolist()
            logger.info(f"✅ Embedding berechnet: {len(query_embedding[0])} Dimensionen")
        except Exception as e:
            logger.error(f"Embedding Fehler: {e}")
            return ""

        # Layer 1: OSP_KERN (kritische Stammdaten)
        if "osp_kern" in _collections:
            try:
                results = _collections["osp_kern"].query(
                    query_embeddings=query_embedding,
                    n_results=self.valves.TOP_K,
                    include=["documents", "metadatas", "distances"]
                )
                if results and results.get("documents"):
                    for i, doc in enumerate(results["documents"][0]):
                        if doc and len(doc) > 50:
                            meta = results.get("metadatas", [[]])[0]
                            filename = meta[i].get("filename", "unbekannt") if meta else "unbekannt"
                            context_parts.append(f"[Quelle: {filename}]\n{doc}")
                    logger.info(f"📚 osp_kern: {len(results['documents'][0])} Treffer")
            except Exception as e:
                logger.error(f"KERN Query Error: {e}")

        # Layer 2: OSP_KPL (Datei-Index)
        if "osp_kpl" in _collections:
            try:
                results = _collections["osp_kpl"].query(
                    query_embeddings=query_embedding,
                    n_results=5,
                    include=["documents", "metadatas"]
                )
                if results and results.get("documents"):
                    for i, doc in enumerate(results["documents"][0]):
                        if doc and len(doc) > 20:
                            meta = results.get("metadatas", [[]])[0]
                            filename = meta[i].get("filename", "unbekannt") if meta else "unbekannt"
                            context_parts.append(f"[Quelle: {filename}]\n{doc}")
            except Exception as e:
                logger.warning(f"KPL Query Error: {e}")

        # Layer 3: OSP_ERWEITERT (nur wenn wenig KERN-Treffer)
        if len(context_parts) < 5 and "osp_erweitert" in _collections:
            try:
                results = _collections["osp_erweitert"].query(
                    query_embeddings=query_embedding,
                    n_results=8,
                    include=["documents", "metadatas"]
                )
                if results and results.get("documents"):
                    for i, doc in enumerate(results["documents"][0]):
                        if doc and len(doc) > 50:
                            meta = results.get("metadatas", [[]])[0]
                            filename = meta[i].get("filename", "unbekannt") if meta else "unbekannt"
                            context_parts.append(f"[Quelle: {filename}]\n{doc}")
                    logger.info(f"📚 osp_erweitert: {len(results['documents'][0])} Treffer")
            except Exception as e:
                logger.warning(f"ERWEITERT Query Error: {e}")

        # Kontext zusammenfügen
        context = "\n\n---\n\n".join(context_parts[:20])  # Max 20 Chunks

        if self.valves.DEBUG_MODE:
            logger.info(f"📊 Gesamt: {len(context_parts)} Kontextblöcke, {len(context)} Zeichen")

        return context

    async def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Wird VOR dem LLM aufgerufen.
        Injiziert RAG-Kontext in die User-Nachricht.
        """
        # Lazy Loading - Thread-safe Singleton
        if not _ensure_initialized():
            logger.warning("⚠️ RAG nicht verfügbar - Request unverändert durchreichen")
            return body

        # Messages extrahieren
        messages = body.get("messages", [])
        if not messages:
            return body

        # Letzte User-Nachricht finden
        user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        if not user_message:
            return body

        logger.info(f"🔍 RAG-Query: '{user_message[:50]}...'")

        # RAG-Kontext laden
        context = self._query_chromadb(user_message)

        if not context:
            logger.info("ℹ️ Kein relevanter Kontext gefunden")
            return body

        # System-Prompt mit Kontext erstellen
        system_prompt = f"""Du bist der OSP-KI-Assistent für Rainer Schneider Kabelsatzbau GmbH & Co. KG.

## KONTEXT AUS WISSENSDATENBANK:

{context}

## ANWEISUNGEN:

1. Nutze NUR den obigen Kontext für deine Antwort
2. Bei Unsicherheit: NACHFRAGEN, nicht raten!
3. Confidence-Level (C: XX%) bei Faktenaussagen angeben
4. NULL-FEHLER-POLITIK: Keine erfundenen Daten!
5. Bei MA-Kürzeln: Immer gegen HR_CORE Personalstamm prüfen
6. Kennzeichne deine Antworten mit [OSP]
"""

        # System-Message einfügen oder erweitern
        has_system = False
        for i, msg in enumerate(messages):
            if msg.get("role") == "system":
                messages[i]["content"] = system_prompt + "\n\n--- URSPRÜNGLICHER SYSTEM-PROMPT ---\n" + msg.get("content", "")
                has_system = True
                break

        if not has_system:
            messages.insert(0, {"role": "system", "content": system_prompt})

        body["messages"] = messages

        logger.info(f"✅ RAG-Kontext injiziert: {len(context)} Zeichen für Query: {user_message[:50]}...")

        return body

    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Wird NACH dem LLM aufgerufen.
        Kann für Nachbearbeitung genutzt werden.
        """
        # Aktuell keine Nachbearbeitung nötig
        return body
