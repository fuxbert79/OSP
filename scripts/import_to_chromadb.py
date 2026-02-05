#!/usr/bin/env python3
"""
OSP ChromaDB Import-Skript
==========================

Import von MD-Dateien in eine ChromaDB Collection.

Verwendung:
    python3 import_to_chromadb.py --collection osp_kern --path /opt/osp/documents
    python3 import_to_chromadb.py --collection osp_erweitert --path /opt/osp/documents_erweitert
    python3 import_to_chromadb.py --collection osp_kern --path /opt/osp/documents --clear

Parameter:
    --collection    Name der Collection (erforderlich)
    --path          Verzeichnis mit MD-Dateien (erforderlich)
    --host          ChromaDB Host (default: localhost)
    --port          ChromaDB Port (default: 8000)
    --model         Embedding-Modell (default: intfloat/multilingual-e5-large)
    --clear         Collection vor Import leeren (optional)
    --dry-run       Nur anzeigen, was importiert würde (optional)

Erstellt: 2025-12-15
"""

import argparse
import hashlib
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

try:
    import chromadb
    from chromadb import Documents, EmbeddingFunction, Embeddings
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    print(f"Fehler: Benötigte Pakete nicht installiert: {e}")
    print("Installation: pip3 install chromadb sentence-transformers")
    sys.exit(1)

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# KONFIGURATION
# =============================================================================

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000
DEFAULT_MODEL = "intfloat/multilingual-e5-large"

# Chunking-Parameter
CHUNK_SIZE = 4800   # Zeichen
CHUNK_OVERLAP = 600 # Zeichen

# Full-Document Mode für diese Dateien (keine Chunks)
# KERN-Dateien immer vollständig importieren!
FULL_DOC_FILES = [
    # OSP_KERN - alle KERN-Dateien vollständig
    "AV_AGK_Arbeitsgang_Katalog.md",
    "DMS_CORE_Dokumentenstruktur.md",
    "HR_CORE_Personalstamm.md",
    "IT_OSP_KI_Chatbot.md",
    "KOM_CORE_Corporate_Identity.md",
    "KST_CORE_Layout_Fertigung.md",
    "OSP_Navigator.md",
    "QM_CORE_Qualitaetspolitik.md",
    "QM_PMV_Prüfmittelverwaltung.md",
    "QM_REK_Reklamationsmanagement.md",
    "TM_CORE_Maschinen_Anlagen.md",
    "TM_WKZ_Werkzeuge.md",
    # CRIMP-Dokument (KRITISCH - enthält Tabellen, NICHT chunken!)
    "TM_CRIMP_Crimpdaten_Werkzeuge.md",
    # Weitere Full-Doc Dateien
    "DMS_FORM_Formblaetter.md"
]


# =============================================================================
# EMBEDDING FUNCTION
# =============================================================================

