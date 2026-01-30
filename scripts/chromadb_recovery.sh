#!/bin/bash
# ============================================================
# ChromaDB Collection Recovery Script für Hetzner Server
# ============================================================
# Server: 46.224.102.30
# Ausführung: bash /mnt/HC_Volume_104189729/osp/scripts/chromadb_recovery.sh
# Erstellt: 2025-12-12
# ============================================================

set -e  # Bei Fehlern abbrechen

echo "============================================================"
echo "  CHROMADB COLLECTION RECOVERY"
echo "  Server: $(hostname)"
echo "  Datum: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

# ============================================================
# PHASE 1: DIAGNOSE
# ============================================================
echo "=== PHASE 1: DIAGNOSE ==="
echo ""

echo "1.1 Laufende Container:"
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
echo ""

echo "1.2 ChromaDB API-Status:"
if curl -s http://localhost:8000/api/v2/heartbeat > /dev/null 2>&1; then
    echo "  ✅ ChromaDB erreichbar"
    echo "  Collections:"
    curl -s http://localhost:8000/api/v2/collections | python3 -c "import json,sys; data=json.load(sys.stdin); [print(f'    - {c[\"name\"]}: {c.get(\"metadata\",{})}') for c in data]" 2>/dev/null || echo "    (keine oder Fehler)"
else
    echo "  ❌ ChromaDB NICHT erreichbar"
fi
echo ""

echo "1.3 Volume-Mounts:"
docker inspect chromadb --format='{{range .Mounts}}  {{.Source}} -> {{.Destination}}{{println}}{{end}}' 2>/dev/null || echo "  Container nicht gefunden"
echo ""

echo "1.4 Persistenz-Verzeichnis:"
if [ -d "/mnt/HC_Volume_104189729/osp/chromadb/data" ]; then
    echo "  ✅ /mnt/HC_Volume_104189729/osp/chromadb/data existiert"
    ls -la /mnt/HC_Volume_104189729/osp/chromadb/data/ | head -10
else
    echo "  ❌ /mnt/HC_Volume_104189729/osp/chromadb/data existiert NICHT"
fi
echo ""

read -p "Weiter mit Phase 2 (Persistenz)? [j/N] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Jj]$ ]]; then
    echo "Abgebrochen."
    exit 1
fi

# ============================================================
# PHASE 2: PERSISTENZ SICHERSTELLEN
# ============================================================
echo ""
echo "=== PHASE 2: PERSISTENZ SICHERSTELLEN ==="
echo ""

echo "2.1 Stoppe ChromaDB Container..."
docker stop chromadb 2>/dev/null || echo "  (war nicht gestartet)"
docker rm chromadb 2>/dev/null || echo "  (existierte nicht)"
echo "  ✅ Alter Container entfernt"

echo "2.2 Erstelle Datenverzeichnis..."
mkdir -p /mnt/HC_Volume_104189729/osp/chromadb/data
chmod 755 /mnt/HC_Volume_104189729/osp/chromadb/data
echo "  ✅ /mnt/HC_Volume_104189729/osp/chromadb/data erstellt"

echo "2.3 Starte ChromaDB mit persistentem Volume..."
docker run -d \
  --name chromadb \
  --network osp-network \
  -p 8000:8000 \
  -v /mnt/HC_Volume_104189729/osp/chromadb/data:/chroma/chroma \
  -e IS_PERSISTENT=TRUE \
  -e ANONYMIZED_TELEMETRY=FALSE \
  -e ALLOW_RESET=TRUE \
  --restart unless-stopped \
  chromadb/chroma:0.5.15

echo "  Warte 15 Sekunden auf Start..."
sleep 15

echo "2.4 Verifiziere ChromaDB..."
if curl -s http://localhost:8000/api/v2/heartbeat > /dev/null 2>&1; then
    echo "  ✅ ChromaDB läuft und ist erreichbar"
