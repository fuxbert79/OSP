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
Deployment: /mnt/HC_Volume_104189729/osp/pipelines/osp_rag.py

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

# ═══════════════════════════════════════════════════════════════════════
# KEYWORD-FILTER (PRE-RAG)
# ═══════════════════════════════════════════════════════════════════════
try:
    from keyword_filter import (
        check_keyword_trigger,
        get_filter_stats,
        reload_filter,
        get_keyword_filter
    )
    KEYWORD_FILTER_AVAILABLE = True
    logger.info("✅ Keyword-Filter Modul geladen")
except ImportError as e:
    logger.warning(f"⚠️ Keyword-Filter Modul nicht verfügbar: {e}")
    KEYWORD_FILTER_AVAILABLE = False

    # Fallback-Funktionen
    def check_keyword_trigger(query, path=None): return None
    def get_filter_stats(): return {"verfügbar": False}
    def reload_filter(path=None): return {"verfügbar": False}
    def get_keyword_filter(path=None): return None

# ═══════════════════════════════════════════════════════════════════════
# MA-KÜRZEL PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════
try:
    from ma_preprocessing import expand_ma_query, get_preprocessor
    MA_PREPROCESSING_AVAILABLE = True
    logger.info("✅ MA-Preprocessing Modul geladen")
except ImportError as e:
    logger.warning(f"⚠️ MA-Preprocessing Modul nicht verfügbar: {e}")
    MA_PREPROCESSING_AVAILABLE = False

    # Fallback-Funktion
    def expand_ma_query(query, json_path=None):
        return query

    def get_preprocessor(json_path=None):
        return None

# ═══════════════════════════════════════════════════════════════════════
# QUERY-NORMALISIERUNG
# ═══════════════════════════════════════════════════════════════════════
try:
    from query_normalizer import normalize_query, get_normalizer
    QUERY_NORMALIZER_AVAILABLE = True
    logger.info("✅ Query-Normalizer Modul geladen")
except ImportError as e:
    logger.warning(f"⚠️ Query-Normalizer nicht verfügbar: {e}")
    QUERY_NORMALIZER_AVAILABLE = False

    def normalize_query(query, path=None):
        return query

    def get_normalizer(path=None):
        return None

# ═══════════════════════════════════════════════════════════════════════
# TAG-ROUTER (ChromaDB WHERE-Filter)
# ═══════════════════════════════════════════════════════════════════════
try:
    from tag_router import get_tag_router, extract_tags, get_where_filter
    TAG_ROUTER_AVAILABLE = True
    logger.info("✅ Tag-Router Modul geladen")
except ImportError as e:
    logger.warning(f"⚠️ Tag-Router nicht verfügbar: {e}")
    TAG_ROUTER_AVAILABLE = False

    def extract_tags(query): return []
    def get_where_filter(query): return None
    def get_tag_router(): return None

# ═══════════════════════════════════════════════════════════════════════
# WARTUNGS-LOOKUP (WIM/WIW/Form-Schemas)
# ═══════════════════════════════════════════════════════════════════════
try:
    from wartungs_lookup import (
        get_wartungs_lookup,
        check_wartungs_lookup,
        get_form_schema_for_query,
        get_wartungs_stats,
        reload_wartungs_lookup
    )
    WARTUNGS_LOOKUP_AVAILABLE = True
    logger.info("✅ Wartungs-Lookup Modul geladen")
