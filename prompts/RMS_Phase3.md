# Claude Code Prompt: RMS Phase 3 & 5 (AKTUALISIERT)

## KONTEXT

Du arbeitest auf dem Hetzner Server (46.224.102.30) für OSP Schneider Kabelsatzbau.

**Bereits erledigt:**
- ✅ Phase 1: E-Mail-Import, QA-ID-Generierung, Reklamation erstellen
- ✅ Phase 2: Anhänge laden, SharePoint-Ordner, Teams-Benachrichtigung
- ✅ Alle RMS-Workflows aktiv und konfiguriert

**Umgebung:**
```bash
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMGFkYS1mMGU5NTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM4MDQxNDQxfQ.Hhqnbitgd-ak_iZruZy1Z_rdHJ75BtcYfv09RO05Rtg"
export N8N_BASE_URL="http://127.0.0.1:5678"
```

**Bestehende Workflows:**
| ID | Name | Status |
|----|------|--------|
| k3rVSLW6O00dtTBr | RMS-Email-Import-V2 | 🟢 Aktiv |
| Eu7T9rCmLub6xO05 | RMS-QA-ID-Generator | 🟢 Aktiv |
| yiR3dlT4AKEZt9ti | RMS-Ordner-Sync | 🟢 Aktiv |
| Z4D6ChArp86tDKC0 | RMS-Eskalation-Monitor | 🟢 Aktiv |
| Aq6gmrE8IX3RKIeF | RMS-Error-Handler | 🟢 Aktiv |

---

## 📁 VORHANDENE DATEIEN AUF DEM SERVER

**Pfad:** `/mnt/HC_Volume_104189729/osp/rms/formulare/f_qm_02_qualitaetsabweichung/`

| Datei | Beschreibung |
|-------|--------------|
| `RMS_Prompt_F_QM_02_Qualitaetsabweichung.md` | KI-Prompt für halbautomatische Befüllung |
| `F_QM_02_Schema.json` | JSON-Schema mit Validierung |
| `F_QM_02_Qualitaetsabweichung.md` | Markdown-Template mit Excel-Mapping |
| `README.md` | Dokumentation |

**WICHTIG:** Diese Dateien sind bereits vorhanden und definieren die Struktur. Nutze sie!

---

## 🎯 PHASE 3: F-QM-02 PDF-Generierung

### Vorhandenes JSON-Schema (F_QM_02_Schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "F-QM-02 Qualitätsabweichung",
  "required": [
    "formblatt_id", "datum", "lieferant", "artikel", 
    "beschreibung", "massnahmen", "ersteller"
  ],
  "properties": {
    "formblatt_id": { "const": "F_QM_02" },
    "abweichungs_nr": { "pattern": "^QA-\\d{4}-\\d{3}$" },
    "datum": { "format": "date" },
    "lieferant": {
      "required": ["firma", "ansprechpartner"],
      "properties": {
        "firma": { "minLength": 2 },
        "ansprechpartner": { "minLength": 2 },
        "telefon": { "pattern": "^[+]?[0-9\\s\\-/]+$" },
        "email": { "format": "email" }
      }
    },
    "artikel": {
      "required": ["nr_schneider", "bezeichnung", "lieferschein_nr", 
                   "lieferdatum", "liefermenge", "beanstandungsmenge"],
      "properties": {
        "liefermenge": { "properties": { "wert": {}, "einheit": {} } },
        "beanstandungsmenge": { "properties": { "wert": {}, "einheit": {} } }
      }
    },
    "beschreibung": { "minLength": 50, "maxLength": 2000 },
    "massnahmen": {
      "minItems": 1,
      "items": {
        "enum": ["untersuchung_abstellen", "untersuchung_8d", 
                 "ersatzlieferung", "ruecksendung_nacharbeit", "gutschrift"]
      }
    },
    "ersteller": { "pattern": "^[A-Z]{2,3}$" },
    "status": { "enum": ["entwurf", "erstellt", "gesendet", "beantwortet", "abgeschlossen"] }
  }
}
```

### Vorhandenes Excel-Mapping (aus F_QM_02_Qualitaetsabweichung.md)

```yaml
excel_mapping:
  sheet: "Seite 1"
  felder:
    abweichungs_nr: I1
    datum: I3
    lieferant_firma: A17:E19        # Merged Cell
    lieferant_ansprechpartner: G17:I19  # Merged Cell
    artikel_nr_schneider: E23
    artikel_nr_lieferant: E24
    artikel_bezeichnung: E25
    lieferschein_nr: E26
    lieferdatum: E27
    liefermenge: E28
    beanstandungsmenge: E29
    beschreibung_abweichung: A33:I42  # Großes Textfeld
  checkboxen:
    untersuchung_abstellen: A47
    untersuchung_8d: A48
    ersatzlieferung: A50
    ruecksendung_nacharbeit: A51
    gutschrift: A52
