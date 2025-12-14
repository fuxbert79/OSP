#!/usr/bin/env python3
"""
OSP ChromaDB Reindexierung mit intfloat/multilingual-e5-large
=============================================================

Dieses Skript:
1. Löscht alle bestehenden Collections
2. Erstellt neue Collections mit E5-large Embeddings (1024 Dimensionen)
3. Indiziert alle Dokumente neu

WICHTIG: E5-Modelle benötigen Präfixe:
- "passage: " für Dokumente
- "query: " für Suchanfragen

Erstellt: 2025-12-14
"""

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# KONFIGURATION
# =============================================================================

CHROMADB_HOST = "localhost"
CHROMADB_PORT = 8000

EMBEDDING_MODEL = "intfloat/multilingual-e5-large"
EMBEDDING_DIM = 1024

# Dokumentenpfade
PATHS = {
    "osp_kern": "/opt/osp/documents",
    "osp_erweitert": "/opt/osp/documents_erweitert",
    "osp_kpl": "/opt/osp/documents_kpl"
}

# Chunking-Parameter
CHUNK_SIZE = 4800   # Zeichen
CHUNK_OVERLAP = 600 # Zeichen

# Full-Document Mode für diese Dateien (keine Chunks)
FULL_DOC_FILES = [
    "TM_CORE_Maschinen_Anlagen.md",
    "TM_WKZ_Werkzeuge.md",
    "HR_CORE_Personalstamm.md",
    "AV_AGK_Arbeitsgang_Katalog.md",
    "OSP_Navigator.md",
    "DMS_FORM_Formblaetter.md"
]


# =============================================================================
# CUSTOM EMBEDDING FUNCTION FÜR E5
# =============================================================================

class E5LargeEmbeddingFunction(EmbeddingFunction[Documents]):
    """
    Custom Embedding Function für intfloat/multilingual-e5-large.

    E5-Modelle erfordern spezielle Präfixe:
    - "passage: " für Dokumente beim Indizieren
    - "query: " für Suchanfragen

    Diese Klasse fügt automatisch "passage: " hinzu für Dokumente.
    Für Queries muss die Pipeline/App "query: " voranstellen.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        logger.info(f"Lade Embedding-Modell: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Modell geladen. Dimension: {self.dimension}")

    def __call__(self, input: Documents) -> Embeddings:
        """
        Erstelle Embeddings für Dokumente.
        Fügt automatisch "passage: " Präfix hinzu.
        """
        # E5 erfordert "passage: " Präfix für Dokumente
        prefixed = [f"passage: {doc}" for doc in input]
        embeddings = self.model.encode(prefixed, normalize_embeddings=True)
        return embeddings.tolist()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_doc_id(filename: str, chunk_index: int = 0) -> str:
    """Generiere eindeutige Document ID"""
    base = f"{filename}_{chunk_index}"
    return hashlib.md5(base.encode()).hexdigest()[:16]


def extract_tag_from_filename(filename: str) -> tuple:
    """Extrahiere TAG und SUBTAG aus Dateiname"""
    name = filename.replace(".md", "")
    parts = name.split("_", 2)
    if len(parts) >= 2:
        return parts[0], parts[1]
    return parts[0], ""


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Teile Text in Chunks mit Überlappung (nach Markdown-Headern)"""
    chunks = []

    # Nach Markdown-Headern splitten
    sections = re.split(r'\n(?=#{1,3}\s)', text)

    current_chunk = ""

    for section in sections:
        if len(current_chunk) + len(section) <= chunk_size:
            current_chunk += section
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # Überlappung beibehalten
            if overlap > 0 and current_chunk:
                overlap_text = current_chunk[-overlap:]
                current_chunk = overlap_text + section
            else:
                current_chunk = section

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks if chunks else [text]


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def delete_all_collections(client: chromadb.HttpClient) -> None:
    """Lösche alle bestehenden Collections"""
    logger.info("Lösche bestehende Collections...")

    collections = client.list_collections()
    for col in collections:
        logger.info(f"  Lösche: {col.name}")
        client.delete_collection(col.name)

    logger.info(f"  ✓ {len(collections)} Collections gelöscht")


