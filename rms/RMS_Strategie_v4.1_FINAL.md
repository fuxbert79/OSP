# 🚀 RMS ENTWICKLUNGS-STRATEGIE v4.1 (FINAL)
## Reklamationsmanagementsystem - Rainer Schneider Kabelsatzbau

**Stand:** 2025-12-20  
**Go-Live MVP:** 02.01.2026  
**Go-Live KI-Features:** 17.01.2026  
**Verantwortlich:** AL (QM/KI-Manager)

---

## 📊 PROJEKT-PARAMETER

| Parameter | Wert |
|-----------|------|
| **Max. QA-Einträge/Jahr** | 150 |
| **Hauptnutzer (Power Apps)** | AL, TS, GF (CS, CA, SV) |
| **Dashboard-Nutzer** | ~54 (alle MA) |
| **Server** | Hetzner CX43 (8 vCPU, 16 GB RAM, 100 GB) |
| **SharePoint-Site** | ✅ `https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS` |
| **KI-Backend** | Claude API via anthropic-proxy (bestehend) |
| **KST-Zuordnung** | HR_CORE_Personalstamm.md (Referenz) |

---

## 🎯 FEATURE-ÜBERSICHT

| Feature | Phase | Status |
|---------|-------|--------|
| SharePoint Listen (5x) | MVP | ⏳ |
| Power Automate Flows (E-Mail, ID, Alarm) | MVP | ⏳ |
| Power Apps (CRUD für AL/TS/GF) | MVP | ⏳ |
| HTML-Dashboard (KST-basiert) | MVP | ⏳ |
| KI-Formblatt-Generator (n8n + Claude) | Phase 2 | ⏳ |
| PDF-Export (pandoc/weasyprint) | Phase 2 | ⏳ |
| Dashboard-Charts (Chart.js) | Phase 3 | ⏳ |
| Teams-App | Phase 3 | ⏳ |
| Ähnliche Reklamationen (ChromaDB) | Phase 3 | ⏳ |

---

## 🏗️ ARCHITEKTUR

```
┌─────────────────────────────────────────────────────────────────┐
│           RMS v4.1 - FINALE ARCHITEKTUR                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HAUPTNUTZER (AL, TS, GF)          ALLE MA (~54)                │
│  ┌─────────────────────┐           ┌─────────────────────┐      │
│  │  Power Apps         │           │  HTML-Dashboard     │      │
│  │  • CRUD             │           │  • KPIs (alle)      │      │
│  │  • KI-Formblatt     │           │  • Eigene KST ✅    │      │
│  │  • PDF-Export       │           │  • Andere KST 🔒    │      │
│  └──────────┬──────────┘           └──────────┬──────────┘      │
│             │                                  │                 │
│             └──────────────┬───────────────────┘                 │
│                            │                                     │
│  ┌─────────────────────────▼─────────────────────────────────┐  │
│  │              SharePoint (Daten + Dokumente)                │  │
│  │  Listen: Reklamationen, Maßnahmen, Schriftverkehr,        │  │
│  │          KPIs, Config                                      │  │
│  │  Docs:   /2026/QA-26001/F_QM_02.pdf, Fotos, E-Mails       │  │
│  └─────────────────────────┬─────────────────────────────────┘  │
│                            │                                     │
│  ┌─────────────────────────▼─────────────────────────────────┐  │
│  │              AUTOMATION                                    │  │
│  │  ┌─────────────────┐  ┌─────────────────┐                 │  │
│  │  │ Power Automate  │  │ n8n (Hetzner)   │                 │  │
│  │  │ • E-Mail-Import │  │ • Claude API    │                 │  │
│  │  │ • QA-ID Gen     │  │ • Formblatt-Gen │                 │  │
│  │  │ • Alarme        │  │ • PDF-Export    │                 │  │
│  │  └─────────────────┘  └─────────────────┘                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  HETZNER CX43: Open WebUI + ChromaDB + n8n + anthropic-proxy    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 SHAREPOINT-STRUKTUR

### Listen (5x)

| Liste | Zweck | Felder (Auszug) |
|-------|-------|-----------------|
| **RMS-Reklamationen** | Stammdaten | QA_ID, Titel, Typ, Prio, Status, KST, Verantwortlich |
| **RMS-Maßnahmen** | Maßnahmenplan | Rekla-Lookup, Typ, Termin, Status, Wirksamkeit |
| **RMS-Schriftverkehr** | E-Mail-Verlauf | Rekla-Lookup, Datum, Richtung, Betreff, Outlook_ID |
| **RMS-KPIs** | Aggregation | Datum, Offene, Kritische, Überfällige, Ø-Tage |
| **RMS-Config** | Konfiguration | Key, Value (CURRENT_YEAR, LAST_ID, etc.) |

### Dokumentstruktur

```
/sites/RMS/Freigegebene Dokumente/
├── 2025/                          ← Alt-Daten (Migration)
├── 2026/                          ← Neue Reklamationen
│   └── QA-26001/
│       ├── Fotos/
│       ├── Schriftverkehr/
│       ├── F_QM_02_Qualitaetsabweichung.pdf
│       └── F_QM_04_8D_Report.pdf
└── Formular-Vorlagen/             ← Schema-Formulare (MD)
    ├── F_QM_02_Qualitaetsabweichung.md
    ├── F_QM_04_8D_Report.md
    └── ...
