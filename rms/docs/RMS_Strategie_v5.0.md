# 🚀 RMS ENTWICKLUNGS-STRATEGIE v5.0
## Reklamationsmanagementsystem - Rainer Schneider Kabelsatzbau

**Stand:** 2025-01-25  
**Go-Live MVP:** 31.01.2026  
**Go-Live Vollständig:** 07.02.2026  
**Verantwortlich:** AL (QM/KI-Manager)

---

## 📊 PROJEKT-PARAMETER

| Parameter | Wert |
|-----------|------|
| **Max. QA-Einträge/Jahr** | 150 |
| **Hauptnutzer (Dashboard)** | AL, TS, GF (CS, CA, SV) |
| **Dashboard-Nutzer** | ~54 (alle MA) |
| **Server** | Hetzner CX43 (8 vCPU, 32 GB RAM, 160 GB NVMe) |
| **SharePoint-Site** | ✅ `https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS` |
| **KI-Backend** | Claude API via anthropic-proxy (bestehend) |
| **KST-Zuordnung** | HR_CORE_Personalstamm.md (Referenz) |

---

## 🔄 ÄNDERUNGEN v4.1 → v5.0

| Aspekt | v4.1 (Alt) | v5.0 (Neu) | Begründung |
|--------|------------|------------|------------|
| **Frontend** | React 18 + shadcn/ui | **Alpine.js + TailwindCSS** | app-development Skill v2.0 |
| **Backend** | FastAPI + PostgreSQL | **FastAPI + SQLite** | Skill-konform, ausreichend für 150/Jahr |
| **Automation** | Power Automate + n8n | **n8n only** | osp-n8n-skill, einheitliche Plattform |
| **Formular-Workflow** | Markdown-Templates | **XLSX/DOCX → PDF** | osp-formular-skill v1.1 |
| **CI Orange** | Nicht definiert | **#DC500F** | CI-Update aus Skills |
| **Power Apps** | CRUD-Interface | **Entfällt** | Alpine.js Dashboard übernimmt |

---

## 🎯 FEATURE-ÜBERSICHT (AKTUALISIERT)

| Feature | Phase | Status | Technologie |
|---------|-------|--------|-------------|
| SharePoint Listen (5x) | MVP | ✅ FERTIG | SharePoint |
| FastAPI Backend + SQLite | MVP | ⏳ | Python 3.11 |
| Alpine.js Dashboard (KST-basiert) | MVP | ⏳ | Alpine.js + TailwindCSS |
| n8n: E-Mail-Import | MVP | ⏳ | n8n + Graph API |
| n8n: QA-ID Generator | MVP | ⏳ | n8n |
| n8n: Formblatt-Generator (Claude) | Phase 2 | ⏳ | n8n + anthropic-proxy |
| PDF-Export (weasyprint) | Phase 2 | ⏳ | weasyprint/LibreOffice |
| Dashboard-Charts (Chart.js) | Phase 2 | ⏳ | Chart.js |
| n8n: Maßnahmen-Alarm | Phase 2 | ⏳ | n8n + Outlook |
| Ähnliche Reklamationen (ChromaDB) | Phase 3 | ⏳ | ChromaDB |
| Teams-Integration | Phase 3 | ⏳ | Graph API |

---

