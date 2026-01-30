#!/usr/bin/env python3
"""
OSP_KPL ChromaDB Collection Setup
=================================

Version: 1.0
Erstellt: 2025-12-13
Server: Hetzner CX33 (46.224.102.30)
ChromaDB: http://localhost:8000

Strategie: Hybrid (Full-Doc + Chunked RAG)
- LAYER 1: Full-Document Mode für tabellenkritische Dateien
- LAYER 2: Chunked RAG für alle anderen Markdown-Dateien
"""

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import hashlib
import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json

# =============================================================================
# KONFIGURATION
# =============================================================================

# ChromaDB Connection
CHROMADB_PATH = "/mnt/HC_Volume_104189729/osp/chromadb/data"
COLLECTION_NAME = "osp_kpl"

# Document Paths (Server) - ACHTUNG: Unterstrich, nicht Bindestrich!
OSP_BASE_PATH = "/mnt/HC_Volume_104189729/osp/documents_kpl"
# Alternative für lokalen Test:
# OSP_BASE_PATH = r"C:\Users\andre\OneDrive - Rainer Schneider Kabelsatzbau und Konfektion\Kommunikationswebsite - OSP Schneider Kabelsatzbau"

# Embedding Model - Multilingual E5-large für beste deutsche Ergebnisse
EMBEDDING_MODEL = "intfloat/multilingual-e5-large"
EMBEDDING_DIM = 1024

# Chunking Parameters
CHUNK_SIZE = 1200  # Tokens (ca. 4800 Zeichen)
CHUNK_OVERLAP = 150  # Tokens (ca. 600 Zeichen)
CHARS_PER_TOKEN = 4  # Approximation für Deutsch

# Full-Document Layer (Tabellen-kritisch)
FULL_DOC_FILES = [
    "TM_CORE_Maschinen_Anlagen.md",
    "TM_WKZ_Werkzeuge.md",
    "HR_CORE_Personalstamm.md",
    "AV_AGK_Arbeitsgang_Katalog.md",
    "DMS_FORM_Formblaetter.md"  # Falls vorhanden
]

# HNSW Index Configuration
# Nur space angeben - M und ef_construction werden von ChromaDB automatisch gesetzt
HNSW_CONFIG = {
    "hnsw:space": "cosine"
}

# =============================================================================
# MODULE-TAG MAPPING
# =============================================================================