```

---

## 👥 BERECHTIGUNGEN & SICHTBARKEIT

### Power Apps (Hauptnutzer)

| User | Rolle | Zugriff |
|------|-------|---------|
| AL | QM-Manager | Vollzugriff (alle Funktionen) |
| TS | Vertretung | Vollzugriff (alle Funktionen) |
| CS, CA, SV | Geschäftsführung | Lesen + Kommentieren |

### Dashboard (alle MA)

**KST-basierte Sichtbarkeit (Referenz: HR_CORE_Personalstamm.md):**

| User sieht | Eigene KST | Andere KST |
|------------|------------|------------|
| KPIs | ✅ Alle | ✅ Alle |
| QA-ID | ✅ | ✅ |
| Typ, Prio, Status | ✅ | ✅ |
| **Titel** | ✅ | ❌ Ausgeblendet |
| **Beschreibung** | ✅ | ❌ Ausgeblendet |
| **Verursacher** | ✅ | ❌ Ausgeblendet |

**Ausnahmen (sehen ALLES):**
- AL, TS (Hauptnutzer)
- CS, CA, SV (Geschäftsführung)
- Abteilungsleiter mit L2/L3

---

## 🔄 KI-FORMBLATT-WORKFLOW (Phase 2)

### Ablauf

```
1. AL/TS klickt "Formblatt generieren" in Power Apps
         │
         ▼
2. Power Apps ruft n8n Webhook auf
   POST /webhook/rms-formblatt
   { qa_id, formular_typ, rekla_daten }
         │
         ▼
3. n8n lädt Schema-Formular aus SharePoint
   GET /sites/RMS/Formular-Vorlagen/F_QM_02.md
         │
         ▼
4. n8n sendet an Claude API (via anthropic-proxy)
   Model: claude-sonnet-4-20250514
   Prompt: "Fülle Formular aus basierend auf Rekla-Daten..."
         │
         ▼
5. Claude returniert ausgefülltes Markdown
         │
         ▼
6. n8n speichert Entwurf in SharePoint
   PUT /sites/RMS/.../QA-26001/F_QM_02_ENTWURF.md
         │
         ▼
7. Power Apps zeigt Vorschau → AL/TS prüft/korrigiert
         │
         ▼
8. Nach Freigabe: n8n konvertiert MD → PDF (pandoc)
         │
         ▼
