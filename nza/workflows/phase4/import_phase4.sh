#!/bin/bash
# ==============================================
# NZA Phase4 Workflows Import Script
# ==============================================
# Dieses Script importiert die korrigierten NZA-Workflows in n8n
#
# Ausführen auf dem Server:
#   cd /mnt/HC_Volume_104189729/osp/nza/workflows/phase4
#   chmod +x import_phase4.sh
#   ./import_phase4.sh
# ==============================================

set -e

# Konfiguration
N8N_URL="${N8N_URL:-http://localhost:5678}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==================================="
echo "NZA Phase4 Workflows Import"
echo "==================================="
echo "n8n URL: $N8N_URL"
echo "Workflows: $SCRIPT_DIR"
echo ""

# Prüfe ob n8n erreichbar ist
echo "Prüfe n8n Verbindung..."
if ! curl -s "${N8N_URL}/healthz" > /dev/null 2>&1; then
    echo "FEHLER: n8n nicht erreichbar unter ${N8N_URL}"
    echo "Starte n8n zuerst: docker-compose up -d"
    exit 1
fi
echo "✓ n8n ist erreichbar"
echo ""

# Liste der zu importierenden Workflows
WORKFLOWS=(
    "NZA-Prozesse-List.json"
    "NZA-Prozesse-Create.json"
    "NZA-Prozesse-Update.json"
    "NZA-Massnahmen-List.json"
    "NZA-Massnahmen-Create.json"
    "NZA-Massnahmen-Update.json"
    "NZA-Bilder-List.json"
    "NZA-Kosten-Info.json"
    "NZA-Kosten-Berechnen.json"
)

echo "Zu importierende Workflows:"
for wf in "${WORKFLOWS[@]}"; do
    if [ -f "$SCRIPT_DIR/$wf" ]; then
        echo "  ✓ $wf"
    else
        echo "  ✗ $wf (NICHT GEFUNDEN)"
    fi
done
echo ""

# Prüfe ob API-Key gesetzt ist
if [ -z "$N8N_API_KEY" ]; then
    echo "HINWEIS: N8N_API_KEY nicht gesetzt."
    echo ""
    echo "Option 1: API-Key setzen und Script erneut starten:"
    echo "  export N8N_API_KEY='dein-api-key'"
    echo "  ./import_phase4.sh"
    echo ""
    echo "Option 2: Manueller Import über Web-UI:"
    echo "  1. Öffne https://n8n.schneider-kabelsatzbau.de/"
    echo "  2. Workflows → Import from File"
    echo "  3. Importiere jeden Workflow einzeln"
    echo "  4. Aktiviere jeden Workflow (Toggle ON)"
    echo ""
    echo "Die Workflow-Dateien befinden sich in:"
    echo "  $SCRIPT_DIR"
    exit 0
fi

echo "Importiere Workflows via API..."
echo ""

for wf in "${WORKFLOWS[@]}"; do
    if [ -f "$SCRIPT_DIR/$wf" ]; then
        echo -n "Importiere $wf... "

        RESPONSE=$(curl -s -X POST "${N8N_URL}/api/v1/workflows" \
            -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
            -H "Content-Type: application/json" \
            -d @"$SCRIPT_DIR/$wf")

        if echo "$RESPONSE" | grep -q '"id"'; then
            WF_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
            echo "✓ (ID: $WF_ID)"

            # Workflow aktivieren
            echo -n "  Aktiviere Workflow... "
            curl -s -X PATCH "${N8N_URL}/api/v1/workflows/${WF_ID}" \
                -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
                -H "Content-Type: application/json" \
                -d '{"active": true}' > /dev/null
            echo "✓"
        else
            echo "✗ FEHLER"
            echo "  Response: $RESPONSE"
        fi
    fi
done

echo ""
echo "==================================="
echo "Import abgeschlossen!"
echo "==================================="
echo ""
echo "Test-URLs:"
echo "  curl https://osp.schneider-kabelsatzbau.de/api/nza/prozesse"
echo "  curl https://osp.schneider-kabelsatzbau.de/api/nza/massnahmen"
echo "  curl https://osp.schneider-kabelsatzbau.de/api/nza/bilder"
echo "  curl https://osp.schneider-kabelsatzbau.de/api/nza/kosten"
