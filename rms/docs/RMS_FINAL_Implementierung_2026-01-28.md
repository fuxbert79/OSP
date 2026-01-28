# RMS Finalisierung - Implementierungsbericht

**Datum:** 2026-01-28
**Status:** ✅ ERFOLGREICH
**Autor:** Claude Code

---

## Zusammenfassung

Die RMS PDF-Generierung und der Schriftverkehr-Lookup wurden erfolgreich implementiert und getestet.

### Test-Ergebnis PDF-Generierung

```json
{
  "success": true,
  "qaId": "QA-26013",
  "formularTyp": "F_QM_02",
  "pdfUrl": "https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS/Freigegebene%20Dokumente/2026/QA-26013/F_QM_02_QA-26013.pdf",
  "xlsxUrl": "https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS/Freigegebene%20Dokumente/2026/QA-26013/F_QM_02_QA-26013.xlsx",
  "message": "F_QM_02 erfolgreich erstellt"
}
```

---

## Implementierte Komponenten

### 1. Python Scripts

| Script | Pfad | Funktion |
|--------|------|----------|
| fill_xlsx_form.py | /opt/osp/scripts/fill_xlsx_form.py | XLSX-Template mit Daten befuellen |
| convert_to_pdf.py | /opt/osp/scripts/convert_to_pdf.py | XLSX zu PDF konvertieren (LibreOffice) |
| formblatt_service.py | /opt/osp/scripts/formblatt_service.py | HTTP-Service fuer PDF-Generierung |

### 2. Systemd Service

```bash
# Service-Datei
/etc/systemd/system/formblatt-service.service

# Status
systemctl status formblatt-service

# Befehle
systemctl start formblatt-service
systemctl stop formblatt-service
systemctl restart formblatt-service
```

**Konfiguration:**
- Port: 5050
- Host: 0.0.0.0 (alle Interfaces)
- Endpoints: /health, /fill-xlsx, /convert-pdf, /generate

### 3. UFW Firewall-Regel

```bash
# Hinzugefuegt fuer Docker-Zugriff
ufw allow from 172.19.0.0/16 to any port 5050 comment "Formblatt-Service fuer Docker"
```

### 4. n8n Workflows aktualisiert

#### RMS-Generate-Formblatt (MN63eCmmUDHzED8G)

**Nodes:**
1. Webhook (POST /webhook/rms-generate-formblatt)
2. Prepare Variables - Formular-Mapping
3. Download Template - SharePoint Graph API
4. Prepare Service Call - Binary zu Base64 konvertieren
5. Generate PDF - HTTP Request an Formblatt-Service
6. Prepare Upload - Daten fuer SharePoint aufbereiten
7. Upload PDF - SharePoint Graph API PUT
8. Upload XLSX - SharePoint Graph API PUT
9. Response - Erfolgs-JSON erstellen
10. Respond to Webhook

**Kritische Korrektur im "Prepare Service Call" Node:**
```javascript
// In n8n werden Binary-Daten im Dateisystem gespeichert (filesystem-v2)
// Daher muss getBinaryDataBuffer verwendet werden
const binaryBuffer = await this.helpers.getBinaryDataBuffer(0, binaryKey);
const templateBase64 = binaryBuffer.toString('base64');
```

#### RMS-Detail-API (5jruolIhqcOGu3GQ)

**Erweiterungen:**
- Massnahmen laden (Liste: 3768f2d8-878c-4a5f-bd52-7486fe93289d)
- Schriftverkehr laden (Liste: 741c6ae8-88bb-406b-bf85-2e11192a528f)
- Sequentielle Verarbeitung mit Zwischenspeicherung

**Nodes:**
1. Webhook (GET /webhook/rms-detail)
2. Load Reklamation
3. Store Reklamation
4. Load Massnahmen (mit OData-Filter)
5. Store Massnahmen
6. Load Schriftverkehr (mit OData-Filter)
7. Build Response
8. Respond to Webhook

---

## Behobene Probleme

### 1. n8n-Docker kann Host nicht erreichen

**Problem:** Docker-Container konnte Port 5050 auf dem Host nicht erreichen.

**Ursache:** UFW Firewall blockierte Verbindungen vom Docker-Subnet.

**Loesung:**
```bash
ufw allow from 172.19.0.0/16 to any port 5050
```

### 2. Binary-Daten nicht als Base64 verfuegbar

**Problem:** n8n speichert Binary-Daten im Dateisystem (`filesystem-v2`), nicht inline.

**Ursache:** Neuere n8n-Versionen verwenden Dateisystem-Speicher fuer Binary-Daten.

**Loesung:**
```javascript
const binaryBuffer = await this.helpers.getBinaryDataBuffer(0, binaryKey);
const templateBase64 = binaryBuffer.toString('base64');
```

### 3. Webhook responseMode falsch

**Problem:** Workflows gaben Fehler "Unused Respond to Webhook node".

**Ursache:** `responseMode: "lastNode"` funktioniert nicht mit "Respond to Webhook" Node.

