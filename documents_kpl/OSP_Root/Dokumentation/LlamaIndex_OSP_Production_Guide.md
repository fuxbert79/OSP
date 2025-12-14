# LlamaIndex Production Guide - OSP Multi-Layer RAG

## Metadata

- **Version**: LlamaIndex 0.14.10 / 0.15.x
- **Use-Case**: Multi-Collection RAG mit ChromaDB + CPU-only Embedding
- **Deployment**: Docker auf Hetzner (Ubuntu 24, 8GB RAM)
- **Last Updated**: Dezember 2025
- **Target Audience**: Production DevOps & Backend Engineers

---

## Table of Contents

1. [Production Setup](#1-production-setup)
2. [Performance Optimization](#2-performance-optimization)
3. [Multi-Index Patterns](#3-multi-index-patterns)
4. [Troubleshooting Guide](#4-troubleshooting-guide)
5. [Code Examples](#5-code-examples)
6. [Best Practices Checklist](#6-best-practices-checklist)
7. [API Reference](#7-api-reference)
8. [Appendix: Migration Guide](#appendix-migration-guide)

---

## 1. Production Setup

### 1.1 Settings API - Globale Konfiguration (v0.10+)

Das **Settings-Objekt** ersetzt das deprecated `ServiceContext` und bietet zentrale, globale Konfiguration für alle LlamaIndex-Module.

```python
from llama_index.core import Settings
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# === GLOBAL SETTINGS KONFIGURATION ===
# Alle LLM und Embedding Calls nutzen diese Settings automatisch

# 1. LLM Configuration
Settings.llm = Anthropic(
    model="claude-sonnet-4-20250514",
    api_key="sk-ant-...",  # Besser: aus Umgebungsvariable
    temperature=0.1,  # Für RAG: niedrig halten
    max_tokens=2048
)

# 2. Embedding Model (CPU-optimiert für 8GB RAM)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    # Wichtig: Model wird beim ersten Call geladen (lazy loading)
    cache_folder="./models"  # Lokal cachen
)

# 3. Text Splitting (Chunking)
Settings.chunk_size = 512  # Optimal für BAAI/bge-small (8-15KB Dokumente)
Settings.chunk_overlap = 100  # 20% Overlap für Kontextkontinuität

# 4. Token Counter (für Claude)
from llama_index.core.callbacks import TokenCountingHandler

token_counter = TokenCountingHandler()
Settings.callback_manager.add_handler(token_counter)

# Optional: Tokenizer für präzises Zählen
# Settings.tokenizer = encoding.encode_ordinary  # tiktoken equivalent

print("✓ Global Settings konfiguriert")
```

**Wichtig**: Settings ist ein **Singleton**. Nach Initialisierung wirken sie automatisch auf alle Indices und Query Engines, die danach erstellt werden.

### 1.2 ChromaDB Integration mit VectorStoreIndex

ChromaDB speichert Embeddings persistent, sodass sie nach Container-Restart verfügbar bleiben.

```python
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import Document

# === PERSISTENT CHROMADB SETUP ===

# 1. ChromaDB Client (Persistent Storage)
chroma_client = chromadb.PersistentClient(
    path="./chroma_db",  # Persistiert auf Disk
    settings=chromadb.Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# 2. Separate Collections für Multi-Layer Setup
collection_kern = chroma_client.get_or_create_collection(
    name="osp_kern",
    metadata={"description": "Kern-Dokumentation (12 Docs)"}
)

collection_erweitert = chroma_client.get_or_create_collection(
    name="osp_erweitert",
    metadata={"description": "Erweiterte Ressourcen (39 Docs)"}
)

# 3. VectorStore für jede Collection
vector_store_kern = ChromaVectorStore(chroma_collection=collection_kern)
vector_store_erweitert = ChromaVectorStore(chroma_collection=collection_erweitert)

# 4. Storage Context mit Vector Stores
storage_context_kern = StorageContext.from_defaults(
    vector_store=vector_store_kern
)
storage_context_erweitert = StorageContext.from_defaults(
    vector_store=vector_store_erweitert
)

# 5. Indices aus Vector Stores laden
# WICHTIG: embed_model MUSS mit dem bei Indexierung verwendeten Model übereinstimmen
index_kern = VectorStoreIndex.from_vector_store(
    vector_store=vector_store_kern,
    storage_context=storage_context_kern
)
index_erweitert = VectorStoreIndex.from_vector_store(
    vector_store=vector_store_erweitert,
    storage_context=storage_context_erweitert
)

print(f"✓ Indices geladen: kern={index_kern}, erweitert={index_erweitert}")
```

**Kritisch**: Embedding-Dimension muss konstant sein. BAAI/bge-small erzeugt 384-dimensionale Vektoren. Ein Wechsel auf andere Models verursacht Fehler (siehe Troubleshooting).

### 1.3 Query Engine Konfiguration

```python
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import ResponseSynthesizer

# === QUERY ENGINE PRO COLLECTION ===

# 1. Retriever mit optimiertem top-k
retriever_kern = index_kern.as_retriever(
    similarity_top_k=3,  # Reduziert auf nur beste 3 Nodes
    # vector_store_query_mode="default" (similarity ist default)
)

# 2. Response Synthesizer (compact für Speed)
synthesizer = ResponseSynthesizer.from_defaults(
    response_mode="compact",  # Schneller als tree_summarize
    num_workers=4  # Parallel processing
)

# 3. Query Engine kombiniert Retriever + Synthesizer
query_engine_kern = RetrieverQueryEngine.from_args(
    retriever=retriever_kern,
    response_synthesizer=synthesizer,
    verbose=False  # Für Production
)

# === QUERY AUSFÜHREN ===
query_text = "Was ist das OSP Kern-System?"
response = query_engine_kern.query(query_text)

print(f"Response: {response.response}")
print(f"Sources: {[n.node.get_content() for n in response.source_nodes]}")
```

**Response Modes Vergleich**:

| Mode | LLM Calls | Speed | Quality | Use Case |
|------|-----------|-------|---------|----------|
| `compact` | 1-2 | ⚡⚡⚡ | Gut | Einfache Fragen, Low-Latency |
| `refine` | k (pro Node) | ⚡⚡ | Sehr Gut | Komplexe Fragen mit viel Context |
| `tree_summarize` | log(k) | ⚡⚡ | Sehr Gut | Längere Dokumente |
| `simple_summarize` | 1 | ⚡⚡⚡ | Gut | Zeitkritisch |

**Für OSP Multi-Layer mit 8GB RAM**: `compact` oder `simple_summarize` bevorzugen.

### 1.4 Anthropic LLM Integration

```python
import os
from llama_index.llms.anthropic import Anthropic

# === ANTHROPIC API SETUP ===

# 1. API Key aus Umgebung (Docker: via environment variable)
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY env variable nicht gesetzt!")

# 2. LLM Initialisierung mit Production-Settings
llm = Anthropic(
    model="claude-sonnet-4-20250514",
    api_key=api_key,
    temperature=0.1,  # Niedrig für faktische Accuracy
    max_tokens=2048,
    # Optional: für Prompt Caching (spart Tokens & Latenz)
    # cache_control=[{"type": "ephemeral", "budget_tokens": 1024}],
    timeout=30  # Timeout für API Calls
)

Settings.llm = llm

# 3. Streaming Support für Real-time Responses
async def stream_query(query_text):
    """Streaming Query für bessere UX"""
    query_engine = index_kern.as_query_engine(
        streaming=True  # Aktiviert Streaming
    )
    
    response = query_engine.query(query_text)
    
    # Streaming Response iterieren
    for chunk in response.response_gen:
        yield chunk

# 4. Token Counting für Cost Control
from llama_index.core.callbacks import TokenCountingHandler

token_counter = TokenCountingHandler()
Settings.callback_manager.add_handler(token_counter)

# Nach Query:
print(f"Prompt tokens: {token_counter.prompt_token_count}")
print(f"Completion tokens: {token_counter.completion_token_count}")
```

**Wichtig**: Claude Sonnet 4 hat 200k Context Window. Bei 51 Dokumenten mit 512 Token Chunks kann man problemlos 10+ Nodes retrievenohne Token Limit zu überschreiten.

### 1.5 Memory Management für 8GB RAM

```python
import gc
from psutil import virtual_memory

def check_memory_usage():
    """Monitoring für 8GB RAM Constraint"""
    mem = virtual_memory()
    usage_percent = mem.percent
    
    # Alert wenn über 70%
    if usage_percent > 70:
        print(f"⚠️ Memory Warning: {usage_percent}%")
        gc.collect()
        
        # Optional: unload embed_model
        if hasattr(Settings.embed_model, 'device'):
            # Modell auf CPU zurück, nicht im VRAM
            pass
    
    return usage_percent

# === EMBEDDING CACHING ===
# Wichtig: Embeddings werden nur einmal bei Indexierung generiert,
# bei Query nur die Query-Embedding berechnet

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    # CPU-only (keine GPU Anforderungen)
    device="cpu",
    # Modell wird nach Gebrauch entladen
    cache_folder="./models"
)

# Nach erfolgreicher Indexierung: 45MB RAM für Modell selbst
# Query Embedding: ~5-10ms für einzelne Query
```

**RAM-Optimierungen**:
- ChromaDB mit PersistentClient: Embeddings bleiben auf Disk, nicht im RAM
- Settings.embed_model wird lazy geladen (nur beim ersten Use)
- Kleinere Modelle (bge-small statt bge-base): 45M vs 110M Parameters

---

## 2. Performance Optimization

### 2.1 Query Caching Strategien

#### A. In-Memory LRU Cache (Einfach, für Single Instance)

```python
from llama_index.core.instrumentation import DispatcherSpan
from functools import lru_cache
import hashlib

class QueryCache:
    """LRU Query Cache für häufige Queries"""
    
    def __init__(self, max_size=100, ttl=3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.access_times = {}
    
    def _hash_query(self, query_text: str, collection: str) -> str:
        """Query + Collection als Cache Key"""
        key = f"{collection}:{query_text}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, query_text: str, collection: str):
        """Cache Hit prüfen"""
        key = self._hash_query(query_text, collection)
        
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        
        return None
    
    def set(self, query_text: str, collection: str, response):
        """Response cachen"""
        key = self._hash_query(query_text, collection)
        
        # LRU: wenn voll, ältesten Entry entfernen
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = response
        self.access_times[key] = time.time()

# === USAGE ===
query_cache = QueryCache(max_size=100)

def query_with_cache(query_text: str, collection: str):
    # Erst Cache prüfen
    cached = query_cache.get(query_text, collection)
    if cached:
        print("✓ Cache HIT")
        return cached
    
    # Sonst Query Engine
    print("→ Cache MISS, querying...")
    query_engine = index_kern.as_query_engine()
    response = query_engine.query(query_text)
    
    # Cachen
    query_cache.set(query_text, collection, response)
    
    return response
```

**Erwartete Cache Hit Rate**: 40-60% bei typischen Support-Szenarien.

#### B. Redis Semantic Cache (Multi-Instance)

```python
import redis
import json
from llama_index.core.cache import RedisCache

# === REDIS SETUP ===
redis_client = redis.Redis(
    host="localhost",  # Docker: service-name
    port=6379,
    db=0,
    decode_responses=True
)

redis_cache = RedisCache(redis_client)

# Settings nutzen Cache automatisch
Settings.cache = redis_cache

# === SEMANTIC CACHING ===
# Ähnliche Queries (nicht nur exakte) triggern Cache Hit

from llama_index.core.embeddings import OpenAIEmbedding

# Mit Semantic Similarity (kostet etwas mehr RAM)
semantic_cache = RedisCache(
    redis_client=redis_client,
    similarity_threshold=0.8,  # 80% Similarity = Hit
    embed_model=Settings.embed_model
)

# Beispiel: Diese Queries holen Cache:
# - "Was ist OSP?" (exakt)
# - "Erklär mir OSP" (semantisch ähnlich)
# - "OSP Definition" (semantisch ähnlich)
```

**Mit Redis**:
- Multi-Container Persistence
- TTL automatisch (nach 24h ablaufen)
- Shared Cache zwischen Instances
- ~10-50ms Redis Latenz (vs. ~500ms Query)

### 2.2 Embedding Caching

Embeddings werden **nur bei Indexierung generiert**, nicht bei Queries. Diese bereits im ChromaDB gespeichert.

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

# === EMBEDDING MODEL CACHING ===

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./models",  # Lokal speichern
    # Bei Docker: Volume mount für Persistenz
)

# Nach erste Indexierung:
# - Modell in cache_folder: ~45MB
# - Bei neuem Container: model wird von local cache geladen (schnell!)
# - Ohne cache: würde von HuggingFace Hub heruntergeladen (langsam!)

# === DOCKER VOLUME FÜR MODELS ===
# Dockerfile:
# VOLUME ["./models"]
# 
# docker-compose.yml:
# volumes:
#   - ./models:/app/models

print(f"Embed model cache: {os.path.expanduser('~')}/.cache/huggingface")
```

**Embedding Speed**:
- Erste Indexierung (51 Docs × 512 Tokens): ~3-5 Sekunden
- Query Embedding: ~5-10ms pro Query
- Mit CPU-Optimierung (IPEX): bis 4.5x schneller

### 2.3 Batch Processing & Async Queries

```python
import asyncio
from llama_index.core.query_engine import AsyncQueryEngine

# === ASYNCHRONOUS QUERY ENGINE ===

async def batch_query_async(queries: list[str], collection: str):
    """Multiple Queries parallel ausführen"""
    
    if collection == "kern":
        query_engine = index_kern.as_query_engine()
    else:
        query_engine = index_erweitert.as_query_engine()
    
    # Parallel Queries
    tasks = [
        query_engine.aquery(q)  # Async variant
        for q in queries
    ]
    
    responses = await asyncio.gather(*tasks)
    
    return responses

# === USAGE ===
async def main():
    queries = [
        "Was ist OSP?",
        "Wie funktioniert die Architektur?",
        "Welche Integrationen existieren?"
    ]
    
    # ~30s sequenziell → ~12s parallel (mit 3 Queries)
    results = await batch_query_async(queries, "kern")
    
    for i, result in enumerate(results):
        print(f"Query {i+1}: {result.response}")

asyncio.run(main())
```

**Performance Impact**:
- 1 Query: 12-15s
- 3 Queries sequenziell: 36-45s
- 3 Queries parallel: 12-15s (nur erste Latenz!)

### 2.4 Response Streaming

Streaming bricht LLM-Response in Chunks, sodass der User sofort Feedback erhält (Progressive Enhancement).

```python
# === STREAMING SETUP ===

def stream_response(query_text: str):
    """Generator für Streaming Responses"""
    
    query_engine = index_kern.as_query_engine(
        streaming=True  # Wichtig!
    )
    
    response = query_engine.query(query_text)
    
    # Response ist Generator
    for chunk in response.response_gen:
        yield chunk

# === FASTAPI INTEGRATION ===
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/query/{query_text}")
async def query_endpoint(query_text: str):
    """Streaming Query Endpoint"""
    
    def generate():
        for chunk in stream_response(query_text):
            yield chunk
    
    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

# Aus Client-Perspektive:
# - Erstes Chunk: ~2-3s (Retrieval)
# - Rest: alle 500ms ein Chunk
# - User sieht progressive Response aufbauend
```

---

## 3. Multi-Index Patterns

### 3.1 RouterQueryEngine für Query Routing

RouterQueryEngine sendet Query an den besten Index basierend auf Inhalt.

```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.selectors import LLMSingleSelector, LLMMultiSelector

# === INDEX TOOLS DEFINIEREN ===

tool_kern = QueryEngineTool.from_defaults(
    query_engine=query_engine_kern,
    name="OSP_Kern",
    description="Kern-Dokumentation für OSP System (technische Spezifikationen, Architektur)"
)

tool_erweitert = QueryEngineTool.from_defaults(
    query_engine=query_engine_erweitert,
    name="OSP_Erweitert",
    description="Erweiterte Ressourcen (Best Practices, Integrations-Guides, FAQs)"
)

# === ROUTER ENGINE ERSTELLEN ===

# Option A: Single Selector (Query → 1 Index)
router_engine_single = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(
        llm=Settings.llm
    ),
    query_engine_tools=[tool_kern, tool_erweitert],
    verbose=True
)

# Option B: Multi Selector (Query → mehrere Indices, kombiniere Responses)
router_engine_multi = RouterQueryEngine(
    selector=LLMMultiSelector.from_defaults(
        llm=Settings.llm
    ),
    query_engine_tools=[tool_kern, tool_erweitert],
    verbose=True
)

# === USAGE ===

# Query 1: Technische Frage → Routed zu "Kern"
response = router_engine_single.query("Wie ist die OSP Architektur aufgebaut?")

# Query 2: Best Practice Frage → Routed zu "Erweitert"
response = router_engine_single.query("Welche Best Practices für OSP Deployment?")

# Query 3: Umfassende Frage → Routed zu BEIDEN
response = router_engine_multi.query("Gib mir kompletten Überblick über OSP")

print(response)
```

**How It Works**:
1. LLM analysiert Query
2. LLM generiert Score für jeden Tool (0-1)
3. Single: Nimmt höchsten Score
4. Multi: Nimmt alle über Threshold (z.B. >0.5)
5. Responses werden kombiniert

### 3.2 Auto-Retrieval mit Metadata Filtering

Auto-Retriever nutzt LLM um automatisch Metadata Filters zu generieren.

```python
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo

# === METADATA SCHEMA DEFINIEREN ===

vector_store_info = VectorStoreInfo(
    content_info="OSP Dokumentation",
    metadata_info=[
        MetadataInfo(
            name="doc_type",
            type="str",
            description="Art des Dokuments: technical_spec, guide, faq, api_reference"
        ),
        MetadataInfo(
            name="component",
            type="str",
            description="OSP Komponente: core, integration, deployment, monitoring"
        ),
        MetadataInfo(
            name="created_date",
            type="date",
            description="Erstellungsdatum des Dokuments (YYYY-MM-DD)"
        ),
        MetadataInfo(
            name="version",
            type="float",
            description="Software-Version dieses Dokuments (z.B. 1.0, 2.1)"
        )
    ]
)

# === AUTO-RETRIEVER ===

auto_retriever = VectorIndexAutoRetriever(
    index=index_kern,
    vector_store_info=vector_store_info,
    similarity_top_k=3,
    empty_query_top_k=10,  # Fallback wenn keine Filter
    verbose=True
)

# === USAGE ===

# Query 1: "API Dokumentation Version 2.0"
# LLM generiert automatisch Filter:
# {doc_type: "api_reference", version: 2.0}
nodes = auto_retriever.retrieve("API Dokumentation Version 2.0")

# Query 2: "Welche Guides gibt es für Deployment?"
# LLM generiert Filter:
# {doc_type: "guide", component: "deployment"}
nodes = auto_retriever.retrieve("Welche Guides für Deployment nach 2024?")
# Zusätzlich Filter: created_date > 2024-01-01
```

**Requirement**: Alle Dokumente müssen mit Metadata versehen sein (beim Indexieren).

### 3.3 Hybrid Search (Vector + Keyword)

Kombiniert semantische Vector Similarity mit Keyword Matching.

```python
from llama_index.core.retrievers import BM25Retriever, QueryFusionRetriever

# === BM25 (KEYWORD) RETRIEVER ===

bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,  # Alle Nodes aus Index
    similarity_top_k=3
)

# === VECTOR RETRIEVER ===

vector_retriever = index_kern.as_retriever(
    similarity_top_k=3
)

# === FUSION: KOMBINIERE BEIDE ===

fusion_retriever = QueryFusionRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    llm=Settings.llm,
    mode="reciprocal_rerank",  # RRF scoring
    similarity_top_k=5,
    num_queries=1,  # Generiere zusätzliche Queries? (0 = Nein)
    use_async=True
)

# === QUERY ENGINE MIT FUSION ===

hybrid_query_engine = index_kern.as_query_engine(
    retriever=fusion_retriever
)

response = hybrid_query_engine.query("OSP Monitoring einrichten")

# Nodes sind jetzt kombiniert aus:
# - Vector Similarity: "monitoring", "metrics"
# - Keyword Match: "monitoring" keyword explicit
# - Better Coverage!
```

**Use Cases**:
- Suchbegriffe, die exakt im Text vorkommen (Keyword)
- Konzeptuelle Suche ("wie funktioniert X", Vector)
- Kombination = Best of Both Worlds

---

## 4. Troubleshooting Guide

### 4.1 API & Installation Fehler

#### FEHLER: `ModuleNotFoundError: llama_index.core`

**Symptom**: 
```
ModuleNotFoundError: No module named 'llama_index.core'
```

**Root Cause**: 
Version-Mismatch oder falsche Import-Pfade. LlamaIndex v0.10+ änderte auf `llama_index.core`.

**Lösung**:

```bash
# Aktualisieren auf mindestens v0.10.0
pip install --upgrade llama-index-core llama-index

# Überprüfe Version
python -c "import llama_index; print(llama_index.__version__)"

# Falls weiterhin Problem: Reinstall in venv
python -m venv env
source env/bin/activate
pip install llama-index==0.14.10 \
  llama-index-embeddings-huggingface \
  llama-index-vector-stores-chroma \
  llama-index-llms-anthropic
```

**Code-Beispiel**:

```python
# ❌ FALSCH (alt)
from llama_index import ServiceContext, VectorStoreIndex

# ✅ RICHTIG (neu)
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.anthropic import Anthropic
```

**Prävention**: Im Requirements.txt explizit pinnen:
```
llama-index-core>=0.14.0,<0.15.0
llama-index-embeddings-huggingface>=0.1.0
llama-index-vector-stores-chroma>=0.1.0
llama-index-llms-anthropic>=0.1.0
```

---

#### FEHLER: `DeprecationWarning: ServiceContext`

**Symptom**:
```
DeprecationWarning: ServiceContext is deprecated. Use Settings instead.
```

**Root Cause**: 
Code nutzt altes ServiceContext Pattern.

**Lösung**:

```python
# ❌ FALSCH (deprecated)
from llama_index import ServiceContext
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model
)
index = VectorStoreIndex.from_documents(
    docs,
    service_context=service_context
)

# ✅ RICHTIG (neu)
from llama_index.core import Settings
Settings.llm = llm
Settings.embed_model = embed_model

# Index automatisch nutzt Settings
index = VectorStoreIndex.from_documents(docs)
```

**Siehe auch**: [Appendix: Migration Guide](#appendix-migration-guide)

---

#### FEHLER: `Anthropic API Authentication Errors`

**Symptom**:
```
AuthenticationError: Invalid API key provided. Get an API key at https://console.anthropic.com
```

**Root Cause**:
- API Key ungültig, abgelaufen oder nicht gesetzt
- Key nicht mit `sk-ant-api03-` präfix

**Lösung**:

```python
import os

# ❌ Falsch: Hardcoded
llm = Anthropic(api_key="sk-ant-xxx")

# ✅ Richtig: Aus Environment
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Set ANTHROPIC_API_KEY environment variable")

llm = Anthropic(
    api_key=api_key,
    model="claude-sonnet-4-20250514"
)
```

**Docker Setup**:

```dockerfile
# Dockerfile
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

```bash
# Docker Run
docker run -e ANTHROPIC_API_KEY=sk-ant-... myapp
```

**Prävention**:
1. API Key in Anthropic Console erzeugen
2. Key muss mit `sk-ant-api03-` beginnen
3. Alle Requests müssen diesen Key enthalten
4. Rate limits beachten (varies by plan)

---

### 4.2 Query Execution Fehler

#### FEHLER: `Slow Response Times (>30s)`

**Symptom**:
```
Query dauert 30+ Sekunden, manchmal mehrere Minuten
```

**Root Cause** (in Reihenfolge der Wahrscheinlichkeit):
1. Zu viele Nodes retrieving (similarity_top_k zu hoch)
2. Response Mode "tree_summarize" mehrere LLM Calls
3. Embedding Generation zu langsam (CPU-only, keine GPU)
4. Netzwerk-Latenz zu ChromaDB oder Anthropic API
5. Memory Thrashing (8GB RAM voll, Swap-Usage)

**Lösung**:

```python
# 1. Reduziere similarity_top_k
retriever = index_kern.as_retriever(similarity_top_k=3)  # War vielleicht 10+

# 2. Nutze "compact" statt "tree_summarize"
from llama_index.core.response_synthesizers import ResponseSynthesizer

synthesizer = ResponseSynthesizer.from_defaults(
    response_mode="compact"  # Schneller
)

# 3. Monitoring: Was dauert am längsten?
from llama_index.core.callbacks import LlamaDebugHandler

debug_handler = LlamaDebugHandler()
Settings.callback_manager.add_handler(debug_handler)

response = query_engine.query("test")

# Output zeigt breakdown:
# - Retrieve: X.XXs
# - Synthesize: X.XXs
# - Total: X.XXs

# 4. Query Caching (reduziert repeating queries zu <100ms)
query_cache = QueryCache(max_size=100)

# 5. Memory Check
from psutil import virtual_memory
mem = virtual_memory()
print(f"Memory usage: {mem.percent}%")
if mem.percent > 80:
    gc.collect()  # Force garbage collection
```

**Code-Beispiel für Profiling**:

```python
import time

def profile_query(query_text):
    """Detailliertes Timing pro Phase"""
    
    start = time.time()
    
    # Phase 1: Retrieve
    retrieve_start = time.time()
    retriever = index_kern.as_retriever(similarity_top_k=3)
    nodes = retriever.retrieve(query_text)
    retrieve_time = time.time() - retrieve_start
    
    # Phase 2: Synthesize
    synthesize_start = time.time()
    response = query_engine_kern.query(query_text)
    synthesize_time = time.time() - synthesize_start
    
    total = time.time() - start
    
    print(f"Retrieve: {retrieve_time:.2f}s")
    print(f"Synthesize: {synthesize_time:.2f}s")
    print(f"Total: {total:.2f}s")
    
    return response

response = profile_query("Was ist OSP?")
```

**Prävention**:
- [ ] Immer top-k begrenzen (max. 5)
- [ ] "compact" mode als Default
- [ ] Query Caching für bekannte Fragen
- [ ] Monitoring von Response Times einbauen

---

#### FEHLER: `Empty/No Results trotz vorhandener Daten`

**Symptom**:
```
retriever.retrieve("test") returns []
```

**Root Cause**:
1. ChromaDB Collection ist leer (Indexierung hat nicht funktioniert)
2. Falsche Collection Name
3. Embedding Dimension Mismatch
4. similarity_top_k=0 oder similarity_threshold zu hoch

**Lösung**:

```python
# 1. Überprüfe ob Collection Daten enthält
collection = chroma_client.get_collection("osp_kern")
count = collection.count()
print(f"Documents in collection: {count}")  # Sollte > 0 sein

# 2. Indexierung neu durchführen, falls nötig
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context_kern,
    show_progress=True  # Siehe Fortschritt
)

# 3. Teste Retriever
retriever = index.as_retriever(similarity_top_k=5)
nodes = retriever.retrieve("test query")

if not nodes:
    # Debug: Alle Nodes abrufen
    all_nodes = retriever.retrieve("dummy")  # Mit falschem Query
    if len(all_nodes) == 0:
        print("ERROR: No nodes in vector store!")
    else:
        print(f"OK: {len(all_nodes)} nodes total")

# 4. Überprüfe Embedding Dimension
embed_model = Settings.embed_model
test_embedding = embed_model.get_text_embedding("test")
print(f"Embedding dimension: {len(test_embedding)}")  # Sollte 384 sein (BAAI/bge-small)

# ChromaDB collection dimension
collection_info = collection.metadata
print(f"Collection metadata: {collection_info}")
```

**Prävention**:
- [ ] Nach Indexierung: `count()` überprüfen
- [ ] Embedding Model konstant halten (nie wechseln ohne Reindex)
- [ ] similarity_top_k >= 1
- [ ] Similarity Threshold kontrollieren

---

#### FEHLER: `Hallucinations (LLM generiert trotz fehlender Daten)`

**Symptom**:
```
Response: "OSP nutzt Machine Learning für..."
(Aber keine ML im Retrieved Context vorhanden)
```

**Root Cause**: 
LLM generiert plausible, aber falsche Antworten basierend auf Training, nicht auf Retrieved Context.

**Lösung**:

```python
# 1. Strikte Prompting: Erzwinge "Unknown" Responses
from llama_index.core.prompts import PromptTemplate

qa_prompt_str = """\
Context information is below.
---------------------
{context_str}
---------------------
Query: {query_str}

Instructions:
- Answer ONLY based on the context provided
- If the context does not contain the answer, respond: "I don't have information about this in the documentation"
- Do NOT generate information not present in context
- Be concise and factual
"""

qa_prompt = PromptTemplate(qa_prompt_str)

# 2. Nutze ResponseSynthesizer mit Custom Prompt
synthesizer = ResponseSynthesizer.from_defaults(
    text_qa_template=qa_prompt,
    refine_template=qa_prompt,
    response_mode="compact"
)

# 3. Grounding mit Quelle-Zitaten
# Stelle sicher dass jede Response Source Nodes nennt
response = query_engine.query("test")
for source in response.source_nodes:
    print(f"Source: {source.node.get_content()[:100]}...")

# 4. Temperature niedrig halten
Settings.llm = Anthropic(
    model="claude-sonnet-4-20250514",
    temperature=0.0  # Deterministic, weniger Kreativität
)

# 5. Retrieval Quality verbessern
# bessere top-k Ranking → bessere Grounding
retriever = index_kern.as_retriever(
    similarity_top_k=5  # Mehr Context = besseres Grounding
)
```

**Prävention**:
- [ ] Prompt Engineering: Explizite "Unknown" Instructions
- [ ] Temperature <= 0.2 für Factual QA
- [ ] Source Citations in Response
- [ ] Regelmässig Responses mit Sources validieren
- [ ] Falls persistentes Problem: Reranker einbauen

---

### 4.3 Vector Store Integration Fehler

#### FEHLER: `ChromaDB Connection Errors`

**Symptom**:
```
ConnectionError: Failed to connect to ChromaDB
sqlite3.OperationalError: database is locked
```

**Root Cause**:
- ChromaDB Datei locked (mehrere Prozesse)
- Falsche Path
- Insufficient Permissions
- Disk voll

**Lösung**:

```python
import chromadb
from pathlib import Path

# 1. Überprüfe Path Existenz
db_path = "./chroma_db"
Path(db_path).mkdir(parents=True, exist_ok=True)

# 2. Check Permissions
import os
if not os.access(db_path, os.W_OK):
    print(f"ERROR: No write permission to {db_path}")

# 3. ChromaDB mit Settings konfigurieren
try:
    client = chromadb.PersistentClient(
        path=db_path,
        settings=chromadb.Settings(
            anonymized_telemetry=False,
            allow_reset=False,  # Verhindert accidental reset
            is_persistent=True
        )
    )
    print("✓ ChromaDB connected")
except Exception as e:
    print(f"ERROR: {e}")
    # Fallback zu In-Memory
    client = chromadb.EphemeralClient()
    print("⚠️ Fallback to in-memory ChromaDB")

# 4. Falls Lock-Fehler: Stelle sicher nur 1 Process zugreift
# In Docker: nur 1 Container mit write-access
```

**Docker Setup für Persistence**:

```dockerfile
# Dockerfile
FROM python:3.11

WORKDIR /app

# Volume für ChromaDB Persistence
VOLUME ["/app/chroma_db"]

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

```yaml
# docker-compose.yml
version: '3'
services:
  rag-app:
    build: .
    volumes:
      - ./chroma_db:/app/chroma_db  # Persist zwischen Restarts
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

**Prävention**:
- [ ] ChromaDB Path persistent (z.B. Docker Volume)
- [ ] Nur 1 Process writes gleichzeitig
- [ ] Regelmässig Backups der `./chroma_db` Datei
- [ ] Monitoring: Disk Space überwachen

---

#### FEHLER: `Embedding Dimension Mismatch`

**Symptom**:
```
ValueError: shapes (384,) and (768,) not aligned
```

**Root Cause**:
Embedding Model bei Query unterscheidet sich von Index-Creation. BAAI/bge-small: 384 dims, aber evt. andere Model bei Reindex verwendet.

**Lösung**:

```python
# 1. Überprüfe Embedding Dimension
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Test Dimension
test_embedding = embed_model.get_text_embedding("test")
print(f"Embedding dimension: {len(test_embedding)}")  # 384

# 2. ChromaDB Collection Info
collection = chroma_client.get_collection("osp_kern")
collection_metadata = collection.metadata

print(f"Collection: {collection_metadata}")

# 3. Stelle sicher Settings.embed_model konsistent
Settings.embed_model = embed_model

# 4. Falls bereits Index mit falscher Dimension existiert:
# - Lösche alte Collection
chroma_client.delete_collection("osp_kern")

# - Reindex mit korrektem Model
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()

# Explicit setzen zum Index-Creation
index = VectorStoreIndex.from_documents(
    documents,
    vector_store=ChromaVectorStore(chroma_collection=collection_kern),
    embed_model=embed_model  # Explizit setzen
)

print("✓ Index reindexed with correct embedding model")
```

**Prävention**:
- [ ] Embedding Model in Dokumentation fixieren
- [ ] In `requirements.txt` Model Name + Version speichern:
  ```
  # BAAI/bge-small-en-v1.5 (384 dims)
  llama-index-embeddings-huggingface
  ```
- [ ] Vor Query: Dimensions-Check
  ```python
  assert len(embed_model.get_text_embedding("test")) == 384
  ```

---

### 4.4 Memory & Resource Fehler

#### FEHLER: `Out of Memory Errors (8GB RAM Limit)`

**Symptom**:
```
MemoryError: Unable to allocate X GiB for an array
OSError: [Errno 12] Cannot allocate memory
```

**Root Cause**:
1. Embedding Model lädt auf GPU (bei CUDA fallback)
2. Zu viele Nodes in Memory
3. Query Caches wachsen unbegrenzt
4. ChromaDB indices nicht optimiert

**Lösung**:

```python
# 1. Explicit CPU-only mode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    device="cpu"  # Erzwinge CPU
)

# 2. Memory Monitoring + GC
import gc
from psutil import virtual_memory

def check_and_free_memory():
    mem = virtual_memory()
    
    print(f"Memory usage: {mem.percent}%")
    
    if mem.percent > 70:
        print("⚠️ Memory high, forcing GC")
        gc.collect()  # Garbage collection
    
    return mem.percent

# 3. Streaming statt BatchLoading
# ❌ Falsch
all_nodes = [load_and_embed(doc) for doc in all_docs]

# ✅ Richtig
def stream_nodes():
    for doc in all_docs:
        node = load_and_embed(doc)
        yield node

# 4. Query Cache mit Max Size
class BoundedQueryCache:
    def __init__(self, max_bytes=100_000_000):  # 100MB
        self.cache = {}
        self.max_bytes = max_bytes
        self.current_bytes = 0
    
    def set(self, key, value):
        import sys
        value_size = sys.getsizeof(value)
        
        while self.current_bytes + value_size > self.max_bytes:
            # Remove oldest
            if self.cache:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
        
        self.cache[key] = value
        self.current_bytes += value_size

# 5. ChromaDB mit PersistentClient (nicht im RAM)
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
    # Embeddings bleiben auf Disk!
)
```

**Docker Resource Limits**:

```yaml
# docker-compose.yml
services:
  rag-app:
    image: myapp
    deploy:
      resources:
        limits:
          memory: 8G  # 8GB max
          cpus: '2'   # 2 CPU cores
    volumes:
      - ./chroma_db:/app/chroma_db
```

**Prävention**:
- [ ] BAAI/bge-small-en-v1.5 (45M params, nicht bge-large 355M)
- [ ] ChromaDB PersistentClient (nicht EphemeralClient)
- [ ] Bounded Query Caches
- [ ] Regelmässiges Memory Monitoring
- [ ] GC nach LLM Calls

---

#### FEHLER: `CPU Usage 100% (Embedding Generation)`

**Symptom**:
```
Query dauert 40+ Sekunden
top: show 1 Python Process at 100% CPU
```

**Root Cause**:
Embedding Model (45M parameters) läuft CPU-intensiv. Bei Batch-Indexierung alle Embeddings gleichzeitig.

**Lösung**:

```python
# 1. Sequential statt Parallel Embedding
from llama_index.core.ingestion import IngestionPipeline

# ❌ Parallel (belastet CPU zu sehr)
pipeline = IngestionPipeline(
    transformations=[...],
    num_workers=4  # Zu viele!
)

# ✅ Sequential
pipeline = IngestionPipeline(
    transformations=[...]
    # num_workers=1 (default)
)

# 2. Batch Embedding mit Pausen
def index_documents_with_throttle(documents, batch_size=5, delay=1):
    """Indexiere mit Pausen zwischen Batches"""
    import time
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        
        # Index batch
        index.insert_nodes([doc_to_node(doc) for doc in batch])
        
        # Pause um CPU zu entspannen
        time.sleep(delay)
        
        print(f"Indexed {i+len(batch)}/{len(documents)} docs")

# 3. CPU Affinity (bei Multi-Core)
import os
os.sched_setaffinity(0, {0, 1})  # Nutze nur 2 cores

# 4. IPEX Optimization (Intel CPU Optimierung)
# Optional: Schneller Embedding auf Intel CPUs
try:
    import intel_extension_for_pytorch as ipex
    
    model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    model = ipex.optimize(model)  # Optimiert für Intel CPUs
except ImportError:
    pass  # IPEX nicht installiert, okay
```

**Prävention**:
- [ ] Batch Indexierung mit Pausen
- [ ] Sequential Processing (num_workers=1)
- [ ] Für Production: Separate Indexing-Phase (nachts)
- [ ] Monitoring von CPU um zu Queries zu verstehen

---

### 4.5 Production Issues

#### FEHLER: `Cache nicht persistent über Container Restart`

**Symptom**:
```
Container restart → Cache ist leer
Erste Query nach Restart: 15-40s
Nach mehreren Queries: schnell (weil wieder im RAM Cache)
```

**Root Cause**:
In-Memory Cache (dict, LRU) wird bei Container-Stop gelöscht.

**Lösung**:

```python
# ❌ In-Memory (nicht persistent)
query_cache = {}  # Verloren nach Restart

# ✅ Redis (persistent)
import redis
redis_client = redis.Redis(host="localhost", port=6379, db=0)

def cache_get_set(query_text, func):
    key = f"query:{query_text}"
    
    # Try Redis first
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    
    # Execute
    result = func()
    
    # Store in Redis (persist 24h)
    redis_client.setex(key, 86400, json.dumps(result))
    
    return result

# ✅ ChromaDB (bereits persistent!)
# Embeddings sind sowieso in PersistentClient gespeichert

# Docker Setup für Redis Persistence
```

**docker-compose.yml**:

```yaml
version: '3'
services:
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes  # AOF Persistence
  
  rag-app:
    build: .
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./chroma_db:/app/chroma_db

volumes:
  redis_data:
```

**Prävention**:
- [ ] Redis für Query Cache (Production)
- [ ] ChromaDB PersistentClient für Embeddings (Standard)
- [ ] Backup Strategy für beide Stores

---

#### FEHLER: `Queries langsam nach Container Restart`

**Symptom**:
```
Erste Query nach Restart: 20-40s
Afterwards: 5-10s (warm cache)
```

**Root Cause**:
Embedding Model wird on-first-use geladen (lazy loading). ChromaDB Collections müssen erneut aufgerufen werden.

**Lösung**:

```python
# 1. Pre-Load Embedding Model beim Startup
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./models"
)

# Trigger load
_ = embed_model.get_text_embedding("warmup")

print("✓ Embedding model warmed up")

# 2. Pre-warm ChromaDB Collections
collections = [
    chroma_client.get_collection("osp_kern"),
    chroma_client.get_collection("osp_erweitert")
]

for collection in collections:
    count = collection.count()
    print(f"✓ Collection '{collection.name}' loaded: {count} documents")

# 3. Startup Health Check
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Warmup beim Application Start"""
    
    # Embed Model load
    _ = embed_model.get_text_embedding("warmup")
    
    # Collections ready
    for coll in collections:
        coll.count()
    
    print("✓ Application ready for queries")

@app.get("/health")
def health():
    return {"status": "ok"}
```

**Docker Startup Script**:

```dockerfile
# Dockerfile
FROM python:3.11

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Prävention**:
- [ ] Embedding Model Pre-loading bei Startup
- [ ] Collection Warm-up
- [ ] Health Checks in Docker
- [ ] Load Balancer Awareness (nicht sofort Traffic nach Start)

---

## 5. Code Examples

### 5.1 Basic Setup (Complete Example)

```python
"""
Vollständiges LlamaIndex RAG Setup mit ChromaDB + Anthropic
Production-ready für OSP Multi-Layer System
"""

import os
from pathlib import Path
import chromadb
from llama_index.core import (
    Settings, VectorStoreIndex, StorageContext, 
    SimpleDirectoryReader
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.anthropic import Anthropic

# === CONFIGURATION ===

class Config:
    DATA_DIR = "./data"
    CHROMA_DB_PATH = "./chroma_db"
    MODELS_CACHE = "./models"
    COLLECTIONS = {
        "kern": "osp_kern",
        "erweitert": "osp_erweitert"
    }

# === INITIALIZATION ===

def setup_settings():
    """Global Settings konfigurieren"""
    
    # LLM
    Settings.llm = Anthropic(
        model="claude-sonnet-4-20250514",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.1,
        max_tokens=2048
    )
    
    # Embedding Model
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        cache_folder=Config.MODELS_CACHE,
        device="cpu"
    )
    
    # Chunking
    Settings.chunk_size = 512
    Settings.chunk_overlap = 100
    
    print("✓ Settings initialized")

def setup_chromadb():
    """ChromaDB Client mit Persistent Storage"""
    
    Path(Config.CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
    
    client = chromadb.PersistentClient(
        path=Config.CHROMA_DB_PATH,
        settings=chromadb.Settings(anonymized_telemetry=False)
    )
    
    return client

def initialize_indices(chroma_client):
    """Create/Load Indices für beide Collections"""
    
    indices = {}
    
    for collection_key, collection_name in Config.COLLECTIONS.items():
        # Get or create collection
        collection = chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"key": collection_key}
        )
        
        # Vector Store
        vector_store = ChromaVectorStore(chroma_collection=collection)
        
        # Storage Context
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        
        # Create Index from Vector Store
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context
        )
        
        indices[collection_key] = index
        
        print(f"✓ Index loaded: {collection_key} ({collection.count()} docs)")
    
    return indices

def index_documents(chroma_client, documents_dir: str):
    """Load Documents & Index them (Nur einmal beim Setup)"""
    
    # Load Documents
    documents = SimpleDirectoryReader(documents_dir).load_data()
    
    print(f"Loading {len(documents)} documents...")
    
    # Index beide Collections
    for collection_key, collection_name in Config.COLLECTIONS.items():
        # Filter documents (z.B. based on path or metadata)
        collection_docs = [d for d in documents]  # TODO: implement filtering
        
        # Create collection
        collection = chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"key": collection_key}
        )
        
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        
        # Index documents
        index = VectorStoreIndex.from_documents(
            documents=collection_docs,
            storage_context=storage_context,
            show_progress=True
        )
        
        print(f"✓ Indexed {collection_name}: {len(collection_docs)} docs")

