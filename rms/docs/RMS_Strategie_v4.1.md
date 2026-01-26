# RMS Strategie v4.1

**Projekt:** RMS - Reklamationsmanagementsystem
**Version:** 4.1
**Stand:** 2026-01-26
**Autor:** AL (QM & KI-Manager)

---

## 1. Übersicht

### 1.1 Zielsetzung

Aufbau eines integrierten Reklamationsmanagementsystems für:
- Zentrale Erfassung aller Reklamationen
- KI-gestützte Formblatt-Ausfüllung
- Transparente Statusverfolgung
- Statistische Auswertungen für KVP

### 1.2 Kennzahlen

| Parameter | Wert |
|-----------|------|
| Erwartete Einträge | ~150/Jahr |
| Typen | INTERN, KUNDE, LIEFERANT |
| Hauptnutzer | AL, TS, GF |
| Dashboard-Nutzer | Alle MA (KST-basiert) |

---

## 2. Architektur

### 2.1 Komponenten

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

### 2.2 ID-Format

**Format:** `QA-JJNNN`

- `QA` - Qualitätsabweichung (Prefix)
- `JJ` - Jahr (2-stellig)
- `NNN` - Laufende Nummer (3-stellig)

**Beispiele:**
- `QA-26001` - Erste Reklamation 2026
- `QA-26150` - 150. Reklamation 2026

---

## 3. Phasen

### Phase 1: MVP

**Ziel:** Grundfunktionalität etablieren

| Feature | Technologie | Status |
|---------|-------------|--------|
| Reklamations-Liste | SharePoint Liste | ⏳ Offen |
| Basis-Dashboard | HTML/CSS/JS | ⏳ Offen |
| E-Mail-Import | Power Automate | ⏳ Offen |
| Formblatt-Templates | Markdown | ⏳ Offen |

### Phase 2: KI-Integration

**Ziel:** Automatisierte Formblatt-Ausfüllung

| Feature | Technologie | Status |
|---------|-------------|--------|
| Formblatt-Generator | n8n + Claude API | ⏳ Offen |
| Ähnlichkeitssuche | ChromaDB | ⏳ Offen |
| Prompt-Templates | System-Prompts | ⏳ Offen |

### Phase 3: Erweiterung

**Ziel:** Vollständige Integration

| Feature | Technologie | Status |
|---------|-------------|--------|
| Charts/Statistiken | Dashboard-Update | ⏳ Offen |
| Teams-App | Power Apps | ⏳ Offen |
| Eskalations-Workflows | n8n | ⏳ Offen |

---

## 4. Formblätter

### 4.1 Übersicht

| ID | Name | Anwendung |
|----|------|-----------|
| F-QM-02 | Qualitätsabweichung | Lieferanten |
| F-QM-03 | 8D-Report | Kunden (vollständig) |
| F-QM-04 | NZA | Intern |
| F-QM-14 | Korrekturmaßnahme | Intern (8D-Light) |

### 4.2 Dateistruktur

Jedes Formblatt hat:
- `.md` - Markdown-Template (menschenlesbar)
- `.json` - JSON-Schema (maschinell)
- `_prompt.md` - KI-System-Prompt

---

## 5. Integration mit OSP

### 5.1 ChromaDB

- Collection: `rms_reklamationen`
- Embedding: E5-large
- Anwendung: Ähnliche Reklamationen finden

### 5.2 HR_CORE

- MA-Kürzel Validierung
- KST-Zuordnung
- Berechtigungsprüfung

### 5.3 n8n Workflows

- E-Mail-Import aus QM-Postfach
- Formblatt-Generator via Claude API
- Alarm-Eskalation bei kritischen Fällen

---

## 6. Nächste Schritte

- [ ] SharePoint-Listen erstellen
- [ ] Formular-Templates finalisieren
- [ ] n8n Workflow für E-Mail-Import
- [ ] Dashboard-Prototyp testen
- [ ] KI-Prompts entwickeln

---

*Teil des OSP-Systems | NULL-FEHLER-POLITIK gilt!*
