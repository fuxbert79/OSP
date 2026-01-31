#!/bin/bash
# =============================================================================
# NZA Workflows Import Script
# Importiert alle n8n Workflows automatisch
# =============================================================================

WORKFLOW_DIR="/mnt/HC_Volume_104189729/osp/nza/workflows"
N8N_CONTAINER="n8n"  # Name des Docker Containers anpassen falls nötig

# Farben
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=========================================="
echo "  NZA Workflows Import"
echo "=========================================="
echo ""

# Prüfen ob Docker läuft und Container existiert
if ! docker ps | grep -q "$N8N_CONTAINER"; then
    echo -e "${RED}Fehler: n8n Container '$N8N_CONTAINER' nicht gefunden!${NC}"
    echo "Verfügbare Container:"
    docker ps --format "table {{.Names}}\t{{.Status}}"
    exit 1
fi

# Workflows in Reihenfolge importieren
WORKFLOWS=(
    "01_NZA_Setup_Listen.json"
    "02_NZA_Setup_Spalten_KPL.json"
    "03_NZA_Import_Mitarbeiter.json"
    "04_NZA_Import_Config.json"
    "05_NZA_Prozesse_API.json"
    "06_NZA_Mitarbeiter_API.json"
    "07_NZA_Massnahmen_API.json"
    "08_NZA_Bilder_API.json"
    "08b_NZA_Bilder_Upload.json"
    "09_NZA_Notify_API.json"
    "10_NZA_Kosten_API.json"
    "11_NZA_Config_API.json"
    "12_NZA_KPIs_API.json"
)

SUCCESS=0
FAILED=0

for WF in "${WORKFLOWS[@]}"; do
    WF_PATH="$WORKFLOW_DIR/$WF"

    if [ ! -f "$WF_PATH" ]; then
        echo -e "${YELLOW}⚠ Übersprungen: $WF (nicht gefunden)${NC}"
        continue
    fi

    echo -n "Importiere $WF ... "

    # Workflow in Container kopieren und importieren
    docker cp "$WF_PATH" "$N8N_CONTAINER:/tmp/$WF" 2>/dev/null
    RESULT=$(docker exec "$N8N_CONTAINER" n8n import:workflow --input="/tmp/$WF" 2>&1)

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC}"
        ((SUCCESS++))
    else
        echo -e "${RED}✗${NC}"
        echo "  Fehler: $RESULT"
        ((FAILED++))
    fi

    # Temp-Datei im Container löschen
    docker exec "$N8N_CONTAINER" rm -f "/tmp/$WF" 2>/dev/null
done

echo ""
echo "=========================================="
echo -e "Ergebnis: ${GREEN}$SUCCESS erfolgreich${NC}, ${RED}$FAILED fehlgeschlagen${NC}"
echo "=========================================="
echo ""
echo "Nächste Schritte:"
echo "1. n8n UI öffnen: http://localhost:5678"
echo "2. Credentials in jedem Workflow zuweisen (Microsoft OAuth2)"
echo "3. Setup-Workflows 01-04 einmalig ausführen"
echo "4. API-Workflows 05-12 aktivieren (Toggle ON)"