def main():
    """Main Application"""
    
    # Setup
    setup_settings()
    chroma_client = setup_chromadb()
    
    # Check if indexing needed
    collection = chroma_client.get_or_create_collection("osp_kern")
    if collection.count() == 0:
        print("First run: Indexing documents...")
        index_documents(chroma_client, Config.DATA_DIR)
    
    # Load indices
    indices = initialize_indices(chroma_client)
    
    # Query Loop
    while True:
        query = input("\n📝 Query: ")
        if query.lower() in ["exit", "quit"]:
            break
        
        # Determine which index (simple: use kern as default)
        index = indices["kern"]
        
        # Query
        query_engine = index.as_query_engine(
            similarity_top_k=3
        )
        
        response = query_engine.query(query)
        
        print(f"\n✅ Response:\n{response.response}")
        print(f"\n📚 Sources:")
        for source in response.source_nodes:
            print(f"  - {source.node.get_content()[:100]}...")

if __name__ == "__main__":
    main()
```

---

### 5.2 Multi-Index Router with Async

```python
"""
Advanced: RouterQueryEngine mit Multi-Index + Async Queries
"""

import asyncio
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.selectors import LLMSingleSelector

async def setup_router(indices):
    """Create Router Engine for Multi-Index Selection"""
    
    # Define tools for each index
    tools = [
        QueryEngineTool.from_defaults(
            query_engine=indices["kern"].as_query_engine(similarity_top_k=3),
            name="OSP_Kern",
            description="Technical core documentation and architecture"
        ),
        QueryEngineTool.from_defaults(
            query_engine=indices["erweitert"].as_query_engine(similarity_top_k=3),
            name="OSP_Extended",
            description="Extended resources, guides, and FAQs"
        )
    ]
    
    # Create router
    router = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=tools,
        verbose=True
    )
    
    return router

