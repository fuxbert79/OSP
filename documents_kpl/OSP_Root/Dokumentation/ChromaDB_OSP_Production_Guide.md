# ChromaDB Production Guide - OSP Multi-Layer RAG System

## Metadata

- **Version**: ChromaDB 0.5.15
- **Use-Case**: Multi-Collection Vector Database für OSP Kern- & Erweiterte Dokumente
- **Last Updated**: December 2025
- **Environment**: Docker Container mit Persistent Storage
- **Dokumentation für**: Production RAG-System mit LlamaIndex Integration

---

## Table of Contents

1. [Production Setup](#1-production-setup)
2. [Query & Retrieval](#2-query--retrieval)
3. [Data Management](#3-data-management)
4. [Troubleshooting Guide](#4-troubleshooting-guide)
5. [Performance Optimization](#5-performance-optimization)
6. [Integration Patterns](#6-integration-patterns)
7. [Backup & Migration](#7-backup--migration)
8. [Docker Deployment](#8-docker-deployment)
9. [Code Examples](#9-code-examples)
10. [Best Practices Checklist](#10-best-practices-checklist)
11. [Appendix: HNSW Index Tuning](#appendix-hnsw-index-tuning-guide)

---

## 1. Production Setup

### 1.1 Client Types: PersistentClient vs HttpClient vs In-Memory

ChromaDB bietet drei verschiedene Client-Modi, die je nach Anforderungen unterschiedliche Vor- und Nachteile haben:

#### PersistentClient (Empfohlen für Produktion mit Docker)

Der **PersistentClient** speichert alle Daten lokal auf der Festplatte und ist ideal für Einzel-Container-Deployments.

```python
import chromadb
from chromadb.config import Settings

# Standard-Konfiguration
client = chromadb.PersistentClient(path="/mnt/HC_Volume_104189729/osp/chromadb/data")

# Mit erweiterten Settings
settings = Settings(
    allow_reset=True,
    anonymized_telemetry=False,
    chroma_db_impl="duckdb+parquet"  # Standard Backend
)
client = chromadb.PersistentClient(
    path="/mnt/HC_Volume_104189729/osp/chromadb/data",
    settings=settings
)
```

**Vorteile:**
- Geringe Latenz (lokale Datenzugriffe)
- Keine Netzwerk-Overhead
- Einfache Deployment-Komplexität
- Ideal für Docker Single-Container-Setup
- Data Privacy durch lokale Speicherung

**Nachteile:**
- Keine horizontale Skalierung möglich
- Nicht für Multi-Instanz-Szenarien geeignet
- SQLite-begrenzte gleichzeitige Zugriffe

#### HttpClient (für Client-Server-Architektur)

Der **HttpClient** verbindet sich mit einem Remote-ChromaDB-Server über HTTP.

```python
import chromadb

# HttpClient für Remote-Server
client = chromadb.HttpClient(
    host="chromadb-server",
    port=8000,
    ssl=False,
    headers={"X_CHROMA_TOKEN": "your-auth-token"}
)
```

**Vorteile:**
- Skalierbarkeit (separate Server-Instanz)
- Mehrere Clients können gleichzeitig zugreifen
- Load-Balancing möglich
- Shared Ressourcen
- Geeignet für Cluster-Deployments (Kubernetes)

**Nachteile:**
- Höhere Netzwerk-Latenz
- Komplexere Deployment-Infrastruktur
- Server-Ausfallrisiko
- Authentifizierung erforderlich

#### In-Memory Client (Nur für Entwicklung)

```python
import chromadb

# Nur für Tests - Daten gehen verloren nach Neustart
client = chromadb.EphemeralClient()
```

**Für OSP-System**: **PersistentClient im Docker-Container** ist die richtige Wahl.

---

### 1.2 Collection Management

Collections sind logische Container für verwandte Documents und deren Embeddings. Das OSP-System nutzt zwei Collections:

#### get_or_create_collection (Empfohlen)

```python
# Sicher für Startups und Restarts
kern_collection = client.get_or_create_collection(
    name="osp_kern",
    metadata={"description": "OSP Kern-Dokumente (APQP, Control Plans)"},
    space="cosine"  # Distance Metric
)

erweitert_collection = client.get_or_create_collection(
    name="osp_erweitert",
    metadata={"description": "OSP Erweiterte Dokumente (VDA, Guidelines)"},
    space="cosine"
)
```

**Best Practice**: Verwende immer `get_or_create_collection()` statt `create_collection()`:
- Verhindert "Collection already exists"-Fehler
- Sicher bei Container-Restarts
- Idempotent (mehrfaches Aufrufen schadet nicht)
- Ideal für Deployment und CI/CD

#### Metadata-Konfiguration

```python
# Erweiterte Metadata mit HNSW-Tuning
collection = client.get_or_create_collection(
    name="osp_kern",
    metadata={
        "description": "Kern-Dokumenten",
        "document_count": "12",
        "embedding_model": "BAAI/bge-small-en-v1.5",
        "embedding_dimension": "384",
        "hnsw:space": "cosine",
        "hnsw:M": "16",
        "hnsw:ef_construction": "200"
    }
)
```

#### Collection Properties Abrufen

```python
# Informationen über Collection
print(f"Collection Name: {kern_collection.name}")
print(f"Metadaten: {kern_collection.metadata}")
print(f"Dokumente in Collection: {kern_collection.count()}")

# Alle Collections auflisten
all_collections = client.list_collections()
for col in all_collections:
    print(f"- {col.name}: {col.count()} Dokumente")
```

---

### 1.3 Embedding Function Configuration

Das OSP-System nutzt das **BAAI/bge-small-en-v1.5** Modell (384 Dimensionen, optimiert für Cosine Similarity).

#### Standard-Embedding mit HuggingFace

```python
from chromadb.utils import embedding_functions

# Default BGE Embedding (wenn nicht anders konfiguriert)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-en-v1.5",
    device="cpu"  # oder "cuda" für GPU
)

# Mit Collection verbinden
collection = client.get_or_create_collection(
    name="osp_kern",
    embedding_function=embedding_function
)
```

#### Custom Embedding Function

```python
from chromadb import Document
from typing import List, Dict, Any

class CustomBGEEmbedding:
    """Custom Embedding für spezielle Anforderungen"""
    
    def __init__(self, model_name="BAAI/bge-small-en-v1.5", 
                 device="cpu",
                 normalize=True):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name, device=device)
        self.normalize = normalize
        self.model_name = model_name
        
    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Embed texts und return embeddings"""
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=self.normalize,
            show_progress_bar=False,
            batch_size=32  # Batch-Verarbeitung für Performance
        )
        return embeddings.tolist()
```

#### Embedding-Dimension Verifikation

```python
def verify_embedding_dimensions(collection, expected_dim=384):
    """Überprüfe, ob Embeddings die richtige Dimension haben"""
    try:
        # Abrufen eines Dokuments mit Embedding
        result = collection.get(limit=1, include=["embeddings"])
        if result["embeddings"]:
            actual_dim = len(result["embeddings"][0])
            if actual_dim != expected_dim:
                raise ValueError(
                    f"Embedding Dimension Mismatch: "
                    f"erwartet {expected_dim}, "
                    f"gefunden {actual_dim}"
                )
            print(f"✓ Embedding-Dimension korrekt: {actual_dim}")
        else:
            print("Warnung: Collection ist leer")
    except Exception as e:
        raise RuntimeError(f"Fehler bei Dimension-Verifikation: {str(e)}")

# Verwendung
verify_embedding_dimensions(kern_collection, expected_dim=384)
```

**WICHTIG**: Wenn Sie das Embedding-Modell ändern, müssen Sie die Collection neuen oder erstellen, da die Dimensionen unterschiedlich sein können:
- `BAAI/bge-small-en-v1.5` = 384 Dimensionen
- `BAAI/bge-base-en-v1.5` = 768 Dimensionen
- `all-MiniLM-L6-v2` = 384 Dimensionen

---

### 1.4 Distance Metrics

ChromaDB unterstützt verschiedene Distanzmetriken für Similarity Search:

```python
# Cosine Similarity (Empfohlen für Embeddings)
collection = client.get_or_create_collection(
    name="osp_kern",
    metadata={"hnsw:space": "cosine"}  # Standard für BGE-Embeddings
)

# Euclidean Distance (L2)
collection = client.get_or_create_collection(
    name="example",
    metadata={"hnsw:space": "l2"}
)

# Inner Product (IP)
collection = client.get_or_create_collection(
    name="example",
    metadata={"hnsw:space": "ip"}
)
```

**Metrik-Vergleich:**

| Metrik | Use-Case | Empfehlung |
|--------|----------|------------|
| Cosine | Text-Embeddings, Winkel-Ähnlichkeit | ✓ BGE-Embeddings |
| L2 | Euclidean Distance, allgemein | Wenn normalisiert |
| IP (Inner Product) | Schnell, aber mag normalisierte Vektoren | Spezielle Fälle |

---

### 1.5 Index Configuration: HNSW Parameters

HNSW (Hierarchical Navigable Small World) ist der Standard-Index für ChromaDB.

#### HNSW Parameter

```python
collection = client.get_or_create_collection(
    name="osp_kern",
    metadata={
        # HNSW-spezifische Parameter
        "hnsw:space": "cosine",
        "hnsw:M": "16",              # Anzahl Verbindungen pro Layer
        "hnsw:ef_construction": "200"  # Suche-Tiefe beim Indexing
    }
)
```

**Parameter-Erklärung:**

- **M** (Connectivity): Maximale Anzahl bidirektionaler Links pro Knoten
  - Standard: 16
  - Kleine Werte (8-12): Weniger Memory, schneller, niedrigere Accuracy
  - Große Werte (20-32): Mehr Memory, besser Accuracy, langsamer
  
- **ef_construction**: Anzahl Kandidaten während Index-Erstellung
  - Standard: 200
  - Niedrig (100): Schnelle Indexierung, niedrigere Recall
  - Hoch (400-500): Beste Recall, aber 2x längere Indexierung

- **ef_search**: Runtime-Parameter für Queries (wird separat in Query-Zeit gesetzt)
  - Standard: ef_construction
  - Wird bei Query angegeben
  - Higher = bessere Accuracy, langsamer

#### Konfiguration für OSP-System

```python
# Optimiert für Produktion mit 51 Dokumenten
HNSW_CONFIG = {
    "hnsw:space": "cosine",
    "hnsw:M": "16",              # Balanced
    "hnsw:ef_construction": "200"  # Good recall für kleine Datasets
}

kern_collection = client.get_or_create_collection(
    name="osp_kern",
    metadata={
        **HNSW_CONFIG,
        "description": "OSP Kern-Dokumente"
    }
)
```

---

## 2. Query & Retrieval

### 2.1 Basic Query Syntax

```python
# Einfache Similarity Search
results = collection.query(
    query_texts=["APQP Prozess und Ablauf"],
    n_results=5,
    include=["documents", "distances", "metadatas"]
)

# Zugriff auf Ergebnisse
for doc, distance, metadata in zip(
    results["documents"][0],
    results["distances"][0],
    results["metadatas"][0]
):
    print(f"Score: {1 - distance:.3f}")  # Cosine → [0,1] Score
    print(f"Doc: {doc[:100]}...")
    print(f"Meta: {metadata}")
```

#### Ergebnis-Struktur

```python
{
    "ids": [["id1", "id2", "id3"]],           # Document IDs
    "documents": [["Doc1", "Doc2", "Doc3"]],  # Document Text
    "distances": [[0.15, 0.32, 0.48]],        # Distanzen
    "metadatas": [[{...}, {...}, {...}]],     # Metadata
    "embeddings": [[...], [...], [...]]       # Embeddings (wenn included)
}
```

### 2.2 Advanced Query Syntax: where & where_document

#### Metadata Filtering (where)

```python
# Nur Dokumente mit bestimmten Metadata auswählen
results = collection.query(
    query_texts=["Control Plan Vorlage"],
    n_results=5,
    where={
        "doc_type": {"$eq": "control_plan"}
    }
)

# Mehrere Filter (AND-Logik)
results = collection.query(
    query_texts=["APQP"],
    where={
        "$and": [
            {"doc_type": {"$eq": "apqp"}},
            {"version": {"$gte": "2"}}
        ]
    }
)

# Oder Filter (OR-Logik)
results = collection.query(
    query_texts=["Qualität"],
    where={
        "$or": [
            {"doc_type": {"$eq": "iso_9001"}},
            {"doc_type": {"$eq": "ppap"}}
        ]
    }
)

# IN Filter (Multiple Werte)
results = collection.query(
    query_texts=["Freigabe"],
    where={
        "status": {"$in": ["approved", "review"]}
    }
)

# NOT Filter
results = collection.query(
    query_texts=["Doku"],
    where={
        "draft": {"$ne": True}  # Nicht Draft-Dokumente
    }
)
```

#### Document Content Filtering (where_document)

```python
# Filter nach Dokumentinhalt (Full-Text-ähnlich)
results = collection.query(
    query_texts=["Qualitätsmanagementsystem"],
    n_results=5,
    where_document={
        "$contains": "ISO 9001"  # Dokument muss "ISO 9001" enthalten
    }
)

# Negation
results = collection.query(
    query_texts=["Fehler"],
    where_document={
        "$not_contains": "deprecated"
    }
)
```

#### Kombinierte Filter

```python
# Metadata + Document-Content Filter
results = collection.query(
    query_texts=["Prozessoptimierung"],
    n_results=5,
    where={
        "status": {"$eq": "active"}  # Metadata Filter
    },
    where_document={
        "$contains": "Lean Six Sigma"  # Content Filter
    }
)
```

### 2.3 Query Performance & Parameters

```python
def optimized_query(collection, query_text, n_results=5, timeout=3):
    """Optimierte Query mit Performance-Überwachung"""
    import time
    
    start = time.time()
    
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=min(n_results, 10),  # Cap bei 10
            include=["documents", "distances", "metadatas"],
            # ef_search wird bei bedarf später angepasst
        )
        
        elapsed = time.time() - start
        
        if elapsed > timeout:
            print(f"Warnung: Query dauerte {elapsed:.2f}s (Timeout: {timeout}s)")
        
        # Confidence Scoring
        scores = [1 - d for d in results["distances"][0]]
        
        return {
            "results": results,
            "scores": scores,
            "elapsed_ms": elapsed * 1000
        }
    
    except Exception as e:
        raise RuntimeError(f"Query fehlgeschlagen: {str(e)}")

# Verwendung
query_result = optimized_query(
    kern_collection,
    "Mikrokrimpen und Crimpverbindungen",
    n_results=5
)
```

### 2.4 Batch Queries

```python
# Mehrere Queries gleichzeitig
queries = [
    "APQP Prozess Dokumentation",
    "VDA PPAP Anforderungen",
    "Crimpverbindungen Qualitätsprüfung"
]

results = collection.query(
    query_texts=queries,
    n_results=3,
    include=["documents", "distances"]
)

# Ergebnisse per Query (Array-Index entspricht Query-Index)
for i, query in enumerate(queries):
    print(f"\nQuery: {query}")
    print(f"Top Result: {results['documents'][i][0][:50]}...")
    print(f"Distance: {results['distances'][i][0]:.3f}")
```

### 2.5 Result Ranking & Scoring

```python
def rank_results(collection, query_text, n_results=10):
    """Ranked Results mit Confidence Scores"""
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )
    
    # Konvertiere Distances zu Scores (0-1, 1=perfekt)
    # Bei Cosine Distance: Score = 1 - distance
    ranked = []
    for doc, dist, meta in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0]
    ):
        score = 1 - dist  # Cosine Distance to Similarity Score
        ranked.append({
            "score": score,
            "text": doc,
            "metadata": meta,
            "distance": dist
        })
    
    # Sortieren nach Score
    ranked.sort(key=lambda x: x["score"], reverse=True)
    
    return ranked

# Verwendung mit Score-Threshold
results = rank_results(kern_collection, "Qualitätskontrolle")

# Nur hohe Scores zurückgeben
high_confidence = [r for r in results if r["score"] > 0.7]

print(f"High Confidence Results ({len(high_confidence)}):")
for r in high_confidence:
    print(f"  [{r['score']:.2%}] {r['text'][:60]}...")
```

---

## 3. Data Management

### 3.1 Adding Documents

#### Einfaches Add

```python
collection.add(
    ids=["doc1", "doc2"],
    documents=["APQP ist der...", "Control Plan müssen..."],
    metadatas=[
        {"doc_type": "apqp", "version": "1"},
        {"doc_type": "control_plan", "version": "2"}
    ]
)
```

#### Add mit Embeddings (Pre-computed)

```python
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-en-v1.5"
)

# Embeddings vorberechnen
documents = ["Text 1", "Text 2"]
embeddings = embedding_function(documents)

collection.add(
    ids=["id1", "id2"],
    documents=documents,
    embeddings=embeddings,  # Pre-computed
    metadatas=[
        {"source": "pdf"},
        {"source": "web"}
    ]
)
```

#### ID-Generierung Strategy

```python
import hashlib
from datetime import datetime

def generate_document_id(content, source=None):
    """Eindeutige Document IDs basierend auf Content MD5"""
    hash_obj = hashlib.md5(content.encode())
    base_id = hash_obj.hexdigest()[:16]  # 16 Zeichen MD5
    
    if source:
        return f"{source}_{base_id}"
    return base_id

# Verwendung
doc_id = generate_document_id(
    "OSP Kern-Dokumentation",
    source="osp_kern"
)
# → "osp_kern_a3f5c2b1e4d8f6a9"

# Oder mit Timestamp für Versioning
def generate_versioned_id(content, doc_type, version="1"):
    """ID mit Versions-Info"""
    base_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{doc_type}_v{version}_{base_hash}_{timestamp}"
```

### 3.2 Batch Operations (Effiziente Bulk Import)

```python
def batch_add_documents(collection, documents, batch_size=100):
    """Füge viele Dokumente in Batches ein (für 51 Dokumente)"""
    
    total_docs = len(documents)
    added = 0
    
    for i in range(0, total_docs, batch_size):
        batch = documents[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        try:
            ids = [doc.get("id") for doc in batch]
            texts = [doc.get("text") for doc in batch]
            metadatas = [doc.get("metadata", {}) for doc in batch]
            
            collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            added += len(batch)
            print(f"✓ Batch {batch_num}: {len(batch)} Dokumente eingefügt ({added}/{total_docs})")
            
        except Exception as e:
            print(f"✗ Batch {batch_num} fehlgeschlagen: {str(e)}")
            raise

    print(f"✓ Alle {added} Dokumente erfolgreich eingefügt")

# Daten vorbereiten
documents = [
    {
        "id": "osp_kern_001",
        "text": "APQP Dokumentation...",
        "metadata": {"doc_type": "apqp", "version": "1"}
    },
    # ... 50 weitere Dokumente
]

# Bulk Import
batch_add_documents(kern_collection, documents, batch_size=25)
```

#### Max Batch Size Bestimmung

```python
# ChromaDB max_batch_size abhängig von SQLite-Limits
max_size = client.max_batch_size
print(f"Max Batch Size: {max_size}")  # Typisch: 41,666

# Für Safety: Batch-Größe reduzieren
SAFE_BATCH_SIZE = min(100, max_size // 400)  # ~100 mit Metadaten
```

### 3.3 Updating Documents

```python
# Update mit upsert (ersetzt existierende oder fügt ein)
collection.upsert(
    ids=["doc1"],
    documents=["Neue Version des APQP..."],
    metadatas=[{"doc_type": "apqp", "version": "2"}]
)

# Oder: Explizites Update
collection.update(
    ids=["doc1"],
    documents=["Aktualisierter Text"],
    metadatas=[{"last_updated": "2025-12-11"}]
)
```

**WICHTIG**: Update und Delete erfordern das gleiche Embedding-Modell!

### 3.4 Deleting Documents

```python
# Einzelnes Dokument löschen
collection.delete(ids=["doc1"])

# Mehrere Dokumente löschen
collection.delete(ids=["doc1", "doc2", "doc3"])

# Mit where-Filter löschen
collection.delete(where={"status": {"$eq": "archived"}})

# Mit where_document löschen
collection.delete(
    where_document={"$contains": "deprecated"}
)
```

### 3.5 Metadata Management

```python
class MetadataManager:
    """Standardisierte Metadata für OSP-Dokumentation"""
    
    STANDARD_SCHEMA = {
        "doc_type": str,           # apqp, control_plan, vda_ppap, etc.
        "version": str,            # "1.0", "2.1"
        "created_date": str,       # ISO 8601
        "last_updated": str,       # ISO 8601
        "author": str,             # Person/Team
        "status": str,             # active, archived, review
        "language": str,           # de, en
        "source": str,             # pdf, web, internal
        "category": str            # Qualität, Prozess, Anforderung
    }
    
    @staticmethod
    def create_metadata(**kwargs):
        """Erstelle validierte Metadata"""
        from datetime import datetime
        
        metadata = {
            "created_date": kwargs.get("created_date", 
                                      datetime.now().isoformat()),
            "last_updated": kwargs.get("last_updated", 
                                      datetime.now().isoformat())
        }
        
        # Nur erlaubte Keys
        for key in MetadataManager.STANDARD_SCHEMA:
            if key in kwargs:
                metadata[key] = str(kwargs[key])
        
        return metadata

# Verwendung
meta = MetadataManager.create_metadata(
    doc_type="apqp",
    version="2.0",
    author="QM-Team",
    status="active"
)

collection.add(
    ids=["doc1"],
    documents=["..."],
    metadatas=[meta]
)
```

---

## 4. Troubleshooting Guide

### 4.1 Connection & Setup Fehler

#### ERROR: Cannot connect to ChromaDB

**Symptom:**
```
ConnectionError: Could not connect to localhost:8000
```

**Root Cause:**
- ChromaDB-Container läuft nicht
- Falscher Host/Port
- Firewall blockiert Port
- CHROMA_API_IMPL nicht gesetzt

**Lösung:**

```bash
# 1. Überprüfe Container-Status
docker ps | grep chromadb
# Falls nicht läuft:
docker-compose -f docker-compose.yml up -d chromadb

# 2. Teste Konnektivität
curl http://localhost:8000/api/v2

# 3. Prüfe Logs
docker logs chromadb

# 4. Überprüfe Environment Variable
echo $CHROMA_API_IMPL  # sollte leer oder "rest" sein
```

**Python-Code:**

```python
import time
import chromadb

def wait_for_chromadb(host="localhost", port=8000, timeout=30):
    """Warte bis ChromaDB erreichbar ist"""
    import urllib.request
    
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(f"http://{host}:{port}/api/v2")
            print("✓ ChromaDB ist erreichbar")
            return True
        except:
            time.sleep(2)
    
    raise ConnectionError(f"ChromaDB nicht erreichbar nach {timeout}s")

# Warte beim Start
wait_for_chromadb()
client = chromadb.HttpClient(host="localhost", port=8000)
```

**Prävention:**
- Health Checks in docker-compose.yml konfigurieren
- Startup-Scripts immer Connection testen
- Logging für Connection-Probleme

---

#### ERROR: Collection 'osp_kern' already exists

**Symptom:**
```
ValueError: Collection osp_kern already exists
```

**Root Cause:**
- Verwendung von `create_collection()` statt `get_or_create_collection()`
- Collection wurde manuell erstellt und Code versucht erneut zu erstellen

**Lösung:**

```python
# ❌ FALSCH:
collection = client.create_collection(name="osp_kern")  # Fehler auf 2. Aufruf

# ✅ RICHTIG:
collection = client.get_or_create_collection(name="osp_kern")  # Idempotent

# Oder explizite Behandlung:
try:
    collection = client.create_collection(name="osp_kern")
except ValueError as e:
    if "already exists" in str(e):
        collection = client.get_collection(name="osp_kern")
    else:
        raise
```

**Prävention:**
- Immer `get_or_create_collection()` verwenden
- Initialisierungscode mehrfach laufen lassen können

---

#### ERROR: PersistentClient path not found

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/mnt/HC_Volume_104189729/osp/chromadb/data'
```

**Root Cause:**
- Pfad existiert nicht
- Falscher Pfad in Konfiguration
- Docker Volume nicht gemountet
- Permissions-Fehler

**Lösung:**

```python
import os
from pathlib import Path

def ensure_chromadb_path(path="/mnt/HC_Volume_104189729/osp/chromadb/data"):
    """Stelle sicher, dass der Pfad existiert"""
    Path(path).mkdir(parents=True, exist_ok=True)
    
    # Überprüfe Schreib-Rechte
    if not os.access(path, os.W_OK):
        raise PermissionError(f"Keine Schreib-Rechte für {path}")
    
    print(f"✓ ChromaDB Pfad bereit: {path}")
    return path

# Verwendung
db_path = ensure_chromadb_path()
client = chromadb.PersistentClient(path=db_path)
```

**Docker-spezifisch:**

```yaml
# docker-compose.yml
services:
  chromadb:
    volumes:
      - ./chromadb_data:/chroma/chroma  # Erstelle Verzeichnis lokal
    user: "1000:1000"  # Permissions setzen
```

**Bash-Setup:**

```bash
# Erstelle Verzeichnis mit korrekten Permissions
mkdir -p ./chromadb_data
chmod 755 ./chromadb_data

# Oder mit Docker
docker exec chromadb mkdir -p /mnt/HC_Volume_104189729/osp/chromadb/data
```

**Prävention:**
- Init-Skripte für Pfad-Erstellung
- Container mit `entrypoint.sh` verwenden
- Volume-Mounts überprüfen

---

#### ERROR: Docker Volume Permissions

**Symptom:**
```
Permission denied: '/chroma/chroma/...'
```

**Root Cause:**
- Container läuft mit anderem User als Host
- Volume gehört falschem User
- SELinux/AppArmor Restriktionen

**Lösung:**

```yaml
# docker-compose.yml mit Permissions
services:
  chromadb:
    image: chromadb/chroma:0.5.15
    user: "0:0"  # Starte als Root (nicht ideal)
    # oder:
    user: "1000:1000"  # Mit UID:GID
    volumes:
      - ./chromadb_data:/chroma/chroma:rw  # Explizite RW Permissions
    environment:
      - CHROMA_ALLOW_RESET=true
```

**Host-Vorbereitung:**

```bash
# Erstelle Verzeichnis mit korrekten Permissions
mkdir -p ./chromadb_data
sudo chown 1000:1000 ./chromadb_data
chmod 755 ./chromadb_data

# Überprüfe
ls -la chromadb_data
# Sollte zeigen: drwxr-xr-x 1000:1000
```

**Prävention:**
- Volume-Owner vom Start an korrekt setzen
- Init-Script vor Container-Start ausführen

---

### 4.2 Collection Management Fehler

#### ERROR: Collection not found

**Symptom:**
```
ValueError: Collection 'osp_kern' does not exist
```

**Root Cause:**
- Collection wurde nicht erstellt
- Falsche Collection-Name
- Falscher Client/Database
- Collection wurde gelöscht

**Lösung:**

```python
def safe_get_collection(client, name, create_if_missing=True):
    """Hole Collection sicher, erstelle wenn nötig"""
    try:
        return client.get_collection(name=name)
    except ValueError as e:
        if "does not exist" in str(e):
            if create_if_missing:
                print(f"Collection '{name}' existiert nicht, erstelle...")
                return client.create_collection(
                    name=name,
                    metadata={"created_timestamp": str(datetime.now())}
                )
            else:
                # Liste verfügbare Collections auf
                collections = client.list_collections()
                names = [c.name for c in collections]
                raise ValueError(
                    f"Collection '{name}' nicht gefunden. "
                    f"Verfügbar: {names}"
                )
        else:
            raise

# Verwendung
kern_collection = safe_get_collection(client, "osp_kern")
```

---

#### ERROR: Duplicate IDs on add()

**Symptom:**
```
ValueError: IDs must be unique, got duplicate: 'osp_001'
```

**Root Cause:**
- Gleiche ID wird mehrfach eingefügt
- Fehlerhaftes ID-Generierungslogik
- Daten aus mehreren Quellen mit gleicher ID

**Lösung:**

```python
def add_with_deduplication(collection, ids, documents, metadatas):
    """Füge Dokumente mit Duplikat-Prüfung ein"""
    
    # Überprüfe auf Duplikate in Input
    if len(ids) != len(set(ids)):
        duplicates = [x for x in ids if ids.count(x) > 1]
        raise ValueError(f"Duplikate in Input IDs: {duplicates}")
    
    # Überprüfe auf existierende IDs
    existing = collection.get(ids=ids, limit=1)
    if existing["ids"]:
        print(f"Warnung: {len(existing['ids'])} IDs existieren bereits")
        # Option 1: Skip existierende
        new_ids, new_docs, new_metas = [], [], []
        for id, doc, meta in zip(ids, documents, metadatas):
            if id not in existing["ids"]:
                new_ids.append(id)
                new_docs.append(doc)
                new_metas.append(meta)
        
        if new_ids:
            collection.add(ids=new_ids, documents=new_docs, metadatas=new_metas)
            return len(new_ids)
        else:
            print("Keine neuen Dokumente zu fügen")
            return 0
    else:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        return len(ids)
```

**ID-Generierungs-Best-Practice:**

```python
import hashlib

def generate_unique_id(text, doc_type, version="1.0"):
    """Generiere eindeutige ID basierend auf Content"""
    # MD5-Hash des Textes (deterministisch)
    content_hash = hashlib.md5(text.encode()).hexdigest()[:12]
    
    # Kombiniere mit Metadaten
    return f"{doc_type}_{version}_{content_hash}"

# Test auf Eindeutigkeit
ids = set()
for doc in documents:
    id = generate_unique_id(doc["text"], doc["type"])
    assert id not in ids, f"Duplikat: {id}"
    ids.add(id)
```

---

#### ERROR: Embedding dimension mismatch

**Symptom:**
```
ValueError: Embedding dimension 768 does not match collection dimensionality 384
```

**Root Cause:**
- Embedding-Modell gewechselt (unterschiedliche Dimensionen)
- BGE-small (384) → BGE-base (768)
- Custom Embedding mit falscher Dimension

**Lösung:**

```python
def verify_and_fix_embedding_dimension(collection, expected_dim=384):
    """Überprüfe und repariere Embedding-Dimension"""
    
    try:
        # Abrufen eines Dokuments
        sample = collection.get(limit=1, include=["embeddings"])
        
        if sample["embeddings"]:
            actual_dim = len(sample["embeddings"][0])
            
            if actual_dim != expected_dim:
                print(f"✗ Dimension-Mismatch: {actual_dim} vs. {expected_dim}")
                print("Lösungsoptionen:")
                print("  1. Alte Collection löschen und neu erstellen")
                print("  2. Embedding-Modell wechseln")
                
                # Option: Collection zurücksetzen
                response = input("Collection neu erstellen? (j/n): ")
                if response.lower() == "j":
                    client.delete_collection(name=collection.name)
                    return client.get_or_create_collection(
                        name=collection.name,
                        metadata={"embedding_dim": str(expected_dim)}
                    )
            else:
                print(f"✓ Embedding-Dimension korrekt: {actual_dim}")
                return collection
    except Exception as e:
        raise RuntimeError(f"Fehler beim Check: {str(e)}")

# Verifiziere Modell-Dimensionen
EMBEDDING_DIMS = {
    "BAAI/bge-small-en-v1.5": 384,
    "BAAI/bge-base-en-v1.5": 768,
    "all-MiniLM-L6-v2": 384
}
```

---

### 4.3 Query Issues

#### ERROR: Empty Results despite existing data

**Symptom:**
```python
results = collection.query(...)
# results["documents"][0] = []  # Leer trotz Daten
```

**Root Cause:**
- Embedding-Modell-Mismatch
- Zu restriktive where/where_document Filter
- Query-Embedding nicht korrekt generiert
- Collection leer trotz Erwartung

**Lösung:**

```python
def debug_empty_results(collection, query_text):
    """Debugge leere Query-Ergebnisse"""
    
    # Schritt 1: Überprüfe Collection-Größe
    count = collection.count()
    print(f"Collection Größe: {count} Dokumente")
    
    if count == 0:
        print("✗ Collection ist leer!")
        return
    
    # Schritt 2: Versuche ohne Filter
    print("\n1. Query ohne Filter:")
    results_no_filter = collection.query(
        query_texts=[query_text],
        n_results=5,
        include=["documents", "distances"]
    )
    
    if results_no_filter["documents"][0]:
        print(f"✓ Ergebnisse ohne Filter: {len(results_no_filter['documents'][0])}")
    else:
        print("✗ Keine Ergebnisse - mögliches Embedding-Modell-Mismatch")
        return
    
    # Schritt 3: Überprüfe Sample-Dokumente
    print("\n2. Sample Dokumente:")
    sample = collection.get(limit=3, include=["documents", "metadatas"])
    for doc, meta in zip(sample["documents"], sample["metadatas"]):
        print(f"  - {doc[:60]}... ({meta})")
    
    # Schritt 4: Überprüfe Embedding-Dimension
    print("\n3. Embedding-Dimension:")
    sample_with_embed = collection.get(limit=1, include=["embeddings"])
    if sample_with_embed["embeddings"]:
        dim = len(sample_with_embed["embeddings"][0])
        print(f"  Aktuelle Dimension: {dim}")

# Verwendung
debug_empty_results(kern_collection, "APQP Prozess")
```

---

#### ERROR: Slow Query Performance (>2s)

**Symptom:**
```
Query dauert länger als 2 Sekunden
```

**Root Cause:**
- zu großes n_results
- zu restriktive where Filter (bearbeitet viele Dokumente)
- HNSW-Index nicht optimiert
- Storage-Performance-Probleme

**Lösung:**

```python
import time

def profile_query_performance(collection, query_text, n_results=5):
    """Analysiere Query-Performance"""
    
    start = time.time()
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "distances"]
    )
    elapsed = time.time() - start
    
    print(f"Query Zeit: {elapsed*1000:.1f}ms")
    
    if elapsed > 2:
        print("\n⚠ Slow Query - Optimierungs-Empfehlungen:")
        print("  1. Reduziere n_results (aktuell: {})".format(n_results))
        print("  2. Vereinfache where Filter")
        print("  3. Überprüfe ef_search Parameter")
        print("  4. Überprüfe Disk I/O Performance")
        
        # Tip: Versuche mit kleineren n_results
        for nr in [3, 1]:
            start = time.time()
            collection.query(
                query_texts=[query_text],
                n_results=nr
            )
            elapsed = time.time() - start
            print(f"  n_results={nr}: {elapsed*1000:.1f}ms")
    
    return results

# Profile verschiedene Queries
profile_query_performance(kern_collection, "APQP", n_results=5)
```

**Optimierungen:**

```python
# 1. Optimierte Query-Parameter
QUERY_CONFIG = {
    "n_results": 5,         # Limit Results
    "include": ["documents", "distances"],  # Nur nötige Felder
    # ef_search optional (später)
}

# 2. Caching für häufige Queries
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_query(query_text, n_results=5):
    """Cache Query-Ergebnisse"""
    return collection.query(
        query_texts=[query_text],
        n_results=n_results
    )

# 3. Batch-Queries besser als Loop
# ❌ Langsam:
for q in queries:
    result = collection.query(query_texts=[q], n_results=5)

# ✅ Schneller:
results = collection.query(
    query_texts=queries,  # Alle auf einmal
    n_results=5
)
```

---

#### ERROR: Wrong Results (Irrelevante Dokumente)

**Symptom:**
```
Query für "APQP" gibt Ergebnisse über "Crimpverbindungen"
```

**Root Cause:**
- Ähnliche Semantik, aber falsche Top-1 Ranking
- Embedding-Modell nicht optimal für Domain
- Embedding-Qualität niedrig

**Lösung:**

```python
def analyze_result_quality(collection, query_text, n_results=5):
    """Analysiere Qualität der Query-Ergebnisse"""
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )
    
    # Cosine Distance → Similarity Score
    scores = [1 - d for d in results["distances"][0]]
    
    print(f"Query: '{query_text}'")
    print(f"{'Rank':<5} {'Score':<8} {'Relevanz':<10} {'Text'}")
    print("-" * 70)
    
    for i, (doc, score, meta) in enumerate(zip(
        results["documents"][0],
        scores,
        results["metadatas"][0]
    ), 1):
        # Relevanz-Indikator
        if score > 0.8:
            relevanz = "✓✓✓ Sehr gut"
        elif score > 0.7:
            relevanz = "✓✓ Gut"
        elif score > 0.6:
            relevanz = "✓ OK"
        else:
            relevanz = "✗ Schlecht"
        
        print(f"{i:<5} {score:<8.3f} {relevanz:<10} {doc[:40]}...")
    
    # Schwellwert-Empfehlung
    min_score = min(scores)
    if min_score < 0.6:
        print(f"\n⚠ Warnung: Niedrigste Score {min_score:.3f}")
        print("  Empfehlung: Score-Schwellwert erhöhen auf 0.7")

# Analyse
analyze_result_quality(kern_collection, "Qualitätsmanagementsystem")

# Mit Re-Ranking für bessere Ergebnisse
def rerank_with_threshold(collection, query_text, threshold=0.7, n_results=10):
    """Filtre Ergebnisse auf Score-Schwellwert"""
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "distances"]
    )
    
    ranked = []
    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        score = 1 - dist
        if score >= threshold:
            ranked.append({"score": score, "text": doc})
    
    return ranked  # Nur hohe Confidence Ergebnisse
```

---

#### ERROR: n_results Limit Exceeded

**Symptom:**
```
ValueError: n_results must be <= collection.count()
```

**Root Cause:**
- Gefordertes n_results größer als Dokumente in Collection
- n_results größer als Dokumente, die where Filter erfüllen

**Lösung:**

```python
def safe_query(collection, query_text, requested_n_results=5):
    """Query mit automatischer n_results Anpassung"""
    
    # Überprüfe Collection-Größe
    collection_size = collection.count()
    
    # Berechne verfügbare Ergebnisse
    safe_n_results = min(requested_n_results, collection_size)
    
    if safe_n_results < requested_n_results:
        print(f"⚠ n_results reduziert: {requested_n_results} → {safe_n_results}")
        print(f"   (Collection Größe: {collection_size})")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=safe_n_results
    )
    
    return results

# Verwendung
results = safe_query(kern_collection, "APQP", requested_n_results=10)
# → Automatisch auf verfügbare Dokumente begrenzt
```

---

### 4.4 Embedding Issues

#### ERROR: Embedding function not set

**Symptom:**
```
ValueError: Embedding function is not set
```

**Root Cause:**
- Collection ohne Embedding Function erstellt
- Embedding Function bei Query nicht übergeben

**Lösung:**

```python
from chromadb.utils import embedding_functions

# Explizite Embedding Function Setting
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-en-v1.5"
)

# Mit Collection verbinden
collection = client.get_or_create_collection(
    name="osp_kern",
    embedding_function=emb_fn
)

# Oder nachträglich:
collection = client.get_collection(
    name="osp_kern",
    embedding_function=emb_fn  # Übergebe hier auch
)
```

---

#### ERROR: Custom embedding model not working

**Symptom:**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Root Cause:**
- HuggingFace Transformers nicht installiert
- Modell existiert nicht auf HuggingFace
- Falsche Model-ID

**Lösung:**

```bash
# Installiere erforderliche Packages
pip install sentence-transformers torch huggingface-hub

# Überprüfe Model-Verfügbarkeit
python -c "from sentence_transformers import SentenceTransformer; \
           m = SentenceTransformer('BAAI/bge-small-en-v1.5'); \
           print('✓ Model verfügbar')"
```

**Python-Code mit Fehlerbehandlung:**

```python
def create_embedding_function(model_name="BAAI/bge-small-en-v1.5"):
    """Erstelle Embedding Function mit Fehlerbehandlung"""
    
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError(
            "sentence-transformers erforderlich: "
            "pip install sentence-transformers"
        )
    
    try:
        # Test: Download Model (first use)
        model = SentenceTransformer(model_name)
        
        # Teste Embedding
        test_text = "Test"
        embedding = model.encode(test_text)
        
        if len(embedding) != 384 and "small" in model_name:
            raise ValueError(f"Dimension mismatch für {model_name}")
        
        print(f"✓ Embedding Function bereit: {model_name} ({len(embedding)}D)")
        
        # Zurück zu ChromaDB Format
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )
    
    except Exception as e:
        raise RuntimeError(f"Fehler beim Setup: {str(e)}")
```

---

#### ERROR: HuggingFace Model Download Fails

**Symptom:**
```
Connection error downloading model from huggingface.co
```

**Root Cause:**
- Keine Internet-Connection
- HuggingFace API Rate Limit
- Proxy/Firewall blockiert Downloads

**Lösung:**

```bash
# Offline Model-Download (einmalig)
mkdir -p ./models
huggingface-cli download BAAI/bge-small-en-v1.5 \
  --local-dir ./models/bge-small-en-v1.5

# Setze Umgebungsvariable
export HF_HOME=./models

# Python: Local Model verwenden
os.environ['HF_HOME'] = './models'

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('./models/bge-small-en-v1.5')
```

---

#### ERROR: Embedding Cache nicht persistent

**Symptom:**
```
Embeddings müssen jedes mal neu berechnet werden
```

**Root Cause:**
- ChromaDB speichert Embeddings nicht
- Manuelle Embedding-Caching nicht implementiert
- Docker Volume nicht persistent

**Lösung:**

```python
import pickle
import os

class EmbeddingCache:
    """Caching für berechnete Embeddings"""
    
    def __init__(self, cache_dir="./embedding_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_path(self, model_name, text):
        """Generiere Cache-Dateipfad"""
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()
        model_safe = model_name.replace("/", "_")
        return os.path.join(
            self.cache_dir,
            f"{model_safe}_{text_hash}.pkl"
        )
    
    def get(self, model_name, text):
        """Abrufe Embedding aus Cache"""
        path = self.get_cache_path(model_name, text)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def set(self, model_name, text, embedding):
        """Speichere Embedding in Cache"""
        path = self.get_cache_path(model_name, text)
        with open(path, 'wb') as f:
            pickle.dump(embedding, f)

# Verwendung
cache = EmbeddingCache()

texts = ["Text 1", "Text 2"]
embeddings = []

for text in texts:
    cached = cache.get("BAAI/bge-small-en-v1.5", text)
    if cached:
        embeddings.append(cached)
    else:
        embedding = embedding_function([text])[0]
        embeddings.append(embedding)
        cache.set("BAAI/bge-small-en-v1.5", text, embedding)
```

---

### 4.5 Production Issues

#### ERROR: ChromaDB Container Crashes

**Symptom:**
```
docker ps zeigt chromadb nicht mehr
Container restartet ständig
```

**Root Cause:**
- Out of Memory (OOM)
- Festplatte voll
- Corrupted Database
- Permission Errors

**Lösung:**

```bash
# 1. Logs überprüfen
docker logs chromadb --tail 100
docker logs chromadb --timestamps

# 2. Container-Ressourcen überprüfen
docker stats chromadb

# 3. Speicherplatz überprüfen
docker exec chromadb df -h

# 4. Manueller Restart
docker restart chromadb

# 5. Vollständiger Restart (mit Volume-Reset)
docker-compose down
docker-compose up -d chromadb

# 6. Health-Check
curl -I http://localhost:8000/api/v2
```

**docker-compose.yml Verbesserungen:**

```yaml
services:
  chromadb:
    image: chromadb/chroma:0.5.15
    restart: on-failure:5  # Nur 5x restart
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v2"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          memory: 2G  # Memory Limit
        reservations:
          memory: 1G  # Memory Reserve
    environment:
      - CHROMA_LOG_LEVEL=debug  # Debug-Logging
```

---

#### ERROR: Database Corruption after Restart

**Symptom:**
```
SQLite database disk image is malformed
Could not open collection
```

**Root Cause:**
- Ungraceful Shutdown
- Disk I/O Fehler
- Unvollständiger Schreibzugriff

**Lösung:**

```python
def check_database_integrity(client):
    """Überprüfe Datenbank-Integrität"""
    
    try:
        # Versuche Zugriff auf Collections
        collections = client.list_collections()
        
        for col in collections:
            count = col.count()
            print(f"✓ Collection '{col.name}': {count} Dokumente")
        
        print("✓ Datenbank-Integrität OK")
        return True
    
    except Exception as e:
        print(f"✗ Datenbank-Fehler: {str(e)}")
        return False

def repair_database(backup_path, data_path):
    """Datenbank aus Backup wiederherstellen"""
    import shutil
    
    if os.path.exists(backup_path):
        print("Restoriere aus Backup...")
        shutil.rmtree(data_path, ignore_errors=True)
        shutil.copytree(backup_path, data_path)
        print("✓ Backup restauriert")
    else:
        print("✗ Kein Backup verfügbar")

# Startup-Überprüfung
client = chromadb.PersistentClient(path="/mnt/HC_Volume_104189729/osp/chromadb/data")
if not check_database_integrity(client):
    repair_database(
        "/backups/chromadb_backup",
        "/mnt/HC_Volume_104189729/osp/chromadb/data"
    )
```

---

#### ERROR: Migration zwischen Versionen

**Symptom:**
```
Collection format incompatible with ChromaDB 0.5.x
```

**Root Cause:**
- ChromaDB-Version wurde aktualisiert
- Datenformat zwischen Versionen nicht kompatibel

**Lösung:**

```python
def migrate_chromadb_version(old_path, new_path):
    """Migriere ChromaDB auf neue Version"""
    
    import json
    
    # 1. Alte Datenbank auslesen
    old_client = chromadb.PersistentClient(path=old_path)
    
    all_data = {}
    for collection in old_client.list_collections():
        print(f"Exportiere Collection: {collection.name}")
        
        data = collection.get(
            include=["documents", "metadatas", "embeddings", "ids"]
        )
        all_data[collection.name] = data
    
    # 2. In Datei speichern
    with open("chromadb_migration.json", "w") as f:
        # embeddings sind Floats, nicht JSON-serializable
        safe_data = {
            name: {
                k: v for k, v in data.items() 
                if k != "embeddings"
            }
            for name, data in all_data.items()
        }
        json.dump(safe_data, f, indent=2)
    
    # 3. Neue Datenbank erstellen und füllen
    new_client = chromadb.PersistentClient(path=new_path)
    
    for col_name, col_data in all_data.items():
        print(f"Importiere Collection: {col_name}")
        
        new_col = new_client.get_or_create_collection(name=col_name)
        
        new_col.add(
            ids=col_data["ids"],
            documents=col_data["documents"],
            metadatas=col_data["metadatas"],
            embeddings=col_data["embeddings"]  # Re-import embeddings
        )
    
    print("✓ Migration abgeschlossen")

# Verwendung
migrate_chromadb_version(
    "/mnt/HC_Volume_104189729/osp/chromadb/data_old",
    "/mnt/HC_Volume_104189729/osp/chromadb/data_new"
)
```

---

## 5. Performance Optimization

### 5.1 HNSW Index Tuning

#### Tuning für kleine Datasets (51 Dokumente)

```python
# Optimale Parameter für OSP-System
HNSW_OPTIMAL = {
    "hnsw:space": "cosine",        # Distance Metric
    "hnsw:M": "16",                # Connectivity (Standard)
    "hnsw:ef_construction": "200"   # Build Quality
}

collection = client.get_or_create_collection(
    name="osp_kern",
    metadata=HNSW_OPTIMAL
)
```

**Tuning-Strategie basierend auf Benchmarks:**

```python
def benchmark_hnsw_parameters(collection, test_queries, params_to_test):
    """Benchmark verschiedene HNSW-Konfigurationen"""
    
    import time
    import json
    
    results = {}
    
    for params in params_to_test:
        M = params.get("M", 16)
        ef_construction = params.get("ef_construction", 200)
        
        config_name = f"M{M}_ef{ef_construction}"
        
        # Erstelle Test-Collection mit Parametern
        test_col = client.get_or_create_collection(
            name=f"test_{config_name}",
            metadata={
                "hnsw:space": "cosine",
                "hnsw:M": str(M),
                "hnsw:ef_construction": str(ef_construction)
            }
        )
        
        # Füge Test-Daten ein
        # ... (Dokumente hinzufügen)
        
        # Benchmark Queries
        total_time = 0
        for query in test_queries:
            start = time.time()
            test_col.query(query_texts=[query], n_results=5)
            total_time += time.time() - start
        
        avg_query_time = total_time / len(test_queries)
        
        results[config_name] = {
            "M": M,
            "ef_construction": ef_construction,
            "avg_query_time_ms": avg_query_time * 1000
        }
        
        # Cleanup
        client.delete_collection(name=f"test_{config_name}")
    
    # Ausgabe
    print("HNSW Benchmark Results:")
    print(json.dumps(results, indent=2))
    
    return results
```

#### Parameter-Empfehlungen

```python
HNSW_CONFIGURATIONS = {
    "fast": {
        "hnsw:M": "8",
        "hnsw:ef_construction": "100",
        "use_case": "Real-time, many queries, high QPS"
    },
    "balanced": {
        "hnsw:M": "16",
        "hnsw:ef_construction": "200",
        "use_case": "Standard, OSP Production"
    },
    "quality": {
        "hnsw:M": "24",
        "hnsw:ef_construction": "400",
        "use_case": "Batch processing, recall-critical"
    }
}

# OSP-System → "balanced"
osp_config = HNSW_CONFIGURATIONS["balanced"]
```

---

### 5.2 Query Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

class QueryCache:
    """LRU-Cache für häufige Queries mit TTL"""
    
    def __init__(self, max_size=128, ttl_seconds=3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def get_cache_key(self, query_text, n_results, where=None):
        """Generiere Cache-Key"""
        key = (query_text, n_results, str(where))
        return hash(key)
    
    def get(self, key):
        """Abrufe aus Cache (mit TTL-Check)"""
        if key in self.cache:
            result, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return result
            else:
                del self.cache[key]  # Expired
        return None
    
    def set(self, key, value):
        """Speichere in Cache"""
        if len(self.cache) >= self.max_size:
            # Entferne ältesten Entry
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, datetime.now())
    
    def clear(self):
        """Leere Cache"""
        self.cache.clear()

# Verwendung
query_cache = QueryCache(max_size=256, ttl_seconds=1800)

def cached_query(collection, query_text, n_results=5, use_cache=True):
    """Query mit optionalem Caching"""
    
    cache_key = query_cache.get_cache_key(query_text, n_results)
    
    if use_cache:
        cached_result = query_cache.get(cache_key)
        if cached_result:
            print(f"Cache HIT: {query_text[:40]}...")
            return cached_result
    
    # Cache MISS - Führe Query aus
    result = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    query_cache.set(cache_key, result)
    return result
```

---

### 5.3 Batch Operations

```python
def batch_query_optimize(collection, queries, batch_size=None):
    """Optimierte Batch-Query-Verarbeitung"""
    
    if batch_size is None:
        # Standard: alle auf einmal
        batch_size = len(queries)
    
    all_results = []
    
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        
        result = collection.query(
            query_texts=batch,
            n_results=5,
            include=["documents", "distances"]
        )
        
        all_results.extend([
            {
                "query": batch[j],
                "results": result["documents"][j],
                "scores": [1 - d for d in result["distances"][j]]
            }
            for j in range(len(batch))
        ])
    
    return all_results

# Vergleich: Batch vs. Loop
import time

queries = [f"Query {i}" for i in range(20)]

# ❌ Langsam: Loop
start = time.time()
for q in queries:
    collection.query(query_texts=[q], n_results=5)
loop_time = time.time() - start

# ✅ Schneller: Batch
start = time.time()
batch_query_optimize(collection, queries)
batch_time = time.time() - start

print(f"Loop Zeit: {loop_time:.3f}s")
print(f"Batch Zeit: {batch_time:.3f}s")
print(f"Speedup: {loop_time/batch_time:.1f}x")
```

---

### 5.4 Memory Management

```python
import psutil
import os

class ChromaDBMemoryMonitor:
    """Überwache ChromaDB Memory-Usage"""
    
    def __init__(self, pid=None):
        self.process = psutil.Process(pid)
    
    def get_memory_usage(self):
        """Hole Memory-Statistiken"""
        memory = self.process.memory_info()
        memory_mb = memory.rss / 1024 / 1024
        return {
            "rss_mb": memory_mb,  # Resident Set Size
            "percent": self.process.memory_percent(),
            "available_mb": psutil.virtual_memory().available / 1024 / 1024
        }
    
    def report(self):
        """Erstelle Memory-Report"""
        mem = self.get_memory_usage()
        print(f"ChromaDB Memory Usage:")
        print(f"  RSS: {mem['rss_mb']:.1f} MB")
        print(f"  % of System: {mem['percent']:.1f}%")
        print(f"  Available: {mem['available_mb']:.1f} MB")
        
        if mem['rss_mb'] > 500:
            print("⚠ High memory usage!")
    
    def check_threshold(self, threshold_mb=500):
        """Überprüfe Memory-Schwellwert"""
        mem = self.get_memory_usage()
        if mem['rss_mb'] > threshold_mb:
            return False, mem['rss_mb']
        return True, mem['rss_mb']

# Verwendung
monitor = ChromaDBMemoryMonitor()
monitor.report()

is_ok, usage = monitor.check_threshold(threshold_mb=500)
if not is_ok:
    print(f"⚠ Memory Schwellwert überschritten: {usage:.1f} MB")
```

**Memory-Optimierungen:**

```python
# 1. Limit Query-Results
results = collection.query(
    query_texts=queries,
    n_results=5,  # Nicht zu groß
    include=["documents", "distances"]  # Nicht "embeddings"
)

# 2. Batch-Prozessierung mit Cleanup
for batch in batches:
    results = collection.query(...)
    process_results(results)
    # results wird GC'd

# 3. Periodische Collection-Cleanup
def cleanup_collection(collection, keep_latest=True):
    """Entferne doppelte/alte Dokumente"""
    # Implementierung je nach Use-Case
    pass
```

---

### 5.5 Disk I/O Optimization

```python
import sqlite3

class DiskIOOptimizer:
    """Optimiere Disk I/O für ChromaDB"""
    
    @staticmethod
    def optimize_sqlite_settings(db_path):
        """Optimiere SQLite für bessere I/O"""
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Optimierungen
        cursor.execute("PRAGMA journal_mode = WAL")    # Write-Ahead Logging
        cursor.execute("PRAGMA synchronous = NORMAL")  # Weniger fsync
        cursor.execute("PRAGMA cache_size = 10000")    # Größerer Cache
        cursor.execute("PRAGMA temp_store = MEMORY")   # Temp in RAM
        
        conn.commit()
        conn.close()
        
        print("✓ SQLite I/O Optimierungen angewendet")

# Anwendung nach ChromaDB-Startup
db_path = "/mnt/HC_Volume_104189729/osp/chromadb/data/chroma.sqlite3"
if os.path.exists(db_path):
    DiskIOOptimizer.optimize_sqlite_settings(db_path)
```

---

## 6. Integration Patterns

### 6.1 LlamaIndex ChromaVectorStore Integration

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# ChromaDB Client setup
import chromadb

chroma_client = chromadb.PersistentClient(
    path="/mnt/HC_Volume_104189729/osp/chromadb/data"
)

kern_collection = chroma_client.get_or_create_collection(
    name="osp_kern",
    metadata={"description": "OSP Kern-Dokumente"}
)

# LlamaIndex Integration
vector_store = ChromaVectorStore(chroma_collection=kern_collection)

# Index erstellen
index = VectorStoreIndex.from_vector_store(vector_store)

# Query Engine
query_engine = index.as_query_engine()

# Query ausführen
response = query_engine.query(
    "Was ist APQP und wie ist der Prozess aufgebaut?"
)

print(response)
```

### 6.2 LangChain ChromaDB Integration

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings  # oder andere
from langchain_core.documents import Document

# ChromaDB via LangChain
vectorstore = Chroma(
    client=chroma_client,
    collection_name="osp_kern",
    embedding_function=OpenAIEmbeddings()  # oder Custom
)

# Documents hinzufügen
documents = [
    Document(page_content="APQP ist...", metadata={"type": "apqp"}),
    Document(page_content="Control Plan...", metadata={"type": "control_plan"})
]

vectorstore.add_documents(documents)

# Query
results = vectorstore.similarity_search(
    "APQP Prozess",
    k=5,
    filter={"type": "apqp"}  # Metadata filtering
)

print(results)
```

### 6.3 Custom Embedding Functions mit LlamaIndex

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Custom HuggingFace Embedding
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./models"
)

# Mit VectorStoreIndex nutzen
from llama_index.core import VectorStoreIndex, Settings

Settings.embed_model = embed_model

index = VectorStoreIndex.from_vector_store(
    vector_store=ChromaVectorStore(chroma_collection=kern_collection),
    embed_model=embed_model
)
```

---

## 7. Backup & Migration

### 7.1 Database Backup Strategies

#### Automatische tägliche Backups

```python
import shutil
from datetime import datetime
import os

class BackupManager:
    """Verwalte ChromaDB Backups"""
    
    def __init__(self, source_path, backup_dir="./chromadb_backups"):
        self.source_path = source_path
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, tag=""):
        """Erstelle Backup mit Timestamp"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"chromadb_backup_{timestamp}"
        if tag:
            backup_name += f"_{tag}"
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copytree(self.source_path, backup_path)
            print(f"✓ Backup erstellt: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"✗ Backup fehlgeschlagen: {str(e)}")
            return None
    
    def restore_backup(self, backup_path):
        """Stelle aus Backup wieder her"""
        
        try:
            # Backup des aktuellen State vor Restore
            self.create_backup(tag="pre_restore")
            
            # Entferne alte Datenbank
            shutil.rmtree(self.source_path, ignore_errors=True)
            
            # Kopiere Backup zurück
            shutil.copytree(backup_path, self.source_path)
            
            print(f"✓ Restore abgeschlossen: {backup_path}")
            return True
        except Exception as e:
            print(f"✗ Restore fehlgeschlagen: {str(e)}")
            return False
    
    def list_backups(self):
        """Liste alle verfügbaren Backups auf"""
        backups = sorted(os.listdir(self.backup_dir))
        for backup in backups:
            path = os.path.join(self.backup_dir, backup)
            size_mb = sum(os.path.getsize(os.path.join(path, f)) 
                         for f in os.listdir(path)) / 1024 / 1024
            print(f"  {backup} ({size_mb:.1f} MB)")
        return backups
    
    def cleanup_old_backups(self, keep_count=7):
        """Behalte nur die letzten N Backups"""
        backups = sorted(os.listdir(self.backup_dir))
        
        if len(backups) > keep_count:
            to_delete = backups[:-keep_count]
            
            for backup in to_delete:
                path = os.path.join(self.backup_dir, backup)
                shutil.rmtree(path)
                print(f"  Gelöscht: {backup}")

# Verwendung
backup_mgr = BackupManager(
    source_path="/mnt/HC_Volume_104189729/osp/chromadb/data",
    backup_dir="./chromadb_backups"
)

# Täglicher Backup
backup_mgr.create_backup(tag="daily")

# Cleanup: Behalte 7 tägliche Backups
backup_mgr.cleanup_old_backups(keep_count=7)

# Übersicht
print("Verfügbare Backups:")
backup_mgr.list_backups()
```

#### Cron Job für automatische Backups

```bash
# crontab -e
# Täglich um 02:00 Uhr Backup erstellen
0 2 * * * python /mnt/HC_Volume_104189729/osp/scripts/backup_chromadb.py

# Wöchentlich (Sonntag um 03:00) alten Backup löschen
0 3 * * 0 python /mnt/HC_Volume_104189729/osp/scripts/cleanup_backups.py
```

**backup_chromadb.py:**

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/mnt/HC_Volume_104189729/osp')

from chromadb_backup import BackupManager

backup_mgr = BackupManager(
    source_path="/mnt/HC_Volume_104189729/osp/chromadb/data",
    backup_dir="/mnt/HC_Volume_104189729/osp/backups/chromadb"
)

backup_path = backup_mgr.create_backup(tag="daily")
if backup_path:
    # Log Backup-Success
    with open("/mnt/HC_Volume_104189729/osp/logs/chromadb_backup.log", "a") as f:
        from datetime import datetime
        f.write(f"{datetime.now().isoformat()} - Backup OK\n")

backup_mgr.cleanup_old_backups(keep_count=30)  # 30 Tage
```

---

### 7.2 Collection Export/Import

```python
import json

def export_collection_to_json(collection, output_file):
    """Exportiere Collection in JSON"""
    
    # Abrufen aller Daten
    all_data = collection.get(
        include=["documents", "metadatas", "ids"]
    )
    
    # Embeddings separat speichern (für Portabilität)
    data_with_embeddings = collection.get(
        include=["embeddings", "ids"]
    )
    
    export_data = {
        "collection_name": collection.name,
        "metadata": collection.metadata or {},
        "documents": {
            "ids": all_data["ids"],
            "documents": all_data["documents"],
            "metadatas": all_data["metadatas"]
        },
        "embeddings": {
            "ids": data_with_embeddings["ids"],
            "embeddings": data_with_embeddings["embeddings"]
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Collection exportiert: {output_file}")
    print(f"  Dokumente: {len(all_data['ids'])}")

def import_collection_from_json(client, json_file):
    """Importiere Collection aus JSON"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    col_name = data["collection_name"]
    
    # Erstelle Collection
    collection = client.get_or_create_collection(
        name=col_name,
        metadata=data.get("metadata", {})
    )
    
    # Füge Dokumente ein
    doc_data = data["documents"]
    embed_data = data["embeddings"]
    
    # Match IDs für Embeddings
    embeddings = []
    for id in doc_data["ids"]:
        idx = embed_data["ids"].index(id)
        embeddings.append(embed_data["embeddings"][idx])
    
    collection.add(
        ids=doc_data["ids"],
        documents=doc_data["documents"],
        metadatas=doc_data["metadatas"],
        embeddings=embeddings
    )
    
    print(f"✓ Collection importiert: {col_name}")
    print(f"  Dokumente: {len(doc_data['ids'])}")
    
    return collection

# Export
export_collection_to_json(
    kern_collection,
    "osp_kern_export.json"
)

# Import in andere Instanz
new_client = chromadb.PersistentClient(path="/new/path")
imported_col = import_collection_from_json(
    new_client,
    "osp_kern_export.json"
)
```

---

### 7.3 Cross-Environment Migration

```python
def migrate_between_environments(source_host, target_host, collection_names):
    """Migriere Collections zwischen Environments"""
    
    # 1. Verbinde mit Source-Environment
    source_client = chromadb.HttpClient(
        host=source_host,
        port=8000
    )
    
    # 2. Verbinde mit Target-Environment
    target_client = chromadb.HttpClient(
        host=target_host,
        port=8000
    )
    
    # 3. Für jede Collection: Export/Import
    for col_name in collection_names:
        print(f"\nMigriere {col_name}...")
        
        source_col = source_client.get_collection(name=col_name)
        
        # Export
        data = source_col.get(
            include=["documents", "metadatas", "embeddings", "ids"]
        )
        
        # Import in Target
        target_col = target_client.get_or_create_collection(
            name=col_name,
            metadata=source_col.metadata
        )
        
        target_col.add(
            ids=data["ids"],
            documents=data["documents"],
            metadatas=data["metadatas"],
            embeddings=data["embeddings"]
        )
        
        print(f"✓ {col_name}: {len(data['ids'])} Dokumente migriert")

# Migrations-Script
migrate_between_environments(
    source_host="localhost:8000",  # Production
    target_host="staging:8000",     # Staging
    collection_names=["osp_kern", "osp_erweitert"]
)
```

---

## 8. Docker Deployment

### 8.1 docker-compose.yml Konfiguration

```yaml
version: '3.8'

services:
  chromadb:
    image: chromadb/chroma:0.5.15
    container_name: osp_chromadb
    
    # Port Mapping
    ports:
      - "8000:8000"
    
    # Persistent Storage
    volumes:
      - ./chromadb_data:/chroma/chroma
      - ./chromadb_config:/chroma/chroma/config
    
    # Environment Variables
    environment:
      # Telemetry & Logging
      - CHROMA_TELEMETRY_DISABLED=true
      - CHROMA_LOG_LEVEL=info
      
      # Persistence
      - PERSIST_DIRECTORY=/chroma/chroma
      - IS_PERSISTENT=true
      
      # Performance
      - CHROMA_SERVER_WORKERS=4
      - CHROMA_SERVER_THREAD_POOL_SIZE=16
      
      # Security (Token-based Auth)
      - CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER=chromadb.auth.token.TokenAuthCredentialsProvider
      - CHROMA_SERVER_AUTH_TOKEN_TRANSPORT_HEADER=X_CHROMA_TOKEN
      - CHROMA_SERVER_AUTH_TOKEN=osp_prod_token_123456
    
    # Restart Policy
    restart: unless-stopped
    
    # Health Check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v2/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # Resource Limits
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
    
    # Logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

# Persistent Storage Definition
volumes:
  chromadb_data:
    driver: local
  chromadb_config:
    driver: local

networks:
  default:
    name: osp_network
    driver: bridge
```

### 8.2 Docker Startup & Monitoring

```bash
#!/bin/bash
# start_chromadb.sh

# Vorbereitung
mkdir -p ./chromadb_data
mkdir -p ./chromadb_config
chmod 755 ./chromadb_data

echo "Starting ChromaDB..."

# Docker Compose Start
docker-compose -f docker-compose.yml up -d chromadb

# Warte auf Startup
echo "Waiting for ChromaDB to be ready..."
for i in {1..30}; do
  if curl -f http://localhost:8000/api/v2/heartbeat > /dev/null 2>&1; then
    echo "✓ ChromaDB ist online"
    break
  fi
  echo "  Versuch $i/30..."
  sleep 2
done

# Health Check
if curl -f http://localhost:8000/api/v2 > /dev/null 2>&1; then
  echo "✓ ChromaDB gesund und bereit"
  docker-compose logs chromadb | tail -20
else
  echo "✗ ChromaDB nicht erreichbar!"
  docker-compose logs chromadb
  exit 1
fi
```

---

## 9. Code Examples

### 9.1 Complete Setup Example

```python
"""
Complete ChromaDB Setup für OSP Production System
"""

import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import hashlib
import os

class OSPChromaDB:
    """Wrapper für OSP ChromaDB Operations"""
    
    def __init__(self, 
                 db_path="/mnt/HC_Volume_104189729/osp/chromadb/data",
                 embedding_model="BAAI/bge-small-en-v1.5"):
        
        # Client initialisieren
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Embedding Function setup
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )
        
        # Collections initialisieren
        self.kern_collection = self.client.get_or_create_collection(
            name="osp_kern",
            embedding_function=self.embedding_fn,
            metadata={
                "description": "OSP Kern-Dokumente",
                "embedding_model": embedding_model,
                "embedding_dimension": "384",
                "created_date": datetime.now().isoformat()
            }
        )
        
        self.erweitert_collection = self.client.get_or_create_collection(
            name="osp_erweitert",
            embedding_function=self.embedding_fn,
            metadata={
                "description": "OSP Erweiterte Dokumente",
                "embedding_model": embedding_model
            }
        )
    
    def add_document(self, 
                     text: str, 
                     doc_type: str,
                     metadata: dict = None,
                     collection_name: str = "osp_kern") -> str:
        """Füge Dokument hinzu und returne ID"""
        
        # ID generieren
        doc_id = hashlib.md5(text.encode()).hexdigest()[:16]
        
        # Metadata vorbereiten
        meta = {
            "doc_type": doc_type,
            "created_date": datetime.now().isoformat(),
            "source": "internal"
        }
        if metadata:
            meta.update(metadata)
        
        # Je nach Collection
        if collection_name == "osp_kern":
            collection = self.kern_collection
        else:
            collection = self.erweitert_collection
        
        # Hinzufügen
        collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[meta]
        )
        
        return doc_id
    
    def query(self, 
              query_text: str,
              n_results: int = 5,
              collection_name: str = "osp_kern",
              where: dict = None) -> list:
        """Führe Query aus"""
        
        collection = (self.kern_collection 
                     if collection_name == "osp_kern" 
                     else self.erweitert_collection)
        
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
            include=["documents", "distances", "metadatas"]
        )
        
        # Formatiere Ergebnisse
        output = []
        for doc, dist, meta in zip(
            results["documents"][0],
            results["distances"][0],
            results["metadatas"][0]
        ):
            output.append({
                "text": doc,
                "score": 1 - dist,  # Cosine to Similarity
                "metadata": meta
            })
        
        return output
    
    def stats(self):
        """Zeige Statistics"""
        print("OSP ChromaDB Statistics:")
        print(f"  osp_kern: {self.kern_collection.count()} Dokumente")
        print(f"  osp_erweitert: {self.erweitert_collection.count()} Dokumente")