```

### Aufgabe: PDF-Generator implementieren

#### Option A: HTML→PDF mit WeasyPrint (EMPFOHLEN)

1. **Verzeichnisse erstellen:**
```bash
mkdir -p /opt/osp/templates
mkdir -p /opt/osp/output
mkdir -p /opt/osp/scripts
```

2. **HTML-Template erstellen:** `/opt/osp/templates/F_QM_02_template.html`

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <style>
    @page { 
      size: A4; 
      margin: 1.5cm 2cm; 
      @bottom-center { content: "Seite " counter(page) " von " counter(pages); font-size: 8pt; }
    }
    body { 
      font-family: Arial, Helvetica, sans-serif; 
      font-size: 10pt; 
      line-height: 1.4;
      color: #333;
    }
    
    /* Header */
    .header { 
      display: flex; 
      justify-content: space-between; 
      align-items: flex-start;
      border-bottom: 2px solid #003366; 
      padding-bottom: 10px; 
      margin-bottom: 15px;
    }
    .logo { height: 45px; }
    .doc-info { 
      text-align: right; 
      font-size: 9pt; 
      color: #666;
    }
    .doc-info strong { 
      font-size: 14pt; 
      color: #003366; 
      display: block;
    }
    
    /* Title */
    .title { 
      background: linear-gradient(135deg, #003366, #004080); 
      color: white; 
      padding: 12px 15px; 
      margin: 15px 0; 
      font-size: 14pt;
      font-weight: bold;
    }
    .title-en { 
      font-size: 10pt; 
      font-weight: normal; 
      font-style: italic; 
    }
    
    /* Sections */
    .section { 
      margin: 15px 0; 
      border: 1px solid #ddd;
      border-radius: 4px;
    }
    .section-header { 
      background: #f5f5f5; 
      padding: 8px 12px; 
      font-weight: bold; 
      color: #003366;
      border-bottom: 1px solid #ddd;
      font-size: 11pt;
    }
    .section-content { 
      padding: 12px; 
    }
    
    /* Tables */
    table { 
      width: 100%; 
      border-collapse: collapse; 
    }
    td { 
      padding: 6px 8px; 
      vertical-align: top;
    }
    .label { 
      font-weight: bold; 
      color: #003366; 
      width: 35%;
      background: #fafafa;
    }
    .value { 
      border-bottom: 1px solid #ccc; 
    }
    
    /* Grid Layout */
    .grid-2 { 
      display: grid; 
      grid-template-columns: 1fr 1fr; 
      gap: 15px; 
    }
    
    /* Beschreibung */
    .beschreibung { 
      min-height: 120px; 
      border: 1px solid #ccc; 
      padding: 10px; 
      background: #fafafa;
      white-space: pre-wrap;
    }
    
    /* Checkboxen */
    .checkbox-list { padding: 0; margin: 0; list-style: none; }
    .checkbox-item { 
      padding: 8px 0; 
      border-bottom: 1px solid #eee;
      display: flex;
      align-items: flex-start;
    }
    .checkbox-item:last-child { border-bottom: none; }
    .checkbox { 
      display: inline-block;
      width: 16px; 
      height: 16px; 
      border: 2px solid #003366; 
      margin-right: 10px;
      text-align: center;
      line-height: 14px;
      font-weight: bold;
      flex-shrink: 0;
    }
    .checkbox.checked { 
      background: #003366; 
      color: white; 
    }
    .checkbox-text { flex: 1; }
    .checkbox-text-en { 
      font-size: 9pt; 
      color: #666; 
      font-style: italic;
    }
    
    /* Priority Badge */
    .priority { 
      display: inline-block;
      padding: 3px 10px; 
      border-radius: 3px;
      font-weight: bold;
      font-size: 9pt;
    }
    .priority-kritisch { background: #dc3545; color: white; }
    .priority-hoch { background: #fd7e14; color: white; }
    .priority-mittel { background: #ffc107; color: #333; }
    .priority-niedrig { background: #28a745; color: white; }
    
    /* Footer */
    .footer { 
      margin-top: 20px;
      padding-top: 10px;
      border-top: 1px solid #ccc; 
      font-size: 8pt; 
      color: #666;
      text-align: center;
    }
    
    /* Signatures */
    .signatures {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 30px;
      margin-top: 20px;
    }
    .signature-box {
      border-top: 1px solid #333;
      padding-top: 5px;
      text-align: center;
      font-size: 9pt;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <img src="/opt/osp/templates/schneider_logo.png" class="logo" alt="Schneider Kabelsatzbau">
    <div class="doc-info">
      <strong>F-QM-02</strong>
      Qualitätsabweichung<br>
      Version: 3.0<br>
      {{ abweichungs_nr }}
    </div>
  </div>

  <!-- Title -->
  <div class="title">
    QUALITÄTSABWEICHUNG / REKLAMATION
    <span class="title-en">Quality Deviation / Complaint</span>
  </div>

  <!-- Absender & Empfänger -->
  <div class="grid-2">
    <div class="section">
      <div class="section-header">📤 Absender / Sender</div>
      <div class="section-content">
        <strong>Rainer Schneider Kabelsatzbau GmbH & Co. KG</strong><br>
        Alte Hütte 3<br>
        57537 Wissen<br><br>
        <strong>Ansprechpartner:</strong> Andreas Löhr<br>
        <strong>Tel:</strong> +49 2742 9336-28<br>
        <strong>E-Mail:</strong> a.loehr@schneider-kabelsatzbau.de
      </div>
    </div>
    
    <div class="section">
      <div class="section-header">📥 Lieferant / Supplier</div>
      <div class="section-content">
        <strong>{{ lieferant_firma }}</strong><br><br>
        <strong>Ansprechpartner:</strong> {{ lieferant_ansprechpartner }}<br>
        {% if lieferant_telefon %}<strong>Tel:</strong> {{ lieferant_telefon }}<br>{% endif %}
        {% if lieferant_email %}<strong>E-Mail:</strong> {{ lieferant_email }}{% endif %}
      </div>
    </div>
  </div>

  <!-- Artikeldaten -->
  <div class="section">
    <div class="section-header">📦 Artikeldaten / Part Data</div>
    <div class="section-content">
      <table>
        <tr>
          <td class="label">Abweichungs-Nr. / Deviation No.</td>
          <td class="value"><strong>{{ abweichungs_nr }}</strong></td>
          <td class="label">Datum / Date</td>
          <td class="value">{{ datum }}</td>
        </tr>
        <tr>
          <td class="label">Artikel-Nr. Schneider</td>
          <td class="value">{{ artikel_nr_schneider }}</td>
          <td class="label">Artikel-Nr. Lieferant</td>
          <td class="value">{{ artikel_nr_lieferant }}</td>
        </tr>
        <tr>
          <td class="label">Artikelbezeichnung / Description</td>
          <td class="value" colspan="3">{{ artikel_bezeichnung }}</td>
        </tr>
        <tr>
          <td class="label">Lieferschein-Nr. / Delivery Note</td>
          <td class="value">{{ lieferschein_nr }}</td>
          <td class="label">Lieferdatum / Delivery Date</td>
          <td class="value">{{ lieferdatum }}</td>
        </tr>
        <tr>
          <td class="label">Liefermenge / Delivered Qty</td>
          <td class="value">{{ liefermenge }}</td>
          <td class="label">Beanstandungsmenge / Defect Qty</td>
          <td class="value"><strong style="color: #dc3545;">{{ beanstandungsmenge }}</strong></td>
        </tr>
      </table>
    </div>
  </div>

  <!-- Beschreibung -->
  <div class="section">
    <div class="section-header">⚠️ Beschreibung der Qualitätsabweichung / Description of Quality Deviation</div>
    <div class="section-content">
      <div class="beschreibung">{{ beschreibung }}</div>
    </div>
  </div>

  <!-- Maßnahmen -->
  <div class="section">
    <div class="section-header">✅ Geforderte Maßnahmen / Required Actions</div>
    <div class="section-content">
      <p><em>Wir bitten um Stellungnahme und fordern Sie zur Nachbesserung auf:</em></p>
      <ul class="checkbox-list">
        <li class="checkbox-item">
          <span class="checkbox {{ 'checked' if 'untersuchung_abstellen' in massnahmen else '' }}">{{ '✓' if 'untersuchung_abstellen' in massnahmen else '' }}</span>
          <span class="checkbox-text">
            Untersuchen Sie Ihren Prozess und stellen Sie die Mängel ab<br>
            <span class="checkbox-text-en">Examine your process and remedy the defects</span>
          </span>
        </li>
        <li class="checkbox-item">
          <span class="checkbox {{ 'checked' if 'untersuchung_8d' in massnahmen else '' }}">{{ '✓' if 'untersuchung_8d' in massnahmen else '' }}</span>
          <span class="checkbox-text">
            Untersuchen Sie Ihren Prozess mittels 8D-Report<br>
            <span class="checkbox-text-en">Examine your process using 8D report</span>
          </span>
        </li>
        <li class="checkbox-item">
          <span class="checkbox {{ 'checked' if 'ersatzlieferung' in massnahmen else '' }}">{{ '✓' if 'ersatzlieferung' in massnahmen else '' }}</span>
          <span class="checkbox-text">
            Wir benötigen schnellstmöglich eine Ersatzlieferung<br>
            <span class="checkbox-text-en">We need a replacement delivery as soon as possible</span>
          </span>
        </li>
        <li class="checkbox-item">
          <span class="checkbox {{ 'checked' if 'ruecksendung_nacharbeit' in massnahmen else '' }}">{{ '✓' if 'ruecksendung_nacharbeit' in massnahmen else '' }}</span>
          <span class="checkbox-text">
            Wir senden die Artikel zur Nacharbeit zurück<br>
            <span class="checkbox-text-en">We will send the items back for rework</span>
          </span>
        </li>
        <li class="checkbox-item">
          <span class="checkbox {{ 'checked' if 'gutschrift' in massnahmen else '' }}">{{ '✓' if 'gutschrift' in massnahmen else '' }}</span>
          <span class="checkbox-text">
            Wir benötigen eine Gutschrift<br>
            <span class="checkbox-text-en">We need a credit note</span>
          </span>
        </li>
      </ul>
    </div>
  </div>

  <!-- Unterschriften -->
  <div class="signatures">
    <div class="signature-box">
      <strong>{{ ersteller }}</strong><br>
      Erstellt von / Created by
    </div>
    <div class="signature-box">
      {{ datum }}<br>
      Datum / Date
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    Rainer Schneider Kabelsatzbau GmbH & Co. KG | Alte Hütte 3 | 57537 Wissen | ISO 9001:2015<br>
    Formblatt F-QM-02 | Qualitätsabweichung | {{ abweichungs_nr }}
  </div>

</body>
</html>
```