MODULE_MAPPING = {
    "ORG": {"cluster": "C1", "name": "Organisation", "level": "L1"},
    "KOM": {"cluster": "C1", "name": "Kommunikation", "level": "L1"},
    "QM": {"cluster": "C2", "name": "Qualitätsmanagement", "level": "L2"},
    "GF": {"cluster": "C2", "name": "Geschäftsführung", "level": "L3"},
    "PM": {"cluster": "C2", "name": "Projektmanagement", "level": "L2"},
    "AV": {"cluster": "C2", "name": "Arbeitsvorbereitung", "level": "L2"},
    "VT": {"cluster": "C3", "name": "Vertrieb", "level": "L2"},
    "EK": {"cluster": "C3", "name": "Einkauf", "level": "L2"},
    "KST": {"cluster": "C3", "name": "Kostenstellen", "level": "L2"},
    "TM": {"cluster": "C4", "name": "Technik/Maschinen", "level": "L2"},
    "IT": {"cluster": "C4", "name": "IT", "level": "L2"},
    "HR": {"cluster": "C4", "name": "Human Resources", "level": "L3"},
    "CMS": {"cluster": "C4", "name": "Compliance", "level": "L2"},
    "FIN": {"cluster": "C4", "name": "Finanzen", "level": "L3"},
    "STR": {"cluster": "C4", "name": "Strategie", "level": "L3"},
    "RES": {"cluster": "C4", "name": "Ressourcen", "level": "L1"},
    "DMS": {"cluster": "C4", "name": "Dokumentenmanagement", "level": "L1"},
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_doc_id(filename: str, chunk_index: int = 0) -> str:
    """Generiere eindeutige Document ID"""
    base = f"{filename}_{chunk_index}"
    return hashlib.md5(base.encode()).hexdigest()[:16]


def extract_tag_from_filename(filename: str) -> Tuple[str, str, str]:
    """
    Extrahiere TAG, SUB-TAG und Beschreibung aus Dateiname
    Format: TAG_SUB-TAG_Beschreibung.md
    
    Returns: (tag, subtag, description)
    """
    name = filename.replace(".md", "")
    parts = name.split("_", 2)
    
    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        return parts[0], parts[1], ""
    else:
        return parts[0], "", ""


def get_module_info(tag: str) -> Dict:
    """Hole Modul-Informationen basierend auf TAG"""
    return MODULE_MAPPING.get(tag, {
        "cluster": "C0",
        "name": "Unbekannt",
        "level": "L1"
    })


def extract_header_metadata(content: str) -> Dict:
    """Extrahiere Metadaten aus Markdown-Header"""
    metadata = {}
    
    # Version
    version_match = re.search(r'\*\*Version:\*\*\s*([\d.]+)', content)
    if version_match:
        metadata["version"] = version_match.group(1)
    
    # Erstellt
    created_match = re.search(r'\*\*Erstellt:\*\*\s*([\d-]+)', content)
    if created_match:
        metadata["created"] = created_match.group(1)
    
    # Aktualisiert
    updated_match = re.search(r'\*\*(?:Aktualisiert|Zuletzt aktualisiert):\*\*\s*([\d-]+)', content)
    if updated_match:
        metadata["updated"] = updated_match.group(1)
    
    # Status
    status_match = re.search(r'\*\*Status:\*\*\s*([^\n|]+)', content)
    if status_match:
        metadata["status"] = status_match.group(1).strip()
    
    # Cluster
    cluster_match = re.search(r'\*\*Cluster:\*\*\s*([^\n|]+)', content)
    if cluster_match:
        metadata["cluster"] = cluster_match.group(1).strip()
    
    # Zugriff/Level
    access_match = re.search(r'\*\*Zugriff:\*\*\s*([^\n|]+)', content)
    if access_match:
        metadata["access_level"] = access_match.group(1).strip()
    
    return metadata


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[Dict]:
    """
    Teile Text in Chunks mit Überlappung
    Chunking nach Markdown-Headern wenn möglich
    """
    chunks = []
    
    # Versuche nach Markdown-Headern zu chunken
    sections = re.split(r'\n(?=#{1,3}\s)', text)
    
    current_chunk = ""
    current_start = 0
    char_limit = chunk_size * CHARS_PER_TOKEN
    overlap_chars = overlap * CHARS_PER_TOKEN
    
    for section in sections:
        if len(current_chunk) + len(section) <= char_limit:
            current_chunk += section
        else:
            if current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "start_char": current_start,
                    "end_char": current_start + len(current_chunk)
                })
            
            # Überlappung beibehalten
            if overlap_chars > 0 and current_chunk:
                overlap_text = current_chunk[-overlap_chars:]
                current_chunk = overlap_text + section
            else:
                current_chunk = section
            
            current_start = current_start + len(current_chunk) - len(section)
    
    # Letzten Chunk hinzufügen
    if current_chunk.strip():
        chunks.append({
            "text": current_chunk.strip(),
            "start_char": current_start,
            "end_char": current_start + len(current_chunk)
        })
    
    return chunks


def extract_keywords(content: str) -> str:
    """Extrahiere Keywords aus dem Dokument"""
    # Primary Keywords suchen
    keywords_match = re.search(
        r'\*\*Primary Keywords:\*\*\s*([^\n]+)',
        content,
        re.IGNORECASE
    )
    
    if keywords_match:
        return keywords_match.group(1).strip()[:500]  # Max 500 Zeichen
    
    return ""


