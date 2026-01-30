# Claude Code Prompt: RMS Phase 1.1 - M365-Benutzer & PDF-Fix

**Datum:** 2026-01-29  
**Ausführung:** Direkt auf Hetzner Server (46.224.102.30)  
**Priorität:** KRITISCH - Beide Probleme blockieren produktiven Einsatz

---

## 🎯 ZIELE

1. **M365-Benutzer aus Graph API laden** - KEINE hardcodierten Namen mehr
2. **PDF-Generierung fixen** - Dateien sind aktuell korrupt/leer
3. **Alle Änderungen durch Tests verifizieren**
4. **Abschließenden Report erstellen**

---

## 🔧 SERVER-ZUGANG

```bash
# Server
IP: 46.224.102.30
User: root

# n8n API
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMGFkYS1mMGU5NTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM4MDQxNDQxfQ.Hhqnbitgd-ak_iZruZy1Z_rdHJ75BtcYfv09RO05Rtg"
export N8N_BASE_URL="http://127.0.0.1:5678"

# Pfade
FRONTEND="/var/www/html/rms/"
SCRIPTS="/opt/osp/scripts/"
```

---

## 📋 SHAREPOINT & GRAPH API REFERENZ

```bash
# Site-ID
SITE_ID="rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"

# n8n Credential für Microsoft OAuth2
CREDENTIAL_ID="Fm3IuAbVYBYDIA4U"

# Graph API Endpoints
# Benutzer: https://graph.microsoft.com/v1.0/users
# Benutzer mit Filter: https://graph.microsoft.com/v1.0/users?$filter=accountEnabled eq true&$select=id,displayName,mail,jobTitle,department
```

---

## AUFGABE 1: M365-Benutzer Integration

### 1.1 Neuen n8n Workflow erstellen: RMS-Users-API

**Zweck:** Lädt alle aktiven M365-Benutzer aus Graph API

**Workflow erstellen:**

```
Name: RMS-Users-API
Webhook: GET /webhook/rms-users
```

**Node 1: Webhook Trigger**
```json
{
  "httpMethod": "GET",
  "path": "rms-users",
  "responseMode": "responseNode"
}
```

**Node 2: Get M365 Users (HTTP Request)**
```
Method: GET
URL: https://graph.microsoft.com/v1.0/users?$filter=accountEnabled eq true&$select=id,displayName,mail,jobTitle,department&$top=100
Authentication: OAuth2
Credential: Microsoft account (Fm3IuAbVYBYDIA4U)
```

**Node 3: Transform Users (Code Node)**
```javascript
const users = $input.item.json.value || [];

// Benutzer transformieren für Frontend
const transformedUsers = users
  .filter(u => u.mail) // Nur Benutzer mit E-Mail
  .map(u => ({
    id: u.id,
    displayName: u.displayName || 'Unbekannt',
    mail: u.mail,
    jobTitle: u.jobTitle || '',
    department: u.department || '',
    // Kürzel aus E-Mail extrahieren (vor dem @)
    kuerzel: u.mail.split('@')[0].substring(0, 2).toUpperCase()
  }))
  .sort((a, b) => a.displayName.localeCompare(b.displayName));

return { users: transformedUsers };
```

**Node 4: Respond to Webhook**
```json
{
  "respondWith": "json",
  "responseBody": "={{ $json }}"
}
```

**Workflow aktivieren!**

### 1.2 Nginx Route hinzufügen

```bash
# In /etc/nginx/sites-available/osp hinzufügen:

location = /api/rms/users {
    proxy_pass http://127.0.0.1:5678/webhook/rms-users;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

```bash
# Syntax prüfen und neu laden
nginx -t && systemctl reload nginx
```

### 1.3 Frontend anpassen: M365-Benutzer laden

**Datei:** `/var/www/html/rms/js/app.js`

**ENTFERNE die hardcodierte VERANTWORTLICHE-Liste komplett!**

**ERSETZE durch dynamisches Laden:**

```javascript
// ============================================
// M365 BENUTZER
// ============================================

let m365Users = [];

async function loadM365Users() {
    try {
        const response = await fetch('/api/rms/users');
        if (!response.ok) {
            console.error('Fehler beim Laden der M365-Benutzer:', response.status);
            return [];
        }
        const data = await response.json();
        m365Users = data.users || [];
        console.log(`${m365Users.length} M365-Benutzer geladen`);
        return m365Users;
    } catch (error) {
        console.error('M365-Benutzer laden fehlgeschlagen:', error);
        return [];
    }
}