3. **Python PDF-Generator:** `/opt/osp/scripts/rms_pdf_generator.py`

```python
#!/usr/bin/env python3
"""
RMS PDF Generator für F-QM-02 Qualitätsabweichung
Verwendet vorhandenes JSON-Schema zur Validierung
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

# WeasyPrint und Jinja2 imports
try:
    from weasyprint import HTML, CSS
    from jinja2 import Template, Environment, FileSystemLoader
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("⚠️ WeasyPrint nicht installiert. Installiere mit: pip install weasyprint jinja2")

# Pfade
TEMPLATE_DIR = "/opt/osp/templates"
OUTPUT_DIR = "/opt/osp/output"
SCHEMA_PATH = "/mnt/HC_Volume_104189729/osp/rms/formulare/f_qm_02_qualitaetsabweichung/F_QM_02_Schema.json"

# Schema laden für Validierung
def load_schema():
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Schema nicht gefunden: {SCHEMA_PATH}")
        return None

SCHEMA = load_schema()

def validate_data(data):
    """Validiert Daten gegen das JSON-Schema (einfache Prüfung)"""
    errors = []
    
    # Pflichtfelder prüfen
    required_fields = ['datum', 'lieferant_firma', 'artikel_nr_schneider', 
                       'artikel_bezeichnung', 'lieferschein_nr', 'beschreibung']
    
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Pflichtfeld fehlt: {field}")
    
    # Beschreibung mindestens 50 Zeichen
    if data.get('beschreibung') and len(data['beschreibung']) < 50:
        errors.append("Beschreibung muss mindestens 50 Zeichen haben")
    
    # Mindestens eine Maßnahme
    if not data.get('massnahmen') or len(data.get('massnahmen', [])) == 0:
        errors.append("Mindestens eine Maßnahme muss ausgewählt werden")
    
    # Abweichungs-Nr Format prüfen (wenn angegeben)
    if data.get('abweichungs_nr'):
        import re
        if not re.match(r'^QA-\d{4}-\d{3}$', data['abweichungs_nr']):
            errors.append("Abweichungs-Nr muss Format QA-YYYY-NNN haben")
    
    return errors

def generate_pdf(data):
    """Generiert PDF aus den Formulardaten"""
    
    if not WEASYPRINT_AVAILABLE:
        return None, "WeasyPrint nicht verfügbar"
    
    # Template laden
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('F_QM_02_template.html')
    
    # Defaults setzen
    if not data.get('abweichungs_nr'):
        year = datetime.now().year
        data['abweichungs_nr'] = f"QA-{year}-XXX"  # Wird später ersetzt
    
    if not data.get('datum'):
        data['datum'] = datetime.now().strftime('%Y-%m-%d')
    
    if not data.get('ersteller'):
        data['ersteller'] = 'System'
    
    # Mengen formatieren
    if isinstance(data.get('liefermenge'), dict):
        data['liefermenge'] = f"{data['liefermenge']['wert']} {data['liefermenge']['einheit']}"
    if isinstance(data.get('beanstandungsmenge'), dict):
        data['beanstandungsmenge'] = f"{data['beanstandungsmenge']['wert']} {data['beanstandungsmenge']['einheit']}"
    
    # HTML rendern
    html_content = template.render(**data)
    
    # PDF generieren
    filename = f"F-QM-02_{data['abweichungs_nr']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Sicherstellen dass Output-Verzeichnis existiert
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # PDF schreiben
    HTML(string=html_content, base_url=TEMPLATE_DIR).write_pdf(filepath)
    
    return filepath, None


class PDFHandler(BaseHTTPRequestHandler):
    
    def _send_json(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/health':
            self._send_json(200, {
                'status': 'ok',
                'service': 'RMS PDF Generator',
                'weasyprint': WEASYPRINT_AVAILABLE,
                'schema_loaded': SCHEMA is not None
            })
        elif self.path == '/schema':
            if SCHEMA:
                self._send_json(200, SCHEMA)
            else:
                self._send_json(404, {'error': 'Schema nicht geladen'})
        else:
            self._send_json(404, {'error': 'Endpoint nicht gefunden'})
    
    def do_POST(self):
        if self.path == '/generate-pdf':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Validieren
                errors = validate_data(data)
                if errors:
                    self._send_json(400, {
                        'success': False,
                        'errors': errors
                    })
                    return
                
                # PDF generieren
                filepath, error = generate_pdf(data)
                
                if error:
                    self._send_json(500, {
                        'success': False,
                        'error': error
                    })
                    return
                
                self._send_json(200, {
                    'success': True,
                    'filepath': filepath,
                    'filename': os.path.basename(filepath)
                })
                
            except json.JSONDecodeError as e:
                self._send_json(400, {'success': False, 'error': f'Ungültiges JSON: {str(e)}'})
            except Exception as e:
                self._send_json(500, {'success': False, 'error': str(e)})
        
        elif self.path == '/validate':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                errors = validate_data(data)
                
                self._send_json(200, {
                    'valid': len(errors) == 0,
                    'errors': errors
                })
            except Exception as e:
                self._send_json(500, {'error': str(e)})
        
        else:
            self._send_json(404, {'error': 'Endpoint nicht gefunden'})


def main():
    port = int(os.environ.get('PDF_GENERATOR_PORT', 5001))
    server = HTTPServer(('0.0.0.0', port), PDFHandler)
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║  RMS PDF Generator - F-QM-02 Qualitätsabweichung              ║
╠═══════════════════════════════════════════════════════════════╣
║  Port:        {port}                                            ║
║  WeasyPrint:  {'✅ Verfügbar' if WEASYPRINT_AVAILABLE else '❌ Nicht installiert'}                              ║
║  Schema:      {'✅ Geladen' if SCHEMA else '❌ Nicht gefunden'}                                 ║
╠═══════════════════════════════════════════════════════════════╣
║  Endpoints:                                                   ║
║    GET  /health       - Status prüfen                         ║
║    GET  /schema       - JSON-Schema abrufen                   ║
║    POST /generate-pdf - PDF generieren                        ║
║    POST /validate     - Daten validieren                      ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    server.serve_forever()


if __name__ == "__main__":
    main()
```

