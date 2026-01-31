#!/bin/bash
# =============================================================================
# NZA Workflows Import via n8n REST API
# Nutzt die n8n API zum Import (API muss aktiviert sein)
# =============================================================================

WORKFLOW_DIR="/mnt/HC_Volume_104189729/osp/nza/workflows"
N8N_URL="http://127.0.0.1:5678"
N8N_API_KEY="${N8N_API_KEY:-}"  # Aus Umgebungsvariable oder hier setzen

# Farben
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=========================================="
echo "  NZA Workflows Import via API"
echo "=========================================="
echo ""

# API Key prüfen
if [ -z "$N8N_API_KEY" ]; then
    echo -e "${YELLOW}Hinweis: N8N_API_KEY nicht gesetzt${NC}"
    echo "Setze mit: export N8N_API_KEY='dein-api-key'"
    echo "API Key findest du in n8n unter: Settings → API"
    echo ""
    read -p "API Key eingeben (oder Enter zum Abbrechen): " N8N_API_KEY
    if [ -z "$N8N_API_KEY" ]; then
        exit 1
    fi
fi

# API-Verbindung testen
echo -n "Teste API-Verbindung... "
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "$N8N_URL/healthz")
if [ "$HEALTH" != "200" ]; then
    echo -e "${RED}Fehler: n8n nicht erreichbar unter $N8N_URL${NC}"
    exit 1
fi
echo -e "${GREEN}OK${NC}"

# Workflows importieren
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
        echo -e "${YELLOW}⚠ Übersprungen: $WF${NC}"
        continue
    fi

    echo -n "Importiere $WF ... "

    RESPONSE=$(curl -s -X POST "$N8N_URL/api/v1/workflows" \
        -H "Content-Type: application/json" \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -d @"$WF_PATH")

    if echo "$RESPONSE" | grep -q '"id"'; then
        WF_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
        echo -e "${GREEN}✓ (ID: $WF_ID)${NC}"
        ((SUCCESS++))
    else
        echo -e "${RED}✗${NC}"
        ERROR=$(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
        echo "  Fehler: ${ERROR:-Unbekannter Fehler}"
        ((FAILED++))
    fi
done

echo ""
echo "=========================================="
echo -e "Ergebnis: ${GREEN}$SUCCESS erfolgreich${NC}, ${RED}$FAILED fehlgeschlagen${NC}"
echo "=========================================="
