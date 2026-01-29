# Claude Code Prompt: RMS Stammdaten Integration

**Datum:** 2026-01-29  
**Ausführung:** Direkt auf Hetzner Server (46.224.102.30)  
**Ziel:** SharePoint-Liste aus CSV erstellen + n8n Workflow + Frontend Autocomplete

---

## 🔧 SERVER-ZUGANG

```bash
# Server
IP: 46.224.102.30
User: root

# n8n API
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMmFlMi1mNzQyLTQxZGUtYTY1OS0xNTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5NTM4MTcwLCJleHAiOjE3NzcyNDA4MDB9.NsECcQH9N-UsiCmXrZkMGLg6ioFbGCuNXWW_XaJAUTY"
export N8N_BASE_URL="http://127.0.0.1:5678"

# Pfade
CSV_FILE="/mnt/HC_Volume_104189729/osp/rms/stammdaten.csv"
FRONTEND="/var/www/html/rms/"
```

---

## 📋 SHAREPOINT REFERENZ

```bash
# Site-ID (RMS)
SITE_ID="rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"

# n8n Credential für Microsoft OAuth2
CREDENTIAL_ID="Fm3IuAbVYBYDIA4U"

# Graph API Base URL
GRAPH_API="https://graph.microsoft.com/v1.0/sites/${SITE_ID}"
```

---

## 🎯 AUFGABEN

### AUFGABE 1: CSV analysieren und bereinigen

**Datei:** `/mnt/HC_Volume_104189729/osp/rms/stammdaten.csv`

**CSV-Struktur:**
```
Name;PLZ;Ort;Adresse;Deb./Kred.-Nr;Typ;Land
```

**Probleme zu beheben:**
1. Mehrzeilige Namen (in Anführungszeichen)
2. BOM am Dateianfang entfernen
3. Leere Felder behandeln

**Python-Script erstellen:** `/opt/osp/scripts/parse_stammdaten.py`

```python
#!/usr/bin/env python3
"""
Parst die Stammdaten CSV und gibt JSON aus
"""
import csv
import json
import sys
from pathlib import Path

def parse_stammdaten(csv_path: str) -> list:
    """Parst die CSV-Datei und gibt eine Liste von Dictionaries zurück"""
    
    stammdaten = []
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        # Semikolon als Delimiter
        reader = csv.DictReader(f, delimiter=';')
        
        for row in reader:
            # Mehrzeilige Namen bereinigen (Zeilenumbrüche durch Leerzeichen ersetzen)
            name = row.get('Name', '').replace('\n', ' ').replace('\r', '').strip()
            
            # Leere Namen überspringen
            if not name:
                continue
            
            stammdaten.append({
                'Title': name,
                'PLZ': row.get('PLZ', '').strip(),
                'Ort': row.get('Ort', '').strip(),
                'Adresse': row.get('Adresse', '').replace('\n', ', ').strip(),
                'DebKredNr': row.get('Deb./Kred.-Nr', '').strip(),
                'StammdatenTyp': row.get('Typ', '').strip(),
                'Land': row.get('Land', '').strip() or 'Deutschland'
            })
    
    return stammdaten

def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else '/mnt/HC_Volume_104189729/osp/rms/stammdaten.csv'
    
    stammdaten = parse_stammdaten(csv_path)
    
    print(f"Parsed {len(stammdaten)} Einträge", file=sys.stderr)
    
    # Statistik
    kunden = len([s for s in stammdaten if s['StammdatenTyp'] == 'Kunde'])
    lieferanten = len([s for s in stammdaten if s['StammdatenTyp'] == 'Lieferant'])
    print(f"  - Kunden: {kunden}", file=sys.stderr)
    print(f"  - Lieferanten: {lieferanten}", file=sys.stderr)
    
    # JSON ausgeben
    print(json.dumps(stammdaten, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

**Ausführbar machen und testen:**
```bash
chmod +x /opt/osp/scripts/parse_stammdaten.py
python3 /opt/osp/scripts/parse_stammdaten.py "$CSV_FILE" > /tmp/stammdaten.json
head -50 /tmp/stammdaten.json
```

---

### AUFGABE 2: SharePoint-Liste erstellen via Graph API

**Erstelle ein Python-Script:** `/opt/osp/scripts/create_stammdaten_list.py`

```python
#!/usr/bin/env python3
"""
Erstellt die RMS-Stammdaten Liste in SharePoint via Graph API
Benötigt: Microsoft OAuth2 Token mit Sites.Manage.All
"""
import requests
import json
import sys
import os