def extract_full_doc_keywords(content: str, filename: str) -> str:
    """
    Extrahiere spezifische Keywords aus Full-Doc Dateien.
    Für TM_CORE: Inventarnummern, Maschinennamen, Hersteller
    Für TM_WKZ: WKZ-Nummern, Kontaktnummern
    Für HR_CORE: MA-Kürzel, Namen
    Für AV_AGK: AGK-Nummern, Prozessnamen
    """
    keywords = []
    
    if "TM_CORE" in filename:
        # Inventarnummern (0281, 0323, 0348, etc.)
        inv_numbers = re.findall(r'\b0[0-9]{3}\b', content)
        keywords.extend(list(set(inv_numbers)))
        
        # Maschinennamen und Hersteller
        machines = re.findall(r'\b(Komax|Schleuniger|Strunk|Harting|Mecal|Adaptronic|TSK|Brady|Weidmüller)\b', content, re.IGNORECASE)
        keywords.extend(list(set(machines)))
        
        # Maschinentypen (Alpha 530, Gamma 255, Kappa 310, etc.)
        types = re.findall(r'\b(Alpha|Gamma|Kappa|Zeta|Beta)\s*\d+\b', content, re.IGNORECASE)
        keywords.extend(list(set(types)))
        
        # Spezifische Modelle
        models = re.findall(r'\b(KNP\s*\d+/\d+|CS\d+|PreFeeder|CrimpCenter)\b', content, re.IGNORECASE)
        keywords.extend(list(set(models)))
        
    elif "TM_WKZ" in filename:
        # WKZ-Nummern (532, 549, 588, 600, etc.)
        wkz_numbers = re.findall(r'\bWKZ[-\s]*(\d{3,4})\b', content, re.IGNORECASE)
        keywords.extend([f"WKZ{n}" for n in set(wkz_numbers)])
        
        # Auch einzelne 3-stellige Nummern in Tabellen
        wkz_standalone = re.findall(r'\|\s*(\d{3})\s*\|', content)
        keywords.extend([f"WKZ{n}" for n in set(wkz_standalone)])
        
        # Kontaktnummern (0-0170360-1, 0-0350415-1, etc.)
        contacts = re.findall(r'\b\d+-\d+-\d+(?:-\d+)?\b', content)
        keywords.extend(list(set(contacts[:50])))  # Max 50
        
        # Werkzeug-Kategorien
        categories = re.findall(r'\b(Festwerkzeug|Umbauwerkzeug|VT-Satz|Crimpwerkzeug|Prüfmittel)\b', content, re.IGNORECASE)
        keywords.extend(list(set(categories)))
        
    elif "HR_CORE" in filename:
        # MA-Kürzel (2 Buchstaben großgeschrieben)
        kuerzel = re.findall(r'\b([A-Z]{2})\b', content)
        # Nur plausible Kürzel (nicht "GB", "MB", etc.)
        valid_kuerzel = [k for k in set(kuerzel) if k not in ['GB', 'MB', 'KB', 'TB', 'MD', 'ID', 'IT', 'HR', 'QM', 'GF', 'VT', 'EK', 'AV', 'PM']]
        keywords.extend(valid_kuerzel[:30])  # Max 30
        
        # Level (L1, L2, L3)
        levels = re.findall(r'\b(L[1-3])\b', content)
        keywords.extend(list(set(levels)))
        
        # OSP-Level
        osp_levels = re.findall(r'\b(OSP-STD|OSP-PRO|OSP-EXP)\b', content, re.IGNORECASE)
        keywords.extend(list(set(osp_levels)))
        
        # Funktionen
        functions = re.findall(r'\b(Geschäftsführer|Prokurist|QM-Manager|KI-Manager|Abteilungsleiter|Sachbearbeiter)\b', content, re.IGNORECASE)
        keywords.extend(list(set(functions)))
        
    elif "AV_AGK" in filename:
        # AGK-Nummern (10100, 20100, 30100, etc.)
        agk_numbers = re.findall(r'\b[1-5]0[0-9]{3}\b', content)
        keywords.extend([f"AGK{n}" for n in set(agk_numbers)])
        
        # Prozessnamen
        processes = re.findall(r'\b(Crimpen|Zuschnitt|Schweißen|Montage|Prüfen|Abisolieren|Bestücken|Löten)\b', content, re.IGNORECASE)
        keywords.extend(list(set(processes)))
    
    # Deduplizieren und zusammenfügen
    unique_keywords = list(dict.fromkeys(keywords))  # Reihenfolge beibehalten
    return ", ".join(unique_keywords[:100])  # Max 100 Keywords

# =============================================================================
# MAIN IMPORT CLASS
# =============================================================================

