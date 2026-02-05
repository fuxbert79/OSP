#!/usr/bin/env python3
"""
OSP KPL Index Import
====================

Erstellt einen Datei-Index in ChromaDB.
Jede Datei = 1 Dokument mit Dateiname, Pfad und Beschreibung.

Verwendung:
    python3 import_kpl_index.py --path /opt/osp/documents_kpl
"""

import argparse
import hashlib
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import chromadb
    from chromadb import Documents, EmbeddingFunction, Embeddings
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    print(f"Fehler: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class E5EmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self, model_name: str = "intfloat/multilingual-e5-large"):
        logger.info(f"Lade Embedding-Modell: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Modell geladen. Dimension: {self.dimension}")

    def __call__(self, input: Documents) -> Embeddings:
        prefixed = [f"passage: {doc}" for doc in input]
        embeddings = self.model.encode(prefixed, normalize_embeddings=True)
        return embeddings.tolist()


def extract_file_info(filepath: Path, base_path: Path) -> dict:
    """Extrahiere Informationen aus einer MD-Datei."""
    filename = filepath.name
    relative_path = filepath.relative_to(base_path)

    # TAG aus Dateiname extrahieren
    name_parts = filename.replace(".md", "").split("_")
    tag = name_parts[0] if name_parts else ""
    subtag = name_parts[1] if len(name_parts) > 1 else ""

    # Titel aus Datei lesen (erste H1 Zeile)
    title = filename.replace(".md", "").replace("_", " ")
    description = ""

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            # Titel aus erstem H1
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1).strip()

            # Beschreibung aus erstem Absatz nach Titel
            desc_match = re.search(r'^#.+\n\n(.+?)(?:\n\n|\n#)', content, re.MULTILINE | re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip()[:500]
    except Exception as e:
        logger.warning(f"  Konnte {filename} nicht lesen: {e}")

    return {
        "filename": filename,
        "filepath": str(filepath),
        "relative_path": str(relative_path),
        "tag": tag,
        "subtag": subtag,
        "title": title,
        "description": description
    }


def create_index_document(info: dict) -> str:
    """Erstelle ein durchsuchbares Index-Dokument."""
    doc = f"""DATEI: {info['filename']}
PFAD: {info['relative_path']}
TAG: [{info['tag']}][{info['subtag']}]
TITEL: {info['title']}

{info['description']}
"""
    return doc


def main():
    parser = argparse.ArgumentParser(description="OSP KPL Index Import")
    parser.add_argument("--path", "-p", required=True, help="Pfad zu documents_kpl")
    parser.add_argument("--host", default="localhost", help="ChromaDB Host")
    parser.add_argument("--port", type=int, default=8000, help="ChromaDB Port")
    parser.add_argument("--clear", action="store_true", help="Collection leeren")
    args = parser.parse_args()

    base_path = Path(args.path)
    if not base_path.exists():
        logger.error(f"Pfad nicht gefunden: {args.path}")
        sys.exit(1)

    # ChromaDB verbinden
    client = chromadb.HttpClient(host=args.host, port=args.port)
    logger.info(f"ChromaDB verbunden: {args.host}:{args.port}")

    # Embedding Function
    embedding_fn = E5EmbeddingFunction()

    # Collection erstellen
    if args.clear:
        try:
            client.delete_collection("osp_kpl")
            logger.info("Collection 'osp_kpl' gelöscht")
        except:
            pass

    collection = client.get_or_create_collection(
        name="osp_kpl",
        embedding_function=embedding_fn,  # type: ignore[arg-type]
        metadata={
            "description": "OSP Datei-Index (KPL)",
            "embedding_model": "intfloat/multilingual-e5-large",
            "embedding_dimension": str(embedding_fn.dimension),
            "type": "file_index",
            "created": datetime.now().isoformat(),
            "hnsw:space": "cosine"
        }
    )
    logger.info(f"Collection 'osp_kpl' bereit")

    # Alle MD-Dateien finden
    md_files = list(base_path.rglob("*.md"))
    logger.info(f"Gefundene MD-Dateien: {len(md_files)}")

    ids = []
    documents = []
    metadatas = []

    for filepath in md_files:
        info = extract_file_info(filepath, base_path)
        doc_id = hashlib.md5(info['filename'].encode()).hexdigest()[:16]

        ids.append(doc_id)
        documents.append(create_index_document(info))
        metadatas.append({
            "filename": info['filename'],
            "filepath": info['filepath'],
            "relative_path": info['relative_path'],
            "tag": info['tag'],
            "subtag": info['subtag'],
            "title": info['title'],
            "type": "file_index",
            "import_date": datetime.now().isoformat()
        })

        logger.info(f"  [{info['tag']}] {info['filename']}")

    # Batch-Upsert
    if ids:
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        logger.info(f"\n✅ {len(ids)} Dateien im Index registriert")
        logger.info(f"Collection 'osp_kpl': {collection.count()} Einträge")
    else:
        logger.warning("Keine Dateien gefunden")


if __name__ == "__main__":
    main()
