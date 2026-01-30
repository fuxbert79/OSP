# RMS - Reklamationsmanagementsystem

**Projekt:** OSP-Integration
**Version:** 0.1.0
**Stand:** 2026-01-26
**Verantwortlich:** AL (QM & KI-Manager)

---

## Übersicht

Das RMS ist Teil des OSP-Ökosystems und dient der zentralen Verwaltung von:
- **Internen Reklamationen (NZA)** - Nach- und Zusatzarbeiten
- **Kundenreklamationen** - Externe Beschwerden
- **Lieferantenreklamationen** - Qualitätsabweichungen

## Architektur

- **Frontend:** HTML-Dashboard (alle MA) + Power Apps (AL, TS, GF)
- **Backend:** SharePoint Lists + n8n Workflows
- **KI:** Claude API für Formblatt-Ausfüllung
- **Dokumente:** SharePoint /sites/RMS/

## Verzeichnisse

| Ordner | Beschreibung |
|--------|--------------|
| backend/ | FastAPI Backend (geplant) |
| dashboard/ | HTML-Dashboard mit KST-Filter |
| workflows/ | n8n Workflow JSON-Exports |
| formulare/ | QM-Formblätter (4 Stück) |
| docs/ | Strategie & Dokumentation |
| prompts/ | System-Prompts für KI-Ausfüllung |

## Formblätter

| ID | Name | Anwendung |
|----|------|-----------|
| F-QM-02 | Qualitätsabweichung | Lieferanten-Reklamation |
| F-QM-03 | 8D-Report | Externe Reklamation (vollständig) |
| F-QM-04 | NZA | Interne Fehler |
| F-QM-14 | Korrekturmaßnahme | Interne Abweichung (8D-Light) |

## Phasen

| Phase | Features | Status |
|-------|----------|--------|
| MVP | SharePoint Listen, Power Automate, Dashboard | ⏳ Offen |
| Phase 2 | KI-Formblatt-Generator (n8n + Claude) | ⏳ Offen |
| Phase 3 | Charts, Teams-App, ChromaDB-Suche | ⏳ Offen |

---

*Teil des OSP-Systems | NULL-FEHLER-POLITIK gilt!*