function populateUserDropdown(selectElementId, selectedValue = '') {
    const select = document.getElementById(selectElementId);
    if (!select) return;
    
    // Bestehende Optionen löschen (außer Platzhalter)
    select.innerHTML = '<option value="">-- Auswählen --</option>';
    
    // M365-Benutzer als Optionen hinzufügen
    m365Users.forEach(user => {
        const option = document.createElement('option');
        option.value = user.mail; // E-Mail als Wert für Benachrichtigungen
        option.textContent = `${user.displayName}${user.jobTitle ? ' (' + user.jobTitle + ')' : ''}`;
        option.dataset.id = user.id;
        option.dataset.displayName = user.displayName;
        option.dataset.mail = user.mail;
        
        if (selectedValue && (selectedValue === user.mail || selectedValue === user.displayName)) {
            option.selected = true;
        }
        
        select.appendChild(option);
    });
}

// Beim Laden der Seite M365-Benutzer abrufen
document.addEventListener('DOMContentLoaded', async function() {
    // M365-Benutzer laden BEVOR andere Initialisierung
    await loadM365Users();
    
    // ... restliche Initialisierung ...
});
```

### 1.4 Dropdowns aktualisieren

**In der Funktion `showDetail()` - Verantwortlich-Dropdown befüllen:**

```javascript
async function showDetail(id) {
    // ... bestehender Code ...
    
    // Nach dem Laden der Daten: Dropdown befüllen
    populateUserDropdown('edit-verantwortlich', data.reklamation?.Verantwortlich || '');
    
    // ... restlicher Code ...
}
```

**In der Funktion `showAddMassnahmeModal()` - Verantwortlich-Dropdown befüllen:**

```javascript
function showAddMassnahmeModal() {
    // ... Modal HTML erstellen ...
    
    // ENTFERNE die hardcodierte verantwortlichOptions Variable!
    
    // Nach dem Einfügen des Modals ins DOM:
    document.body.insertAdjacentHTML('beforeend', html);
    
    // Dropdown dynamisch befüllen
    populateUserDropdown('m-verantwortlich');
    
    // ... restlicher Code ...
}
```

### 1.5 HTML anpassen

**Datei:** `/var/www/html/rms/index.html`

**Im Edit-Modal - Verantwortlich-Dropdown:**
```html
<!-- VORHER (hardcodiert): -->
<select id="edit-verantwortlich" class="form-control">
    <option value="">-- Auswählen --</option>
    <option value="AL">AL - Andreas Loehr</option>
    <!-- ... mehr hardcodierte Optionen ... -->
</select>

<!-- NACHHER (dynamisch): -->
<select id="edit-verantwortlich" class="form-control">
    <option value="">-- Auswählen --</option>
    <!-- Wird dynamisch durch JavaScript befüllt -->
</select>
```

### 1.6 Maßnahmen-Template anpassen

**Datei:** `/var/www/html/rms/js/massnahmen-templates.js`

**ENTFERNE die hardcodierte VERANTWORTLICHE-Konstante komplett!**

```javascript
// ENTFERNEN:
// const VERANTWORTLICHE = [
//     { kuerzel: 'AL', name: 'Andreas Loehr', ... },
//     ...
// ];

// Die Maßnahmen-Templates können bleiben, aber ohne empfohlenerVerantwortlicher
// oder mit null/undefined als Wert
```

---

## AUFGABE 2: PDF-Generierung fixen

### 2.1 Problem-Analyse

**Symptom:** PDF wird erstellt und nach SharePoint hochgeladen, aber Datei ist korrupt.

**Mögliche Ursachen:**
1. XLSX-Template wird nicht korrekt von SharePoint geladen
2. fill_xlsx_form.py befüllt keine Felder (falsches Mapping)
3. LibreOffice-Konvertierung schlägt fehl
4. Binary-Daten werden falsch an SharePoint übertragen

### 2.2 Diagnose-Schritte ausführen

```bash
# 1. Formblatt-Service Status prüfen
systemctl status formblatt-service
journalctl -u formblatt-service -n 100 --no-pager

# 2. Temp-Verzeichnis prüfen
ls -la /tmp/rms-forms/