async def batch_queries(router, queries: list[str]):
    """Execute multiple queries in parallel"""
    
    tasks = [
        router.aquery(q)
        for q in queries
    ]
    
    responses = await asyncio.gather(*tasks)
    
    return responses

async def main_async():
    """Example: Async Multi-Index Queries"""
    
    # Setup (from previous example)
    setup_settings()
    chroma_client = setup_chromadb()
    indices = initialize_indices(chroma_client)
    
    # Create router
    router = await setup_router(indices)
    
    # Multiple queries
    queries = [
        "Was ist OSP Kern-Architektur?",
        "Beste Practices für Deployment",
        "Integrationsmöglichkeiten mit X"
    ]
    
    print(f"Executing {len(queries)} queries in parallel...")
    
    responses = await batch_queries(router, queries)
    
    for i, response in enumerate(responses):
        print(f"\n[{i+1}] {queries[i]}")
        print(f"Response: {response.response}")

if __name__ == "__main__":
    asyncio.run(main_async())
```

---

### 5.3 Query Caching Implementation

```python
"""
Query Caching mit LRU + Redis Fallback
"""

import json
import hashlib
from functools import lru_cache
from time import time
from typing import Optional

class HybridQueryCache:
    """LRU Memory Cache + Redis Fallback"""
    
    def __init__(self, memory_size=100, redis_client=None, ttl=3600):
        self.memory_size = memory_size
        self.redis_client = redis_client
        self.ttl = ttl
        self.memory_cache = {}
        self.access_times = {}
    
    def _generate_key(self, query: str, collection: str) -> str:
        """Create cache key from query + collection"""
        combined = f"{collection}:{query}".encode()
        return hashlib.md5(combined).hexdigest()
    
    def get(self, query: str, collection: str) -> Optional[dict]:
        """Retrieve from memory first, then Redis"""
        
        key = self._generate_key(query, collection)
        
        # Try memory cache first
        if key in self.memory_cache:
            self.access_times[key] = time()
            return self.memory_cache[key]
        
        # Try Redis if available
        if self.redis_client:
            try:
                cached = self.redis_client.get(key)
                if cached:
                    value = json.loads(cached)
                    # Also store in memory for faster future access
                    self.memory_cache[key] = value
                    return value
            except Exception as e:
                print(f"Redis get error: {e}")
        
        return None
    
    def set(self, query: str, collection: str, response: dict):
        """Store in both memory and Redis"""
        
        key = self._generate_key(query, collection)
        
        # Memory cache (LRU eviction)
        if len(self.memory_cache) >= self.memory_size:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.memory_cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.memory_cache[key] = response
        self.access_times[key] = time()
        
        # Redis persistence
        if self.redis_client:
            try:
                self.redis_client.setex(
                    key,
                    self.ttl,
                    json.dumps(response, default=str)
                )
            except Exception as e:
                print(f"Redis set error: {e}")

