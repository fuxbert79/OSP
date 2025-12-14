"""
OSP Multi-Layer RAG Pipeline mit Kontakt-Lookup
===============================================

Erweiterte Pipeline mit JSON-basiertem Kontakt-Lookup
für sofortige Antworten bei Werkzeug-Anfragen.

Embedding-Modell: intfloat/multilingual-e5-large (1024 dim)
WICHTIG: E5-Modelle erfordern Präfixe:
- "passage: " für Dokumente (beim Indizieren)
- "query: " für Suchanfragen

Autor: AL
Stand: 2025-12-14
Deployment: /opt/osp/pipelines/osp_rag.py

Architektur:
┌─────────────────────────────────────────┐
│           USER MESSAGE                   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  STEP 1: KONTAKT-LOOKUP (PRE-RAG)       │
│  Pattern: \\d-\\d{6,7}-\\d               │
│  → Bei Treffer: Direkte Antwort         │
└─────────────────┬───────────────────────┘
                  │ Kein Match
                  ▼
┌─────────────────────────────────────────┐
│  STEP 2: RAG-VERARBEITUNG (E5-large)    │
│  → ChromaDB Query → LLM Response        │
└─────────────────────────────────────────┘
"""

import logging
import os
import sys
from pathlib import Path
from typing import Union, Generator, Iterator, List, Optional

from pydantic import BaseModel, Field

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Modul-Pfad hinzufügen für Lookup-Import
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

try:
    from kontakt_lookup import check_kontakt_lookup, get_lookup_stats, reload_lookup_cache
    LOOKUP_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Kontakt-Lookup Modul nicht verfügbar: {e}")
    LOOKUP_AVAILABLE = False

    # Fallback-Funktionen
    def check_kontakt_lookup(msg): return None
    def get_lookup_stats(): return {"verfügbar": False}
    def reload_lookup_cache(): return False


class Valves(BaseModel):
    """Pipeline-Konfigurationsparameter (können in WebUI geändert werden)"""
    ANTHROPIC_API_KEY: str = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""),
        description="Anthropic API Key"
    )
    CHROMADB_HOST: str = Field(default="chromadb", description="ChromaDB Host")
    CHROMADB_PORT: int = Field(default=8000, description="ChromaDB Port")
    ENABLE_LOGGING: bool = Field(default=True, description="Logging aktivieren")
    ENABLE_LOOKUP: bool = Field(default=True, description="Kontakt-Lookup aktivieren")
    MAX_CONTEXT_LENGTH: int = Field(default=16000, description="Max Context-Länge")
    USE_STREAMING: bool = Field(default=True, description="Streaming aktivieren")
    TOP_K: int = Field(default=15, description="Anzahl der RAG-Ergebnisse")


