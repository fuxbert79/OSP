#!/usr/bin/env python3
"""
Fügt den Schriftverkehr-Node zum RMS-Email-Import-V2 Workflow hinzu.
Phase 5 der RMS-Implementation.
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
SCHRIFTVERKEHR_LIST_ID = "741c6ae8-88bb-406b-bf85-2e11192a528f"


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
    print("Phase 5: Schriftverkehr-Node hinzufügen")
    print("=" * 60)

    # Workflow laden
    print("\n1. Lade Workflow...")
    wf = get_workflow()
    print(f"   Workflow: {wf['name']}")
    print(f"   Nodes: {len(wf['nodes'])}")

    # Prüfen ob Node schon existiert
    existing_names = [n['name'] for n in wf['nodes']]
    if '16. Schriftverkehr erstellen' in existing_names:
        print("\n⚠️  Node '16. Schriftverkehr erstellen' existiert bereits!")
        return

    # Neuen Node erstellen
    print("\n2. Erstelle Schriftverkehr-Node...")

    schriftverkehr_node = {
        "parameters": {
            "method": "POST",
            "url": f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists/{SCHRIFTVERKEHR_LIST_ID}/items",
            "authentication": "predefinedCredentialType",
            "nodeCredentialType": "microsoftOAuth2Api",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": """={
  "fields": {
    "Title": "{{ $('4. E-Mail-Parser').item.json.subject ? $('4. E-Mail-Parser').item.json.subject.substring(0, 250) : 'Kein Betreff' }}",
    "QA_IDLookupId": {{ $('9. Reklamation erstellen').item.json.id || $('7a. Rekla suchen').item.json.value[0].id || 0 }},
    "Datum": "{{ $('4. E-Mail-Parser').item.json.receivedDateTime }}",
    "Typ": "E-Mail Eingang",
    "Absender": "{{ $('4. E-Mail-Parser').item.json.fromName }} ({{ $('4. E-Mail-Parser').item.json.from }})",
    "Betreff": "{{ $('4. E-Mail-Parser').item.json.subject }}",
    "Inhalt": "{{ $('4. E-Mail-Parser').item.json.bodyPreview ? $('4. E-Mail-Parser').item.json.bodyPreview.substring(0, 500) : '' }}",
    "Richtung": "Eingehend"
  }
}""",
            "options": {}
        },
        "id": "schriftverkehr-node-001",
        "name": "16. Schriftverkehr erstellen",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1328, 520],
        "credentials": {
            "microsoftOAuth2Api": {
                "id": CREDENTIAL_ID,
                "name": "Microsoft account"
            }
        }
    }

    # Node hinzufügen
    wf['nodes'].append(schriftverkehr_node)
    print(f"   ✅ Node erstellt: 16. Schriftverkehr erstellen")

    # Connection hinzufügen: 12. Ins Archiv → 16. Schriftverkehr erstellen (parallel zu 13)
    print("\n3. Erstelle Connection...")

    if "connections" not in wf:
        wf["connections"] = {}

    # 12. Ins Archiv hat bereits eine Connection zu 13. Anhänge laden
    # Wir fügen eine zweite parallele Connection hinzu
    if "12. Ins Archiv" in wf["connections"]:
        main_outputs = wf["connections"]["12. Ins Archiv"].get("main", [[]])
        # Füge zur ersten Output-Gruppe hinzu (parallel)
        if len(main_outputs) > 0:
            main_outputs[0].append({
                "node": "16. Schriftverkehr erstellen",
                "type": "main",
                "index": 0
            })
        wf["connections"]["12. Ins Archiv"]["main"] = main_outputs
    else:
        wf["connections"]["12. Ins Archiv"] = {
            "main": [[
                {"node": "16. Schriftverkehr erstellen", "type": "main", "index": 0}
            ]]
        }

    print(f"   ✅ Connection: 12. Ins Archiv → 16. Schriftverkehr erstellen")

    # Workflow speichern
    print("\n4. Speichere Workflow...")
    result = update_workflow(wf)
    print(f"   ✅ Workflow aktualisiert!")

    # Zusammenfassung
    print("\n" + "=" * 60)
    print("✅ PHASE 5 ABGESCHLOSSEN")
    print("=" * 60)
    print(f"""
Neuer Node: 16. Schriftverkehr erstellen
  - Position: Nach 12. Ins Archiv (parallel zu 13. Anhänge laden)
  - Funktion: Erstellt Eintrag in SharePoint-Liste 'RMS-Schriftverkehr'
  - Liste-ID: {SCHRIFTVERKEHR_LIST_ID}

Schriftverkehr-Felder:
  - Title: E-Mail Betreff (max 250 Zeichen)
  - QA_IDLookupId: SharePoint Item-ID der Reklamation
  - Datum: Empfangsdatum der E-Mail
  - Typ: "E-Mail Eingang"
  - Absender: Name + E-Mail
  - Betreff: Original-Betreff
  - Inhalt: Vorschau (max 500 Zeichen)
  - Richtung: "Eingehend"
""")


if __name__ == "__main__":
    main()