def import_collection(
    client: chromadb.HttpClient,
    collection_name: str,
    base_path: str,
    embedding_fn: E5LargeEmbeddingFunction
) -> int:
    """Importiere Dokumente in eine Collection"""

    logger.info(f"\n{'='*60}")
    logger.info(f"Collection: {collection_name}")
    logger.info(f"Pfad: {base_path}")
    logger.info(f"{'='*60}")

    # Collection erstellen
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
        metadata={
            "description": f"OSP Collection: {collection_name}",
            "embedding_model": EMBEDDING_MODEL,
            "embedding_dimension": str(EMBEDDING_DIM),
            "created": datetime.now().isoformat(),
            "hnsw:space": "cosine"
        }
    )

    base = Path(base_path)
    if not base.exists():
        logger.warning(f"Verzeichnis nicht gefunden: {base_path}")
        return 0

    # Alle Markdown-Dateien finden
    md_files = list(base.rglob("*.md"))
    logger.info(f"Gefundene Dateien: {len(md_files)}")

    total_docs = 0

    for filepath in md_files:
        try:
            filename = filepath.name

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                logger.warning(f"  Leere Datei: {filename}")
                continue

            tag, subtag = extract_tag_from_filename(filename)

            # Full-Doc oder Chunked?
            if filename in FULL_DOC_FILES:
                # Full Document Mode
                doc_id = generate_doc_id(filename, 0)

                collection.add(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[{
                        "filename": filename,
                        "filepath": str(filepath),
                        "tag": tag,
                        "subtag": subtag,
                        "mode": "full_document",
                        "chunk_index": 0,
                        "total_chunks": 1,
                        "char_count": len(content),
                        "import_date": datetime.now().isoformat()
                    }]
                )

                logger.info(f"  ✓ [FULL] {filename} ({len(content):,} Zeichen)")
                total_docs += 1

            else:
                # Chunked Mode
                chunks = chunk_text(content)

                ids = []
                documents = []
                metadatas = []

                for i, chunk in enumerate(chunks):
                    doc_id = generate_doc_id(filename, i)

                    ids.append(doc_id)
                    documents.append(chunk)
                    metadatas.append({
                        "filename": filename,
                        "filepath": str(filepath),
                        "tag": tag,
                        "subtag": subtag,
                        "mode": "chunked",
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "char_count": len(chunk),
                        "import_date": datetime.now().isoformat()
                    })

                collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )

                logger.info(f"  ✓ [CHUNK] {filename} → {len(chunks)} Chunks")
                total_docs += len(chunks)

        except Exception as e:
            logger.error(f"  ✗ {filepath.name}: {e}")

    logger.info(f"\nCollection {collection_name}: {collection.count()} Dokumente")
    return total_docs


def verify_collections(client: chromadb.HttpClient, embedding_fn: E5LargeEmbeddingFunction) -> None:
    """Verifiziere die Collections mit Test-Queries"""

    logger.info("\n" + "="*60)
    logger.info("VERIFIKATION")
    logger.info("="*60)

    collections = client.list_collections()

    for col in collections:
        collection = client.get_collection(col.name, embedding_function=embedding_fn)
        logger.info(f"\n{col.name}: {collection.count()} Dokumente")

    # Test-Queries
    test_queries = [
        ("osp_kern", "Wer ist AL?", "HR_CORE"),
        ("osp_kern", "Komax Maschinen", "TM_CORE"),
        ("osp_kern", "NULL-FEHLER-POLITIK", "QM oder KOM")
    ]

    logger.info("\n--- Test-Queries ---")

    for coll_name, query, expected in test_queries:
        try:
            collection = client.get_collection(coll_name, embedding_function=embedding_fn)

            # E5 erfordert "query: " Präfix für Anfragen
            query_with_prefix = f"query: {query}"

            # Manuelles Encoding für Query
            query_embedding = embedding_fn.model.encode(
                [query_with_prefix],
                normalize_embeddings=True
            ).tolist()

            results = collection.query(
                query_embeddings=query_embedding,
                n_results=3,
                include=["metadatas", "distances"]
            )

            logger.info(f"\nQuery: '{query}' → erwartet: {expected}")

            if results["ids"][0]:
                for i, (meta, dist) in enumerate(zip(
                    results["metadatas"][0],
                    results["distances"][0]
                )):
                    score = 1 - dist  # Cosine similarity
                    filename = meta.get('filename', 'N/A')
                    logger.info(f"  {i+1}. {filename} (Score: {score:.3f})")
            else:
                logger.warning("  Keine Ergebnisse")

        except Exception as e:
            logger.error(f"  Query-Fehler: {e}")


def main():
    """Main Entry Point"""

    logger.info("="*60)
    logger.info("OSP ChromaDB Reindexierung")
    logger.info(f"Embedding-Modell: {EMBEDDING_MODEL}")
    logger.info(f"Dimension: {EMBEDDING_DIM}")
    logger.info("="*60)

    # ChromaDB Client verbinden
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

    try:
        client.heartbeat()
        logger.info(f"✓ ChromaDB verbunden: {CHROMADB_HOST}:{CHROMADB_PORT}")
    except Exception as e:
        logger.error(f"ChromaDB nicht erreichbar: {e}")
        return

    # E5 Embedding Function initialisieren
    embedding_fn = E5LargeEmbeddingFunction(EMBEDDING_MODEL)

    # Alle Collections löschen
    delete_all_collections(client)

    # Collections neu erstellen und importieren
    total = 0

    for collection_name, path in PATHS.items():
        count = import_collection(client, collection_name, path, embedding_fn)
        total += count

    # Verifikation
    verify_collections(client, embedding_fn)

    # Zusammenfassung
    logger.info("\n" + "="*60)
    logger.info("REINDEXIERUNG ABGESCHLOSSEN")
    logger.info("="*60)

    collections = client.list_collections()
    for col in collections:
        collection = client.get_collection(col.name, embedding_function=embedding_fn)
        logger.info(f"  {col.name}: {collection.count()} Dokumente")

    logger.info(f"\nGesamt: {total} Dokumente importiert")
    logger.info(f"Embedding-Modell: {EMBEDDING_MODEL}")
    logger.info(f"Dimension: {EMBEDDING_DIM}")

    logger.info("\n⚠️  WICHTIG: Pipeline muss 'query: ' Präfix für Anfragen verwenden!")


if __name__ == "__main__":
    main()