class OSPKPLImporter:
    """
    OSP_KPL Collection Importer
    
    Hybrid-Strategie:
    - Full-Document Mode für tabellenkritische Dateien
    - Chunked RAG für alle anderen Dateien
    """
    
    def __init__(self, chromadb_path: str = CHROMADB_PATH):
        """Initialize ChromaDB Client und Collection"""
        
        print("=" * 60)
        print("OSP_KPL Collection Setup")
        print("=" * 60)
        
        # ChromaDB Client
        settings = Settings(
            allow_reset=True,
            anonymized_telemetry=False
        )
        
        self.client = chromadb.PersistentClient(
            path=chromadb_path,
            settings=settings
        )
        
        print(f"✓ ChromaDB Client verbunden: {chromadb_path}")
        
        # Embedding Function - Versuche verschiedene Methoden
        self.embedding_fn = None
        self.manual_embedder = None
        
        # Methode 1: Versuche ChromaDB Wrapper
        try:
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=EMBEDDING_MODEL,
                device="cpu"
            )
            print(f"✓ Embedding Model geladen (ChromaDB Wrapper): {EMBEDDING_MODEL}")
        except Exception as e:
            print(f"⚠ ChromaDB Wrapper fehlgeschlagen: {e}")
            print("  → Versuche manuelle Embedding-Berechnung...")
            
            # Methode 2: Manuelles Embedding mit sentence-transformers
            try:
                from sentence_transformers import SentenceTransformer
                self.manual_embedder = SentenceTransformer(EMBEDDING_MODEL, device="cpu")
                print(f"✓ Embedding Model geladen (manuell): {EMBEDDING_MODEL}")
            except ImportError:
                print("⚠ sentence-transformers nicht verfügbar")
                print("  → Verwende ChromaDB Default Embedding")
                # Methode 3: ChromaDB Default (Fallback - NICHT EMPFOHLEN für E5-large Collections!)
                self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
                print("⚠ Default Embedding Function aktiviert (NICHT kompatibel mit E5-large!)")
        
        # Collection erstellen/abrufen
        collection_kwargs = {
            "name": COLLECTION_NAME,
            "metadata": {
                "description": "OSP Komplett - Alle OSP Markdown-Dokumente",
                "embedding_model": EMBEDDING_MODEL,
                "embedding_dimension": str(EMBEDDING_DIM),
                "strategy": "hybrid_full_doc_chunked",
                "created": datetime.now().isoformat(),
                **HNSW_CONFIG
            }
        }
        
        # Nur Embedding-Funktion hinzufügen wenn verfügbar (nicht bei manuellem Embedding)
        if self.embedding_fn is not None:
            collection_kwargs["embedding_function"] = self.embedding_fn
        
        self.collection = self.client.get_or_create_collection(**collection_kwargs)
        
        print(f"✓ Collection erstellt/geladen: {COLLECTION_NAME}")
        print(f"  - Aktuelle Dokumente: {self.collection.count()}")
        print(f"  - Embedding-Modus: {'Manuell' if self.manual_embedder else 'ChromaDB Wrapper'}")
        
        # Statistiken
        self.stats = {
            "full_doc_count": 0,
            "chunked_count": 0,
            "total_chunks": 0,
            "errors": []
        }
    
    def is_full_doc_file(self, filename: str) -> bool:
        """Prüfe ob Datei im Full-Document Mode verarbeitet werden soll"""
        return filename in FULL_DOC_FILES
    
    def import_full_document(self, filepath: Path) -> bool:
        """
        Importiere Dokument als Ganzes (Full-Document Mode)
        Für tabellenkritische Dateien mit Inventarnummern, Werkzeuglisten etc.
        MIT KEYWORD-BOOST für bessere Suche!
        """
        try:
            filename = filepath.name
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Metadaten extrahieren
            tag, subtag, description = extract_tag_from_filename(filename)
            module_info = get_module_info(tag)
            header_meta = extract_header_metadata(content)
            
            # Standard Keywords aus Header
            keywords = extract_keywords(content)
            
            # ZUSÄTZLICH: Spezifische Keywords für Full-Doc Dateien
            full_doc_keywords = extract_full_doc_keywords(content, filename)
            if full_doc_keywords:
                if keywords:
                    keywords = f"{keywords}, {full_doc_keywords}"
                else:
                    keywords = full_doc_keywords
            
            # Document ID
            doc_id = generate_doc_id(filename, chunk_index=0)
            
            # Metadata zusammenstellen
            metadata = {
                "filename": filename,
                "filepath": str(filepath),
                "tag": tag,
                "subtag": subtag,
                "description": description,
                "cluster": module_info.get("cluster", "C0"),
                "module_name": module_info.get("name", ""),
                "access_level": module_info.get("level", "L1"),
                "import_mode": "full_document",
                "chunk_index": 0,
                "total_chunks": 1,
                "char_count": len(content),
                "import_date": datetime.now().isoformat(),
                **header_meta
            }
            
            if keywords:
                metadata["keywords"] = keywords[:1000]  # Max 1000 Zeichen für Keywords
            
            # In Collection einfügen
            self.collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[metadata]
            )
            
            self.stats["full_doc_count"] += 1
            keyword_count = len(keywords.split(", ")) if keywords else 0
            print(f"  ✓ [FULL-DOC] {filename} ({len(content):,} Zeichen, {keyword_count} Keywords)")
            
            return True
            
        except Exception as e:
            self.stats["errors"].append({
                "file": str(filepath),
                "error": str(e),
                "mode": "full_document"
            })
            print(f"  ✗ [ERROR] {filepath.name}: {e}")
            return False
    
    def import_chunked_document(self, filepath: Path) -> bool:
        """
        Importiere Dokument in Chunks (Standard RAG Mode)
        """
        try:
            filename = filepath.name
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Metadaten extrahieren
            tag, subtag, description = extract_tag_from_filename(filename)
            module_info = get_module_info(tag)
            header_meta = extract_header_metadata(content)
            keywords = extract_keywords(content)
            
            # Text in Chunks teilen
            chunks = chunk_text(content, CHUNK_SIZE, CHUNK_OVERLAP)
            
            if not chunks:
                print(f"  ⚠ [SKIP] {filename}: Keine Chunks generiert")
                return False
            
            # Chunks importieren
            ids = []
            documents = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                doc_id = generate_doc_id(filename, chunk_index=i)
                
                metadata = {
                    "filename": filename,
                    "filepath": str(filepath),
                    "tag": tag,
                    "subtag": subtag,
                    "description": description,
                    "cluster": module_info.get("cluster", "C0"),
                    "module_name": module_info.get("name", ""),
                    "access_level": module_info.get("level", "L1"),
                    "import_mode": "chunked",
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "start_char": chunk["start_char"],
                    "end_char": chunk["end_char"],
                    "char_count": len(chunk["text"]),
                    "import_date": datetime.now().isoformat(),
                    **header_meta
                }
                
                if keywords and i == 0:  # Keywords nur im ersten Chunk
                    metadata["keywords"] = keywords
                
                ids.append(doc_id)
                documents.append(chunk["text"])
                metadatas.append(metadata)
            
            # Batch-Insert
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            self.stats["chunked_count"] += 1
            self.stats["total_chunks"] += len(chunks)
            
            print(f"  ✓ [CHUNKED] {filename} → {len(chunks)} Chunks")
            
            return True
            
        except Exception as e:
            self.stats["errors"].append({
                "file": str(filepath),
                "error": str(e),
                "mode": "chunked"
            })
            print(f"  ✗ [ERROR] {filepath.name}: {e}")
            return False
    
    def import_directory(self, base_path: str) -> Dict:
        """
        Importiere alle Markdown-Dateien aus Verzeichnis
        """
        print("\n" + "-" * 60)
        print("Starte Import...")
        print("-" * 60)
        
        base = Path(base_path)
        
        if not base.exists():
            raise FileNotFoundError(f"Verzeichnis nicht gefunden: {base_path}")
        
        # Alle Markdown-Dateien finden
        md_files = list(base.rglob("*.md"))
        
        # Sortieren: Full-Doc zuerst, dann Chunked
        full_doc_files = [f for f in md_files if self.is_full_doc_file(f.name)]
        chunked_files = [f for f in md_files if not self.is_full_doc_file(f.name)]
        
        print(f"\nGefundene Dateien:")
        print(f"  - Full-Document: {len(full_doc_files)}")
        print(f"  - Chunked: {len(chunked_files)}")
        print(f"  - Gesamt: {len(md_files)}")
        
        # Full-Document Import
        if full_doc_files:
            print(f"\n📄 LAYER 1: Full-Document Import ({len(full_doc_files)} Dateien)")
            for filepath in full_doc_files:
                self.import_full_document(filepath)
        
        # Chunked Import
        if chunked_files:
            print(f"\n📑 LAYER 2: Chunked Import ({len(chunked_files)} Dateien)")
            for filepath in chunked_files:
                self.import_chunked_document(filepath)
        
        return self.get_statistics()
    
    def get_statistics(self) -> Dict:
        """Hole Import-Statistiken"""
        return {
            "collection_name": COLLECTION_NAME,
            "total_documents": self.collection.count(),
            "full_doc_files": self.stats["full_doc_count"],
            "chunked_files": self.stats["chunked_count"],
            "total_chunks": self.stats["total_chunks"],
            "errors": len(self.stats["errors"]),
            "error_details": self.stats["errors"]
        }
    
    def verify_collection(self) -> None:
        """Verifiziere Collection nach Import"""
        print("\n" + "=" * 60)
        print("VERIFIKATION")
        print("=" * 60)
        
        stats = self.get_statistics()
        
        print(f"\n📊 Collection: {stats['collection_name']}")
        print(f"   Dokumente gesamt: {stats['total_documents']}")
        print(f"   Full-Doc Dateien: {stats['full_doc_files']}")
        print(f"   Chunked Dateien: {stats['chunked_files']}")
        print(f"   Chunks gesamt: {stats['total_chunks']}")
        print(f"   Fehler: {stats['errors']}")
        
        # Keywords für Full-Doc Dateien anzeigen
        print("\n🔑 Keywords in Full-Doc Dateien:")
        full_docs = self.collection.get(
            where={"import_mode": "full_document"},
            include=["metadatas"]
        )
        
        for meta in full_docs["metadatas"]:
            filename = meta.get("filename", "?")
            keywords = meta.get("keywords", "")
            keyword_count = len(keywords.split(", ")) if keywords else 0
            print(f"   {filename}: {keyword_count} Keywords")
            if keywords:
                # Erste 5 Keywords zeigen
                first_keywords = ", ".join(keywords.split(", ")[:5])
                print(f"      → {first_keywords}...")
        
        # Sample Queries - normale Embedding-Suche
        print("\n🔍 Test-Queries (Embedding):")
        
        test_queries = [
            ("Komax Alpha 530", "TM_CORE Maschine"),
            ("NULL-FEHLER-POLITIK", "KOM_AIR Regel"),
            ("Personalstamm", "HR_CORE")
        ]
        
        for query, expected in test_queries:
            results = self.collection.query(
                query_texts=[query],
                n_results=3,
                include=["metadatas", "distances"]
            )
            
            if results["ids"][0]:
                print(f"\n   Query: '{query}'")
                for i, (meta, dist) in enumerate(zip(results["metadatas"][0], results["distances"][0])):
                    score = 1 - dist
                    filename = meta.get('filename', 'N/A')
                    mode = meta.get('import_mode', 'N/A')
                    print(f"   {i+1}. {filename} (Score: {score:.1%}, Mode: {mode})")
        
        # Keyword-basierte Suche testen
        print("\n🔑 Test-Queries (Keyword in Metadata):")
        
        keyword_tests = [
            ("0348", "Inventarnummer"),
            ("WKZ602", "Werkzeug"),
            ("Alpha 530", "Maschinentyp")
        ]
        
        for keyword, desc in keyword_tests:
            # Suche in keywords Feld
            try:
                results = self.collection.get(
                    where={"keywords": {"$contains": keyword}},
                    include=["metadatas"]
                )
                
                if results["ids"]:
                    print(f"\n   Keyword '{keyword}' ({desc}):")
                    for meta in results["metadatas"][:3]:
                        print(f"   → {meta.get('filename', 'N/A')}")
                else:
                    print(f"\n   Keyword '{keyword}' ({desc}): Nicht gefunden")
            except Exception as e:
                print(f"\n   Keyword '{keyword}': Suche nicht unterstützt ({e})")
    
    def clear_collection(self) -> None:
        """Lösche alle Dokumente aus Collection"""
        print("\n⚠️  Lösche Collection...")
        
        # Alle IDs holen
        all_docs = self.collection.get()
        if all_docs["ids"]:
            self.collection.delete(ids=all_docs["ids"])
            print(f"   ✓ {len(all_docs['ids'])} Dokumente gelöscht")
        else:
            print("   ℹ Collection war bereits leer")


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Main Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="OSP_KPL ChromaDB Collection Setup"
    )
    parser.add_argument(
        "--path",
        type=str,
        default=OSP_BASE_PATH,
        help="Pfad zu OSP-Dokumenten"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Collection vor Import leeren"
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Nur Verifikation, kein Import"
    )
    parser.add_argument(
        "--chromadb-path",
        type=str,
        default=CHROMADB_PATH,
        help="Pfad zu ChromaDB Daten"
    )
    
    args = parser.parse_args()
    
    # Importer initialisieren
    importer = OSPKPLImporter(chromadb_path=args.chromadb_path)
    
    if args.verify_only:
        importer.verify_collection()
        return
    
    if args.clear:
        importer.clear_collection()
    
    # Import durchführen
    stats = importer.import_directory(args.path)
    
    # Verifikation
    importer.verify_collection()
    
    # Summary
    print("\n" + "=" * 60)
    print("IMPORT ABGESCHLOSSEN")
    print("=" * 60)
    print(json.dumps(stats, indent=2, default=str))


if __name__ == "__main__":
    main()
