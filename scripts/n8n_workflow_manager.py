#!/usr/bin/env python3
"""
n8n Workflow Manager für OSP
============================
Automatisiert Workflow-Bearbeitung über die n8n REST API.

Funktionen:
- Workflows abrufen und aktualisieren
- Credentials zu Nodes zuweisen
- Neue Nodes hinzufügen
- Workflow-Konfiguration ändern

Verwendung:
    python n8n_workflow_manager.py --help

Autor: AL (QM & KI-Manager)
Version: 1.0.0
Erstellt: 2026-01-27
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Optional
import urllib.request
import urllib.error


# =============================================================================
# KONFIGURATION
# =============================================================================

@dataclass
class N8nConfig:
    """n8n Server Konfiguration"""
    base_url: str = "https://n8n.schneider-kabelsatzbau.de"
    api_key: str = ""  # Wird aus Umgebungsvariable oder Parameter geladen
    
    @property
    def headers(self) -> dict:
        return {
            "X-N8N-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }


# =============================================================================
# API CLIENT
# =============================================================================

class N8nApiClient:
    """Client für n8n REST API"""
    
    def __init__(self, config: N8nConfig):
        self.config = config
        self._validate_config()
    
    def _validate_config(self):
        if not self.config.api_key:
            raise ValueError(
                "n8n API Key fehlt!\n"
                "Setze N8N_API_KEY Umgebungsvariable oder übergebe --api-key Parameter.\n"
                "API Key erstellen: n8n UI → Settings → API → Generate API Key"
            )
    
    def _request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        """HTTP Request an n8n API"""
        url = f"{self.config.base_url}/api/v1{endpoint}"
        
        req = urllib.request.Request(
            url,
            method=method,
            headers=self.config.headers
        )
        
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            raise RuntimeError(f"API Error {e.code}: {e.reason}\n{error_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Connection Error: {e.reason}")
    
    # -------------------------------------------------------------------------
    # WORKFLOWS
    # -------------------------------------------------------------------------
    
    def list_workflows(self, active_only: bool = False) -> list:
        """Liste alle Workflows"""
        result = self._request("GET", "/workflows")
        workflows = result.get("data", [])
        if active_only:
            workflows = [w for w in workflows if w.get("active")]
        return workflows
    
    def get_workflow(self, workflow_id: str) -> dict:
        """Hole Workflow Details"""
        return self._request("GET", f"/workflows/{workflow_id}")

    def create_workflow(self, workflow_data: dict) -> dict:
        """Erstelle neuen Workflow (POST)

        Pflichtfelder: name, nodes, connections
        """
        required_fields = {"name", "nodes", "connections"}
        for field in required_fields:
            if field not in workflow_data:
                raise ValueError(f"Pflichtfeld '{field}' fehlt")
        return self._request("POST", "/workflows", workflow_data)
    
    def update_workflow(self, workflow_id: str, workflow_data: dict) -> dict:
        """Aktualisiere Workflow (PUT - überschreibt komplett)

        n8n v2.x erlaubt nur bestimmte Felder im PUT-Request.
        Felder wie id, createdAt, updatedAt, active, versionId werden gefiltert.
        """
        # Nur erlaubte Felder für n8n v2.x API (strikt)
        # Siehe: https://docs.n8n.io/api/api-reference/#tag/Workflow/paths/~1workflows~1{id}/put
        # Pflicht: name, nodes, connections
        # Optional: settings, staticData (nur wenn nicht leer)
        allowed_fields = {"name", "nodes", "connections", "settings", "staticData"}

        # Erlaubte Settings-Felder (n8n v2.x Public API)
        allowed_settings_fields = {
            "executionOrder", "saveManualExecutions", "callerPolicy",
            "errorWorkflow", "timezone", "saveDataErrorExecution",
            "saveDataSuccessExecution", "saveExecutionProgress"
        }

        filtered_data = {}
        for k, v in workflow_data.items():
            if k not in allowed_fields or v is None:
                continue
            # Leere dicts/listen nicht mitschicken
            if isinstance(v, (dict, list)) and not v:
                continue
            # Settings filtern - nur erlaubte Felder
            if k == "settings" and isinstance(v, dict):
                v = {sk: sv for sk, sv in v.items() if sk in allowed_settings_fields}
                if not v:  # Wenn settings jetzt leer ist, nicht mitschicken
                    continue
            filtered_data[k] = v

        return self._request("PUT", f"/workflows/{workflow_id}", filtered_data)
    
    def activate_workflow(self, workflow_id: str) -> dict:
        """Aktiviere Workflow"""
        return self._request("POST", f"/workflows/{workflow_id}/activate")
    
    def deactivate_workflow(self, workflow_id: str) -> dict:
        """Deaktiviere Workflow"""
        return self._request("POST", f"/workflows/{workflow_id}/deactivate")
    
    # -------------------------------------------------------------------------
    # CREDENTIALS
    # -------------------------------------------------------------------------
    
    def list_credentials(self) -> list:
        """Liste alle Credentials"""
        result = self._request("GET", "/credentials")
        return result.get("data", [])
    
    def get_credential_by_name(self, name: str) -> Optional[dict]:
        """Finde Credential by Name"""
        credentials = self.list_credentials()
        for cred in credentials:
            if cred.get("name") == name:
                return cred
        return None
    
    def get_credential_by_type(self, cred_type: str) -> list:
        """Finde alle Credentials eines Typs"""
        credentials = self.list_credentials()
        return [c for c in credentials if c.get("type") == cred_type]


# =============================================================================
# WORKFLOW MODIFIER
# =============================================================================

class WorkflowModifier:
    """Modifiziert Workflow-Struktur"""
    
    def __init__(self, workflow: dict):
        self.workflow = workflow
        self.nodes = workflow.get("nodes", [])
        self.modified = False
    
    def find_node_by_name(self, name: str) -> Optional[dict]:
        """Finde Node by Name"""
        for node in self.nodes:
            if node.get("name") == name:
                return node
        return None
    
    def find_nodes_by_type(self, node_type: str) -> list:
        """Finde alle Nodes eines Typs"""
        return [n for n in self.nodes if n.get("type") == node_type]
    
    def set_node_credential(self, node_name: str, credential_id: str, credential_name: str, credential_type: str) -> bool:
        """Setze Credential für einen Node"""
        node = self.find_node_by_name(node_name)
        if not node:
            print(f"⚠️  Node '{node_name}' nicht gefunden")
            return False
        
        # Credentials-Struktur setzen
        if "credentials" not in node:
            node["credentials"] = {}
        
        node["credentials"][credential_type] = {
            "id": credential_id,
            "name": credential_name
        }
        
        self.modified = True
        print(f"✅ Credential '{credential_name}' → Node '{node_name}'")
        return True
    
    def set_node_parameter(self, node_name: str, param_path: str, value: Any) -> bool:
        """Setze Parameter für einen Node (unterstützt verschachtelte Pfade wie 'options.timeout')"""
        node = self.find_node_by_name(node_name)
        if not node:
            print(f"⚠️  Node '{node_name}' nicht gefunden")
            return False
        
        if "parameters" not in node:
            node["parameters"] = {}
        
        # Verschachtelte Pfade unterstützen
        parts = param_path.split(".")
        target = node["parameters"]
        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]
        
        target[parts[-1]] = value
        self.modified = True
        print(f"✅ Parameter '{param_path}' = '{value}' → Node '{node_name}'")
        return True
    
    def add_node(self, node_config: dict) -> bool:
        """Füge neuen Node hinzu"""
        # Prüfe ob Name bereits existiert
        if self.find_node_by_name(node_config.get("name", "")):
            print(f"⚠️  Node '{node_config.get('name')}' existiert bereits")
            return False
        
        self.nodes.append(node_config)
        self.modified = True
        print(f"✅ Node '{node_config.get('name')}' hinzugefügt")
        return True
    
    def add_connection(self, from_node: str, to_node: str, from_output: int = 0, to_input: int = 0) -> bool:
        """Füge Connection zwischen Nodes hinzu"""
        if "connections" not in self.workflow:
            self.workflow["connections"] = {}
        
        connections = self.workflow["connections"]
        
        if from_node not in connections:
            connections[from_node] = {"main": []}
        
        # Stelle sicher, dass genug Output-Slots existieren
        while len(connections[from_node]["main"]) <= from_output:
            connections[from_node]["main"].append([])
        
        # Füge Connection hinzu
        connections[from_node]["main"][from_output].append({
            "node": to_node,
            "type": "main",
            "index": to_input
        })
        
        self.modified = True
        print(f"✅ Connection: '{from_node}' → '{to_node}'")
        return True
    
    def get_workflow(self) -> dict:
        """Gib modifizierten Workflow zurück"""
        return self.workflow
    
    def print_nodes_summary(self):
        """Zeige Node-Übersicht"""
        print("\n📋 NODES IM WORKFLOW:")
        print("-" * 60)
        for node in self.nodes:
            creds = node.get("credentials", {})
            cred_str = ", ".join(creds.keys()) if creds else "keine"
            print(f"  • {node.get('name'):40} | Creds: {cred_str}")
        print("-" * 60)


# =============================================================================
# RMS-EMAIL-IMPORT-V2 SPEZIFISCH
# =============================================================================

def configure_rms_workflow(client: N8nApiClient, workflow_id: str, credential_id: str, credential_name: str):
    """
    Konfiguriere RMS-Email-Import-V2 Workflow
    - Setze Microsoft OAuth2 Credential für alle HTTP Request Nodes
    """
    print(f"\n🔧 Konfiguriere RMS-Email-Import-V2 (ID: {workflow_id})")
    print("=" * 60)
    
    # Workflow laden
    workflow = client.get_workflow(workflow_id)
    modifier = WorkflowModifier(workflow)
    
    # Übersicht anzeigen
    modifier.print_nodes_summary()
    
    # Nodes die Microsoft OAuth2 brauchen (inkl. Phase 2 Nodes)
    ms_oauth_nodes = [
        "2. E-Mails abrufen",
        "5a. In Junk verschieben",
        "7a. Rekla suchen",
        "7b. Config laden",
        "9. Reklamation erstellen",
        "10a. Config aktualisieren",
        "11. Als gelesen markieren",
        "12. Ins Archiv",
        # Phase 2 Nodes
        "13. Anhänge laden",
        "14. SharePoint Upload",
        "15. Teams Benachrichtigung"
    ]
    
    print(f"\n🔑 Setze Credential '{credential_name}' (ID: {credential_id})")
    print("-" * 60)
    
    for node_name in ms_oauth_nodes:
        modifier.set_node_credential(
            node_name=node_name,
            credential_id=credential_id,
            credential_name=credential_name,
            credential_type="microsoftOAuth2Api"
        )
    
    if modifier.modified:
        print(f"\n💾 Speichere Workflow...")
        updated = client.update_workflow(workflow_id, modifier.get_workflow())
        print(f"✅ Workflow aktualisiert!")
        return updated
    else:
        print("ℹ️  Keine Änderungen vorgenommen")
        return workflow


def add_phase2_nodes(client: N8nApiClient, workflow_id: str):
    """
    Füge Phase 2 Nodes zum RMS-Workflow hinzu:
    - E-Mail Anhänge extrahieren
    - SharePoint Upload
    - Teams Benachrichtigung
    """
    print(f"\n🚀 Füge Phase 2 Nodes hinzu (ID: {workflow_id})")
    print("=" * 60)
    
    workflow = client.get_workflow(workflow_id)
    modifier = WorkflowModifier(workflow)
    
    # Node: Anhänge extrahieren
    attachment_node = {
        "parameters": {
            "url": "=https://graph.microsoft.com/v1.0/users/reklamation@schneider-kabelsatzbau.de/messages/{{ $json.messageId }}/attachments",
            "authentication": "predefinedCredentialType",
            "nodeCredentialType": "microsoftOAuth2Api",
            "options": {}
        },
        "id": "attachment-node-001",
        "name": "13. Anhänge laden",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1328, 304]
    }
    
    # Node: SharePoint Upload
    sharepoint_node = {
        "parameters": {
            "method": "PUT",
            "url": "=https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com/drive/root:/Reklamationen/{{ $now.format('YYYY') }}/{{ $now.format('MM') }}/{{ $json.qaId }}/{{ $json.name }}:/content",
            "authentication": "predefinedCredentialType",
            "nodeCredentialType": "microsoftOAuth2Api",
            "sendBody": True,
            "contentType": "binaryData",
            "options": {}
        },
        "id": "sharepoint-node-001",
        "name": "14. SharePoint Upload",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1552, 304]
    }
    
    # Node: Teams Benachrichtigung
    teams_node = {
        "parameters": {
            "method": "POST",
            "url": "=https://graph.microsoft.com/v1.0/teams/{{ $env.TEAMS_QM_TEAM_ID }}/channels/{{ $env.TEAMS_QM_CHANNEL_ID }}/messages",
            "authentication": "predefinedCredentialType",
            "nodeCredentialType": "microsoftOAuth2Api",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": """={
  "body": {
    "contentType": "html",
    "content": "<b>🔔 Neue Reklamation:</b> {{ $json.qaId }}<br>Kunde: {{ $json.fromName }}<br>Betreff: {{ $json.subject }}"
  }
}""",
            "options": {}
        },
        "id": "teams-node-001",
        "name": "15. Teams Benachrichtigung",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1776, 304]
    }
    
    # Nodes hinzufügen
    modifier.add_node(attachment_node)
    modifier.add_node(sharepoint_node)
    modifier.add_node(teams_node)
    
    # Connections hinzufügen
    modifier.add_connection("12. Ins Archiv", "13. Anhänge laden")
    modifier.add_connection("13. Anhänge laden", "14. SharePoint Upload")
    modifier.add_connection("14. SharePoint Upload", "15. Teams Benachrichtigung")
    
    if modifier.modified:
        print(f"\n💾 Speichere Workflow...")
        updated = client.update_workflow(workflow_id, modifier.get_workflow())
        print(f"✅ Phase 2 Nodes hinzugefügt!")
        return updated
    
    return workflow


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="n8n Workflow Manager für OSP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Workflows auflisten
  python n8n_workflow_manager.py list
  
  # Credentials auflisten
  python n8n_workflow_manager.py credentials
  
  # Workflow Details anzeigen
  python n8n_workflow_manager.py show --id k3rVSLW6O00dtTBr
  
  # RMS-Workflow konfigurieren (Credentials setzen)
  python n8n_workflow_manager.py configure-rms --id k3rVSLW6O00dtTBr --cred-id YOUR_CRED_ID --cred-name "Microsoft OAuth2"
  
  # Phase 2 Nodes hinzufügen
  python n8n_workflow_manager.py add-phase2 --id k3rVSLW6O00dtTBr

Umgebungsvariablen:
  N8N_API_KEY     API Key für n8n (oder --api-key Parameter)
  N8N_BASE_URL    Base URL (default: https://n8n.schneider-kabelsatzbau.de)
"""
    )
    
    parser.add_argument(
        "command",
        choices=["list", "credentials", "show", "configure-rms", "add-phase2", "export", "backup"],
        help="Auszuführender Befehl"
    )
    parser.add_argument("--api-key", help="n8n API Key")
    parser.add_argument("--base-url", default="https://n8n.schneider-kabelsatzbau.de", help="n8n Base URL")
    parser.add_argument("--id", help="Workflow ID")
    parser.add_argument("--cred-id", help="Credential ID")
    parser.add_argument("--cred-name", help="Credential Name")
    parser.add_argument("--output", "-o", help="Output-Datei für Export")
    parser.add_argument("--active-only", action="store_true", help="Nur aktive Workflows")
    
    args = parser.parse_args()
    
    # Config erstellen
    config = N8nConfig(
        base_url=args.base_url or os.environ.get("N8N_BASE_URL", "https://n8n.schneider-kabelsatzbau.de"),
        api_key=args.api_key or os.environ.get("N8N_API_KEY", "")
    )
    
    try:
        client = N8nApiClient(config)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Commands
    if args.command == "list":
        workflows = client.list_workflows(active_only=args.active_only)
        print(f"\n📋 WORKFLOWS ({len(workflows)})")
        print("-" * 80)
        for wf in workflows:
            status = "🟢" if wf.get("active") else "⚪"
            print(f"{status} {wf.get('id'):20} | {wf.get('name'):40}")
        print("-" * 80)
    
    elif args.command == "credentials":
        credentials = client.list_credentials()
        print(f"\n🔑 CREDENTIALS ({len(credentials)})")
        print("-" * 80)
        for cred in credentials:
            print(f"  {cred.get('id'):10} | {cred.get('type'):30} | {cred.get('name')}")
        print("-" * 80)
    
    elif args.command == "show":
        if not args.id:
            print("❌ --id Parameter erforderlich")
            sys.exit(1)
        workflow = client.get_workflow(args.id)
        modifier = WorkflowModifier(workflow)
        print(f"\n📄 WORKFLOW: {workflow.get('name')}")
        print(f"   ID: {workflow.get('id')}")
        print(f"   Aktiv: {'Ja' if workflow.get('active') else 'Nein'}")
        modifier.print_nodes_summary()
    
    elif args.command == "configure-rms":
        if not args.id:
            print("❌ --id Parameter erforderlich")
            sys.exit(1)
        if not args.cred_id or not args.cred_name:
            print("❌ --cred-id und --cred-name Parameter erforderlich")
            print("\nVerfügbare Credentials:")
            credentials = client.list_credentials()
            for cred in credentials:
                if "microsoft" in cred.get("type", "").lower():
                    print(f"  ID: {cred.get('id')} | Name: {cred.get('name')} | Type: {cred.get('type')}")
            sys.exit(1)
        configure_rms_workflow(client, args.id, args.cred_id, args.cred_name)
    
    elif args.command == "add-phase2":
        if not args.id:
            print("❌ --id Parameter erforderlich")
            sys.exit(1)
        add_phase2_nodes(client, args.id)
    
    elif args.command == "export":
        if not args.id:
            print("❌ --id Parameter erforderlich")
            sys.exit(1)
        workflow = client.get_workflow(args.id)
        output_file = args.output or f"workflow_{args.id}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        print(f"✅ Exportiert nach: {output_file}")
    
    elif args.command == "backup":
        workflows = client.list_workflows()
        backup_dir = args.output or "n8n_backup"
        os.makedirs(backup_dir, exist_ok=True)
        for wf in workflows:
            full_wf = client.get_workflow(wf.get("id"))
            filename = f"{backup_dir}/{wf.get('id')}_{wf.get('name').replace(' ', '_').replace('/', '_')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(full_wf, f, indent=2, ensure_ascii=False)
            print(f"✅ {filename}")
        print(f"\n✅ Backup abgeschlossen: {len(workflows)} Workflows → {backup_dir}/")


if __name__ == "__main__":
    main()