else
    echo "  ❌ ChromaDB nicht erreichbar!"
    docker logs chromadb --tail 20
    exit 1
fi
echo ""

# ============================================================
# PHASE 3: COLLECTIONS ERSTELLEN
# ============================================================
echo "=== PHASE 3: COLLECTIONS ERSTELLEN ==="
echo ""

echo "3.1 Installiere Python-Dependencies..."
pip3 install chromadb --break-system-packages -q 2>/dev/null || pip3 install chromadb -q
echo "  ✅ chromadb installiert"

echo "3.2 Erstelle Collections..."

python3 << 'PYEOF'
import chromadb
import sys

try:
    print("  Verbinde zu ChromaDB...")
    client = chromadb.HttpClient(host="localhost", port=8000)
    
    # Alte OSP_COMPLETE löschen
    collections = [c.name for c in client.list_collections()]
    if "OSP_COMPLETE" in collections:
        print("  🗑️ Lösche veraltete OSP_COMPLETE...")
        client.delete_collection("OSP_COMPLETE")
    
    # osp_kern erstellen
    CLUSTER_KERN = ["ORG", "KOM", "QM", "GF", "PM", "AV", "VT", "EK"]
    osp_kern = client.get_or_create_collection(
        name="osp_kern",
        metadata={
            "description": "OSP Kern-Dokumente (Cluster 1-2: Kontext & Fuehrung)",
            "modules": ",".join(CLUSTER_KERN),
            "hnsw:space": "cosine"
        }
    )
    print(f"  ✅ osp_kern erstellt")
    
    # osp_erweitert erstellen
    CLUSTER_ERWEITERT = ["KST", "DMS", "TM", "IT", "HR", "RES", "CMS", "FIN", "STR", "BN"]
    osp_erweitert = client.get_or_create_collection(
        name="osp_erweitert",
        metadata={
            "description": "OSP Erweiterte Dokumente (Cluster 3-4: Kernprozesse & Support)",
            "modules": ",".join(CLUSTER_ERWEITERT),
            "hnsw:space": "cosine"
        }
    )
    print(f"  ✅ osp_erweitert erstellt")
    
    # Status
    print("\n  📊 Collection-Status:")
    for col in client.list_collections():
        print(f"    - {col.name}: {col.count()} Dokumente")
    
except Exception as e:
    print(f"  ❌ Fehler: {e}")
    sys.exit(1)
PYEOF

echo ""

# ============================================================
# PHASE 4: DOKUMENTE IMPORTIEREN
# ============================================================
echo "=== PHASE 4: DOKUMENTE IMPORTIEREN ==="
echo ""

DOCS_PATH="/mnt/HC_Volume_104189729/osp/documents"

if [ ! -d "$DOCS_PATH" ]; then
    echo "  ⚠️ Dokumenten-Verzeichnis $DOCS_PATH existiert nicht."
    echo "  Erstelle es und kopiere OSP-Markdown-Dateien dorthin."
    mkdir -p "$DOCS_PATH"
    echo ""
    echo "  Kopiere Dateien vom Windows-PC mit:"
    echo "  scp -r 'C:\\Users\\andre\\OneDrive...\\Main\\*' root@46.224.102.30:$DOCS_PATH/"
    echo ""
    read -p "Drücke Enter wenn Dateien kopiert sind..." -r
fi

echo "4.1 Importiere Dokumente..."

python3 << 'PYEOF'
import chromadb
import os
import glob
import hashlib

CHROMADB_HOST = "localhost"
CHROMADB_PORT = 8000
DOCS_PATH = "/mnt/HC_Volume_104189729/osp/documents"

CLUSTER_KERN = ["ORG", "KOM", "QM", "GF", "PM", "AV", "VT", "EK"]
CLUSTER_ERWEITERT = ["KST", "DMS", "TM", "IT", "HR", "RES", "CMS", "FIN", "STR", "BN"]