4. **Systemd Service:** `/etc/systemd/system/rms-pdf-generator.service`

```ini
[Unit]
Description=RMS PDF Generator Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/osp/scripts
ExecStart=/usr/bin/python3 /opt/osp/scripts/rms_pdf_generator.py
Restart=always
RestartSec=5
Environment=PDF_GENERATOR_PORT=5001

[Install]
WantedBy=multi-user.target
```

### Aufgaben Phase 3

```bash
# 1. Abhängigkeiten installieren
pip install weasyprint jinja2 --break-system-packages

# 2. Verzeichnisse erstellen
mkdir -p /opt/osp/templates /opt/osp/output /opt/osp/scripts

# 3. Schneider Logo kopieren (falls vorhanden)
# Logo sollte als PNG vorhanden sein
cp /pfad/zum/logo.png /opt/osp/templates/schneider_logo.png

# Alternativ: Platzhalter erstellen
# convert -size 150x45 xc:white -fill '#003366' -gravity center \
#   -pointsize 12 -annotate 0 'SCHNEIDER' /opt/osp/templates/schneider_logo.png

# 4. HTML-Template erstellen (siehe oben)
nano /opt/osp/templates/F_QM_02_template.html

# 5. Python-Script erstellen (siehe oben)
nano /opt/osp/scripts/rms_pdf_generator.py
chmod +x /opt/osp/scripts/rms_pdf_generator.py

# 6. Service einrichten
nano /etc/systemd/system/rms-pdf-generator.service
systemctl daemon-reload
systemctl enable rms-pdf-generator
systemctl start rms-pdf-generator

# 7. Status prüfen
systemctl status rms-pdf-generator
curl http://localhost:5001/health

# 8. Test-PDF generieren
curl -X POST http://localhost:5001/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "abweichungs_nr": "QA-2026-001",
    "datum": "2026-01-27",
    "lieferant_firma": "Würth GmbH",
    "lieferant_ansprechpartner": "Max Mustermann",
    "artikel_nr_schneider": "45789",
    "artikel_bezeichnung": "Stecker Typ B12",
    "lieferschein_nr": "LS-4578123",
    "lieferdatum": "2026-01-25",
    "liefermenge": "500 Stk",
    "beanstandungsmenge": "50 Stk",
    "beschreibung": "Bei der Wareneingangsprüfung wurden 50 Stecker mit verbogenen Kontakten festgestellt. Die Kontakte sind so stark deformiert, dass eine Verwendung nicht möglich ist.",
    "massnahmen": ["ersatzlieferung", "untersuchung_8d"],
    "ersteller": "AL"
  }'

# 9. PDF prüfen
ls -la /opt/osp/output/
```