# === USAGE ===

# Setup
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
query_cache = HybridQueryCache(
    memory_size=100,
    redis_client=redis_client,
    ttl=3600
)

def query_with_cache(query_text: str, collection: str, query_engine):
    """Query with automatic caching"""
    
    # Try cache
    cached = query_cache.get(query_text, collection)
    if cached:
        print("✓ Cache HIT")
        return cached
    
    # Execute query
    print("→ Cache MISS, executing query...")
    response = query_engine.query(query_text)
    
    # Cache result
    result = {
        "response": response.response,
        "sources": [
            n.node.get_content()[:200] 
            for n in response.source_nodes
        ]
    }
    
    query_cache.set(query_text, collection, result)
    
    return result
```

---

## 6. Best Practices Checklist

Nutze diese Checkliste für Production-Readiness:

### Initiale Setup Phase

- [ ] **Settings API verwenden** (nicht ServiceContext)
- [ ] **ChromaDB PersistentClient** (nicht Ephemeral)
- [ ] **Embedding Model pinnen** (BAAI/bge-small-en-v1.5, 384 dims)
- [ ] **API Keys in Environment** (nicht hardcoded)
- [ ] **LLM Temperature = 0.0-0.1** (faktisch, nicht kreativ)

### Indexierung

- [ ] **Alle Dokumente mit Metadata** (doc_type, component, version)
- [ ] **Chunk Size = 512 Tokens** (optimal für 8-15KB Dokumente)
- [ ] **Chunk Overlap = 100** (20% für Kontextkontinuität)
- [ ] **Nach Indexierung: count() überprüfen**
- [ ] **Embeddings auf Disk persistent** (ChromaDB)

### Query Engine

- [ ] **similarity_top_k ≤ 5** (performance & quality tradeoff)
- [ ] **Response Mode = "compact"** (nicht tree_summarize default)
- [ ] **Streaming enabled** (für UX progressiv)
- [ ] **Query Caching implementiert** (LRU oder Redis)

### Performance

- [ ] **Sub-10s Response Time** (retrieve + synthesize)
- [ ] **Async Queries für Batch** (parallel execution)
- [ ] **Memory Monitoring** (< 70% regular usage)
- [ ] **CPU Affinity** (bei CPU-constrained)
- [ ] **Pre-warming on Startup** (embedding model + collections)

### Production Deployment

- [ ] **Docker Health Checks** eingebaut
- [ ] **Persistent Volumes** für ChromaDB + Models
- [ ] **Error Handling** mit Fallbacks
- [ ] **Logging & Monitoring** (response times, cache hits)
- [ ] **HTTPS/API Key Auth** (für Multi-User)
- [ ] **Rate Limiting** (max queries/min)

### Sicherheit

- [ ] **API Keys nicht in Code**
- [ ] **ANTHROPIC_API_KEY als Secret**
- [ ] **Sensitive Data Masking** (wenn applicable)
- [ ] **Access Logging** (wer fragt was)

### Testing & Validation

- [ ] **Unit Tests** für Custom Components
- [ ] **Integration Tests** (Query Engine + Cache)
- [ ] **Load Tests** (concurrent queries)
- [ ] **Source Validation** (responses grounded?)
- [ ] **Regression Tests** (keine Hallucinations new queries)

---

## 7. API Reference

### Settings (Global Configuration)

```python
from llama_index.core import Settings