class E5EmbeddingFunction(EmbeddingFunction[Documents]):
    """
    Custom Embedding Function für E5-Modelle.

    E5-Modelle erfordern spezielle Präfixe:
    - "passage: " für Dokumente beim Indizieren
    - "query: " für Suchanfragen
    """

    def __init__(self, model_name: str):
        logger.info(f"Lade Embedding-Modell: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.is_e5 = "e5" in model_name.lower()
        logger.info(f"Modell geladen. Dimension: {self.dimension}, E5-Präfix: {self.is_e5}")

    def __call__(self, input: Documents) -> Embeddings:
        """Erstelle Embeddings für Dokumente."""
        if self.is_e5:
            # E5 erfordert "passage: " Präfix für Dokumente
            prefixed = [f"passage: {doc}" for doc in input]
        else:
            prefixed = input
        embeddings = self.model.encode(prefixed, normalize_embeddings=True)
        return embeddings.tolist()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_doc_id(filename: str, chunk_index: int = 0) -> str:
    """Generiere eindeutige Document ID."""
    base = f"{filename}_{chunk_index}"
    return hashlib.md5(base.encode()).hexdigest()[:16]


def extract_tag_from_filename(filename: str) -> Tuple[str, str]:
    """Extrahiere TAG und SUBTAG aus Dateiname."""
    name = filename.replace(".md", "")
    parts = name.split("_", 2)
    if len(parts) >= 2:
        return parts[0], parts[1]
    return parts[0], ""


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Teile Text in Chunks mit Überlappung (nach Markdown-Headern)."""
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
# MAIN IMPORT FUNCTION
# =============================================================================

def import_documents(
    client: "chromadb.HttpClient",  # type: ignore[type-arg]
    collection_name: str,
    base_path: str,
    embedding_fn: E5EmbeddingFunction,
    clear_collection: bool = False,
    dry_run: bool = False
) -> int:
    """Importiere Dokumente in eine Collection."""

    logger.info(f"\n{'='*60}")
    logger.info(f"Collection: {collection_name}")
    logger.info(f"Pfad: {base_path}")
    logger.info(f"Clear: {clear_collection}, Dry-Run: {dry_run}")
    logger.info(f"{'='*60}")

    base = Path(base_path)
    if not base.exists():
        logger.error(f"Verzeichnis nicht gefunden: {base_path}")
        return 0

    # Alle Markdown-Dateien finden
    md_files = list(base.rglob("*.md"))
    logger.info(f"Gefundene MD-Dateien: {len(md_files)}")

    if dry_run:
        logger.info("\n--- DRY RUN - Keine Änderungen ---")
        for f in md_files:
            logger.info(f"  {f.name}")
        return len(md_files)

    # Collection erstellen oder holen
    try:
        if clear_collection:
            try:
                client.delete_collection(collection_name)
                logger.info(f"Collection '{collection_name}' gelöscht")
            except Exception:
                pass  # Collection existierte nicht

        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_fn,
            metadata={
                "description": f"OSP Collection: {collection_name}",
                "embedding_model": "intfloat/multilingual-e5-large",
                "embedding_dimension": str(embedding_fn.dimension),
                "created": datetime.now().isoformat(),
                "hnsw:space": "cosine"
            }
        )
        logger.info(f"Collection '{collection_name}' bereit (aktuell: {collection.count()} Dokumente)")

    except Exception as e:
        logger.error(f"Fehler beim Erstellen der Collection: {e}")
        return 0

    total_docs = 0
    errors = 0

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

                collection.upsert(
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

                logger.info(f"  [FULL] {filename} ({len(content):,} Zeichen)")
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

                collection.upsert(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )

                logger.info(f"  [CHUNK] {filename} -> {len(chunks)} Chunks")
                total_docs += len(chunks)

        except Exception as e:
            logger.error(f"  FEHLER {filepath.name}: {e}")
            errors += 1

    logger.info(f"\n{'='*60}")
    logger.info(f"Import abgeschlossen: {total_docs} Dokumente")
    logger.info(f"Collection '{collection_name}': {collection.count()} Dokumente gesamt")
    if errors > 0:
        logger.warning(f"Fehler: {errors}")
    logger.info(f"{'='*60}")

    return total_docs


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="OSP ChromaDB Import - Importiert MD-Dateien in ChromaDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s --collection osp_kern --path /opt/osp/documents
  %(prog)s --collection osp_erweitert --path /opt/osp/documents_erweitert --clear
  %(prog)s --collection test --path ./docs --dry-run
        """
    )

    parser.add_argument(
        "--collection", "-c",
        required=True,
        help="Name der ChromaDB Collection"
    )
    parser.add_argument(
        "--path", "-p",
        required=True,
        help="Pfad zum Verzeichnis mit MD-Dateien"
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"ChromaDB Host (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"ChromaDB Port (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        help=f"Embedding-Modell (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Collection vor Import leeren"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Nur anzeigen, was importiert würde"
    )

    args = parser.parse_args()

    logger.info("="*60)
    logger.info("OSP ChromaDB Import")
    logger.info("="*60)

    # ChromaDB Client verbinden
    try:
        client = chromadb.HttpClient(host=args.host, port=args.port)
        heartbeat = client.heartbeat()
        logger.info(f"ChromaDB verbunden: {args.host}:{args.port}")
    except Exception as e:
        logger.error(f"ChromaDB nicht erreichbar: {e}")
        sys.exit(1)

    # Embedding Function initialisieren
    try:
        embedding_fn = E5EmbeddingFunction(args.model)
    except Exception as e:
        logger.error(f"Fehler beim Laden des Embedding-Modells: {e}")
        sys.exit(1)

    # Import durchführen
    count = import_documents(
        client=client,
        collection_name=args.collection,
        base_path=args.path,
        embedding_fn=embedding_fn,
        clear_collection=args.clear,
        dry_run=args.dry_run
    )

    if count > 0:
        logger.info(f"\nErfolgreich: {count} Dokumente importiert")
    else:
        logger.warning("\nKeine Dokumente importiert")
        sys.exit(1)


if __name__ == "__main__":
    main()