### n8n Integration (nach PDF-Generator)

**Neuer Node in RMS-Email-Import-V2:** "PDF generieren"

```javascript
// Position: Nach Node 9 (Reklamation erstellen)
// Type: HTTP Request
// Method: POST
// URL: http://localhost:5001/generate-pdf

// Body (JSON):
{
  "abweichungs_nr": "{{ $json.newQaId }}",
  "datum": "{{ new Date().toISOString().split('T')[0] }}",
  "lieferant_firma": "{{ $json.fromName || 'Unbekannt' }}",
  "lieferant_ansprechpartner": "{{ $json.from }}",
  "lieferant_email": "{{ $json.from }}",
  "artikel_nr_schneider": "",
  "artikel_bezeichnung": "{{ $json.subject }}",
  "lieferschein_nr": "",
  "lieferdatum": "",
  "liefermenge": "",
  "beanstandungsmenge": "",
  "beschreibung": "{{ $json.bodyPreview }}",
  "massnahmen": ["untersuchung_abstellen"],
  "ersteller": "System"
}
```

**Nächster Node:** "PDF nach SharePoint"

```javascript
// Type: HTTP Request
// Method: PUT
// URL: https://graph.microsoft.com/v1.0/drives/{{ $('Drive-ID').item.json.id }}/root:/Reklamationen/{{ $json.jahr }}/{{ $json.qaId }}/Dokumente/{{ $json.filename }}:/content
// Credential: Microsoft OAuth2
// Body: Binary (PDF File Content)
```