# LLM
Settings.llm = Anthropic(...)

# Embedding Model
Settings.embed_model = HuggingFaceEmbedding(...)

# Chunking
Settings.chunk_size = 512
Settings.chunk_overlap = 100

# Callbacks
Settings.callback_manager.add_handler(...)

# Tokenizer
Settings.tokenizer = ...  # Optional

# Prompt Helper
Settings.context_window = 200000  # Claude Sonnet
Settings.num_output = 2048
```

### VectorStoreIndex

```python
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

# From Vector Store (Preferred für Production)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context
)

# From Documents
index = VectorStoreIndex.from_documents(
    documents=documents,
    vector_store=vector_store,
    show_progress=True
)

# Retriever
retriever = index.as_retriever(similarity_top_k=3)

# Query Engine
query_engine = index.as_query_engine(
    streaming=True,
    similarity_top_k=3
)

response = query_engine.query("What is X?")
# response.response → String
# response.source_nodes → [NodeWithScore, ...]
```

### ChromaVectorStore

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("my_collection")

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

# Methods
vector_store.add(nodes=[...])
vector_store.delete(node_ids=[...])
vector_store.client.delete_collection("old_collection")
```

### HuggingFaceEmbedding

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./models",
    device="cpu",
    trust_remote_code=False
)