# 3. LibreOffice testen
echo "Test" > /tmp/test.txt
libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.txt
ls -la /tmp/test.pdf
file /tmp/test.pdf

# 4. Test-XLSX erstellen und konvertieren
python3 << 'EOF'
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws['A1'] = 'Test'
ws['B1'] = 'Wert'
wb.save('/tmp/rms-forms/test_manual.xlsx')
print('XLSX erstellt')
EOF

# 5. XLSX zu PDF konvertieren
python3 /opt/osp/scripts/convert_to_pdf.py /tmp/rms-forms/test_manual.xlsx /tmp/rms-forms/test_manual.pdf

# 6. Ergebnis prüfen
ls -la /tmp/rms-forms/test_manual.*
file /tmp/rms-forms/test_manual.pdf
```

### 2.3 fill_xlsx_form.py überprüfen und fixen

**Datei:** `/opt/osp/scripts/fill_xlsx_form.py`

**Problem:** Das Script findet möglicherweise keine Felder im Template oder das Mapping stimmt nicht.

**Analyse des aktuellen Templates:**

```bash
# Template aus SharePoint herunterladen (manuell oder via curl mit Auth)
# Dann analysieren:
python3 /opt/osp/scripts/fill_xlsx_form.py /tmp/rms-forms/FQM02_template.xlsx --analyze
```

**Verbessertes fill_xlsx_form.py:**

```python
#!/usr/bin/env python3
"""
RMS Formular-Befüller v2.0
Befüllt XLSX-Templates mit Reklamationsdaten
"""

import argparse
import json
import sys
import re
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    print("ERROR: openpyxl nicht installiert")
    sys.exit(1)


def find_and_fill_cells(ws, data: dict, verbose: bool = True):
    """
    Durchsucht das Worksheet nach Platzhaltern und befüllt sie.
    Unterstützt verschiedene Platzhalter-Formate:
    - {{feldname}}
    - {feldname}
    - [feldname]
    - Zellen mit bestimmten Labels
    """
    filled_count = 0
    
    # Mapping von möglichen Feldnamen zu Datenschlüsseln
    field_aliases = {
        'qa_id': ['qa_id', 'QA_ID', 'abweichungs_nr', 'Abweichungs_Nr', 'id'],
        'datum': ['datum', 'Datum', 'date', 'erfassungsdatum', 'Erfassungsdatum'],
        'titel': ['titel', 'Title', 'title', 'betreff', 'Betreff'],
        'beschreibung': ['beschreibung', 'Beschreibung', 'description'],
        'typ': ['typ', 'Typ', 'Rekla_Typ', 'rekla_typ'],
        'status': ['status', 'Status', 'Rekla_Status'],
        'prioritaet': ['prioritaet', 'Prioritaet', 'priorität', 'Priorität'],
        'lieferant': ['lieferant', 'Lieferant', 'Absender', 'absender', 'firma'],
        'verantwortlich': ['verantwortlich', 'Verantwortlich', 'responsible'],
    }
    
    def get_value_for_field(field_name: str) -> str:
        """Findet den Wert für ein Feld anhand von Aliases"""
        field_lower = field_name.lower().replace('_', '').replace('-', '')
        
        # Direkte Übereinstimmung
        if field_name in data:
            return str(data[field_name])
        
        # Alias-Suche
        for canonical, aliases in field_aliases.items():
            if field_lower in [a.lower().replace('_', '') for a in aliases]:
                for alias in aliases:
                    if alias in data:
                        return str(data[alias])
        
        # Case-insensitive Suche
        for key, value in data.items():
            if key.lower() == field_lower:
                return str(value)
        
        return None
    
    # Durch alle Zellen iterieren
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is None:
                continue
            
            cell_value = str(cell.value)
            
            # Platzhalter-Pattern suchen
            patterns = [
                r'\{\{(\w+)\}\}',  # {{feldname}}
                r'\{(\w+)\}',      # {feldname}
                r'\[(\w+)\]',      # [feldname]
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, cell_value)
                for match in matches:
                    value = get_value_for_field(match)
                    if value:
                        # Platzhalter ersetzen
                        cell_value = re.sub(
                            pattern.replace(r'(\w+)', re.escape(match)),
                            value,
                            cell_value
                        )
                        filled_count += 1
                        if verbose:
                            print(f"  ✅ {cell.coordinate}: {match} → {value[:50]}")
            
            # Aktualisierte Wert setzen
            if cell_value != str(cell.value):
                cell.value = cell_value
    
    return filled_count