# Konfiguration
SITE_ID = "rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"
GRAPH_API = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}"

def get_access_token():
    """
    Holt Access Token - MUSS MANUELL GESETZT WERDEN
    Alternativ: n8n Workflow nutzen
    """
    # Token aus Umgebungsvariable oder Datei
    token = os.environ.get('GRAPH_TOKEN')
    if not token:
        token_file = '/tmp/graph_token.txt'
        if os.path.exists(token_file):
            with open(token_file) as f:
                token = f.read().strip()
    return token

def create_list(token: str) -> dict:
    """Erstellt die SharePoint-Liste"""
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Liste definieren
    list_definition = {
        "displayName": "RMS-Stammdaten",
        "description": "Kunden- und Lieferantenstammdaten für RMS",
        "columns": [
            {
                "name": "PLZ",
                "text": {
                    "allowMultipleLines": False,
                    "maxLength": 20
                }
            },
            {
                "name": "Ort",
                "text": {
                    "allowMultipleLines": False,
                    "maxLength": 100
                }
            },
            {
                "name": "Adresse",
                "text": {
                    "allowMultipleLines": True
                }
            },
            {
                "name": "DebKredNr",
                "text": {
                    "allowMultipleLines": False,
                    "maxLength": 20
                }
            },
            {
                "name": "StammdatenTyp",
                "choice": {
                    "allowTextEntry": False,
                    "choices": ["Kunde", "Lieferant"],
                    "displayAs": "dropDownMenu"
                }
            },
            {
                "name": "Land",
                "text": {
                    "allowMultipleLines": False,
                    "maxLength": 100
                }
            }
        ],
        "list": {
            "template": "genericList"
        }
    }
    
    # Liste erstellen
    response = requests.post(
        f"{GRAPH_API}/lists",
        headers=headers,
        json=list_definition
    )
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Liste erstellt: {result['id']}")
        return result
    else:
        print(f"❌ Fehler: {response.status_code}")
        print(response.text)
        return None

def main():
    token = get_access_token()
    if not token:
        print("❌ Kein Access Token gefunden!")
        print("Setze GRAPH_TOKEN Umgebungsvariable oder erstelle /tmp/graph_token.txt")
        sys.exit(1)
    
    result = create_list(token)
    if result:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

**WICHTIG:** Da wir keinen direkten Graph API Token haben, nutzen wir stattdessen n8n!

---

### AUFGABE 3: n8n Workflow für SharePoint-Liste erstellen

**Erstelle Workflow:** `RMS-Create-Stammdaten-List`

Da die Graph API Authentifizierung über n8n läuft, erstellen wir einen Workflow:

**Workflow-Struktur:**
```
[Manual Trigger] → [HTTP Request: Create List] → [Response]
```

**HTTP Request Node - Create List:**
```
Method: POST
URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/lists
Authentication: OAuth2
Credential: Microsoft account (Fm3IuAbVYBYDIA4U)
Body (JSON):
```

```json
{
  "displayName": "RMS-Stammdaten",
  "description": "Kunden- und Lieferantenstammdaten für RMS",
  "columns": [
    {
      "name": "PLZ",
      "text": { "allowMultipleLines": false, "maxLength": 20 }
    },
    {
      "name": "Ort",
      "text": { "allowMultipleLines": false, "maxLength": 100 }
    },
    {
      "name": "Adresse",
      "text": { "allowMultipleLines": true }
    },
    {
      "name": "DebKredNr",
      "text": { "allowMultipleLines": false, "maxLength": 20 }
    },
    {
      "name": "StammdatenTyp",
      "choice": {
        "allowTextEntry": false,
        "choices": ["Kunde", "Lieferant"],
        "displayAs": "dropDownMenu"
      }
    },
    {
      "name": "Land",
      "text": { "allowMultipleLines": false, "maxLength": 100 }
    }
  ],
  "list": {
    "template": "genericList"
  }
}
```

**Nach Ausführung:** Liste-ID notieren für nächsten Schritt!

---

### AUFGABE 4: CSV-Daten in SharePoint importieren

**n8n Workflow:** `RMS-Import-Stammdaten`

**Workflow-Struktur:**
```
[Manual Trigger] → [Read JSON File] → [Split In Batches (50)] → [HTTP Request: Create Item] → [Wait 1s]
```