# Get embedding for text
embedding = embed_model.get_text_embedding("Hello world")
# embedding → List[float] (384 dims for bge-small)

# Get text embeddings (batch)
embeddings = embed_model.get_text_embeddings(["text1", "text2"])
```

### Anthropic LLM

```python
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(
    model="claude-sonnet-4-20250514",
    api_key="sk-ant-...",
    temperature=0.1,
    max_tokens=2048,
    timeout=30
)

# Complete
response = llm.complete("Hello")
# response.text → String

# Chat
response = llm.chat([
    ChatMessage(role="user", content="Hello")
])

# Streaming
response = llm.stream_complete("Hello")
for chunk in response:
    print(chunk.delta, end="")
```

---

## Appendix: Migration Guide

### ServiceContext → Settings (v0.10+)

#### Before (Deprecated)

```python
from llama_index import ServiceContext, set_global_service_context

llm = OpenAI(model="gpt-3.5-turbo")
embed_model = OpenAIEmbedding()

service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model,
    chunk_size=512
)

set_global_service_context(service_context)

index = VectorStoreIndex.from_documents(
    documents,
    service_context=service_context
)
```

#### After (Current)

```python
from llama_index.core import Settings, VectorStoreIndex

Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding()
Settings.chunk_size = 512

# Automatic: index uses Settings
index = VectorStoreIndex.from_documents(documents)
```

#### Migration Checklist

1. Remove `ServiceContext` imports
2. Replace with `Settings` global assignments
3. Remove `service_context=` parameter from index creation
4. Update imports:
   ```python
   # Old
   from llama_index import VectorStoreIndex
   
   # New
   from llama_index.core import VectorStoreIndex
   ```
5. Test all Query Engines (should work without changes)

---

## References & Further Reading

- **Official Docs**: https://developers.llamaindex.ai/
- **GitHub**: https://github.com/run-llama/llama_index
- **Community**: https://community.llamaindex.ai/
- **ChromaDB Docs**: https://docs.trychroma.com/
- **Anthropic API**: https://console.anthropic.com/docs/

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Maintainer**: Quality Engineering Team

*For updates and corrections, please refer to official LlamaIndex documentation.*
