#!/bin/bash
# ==============================================================================
# OSP_KPL ChromaDB Collection Setup Script
# ==============================================================================
# Version: 1.0
# Server: Hetzner CX33 (46.224.102.30)
# Erstellt: 2025-12-13
#
# Verwendung:
#   ./setup_osp_kpl.sh [--clear] [--verify-only]
#
# Optionen:
#   --clear       Collection vor Import leeren
#   --verify-only Nur Verifikation, kein Import
#   --help        Diese Hilfe anzeigen
# ==============================================================================

set -e  # Exit bei Fehlern

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Konfiguration
OSP_BASE="/opt/osp"
CHROMADB_DATA="${OSP_BASE}/chromadb/data"
DOCUMENTS_PATH="${OSP_BASE}/documents_kpl"
SCRIPT_PATH="${OSP_BASE}/scripts/osp_kpl_collection_setup.py"
LOG_PATH="${OSP_BASE}/logs"
LOG_FILE="${LOG_PATH}/osp_kpl_import_$(date +%Y%m%d_%H%M%S).log"

# Funktionen
print_header() {
    echo -e "${BLUE}"
    echo "============================================================"
    echo "  OSP_KPL ChromaDB Collection Setup"
    echo "============================================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

show_help() {
    echo "Verwendung: $0 [OPTIONEN]"
    echo ""
    echo "Optionen:"
    echo "  --clear         Collection vor Import leeren"
    echo "  --verify-only   Nur Verifikation durchführen"
    echo "  --help          Diese Hilfe anzeigen"
    echo ""
    echo "Beispiele:"
    echo "  $0                    # Standard-Import"
    echo "  $0 --clear            # Clear + Import"
    echo "  $0 --verify-only      # Nur Status prüfen"
    exit 0
}

check_prerequisites() {
    print_info "Prüfe Voraussetzungen..."
    
    # Python prüfen
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 nicht gefunden!"
        exit 1
    fi
    print_success "Python3: $(python3 --version)"
    
    # ChromaDB Container prüfen
    if docker ps | grep -q chromadb; then
        print_success "ChromaDB Container läuft"
    else
        print_warning "ChromaDB Container nicht aktiv!"
        print_info "Versuche zu starten..."
        docker-compose -f ${OSP_BASE}/docker-compose.yml up -d chromadb
        sleep 5
    fi
    
    # Verzeichnisse prüfen
    if [ ! -d "$DOCUMENTS_PATH" ]; then
        print_error "Dokumente-Verzeichnis nicht gefunden: $DOCUMENTS_PATH"
        exit 1
    fi
    print_success "Dokumente-Pfad: $DOCUMENTS_PATH"
    
    if [ ! -d "$CHROMADB_DATA" ]; then
        print_warning "ChromaDB-Daten-Verzeichnis erstellen..."
        mkdir -p "$CHROMADB_DATA"
    fi
    print_success "ChromaDB-Pfad: $CHROMADB_DATA"
    
    # Log-Verzeichnis
    mkdir -p "$LOG_PATH"
    print_success "Log-Pfad: $LOG_PATH"
    
    # Script prüfen
    if [ ! -f "$SCRIPT_PATH" ]; then
        print_error "Import-Script nicht gefunden: $SCRIPT_PATH"
        exit 1
    fi
    print_success "Import-Script: $SCRIPT_PATH"
}

count_documents() {
    print_info "Zähle Dokumente..."
    
    md_count=$(find "$DOCUMENTS_PATH" -name "*.md" | wc -l)
    print_info "Gefundene Markdown-Dateien: $md_count"
    
    # Full-Doc Dateien prüfen
    full_doc_files=("TM_CORE_Maschinen_Anlagen.md" "TM_WKZ_Werkzeuge.md" "HR_CORE_Personalstamm.md" "AV_AGK_Arbeitsgang_Katalog.md")
    
    for file in "${full_doc_files[@]}"; do
        if find "$DOCUMENTS_PATH" -name "$file" | grep -q .; then
            print_success "Full-Doc: $file"
        else
            print_warning "Full-Doc fehlt: $file"
        fi
    done
}

install_dependencies() {
    print_info "Installiere Python-Abhängigkeiten..."
    
    pip3 install -q chromadb sentence-transformers
    print_success "Abhängigkeiten installiert"
}

run_import() {
    local args="$1"
    
    print_header
    
    print_info "Starte Import..."
    print_info "Log-Datei: $LOG_FILE"
    echo ""
    
    # Python-Script ausführen
    python3 "$SCRIPT_PATH" \
        --path "$DOCUMENTS_PATH" \
        --chromadb-path "$CHROMADB_DATA" \
        $args \
        2>&1 | tee "$LOG_FILE"
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        print_success "Import erfolgreich abgeschlossen!"
    else
        print_error "Import fehlgeschlagen! Siehe Log: $LOG_FILE"
        exit 1
    fi
}

# ==============================================================================
# MAIN
# ==============================================================================

# Parameter parsen
CLEAR_FLAG=""
VERIFY_ONLY_FLAG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --clear)
            CLEAR_FLAG="--clear"
            shift
            ;;
        --verify-only)
            VERIFY_ONLY_FLAG="--verify-only"
            shift
            ;;
        --help|-h)
            show_help
            ;;
        *)
            print_error "Unbekannte Option: $1"
            show_help
            ;;
    esac
done

# Ausführung
print_header

echo "Datum: $(date)"
echo "Server: $(hostname)"
echo ""

check_prerequisites
count_documents

if [ -n "$VERIFY_ONLY_FLAG" ]; then
    print_info "Modus: Nur Verifikation"
    run_import "--verify-only"
else
    if [ -n "$CLEAR_FLAG" ]; then
        print_warning "Modus: Clear + Import"
        run_import "--clear"
    else
        print_info "Modus: Standard-Import"
        run_import ""
    fi
fi

echo ""
print_info "============================================================"
print_info "  Setup abgeschlossen!"
print_info "============================================================"
echo ""
print_info "Nächste Schritte:"
echo "  1. Open WebUI Pipeline konfigurieren"
echo "  2. RAG-Queries testen"
echo "  3. API System-Prompt aktualisieren"
echo ""