**Node 1: Read JSON File (Code Node)**
```javascript
const fs = require('fs');
const data = fs.readFileSync('/tmp/stammdaten.json', 'utf8');
const stammdaten = JSON.parse(data);

// In Batches aufteilen für bessere Performance
return stammdaten.map(item => ({ json: item }));
```

**Node 2: Split In Batches**
- Batch Size: 50
- (Verhindert Rate Limiting)

**Node 3: HTTP Request - Create Item**
```
Method: POST
URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/lists/{{LISTE_ID}}/items
Authentication: OAuth2
Credential: Microsoft account
Body (JSON):
```
```json
{
  "fields": {
    "Title": "{{ $json.Title }}",
    "PLZ": "{{ $json.PLZ }}",
    "Ort": "{{ $json.Ort }}",
    "Adresse": "{{ $json.Adresse }}",
    "DebKredNr": "{{ $json.DebKredNr }}",
    "StammdatenTyp": "{{ $json.StammdatenTyp }}",
    "Land": "{{ $json.Land }}"
  }
}
```

**Node 4: Wait**
- Wait: 1 Second (Rate Limiting vermeiden)

---

### AUFGABE 5: n8n Workflow für Stammdaten-Abfrage

**Workflow:** `RMS-Stammdaten-API`

**Webhook:** GET `/webhook/rms-stammdaten`

**Parameter:**
- `typ` - Optional: "Kunde" oder "Lieferant"
- `search` - Optional: Suchbegriff

**Workflow-Struktur:**
```
[Webhook] → [Build Query] → [HTTP Request: Get Items] → [Transform] → [Respond]
```

**Node 2: Build Query (Code Node)**
```javascript
const typ = $json.query?.typ || '';
const search = $json.query?.search || '';

let filter = '';
const filters = [];

if (typ) {
  filters.push(`fields/StammdatenTyp eq '${typ}'`);
}

if (search) {
  // OData substringof für Suche
  filters.push(`(substringof('${search}', fields/Title) or substringof('${search}', fields/DebKredNr))`);
}

if (filters.length > 0) {
  filter = '&$filter=' + filters.join(' and ');
}

return {
  filter: filter,
  top: 100
};
```

**Node 3: HTTP Request**
```
Method: GET
URL: https://graph.microsoft.com/v1.0/sites/{{SITE_ID}}/lists/{{STAMMDATEN_LIST_ID}}/items?$expand=fields&$top={{ $json.top }}{{ $json.filter }}
Authentication: OAuth2
Credential: Microsoft account
Headers:
  Prefer: HonorNonIndexedQueriesWarningMayFailRandomly
```

**Node 4: Transform (Code Node)**
```javascript
const items = $input.first().json.value || [];

const stammdaten = items.map(item => ({
  id: item.id,
  name: item.fields.Title,
  plz: item.fields.PLZ || '',
  ort: item.fields.Ort || '',
  adresse: item.fields.Adresse || '',
  debKredNr: item.fields.DebKredNr || '',
  typ: item.fields.StammdatenTyp || '',
  land: item.fields.Land || ''
}));

return {
  stammdaten: stammdaten,
  count: stammdaten.length
};
```

**Node 5: Respond to Webhook**

---

### AUFGABE 6: Nginx Route hinzufügen

**Datei:** `/etc/nginx/sites-available/osp`

```nginx
# === RMS Stammdaten API (2026-01-29) ===
location = /api/rms/stammdaten {
    proxy_pass http://127.0.0.1:5678/webhook/rms-stammdaten;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}
```

```bash
nginx -t && systemctl reload nginx
```

---

### AUFGABE 7: Frontend Autocomplete implementieren

**Datei:** `/var/www/html/rms/js/app.js`

**Neue Funktionen hinzufügen:**

