# Claude Code Prompt: RMS Finalisierung - PDF-Workflow & Schriftverkehr

**Datum:** 2026-01-28  
**Status:** LibreOffice ✅, openpyxl ✅, SharePoint-Templates ✅  
**Ziel:** PDF-Generierung funktionsfähig machen + Schriftverkehr fixen

---

## 📊 AKTUELLER STATUS

### ✅ Bereits erledigt
- LibreOffice installiert (libreoffice-calc, libreoffice-writer 4:24.2.7)
- openpyxl installiert (3.1.5)
- XLSX-Templates in SharePoint hochgeladen:
  - `/Formular-Vorlagen/f_qm_02_qualitaetsabweichung/FQM02_Qualitaetsabweichung.xlsx`
  - `/Formular-Vorlagen/f_qm_03_8D_Report/FQM03_8D_Report.xlsx`
  - `/Formular-Vorlagen/f_qm_04_nza/FQM04_NZA.xlsx`
  - `/Formular-Vorlagen/f_qm_14_korrekturmassnahme/FQM14_Korrekturmassnahmen.xlsx`
- n8n Workflow RMS-Generate-Formblatt existiert (ID: MN63eCmmUDHzED8G) - Platzhalter

### 🔴 Heute noch umzusetzen
1. **fill_xlsx_form.py** Script vervollständigen
2. **n8n Workflow** RMS-Generate-Formblatt finalisieren
3. **Schriftverkehr** Lookup-Problem beheben
4. **Test** Ende-zu-Ende PDF-Generierung

---

## 🔧 UMGEBUNG

```bash
# Server
IP: 46.224.102.30
User: root

# API
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMGFkYS1mMGU5NTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM4MDQxNDQxfQ.Hhqnbitgd-ak_iZruZy1Z_rdHJ75BtcYfv09RO05Rtg"
export N8N_BASE_URL="http://127.0.0.1:5678"

# SharePoint
SITE_ID="rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"
CREDENTIAL_ID="Fm3IuAbVYBYDIA4U"

# Pfade
SCRIPTS_DIR="/opt/osp/scripts"
TEMP_DIR="/tmp/rms-forms"

# Bestehende Workflows
RMS_GENERATE_FORMBLATT="MN63eCmmUDHzED8G"
RMS_DETAIL_API="5jruolIhqcOGu3GQ"
```

---

## AUFGABE 1: fill_xlsx_form.py Script erstellen

Erstelle `/opt/osp/scripts/fill_xlsx_form.py`:

