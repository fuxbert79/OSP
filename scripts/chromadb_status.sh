#!/bin/bash
#
# OSP ChromaDB Status Helper
# ==========================
#
# Zeigt Status und Collections der ChromaDB an.
# Verwendet die korrekte API v2 für ChromaDB 1.0.0
#
# Verwendung:
#   ./chromadb_status.sh              # Alle Collections anzeigen
#   ./chromadb_status.sh heartbeat    # Nur Heartbeat prüfen
#   ./chromadb_status.sh count        # Collection-Counts anzeigen
#   ./chromadb_status.sh details      # Detaillierte Collection-Infos
#
# Erstellt: 2025-12-15
#

# Konfiguration
CHROMADB_HOST="${CHROMADB_HOST:-localhost}"
CHROMADB_PORT="${CHROMADB_PORT:-8000}"
CHROMADB_TENANT="${CHROMADB_TENANT:-default_tenant}"
CHROMADB_DATABASE="${CHROMADB_DATABASE:-default_database}"

# API Base URL (ChromaDB 1.0.0)
API_BASE="http://${CHROMADB_HOST}:${CHROMADB_PORT}/api/v2"
COLLECTIONS_URL="${API_BASE}/tenants/${CHROMADB_TENANT}/databases/${CHROMADB_DATABASE}/collections"

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktionen
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  OSP ChromaDB Status (v1.0.0)${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo -e "  Host: ${CHROMADB_HOST}:${CHROMADB_PORT}"
    echo -e "  Tenant: ${CHROMADB_TENANT}"
    echo -e "  Database: ${CHROMADB_DATABASE}"
    echo ""
}

check_heartbeat() {
    local response
    response=$(curl -s "${API_BASE}/heartbeat" 2>/dev/null)

    if [[ $response == *"heartbeat"* ]]; then
        echo -e "${GREEN}✓ ChromaDB erreichbar${NC}"
        return 0
    else
        echo -e "${RED}✗ ChromaDB nicht erreichbar${NC}"
        echo "  URL: ${API_BASE}/heartbeat"
        return 1
    fi
}

list_collections() {
    local response
    response=$(curl -s "${COLLECTIONS_URL}" 2>/dev/null)

    if [[ -z "$response" ]] || [[ "$response" == *"error"* ]]; then
        echo -e "${RED}Fehler beim Abrufen der Collections${NC}"
        echo "$response"
        return 1
    fi

    echo -e "${GREEN}Collections:${NC}"
    echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if not data:
        print('  (keine Collections)')
    else:
        for col in data:
            name = col.get('name', 'N/A')
            dim = col.get('dimension', 'N/A')
            meta = col.get('metadata', {})
            model = meta.get('embedding_model', 'N/A')
            print(f'  - {name} (dim: {dim}, model: {model})')
except json.JSONDecodeError as e:
    print(f'  JSON Parse Error: {e}')
except Exception as e:
    print(f'  Fehler: {e}')
"
}

show_counts() {
    echo -e "${GREEN}Collection Document Counts:${NC}"

    # Nutze Python-Client für korrekte Counts (REST API braucht UUID)
    python3 -c "
import chromadb
try:
    client = chromadb.HttpClient(host='${CHROMADB_HOST}', port=${CHROMADB_PORT})
    collections = client.list_collections()
    if not collections:
        print('  (keine Collections)')
    else:
        for col in collections:
            count = client.get_collection(col.name).count()
            print(f'  - {col.name}: \033[1;33m{count}\033[0m Dokumente')
except Exception as e:
    print(f'  Fehler: {e}')
" 2>/dev/null
}

show_details() {
    echo -e "${GREEN}Collection Details:${NC}"
    curl -s "${COLLECTIONS_URL}" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for col in data:
        print(f\"\\n  === {col.get('name', 'N/A')} ===\")
        print(f\"  ID: {col.get('id', 'N/A')}\")
        print(f\"  Dimension: {col.get('dimension', 'N/A')}\")
        meta = col.get('metadata', {})
        print(f\"  Embedding Model: {meta.get('embedding_model', 'N/A')}\")
        print(f\"  Created: {meta.get('created', 'N/A')}\")
        print(f\"  HNSW Space: {meta.get('hnsw:space', 'N/A')}\")
except Exception as e:
    print(f'Fehler: {e}')
"
}

show_help() {
    echo "Verwendung: $0 [BEFEHL]"
    echo ""
    echo "Befehle:"
    echo "  (leer)      Alle Collections auflisten"
    echo "  heartbeat   Nur Heartbeat prüfen"
    echo "  count       Document Counts anzeigen"
    echo "  details     Detaillierte Collection-Infos"
    echo "  help        Diese Hilfe anzeigen"
    echo ""
    echo "API-Pfade (ChromaDB 1.0.0):"
    echo "  Heartbeat:    ${API_BASE}/heartbeat"
    echo "  Collections:  ${COLLECTIONS_URL}"
    echo ""
    echo "Umgebungsvariablen:"
    echo "  CHROMADB_HOST     (default: localhost)"
    echo "  CHROMADB_PORT     (default: 8000)"
    echo "  CHROMADB_TENANT   (default: default_tenant)"
    echo "  CHROMADB_DATABASE (default: default_database)"
}

# Main
print_header

case "${1:-}" in
    heartbeat)
        check_heartbeat
        ;;
    count)
        check_heartbeat && show_counts
        ;;
    details)
        check_heartbeat && show_details
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        check_heartbeat && list_collections
        ;;
esac