---

## 🎯 PHASE 5: Schriftverkehr-Eintrag

### SharePoint-Liste: RMS-Schriftverkehr

**Liste-ID:** `741c6ae8-88bb-406b-bf85-2e11192a528f`

**Spalten (aus vorhandener Struktur):**
| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | Betreff/Titel |
| QA_IDLookupId | Lookup | Verknüpfung zur Reklamation (Item-ID!) |
| Datum | DateTime | Datum des Eintrags |
| Typ | Choice | E-Mail Eingang, E-Mail Ausgang, Telefonat, Brief, Fax |
| Absender | Text | Name + E-Mail |
| Betreff | Text | Original-Betreff |
| Inhalt | Note | Zusammenfassung (max. 500 Zeichen) |
| Richtung | Choice | Eingehend, Ausgehend |

### n8n Node: "Schriftverkehr erstellen"

**Position:** Nach Node 12 (Ins Archiv) - parallel möglich

```javascript
// Type: HTTP Request
// Method: POST
// URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/lists/741c6ae8-88bb-406b-bf85-2e11192a528f/items
// Credential: Microsoft OAuth2
// Headers: Content-Type: application/json

// Body:
{
  "fields": {
    "Title": "{{ $json.subject.substring(0, 250) }}",
    "QA_IDLookupId": {{ $json.reklaItemId }},
    "Datum": "{{ $json.receivedDateTime }}",
    "Typ": "E-Mail Eingang",
    "Absender": "{{ $json.fromName }} ({{ $json.from }})",
    "Betreff": "{{ $json.subject }}",
    "Inhalt": "{{ $json.bodyPreview ? $json.bodyPreview.substring(0, 500) : '' }}",
    "Richtung": "Eingehend"
  }
}
```