```javascript
// ============================================
// STAMMDATEN AUTOCOMPLETE
// ============================================

let stammdatenCache = { kunden: [], lieferanten: [] };

async function loadStammdaten(typ = '') {
    try {
        const url = typ ? `/api/rms/stammdaten?typ=${typ}` : '/api/rms/stammdaten';
        const response = await fetch(url);
        if (!response.ok) throw new Error('Stammdaten API nicht verfügbar');
        
        const data = await response.json();
        
        if (typ === 'Kunde') {
            stammdatenCache.kunden = data.stammdaten;
        } else if (typ === 'Lieferant') {
            stammdatenCache.lieferanten = data.stammdaten;
        } else {
            // Alle laden und cachen
            stammdatenCache.kunden = data.stammdaten.filter(s => s.typ === 'Kunde');
            stammdatenCache.lieferanten = data.stammdaten.filter(s => s.typ === 'Lieferant');
        }
        
        console.log(`Stammdaten geladen: ${data.count} Einträge`);
        return data.stammdaten;
    } catch (error) {
        console.error('Stammdaten laden fehlgeschlagen:', error);
        return [];
    }
}

function setupStammdatenAutocomplete(inputId, listId, typ) {
    const input = document.getElementById(inputId);
    const datalist = document.getElementById(listId);
    
    if (!input || !datalist) return;
    
    // Datalist mit Stammdaten befüllen
    const stammdaten = typ === 'Kunde' ? stammdatenCache.kunden : stammdatenCache.lieferanten;
    
    datalist.innerHTML = stammdaten.map(s => 
        `<option value="${s.name}" data-id="${s.id}" data-debkred="${s.debKredNr}">${s.name} (${s.debKredNr})</option>`
    ).join('');
    
    // Bei Auswahl zusätzliche Daten setzen
    input.addEventListener('change', (e) => {
        const selected = stammdaten.find(s => s.name === e.target.value);
        if (selected) {
            // Optional: Versteckte Felder mit ID/DebKredNr füllen
            const hiddenId = document.getElementById(inputId + '-id');
            const hiddenNr = document.getElementById(inputId + '-nr');
            if (hiddenId) hiddenId.value = selected.id;
            if (hiddenNr) hiddenNr.value = selected.debKredNr;
        }
    });
}

// Beim Laden der Seite Stammdaten cachen
document.addEventListener('DOMContentLoaded', async () => {
    // ... bestehender Code ...
    
    // Stammdaten laden
    await loadStammdaten();
});
```

**HTML für Autocomplete (im Detail-Modal oder Erfassungs-Formular):**

```html
<!-- Absender/Lieferant Feld mit Autocomplete -->
<div class="form-group">
    <label for="edit-absender">Absender (Kunde/Lieferant)</label>
    <input type="text" id="edit-absender" class="form-control" list="absender-datalist" placeholder="Name eingeben...">
    <datalist id="absender-datalist"></datalist>
    <input type="hidden" id="edit-absender-id">
    <input type="hidden" id="edit-absender-nr">
</div>
```

---

## ✅ CHECKLISTE

### Phase 1: Vorbereitung
- [ ] CSV analysiert und geparst
- [ ] `/tmp/stammdaten.json` erstellt
- [ ] Anzahl Einträge geprüft (~1.297)

### Phase 2: SharePoint-Liste
- [ ] n8n Workflow "RMS-Create-Stammdaten-List" erstellt
- [ ] Workflow ausgeführt - Liste erstellt
- [ ] Liste-ID notiert: `_______________`

### Phase 3: Daten-Import
- [ ] n8n Workflow "RMS-Import-Stammdaten" erstellt
- [ ] Liste-ID im Workflow eingetragen
- [ ] Import gestartet
- [ ] Alle ~1.297 Einträge importiert

### Phase 4: API
- [ ] n8n Workflow "RMS-Stammdaten-API" erstellt
- [ ] Nginx Route hinzugefügt
- [ ] API-Test: `curl https://osp.schneider-kabelsatzbau.de/api/rms/stammdaten?typ=Kunde`

### Phase 5: Frontend
- [ ] Autocomplete-Funktionen in app.js
- [ ] Datalist im HTML
- [ ] Browser-Test

---

## 📝 REPORT

Nach Abschluss Report erstellen:
`/mnt/HC_Volume_104189729/osp/rms/docs/RMS_Stammdaten_Integration_Report_2026-01-29.md`

---

## ⚠️ WICHTIGE HINWEISE

1. **Rate Limiting:** Graph API hat Limits - daher Batches mit Wartezeit
2. **Import dauert:** ~1.300 Einträge × 1s = ~22 Minuten
3. **Liste-ID:** Nach Erstellung der Liste die ID notieren und in Import-Workflow eintragen
4. **Backup:** Vor Änderungen Frontend-Backup erstellen

```bash
cp -r /var/www/html/rms/ /var/www/html/rms_backup_$(date +%Y%m%d_%H%M%S)/
```

---

*Erstellt: 2026-01-29*