## 🏗️ ARCHITEKTUR v5.0

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RMS v5.0 - SKILL-KONFORME ARCHITEKTUR            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ALLE NUTZER (~54)                                                   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              Alpine.js + TailwindCSS Dashboard                 │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │  │
│  │  │ KPI-Cards   │  │ Rekla-Liste │  │ Detail-Ansicht      │   │  │
│  │  │ (alle)      │  │ (KST-Filter)│  │ + Formblatt-Button  │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘   │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                               │ REST API                             │
│  ┌────────────────────────────▼──────────────────────────────────┐  │
│  │                    FastAPI Backend                             │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │  │
│  │  │ /reklamation │  │ /massnahmen  │  │ /formblatt       │    │  │
│  │  │ CRUD         │  │ CRUD         │  │ → n8n Webhook    │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘    │  │
│  │                          │                                     │  │
│  │                    ┌─────▼─────┐                               │  │
│  │                    │  SQLite   │                               │  │
│  │                    │  rms.db   │                               │  │
│  │                    └───────────┘                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                               │                                      │
│  ┌────────────────────────────▼──────────────────────────────────┐  │
│  │                    n8n Workflows                               │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │  │
│  │  │ E-Mail-Import│  │ QA-ID Gen    │  │ Formblatt-Gen    │    │  │
│  │  │ (Graph API)  │  │ (Counter)    │  │ (Claude + PDF)   │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                               │                                      │
│  ┌────────────────────────────▼──────────────────────────────────┐  │
│  │              SharePoint (Dokumente + Backup)                   │  │
│  │  Docs:   /2026/QA-26001/F_QM_02.pdf, Fotos, E-Mails           │  │
│  │  Listen: Backup-Sync (optional)                                │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  HETZNER CX43: Open WebUI + ChromaDB + n8n + anthropic-proxy + RMS  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 TECH-STACK (SKILL-KONFORM)

### Frontend (app-development Skill v2.0)

| Komponente | Technologie | Version |
|------------|-------------|---------|
| Framework | Alpine.js | 3.x |
| CSS | TailwindCSS | 3.x |
| Icons | Lucide Icons | Latest |
| Charts | Chart.js | 4.x |

### Backend (app-development Skill v2.0)

| Komponente | Technologie | Version |
|------------|-------------|---------|
| Framework | FastAPI | 0.109+ |
| ORM | SQLAlchemy | 2.0 |
| Datenbank | SQLite | 3.x |
| Validation | Pydantic | 2.x |

### Automation (osp-n8n-skill)

| Komponente | Technologie | Version |
|------------|-------------|---------|
| Workflow Engine | n8n | 1.123.6 |
| Microsoft 365 | Graph API | v1.0 |
| KI | Claude API | anthropic-proxy |
| PDF | weasyprint / LibreOffice | Latest |

### CI-Farben (VERBINDLICH)

```css
/* Primär */
--schneider-blau:       #003366;
--schneider-blau-hell:  #0080C9;
--schneider-orange:     #DC500F;  /* NEU aus CI-Update */

/* Neutral */
--schneider-grau:       #6B7280;
--schneider-weiss:      #FFFFFF;

/* Status */
--status-success:       #22C55E;
--status-warning:       #F59E0B;
--status-error:         #EF4444;
--status-info:          #3B82F6;

/* Fonts */
--font-headlines:       'Montserrat', sans-serif;
--font-body:            'Open Sans', sans-serif;

/* Radius */
--border-radius:        10px;
```

---

## 📋 SHAREPOINT-STRUKTUR (UNVERÄNDERT)

### Listen (5x) - ✅ BEREITS ERSTELLT

| Liste | Status | Felder (Auszug) |
|-------|--------|-----------------|
| **RMS-Reklamationen** | ✅ | QA_ID, Titel, Typ, Prio, Status, KST, Verantwortlich |
| **RMS-Maßnahmen** | ✅ | Rekla-Lookup, Typ, Termin, Status, Wirksamkeit |
| **RMS-Schriftverkehr** | ✅ | Rekla-Lookup, Datum, Richtung, Betreff, Outlook_ID |
| **RMS-KPIs** | ✅ | Datum, Offene, Kritische, Überfällige, Ø-Tage |
| **RMS-Config** | ✅ | Key, Value (CURRENT_YEAR=2026, Last_ID=1, etc.) |

### Dokumentstruktur

