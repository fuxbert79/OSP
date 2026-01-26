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

```
┌─────────────────────────────────────────────────────────────┐
│                    RMS ARCHITEKTUR                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Power Apps  │  │ Dashboard   │  │ n8n Workflows       │ │
│  │ (CRUD)      │  │ (HTML)      │  │ • E-Mail-Import     │ │
│  │ AL, TS, GF  │  │ Alle MA     │  │ • Formblatt-Gen     │ │
│  └──────┬──────┘  └──────┬──────┘  │ • Alarme            │ │
│         │                │         └──────────┬──────────┘ │
│         └────────────────┼───────────────────┘             │
│                          │                                  │
│  ┌───────────────────────▼─────────────────────────────────┐   │
│  │              SharePoint (Daten + Dokumente)          │   │
│  │  Listen: Reklamationen, Maßnahmen, Schriftverkehr   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              OSP Backend (Hetzner CX43)               │  │
│  │  • ChromaDB (ähnliche Reklas)                        │  │
│  │  • Claude API (Formblatt-KI)                         │  │
│  │  • Open WebUI (Chat-Interface)                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Verzeichnisse

| Ordner | Beschreibung |
|--------|--------------|
| `backend/` | FastAPI Backend (geplant) |
| `dashboard/` | HTML-Dashboard mit KST-Filter |
| `workflows/` | n8n Workflow JSON-Exports |
| `formulare/` | QM-Formblätter (4 Stück) |
| `docs/` | Strategie & Dokumentation |
| `prompts/` | System-Prompts für KI-Ausfüllung |

## Formblätter

| ID | Name | Anwendung |
|----|------|-----------|
| F-QM-02 | Qualitätsabweichung | Lieferanten-Reklamation |
| F-QM-03 | 8D-Report | Externe Reklamation (vollständig) |
| F-QM-04 | NZA | Interne Fehler |
| F-QM-14 | Korrekturmaßnahme | Interne Abweichung (8D-Light) |

## Nächste Schritte

- [ ] Formular-Templates nach `/rms/formulare/` kopieren
- [ ] n8n Workflow für Formblatt-Generator erstellen
- [ ] Dashboard-Prototyp entwickeln
- [ ] SharePoint-Listen mit Server synchronisieren

---

*Teil des OSP-Systems | NULL-FEHLER-POLITIK gilt!*