def classify_document(filename):
    filename_upper = filename.upper()
    for module in CLUSTER_KERN:
        if module in filename_upper:
            return "kern"
    return "erweitert"

def generate_doc_id(content, filename):
    return hashlib.md5(f"{filename}_{content[:100]}".encode()).hexdigest()

try:
    print("  Verbinde zu ChromaDB...")
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    
    osp_kern = client.get_collection("osp_kern")
    osp_erweitert = client.get_collection("osp_erweitert")
    
    if not os.path.exists(DOCS_PATH):
        print(f"  ⚠️ Pfad {DOCS_PATH} existiert nicht. Überspringe Import.")
    else:
        md_files = glob.glob(f"{DOCS_PATH}/**/*.md", recursive=True)
        print(f"  📁 Gefunden: {len(md_files)} Markdown-Dateien")
        
        kern_count = 0
        erweitert_count = 0
        errors = 0
        
        for filepath in md_files:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                filename = os.path.basename(filepath)
                doc_id = generate_doc_id(content, filename)
                classification = classify_document(filename)
                
                metadata = {
                    "filename": filename,
                    "filepath": filepath,
                    "classification": classification
                }
                
                if classification == "kern":
                    osp_kern.upsert(ids=[doc_id], documents=[content], metadatas=[metadata])
                    kern_count += 1
                else:
                    osp_erweitert.upsert(ids=[doc_id], documents=[content], metadatas=[metadata])
                    erweitert_count += 1
                    
            except Exception as e:
                print(f"    ❌ {os.path.basename(filepath)}: {e}")
                errors += 1
        
        print(f"\n  📊 IMPORT ERGEBNIS:")
        print(f"    osp_kern: {osp_kern.count()} Dokumente ({kern_count} verarbeitet)")
        print(f"    osp_erweitert: {osp_erweitert.count()} Dokumente ({erweitert_count} verarbeitet)")
        if errors > 0:
            print(f"    ⚠️ Fehler: {errors}")

except Exception as e:
    print(f"  ❌ Fehler: {e}")
PYEOF

echo ""

# ============================================================
# PHASE 5: PIPELINE AKTUALISIEREN
# ============================================================
echo "=== PHASE 5: PIPELINE AKTUALISIEREN ==="
echo ""

echo "5.1 Erstelle Multi-Collection RAG Pipeline..."

mkdir -p /mnt/HC_Volume_104189729/osp/pipelines

cat > /mnt/HC_Volume_104189729/osp/pipelines/osp_rag.py << 'PIPELINE_EOF'
"""
OSP Multi-Collection RAG Pipeline
Verwendet osp_kern und osp_erweitert Collections
Version: 2.0
"""