except ImportError as e:
    logger.warning(f"⚠️ Wartungs-Lookup nicht verfügbar: {e}")
    WARTUNGS_LOOKUP_AVAILABLE = False

    def check_wartungs_lookup(query): return None
    def get_form_schema_for_query(query): return None
    def get_wartungs_stats(): return {"verfügbar": False}
    def reload_wartungs_lookup(): return False
    def get_wartungs_lookup(path=None): return None


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
    ENABLE_KEYWORD_FILTER: bool = Field(default=True, description="Keyword-Trigger Pre-RAG Filter aktivieren")
    ENABLE_MA_PREPROCESSING: bool = Field(default=True, description="MA-Kürzel Query-Expansion aktivieren")
    ENABLE_QUERY_NORMALIZATION: bool = Field(default=True, description="Query-Normalisierung (Tippfehler, Case) aktivieren")
    ENABLE_TAG_ROUTING: bool = Field(default=True, description="Tag-basiertes ChromaDB WHERE-Filter Routing")
    ENABLE_WARTUNGS_LOOKUP: bool = Field(default=True, description="Wartungs-Lookup (WIM/WIW/Form-Schemas) aktivieren")
    MA_KUERZEL_PATH: str = Field(default="/app/backend/data/lookups/ma_kuerzel.json", description="Pfad zur MA-Kürzel JSON")
    LOOKUPS_PATH: str = Field(default="/app/backend/data/lookups", description="Pfad zum Lookups-Verzeichnis")
    DOCUMENTS_PATH: str = Field(default="/app/backend/data/docs", description="Pfad zum Documents-Verzeichnis")
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
        self.ma_preprocessor = None  # MA-Kürzel Preprocessing
        self.keyword_filter = None   # Keyword-Trigger Pre-RAG Filter
        self.keyword_filter_stats = None
        self.query_normalizer = None  # Query-Normalisierung (Tippfehler)
        self.tag_router = None        # Tag-basiertes ChromaDB Routing
        self.wartungs_lookup = None   # WIM/WIW/Form-Schema Lookup
        self.wartungs_lookup_stats = None

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
        # MA-KÜRZEL PREPROCESSING INITIALISIEREN
        # ═══════════════════════════════════════════════════════════════
        if MA_PREPROCESSING_AVAILABLE and self.valves.ENABLE_MA_PREPROCESSING:
            try:
                self.ma_preprocessor = get_preprocessor(self.valves.MA_KUERZEL_PATH)
                if self.ma_preprocessor and self.ma_preprocessor._loaded:
                    logger.info(
                        f"✅ MA-Preprocessing aktiv: "
                        f"{len(self.ma_preprocessor.kuerzel_set)} Kürzel, "
                        f"{len(self.ma_preprocessor.patterns)} Patterns"
                    )
                else:
                    logger.warning("⚠️ MA-Preprocessing konnte nicht initialisiert werden")
            except Exception as e:
                logger.error(f"❌ MA-Preprocessing Fehler: {e}")
                self.ma_preprocessor = None
        else:
            logger.info("ℹ️ MA-Preprocessing deaktiviert")

        # ═══════════════════════════════════════════════════════════════
        # QUERY-NORMALIZER INITIALISIEREN
        # ═══════════════════════════════════════════════════════════════
        if QUERY_NORMALIZER_AVAILABLE and self.valves.ENABLE_QUERY_NORMALIZATION:
            try:
                self.query_normalizer = get_normalizer()
                stats = self.query_normalizer.get_stats()
                if stats.get('verfügbar'):
                    logger.info(
                        f"✅ Query-Normalizer aktiv: "
                        f"{stats['corrections_count']} Korrekturen"
                    )
                else:
                    logger.warning("⚠️ Query-Normalizer: Keine Korrekturen geladen")
            except Exception as e:
                logger.error(f"❌ Query-Normalizer Fehler: {e}")
                self.query_normalizer = None
        else:
            logger.info("ℹ️ Query-Normalizer deaktiviert")

        # ═══════════════════════════════════════════════════════════════
        # KEYWORD-FILTER INITIALISIEREN (PRE-RAG)
        # ═══════════════════════════════════════════════════════════════
        if KEYWORD_FILTER_AVAILABLE and self.valves.ENABLE_KEYWORD_FILTER:
            try:
                self.keyword_filter = get_keyword_filter(Path(self.valves.DOCUMENTS_PATH))
                self.keyword_filter_stats = self.keyword_filter.get_stats()
                if self.keyword_filter_stats.get('verfügbar'):
                    logger.info(
                        f"✅ Keyword-Filter aktiv: "
                        f"{self.keyword_filter_stats['patterns_count']} Patterns, "
                        f"Pfad: {self.keyword_filter_stats['documents_path']}"
                    )
                else:
                    logger.warning("⚠️ Keyword-Filter initialisiert aber Dokumente nicht verfügbar")
            except Exception as e:
                logger.error(f"❌ Keyword-Filter Fehler: {e}")
                self.keyword_filter = None
                self.keyword_filter_stats = {"verfügbar": False, "error": str(e)}
        else:
            logger.info("ℹ️ Keyword-Filter deaktiviert")
            self.keyword_filter_stats = {"verfügbar": False, "reason": "deaktiviert"}

        # ═══════════════════════════════════════════════════════════════
        # TAG-ROUTER INITIALISIEREN (ChromaDB WHERE-Filter)
        # ═══════════════════════════════════════════════════════════════
        if TAG_ROUTER_AVAILABLE and self.valves.ENABLE_TAG_ROUTING:
            try:
                self.tag_router = get_tag_router()
                logger.info(f"✅ Tag-Router aktiv: {len(self.tag_router.compiled_patterns)} TAGs")
            except Exception as e:
                logger.error(f"❌ Tag-Router Fehler: {e}")
                self.tag_router = None
        else:
            logger.info("ℹ️ Tag-Router deaktiviert")

        # ═══════════════════════════════════════════════════════════════
        # WARTUNGS-LOOKUP INITIALISIEREN (WIM/WIW/Form-Schemas)
        # ═══════════════════════════════════════════════════════════════
        if WARTUNGS_LOOKUP_AVAILABLE and self.valves.ENABLE_WARTUNGS_LOOKUP:
            try:
                self.wartungs_lookup = get_wartungs_lookup(Path(self.valves.LOOKUPS_PATH))
                self.wartungs_lookup_stats = get_wartungs_stats()
                if self.wartungs_lookup_stats.get('verfügbar'):
                    logger.info(
                        f"✅ Wartungs-Lookup aktiv: "
                        f"WIM={self.wartungs_lookup_stats['wim']['maschinen']} Maschinen, "
                        f"WIW={self.wartungs_lookup_stats['wiw']['werkzeuge']} Werkzeuge, "
                        f"Forms={self.wartungs_lookup_stats['forms']['formulare']} Formulare"
                    )
                else:
                    logger.warning("⚠️ Wartungs-Lookup: Daten nicht vollständig geladen")
            except Exception as e:
                logger.error(f"❌ Wartungs-Lookup Fehler: {e}")
                self.wartungs_lookup = None
                self.wartungs_lookup_stats = {"verfügbar": False, "error": str(e)}
        else:
            logger.info("ℹ️ Wartungs-Lookup deaktiviert")
            self.wartungs_lookup_stats = {"verfügbar": False, "reason": "deaktiviert"}

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
        # STEP -1: QUERY-NORMALISIERUNG (Tippfehler, Case)
        # ═══════════════════════════════════════════════════════════════
        if QUERY_NORMALIZER_AVAILABLE and self.valves.ENABLE_QUERY_NORMALIZATION:
            normalized = normalize_query(user_message)
            if normalized != user_message.lower():
                logger.info(f"📝 Query normalisiert: '{user_message}' → '{normalized}'")
                user_message = normalized

        # ═══════════════════════════════════════════════════════════════
        # STEP 0: MA-KÜRZEL QUERY-EXPANSION
        # ═══════════════════════════════════════════════════════════════
        original_query = user_message
        if MA_PREPROCESSING_AVAILABLE and self.valves.ENABLE_MA_PREPROCESSING:
            expanded_query = expand_ma_query(user_message, self.valves.MA_KUERZEL_PATH)
            if expanded_query != user_message:
                logger.info(f"🔄 MA-Expansion: '{user_message}' → '{expanded_query[:80]}...'")
                user_message = expanded_query

        # ═══════════════════════════════════════════════════════════════
        # STEP 1: KONTAKT-LOOKUP (VOR RAG!) - verwendet Original-Query
        # ═══════════════════════════════════════════════════════════════
        if LOOKUP_AVAILABLE and self.valves.ENABLE_LOOKUP:
            lookup_result = check_kontakt_lookup(original_query)

            if lookup_result is not None:
                # Treffer! Direkte Antwort ohne RAG
                logger.info("📦 Kontakt-Lookup Treffer - Direkte Antwort")
                return lookup_result

        # ═══════════════════════════════════════════════════════════════
        # STEP 1.3: WARTUNGS-LOOKUP (WIM/WIW) - PRE-RAG
        # Wartungsanfragen für Maschinen/Werkzeuge mit direkter Antwort
        # ═══════════════════════════════════════════════════════════════
        if WARTUNGS_LOOKUP_AVAILABLE and self.valves.ENABLE_WARTUNGS_LOOKUP:
            wartungs_result = check_wartungs_lookup(original_query)

            if wartungs_result is not None:
                # Treffer! Direkte Antwort mit Wartungsdaten/PDFs
                logger.info("🔧 Wartungs-Lookup Treffer - Direkte Antwort")
                return wartungs_result

        # ═══════════════════════════════════════════════════════════════
        # STEP 1.5: KEYWORD-FILTER (PRE-RAG)
        # Kritische Keywords triggern direktes Laden des Zieldokuments
        # ═══════════════════════════════════════════════════════════════
        keyword_context = None
        if KEYWORD_FILTER_AVAILABLE and self.valves.ENABLE_KEYWORD_FILTER and self.keyword_filter:
            keyword_result = self.keyword_filter.get_triggered_context(user_message)

            if keyword_result:
                # Keyword-Trigger! Dokument direkt als Kontext verwenden
                logger.info(
                    f"🎯 Keyword-Trigger: '{keyword_result['trigger']}' → "
                    f"{keyword_result['filename']} (P{keyword_result['priority']})"
                )
                keyword_context = keyword_result

        # ═══════════════════════════════════════════════════════════════
        # STEP 2: NORMALE RAG-VERARBEITUNG (oder Keyword-Context nutzen)
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
            # 2.1 Context zusammenstellen
            # ───────────────────────────────────────────────────────────
            context_parts = []

            # 2.1a KEYWORD-TRIGGER KONTEXT (höchste Priorität)
            if keyword_context:
                keyword_doc = keyword_context['document']
                keyword_file = keyword_context['filename']
                keyword_trigger = keyword_context['trigger']

                # Truncate wenn zu lang
                max_keyword_len = self.valves.MAX_CONTEXT_LENGTH // 2
                if len(keyword_doc) > max_keyword_len:
                    keyword_doc = keyword_doc[:max_keyword_len] + "\n...[TRUNCATED]..."

                context_parts.append(
                    f"[PRIORITÄT: KEYWORD-TRIGGER '{keyword_trigger}']\n"
                    f"[Quelle: {keyword_file} | Score: 1.00 (direkt)]\n{keyword_doc}"
                )
                logger.info(f"📄 Keyword-Context: {keyword_file} ({len(keyword_doc)} Zeichen)")

            # 2.1b RAG KONTEXT (ergänzend)
            rag_context = self._retrieve_context(user_message)

            if rag_context:
                # Wenn Keyword-Context vorhanden, reduziere RAG-Context-Länge
                if keyword_context:
                    remaining_len = self.valves.MAX_CONTEXT_LENGTH - len(context_parts[0])
                    if len(rag_context) > remaining_len:
                        rag_context = rag_context[:remaining_len] + "\n...[TRUNCATED]..."
                context_parts.append(rag_context)
            elif not keyword_context:
                logger.warning("⚠️ Kein relevanter Kontext gefunden")
                context_parts.append("Keine relevanten Dokumente gefunden.")

            # Finaler Context
            context = "\n\n" + "═" * 50 + "\n\n".join(context_parts)

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

            # ─────────────────────────────────────────────────────────────
            # TAG-FILTER FÜR CHROMADB (nur für osp_kern Collection)
            # ─────────────────────────────────────────────────────────────
            where_filter = None
            if self.tag_router and self.valves.ENABLE_TAG_ROUTING:
                where_filter = get_where_filter(query)
                if where_filter:
                    logger.info(f"🏷️ Tag-Filter: {where_filter}")

            for collection_name in collections_priority:
                try:
                    collection = self.chroma_client.get_collection(collection_name)

                    # TAG-Filter nur für osp_kern verwenden
                    current_where = where_filter if collection_name == "osp_kern" else None

                    # Verwende query_embeddings statt query_texts für E5
                    results = collection.query(
                        query_embeddings=query_embedding,
                        n_results=top_k,
                        where=current_where,
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

═══════════════════════════════════════════════════════════════════════
⚠️ NULL-FEHLER-POLITIK (ABSOLUT VERBINDLICH!)
═══════════════════════════════════════════════════════════════════════

1. NIEMALS Informationen erfinden - bei Unsicherheit NACHFRAGEN
2. KEINE erfundenen MA-Kürzel - nur aus HR_CORE_Personalstamm.md
3. KEINE Phantasie-Daten bei Crimp/Werkzeug-Anfragen - VERIFIZIEREN
4. Confidence-Level (C: XX%) bei JEDER Faktenaussage PFLICHT
5. Bei Widersprüchen: TRANSPARENT melden, nicht verschweigen

═══════════════════════════════════════════════════════════════════════
MA-KÜRZEL SYSTEM
═══════════════════════════════════════════════════════════════════════

Mitarbeiter werden mit 2-3 Buchstaben-Kürzeln identifiziert.
Quelle: HR_CORE_Personalstamm.md (OSP_KERN)

SCHLÜSSELPERSONEN:
- AL = Andreas Löhr (QM-Manager & KI-Manager, L3, OSP-EXP)
- CS = Kaufmännischer Geschäftsführer (L3)
- CA = Technischer Geschäftsführer (L3)
- SV = Prokurist (L3)
- MD = Technik/Maschinen (L2)

Bei Fragen wie "Wer ist [KÜRZEL]?" oder "Was macht [KÜRZEL]?":
→ Suche im HR_CORE_Personalstamm.md
→ Gib Name, Funktion, Abteilung, ggf. Kontakt an
→ Bei unbekanntem Kürzel: "Kürzel nicht im Personalstamm gefunden"

═══════════════════════════════════════════════════════════════════════
ANTWORT-FORMAT
═══════════════════════════════════════════════════════════════════════

1. Antworte NUR basierend auf dem bereitgestellten Kontext
2. Strukturiere Antworten klar (Bullet Points, Tabellen wenn sinnvoll)
3. Zitiere die Quelle: [Quelle: Dateiname]
4. Confidence-Level am Ende: (C: XX%)
5. Kennzeichne mit [OSP] am Schluss

CONFIDENCE-SKALA:
- C: 90-100% = Direkt aus Kontext, eindeutig
- C: 70-89%  = Aus Kontext ableitbar, hohe Sicherheit
- C: 50-69%  = Teilweise im Kontext, Interpretation nötig
- C: <50%    = Unzureichender Kontext → NACHFRAGEN!

═══════════════════════════════════════════════════════════════════════
KONTEXT (aus ChromaDB RAG)
═══════════════════════════════════════════════════════════════════════

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
        ma_status = {"verfügbar": False}
        if self.ma_preprocessor and self.ma_preprocessor._loaded:
            ma_status = {
                "verfügbar": True,
                "kuerzel_count": len(self.ma_preprocessor.kuerzel_set),
                "patterns_count": len(self.ma_preprocessor.patterns)
            }

        return {
            "name": self.name,
            "id": self.id,
            "lookup": self.lookup_stats or {"verfügbar": False},
            "keyword_filter": self.keyword_filter_stats or {"verfügbar": False},
            "wartungs_lookup": self.wartungs_lookup_stats or {"verfügbar": False},
            "ma_preprocessing": ma_status,
            "chromadb": self.chroma_client is not None,
            "llm": self.llm_client is not None,
            "embedding_model": "intfloat/multilingual-e5-large" if self.embedding_model else None,
            "embedding_dim": self.embedding_model.get_sentence_embedding_dimension() if self.embedding_model else 0
        }

    def reload_keyword_filter(self) -> dict:
        """
        Lädt den Keyword-Filter neu (nach Pattern-Änderungen).
        Kann über API aufgerufen werden.
        """
        if KEYWORD_FILTER_AVAILABLE:
            self.keyword_filter_stats = reload_filter(Path(self.valves.DOCUMENTS_PATH))
            self.keyword_filter = get_keyword_filter(Path(self.valves.DOCUMENTS_PATH))
            return {
                "success": True,
                "stats": self.keyword_filter_stats
            }
        return {"success": False, "reason": "Keyword-Filter nicht verfügbar"}

    def reload_wartungs_lookup(self) -> dict:
        """
        Lädt den Wartungs-Lookup neu (nach JSON-Updates).
        Kann über API aufgerufen werden.
        """
        if WARTUNGS_LOOKUP_AVAILABLE:
            success = reload_wartungs_lookup()
            self.wartungs_lookup_stats = get_wartungs_stats()
            return {
                "success": success,
                "stats": self.wartungs_lookup_stats
            }
        return {"success": False, "reason": "Wartungs-Lookup nicht verfügbar"}


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
