#!/usr/bin/env python3
"""
Fuegt PDF-Generierungs-Nodes zum RMS-Email-Import-V2 Workflow hinzu.
Phase 3 der RMS-Implementation.

Nodes:
  - 17. PDF generieren (POST zu localhost:5001/generate-pdf)
  - 18. PDF nach SharePoint (Upload via Graph API)
"""

import json
import os
import urllib.request
import urllib.error

API_KEY = os.environ.get("N8N_API_KEY")
BASE_URL = "http://127.0.0.1:5678/api/v1"
WORKFLOW_ID = "k3rVSLW6O00dtTBr"
CREDENTIAL_ID = "Fm3IuAbVYBYDIA4U"

# SharePoint IDs
SITE_ID = "rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"


def get_workflow():
    """Lade Workflow"""
    req = urllib.request.Request(
        f"{BASE_URL}/workflows/{WORKFLOW_ID}",
        headers={"X-N8N-API-KEY": API_KEY}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def update_workflow(workflow_data):
    """Update Workflow (nur erlaubte Felder)"""
    allowed_fields = {"name", "nodes", "connections", "settings", "staticData"}
    allowed_settings = {
        "executionOrder", "saveManualExecutions", "callerPolicy",
        "errorWorkflow", "timezone", "saveDataErrorExecution",
        "saveDataSuccessExecution", "saveExecutionProgress"
    }

    filtered = {}
    for k, v in workflow_data.items():
        if k not in allowed_fields or v is None:
            continue
        if isinstance(v, (dict, list)) and not v:
            continue
        if k == "settings" and isinstance(v, dict):
            v = {sk: sv for sk, sv in v.items() if sk in allowed_settings}
            if not v:
                continue
        filtered[k] = v

    req = urllib.request.Request(
        f"{BASE_URL}/workflows/{WORKFLOW_ID}",
        data=json.dumps(filtered).encode('utf-8'),
        headers={
            "X-N8N-API-KEY": API_KEY,
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main():
    print("=" * 60)
    print("Phase 3: PDF-Nodes hinzufuegen")
    print("=" * 60)

    # Workflow laden
    print("\n1. Lade Workflow...")
    wf = get_workflow()
    print(f"   Workflow: {wf['name']}")
    print(f"   Nodes: {len(wf['nodes'])}")

    # Pruefen ob Nodes schon existieren
    existing_names = [n['name'] for n in wf['nodes']]
    if '17. PDF generieren' in existing_names:
        print("\n Node '17. PDF generieren' existiert bereits!")
        return
    if '18. PDF vorbereiten' in existing_names:
        print("\n Node '18. PDF vorbereiten' existiert bereits!")
        return
    if '19. PDF nach SharePoint' in existing_names:
        print("\n Node '19. PDF nach SharePoint' existiert bereits!")
        return

    # Finde Position von Node 9 (Reklamation erstellen)
    node_9_pos = [224, 304]
    for node in wf['nodes']:
        if node['name'] == '9. Reklamation erstellen':
            node_9_pos = node.get('position', [224, 304])
            break

    # PDF generieren Node - wird nach 9. Reklamation erstellen eingefuegt
    # Position: unterhalb von 9, vor den Archiv-Nodes
    print("\n2. Erstelle PDF-Nodes...")

    pdf_generate_node = {
        "parameters": {
            "method": "POST",
            "url": "http://localhost:5001/generate-pdf",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": """={
  "abweichungs_nr": "{{ $('8b. QA-ID generieren').item.json.newQaId || $('8a-FALSE. Alte QA-ID').item.json.existingQaId || 'QA-XXXX-XXX' }}",
  "datum": "{{ new Date().toISOString().split('T')[0] }}",
  "lieferant_firma": "{{ $('4. E-Mail-Parser').item.json.fromName || 'Unbekannt' }}",
  "lieferant_ansprechpartner": "",
  "lieferant_email": "{{ $('4. E-Mail-Parser').item.json.from }}",
  "artikel_nr_schneider": "",
  "artikel_bezeichnung": "{{ $('4. E-Mail-Parser').item.json.subject }}",
  "lieferschein_nr": "",
  "lieferdatum": "",
  "liefermenge": "",
  "beanstandungsmenge": "",
  "beschreibung": "{{ $('4. E-Mail-Parser').item.json.bodyPreview || 'Aus E-Mail importiert. Details siehe Anhang.' }}",
  "massnahmen": ["untersuchung_abstellen"],
  "ersteller": "System",
  "return_base64": true
}""",
            "options": {
                "response": {
                    "response": {
                        "responseFormat": "json"
                    }
                }
            }
        },
        "id": "pdf-generate-node-001",
        "name": "17. PDF generieren",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [448, 520],
        "onError": "continueErrorOutput"
    }

    # Code Node zum Base64-Decodieren
    pdf_decode_node = {
        "parameters": {
            "mode": "runOnceForEachItem",
            "jsCode": """// Decode Base64 PDF content and prepare for upload
const item = $input.item.json;

if (!item.success || !item.content_base64) {
  return { error: 'PDF-Generierung fehlgeschlagen', details: item };
}

// Return binary data for next node
const binaryData = Buffer.from(item.content_base64, 'base64');

return {
  filename: item.filename,
  filepath: item.filepath,
  binaryData: item.content_base64,
  contentLength: binaryData.length
};"""
        },
        "id": "pdf-decode-node-001",
        "name": "18. PDF vorbereiten",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [672, 520]
    }

    # PDF nach SharePoint Upload Node (mit Base64 direkt im Body)
    pdf_upload_node = {
        "parameters": {
            "method": "PUT",
            "url": f"=https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drive/root:/Reklamationen/{{{{ new Date().getFullYear() }}}}/{{{{ String(new Date().getMonth() + 1).padStart(2, '0') }}}}/{{{{ $('8b. QA-ID generieren').item.json.newQaId || $('8a-FALSE. Alte QA-ID').item.json.existingQaId || 'UNKNOWN' }}}}/Dokumente/{{{{ $json.filename }}}}:/content",
            "authentication": "predefinedCredentialType",
            "nodeCredentialType": "microsoftOAuth2Api",
            "sendBody": True,
            "contentType": "raw",
            "rawContentType": "application/pdf",
            "body": "={{ Buffer.from($json.binaryData, 'base64') }}",
            "options": {}
        },
        "id": "pdf-upload-node-001",
        "name": "19. PDF nach SharePoint",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [896, 520],
        "credentials": {
            "microsoftOAuth2Api": {
                "id": CREDENTIAL_ID,
                "name": "Microsoft account"
            }
        },
        "onError": "continueErrorOutput"
    }

    # Nodes hinzufuegen
    wf['nodes'].append(pdf_generate_node)
    wf['nodes'].append(pdf_decode_node)
    wf['nodes'].append(pdf_upload_node)
    print(f"   Node erstellt: 17. PDF generieren")
    print(f"   Node erstellt: 18. PDF vorbereiten")
    print(f"   Node erstellt: 19. PDF nach SharePoint")

    # Connections hinzufuegen
    print("\n3. Erstelle Connections...")

    if "connections" not in wf:
        wf["connections"] = {}

    # 9. Reklamation erstellen -> 17. PDF generieren (parallel zu 10. Config updaten?)
    # Wir fuegen eine Connection von 9 zu 17 hinzu
    if "9. Reklamation erstellen" in wf["connections"]:
        main_outputs = wf["connections"]["9. Reklamation erstellen"].get("main", [[]])
        if len(main_outputs) > 0:
            main_outputs[0].append({
                "node": "17. PDF generieren",
                "type": "main",
                "index": 0
            })
        wf["connections"]["9. Reklamation erstellen"]["main"] = main_outputs
    else:
        wf["connections"]["9. Reklamation erstellen"] = {
            "main": [[{"node": "17. PDF generieren", "type": "main", "index": 0}]]
        }

    # 17. PDF generieren -> 18. PDF vorbereiten -> 19. PDF nach SharePoint
    wf["connections"]["17. PDF generieren"] = {
        "main": [[{"node": "18. PDF vorbereiten", "type": "main", "index": 0}]]
    }
    wf["connections"]["18. PDF vorbereiten"] = {
        "main": [[{"node": "19. PDF nach SharePoint", "type": "main", "index": 0}]]
    }

    print(f"   Connection: 9. Reklamation erstellen -> 17. PDF generieren")
    print(f"   Connection: 17. PDF generieren -> 18. PDF vorbereiten")
    print(f"   Connection: 18. PDF vorbereiten -> 19. PDF nach SharePoint")

    # Workflow speichern
    print("\n4. Speichere Workflow...")
    result = update_workflow(wf)
    print(f"   Workflow aktualisiert!")

    # Zusammenfassung
    print("\n" + "=" * 60)
    print("PHASE 3 NODES ABGESCHLOSSEN")
    print("=" * 60)
    print(f"""
Neue Nodes:
  - 17. PDF generieren
    Position: Nach 9. Reklamation erstellen (parallel)
    Funktion: Ruft PDF-Generator auf localhost:5001 auf
    Gibt Base64-codierten PDF-Inhalt zurueck

  - 18. PDF vorbereiten
    Position: Nach 17. PDF generieren
    Funktion: Bereitet PDF-Daten fuer Upload vor

  - 19. PDF nach SharePoint
    Position: Nach 18. PDF vorbereiten
    Funktion: Laedt PDF nach SharePoint hoch
    Pfad: /Reklamationen/{{Jahr}}/{{Monat}}/{{QA-ID}}/Dokumente/{{Dateiname}}
""")


if __name__ == "__main__":
    main()
