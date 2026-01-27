# RMS Phase 3 & 5 - Implementierungsbericht

**Datum:** 2026-01-27
**Erstellt von:** Claude Code
**Verantwortlich:** AL (QM & KI-Manager)

---

## Inhaltsverzeichnis

1. [Uebersicht](#uebersicht)
2. [Phase 5: Schriftverkehr](#phase-5-schriftverkehr)
3. [Phase 3: PDF-Generierung](#phase-3-pdf-generierung)
4. [Workflow-Struktur](#workflow-struktur)
5. [Neue Dateien](#neue-dateien)
6. [Service-Konfiguration](#service-konfiguration)
7. [API-Dokumentation](#api-dokumentation)
8. [Test-Ergebnisse](#test-ergebnisse)
9. [Naechste Schritte](#naechste-schritte)

---

## Uebersicht

### Ausgangssituation

Der RMS-Email-Import-V2 Workflow (ID: `k3rVSLW6O00dtTBr`) hatte 25 Nodes und verarbeitete E-Mails aus dem Reklamations-Postfach. Phase 1 und 2 waren bereits implementiert:

- **Phase 1:** E-Mail-Import, QA-ID-Generierung, Reklamation erstellen
- **Phase 2:** Anhaenge laden, SharePoint Upload, Teams-Benachrichtigung

### Ziel

Erweiterung um:
- **Phase 5:** Schriftverkehr-Eintraege in SharePoint erstellen
- **Phase 3:** PDF-Generierung fuer F-QM-02 Formblatt

### Ergebnis

| Metrik | Vorher | Nachher |
|--------|--------|---------|
| Workflow Nodes | 25 | 28 |
| Neue Services | 0 | 1 (PDF-Generator) |
| Neue Scripts | 0 | 3 |

---

## Phase 5: Schriftverkehr

### Beschreibung

Automatische Erstellung von Schriftverkehr-Eintraegen in der SharePoint-Liste `RMS-Schriftverkehr` fuer jede eingehende E-Mail.

### SharePoint-Liste

| Parameter | Wert |
|-----------|------|
| Liste-ID | `741c6ae8-88bb-406b-bf85-2e11192a528f` |
| Site | rainerschneiderkabelsatz.sharepoint.com |

### Felder

| Spalte | Typ | Inhalt |
|--------|-----|--------|
| Title | Text | E-Mail Betreff (max 250 Zeichen) |
| QA_IDLookupId | Lookup | SharePoint Item-ID der Reklamation |
| Datum | DateTime | Empfangsdatum der E-Mail |
| Typ | Choice | "E-Mail Eingang" |
| Absender | Text | Name + E-Mail-Adresse |
| Betreff | Text | Original-Betreff |
| Inhalt | Note | Vorschau (max 500 Zeichen) |
| Richtung | Choice | "Eingehend" |

### Neuer Node

**Name:** 16. Schriftverkehr erstellen
**Typ:** HTTP Request
**Position:** Nach Node 12 (Ins Archiv), parallel zu Node 13 (Anhaenge laden)
**Credential:** Microsoft OAuth2 (ID: Fm3IuAbVYBYDIA4U)

### Implementierung

Script: `/opt/osp/scripts/add_schriftverkehr_node.py`

```python
# Kern-Logik des Nodes
{
  "fields": {
    "Title": "{{ E-Mail Betreff (max 250 Zeichen) }}",
    "QA_IDLookupId": {{ SharePoint Item-ID }},
    "Datum": "{{ receivedDateTime }}",
    "Typ": "E-Mail Eingang",
    "Absender": "{{ fromName }} ({{ from }})",
    "Betreff": "{{ subject }}",
    "Inhalt": "{{ bodyPreview (max 500 Zeichen) }}",
    "Richtung": "Eingehend"
  }
}
```

### Wichtiger Hinweis: Lookup-ID

Die `QA_IDLookupId` muss die **SharePoint Item-ID** sein, nicht die QA-ID!

```javascript
// Im Node wird die ID aus verschiedenen Quellen geholt:
QA_IDLookupId: $('9. Reklamation erstellen').item.json.id
            || $('7a. Rekla suchen').item.json.value[0].id
            || 0
```

---

## Phase 3: PDF-Generierung

### Beschreibung

Automatische Generierung von F-QM-02 Qualitaetsabweichungs-PDFs basierend auf dem vorhandenen JSON-Schema und HTML-Template.

### Komponenten

1. **PDF-Generator Service** (Port 5001)
2. **HTML-Template** fuer F-QM-02
3. **n8n Nodes** fuer Workflow-Integration

### PDF-Generator Service

#### Installation

```bash
# 1. Abhaengigkeiten installieren
pip install weasyprint jinja2 --break-system-packages

# 2. System-Bibliotheken (fuer WeasyPrint)
apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 \
                   libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# 3. Verzeichnisse erstellen
mkdir -p /opt/osp/templates /opt/osp/output /opt/osp/scripts
```

#### Dateien

| Datei | Pfad | Beschreibung |
|-------|------|--------------|
| PDF-Generator | `/opt/osp/scripts/rms_pdf_generator.py` | Python HTTP-Server |
| HTML-Template | `/opt/osp/templates/F_QM_02_template.html` | Jinja2 Template |
| Logo | `/opt/osp/templates/schneider_logo.svg` | Firmen-Logo (Platzhalter) |
| Systemd Service | `/etc/systemd/system/rms-pdf-generator.service` | Service-Definition |
| Output | `/opt/osp/output/` | Generierte PDFs |

#### Service-Befehle

```bash
# Service aktivieren und starten
systemctl daemon-reload
systemctl enable rms-pdf-generator
systemctl start rms-pdf-generator

# Status pruefen
systemctl status rms-pdf-generator

# Logs anzeigen
journalctl -u rms-pdf-generator -f

# Neustart
systemctl restart rms-pdf-generator
```

### HTML-Template

Das Template `/opt/osp/templates/F_QM_02_template.html` enthaelt:

- **Header:** Logo + Dokumenten-Info
- **Titel:** QUALITAETSABWEICHUNG / REKLAMATION
- **Absender:** Schneider Kabelsatzbau Kontaktdaten
- **Lieferant:** Dynamische Felder
- **Artikeldaten:** Tabelle mit allen relevanten Feldern
- **Beschreibung:** Freitext-Bereich
- **Massnahmen:** Checkbox-Liste (5 Optionen)
- **Unterschriften:** Ersteller + Datum
- **Footer:** Firmenadresse + ISO-Zertifizierung

### Neue n8n Nodes

#### Node 17: PDF generieren

**Typ:** HTTP Request (POST)
**URL:** `http://localhost:5001/generate-pdf`
**Position:** Nach Node 9 (Reklamation erstellen), parallel

**Request Body:**
```json
{
  "abweichungs_nr": "{{ QA-ID }}",
  "datum": "{{ aktuelles Datum }}",
  "lieferant_firma": "{{ Absender Name }}",
  "lieferant_email": "{{ Absender E-Mail }}",
  "artikel_bezeichnung": "{{ E-Mail Betreff }}",
  "beschreibung": "{{ E-Mail Vorschau }}",
  "massnahmen": ["untersuchung_abstellen"],
  "ersteller": "System",
  "return_base64": true
}
```

#### Node 18: PDF vorbereiten

**Typ:** Code
**Funktion:** Dekodiert Base64 und bereitet Daten fuer Upload vor

```javascript
const item = $input.item.json;

if (!item.success || !item.content_base64) {
  return { error: 'PDF-Generierung fehlgeschlagen', details: item };
}

const binaryData = Buffer.from(item.content_base64, 'base64');

return {
  filename: item.filename,
  filepath: item.filepath,
  binaryData: item.content_base64,
  contentLength: binaryData.length
};
```

#### Node 19: PDF nach SharePoint

**Typ:** HTTP Request (PUT)
**URL:** `https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drive/root:/Reklamationen/{Jahr}/{Monat}/{QA-ID}/Dokumente/{Dateiname}:/content`
**Credential:** Microsoft OAuth2

---

## Workflow-Struktur

### Aktueller Ablauf (28 Nodes)

```
1. Schedule (5 Min)
   |
2. E-Mails abrufen (Graph API)
   |
3. E-Mails vorhanden? --Nein--> Ende
   |Ja
4. E-Mail-Parser
   |
3a. Split E-Mails
   |
5. Spam? --Ja--> 5a. In Junk verschieben
   |Nein
6. QA-ID gefunden? --Nein--> 8b. QA-ID generieren
   |Ja
7a. Rekla suchen
7b. Config laden
   |
8a. Rekla existiert?
   |-- Ja --> 8a-TRUE. Daten mergen
   |-- Nein -> 8a-FALSE. Alte QA-ID
   |
9. Reklamation erstellen
   |
   +---------------------------+
   |                           |
   v                           v
10. Config updaten?      [PHASE 3]
   |                     17. PDF generieren
11. Als gelesen markieren    |
   |                     18. PDF vorbereiten
12. Ins Archiv               |
   |                     19. PDF nach SharePoint
   +-------------+
   |             |
   v             v
[PHASE 2]    [PHASE 5]
13. Anhaenge   16. Schriftverkehr
   |               erstellen
14. SharePoint Upload
   |
15. Teams Benachrichtigung
```

### Nodes mit Credentials

| Node | Credential | Phase |
|------|------------|-------|
| 2. E-Mails abrufen | Microsoft OAuth2 | 1 |
| 5a. In Junk verschieben | Microsoft OAuth2 | 1 |
| 7a. Rekla suchen | Microsoft OAuth2 | 1 |
| 7b. Config laden | Microsoft OAuth2 | 1 |
| 9. Reklamation erstellen | Microsoft OAuth2 | 1 |
| 10a. Config aktualisieren | Microsoft OAuth2 | 1 |
| 11. Als gelesen markieren | Microsoft OAuth2 | 1 |
| 12. Ins Archiv | Microsoft OAuth2 | 1 |
| 13. Anhaenge laden | Microsoft OAuth2 | 2 |
| 14. SharePoint Upload | Microsoft OAuth2 | 2 |
| 15. Teams Benachrichtigung | Microsoft OAuth2 | 2 |
| 16. Schriftverkehr erstellen | Microsoft OAuth2 | 5 |
| 17. PDF generieren | - (localhost) | 3 |
| 18. PDF vorbereiten | - (Code Node) | 3 |
| 19. PDF nach SharePoint | Microsoft OAuth2 | 3 |

---

## Neue Dateien

### Scripts

| Datei | Beschreibung |
|-------|--------------|
| `/opt/osp/scripts/add_schriftverkehr_node.py` | Fuegt Node 16 zum Workflow hinzu |
| `/opt/osp/scripts/add_pdf_nodes.py` | Fuegt Nodes 17-19 zum Workflow hinzu |
| `/opt/osp/scripts/rms_pdf_generator.py` | PDF-Generator HTTP-Server |

### Templates

| Datei | Beschreibung |
|-------|--------------|
| `/opt/osp/templates/F_QM_02_template.html` | Jinja2 HTML-Template fuer F-QM-02 |
| `/opt/osp/templates/schneider_logo.svg` | Firmen-Logo (Platzhalter) |

### Konfiguration

| Datei | Beschreibung |
|-------|--------------|
| `/etc/systemd/system/rms-pdf-generator.service` | Systemd Service Definition |

### Backups

| Verzeichnis | Beschreibung |
|-------------|--------------|
| `/opt/osp/backups/n8n_20260127_phase3_5/` | Backup aller Workflows nach Phase 3+5 |

---

## Service-Konfiguration

### rms-pdf-generator.service

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

StandardOutput=journal
StandardError=journal
SyslogIdentifier=rms-pdf-generator

[Install]
WantedBy=multi-user.target
```

### Umgebungsvariablen

| Variable | Wert | Beschreibung |
|----------|------|--------------|
| PDF_GENERATOR_PORT | 5001 | HTTP-Port des Services |
| N8N_API_KEY | (siehe Datenbank) | API-Key fuer n8n Management |

---

## API-Dokumentation

### PDF-Generator API (Port 5001)

#### GET /health

Status-Check des Services.

**Response:**
```json
{
  "status": "ok",
  "service": "RMS PDF Generator",
  "version": "1.0.0",
  "weasyprint": true,
  "schema_loaded": true,
  "template_dir": "/opt/osp/templates",
  "output_dir": "/opt/osp/output"
}
```

#### GET /schema

Gibt das JSON-Schema fuer F-QM-02 zurueck.

#### POST /validate

Validiert Formulardaten ohne PDF zu generieren.

**Request:**
```json
{
  "datum": "2026-01-27",
  "lieferant_firma": "Test GmbH",
  "artikel_nr_schneider": "12345",
  "artikel_bezeichnung": "Test-Artikel",
  "lieferschein_nr": "LS-001",
  "beschreibung": "Mindestens 50 Zeichen lange Beschreibung...",
  "massnahmen": ["ersatzlieferung"]
}
```

**Response:**
```json
{
  "valid": true,
  "errors": []
}
```

#### POST /generate-pdf

Generiert ein PDF aus den Formulardaten.

**Request:**
```json
{
  "abweichungs_nr": "QA-2026-001",
  "datum": "2026-01-27",
  "lieferant_firma": "Wuerth GmbH",
  "lieferant_ansprechpartner": "Max Mustermann",
  "lieferant_telefon": "+49 123 456789",
  "lieferant_email": "max@wuerth.de",
  "artikel_nr_schneider": "45789",
  "artikel_nr_lieferant": "WU-12345",
  "artikel_bezeichnung": "Stecker Typ B12",
  "lieferschein_nr": "LS-4578123",
  "lieferdatum": "2026-01-25",
  "liefermenge": "500 Stk",
  "beanstandungsmenge": "50 Stk",
  "beschreibung": "Bei der Wareneingangspruefung wurden 50 Stecker mit verbogenen Kontakten festgestellt...",
  "massnahmen": ["ersatzlieferung", "untersuchung_8d"],
  "ersteller": "AL",
  "return_base64": true
}
```

**Response:**
```json
{
  "success": true,
  "filepath": "/opt/osp/output/F-QM-02_QA-2026-001_20260127_211225.pdf",
  "filename": "F-QM-02_QA-2026-001_20260127_211225.pdf",
  "content_base64": "JVBERi0xLjQKJeLjz9MK..."
}
```

### Validierungsregeln

| Feld | Regel |
|------|-------|
| datum | Pflicht, Format YYYY-MM-DD |
| lieferant_firma | Pflicht |
| artikel_nr_schneider | Pflicht |
| artikel_bezeichnung | Pflicht |
| lieferschein_nr | Pflicht |
| beschreibung | Pflicht, min. 50 Zeichen |
| massnahmen | Pflicht, min. 1 Auswahl |
| abweichungs_nr | Optional, Format QA-YYYY-NNN |

---

## Test-Ergebnisse

### PDF-Generator Health Check

```bash
$ curl -s http://localhost:5001/health | python3 -m json.tool
{
    "status": "ok",
    "service": "RMS PDF Generator",
    "version": "1.0.0",
    "weasyprint": true,
    "schema_loaded": true,
    "template_dir": "/opt/osp/templates",
    "output_dir": "/opt/osp/output"
}
```

### Test-PDF Generierung

```bash
$ curl -s -X POST http://localhost:5001/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{...}' | python3 -m json.tool

{
    "success": true,
    "filepath": "/opt/osp/output/F-QM-02_QA-2026-001_20260127_211225.pdf",
    "filename": "F-QM-02_QA-2026-001_20260127_211225.pdf"
}

$ ls -la /opt/osp/output/
-rw-r--r-- 1 root root 23461 Jan 27 21:12 F-QM-02_QA-2026-001_20260127_211225.pdf
```

### Workflow-Verifizierung

```
$ python3 /opt/osp/scripts/n8n_workflow_manager.py show --id k3rVSLW6O00dtTBr

WORKFLOW: RMS-Email-Import-V2
   ID: k3rVSLW6O00dtTBr
   Aktiv: Ja

NODES IM WORKFLOW: 28
  - 1. Schedule (5 Min)
  - 2. E-Mails abrufen
  ...
  - 16. Schriftverkehr erstellen    [NEU - Phase 5]
  - 17. PDF generieren              [NEU - Phase 3]
  - 18. PDF vorbereiten             [NEU - Phase 3]
  - 19. PDF nach SharePoint         [NEU - Phase 3]
```

---

## Naechste Schritte

### Manuelle Tests erforderlich

1. **End-to-End Test Schriftverkehr:**
   - Test-E-Mail an reklamation@schneider-kabelsatzbau.de senden
   - Pruefen ob Schriftverkehr-Eintrag in SharePoint erstellt wird
   - QA_IDLookupId-Verknuepfung verifizieren

2. **End-to-End Test PDF:**
   - Workflow manuell ausloesen oder Test-E-Mail senden
   - Pruefen ob PDF generiert wird
   - Pruefen ob PDF in SharePoint hochgeladen wird
   - Pfad: `/Reklamationen/{Jahr}/{Monat}/{QA-ID}/Dokumente/`

3. **Logo ersetzen:**
   - Echtes Firmen-Logo als PNG bereitstellen
   - Pfad: `/opt/osp/templates/schneider_logo.png`
   - Template anpassen (SVG -> PNG)

### Bekannte Einschraenkungen

1. **PDF-Upload:** Der Upload verwendet Base64-Encoding, was bei grossen PDFs zu Performance-Problemen fuehren kann.

2. **Error Handling:** Bei Fehlern in den PDF-Nodes wird der Workflow fortgesetzt (onError: continueErrorOutput). Fehler sollten im RMS-Error-Handler ueberwacht werden.

3. **Schriftverkehr Lookup:** Die Lookup-Verknuepfung funktioniert nur, wenn die Reklamation zuvor erstellt wurde (Node 9) oder gefunden wurde (Node 7a).

### Empfehlungen

1. **Monitoring einrichten:** PDF-Generator Service in Monitoring aufnehmen
2. **Logs rotieren:** `/opt/osp/output/` regelmaessig bereinigen
3. **Backup-Strategie:** Workflow-Backups in regelmaessigen Abstaenden erstellen

---

## Referenzen

### IDs und URLs

| Ressource | Wert |
|-----------|------|
| n8n API | http://127.0.0.1:5678 |
| PDF Generator | http://localhost:5001 |
| Workflow ID | k3rVSLW6O00dtTBr |
| Microsoft Credential ID | Fm3IuAbVYBYDIA4U |
| SharePoint Site ID | rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c |
| Reklamations-Liste | e9b1d926-085a-4435-a012-114ca9ba59a8 |
| Schriftverkehr-Liste | 741c6ae8-88bb-406b-bf85-2e11192a528f |
| Config-Liste | f89562e1-e566-42d7-a58b-917b739c3a38 |

### Dokumentation

| Dokument | Pfad |
|----------|------|
| Workflow-Uebersicht | /opt/osp/docs/RMS_WORKFLOWS.md |
| Phase 3+5 Prompt | /mnt/HC_Volume_104189729/osp/prompts/RMS_Phase3.md |
| F-QM-02 Schema | /mnt/HC_Volume_104189729/osp/rms/formulare/f_qm_02_qualitaetsabweichung/F_QM_02_Schema.json |

---

*Erstellt: 2026-01-27 | Claude Code | Teil des OSP-Systems*
