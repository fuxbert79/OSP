#!/usr/bin/env python3
"""
ChromaDB Migration Script
=========================
Erstellt Collections neu und indiziert alle Dokumente.

Collections:
- osp_kern: 12 KERN-Dateien aus /mnt/HC_Volume_104189729/osp/documents/
- osp_erweitert: ~46 Dateien aus /mnt/HC_Volume_104189729/osp/documents_erweitert/
- osp_kpl: Alle Dateien aus /mnt/HC_Volume_104189729/osp/documents_kpl/

Erstellt: 2025-12-14
"""

import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import hashlib
import os
import re
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Konfiguration
CHROMADB_HOST = "localhost"
CHROMADB_PORT = 8000
EMBEDDING_MODEL = "intfloat/multilingual-e5-large"
EMBEDDING_DIM = 1024


class E5LargeEmbeddingFunction:
    """Custom Embedding Function für intfloat/multilingual-e5-large."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name, device="cpu")

    def __call__(self, input: list) -> list:
        # E5 erwartet "query: " Prefix für Queries
        prefixed = [f"query: {text}" if not text.startswith("query:") else text for text in input]
        embeddings = self.model.encode(prefixed, normalize_embeddings=True)
        return embeddings.tolist()

# Pfade
PATHS = {
    "osp_kern": "/mnt/HC_Volume_104189729/osp/documents",
    "osp_erweitert": "/mnt/HC_Volume_104189729/osp/documents_erweitert",
    "osp_kpl": "/mnt/HC_Volume_104189729/osp/documents_kpl"
}

# Chunking
CHUNK_SIZE = 4800  # Zeichen
CHUNK_OVERLAP = 600  # Zeichen

# Full-Document Mode für diese Dateien (keine Chunks)
FULL_DOC_FILES = [
    "TM_CORE_Maschinen_Anlagen.md",
    "TM_WKZ_Werkzeuge.md",
    "HR_CORE_Personalstamm.md",
    "AV_AGK_Arbeitsgang_Katalog.md",
    "OSP_Navigator.md"
]


def generate_doc_id(filename: str, chunk_index: int = 0) -> str:
    """Generiere eindeutige Document ID"""
    base = f"{filename}_{chunk_index}"
    return hashlib.md5(base.encode()).hexdigest()[:16]


def extract_tag_from_filename(filename: str):
    """Extrahiere TAG aus Dateiname"""
    name = filename.replace(".md", "")
    parts = name.split("_", 2)
    if len(parts) >= 2:
        return parts[0], parts[1]
    return parts[0], ""


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Teile Text in Chunks mit Überlappung"""
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
            # Überlappung
            if overlap > 0 and current_chunk:
                overlap_text = current_chunk[-overlap:]
                current_chunk = overlap_text + section
            else:
                current_chunk = section

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks if chunks else [text]


def import_collection(client, collection_name: str, base_path: str, embedding_fn):
    """Importiere Dokumente in eine Collection"""

    logger.info(f"=== Erstelle Collection: {collection_name} ===")

    # Collection erstellen
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
        metadata={
            "description": f"OSP Collection: {collection_name}",
            "created": datetime.now().isoformat(),
            "hnsw:space": "cosine",
            "embedding_model": EMBEDDING_MODEL,
            "embedding_dimension": str(EMBEDDING_DIM)
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
                logger.warning(f"Leere Datei: {filename}")
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

    logger.info(f"Collection {collection_name}: {collection.count()} Dokumente")
    return total_docs


def main():
    logger.info("=" * 60)
    logger.info("ChromaDB Migration gestartet")
    logger.info("=" * 60)

    # Client verbinden
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

    # Heartbeat prüfen
    try:
        client.heartbeat()
        logger.info(f"✓ ChromaDB verbunden: {CHROMADB_HOST}:{CHROMADB_PORT}")
    except Exception as e:
        logger.error(f"ChromaDB nicht erreichbar: {e}")
        return

    # Embedding Function
    embedding_fn = E5LargeEmbeddingFunction(EMBEDDING_MODEL)
    logger.info(f"✓ Embedding Function: {EMBEDDING_MODEL} ({EMBEDDING_DIM} dim)")

    # Collections importieren
    total = 0

    for collection_name, path in PATHS.items():
        count = import_collection(client, collection_name, path, embedding_fn)
        total += count

    # Zusammenfassung
    logger.info("")
    logger.info("=" * 60)
    logger.info("MIGRATION ABGESCHLOSSEN")
    logger.info("=" * 60)

    collections = client.list_collections()
    for col in collections:
        logger.info(f"  {col.name}: {col.count()} Dokumente")

    logger.info(f"\nGesamt: {total} Dokumente importiert")


if __name__ == "__main__":
    main()