def fill_by_position(ws, data: dict, form_type: str, verbose: bool = True):
    """
    Befüllt Zellen basierend auf vordefinierten Positionen für bekannte Formulare.
    """
    # Positions-Mappings für verschiedene Formulare
    mappings = {
        'F_QM_02': {
            # Zeile 1-5: Header-Bereich
            'C3': 'qa_id',
            'C4': 'datum',
            # Zeile 10-20: Lieferantendaten
            'C12': 'lieferant',
            'C14': 'artikel',
            # Zeile 25-40: Fehlerbeschreibung
            'A26': 'beschreibung',
            # Anpassen nach tatsächlichem Template!
        },
        'F_QM_03': {
            'D3': 'qa_id',
            'D4': 'datum',
            'D5': 'kunde',
            'B10': 'd1_team',
            'B14': 'd2_problembeschreibung',
        },
        'F_QM_04': {
            'D3': 'nza_nr',
            'D4': 'datum',
            'B10': 'fehler_beschreibung',
        },
        'F_QM_14': {
            'D3': 'km_nr',
            'D4': 'datum',
            'B10': 'abweichung',
        }
    }
    
    mapping = mappings.get(form_type, {})
    if not mapping:
        if verbose:
            print(f"  ⚠️ Kein Positions-Mapping für {form_type}")
        return 0
    
    filled_count = 0
    for cell_ref, field_name in mapping.items():
        # Wert aus data holen (case-insensitive)
        value = None
        for key in data:
            if key.lower() == field_name.lower():
                value = data[key]
                break
        
        if value:
            try:
                ws[cell_ref] = str(value)
                filled_count += 1
                if verbose:
                    print(f"  ✅ {cell_ref} = {str(value)[:50]}")
            except Exception as e:
                if verbose:
                    print(f"  ❌ {cell_ref}: {e}")
    
    return filled_count


def fill_workbook(template_path: str, output_path: str, data: dict, form_type: str = None):
    """Hauptfunktion zum Befüllen eines XLSX-Templates"""
    
    print(f"📄 Lade Template: {template_path}")
    
    try:
        wb = load_workbook(template_path)
    except Exception as e:
        print(f"❌ Fehler beim Laden: {e}")
        return False
    
    ws = wb.active
    print(f"   Sheet: {ws.title}, Dimensionen: {ws.dimensions}")
    
    # Formulartyp erkennen
    if not form_type:
        filename = Path(template_path).stem.upper()
        if 'QM02' in filename or 'QM_02' in filename:
            form_type = 'F_QM_02'
        elif 'QM03' in filename or '8D' in filename:
            form_type = 'F_QM_03'
        elif 'QM04' in filename or 'NZA' in filename:
            form_type = 'F_QM_04'
        elif 'QM14' in filename:
            form_type = 'F_QM_14'
    
    print(f"   Formulartyp: {form_type or 'Unbekannt'}")
    print(f"   Daten-Felder: {list(data.keys())}")
    
    # Methode 1: Platzhalter suchen und ersetzen
    print("\n🔍 Suche Platzhalter...")
    filled_placeholders = find_and_fill_cells(ws, data)
    
    # Methode 2: Positions-basiertes Befüllen
    print("\n📍 Positions-basiertes Befüllen...")
    filled_positions = fill_by_position(ws, data, form_type) if form_type else 0
    
    total_filled = filled_placeholders + filled_positions
    
    # Speichern
    print(f"\n💾 Speichere: {output_path}")
    try:
        wb.save(output_path)
        wb.close()
        
        # Dateigröße prüfen
        size = Path(output_path).stat().st_size
        print(f"   Größe: {size} Bytes")
        
        if size < 1000:
            print("   ⚠️ WARNUNG: Datei sehr klein!")
        
        print(f"\n✅ {total_filled} Felder befüllt")
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")
        return False