# Verwendung
if __name__ == "__main__":
    # Initialize
    osp_db = OSPChromaDB()
    
    # Add Documents
    doc1_id = osp_db.add_document(
        text="APQP ist der Advanced Product Quality Planning Prozess...",
        doc_type="apqp",
        metadata={"version": "1.0", "author": "QM"}
    )
    
    # Query
    results = osp_db.query("APQP Prozessablauf")
    
    for r in results:
        print(f"[{r['score']:.2%}] {r['text'][:60]}...")
    
    # Stats
    osp_db.stats()
```

---

### 9.2 Batch Import mit Error Handling

```python
import csv
from typing import List, Dict

def batch_import_documents(collection, 
                          csv_file: str,
                          batch_size: int = 50) -> Dict:
    """
    Importiere Dokumente aus CSV-Datei in Batches
    
    CSV Format:
    id,text,doc_type,version,status
    """
    
    documents = []
    
    # Lese CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            documents.append(row)
    
    # Batch Processing
    total = len(documents)
    added = 0
    failed = 0
    
    for i in range(0, total, batch_size):
        batch = documents[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        try:
            ids = [doc['id'] for doc in batch]
            texts = [doc['text'] for doc in batch]
            metadatas = [
                {
                    'doc_type': doc.get('doc_type', 'unknown'),
                    'version': doc.get('version', '1.0'),
                    'status': doc.get('status', 'active')
                }
                for doc in batch
            ]
            
            collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            added += len(batch)
            print(f"✓ Batch {batch_num}: {len(batch)} Dokumente")
            
        except Exception as e:
            failed += len(batch)
            print(f"✗ Batch {batch_num} fehlgeschlagen: {str(e)}")
    
    return {
        "total": total,
        "added": added,
        "failed": failed,
        "success_rate": (added / total * 100) if total > 0 else 0
    }

# Verwendung
result = batch_import_documents(
    kern_collection,
    "osp_documents.csv",
    batch_size=50
)

print(f"Import Summary:")
print(f"  Total: {result['total']}")
print(f"  Added: {result['added']}")
print(f"  Failed: {result['failed']}")
print(f"  Success Rate: {result['success_rate']:.1f}%")
```

---

## 10. Best Practices Checklist

### Pre-Production Checklist

- [ ] **PersistentClient für Production** verwenden
- [ ] **get_or_create_collection()** statt create_collection()
- [ ] **Unique Document IDs** (MD5 Hash oder UUID)
- [ ] **Metadata Schema** dokumentiert und standardisiert
- [ ] **HNSW Index** auf M=16, ef_construction=200 tuned
- [ ] **Health Checks** in docker-compose.yml konfiguriert
- [ ] **Resource Limits** (CPU, Memory) festgelegt
- [ ] **Docker Volume** für Persistence konfiguriert
- [ ] **Backup Strategy** implementiert (täglich)
- [ ] **Monitoring/Logging** eingerichtet

### Runtime Checklist

- [ ] **Regular Backups** (täglich/wöchentlich)
- [ ] **Memory Usage** überwachen (<500MB für 51 Docs)
- [ ] **Query Performance** monitoren (<2s)
- [ ] **Embedding Dimension** verifiziert (384)
- [ ] **Collection Count** regelmäßig überprüfen
- [ ] **Error Logging** aktiviert
- [ ] **Connection Pooling** (bei HttpClient)
- [ ] **Cache Strategy** implementiert

### Security Checklist

- [ ] **Authentication** aktiviert (Token-based)
- [ ] **Environment Secrets** nicht hardcoded
- [ ] **Docker Container** als non-root user
- [ ] **Volume Permissions** korrekt gesetzt
- [ ] **Firewall Rules** eingerichtet (nur Port 8000 intern)
- [ ] **Data Encryption** (bei sensiblen Daten)

---

## Appendix: HNSW Index Tuning Guide

### HNSW Konzepte

**HNSW** (Hierarchical Navigable Small World) ist eine Graphen-basierte Indexierungsmethode für Nearest Neighbor Search.

```
Struktur:
Layer 2: [○]----[○]
         /         \
Layer 1: [●]--[●]--[○]--[○]
         /    \            \
Layer 0: [●]--[●]--[●]--[○]--[○]--[●]
```

### Parameter-Impact

| Parameter | Standard | Impact auf Query | Impact auf Build | Memory |
|-----------|----------|-----------------|------------------|--------|
| M | 16 | Connectivity | Build-Zeit | +10% pro +1 |
| ef_construction | 200 | Recall | +5% pro +50 | 0% |
| ef_search | ef_con | Query-Zeit | N/A | 0% |

### Tuning-Strategie

```python
# 1. Baseline: Default Parameters
default_config = {
    "hnsw:space": "cosine",
    "hnsw:M": "16",
    "hnsw:ef_construction": "200"
}

# 2. Wenn Recall schlecht → ef_construction erhöhen
high_recall_config = {
    "hnsw:M": "16",
    "hnsw:ef_construction": "400"  # 2x höher
}

# 3. Wenn Query zu langsam → ef_search reduzieren (query-time)
# oder M reduzieren (permanent)

# 4. Wenn Memory zu hoch → M reduzieren
low_memory_config = {
    "hnsw:M": "8",
    "hnsw:ef_construction": "100"
}
```

### Empfehlungen nach Dataset-Größe

```python
HNSW_BY_SIZE = {
    "tiny": {        # 1-100 Dokumente
        "M": "8",
        "ef_construction": "100"
    },
    "small": {       # 100-1K (OSP-System hier)
        "M": "16",
        "ef_construction": "200"
    },
    "medium": {      # 1K-100K
        "M": "20",
        "ef_construction": "300"
    },
    "large": {       # 100K+
        "M": "24",
        "ef_construction": "400"
    }
}

# OSP: 51 Dokumente → "small" config
osp_config = HNSW_BY_SIZE["small"]
```

---

## Troubleshooting Flowchart

```
Problem gemeldet
    ↓
[Fehler-Kategorie?]
    ├─→ Connection Error ─→ Container läuft? → Port frei?
    ├─→ Collection Error ─→ Collection existiert? → ID unique?
    ├─→ Query Error ─→ Embedding-Modell Match? → n_results OK?
    ├─→ Performance ─→ Batch-Queries? → HNSW tuned?
    └─→ Data Corruption ─→ Aus Backup restore
```

---

## Support & Weiterführende Ressourcen

**Offizielle Dokumentation:**
- https://docs.trychroma.com
- https://github.com/chroma-core/chroma
- https://cookbook.chromadb.dev

**Häufige Issues:**
- GitHub Issues: chroma-core/chroma
- Reddit: r/vectordatabase
- Stack Overflow: Tag "chromadb"

**Kontakt OSP-Team:**
- QM: [Email]
- IT-Support: [Email]
- Backup-Location: /mnt/HC_Volume_104189729/osp/backups/

---

## Version History

| Version | Datum | Änderungen |
|---------|-------|----------|
| 1.0 | 2025-12-11 | Initial Production Guide |
| | | ChromaDB 0.5.15 |
| | | 10 Hauptkapitel |
| | | 50+ Code Examples |

---

**Ende der Dokumentation**