#!/usr/bin/env python3
"""
RMS Dashboard API Workflow für n8n
Erstellt den Webhook-Workflow für SharePoint-Integration

Verwendung:
    export N8N_API_KEY="..."
    export N8N_BASE_URL="http://127.0.0.1:5678"
    python3 create_dashboard_api.py

Autor: AL (via Claude)
Stand: 2026-01-28
"""

import json
import urllib.request
import urllib.error
import os
import sys
from typing import Optional

# Konfiguration
N8N_BASE_URL = os.environ.get('N8N_BASE_URL', 'http://127.0.0.1:5678')
N8N_API_KEY = os.environ.get('N8N_API_KEY', '')

# SharePoint IDs
SITE_ID = "rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"
REKLAMATIONEN_LIST_ID = "e9b1d926-085a-4435-a012-114ca9ba59a8"
MASSNAHMEN_LIST_ID = "3768f2d8-878c-4a5f-bd52-7486fe93289d"
SCHRIFTVERKEHR_LIST_ID = "741c6ae8-88bb-406b-bf85-2e11192a528f"
KPI_LIST_ID = "f66e805e-8315-4714-a18e-5c59a05d631f"


def create_workflow() -> dict:
    """Erstellt die Workflow-Definition für die RMS Dashboard API."""
    return {
        "name": "RMS-Dashboard-API",
        "nodes": [
            # Webhook Trigger
            {
                "parameters": {
                    "httpMethod": "GET",
                    "path": "rms/kpis",
                    "responseMode": "responseNode",
                    "options": {
                        "allowedOrigins": "*"
                    }
                },
                "id": "webhook-kpis",
                "name": "Webhook KPIs",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [250, 100],
                "webhookId": "rms-kpis"
            },
            {
                "parameters": {
                    "httpMethod": "GET",
                    "path": "rms/reklamationen",
                    "responseMode": "responseNode",
                    "options": {
                        "allowedOrigins": "*"
                    }
                },
                "id": "webhook-reklamationen",
                "name": "Webhook Reklamationen",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [250, 300],
                "webhookId": "rms-reklamationen"
            },
            {
                "parameters": {
                    "httpMethod": "GET",
                    "path": "rms/reklamation/:id",
                    "responseMode": "responseNode",
                    "options": {
                        "allowedOrigins": "*"
                    }
                },
                "id": "webhook-detail",
                "name": "Webhook Detail",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [250, 500],
                "webhookId": "rms-detail"
            },
            {
                "parameters": {
                    "httpMethod": "GET",
                    "path": "rms/charts",
                    "responseMode": "responseNode",
                    "options": {
                        "allowedOrigins": "*"
                    }
                },
                "id": "webhook-charts",
                "name": "Webhook Charts",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [250, 700],
                "webhookId": "rms-charts"
            },

            # SharePoint Nodes für KPIs
            {
                "parameters": {
                    "resource": "listItem",
                    "operation": "getAll",
                    "siteId": SITE_ID,
                    "listId": REKLAMATIONEN_LIST_ID,
                    "returnAll": True,
                    "options": {}
                },
                "id": "sp-kpis",
                "name": "SP Get All for KPIs",
                "type": "n8n-nodes-base.microsoftSharePoint",
                "typeVersion": 1,
                "position": [500, 100],
                "credentials": {
                    "microsoftSharePointOAuth2Api": {
                        "id": "sharepoint-cred",
                        "name": "SharePoint OAuth2"
                    }
                }
            },

            # KPI Berechnung
            {
                "parameters": {
                    "jsCode": """
const items = $input.all();
const today = new Date();

let offen = 0;
let kritisch = 0;
let ueberfaellig = 0;
let totalDays = 0;
let closedCount = 0;

for (const item of items) {
    const fields = item.json.fields || item.json;
    const status = fields.Rekla_Status || '';
    const prioritaet = fields.Prioritaet || '';
    const zieldatum = fields.Zieldatum ? new Date(fields.Zieldatum) : null;
    const erfassung = fields.Erfassungsdatum ? new Date(fields.Erfassungsdatum) : null;
    const abschluss = fields.Abschlussdatum ? new Date(fields.Abschlussdatum) : null;

    if (status !== 'Abgeschlossen') {
        offen++;
        if (prioritaet === 'kritisch') kritisch++;
        if (zieldatum && zieldatum < today) ueberfaellig++;
    } else if (erfassung && abschluss) {
        const days = (abschluss - erfassung) / (1000 * 60 * 60 * 24);
        totalDays += days;
        closedCount++;
    }
}

const durchschnitt = closedCount > 0 ? totalDays / closedCount : 0;

return [{
    json: {
        offen,
        kritisch,
        ueberfaellig,
        durchschnitt: Math.round(durchschnitt * 10) / 10
    }
}];
"""
                },
                "id": "calc-kpis",
                "name": "Calculate KPIs",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [750, 100]
            },

            # Response Nodes
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{ $json }}",
                    "options": {
                        "responseHeaders": {
                            "entries": [
                                {"name": "Access-Control-Allow-Origin", "value": "*"},
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        }
                    }
                },
                "id": "response-kpis",
                "name": "Response KPIs",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [1000, 100]
            },

            # SharePoint für Reklamationen-Liste
            {
                "parameters": {
                    "resource": "listItem",
                    "operation": "getAll",
                    "siteId": SITE_ID,
                    "listId": REKLAMATIONEN_LIST_ID,
                    "returnAll": True,
                    "options": {
                        "orderBy": "Erfassungsdatum desc"
                    }
                },
                "id": "sp-reklamationen",
                "name": "SP Get Reklamationen",
                "type": "n8n-nodes-base.microsoftSharePoint",
                "typeVersion": 1,
                "position": [500, 300],
                "credentials": {
                    "microsoftSharePointOAuth2Api": {
                        "id": "sharepoint-cred",
                        "name": "SharePoint OAuth2"
                    }
                }
            },

            # Filter und Format Reklamationen
            {
                "parameters": {
                    "jsCode": """
const items = $input.all();
const query = $('Webhook Reklamationen').first().json.query || {};

let result = items.map(item => {
    const fields = item.json.fields || item.json;
    return {
        id: item.json.id || fields.ID,
        QA_ID: fields.QA_ID || fields.Title,
        Rekla_Typ: fields.Rekla_Typ,
        Title: fields.Title || fields.Betreff,
        Rekla_Status: fields.Rekla_Status,
        Prioritaet: fields.Prioritaet,
        KST: fields.KST,
        Erfassungsdatum: fields.Erfassungsdatum
    };
});

// Filter anwenden
if (query.typ) {
    result = result.filter(r => r.Rekla_Typ === query.typ);
}
if (query.status) {
    result = result.filter(r => r.Rekla_Status === query.status);
}
if (query.kst) {
    result = result.filter(r => r.KST === query.kst);
}

return [{ json: result }];
"""
                },
                "id": "format-reklamationen",
                "name": "Format Reklamationen",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [750, 300]
            },

            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{ $json }}",
                    "options": {
                        "responseHeaders": {
                            "entries": [
                                {"name": "Access-Control-Allow-Origin", "value": "*"},
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        }
                    }
                },
                "id": "response-reklamationen",
                "name": "Response Reklamationen",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [1000, 300]
            },

            # Detail-Abruf
            {
                "parameters": {
                    "resource": "listItem",
                    "operation": "get",
                    "siteId": SITE_ID,
                    "listId": REKLAMATIONEN_LIST_ID,
                    "itemId": "={{ $json.params.id }}"
                },
                "id": "sp-detail",
                "name": "SP Get Detail",
                "type": "n8n-nodes-base.microsoftSharePoint",
                "typeVersion": 1,
                "position": [500, 500],
                "credentials": {
                    "microsoftSharePointOAuth2Api": {
                        "id": "sharepoint-cred",
                        "name": "SharePoint OAuth2"
                    }
                }
            },

            # Maßnahmen für Detail
            {
                "parameters": {
                    "resource": "listItem",
                    "operation": "getAll",
                    "siteId": SITE_ID,
                    "listId": MASSNAHMEN_LIST_ID,
                    "returnAll": True,
                    "options": {
                        "filter": "ReklamationId eq {{ $json.params.id }}"
                    }
                },
                "id": "sp-massnahmen",
                "name": "SP Get Massnahmen",
                "type": "n8n-nodes-base.microsoftSharePoint",
                "typeVersion": 1,
                "position": [500, 600],
                "credentials": {
                    "microsoftSharePointOAuth2Api": {
                        "id": "sharepoint-cred",
                        "name": "SharePoint OAuth2"
                    }
                }
            },

            # Schriftverkehr für Detail
            {
                "parameters": {
                    "resource": "listItem",
                    "operation": "getAll",
                    "siteId": SITE_ID,
                    "listId": SCHRIFTVERKEHR_LIST_ID,
                    "returnAll": True,
                    "options": {
                        "filter": "ReklamationId eq {{ $json.params.id }}"
                    }
                },
                "id": "sp-schriftverkehr",
                "name": "SP Get Schriftverkehr",
                "type": "n8n-nodes-base.microsoftSharePoint",
                "typeVersion": 1,
                "position": [500, 700],
                "credentials": {
                    "microsoftSharePointOAuth2Api": {
                        "id": "sharepoint-cred",
                        "name": "SharePoint OAuth2"
                    }
                }
            },

            # Detail kombinieren
            {
                "parameters": {
                    "jsCode": """
const reklamation = $('SP Get Detail').first().json;
const massnahmen = $('SP Get Massnahmen').all();
const schriftverkehr = $('SP Get Schriftverkehr').all();

const fields = reklamation.fields || reklamation;

return [{
    json: {
        id: reklamation.id || fields.ID,
        QA_ID: fields.QA_ID || fields.Title,
        Rekla_Typ: fields.Rekla_Typ,
        Title: fields.Title || fields.Betreff,
        Rekla_Status: fields.Rekla_Status,
        Prioritaet: fields.Prioritaet,
        KST: fields.KST,
        Erfassungsdatum: fields.Erfassungsdatum,
        Zieldatum: fields.Zieldatum,
        Verantwortlich: fields.Verantwortlich,
        Beschreibung: fields.Beschreibung,
        sharePointUrl: `https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS/Lists/Reklamationen/DispForm.aspx?ID=${reklamation.id}`,
        massnahmen: massnahmen.map(m => ({
            Title: m.json.fields?.Title || m.json.Title,
            Termin: m.json.fields?.Termin || m.json.Termin,
            Status: m.json.fields?.Status || m.json.Status
        })),
        schriftverkehr: schriftverkehr.map(s => ({
            Datum: s.json.fields?.Datum || s.json.Datum,
            Typ: s.json.fields?.Typ || s.json.Typ,
            Betreff: s.json.fields?.Betreff || s.json.Betreff
        }))
    }
}];
"""
                },
                "id": "combine-detail",
                "name": "Combine Detail",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [750, 550]
            },

            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{ $json }}",
                    "options": {
                        "responseHeaders": {
                            "entries": [
                                {"name": "Access-Control-Allow-Origin", "value": "*"},
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        }
                    }
                },
                "id": "response-detail",
                "name": "Response Detail",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [1000, 550]
            },

            # Charts Daten
            {
                "parameters": {
                    "resource": "listItem",
                    "operation": "getAll",
                    "siteId": SITE_ID,
                    "listId": REKLAMATIONEN_LIST_ID,
                    "returnAll": True,
                    "options": {}
                },
                "id": "sp-charts",
                "name": "SP Get All for Charts",
                "type": "n8n-nodes-base.microsoftSharePoint",
                "typeVersion": 1,
                "position": [500, 800],
                "credentials": {
                    "microsoftSharePointOAuth2Api": {
                        "id": "sharepoint-cred",
                        "name": "SharePoint OAuth2"
                    }
                }
            },

            # Chart-Daten berechnen
            {
                "parameters": {
                    "jsCode": """
const items = $input.all();
const monthNames = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];

// Trend: Letzte 6 Monate
const trendData = {};
const typData = { KUNDE: 0, LIEFERANT: 0, INTERN: 0 };
const kstData = {};

for (const item of items) {
    const fields = item.json.fields || item.json;
    const typ = fields.Rekla_Typ || 'INTERN';
    const kst = fields.KST || 'Unbekannt';
    const datum = fields.Erfassungsdatum ? new Date(fields.Erfassungsdatum) : null;

    // Typ
    if (typData.hasOwnProperty(typ)) {
        typData[typ]++;
    }

    // KST
    kstData[kst] = (kstData[kst] || 0) + 1;

    // Trend (letzte 6 Monate)
    if (datum) {
        const key = `${datum.getFullYear()}-${String(datum.getMonth() + 1).padStart(2, '0')}`;
        trendData[key] = (trendData[key] || 0) + 1;
    }
}

// Trend sortieren und letzte 6 Monate nehmen
const sortedMonths = Object.keys(trendData).sort().slice(-6);
const trendLabels = sortedMonths.map(m => {
    const [year, month] = m.split('-');
    return monthNames[parseInt(month) - 1];
});
const trendValues = sortedMonths.map(m => trendData[m]);

// KST sortieren
const sortedKst = Object.entries(kstData).sort((a, b) => b[1] - a[1]);

return [{
    json: {
        trend: {
            labels: trendLabels,
            values: trendValues
        },
        typ: [typData.KUNDE, typData.LIEFERANT, typData.INTERN],
        kst: {
            labels: sortedKst.map(k => k[0]),
            values: sortedKst.map(k => k[1])
        }
    }
}];
"""
                },
                "id": "calc-charts",
                "name": "Calculate Charts",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [750, 800]
            },

            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{ $json }}",
                    "options": {
                        "responseHeaders": {
                            "entries": [
                                {"name": "Access-Control-Allow-Origin", "value": "*"},
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        }
                    }
                },
                "id": "response-charts",
                "name": "Response Charts",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [1000, 800]
            }
        ],
        "connections": {
            "Webhook KPIs": {
                "main": [[{"node": "SP Get All for KPIs", "type": "main", "index": 0}]]
            },
            "SP Get All for KPIs": {
                "main": [[{"node": "Calculate KPIs", "type": "main", "index": 0}]]
            },
            "Calculate KPIs": {
                "main": [[{"node": "Response KPIs", "type": "main", "index": 0}]]
            },
            "Webhook Reklamationen": {
                "main": [[{"node": "SP Get Reklamationen", "type": "main", "index": 0}]]
            },
            "SP Get Reklamationen": {
                "main": [[{"node": "Format Reklamationen", "type": "main", "index": 0}]]
            },
            "Format Reklamationen": {
                "main": [[{"node": "Response Reklamationen", "type": "main", "index": 0}]]
            },
            "Webhook Detail": {
                "main": [[
                    {"node": "SP Get Detail", "type": "main", "index": 0},
                    {"node": "SP Get Massnahmen", "type": "main", "index": 0},
                    {"node": "SP Get Schriftverkehr", "type": "main", "index": 0}
                ]]
            },
            "SP Get Detail": {
                "main": [[{"node": "Combine Detail", "type": "main", "index": 0}]]
            },
            "SP Get Massnahmen": {
                "main": [[{"node": "Combine Detail", "type": "main", "index": 0}]]
            },
            "SP Get Schriftverkehr": {
                "main": [[{"node": "Combine Detail", "type": "main", "index": 0}]]
            },
            "Combine Detail": {
                "main": [[{"node": "Response Detail", "type": "main", "index": 0}]]
            },
            "Webhook Charts": {
                "main": [[{"node": "SP Get All for Charts", "type": "main", "index": 0}]]
            },
            "SP Get All for Charts": {
                "main": [[{"node": "Calculate Charts", "type": "main", "index": 0}]]
            },
            "Calculate Charts": {
                "main": [[{"node": "Response Charts", "type": "main", "index": 0}]]
            }
        },
        "active": True,
        "settings": {
            "executionOrder": "v1"
        }
    }