def analyze_workbook(filepath: str):
    """Analysiert ein Workbook und zeigt alle Zellen mit Inhalt"""
    
    print(f"\n📊 Analyse: {filepath}")
    
    try:
        wb = load_workbook(filepath)
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        print(f"\n📋 Sheet: {sheet_name}")
        print(f"   Dimensionen: {ws.dimensions}")
        
        # Zellen mit Inhalt sammeln
        cells = []
        for row in ws.iter_rows(max_row=100, max_col=20):
            for cell in row:
                if cell.value:
                    value_str = str(cell.value)[:60]
                    # Platzhalter hervorheben
                    if '{{' in value_str or '{' in value_str or '[' in value_str:
                        cells.append(f"   🔶 {cell.coordinate}: {value_str}")
                    else:
                        cells.append(f"   {cell.coordinate}: {value_str}")
        
        print(f"\n   Zellen mit Inhalt ({len(cells)}):")
        for c in cells[:50]:
            print(c)
        
        if len(cells) > 50:
            print(f"   ... und {len(cells) - 50} weitere")
    
    wb.close()


def main():
    parser = argparse.ArgumentParser(description="RMS Formular-Befüller v2.0")
    parser.add_argument("template", help="Pfad zum XLSX-Template")
    parser.add_argument("output", nargs="?", help="Pfad zur Ausgabedatei")
    parser.add_argument("--data", "-d", help="JSON-String mit Felddaten")
    parser.add_argument("--data-file", "-f", help="JSON-Datei mit Felddaten")
    parser.add_argument("--analyze", "-a", action="store_true", help="Template analysieren")
    parser.add_argument("--form-type", "-t", help="Formulartyp (F_QM_02, F_QM_03, etc.)")
    
    args = parser.parse_args()
    
    if not Path(args.template).exists():
        print(f"❌ Template nicht gefunden: {args.template}")
        sys.exit(1)
    
    if args.analyze:
        analyze_workbook(args.template)
        return
    
    # Daten laden
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"❌ Ungültiges JSON: {e}")
            sys.exit(1)
    elif args.data_file:
        with open(args.data_file) as f:
            data = json.load(f)
    else:
        print("❌ Keine Daten angegeben. Verwende --data oder --data-file")
        sys.exit(1)
    
    if not args.output:
        template_path = Path(args.template)
        args.output = str(template_path.parent / f"filled_{template_path.name}")
    
    success = fill_workbook(args.template, args.output, data, args.form_type)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

### 2.4 convert_to_pdf.py überprüfen und fixen

**Datei:** `/opt/osp/scripts/convert_to_pdf.py`

```python
#!/usr/bin/env python3
"""
Konvertiert XLSX/DOCX zu PDF mit LibreOffice Headless
Version 2.0 - Mit verbesserter Fehlerbehandlung
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path


def convert_to_pdf(input_path: str, output_path: str = None) -> str:
    """Konvertiert Dokument zu PDF"""
    
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"❌ Datei nicht gefunden: {input_path}")
        return None
    
    print(f"📄 Input: {input_file}")
    print(f"   Größe: {input_file.stat().st_size} Bytes")
    
    # Output-Pfad bestimmen
    if output_path:
        output_file = Path(output_path)
        output_dir = output_file.parent
    else:
        output_dir = input_file.parent
        output_file = output_dir / f"{input_file.stem}.pdf"
    
    # Sicherstellen dass Output-Verzeichnis existiert
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Temporäres Verzeichnis für LibreOffice
    tmp_dir = Path('/tmp/libreoffice_convert')
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    # HOME-Verzeichnis setzen (wichtig für LibreOffice)
    env = os.environ.copy()
    env['HOME'] = str(tmp_dir)
    
    # LibreOffice Headless ausführen
    cmd = [
        "libreoffice",
        "--headless",
        "--invisible",
        "--nologo",
        "--nofirststartwizard",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(input_file)
    ]
    
    print(f"🔄 Konvertiere zu PDF...")
    print(f"   Befehl: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )
        
        print(f"   Return Code: {result.returncode}")
        
        if result.stdout:
            print(f"   Stdout: {result.stdout[:500]}")
        if result.stderr:
            print(f"   Stderr: {result.stderr[:500]}")
        
        # LibreOffice erstellt PDF mit gleichem Basename
        generated_pdf = output_dir / f"{input_file.stem}.pdf"
        
        if not generated_pdf.exists():
            print(f"❌ PDF wurde nicht erstellt!")
            print(f"   Erwartet: {generated_pdf}")
            
            # Suche nach PDFs im Verzeichnis
            pdfs = list(output_dir.glob("*.pdf"))
            if pdfs:
                print(f"   Gefundene PDFs: {pdfs}")
            
            return None
        
        # Falls anderer Output-Name gewünscht
        if output_path and generated_pdf != output_file:
            shutil.move(str(generated_pdf), str(output_file))
            generated_pdf = output_file
        
        # Ergebnis prüfen
        pdf_size = generated_pdf.stat().st_size
        print(f"✅ PDF erstellt: {generated_pdf}")
        print(f"   Größe: {pdf_size} Bytes")
        
        if pdf_size < 1000:
            print("   ⚠️ WARNUNG: PDF sehr klein - möglicherweise leer!")
        
        # PDF-Header prüfen
        with open(generated_pdf, 'rb') as f:
            header = f.read(8)
            if not header.startswith(b'%PDF'):
                print(f"   ⚠️ WARNUNG: Datei beginnt nicht mit %PDF!")
                print(f"   Header: {header}")
        
        return str(generated_pdf)
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout bei PDF-Konvertierung (120s)")
        return None
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Verwendung: python3 convert_to_pdf.py input.xlsx [output.pdf]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = convert_to_pdf(input_path, output_path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
```

