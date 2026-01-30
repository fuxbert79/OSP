# 📊 RMS STATUS-BERICHT & ROADMAP

**Stand:** 26.01.2026  
**Projekt:** Reklamationsmanagementsystem (RMS)  
**Verantwortlich:** AL (QM & KI-Manager)

---

## 🔍 PROJEKT-HISTORIE (Zusammenfassung)

### Was wurde Ende Dezember 2025 geplant?

Das RMS-Projekt wurde am **20.-22.12.2025** konzipiert mit folgender Strategie:

| Entscheidung | Beschreibung |
|--------------|--------------|
| **Architektur** | Microsoft 365 Native (statt Custom FastAPI/React) |
| **Datenbank** | SharePoint Lists (statt PostgreSQL) |
| **Dashboard** | HTML + Chart.js auf Hetzner |
| **KI-Integration** | n8n + Claude API für Formblatt-Ausfüllung |
| **Hauptnutzer** | AL, TS, GF (nur 3 Power Apps User) |
| **Alle MA** | Dashboard mit KST-basierter Sichtbarkeit |

### Geplanter Zeitplan (ursprünglich)

| Phase | Datum | Status |
|-------|-------|--------|
| Phase 1a: SharePoint Listen | 22.12.2025 | ✅ ERLEDIGT |
| Phase 1b: Formular-Konvertierung | 22.12.2025 | ✅ ERLEDIGT (heute wiederholt) |
| Phase 1c: Power Automate | 27.-28.12.2025 | ❓ UNKLAR |
| Phase 1d: Power Apps | 29.12.2025 | ❓ UNKLAR |
| Phase 1e: HTML-Dashboard | 30.12.2025 | ❓ UNKLAR |
| **MVP Go-Live** | **02.01.2026** | ❌ VERPASST |
| Phase 2: KI-Features | 06.-17.01.2026 | ❓ NICHT GESTARTET |
| Phase 3: Erweiterungen | ab 20.01.2026 | ❓ NICHT GESTARTET |

---

## ✅ WAS IST DEFINITIV ERLEDIGT?

### 1. SharePoint-Site & Listen (Phase 1a)

**URL:** `https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS`

| Liste | Spalten | Status |
|-------|---------|--------|
| **RMS-Reklamationen** | QA_ID, Titel, Rekla_Typ, Prioritaet, Rekla_Status, Beschreibung, KST, Verantwortlich, Erfassungsdatum, Zieldatum | ✅ |
| **RMS-Maßnahmen** | Rekla-Lookup, Typ, Termin, Status, Wirksamkeit | ✅ |
| **RMS-Schriftverkehr** | Rekla-Lookup, Datum, Richtung, Betreff, Outlook_ID | ✅ |
| **RMS-KPIs** | Datum, Offene, Kritische, Überfällige, Ø-Tage | ✅ |
| **RMS-Config** | Key, Value | ✅ |

**RMS-Config Einträge:**
- CURRENT_YEAR = 2026
- Last_ID = 1
- EMAIL_REKLAMATION = reklamation@schneider-kabelsatzbau.de
- EMAIL_NZA = nza@schneider-kabelsatzbau.de
- ALARM_TAGE = 3
- ADMIN_EMAIL = [deine Email]

### 2. Formular-Konvertierung (Phase 1b) - HEUTE WIEDERHOLT

| Formular | Dateien | Status |
|----------|---------|--------|
| **F-QM-02** Qualitätsabweichung | .md + .json + RMS_Prompt | ✅ |
| **F-QM-03** 8D-Report (extern) | .md + .json + RMS_Prompt | ✅ |
| **F-QM-04** NZA | .md + .json + RMS_Prompt | ✅ |
| **F-QM-14** Korrekturmaßnahme (8D-Light intern) | .md + .json + RMS_Prompt | ✅ |

**Gesamt:** 12 Dateien + 1 Übersichtsdokument

---

## ❓ WAS IST UNKLAR / OFFEN?

Diese Punkte waren für **27.12.2025 - 02.01.2026** geplant:

### Phase 1c: Power Automate Flows (4 Stück)

| Flow | Funktion | Status? |
|------|----------|---------|
| **RMS-Email-Import** | Neue E-Mail → neuer Eintrag in RMS-Reklamationen | ❓ |
| **RMS-QA-ID-Generator** | Generiert QA-26001, QA-26002, etc. | ❓ |
| **RMS-Maßnahmen-Alarm** | Erinnerung bei Termin-Überschreitung | ❓ |
| **RMS-Ordner-Sync** | Erstellt SharePoint-Ordner /2026/QA-26xxx/ | ❓ |