```python
#!/usr/bin/env python3
"""
RMS Formular-Befüller
Befüllt XLSX-Templates mit Reklamationsdaten

Verwendung:
    python3 fill_xlsx_form.py template.xlsx output.xlsx --data '{"field": "value"}'
    python3 fill_xlsx_form.py template.xlsx --analyze  # Zeigt verfügbare Felder
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from openpyxl import load_workbook
    from openpyxl.styles import Font, PatternFill
except ImportError:
    print("ERROR: openpyxl nicht installiert. Bitte ausführen:")
    print("  pip install openpyxl --break-system-packages")
    sys.exit(1)


# Feld-Mappings für verschiedene Formulare
FIELD_MAPPINGS = {
    "F_QM_02": {
        # Zelle: Datenfeld
        "I1": "abweichungs_nr",      # QA-ID
        "I3": "datum",                # Datum
        "A17": "lieferant_firma",     # Lieferant Firma (merged A17:E19)
        "E23": "artikel_nr_schneider",
        "E24": "artikel_nr_lieferant",
        "E25": "artikel_bezeichnung",
        "E26": "lieferschein_nr",
        "E27": "lieferdatum",
        "E28": "liefermenge",
        "E29": "beanstandungsmenge",
        "A33": "beschreibung",        # Beschreibung (merged A33:I42)
        # Checkboxen (als Text "☑" oder "☐")
        "A47": "cb_untersuchung_abstellen",
        "A48": "cb_untersuchung_8d",
        "A49": "cb_ersatzlieferung",
        "A50": "cb_ruecksendung",
        "A51": "cb_gutschrift",
        "A52": "cb_sonstiges",
        # Unterschrift
        "B56": "ersteller",
        "F56": "datum_unterschrift"
    },
    "F_QM_03": {
        "D3": "qa_id",
        "D4": "kunde",
        "D5": "artikel",
        "D6": "datum_reklamation",
        "B10": "d1_team",
        "B14": "d2_problembeschreibung",
        "B18": "d3_sofortmassnahme",
        "B22": "d4_ursachenanalyse",
        "B26": "d5_korrekturmassnahmen",
        "B30": "d6_wirksamkeit",
        "B34": "d7_vorbeugung",
        "B38": "d8_abschluss",
        "D40": "ersteller",
        "H40": "datum_abschluss"
    },
    "F_QM_04": {
        "D3": "nza_nr",
        "D4": "datum",
        "D5": "auftrag",
        "D6": "artikel",
        "B10": "fehler_beschreibung",
        "B14": "ursache",
        "B18": "massnahme",
        "D22": "aufwand_minuten",
        "D23": "kosten",
        "D26": "ersteller"
    },
    "F_QM_14": {
        "D3": "km_nr",
        "D4": "datum",
        "D5": "bezug_reklamation",
        "B10": "abweichung",
        "B14": "ursache",
        "B18": "korrekturmassnahme",
        "B22": "vorbeugung",
        "D26": "termin",
        "D27": "verantwortlich",
        "D30": "wirksamkeit_geprueft",
        "D31": "wirksamkeit_datum",
        "D34": "ersteller"
    }
}


def detect_form_type(filepath: str) -> str:
    """Erkennt Formulartyp aus Dateinamen"""
    filename = Path(filepath).stem.upper()
    
    if "QM02" in filename or "QM_02" in filename:
        return "F_QM_02"
    elif "QM03" in filename or "QM_03" in filename or "8D" in filename:
        return "F_QM_03"
    elif "QM04" in filename or "QM_04" in filename or "NZA" in filename:
        return "F_QM_04"
    elif "QM14" in filename or "QM_14" in filename or "KORREKTUR" in filename:
        return "F_QM_14"
    
    return None


def analyze_workbook(filepath: str):
    """Analysiert ein Workbook und zeigt Zellen mit Inhalt"""
    wb = load_workbook(filepath)
    
    print(f"\n📊 Analyse: {filepath}")
    print(f"   Sheets: {wb.sheetnames}")
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        print(f"\n   Sheet: {sheet_name}")
        print(f"   Dimensionen: {ws.dimensions}")
        
        # Zeige Zellen mit Inhalt
        cells_with_content = []
        for row in ws.iter_rows(max_row=60, max_col=10):
            for cell in row:
                if cell.value:
                    cells_with_content.append(f"   {cell.coordinate}: {str(cell.value)[:50]}")
        
        print(f"   Zellen mit Inhalt ({len(cells_with_content)}):")
        for c in cells_with_content[:20]:
            print(c)
        if len(cells_with_content) > 20:
            print(f"   ... und {len(cells_with_content) - 20} weitere")
    
    wb.close()


def fill_workbook(template_path: str, output_path: str, data: dict, form_type: str = None):
    """Befüllt ein XLSX-Template mit Daten"""
    
    # Formulartyp erkennen
    if not form_type:
        form_type = detect_form_type(template_path)
    
    if not form_type or form_type not in FIELD_MAPPINGS:
        print(f"⚠️  Unbekannter Formulartyp. Verwende generisches Mapping.")
        # Generisches Mapping: Daten direkt in angegebene Zellen
        mapping = {k: k for k in data.keys() if len(k) <= 4}  # Nur Zell-Referenzen
    else:
        mapping = FIELD_MAPPINGS[form_type]
        print(f"✅ Formulartyp erkannt: {form_type}")
    
    # Template laden
    wb = load_workbook(template_path)
    ws = wb.active
    
    # Invertiertes Mapping: Datenfeld -> Zelle
    field_to_cell = {v: k for k, v in mapping.items()}
    
    filled_count = 0
    
    for field, value in data.items():
        if value is None or value == "":
            continue
            
        # Zelle finden
        cell_ref = field_to_cell.get(field)
        
        if not cell_ref:
            # Vielleicht ist field direkt eine Zell-Referenz (z.B. "A1")
            if len(field) <= 4 and field[0].isalpha():
                cell_ref = field
            else:
                print(f"   ⚠️  Kein Mapping für Feld: {field}")
                continue
        
        try:
            # Checkbox-Handling
            if field.startswith("cb_"):
                ws[cell_ref] = "☑" if value in [True, "true", "1", "ja", "yes", "☑"] else "☐"
            else:
                ws[cell_ref] = str(value)
            
            filled_count += 1
            print(f"   ✅ {cell_ref} = {str(value)[:30]}")
            
        except Exception as e:
            print(f"   ❌ Fehler bei {cell_ref}: {e}")
    
    # Speichern
    wb.save(output_path)
    wb.close()
    
    print(f"\n✅ {filled_count} Felder befüllt")
    print(f"   Ausgabe: {output_path}")
    
    return filled_count > 0


def main():
    parser = argparse.ArgumentParser(description="RMS Formular-Befüller")
    parser.add_argument("template", help="Pfad zum XLSX-Template")
    parser.add_argument("output", nargs="?", help="Pfad zur Ausgabedatei")
    parser.add_argument("--data", "-d", help="JSON-String mit Felddaten")
    parser.add_argument("--data-file", "-f", help="JSON-Datei mit Felddaten")
    parser.add_argument("--analyze", "-a", action="store_true", help="Template analysieren")
    parser.add_argument("--form-type", "-t", help="Formulartyp (F_QM_02, F_QM_03, etc.)")
    
    args = parser.parse_args()
    
    # Template prüfen
    if not Path(args.template).exists():
        print(f"❌ Template nicht gefunden: {args.template}")
        sys.exit(1)
    
    # Analyse-Modus
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
    
    # Output-Pfad
    if not args.output:
        template_path = Path(args.template)
        args.output = str(template_path.parent / f"filled_{template_path.name}")
    
    # Befüllen
    success = fill_workbook(args.template, args.output, data, args.form_type)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

**Ausführbar machen:**
```bash
chmod +x /opt/osp/scripts/fill_xlsx_form.py
```

**Test:**
```bash
# Analyse
python3 /opt/osp/scripts/fill_xlsx_form.py /tmp/test_template.xlsx --analyze