from typing import List, Union, Generator
import chromadb
from anthropic import Anthropic
import logging
import os

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self):
        self.name = "[OSP] Claude RAG"
        self.kern_collection = None
        self.erweitert_collection = None
        self.anthropic = None
    
    async def on_startup(self):
        """Initialisiere ChromaDB und Anthropic"""
        try:
            # ChromaDB Client
            client = chromadb.HttpClient(host="chromadb", port=8000)
            
            # Collections laden
            self.kern_collection = client.get_collection(name="osp_kern")
            self.erweitert_collection = client.get_collection(name="osp_erweitert")
            
            kern_count = self.kern_collection.count()
            erweitert_count = self.erweitert_collection.count()
            
            logger.info(f"✅ osp_kern: {kern_count} docs")
            logger.info(f"✅ osp_erweitert: {erweitert_count} docs")
            
            # Anthropic Client
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                self.anthropic = Anthropic(api_key=api_key)
                logger.info("✅ Anthropic API verbunden")
            
            logger.info("✅ OSP RAG Pipeline bereit!")
            
        except Exception as e:
            logger.error(f"❌ Startup Error: {e}")
    
    async def on_shutdown(self):
        logger.info("🛑 OSP RAG Pipeline gestoppt")
    
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict
    ) -> str:
        """Hauptverarbeitung"""
        
        if not self.kern_collection or not self.erweitert_collection:
            return "❌ ChromaDB nicht verbunden. Bitte Container prüfen."
        
        try:
            # 1. Suche in beiden Collections
            kern_results = self.kern_collection.query(
                query_texts=[user_message],
                n_results=3
            )
            erweitert_results = self.erweitert_collection.query(
                query_texts=[user_message],
                n_results=3
            )
            
            # 2. Kombiniere Ergebnisse
            all_docs = []
            all_sources = []
            
            if kern_results.get("documents"):
                all_docs.extend(kern_results["documents"][0])
                if kern_results.get("metadatas"):
                    all_sources.extend([m.get("filename", "?") for m in kern_results["metadatas"][0]])
            
            if erweitert_results.get("documents"):
                all_docs.extend(erweitert_results["documents"][0])
                if erweitert_results.get("metadatas"):
                    all_sources.extend([m.get("filename", "?") for m in erweitert_results["metadatas"][0]])
            
            context = "\n\n---\n\n".join(all_docs)
            
            if not context.strip():
                return "📭 Keine relevanten Dokumente in osp_kern oder osp_erweitert gefunden."
            
            # 3. LLM-Antwort generieren
            if not self.anthropic:
                return f"📋 Kontext gefunden (LLM nicht konfiguriert):\n{context[:3000]}..."
            
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                temperature=0.2,
                messages=[{
                    "role": "user",
                    "content": f"""Du bist der OSP-Assistent für Rainer Schneider Kabelsatzbau GmbH & Co. KG.

KONTEXT aus OSP-Dokumenten:
{context}

FRAGE: {user_message}

REGELN (NULL-FEHLER-POLITIK):
- Antworte NUR basierend auf dem Kontext
- Wenn unsicher, sage es ehrlich
- Confidence-Level angeben: (C: XX%)
- Am Ende [OSP] wenn aus OSP-Dokumenten
- NIEMALS Informationen erfinden!

Antworte auf Deutsch:"""
                }]
            )
            
            sources_str = ", ".join(set(all_sources))
            return response.content[0].text + f"\n\n---\n📚 Quellen: {sources_str}"
            
        except Exception as e:
            logger.error(f"❌ Query Error: {e}")
            return f"❌ Fehler bei der Verarbeitung: {e}"

pipeline = Pipeline()
PIPELINE_EOF

echo "  ✅ Pipeline erstellt"

echo "5.2 Kopiere Pipeline in Container..."
docker cp /mnt/HC_Volume_104189729/osp/pipelines/osp_rag.py pipelines:/app/pipelines/ 2>/dev/null || echo "  (Pipeline-Container prüfen)"

echo "5.3 Starte Pipeline neu..."
docker restart pipelines
sleep 10
echo "  ✅ Pipeline neugestartet"

echo ""

# ============================================================
# PHASE 6: VALIDIERUNG
# ============================================================
echo "=== PHASE 6: VALIDIERUNG ==="
echo ""

echo "6.1 Collection-Status:"
curl -s http://localhost:8000/api/v2/collections | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    print('  Collections:')
    for c in data:
        print(f'    - {c[\"name\"]}')
except:
    print('  (Fehler beim Parsen)')
"

echo ""
echo "6.2 Pipeline-Logs:"
docker logs pipelines --tail 15 2>&1 | grep -E "osp_kern|osp_erweitert|Error|error|✅|❌" || echo "  (keine relevanten Logs)"

echo ""
echo "============================================================"
echo "  RECOVERY ABGESCHLOSSEN"
echo "============================================================"
echo ""
echo "  Test im Browser: http://46.224.102.30:3000"
echo "  → Neuer Chat"
echo "  → Modell: [OSP] Claude RAG"
echo "  → Testfrage: 'Was ist unsere Qualitätspolitik?'"
echo ""
echo "============================================================"