class Pipeline:
    """
    OSP Multi-Layer RAG Pipeline für Schneider Kabelsatzbau.
    
    Features:
    - Kontakt-WKZ Lookup (JSON-basiert, vor RAG)
    - Multi-Layer RAG (KERN → KPL → ERWEITERT)
    - Streaming Support
    - Confidence-Level Tracking
    
    Attributes:
        name: Pipeline-Name für WebUI
        id: Eindeutige Pipeline-ID
        valves: Konfigurationsparameter
    """
    
    def __init__(self):
        """
        Initialize Pipeline.

        ⚠️ WICHTIG: Keine schweren Operationen hier!
        Nutze on_startup() für Resource-Loading.
        """
        self.name = "OSP Multi-Layer RAG"
        self.id = "osp_rag"

        # Pydantic-Valves (können in WebUI geändert werden)
        self.valves = Valves()

        # Lazy-loaded Resources
        self.router = None
        self.llm_client = None
        self.chroma_client = None
        self.lookup_stats = None
        self.embedding_model = None  # E5-large für Query-Embeddings
    
    async def on_startup(self):
        """
        Asynchron lifecycle hook - wird EINMAL beim Container-Start aufgerufen.
        
        Initialisiert:
        - Kontakt-Lookup System
        - ChromaDB Verbindung
        - LLM Client
        """
        logger.info("🚀 OSP RAG Pipeline Starting...")
        
        # ═══════════════════════════════════════════════════════════════
        # LOOKUP-SYSTEM INITIALISIEREN
        # ═══════════════════════════════════════════════════════════════
        if LOOKUP_AVAILABLE and self.valves.ENABLE_LOOKUP:
            self.lookup_stats = get_lookup_stats()
            if self.lookup_stats.get('verfügbar'):
                logger.info(
                    f"✅ Kontakt-Lookup aktiv: "
                    f"{self.lookup_stats['eintraege']} Einträge "
                    f"(Stand: {self.lookup_stats['stand']})"
                )
            else:
                logger.warning("⚠️ Kontakt-Lookup nicht verfügbar - nur RAG-Modus")
        else:
            logger.info("ℹ️ Kontakt-Lookup deaktiviert")
        
        # ═══════════════════════════════════════════════════════════════
        # E5-LARGE EMBEDDING-MODELL LADEN
        # ═══════════════════════════════════════════════════════════════
        try:
            from sentence_transformers import SentenceTransformer

            logger.info("📥 Lade E5-large Embedding-Modell...")
            self.embedding_model = SentenceTransformer(
                'intfloat/multilingual-e5-large',
                device='cpu'
            )
            logger.info(f"✅ E5-large geladen (Dimension: {self.embedding_model.get_sentence_embedding_dimension()})")

        except Exception as e:
            logger.error(f"❌ E5-large Modell konnte nicht geladen werden: {e}")
            self.embedding_model = None

        # ═══════════════════════════════════════════════════════════════
        # CHROMADB INITIALISIEREN
        # ═══════════════════════════════════════════════════════════════
        try:
            import chromadb
            from chromadb.config import Settings

            self.chroma_client = chromadb.HttpClient(
                host=self.valves.CHROMADB_HOST,
                port=self.valves.CHROMADB_PORT,
                settings=Settings(anonymized_telemetry=False)
            )

            # Verbindung testen
            collections = self.chroma_client.list_collections()
            logger.info(f"✅ ChromaDB verbunden: {len(collections)} Collections")

        except Exception as e:
            logger.error(f"❌ ChromaDB Verbindung fehlgeschlagen: {e}")
            self.chroma_client = None
        
        # ═══════════════════════════════════════════════════════════════
        # LLM CLIENT INITIALISIEREN
        # ═══════════════════════════════════════════════════════════════
        try:
            from anthropic import Anthropic
            
            api_key = self.valves.ANTHROPIC_API_KEY
            if api_key:
                self.llm_client = Anthropic(api_key=api_key)
                logger.info("✅ Anthropic Client initialisiert")
            else:
                logger.warning("⚠️ ANTHROPIC_API_KEY nicht gesetzt")
                
        except ImportError:
            logger.warning("⚠️ Anthropic SDK nicht installiert")
        except Exception as e:
            logger.error(f"❌ LLM Client Fehler: {e}")
        
        logger.info("✅ OSP RAG Pipeline Ready")
    
    async def on_shutdown(self):
        """
        Lifecycle hook - wird beim Container-Shutdown aufgerufen.
        Cleanup für Ressourcen.
        """
        logger.info("🛑 OSP RAG Pipeline Shutdown...")
        
        # ChromaDB Verbindung schließen (falls nötig)
        if self.chroma_client:
            try:
                # HttpClient hat kein explizites close()
                pass
            except Exception as e:
                logger.error(f"Shutdown Error: {e}")
        
        logger.info("✅ OSP RAG Pipeline gestoppt")
    
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict,
    ) -> Union[str, Generator, Iterator]:
        """
        Main Processing Method mit Lookup-First-Strategie.
        
        Ablauf:
        1. Kontakt-Lookup prüfen (schnell, deterministisch)
        2. Falls Treffer: Direkte Antwort zurückgeben
        3. Falls kein Treffer: Normale RAG-Verarbeitung
        
        Parameters:
            user_message: Die aktuelle User-Eingabe
            model_id: Das ausgewählte Modell-ID in WebUI
            messages: Komplette Chat-History
            body: Zusätzliche Parameter (OpenAI-compatible)
        
        Returns:
            str oder Generator mit der Antwort
        """
        
        # ═══════════════════════════════════════════════════════════════
        # STEP 1: KONTAKT-LOOKUP (VOR RAG!)
        # ═══════════════════════════════════════════════════════════════
        if LOOKUP_AVAILABLE and self.valves.ENABLE_LOOKUP:
            lookup_result = check_kontakt_lookup(user_message)
            
            if lookup_result is not None:
                # Treffer! Direkte Antwort ohne RAG
                logger.info("📦 Kontakt-Lookup Treffer - Direkte Antwort")
                return lookup_result
        
        # ═══════════════════════════════════════════════════════════════
        # STEP 2: NORMALE RAG-VERARBEITUNG
        # ═══════════════════════════════════════════════════════════════
        logger.info("🔍 Starte RAG-Verarbeitung...")
        
        # Prüfen ob RAG verfügbar
        if not self.chroma_client:
            return self._error_response(
                "ChromaDB nicht verfügbar. Bitte Administrator kontaktieren."
            )
        
        if not self.llm_client:
            return self._error_response(
                "LLM nicht verfügbar. Bitte API-Key prüfen."
            )
        
        try:
            # ───────────────────────────────────────────────────────────
            # 2.1 Context aus ChromaDB abrufen
            # ───────────────────────────────────────────────────────────
            context = self._retrieve_context(user_message)
            
            if not context:
                logger.warning("⚠️ Kein relevanter Kontext gefunden")
                context = "Keine relevanten Dokumente gefunden."
            
            # ───────────────────────────────────────────────────────────
            # 2.2 LLM Response generieren
            # ───────────────────────────────────────────────────────────
            response = self._generate_response(
                user_message=user_message,
                context=context,
                messages=messages,
                body=body
            )
            
            return response
            
        except Exception as e:
            logger.error(f"RAG-Fehler: {e}")
            return self._error_response(str(e))
    
    def _retrieve_context(self, query: str) -> str:
        """
        Ruft relevanten Kontext aus ChromaDB ab.

        Multi-Layer Strategie:
        1. OSP_KERN (Priorität 1)
        2. OSP_KPL (Priorität 2)
        3. OSP_ERWEITERT (Priorität 3)

        WICHTIG: E5-Modelle erfordern "query: " Präfix für Suchanfragen!
        """
        try:
            # ─────────────────────────────────────────────────────────────
            # E5-QUERY EMBEDDING BERECHNEN
            # ─────────────────────────────────────────────────────────────
            if self.embedding_model is None:
                logger.error("❌ E5-Embedding-Modell nicht verfügbar!")
                return ""

            # E5-Modelle erfordern "query: " Präfix für Suchanfragen
            query_with_prefix = f"query: {query}"
            query_embedding = self.embedding_model.encode(
                [query_with_prefix],
                normalize_embeddings=True
            ).tolist()

            logger.debug(f"Query-Embedding berechnet für: '{query[:50]}...'")

            # ─────────────────────────────────────────────────────────────
            # MULTI-LAYER SUCHE
            # ─────────────────────────────────────────────────────────────
            collections_priority = [
                "osp_kern",
                "osp_kpl",
                "osp_erweitert"
            ]

            all_results = []
            top_k = self.valves.TOP_K

            for collection_name in collections_priority:
                try:
                    collection = self.chroma_client.get_collection(collection_name)

                    # Verwende query_embeddings statt query_texts für E5
                    results = collection.query(
                        query_embeddings=query_embedding,
                        n_results=top_k,
                        include=["documents", "metadatas", "distances"]
                    )

                    num_ids = len(results.get('ids', [[]])[0])
                    has_docs = bool(results.get('documents') and results['documents'][0])
                    logger.info(f"  {collection_name}: {num_ids} IDs, docs={has_docs}")

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

                except Exception as e:
                    logger.warning(f"Collection {collection_name} nicht verfügbar: {e}")
                    continue

            logger.info(f"  Gesamt all_results: {len(all_results)}")

            # Nach Distanz sortieren (niedrigste = beste Übereinstimmung)
            all_results.sort(key=lambda x: x['distance'])

            # Top-Ergebnisse für Kontext zusammenstellen
            context_parts = []
            max_length = self.valves.MAX_CONTEXT_LENGTH
            current_length = 0

            logger.debug(f"  Baue Kontext aus {len(all_results)} Ergebnissen (max_length={max_length})")

            for result in all_results[:top_k]:
                doc = result['document']
                filename = result['filename']
                score = 1 - result['distance']  # Cosine similarity

                if doc is None or len(doc) == 0:
                    continue
                if current_length + len(doc) > max_length:
                    if current_length == 0:
                        # Erstes Dokument ist zu groß - truncate
                        truncated = doc[:max_length - 200] + "\n...[TRUNCATED]..."
                        context_parts.append(f"[Quelle: {filename} | Score: {score:.2f}]\n{truncated}")
                        current_length = len(truncated)
                    break

                context_parts.append(f"[Quelle: {filename} | Score: {score:.2f}]\n{doc}")
                current_length += len(doc)

            logger.info(f"📚 {len(context_parts)} Kontextblöcke ({current_length} Zeichen)")

            return "\n\n---\n\n".join(context_parts)

        except Exception as e:
            logger.error(f"Context Retrieval Error: {e}")
            return ""
    
    def _generate_response(
        self,
        user_message: str,
        context: str,
        messages: List[dict],
        body: dict
    ) -> str:
        """
        Generiert LLM Response mit Kontext.
        """
        system_prompt = """Du bist der OSP-Assistent für Rainer Schneider Kabelsatzbau GmbH & Co. KG.

WICHTIGE REGELN:
1. Antworte NUR basierend auf dem bereitgestellten Kontext
2. Gib Confidence-Level an: (C: XX%)
3. Bei Unsicherheit: Nachfragen statt raten
4. Kennzeichne Antworten mit [OSP]
5. NULL-FEHLER-POLITIK: Keine erfundenen Daten!

KONTEXT:
{context}
""".format(context=context)
        
        try:
            response = self.llm_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=body.get("max_tokens", 2000),
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"LLM Generation Error: {e}")
            raise
    
    def _error_response(self, error_msg: str) -> str:
        """
        Formatiert eine Fehler-Antwort im OSP-Standard.
        """
        return f"""❌ **Fehler bei der Verarbeitung**

{error_msg}

**Mögliche Lösungen:**
1. Anfrage neu formulieren
2. Administrator kontaktieren (AL)

(C: 0%) [OSP-Error]"""
    
    # ═══════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════
    
    def reload_lookup(self) -> dict:
        """
        Lädt die Lookup-Daten neu (nach JSON-Update).
        Kann über API aufgerufen werden.
        """
        if LOOKUP_AVAILABLE:
            success = reload_lookup_cache()
            self.lookup_stats = get_lookup_stats()
            return {
                "success": success,
                "stats": self.lookup_stats
            }
        return {"success": False, "reason": "Lookup nicht verfügbar"}
    
    def get_status(self) -> dict:
        """
        Gibt den aktuellen Pipeline-Status zurück.
        """
        return {
            "name": self.name,
            "id": self.id,
            "lookup": self.lookup_stats or {"verfügbar": False},
            "chromadb": self.chroma_client is not None,
            "llm": self.llm_client is not None,
            "embedding_model": "intfloat/multilingual-e5-large" if self.embedding_model else None,
            "embedding_dim": self.embedding_model.get_sentence_embedding_dimension() if self.embedding_model else 0
        }


# Pipeline-Instanz für Open WebUI
pipeline = Pipeline()


# ═══════════════════════════════════════════════════════════════════════
# STANDALONE TEST
# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("=== OSP RAG Pipeline Test ===\n")
        
        # Startup
        await pipeline.on_startup()
        
        # Status
        print(f"Status: {pipeline.get_status()}\n")
        
        # Test-Anfragen
        test_queries = [
            "Welches WKZ für 0-0350415-1?",  # Lookup
            "Zeige mir den Komax Alpha 530",  # RAG
        ]
        
        for query in test_queries:
            print(f"Query: {query}")
            result = pipeline.pipe(query, "osp_rag", [], {})
            print(f"Result:\n{result}\n")
            print("-" * 50)
        
        # Shutdown
        await pipeline.on_shutdown()
    
    asyncio.run(test())