def deploy_workflow(workflow: dict) -> Optional[dict]:
    """Deployt den Workflow via n8n API."""
    if not N8N_API_KEY:
        print("FEHLER: N8N_API_KEY nicht gesetzt!")
        print("Setze: export N8N_API_KEY='dein-api-key'")
        return None

    url = f"{N8N_BASE_URL}/api/v1/workflows"
    data = json.dumps(workflow).encode('utf-8')

    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-N8N-API-KEY', N8N_API_KEY)

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Fehler {e.code}: {error_body}")
        return None
    except urllib.error.URLError as e:
        print(f"Verbindungsfehler: {e.reason}")
        return None


def export_workflow(workflow: dict, filename: str = "rms_dashboard_api_workflow.json"):
    """Exportiert den Workflow als JSON-Datei."""
    filepath = os.path.join(os.path.dirname(__file__), "..", "rms", "workflows", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"Workflow exportiert: {filepath}")
    return filepath


def main():
    """Hauptfunktion."""
    print("=" * 60)
    print("RMS Dashboard API Workflow Generator")
    print("=" * 60)

    workflow = create_workflow()

    # Immer als JSON exportieren
    export_path = export_workflow(workflow)

    # Deployment nur wenn API Key vorhanden
    if N8N_API_KEY:
        print("\nDeploye Workflow zu n8n...")
        result = deploy_workflow(workflow)
        if result:
            print(f"Workflow erstellt!")
            print(f"  ID: {result.get('id')}")
            print(f"  Name: {result.get('name')}")
            print(f"  Status: {'Aktiv' if result.get('active') else 'Inaktiv'}")
            print("\nWebhook-URLs:")
            print(f"  KPIs:          {N8N_BASE_URL}/webhook/rms/kpis")
            print(f"  Reklamationen: {N8N_BASE_URL}/webhook/rms/reklamationen")
            print(f"  Detail:        {N8N_BASE_URL}/webhook/rms/reklamation/:id")
            print(f"  Charts:        {N8N_BASE_URL}/webhook/rms/charts")
        else:
            print("Deployment fehlgeschlagen!")
            print(f"Workflow manuell importieren: {export_path}")
    else:
        print("\nKein N8N_API_KEY - nur Export erstellt")
        print(f"Importiere manuell: {export_path}")

    print("\n" + "=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