# Befüllen
python3 /opt/osp/scripts/fill_xlsx_form.py \
    /tmp/FQM02_Qualitaetsabweichung.xlsx \
    /tmp/filled_QA-26013.xlsx \
    --data '{"abweichungs_nr": "QA-26013", "datum": "2026-01-28", "lieferant_firma": "Test GmbH"}'
```

---

## AUFGABE 2: convert_to_pdf.py Script erstellen

Erstelle `/opt/osp/scripts/convert_to_pdf.py`:

```python
#!/usr/bin/env python3
"""
Konvertiert XLSX/DOCX zu PDF mit LibreOffice Headless

Verwendung:
    python3 convert_to_pdf.py input.xlsx output.pdf
    python3 convert_to_pdf.py input.xlsx  # Output: input.pdf
"""

import subprocess
import sys
import shutil
from pathlib import Path


def convert_to_pdf(input_path: str, output_path: str = None) -> str:
    """Konvertiert Dokument zu PDF"""
    
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {input_path}")
    
    # Output-Pfad bestimmen
    if output_path:
        output_file = Path(output_path)
        output_dir = output_file.parent
    else:
        output_dir = input_file.parent
        output_file = output_dir / f"{input_file.stem}.pdf"
    
    # LibreOffice Headless ausführen
    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(input_file)
    ]
    
    print(f"📄 Konvertiere: {input_file.name} → PDF")
    print(f"   Befehl: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"❌ LibreOffice Fehler: {result.stderr}")
            return None
        
        # LibreOffice erstellt PDF im outdir mit gleichem Basename
        generated_pdf = output_dir / f"{input_file.stem}.pdf"
        
        # Falls anderer Output-Name gewünscht, umbenennen
        if output_path and generated_pdf != output_file:
            shutil.move(str(generated_pdf), str(output_file))
        
        if output_file.exists():
            print(f"✅ PDF erstellt: {output_file}")
            print(f"   Größe: {output_file.stat().st_size / 1024:.1f} KB")
            return str(output_file)
        else:
            print(f"❌ PDF nicht erstellt")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout bei PDF-Konvertierung")
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

**Ausführbar machen:**
```bash
chmod +x /opt/osp/scripts/convert_to_pdf.py
```

**Test:**
```bash
python3 /opt/osp/scripts/convert_to_pdf.py /tmp/filled_QA-26013.xlsx /tmp/QA-26013.pdf
```

---

## AUFGABE 3: n8n Workflow RMS-Generate-Formblatt finalisieren

Aktualisiere den Workflow `MN63eCmmUDHzED8G`:

### Node 1: Webhook Trigger (existiert)
- Method: POST
- Path: `rms-generate-formblatt`

### Node 2: Prepare Variables (Code Node) - NEU
```javascript
const body = $json.body || $json;

// Formulartyp-Mapping
const formTypeMappings = {
    'F_QM_02': 'f_qm_02_qualitaetsabweichung/FQM02_Qualitaetsabweichung.xlsx',
    'F_QM_03': 'f_qm_03_8D_Report/FQM03_8D_Report.xlsx',
    'F_QM_04': 'f_qm_04_nza/FQM04_NZA.xlsx',
    'F_QM_14': 'f_qm_14_korrekturmassnahme/FQM14_Korrekturmassnahmen.xlsx'
};

const templatePath = formTypeMappings[body.formularTyp] || formTypeMappings['F_QM_02'];
const qaId = body.qaId || 'UNKNOWN';
const year = qaId.split('-')[1]?.substring(0, 2) || '26';
const fullYear = '20' + year;

// Daten für Formular aufbereiten
const reklaData = body.reklamationsDaten || {};
const formData = {
    abweichungs_nr: qaId,
    datum: new Date().toISOString().split('T')[0],
    lieferant_firma: reklaData.Absender || reklaData.Lieferant || '',
    artikel_bezeichnung: reklaData.Title || '',
    beschreibung: reklaData.Beschreibung || '',
    ersteller: body.ersteller || 'System',
    // Weitere Felder aus reklaData...
    ...reklaData
};

return {
    qaId,
    fullYear,
    formularTyp: body.formularTyp,
    templatePath,
    formData: JSON.stringify(formData),
    outputFilename: `${body.formularTyp}_${qaId}`
};
```

### Node 3: Download Template (HTTP Request)
```
Method: GET
URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/drive/root:/Formular-Vorlagen/{{ $json.templatePath }}:/content
Authentication: OAuth2 (Microsoft account)
Response Format: File
```

### Node 4: Save Template (Write Binary File)
```
File Name: /tmp/rms-forms/template_{{ $json.qaId }}.xlsx
```

### Node 5: Fill XLSX (Execute Command)
```bash
mkdir -p /tmp/rms-forms && \
python3 /opt/osp/scripts/fill_xlsx_form.py \
    "/tmp/rms-forms/template_{{ $('Prepare Variables').item.json.qaId }}.xlsx" \
    "/tmp/rms-forms/filled_{{ $('Prepare Variables').item.json.qaId }}.xlsx" \
    --data '{{ $('Prepare Variables').item.json.formData }}' \
    --form-type "{{ $('Prepare Variables').item.json.formularTyp }}"
```

### Node 6: Convert to PDF (Execute Command)
```bash
python3 /opt/osp/scripts/convert_to_pdf.py \
    "/tmp/rms-forms/filled_{{ $('Prepare Variables').item.json.qaId }}.xlsx" \
    "/tmp/rms-forms/{{ $('Prepare Variables').item.json.outputFilename }}.pdf"
```

### Node 7: Read PDF (Read Binary File)
```
File Path: /tmp/rms-forms/{{ $('Prepare Variables').item.json.outputFilename }}.pdf
```

### Node 8: Upload PDF to SharePoint (HTTP Request)
```
Method: PUT
URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/drive/root:/{{ $('Prepare Variables').item.json.fullYear }}/{{ $('Prepare Variables').item.json.qaId }}/{{ $('Prepare Variables').item.json.outputFilename }}.pdf:/content
Authentication: OAuth2
Body: Binary (from previous node)
Headers:
  Content-Type: application/pdf
```

### Node 9: Read XLSX (Read Binary File)
```
File Path: /tmp/rms-forms/filled_{{ $('Prepare Variables').item.json.qaId }}.xlsx
```

### Node 10: Upload XLSX to SharePoint (HTTP Request)
```
Method: PUT
URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/drive/root:/{{ $('Prepare Variables').item.json.fullYear }}/{{ $('Prepare Variables').item.json.qaId }}/{{ $('Prepare Variables').item.json.outputFilename }}.xlsx:/content
Authentication: OAuth2
Body: Binary (from Node 9)
```

### Node 11: Cleanup (Execute Command)
```bash
rm -f /tmp/rms-forms/*_{{ $('Prepare Variables').item.json.qaId }}.*
```

### Node 12: Response (Code Node)
```javascript
const vars = $('Prepare Variables').item.json;
const siteUrl = 'https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS';

return {
    success: true,
    qaId: vars.qaId,
    formularTyp: vars.formularTyp,
    pdfUrl: `${siteUrl}/Freigegebene%20Dokumente/${vars.fullYear}/${vars.qaId}/${vars.outputFilename}.pdf`,
    xlsxUrl: `${siteUrl}/Freigegebene%20Dokumente/${vars.fullYear}/${vars.qaId}/${vars.outputFilename}.xlsx`,
    message: `${vars.formularTyp} erfolgreich erstellt`
};
```

### Node 13: Respond to Webhook

**Connections:**
```
Webhook → Prepare Variables → Download Template → Save Template → Fill XLSX → Convert to PDF → Read PDF → Upload PDF → Read XLSX → Upload XLSX → Cleanup → Response → Respond
```

---

## AUFGABE 4: Schriftverkehr-Lookup prüfen/fixen

### 4.1 Prüfen ob Lookup-Spalte korrekt konfiguriert ist

Die Schriftverkehr-Liste hat eine Lookup-Spalte `QA_IDLookupId` die auf die Reklamationen-Liste verweist.

**Problem:** Der Filter `fields/QA_IDLookupId eq {id}` funktioniert möglicherweise nicht.

**Lösung 1: OData-Filter anpassen**

Im RMS-Detail-API Workflow (5jruolIhqcOGu3GQ) den Schriftverkehr-Node anpassen:

```
URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/lists/741c6ae8-88bb-406b-bf85-2e11192a528f/items?$expand=fields&$filter=fields/QA_IDLookupId eq {{ $json.query.id }}
Headers: 
  Prefer: HonorNonIndexedQueriesWarningMayFailRandomly
```

**Lösung 2: Alle laden und clientseitig filtern**

Falls OData-Filter nicht funktioniert, alle Einträge laden und im Code-Node filtern:

```javascript
// Im Merge Results Node
const svItems = $('Schriftverkehr laden').item.json.value || [];
const reklaId = parseInt($json.query.id);

const filteredSV = svItems.filter(item => {
    const lookupId = item.fields?.QA_IDLookupId;
    return lookupId === reklaId || lookupId === String(reklaId);
});

return {
    // ...
    schriftverkehr: filteredSV.map(s => s.fields)
};
```

### 4.2 Schriftverkehr-Liste Spalten prüfen

Prüfe in SharePoint ob diese Spalten existieren:
- `QA_IDLookupId` (Lookup auf Reklamationen)
- `Datum`
- `Typ` (Choice: E-Mail Eingang, E-Mail Ausgang, Telefonat, Brief)
- `Betreff`
- `Richtung` (Choice: Eingehend, Ausgehend)

---

## AUFGABE 5: Temp-Verzeichnis erstellen

```bash
mkdir -p /tmp/rms-forms
chmod 777 /tmp/rms-forms
```

---

## ✅ CHECKLISTE

Nach Abschluss prüfen:

### Scripts
- [ ] `/opt/osp/scripts/fill_xlsx_form.py` erstellt und ausführbar
- [ ] `/opt/osp/scripts/convert_to_pdf.py` erstellt und ausführbar
- [ ] Test: `python3 fill_xlsx_form.py --analyze /tmp/test.xlsx`
- [ ] Test: `python3 convert_to_pdf.py /tmp/test.xlsx`

### n8n Workflow
- [ ] RMS-Generate-Formblatt Workflow aktualisiert
- [ ] Alle Nodes korrekt verbunden
- [ ] Workflow aktiviert

### Ende-zu-Ende Test
- [ ] Dashboard öffnen
- [ ] Reklamation auswählen
- [ ] "PDF erstellen" klicken
- [ ] Formular-Typ wählen (z.B. F-QM-02)
- [ ] PDF wird in SharePoint erstellt
- [ ] PDF erscheint in Dokumente-Sektion

### Schriftverkehr
- [ ] Schriftverkehr wird im Detail-Modal angezeigt
- [ ] Lookup funktioniert

---

## 📚 REFERENZEN

| Resource | Wert |
|----------|------|
| Dashboard | https://osp.schneider-kabelsatzbau.de/rms/ |
| n8n | http://46.224.102.30:5678 |
| SharePoint Templates | /Formular-Vorlagen/ |
| Scripts | /opt/osp/scripts/ |
| Temp | /tmp/rms-forms/ |
| Workflow ID | MN63eCmmUDHzED8G |

---

## 🔧 TROUBLESHOOTING

### LibreOffice Fehler
```bash
# Test ob LibreOffice funktioniert
libreoffice --headless --version

# Falls "no display" Fehler
export HOME=/tmp
libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.xlsx
```

### Berechtigungsfehler
```bash
chown -R root:root /opt/osp/scripts/
chmod +x /opt/osp/scripts/*.py
```

### SharePoint Upload Fehler
- Prüfen ob Ordner `/2026/QA-XXXXX/` existiert
- Falls nicht, muss der Ordner zuerst erstellt werden (siehe RMS-Ordner-Sync Workflow)

---

*Erstellt: 2026-01-28 | Ziel: PDF-Generierung funktionsfähig*