### 2.5 n8n Workflow RMS-Generate-Formblatt debuggen

**Workflow-ID:** `MN63eCmmUDHzED8G`

**Wichtige Prüfpunkte:**

1. **Template-Download:** Wird das XLSX korrekt von SharePoint geladen?
2. **Binary-Konvertierung:** Wird Base64 korrekt verarbeitet?
3. **Script-Aufruf:** Werden die Scripts mit korrekten Parametern aufgerufen?
4. **Upload:** Werden die Dateien korrekt nach SharePoint hochgeladen?

**Debug-Node einfügen (nach jedem kritischen Schritt):**

```javascript
// Debug Code Node
console.log('=== DEBUG ===');
console.log('Input:', JSON.stringify($input.item.json, null, 2));

// Für Binary-Daten
if ($input.item.binary) {
    for (const key of Object.keys($input.item.binary)) {
        const bin = $input.item.binary[key];
        console.log(`Binary "${key}":`, {
            mimeType: bin.mimeType,
            fileSize: bin.fileSize,
            fileName: bin.fileName
        });
    }
}

return $input.item.json;
```

### 2.6 Formblatt-Service aktualisieren

**Datei:** `/opt/osp/scripts/formblatt_service.py`

Stelle sicher, dass der Service die aktualisierten Scripts verwendet:

```bash
# Service neu starten nach Script-Updates
systemctl restart formblatt-service

# Logs prüfen
journalctl -u formblatt-service -f
```

---

## AUFGABE 3: Tests durchführen

### 3.1 Test M365-Benutzer API

```bash
# Test 1: API-Endpoint erreichbar?
curl -s https://osp.schneider-kabelsatzbau.de/api/rms/users | head -c 500

# Erwartetes Ergebnis: JSON mit users-Array
# {
#   "users": [
#     {"id": "...", "displayName": "...", "mail": "...", ...},
#     ...
#   ]
# }
```

### 3.2 Test Frontend M365-Dropdown

```bash
# Browser öffnen: https://osp.schneider-kabelsatzbau.de/rms/
# 
# Test-Schritte:
# 1. Seite laden
# 2. Browser Console öffnen (F12)
# 3. Prüfen: "X M365-Benutzer geladen" in Console?
# 4. Reklamation öffnen
# 5. "Bearbeiten" klicken
# 6. Dropdown "Verantwortlich" prüfen - echte Namen aus M365?
# 7. "Neue Maßnahme" öffnen
# 8. Dropdown "Verantwortlich" prüfen - echte Namen aus M365?
```

### 3.3 Test PDF-Generierung

```bash
# Test 1: Manueller Script-Test
cd /tmp/rms-forms

# Dummy-Daten erstellen
cat > /tmp/rms-forms/test_data.json << 'EOF'
{
    "qa_id": "QA-TEST-001",
    "datum": "2026-01-29",
    "titel": "Test Reklamation",
    "beschreibung": "Dies ist eine Test-Beschreibung",
    "lieferant": "Test Lieferant GmbH",
    "prioritaet": "hoch"
}
EOF

# Template herunterladen (falls nicht vorhanden)
# Dann befüllen:
python3 /opt/osp/scripts/fill_xlsx_form.py \
    /tmp/rms-forms/FQM02_template.xlsx \
    /tmp/rms-forms/test_filled.xlsx \
    --data-file /tmp/rms-forms/test_data.json \
    --form-type F_QM_02

# PDF erstellen
python3 /opt/osp/scripts/convert_to_pdf.py \
    /tmp/rms-forms/test_filled.xlsx \
    /tmp/rms-forms/test_output.pdf

# Ergebnis prüfen
ls -la /tmp/rms-forms/test_*
file /tmp/rms-forms/test_output.pdf

# PDF-Inhalt prüfen (erste Zeilen)
head -c 100 /tmp/rms-forms/test_output.pdf
```