9. PDF gespeichert: /QA-26001/F_QM_02.pdf
```

### Schema-Formulare (Markdown)

**Benötigt (AL konvertiert selbst):**

| Formular | Beschreibung | Status |
|----------|--------------|--------|
| F_QM_02 | Qualitätsabweichung | ⏳ AL konvertiert |
| F_QM_04 | 8D-Report (D1-D8) | ⏳ AL konvertiert |
| F_QM_03 | Korrekturmaßnahme | ⏳ Optional |

**Format-Anforderung:**
- Markdown mit Platzhaltern: `{{QA_ID}}`, `{{DATUM}}`, `{{BESCHREIBUNG}}`
- Kompatibel mit pandoc/weasyprint für PDF-Export
- CI-konform (Schneider-Blau #003366)

---

## ⏱️ ZEITPLAN

### Phase 1: MVP (Go-Live 02.01.2026)

| Datum | Aufgabe | Verantwortlich | Stunden |
|-------|---------|----------------|---------|
| **VOR 22.12.** | Schema-Formulare konvertieren | AL | ~4h |
| 22.12. | SharePoint Listen erstellen | AL + IT-Admin | 4h |
| 27.12. | Power Automate: E-Mail-Import | AL | 4h |
| 27.12. | Power Automate: QA-ID Generator | AL | 2h |
| 28.12. | Power Automate: Maßnahmen-Alarm | AL | 2h |
| 28.12. | Power Automate: Ordner-Sync | AL | 2h |
| 29.12. | Power Apps: Dashboard-View | AL | 4h |
| 29.12. | Power Apps: Detail-View + CRUD | AL | 4h |
| 30.12. | HTML-Dashboard: Basis + KPIs | AL | 4h |
| 30.12. | HTML-Dashboard: KST-Filter | AL | 4h |
| 31.12. | Testing + Schulung TS | AL | 4h |
| **02.01.** | **GO-LIVE MVP** | AL | 2h |

**MVP-Umfang:**
- ✅ Reklamationen erfassen/bearbeiten
- ✅ E-Mail-Import automatisch
- ✅ Dashboard mit KST-Filter
- ❌ KI-Formblatt (Phase 2)
- ❌ Teams-App (Phase 3)

### Phase 2: KI-Features (06.-17.01.2026)

| Datum | Aufgabe | Stunden |
|-------|---------|---------|
| 06.-07.01. | n8n Workflow: Formblatt-Generator | 8h |
| 08.01. | Claude-Prompt optimieren | 4h |
| 09.-10.01. | n8n Workflow: PDF-Export | 6h |
| 13.01. | Integration in Power Apps | 4h |
| 14.-15.01. | Testing | 4h |
| **17.01.** | **GO-LIVE KI-Features** | 2h |

### Phase 3: Erweiterungen (ab 20.01.2026)

| Feature | Geschätzter Aufwand |
|---------|---------------------|
| Dashboard-Charts (Chart.js) | 8h |
| Teams-App Deployment | 4h |
| Ähnliche Reklamationen (ChromaDB) | 12h |
| Automatische Kategorisierung | 8h |

---

## 💰 KOSTEN

| Position | Einmalig | Jährlich |
|----------|----------|----------|
| Entwicklung AL (~50h à €80) | €4.000 | - |
| Hetzner (anteilig 10%) | - | €108 |
| Claude API (~150 Formblätter) | - | ~€50 |
| Microsoft 365 | - | ✅ Vorhanden |
| **TOTAL** | **€4.000** | **~€160** |

**3-Jahres-TCO:** ~€4.500

---

## ✅ CHECKLISTEN

### Vor Phase 1 (bis 21.12.2025)
- [ ] Schema-Formulare konvertieren (F_QM_02, F_QM_04)
- [ ] SharePoint-Berechtigungen prüfen
- [ ] Power Automate Connector testen

### Phase 1 MVP (02.01.2026)
- [ ] SharePoint 5 Listen erstellt
- [ ] Power Automate 4 Flows aktiv
- [ ] Power Apps veröffentlicht
- [ ] HTML-Dashboard deployed
- [ ] KST-Filter aus HR_CORE funktioniert
- [ ] Schulung TS abgeschlossen
- [ ] Test-Reklamation erfolgreich

### Phase 2 KI-Features (17.01.2026)
- [ ] n8n Workflow: Formblatt-Generator
- [ ] n8n Workflow: PDF-Export
- [ ] Claude-Prompt getestet
- [ ] Integration Power Apps
- [ ] F_QM_02 + F_QM_04 generiert

### Phase 3 Erweiterungen (ab 20.01.2026)
- [ ] Dashboard-Charts
- [ ] Teams-App
- [ ] ChromaDB-Integration

---

## 📁 REFERENZ-DOKUMENTE

| Dokument | Zweck | Speicherort |
|----------|-------|-------------|
| HR_CORE_Personalstamm.md | KST-Zuordnung für Dashboard | OSP/Main/HR_Human_Resources/ |
| QM_REK_Reklamationsmanagement.md | Prozessbeschreibung | OSP/Main/QM_Qualitaetsmanagement/ |
| F_QM_02_Qualitaetsabweichung.md | Schema-Formular | OSP/Formblätter/ (nach Konvertierung) |
| F_QM_04_8D_Report.md | Schema-Formular | OSP/Formblätter/ (nach Konvertierung) |

---

## 🔗 TECHNISCHE DETAILS

### Server-Endpunkte (Hetzner)

| Dienst | URL | Port |
|--------|-----|------|
| Open WebUI | https://osp.schneider-kabelsatzbau.de | 443 |
| n8n | http://localhost:5678 | 5678 |
| anthropic-proxy | http://localhost:8080 | 8080 |
| HTML-Dashboard | http://localhost:3001 | 3001 |

### SharePoint API

```
Base-URL: https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS
Lists:    /_api/web/lists/getbytitle('RMS-Reklamationen')/items
Docs:     /_api/web/GetFolderByServerRelativeUrl('/sites/RMS/...')
Auth:     Azure AD App Registration + MSAL.js
```

### n8n Webhooks

```
Formblatt-Generator: POST /webhook/rms-formblatt
PDF-Export:          POST /webhook/rms-pdf-export
E-Mail-Backup:       GET  /webhook/rms-email-check (Cron)
```

---

## 📝 ENTSCHEIDUNGEN (Dokumentiert)

| Datum | Entscheidung | Begründung |
|-------|--------------|------------|
| 20.12.2025 | M365 Native statt Custom | Weniger Risiko, IT-Admin Support |
| 20.12.2025 | KST-Zuordnung aus HR_CORE | Bereits vorhanden, Single Source of Truth |
| 20.12.2025 | Teams-App in Phase 3 | MVP-Fokus auf Kernfunktionen |
| 20.12.2025 | Claude API für KI-Features | anthropic-proxy bereits konfiguriert |
| 20.12.2025 | HTML-Dashboard statt Power BI | AL kennt HTML/CSS/JS |

---

**Dokument-Version:** 4.1 FINAL  
**Erstellt:** 2025-12-20  
**Nächster Review:** Nach Go-Live MVP (03.01.2026)

---

*[QM] Rainer Schneider Kabelsatzbau GmbH & Co. KG*