**Loesung:** `responseMode: "responseNode"` verwenden.

---

## API-Dokumentation

### POST /api/rms/generate-formblatt

Generiert ein ausgefuelltes QM-Formblatt als PDF.

**Request:**
```json
{
  "qaId": "QA-26013",
  "formularTyp": "F_QM_02",
  "reklamationsDaten": {
    "Absender": "Lieferant GmbH",
    "Title": "Reklamationstitel",
    "Beschreibung": "Beschreibungstext"
  },
  "ersteller": "AL"
}
```

**Unterstuetzte Formulartypen:**
- `F_QM_02` - Qualitaetsabweichung (Lieferantenreklamation)
- `F_QM_03` - 8D-Report
- `F_QM_04` - Nach-/Zusatzarbeiten
- `F_QM_14` - Korrekturmassnahme

**Response:**
```json
{
  "success": true,
  "qaId": "QA-26013",
  "formularTyp": "F_QM_02",
  "pdfUrl": "https://...sharepoint.com/.../F_QM_02_QA-26013.pdf",
  "xlsxUrl": "https://...sharepoint.com/.../F_QM_02_QA-26013.xlsx",
  "message": "F_QM_02 erfolgreich erstellt"
}
```

### GET /api/rms/detail?id={id}

Laedt Reklamationsdetails inkl. Massnahmen und Schriftverkehr.

**Response:**
```json
{
  "reklamation": { "QA_ID": "...", "Title": "...", ... },
  "massnahmen": [{ "Title": "...", "Massnahme_Typ": "...", ... }],
  "schriftverkehr": [{ "Datum": "...", "Typ": "...", ... }],
  "sharePointUrl": "https://..."
}
```

---

## SharePoint-Konfiguration

### Listen-IDs

| Liste | ID |
|-------|-----|
| Reklamationen | e9b1d926-085a-4435-a012-114ca9ba59a8 |
| Massnahmen | 3768f2d8-878c-4a5f-bd52-7486fe93289d |
| Schriftverkehr | 741c6ae8-88bb-406b-bf85-2e11192a528f |

### Template-Pfade in SharePoint

```
/sites/RMS/Freigegebene Dokumente/Formular-Vorlagen/
├── f_qm_02_qualitaetsabweichung/
│   └── FQM02_Qualitaetsabweichung.xlsx
├── f_qm_03_8D_Report/
│   └── FQM03_8D_Report.xlsx
├── f_qm_04_nza/
│   └── FQM04_NZA.xlsx
└── f_qm_14_korrekturmassnahme/
    └── FQM14_Korrekturmassnahmen.xlsx
```

### Output-Pfade

```
/sites/RMS/Freigegebene Dokumente/{JJJJ}/{QA-ID}/
├── F_QM_02_{QA-ID}.pdf
└── F_QM_02_{QA-ID}.xlsx
```

---

## Technische Details

### Server-Architektur

```
                                  ┌─────────────────┐
                                  │   SharePoint    │
                                  │  Graph API      │
                                  └────────┬────────┘
                                           │
┌─────────┐    ┌─────────┐    ┌────────────┴──────────────┐
│ Browser │────│  nginx  │────│          n8n              │
└─────────┘    │ :443    │    │ (Docker: osp-network)     │
               └─────────┘    └────────────┬──────────────┘
                                           │ HTTP :5050
                                           │ via 172.19.0.1
                              ┌────────────┴──────────────┐
                              │   formblatt-service.py    │
                              │   (systemd service)       │
                              │                           │
                              │  ┌───────────────────┐    │
                              │  │ fill_xlsx_form.py │    │
                              │  │ convert_to_pdf.py │    │
                              │  │ (openpyxl)        │    │
                              │  │ (LibreOffice)     │    │
                              │  └───────────────────┘    │
                              └───────────────────────────┘
```

### Versionen

| Komponente | Version |
|------------|---------|
| LibreOffice | 24.2.7.2 |
| openpyxl | 3.1.5 |
| n8n | latest (Docker) |
| Python | 3.12 |

---

## Checkliste

- [x] Scripts erstellt (fill_xlsx_form.py, convert_to_pdf.py, formblatt_service.py)
- [x] Systemd Service konfiguriert
- [x] UFW Firewall-Regel hinzugefuegt
- [x] RMS-Generate-Formblatt Workflow aktualisiert
- [x] RMS-Detail-API Workflow erweitert
- [x] PDF-Generierung getestet - ERFOLGREICH
- [x] Schriftverkehr-Lookup getestet - ERFOLGREICH

---

## Wartung

### Service neustarten
```bash
systemctl restart formblatt-service
```

### Logs pruefen
```bash
journalctl -u formblatt-service -f
```

### Workflow-Status in n8n pruefen
```bash
curl -s -H "X-N8N-API-KEY: $N8N_KEY" "http://127.0.0.1:5678/api/v1/workflows/MN63eCmmUDHzED8G"
```

---

*Erstellt: 2026-01-28 19:55 UTC*
*Getestet: PDF-Generierung und Schriftverkehr-Lookup funktionieren*