### WICHTIG: Lookup-ID

Die `QA_IDLookupId` muss die **SharePoint Item-ID** sein, NICHT die QA-ID!

**Sicherstellen:** Nach dem Erstellen/Finden der Reklamation die Item-ID speichern:

```javascript
// Im Workflow nach "9. Reklamation erstellen" 
// oder nach "7a. Rekla suchen":

// Die Response enthält:
{
  "id": "123",  // <-- Das ist die SharePoint Item-ID für den Lookup
  "fields": {
    "QA_ID": "QA-26001",
    ...
  }
}

// Diese ID als reklaItemId weitergeben
```

### Aufgaben Phase 5

```bash
# 1. SharePoint-Liste prüfen (Spalten verifizieren)
# Manuell in SharePoint prüfen oder via Graph API:
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/.../lists/741c6ae8-88bb-406b-bf85-2e11192a528f/columns"

# 2. n8n Workflow erweitern
# - Node "Schriftverkehr erstellen" hinzufügen
# - Position: Nach "Ins Archiv" oder parallel
# - Credential: Microsoft account

# 3. Test durchführen
# - Test-E-Mail senden
# - Workflow ausführen
# - Prüfen: Schriftverkehr-Eintrag in SharePoint Liste?
```

---

## ZUSAMMENFASSUNG