### 3.4 Test über Dashboard

```bash
# Browser öffnen: https://osp.schneider-kabelsatzbau.de/rms/
#
# Test-Schritte:
# 1. Reklamation auswählen
# 2. Detail-Modal öffnen
# 3. "PDF erstellen" Button klicken
# 4. Formular-Typ wählen (F-QM-02)
# 5. Warten auf Ergebnis
# 6. PDF-Link anklicken
# 7. PDF sollte sich öffnen und INHALT haben
```

---

## AUFGABE 4: Report erstellen

Nach Abschluss aller Arbeiten einen detaillierten Report erstellen:

**Datei:** `/var/www/html/rms/docs/RMS_Phase1_1_Report_2026-01-29.md`

```markdown
# RMS Phase 1.1 - Implementierungsbericht

**Datum:** 2026-01-29
**Status:** [ERFOLGREICH/TEILWEISE/FEHLGESCHLAGEN]

## Durchgeführte Änderungen

### 1. M365-Benutzer Integration
- [ ] n8n Workflow RMS-Users-API erstellt (ID: ...)
- [ ] Nginx Route /api/rms/users hinzugefügt
- [ ] Frontend: Dynamisches Laden der Benutzer
- [ ] Hardcodierte Listen entfernt

**Test-Ergebnis:** [Bestanden/Nicht bestanden]
**Anzahl geladener Benutzer:** X

### 2. PDF-Generierung Fix
- [ ] fill_xlsx_form.py aktualisiert (Version 2.0)
- [ ] convert_to_pdf.py aktualisiert (Version 2.0)
- [ ] n8n Workflow debugged

**Test-Ergebnis:** [Bestanden/Nicht bestanden]
**PDF-Größe bei Test:** X Bytes

## Test-Protokoll

| Test | Ergebnis | Bemerkung |
|------|----------|-----------|
| M365 API erreichbar | ✅/❌ | |
| Benutzer werden geladen | ✅/❌ | X Benutzer |
| Dropdown zeigt echte Namen | ✅/❌ | |
| PDF-Script funktioniert | ✅/❌ | |
| PDF hat Inhalt | ✅/❌ | X Bytes |
| PDF öffnet sich | ✅/❌ | |

## Bekannte Einschränkungen

- ...

## Nächste Schritte

- ...
```

---

## ✅ ABSCHLUSS-CHECKLISTE

Vor Abschluss ALLE Punkte prüfen:

### M365-Integration
- [ ] n8n Workflow RMS-Users-API aktiv
- [ ] API `/api/rms/users` gibt Benutzer zurück
- [ ] Console zeigt "X M365-Benutzer geladen"
- [ ] Edit-Modal: Dropdown zeigt ECHTE M365-Benutzer
- [ ] Maßnahmen-Modal: Dropdown zeigt ECHTE M365-Benutzer
- [ ] Keine hardcodierten Namen mehr im Code

### PDF-Generierung
- [ ] fill_xlsx_form.py Version 2.0 installiert
- [ ] convert_to_pdf.py Version 2.0 installiert
- [ ] Manueller Test erfolgreich (PDF > 1000 Bytes)
- [ ] Dashboard-Test erfolgreich (PDF öffnet sich mit Inhalt)

### Allgemein
- [ ] Keine JavaScript-Fehler in Browser Console
- [ ] Alle n8n Workflows aktiv
- [ ] Report erstellt

---

## 📚 REFERENZEN

| Resource | Wert |
|----------|------|
| Dashboard | https://osp.schneider-kabelsatzbau.de/rms/ |
| n8n | http://46.224.102.30:5678 |
| Graph API Users | https://graph.microsoft.com/v1.0/users |
| Frontend | /var/www/html/rms/ |
| Scripts | /opt/osp/scripts/ |

---

*Erstellt: 2026-01-29*
*Wichtig: Alle Änderungen TESTEN bevor als abgeschlossen markiert!*