```
/sites/RMS/Freigegebene Dokumente/
├── 2025/                          ← Alt-Daten (Migration)
├── 2026/                          ← Neue Reklamationen
│   └── QA-26001/
│       ├── Fotos/
│       ├── Schriftverkehr/
│       ├── F_QM_02_Qualitaetsabweichung.pdf
│       └── F_QM_03_8D_Report.pdf
└── Formular-Vorlagen/             ← XLSX/DOCX Originale
    ├── F_QM_02_Qualitaetsabweichung.xlsx
    ├── F_QM_03_8D_Report.xlsx
    ├── F_QM_04_NZA.xlsx
    └── F_QM_14_Korrekturmassnahme.xlsx
```

---

## 👥 BERECHTIGUNGEN & SICHTBARKEIT

### Dashboard-Zugriff

| Rolle | Sichtbarkeit | Aktionen |
|-------|--------------|----------|
| **AL, TS** (QM) | Alles | CRUD, Formblatt, Export |
| **CS, CA, SV** (GF) | Alles | Lesen, Kommentieren |
| **Abteilungsleiter** (L2) | Alles | Lesen eigene KST bearbeiten |
| **Mitarbeiter** (L1) | Eigene KST | Nur Lesen |

### KST-basierte Sichtbarkeit

| User sieht | Eigene KST | Andere KST |
|------------|------------|------------|
| KPIs | ✅ Alle | ✅ Alle |
| QA-ID, Typ, Prio, Status | ✅ | ✅ |
| **Titel** | ✅ | ❌ Ausgeblendet |
| **Beschreibung** | ✅ | ❌ Ausgeblendet |
| **Verursacher** | ✅ | ❌ Ausgeblendet |

---

## 🔄 FORMBLATT-WORKFLOW (osp-formular-skill v1.1)

### Primärformat: XLSX → PDF (EMPFOHLEN)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. User klickt "Formblatt generieren" im Dashboard             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. FastAPI sendet Request an n8n Webhook                       │
│     POST /webhook/rms-formblatt                                 │
│     { qa_id, formular_typ, rekla_daten }                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. n8n lädt XLSX-Original aus SharePoint                       │
│     GET /sites/RMS/Formular-Vorlagen/F_QM_02.xlsx               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. n8n sendet an Claude API (via anthropic-proxy)              │
│     "Extrahiere Felddaten aus Reklamation für Formular..."      │
│     → Claude returniert JSON mit Feld-Werten                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. n8n befüllt XLSX mit fill_xlsx_form.py                      │
│     python3 fill_xlsx_form.py template.xlsx output.xlsx         │
│             --data '{"qa_id": "QA-26001", ...}'                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. n8n konvertiert zu PDF mit LibreOffice Headless             │
│     python3 convert_to_pdf.py output.xlsx output.pdf            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  7. n8n speichert in SharePoint                                 │
│     PUT /sites/RMS/2026/QA-26001/F_QM_02.pdf                    │
│     PUT /sites/RMS/2026/QA-26001/F_QM_02.xlsx (editierbar)      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  8. Dashboard zeigt Download-Link                               │
│     Optional: Email an Lieferant senden                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⏱️ ZEITPLAN (AKTUALISIERT)

### Woche 1: MVP (27.01. - 31.01.2026)