### Phase 1d: Power Apps

| App | Funktion | Status? |
|-----|----------|---------|
| **RMS Dashboard** | CRUD für AL, TS, GF | ❓ |
| **RMS Detail-View** | Einzelansicht mit Maßnahmen | ❓ |

### Phase 1e: HTML-Dashboard

| Komponente | Funktion | Status? |
|------------|----------|---------|
| **KPI-Cards** | Offene, Kritische, Überfällige | ❓ |
| **Tabelle** | Liste aller Reklamationen | ❓ |
| **KST-Filter** | Sichtbarkeit nach Kostenstelle | ❓ |
| **Charts** | (Phase 2/3) | ❓ |

---

## 🎯 EMPFOHLENE NÄCHSTE SCHRITTE

### Option A: MVP nachholen (Minimalvariante)

Wenn du das RMS schnell produktiv haben willst:

| Priorität | Aufgabe | Aufwand |
|-----------|---------|---------|
| 1 | Power Automate: QA-ID-Generator | 2h |
| 2 | Power Automate: E-Mail-Import | 4h |
| 3 | Power Apps: Einfaches CRUD | 4h |
| 4 | HTML-Dashboard: Basis-Tabelle | 4h |
| **TOTAL** | **MVP funktionsfähig** | **~14h** |

### Option B: KI-Formblatt-fokussiert

Wenn die KI-Ausfüllung der Formblätter Priorität hat:

| Priorität | Aufgabe | Aufwand |
|-----------|---------|---------|
| 1 | n8n Workflow: Formblatt-Generator | 8h |
| 2 | RMS-Prompts in Open WebUI hinterlegen | 2h |
| 3 | Test mit echten Reklamationsdaten | 2h |
| **TOTAL** | **KI-Formblätter funktionsfähig** | **~12h** |

### Option C: Vollständiger Reset & Neuplanung

Wenn du neu priorisieren willst:
→ Roadmap-Session mit Festlegung realistischer Termine

---

## 📁 DATEIEN IM OSP-VERZEICHNIS

Laut Projekt-Ordner sollten diese Dateien existieren:

```
C:\Users\andre\OneDrive - Rainer Schneider Kabelsatzbau...\App_Engineering\RMS\
├── formulare/
│   ├── f_qm_02_qualitaetsabweichung/
│   │   ├── F_QM_02_Qualitaetsabweichung.md
│   │   ├── F_QM_02_Schema.json
│   │   └── RMS_Prompt_F_QM_02_Qualitaetsabweichung.md
│   ├── f_qm_03_8d_report/
│   ├── f_qm_04_nza/
│   └── f_qm_14_korrekturmassnahme/
├── RMS_Strategie_v4.1_FINAL.md
├── RMS_Formular_Uebersicht.md
└── Workflow-Liste-Ergaenzt.csv
```

---

## 🔧 TECHNISCHE INFRASTRUKTUR (bestätigt)

| Komponente | Status | Details |
|------------|--------|---------|
| **Hetzner CX43** | ✅ Läuft | 8 vCPU, 32 GB RAM, IP: 46.224.102.30 |
| **Open WebUI** | ✅ Läuft | v0.6.41 |
| **ChromaDB** | ✅ Läuft | v0.5.15 |
| **n8n** | ✅ Läuft | Auf Hetzner |
| **anthropic-proxy** | ✅ Läuft | Claude API Zugang |
| **SharePoint RMS-Site** | ✅ Existiert | Listen erstellt |

---

## ❗ KLÄRUNGSBEDARF

Bitte beantworte diese Fragen:

1. **Power Automate Flows:** Wurden die 4 Flows zwischen 27.12. und 02.01. erstellt?
2. **Power Apps:** Wurde eine App erstellt?
3. **HTML-Dashboard:** Wurde etwas auf Hetzner deployed?
4. **Aktuelle Arbeitsweise:** Wie erfasst du aktuell Reklamationen? (Noch manuell per Excel/Outlook?)
5. **Priorität:** Was ist wichtiger - MVP mit Basis-Funktion oder KI-Formblätter?

---

*Erstellt: 26.01.2026 | Autor: OSP-System*