### Phase 3: PDF-Generierung
| # | Aufgabe | Status |
|---|---------|--------|
| 1 | WeasyPrint + Jinja2 installieren | ERLEDIGT (2026-01-27) |
| 2 | Verzeichnisse erstellen | ERLEDIGT (2026-01-27) |
| 3 | HTML-Template erstellen | ERLEDIGT (2026-01-27) |
| 4 | Python PDF-Generator Script | ERLEDIGT (2026-01-27) |
| 5 | Systemd Service einrichten | ERLEDIGT (2026-01-27) |
| 6 | Service starten und testen | ERLEDIGT (2026-01-27) |
| 7 | n8n Node "PDF generieren" | ERLEDIGT (2026-01-27) |
| 8 | n8n Node "PDF nach SharePoint" | ERLEDIGT (2026-01-27) |
| 9 | End-to-End Test | MANUELL |

### Phase 5: Schriftverkehr
| # | Aufgabe | Status |
|---|---------|--------|
| 1 | SharePoint-Liste pruefen | ERLEDIGT (2026-01-27) |
| 2 | n8n Node "Schriftverkehr erstellen" | ERLEDIGT (2026-01-27) |
| 3 | Lookup-ID Mapping pruefen | ERLEDIGT (2026-01-27) |
| 4 | Test durchfuehren | MANUELL |

---

## ERGEBNIS (2026-01-27)

**Neue Nodes im RMS-Email-Import-V2 Workflow (ID: k3rVSLW6O00dtTBr):**
- 16. Schriftverkehr erstellen (Phase 5)
- 17. PDF generieren (Phase 3)
- 18. PDF vorbereiten (Phase 3)
- 19. PDF nach SharePoint (Phase 3)

**Neue Services:**
- rms-pdf-generator.service (Port 5001)

**Neue Scripts:**
- /opt/osp/scripts/add_schriftverkehr_node.py
- /opt/osp/scripts/add_pdf_nodes.py
- /opt/osp/scripts/rms_pdf_generator.py

**Workflow hat jetzt 28 Nodes.**

---

## 📚 REFERENZEN

| Resource | Wert |
|----------|------|
| n8n API | http://127.0.0.1:5678 |
| PDF Generator | http://localhost:5001 |
| Microsoft Credential ID | Fm3IuAbVYBYDIA4U |
| RMS-Reklamationen Liste | e9b1d926-085a-4435-a012-114ca9ba59a8 |
| RMS-Schriftverkehr Liste | 741c6ae8-88bb-406b-bf85-2e11192a528f |
| RMS-Config Liste | f89562e1-e566-42d7-a58b-917b739c3a38 |
| F-QM-02 Dateien | /mnt/HC_Volume_104189729/osp/rms/formulare/f_qm_02_qualitaetsabweichung/ |

---

## ⚡ EMPFOHLENE REIHENFOLGE

1. **Phase 5 zuerst** (einfacher - nur n8n Node)
2. **Phase 3 danach** (PDF-Generator Setup erforderlich)

Starte mit Phase 5!