| Datum | Aufgabe | Deliverable | Stunden |
|-------|---------|-------------|---------|
| Mo 27.01. | Projektstruktur anlegen | /backend, /frontend, /n8n-workflows | 1h |
| Mo 27.01. | FastAPI Skeleton | main.py, config.py, database.py | 3h |
| Mo 27.01. | SQLite Schema | models/*.py | 2h |
| Di 28.01. | CRUD Reklamationen | routers/reklamationen.py | 3h |
| Di 28.01. | CRUD Maßnahmen | routers/massnahmen.py | 2h |
| Di 28.01. | CRUD Korrespondenz | routers/korrespondenz.py | 1h |
| Mi 29.01. | Alpine.js Dashboard | index.html, app.js | 4h |
| Mi 29.01. | KPI-Cards + Liste | Basis-UI fertig | 2h |
| Do 30.01. | KST-Filter-Logik | HR_CORE Integration | 3h |
| Do 30.01. | Detail-Ansicht | Modal/Drawer | 3h |
| Fr 31.01. | n8n: E-Mail-Import | rms-email-import.json | 3h |
| Fr 31.01. | n8n: QA-ID Generator | rms-qa-id-generator.json | 2h |
| Fr 31.01. | Docker Deployment | docker-compose.yml | 1h |

**Woche 1 Meilenstein:** MVP lauffähig auf Hetzner

### Woche 2: Vollständig (03.02. - 07.02.2026)

| Datum | Aufgabe | Deliverable | Stunden |
|-------|---------|-------------|---------|
| Mo 03.02. | n8n: Formblatt-Generator | rms-formblatt-generator.json | 4h |
| Mo 03.02. | Claude-Prompt für Formblatt | Prompt + Test | 2h |
| Di 04.02. | PDF-Export Setup | weasyprint/LibreOffice | 3h |
| Di 04.02. | SharePoint-Upload | n8n Node konfigurieren | 2h |
| Mi 05.02. | Dashboard: Chart.js | charts.js Modul | 3h |
| Mi 05.02. | KPI-Berechnung | kpi_service.py | 2h |
| Do 06.02. | n8n: Maßnahmen-Alarm | rms-alarm.json | 2h |
| Do 06.02. | Integration-Tests | test_rms.py | 3h |
| Fr 07.02. | Dokumentation | README.md, API-Docs | 2h |
| Fr 07.02. | Schulung TS | Live-Demo | 2h |
| Fr 07.02. | **GO-LIVE** | Produktivschaltung | 1h |

**Woche 2 Meilenstein:** RMS v1.0 produktiv

### Phase 3: Erweiterungen (ab KW 7)

| Feature | Aufwand | Priorität |
|---------|---------|-----------|
| ChromaDB: Ähnliche Reklamationen | 8h | 🟢 Optional |
| Teams-Benachrichtigungen | 4h | 🟢 Optional |
| Mobile-Optimierung | 4h | 🟡 Mittel |
| Automatische Kategorisierung | 8h | 🟢 Optional |

---

## 📁 DATEISTRUKTUR (ZIEL)

```
App_Engineering/RMS/
├── docs/
│   ├── RMS_Strategie_v5.0.md            ← Diese Datei
│   ├── RMS_API_Docs.md                  ← API Dokumentation
│   └── RMS_Phase1_Zusammenfassung.md    ← SharePoint Status
│
├── backend/
│   ├── main.py                          ← FastAPI Entry (max. 300 Zeilen)
│   ├── config.py                        ← Konfiguration (max. 400 Zeilen)
│   ├── database.py                      ← SQLite + SQLAlchemy (max. 200 Zeilen)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── reklamation.py               ← (max. 200 Zeilen)
│   │   ├── massnahme.py
│   │   └── korrespondenz.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── reklamation.py               ← (max. 300 Zeilen)
│   │   └── massnahme.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── reklamationen.py             ← (max. 400 Zeilen)
│   │   ├── massnahmen.py
│   │   ├── korrespondenz.py
│   │   └── formblatt.py
│   └── services/
│       ├── __init__.py
│       ├── qa_id_generator.py           ← (max. 500 Zeilen)
│       ├── kpi_calculator.py
│       └── hr_core_lookup.py
│
├── frontend/
│   ├── index.html                       ← Alpine.js SPA (max. 400 Zeilen)
│   ├── static/
│   │   ├── app.js                       ← Alpine.js Logic (max. 200 Zeilen)
│   │   ├── api.js                       ← API Calls (max. 400 Zeilen)
│   │   └── charts.js                    ← Chart.js (max. 300 Zeilen)
│   └── assets/
│       └── logo_schneider.png
│
├── n8n-workflows/
│   ├── rms-email-import.json
│   ├── rms-qa-id-generator.json
│   ├── rms-formblatt-generator.json
│   ├── rms-sharepoint-upload.json
│   └── rms-alarm.json
│
├── formulare/                           ← Bestehend - BEIBEHALTEN
│   ├── RMS_Formular_Uebersicht.md
│   ├── f_qm_02_qualitaetsabweichung/
│   ├── f_qm_03_8D_Report/
│   ├── f_qm_04_nza/
│   └── f_qm_14_korrekturmaßnahmen/
│
├── scripts/
│   ├── fill_xlsx_form.py                ← Aus osp-formular-skill
│   ├── convert_to_pdf.py                ← Aus osp-formular-skill
│   └── migrate_legacy_data.py           ← 2025er Daten migrieren
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 💰 KOSTEN (AKTUALISIERT)

| Position | Einmalig | Jährlich |
|----------|----------|----------|
| Entwicklung AL (~30h intern) | €0 | - |
| Hetzner CX43 (anteilig 10%) | - | €108 |
| Claude API (~150 Formblätter) | - | ~€50 |
| Microsoft 365 | - | ✅ Vorhanden |
| **TOTAL** | **€0** | **~€160** |

**3-Jahres-TCO:** ~€480

---

## ✅ CHECKLISTEN

### ✅ Bereits erledigt (Phase 1 - Dezember 2025)
- [x] SharePoint-Site erstellt
- [x] 5 Listen konfiguriert
- [x] Config-Einträge gesetzt
- [x] Formular-Vorlagen konvertiert (MD + JSON + Prompt)
- [x] Test-Reklamation QA-26001 angelegt

### ⏳ Woche 1 (27.-31.01.2026)
- [ ] FastAPI Backend Skeleton
- [ ] SQLite Schema + Models
- [ ] CRUD Endpoints
- [ ] Alpine.js Dashboard
- [ ] KST-Filter-Logik
- [ ] n8n E-Mail-Import
- [ ] n8n QA-ID Generator
- [ ] Docker Deployment

### ⏳ Woche 2 (03.-07.02.2026)
- [ ] n8n Formblatt-Generator
- [ ] Claude-Integration
- [ ] PDF-Export
- [ ] SharePoint-Upload
- [ ] Chart.js Dashboard
- [ ] Maßnahmen-Alarm
- [ ] Tests + Dokumentation
- [ ] **GO-LIVE**

---

## 📝 ENTSCHEIDUNGEN (Dokumentiert)

| Datum | Entscheidung | Begründung |
|-------|--------------|------------|
| 20.12.2025 | SharePoint als Dokumenten-Speicher | M365 vorhanden |
| 20.12.2025 | KST-Zuordnung aus HR_CORE | Single Source of Truth |
| **25.01.2026** | **Alpine.js statt React** | app-development Skill v2.0 |
| **25.01.2026** | **SQLite statt PostgreSQL** | Skill-konform, 150/Jahr ausreichend |
| **25.01.2026** | **n8n only (kein Power Automate)** | osp-n8n-skill, einheitlich |
| **25.01.2026** | **XLSX → PDF statt Markdown** | osp-formular-skill v1.1 |

---

## 🔗 REFERENZEN

| Dokument | Zweck |
|----------|-------|
| app-development Skill v2.0 | Tech-Stack Vorgaben |
| osp-formular-skill v1.1 | Formular-Workflow |
| osp-n8n-skill | Workflow-Templates |
| HR_CORE_Personalstamm.md | KST-Zuordnung |
| QM_REK_Reklamationsmanagement.md | Prozessbeschreibung |

---

**Dokument-Version:** 5.0  
**Erstellt:** 2025-01-25  
**Nächster Review:** Nach Go-Live (08.02.2026)

---

*[QM][RMS] Rainer Schneider Kabelsatzbau GmbH & Co. KG*  
*OSP-Skill-konform v2.0*
