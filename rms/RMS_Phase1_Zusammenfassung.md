# 📋 RMS ENTWICKLUNG - STATUSBERICHT

**Projekt:** Reklamationsmanagementsystem (RMS)  
**Site:** https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS

---

## ✅ PHASE 1 ABGESCHLOSSEN: SharePoint-Struktur

### Erstellte Listen

| Liste | Spalten | Test-Daten | Status |
|-------|---------|------------|--------|
| **RMS-Reklamationen** | 10 | QA-26001 (Test) | ✅ Fertig |
| **RMS-Massnahmen** | 8 | 1 Test-Maßnahme | ✅ Fertig |
| **RMS-Schriftverkehr** | 8 | - | ✅ Fertig |
| **RMS-KPIs** | 7 | - | ✅ Fertig |
| **RMS-Config** | 3 | 6 Einträge | ✅ Fertig |

### Spalten-Übersicht

**RMS-Reklamationen:**
- Titel, QA_ID, Rekla_Typ, Prioritaet, Rekla_Status, Beschreibung, KST, Verantwortlich, Erfassungsdatum, Zieldatum

**RMS-Massnahmen:**
- Titel, Reklamation (Lookup), Reklamation:QA_ID, Massnahme_Typ, Massnahmen_Beschreibung, Verantwortlich, Termin, Massnahmen_Status

**RMS-Schriftverkehr:**
- Titel, Reklamation (Lookup), Reklamation:QA_ID, Email_Datum, Richtung, Absender, Empfaenger, Inhalt

**RMS-KPIs:**
- Titel, KPI_Datum, Offene_Gesamt, Offene_kritisch, Offene_hoch, Ueberfaellige_Massnahmen, Durchlaufzeit_Avg

**RMS-Config (6 Einträge):**
- CURRENT_YEAR = 2026
- Last_ID = 1
- EMAIL_REKLAMATION = reklamation@schneider-kabelsatzbau.de
- EMAIL_NZA = nza@schneider-kabelsatzbau.de
- ALARM_TAGE = 3
- ADMIN_EMAIL = a.loehr@schneider-kabelsatzbau.de

### Hochgeladene Formular-Vorlagen

**Ordner:** /sites/RMS/Dokumente/Formular-Vorlagen/

| Formular | Dateien |
|----------|---------|
| F_QM_02 Qualitätsabweichung | .md, .json, Prompt.md |
| F_QM_03 8D-Report | .md, .json, Prompt.md |
| F_QM_04 NZA | .md, .json, Prompt.md |
| F_QM_14 Korrekturmaßnahme | .md, .json, Prompt.md |

---

## ⏭️ NÄCHSTE SCHRITTE

### Phase 1b: Power Automate Flows

| # | Flow | Zweck | Status |
|---|------|-------|--------|
| 1 | **E-Mail-Import** | Automatisch Reklas aus Outlook erstellen | ⏳ Nächster Schritt |
| 2 | **QA-ID Generator** | Eindeutige IDs vergeben (QA-JJNNN) | ⏳ Nächster Schritt |
| 3 | Maßnahmen-Alarm | Tägliche Erinnerung bei Fälligkeit | ⏳ |
| 4 | Ordner-Sync | SharePoint-Ordner pro Reklamation | ⏳ |

### Phase 1c: Power Apps
| # | App | Zweck | Status |
|---|-----|-------|--------|
| 5 | Dashboard-View | Übersicht aller Reklamationen | ⏳ |
| 6 | Detail-View | Einzelne Reklamation bearbeiten | ⏳ |

### Phase 1d: HTML-Dashboard
| # | Komponente | Zweck | Status |
|---|------------|-------|--------|
| 7 | KPI-Cards | Offene, Kritische, Überfällige | ⏳ |
| 8 | Tabelle mit KST-Filter | Liste mit Sichtbarkeitslogik | ⏳ |

---

## 📅 ZEITPLAN

| Datum | Aufgabe |
|-------|---------|
| ✅ 22.12. | SharePoint Listen + Formulare |
| TBD | Power Automate: E-Mail-Import + QA-ID Generator |
| TBD | Power Automate: Alarm + Ordner-Sync |
| TBD | Power Apps |
| TBD | HTML-Dashboard |
| TBD | Testing |
| **02.01.2026** | **GO-LIVE MVP** |

---

*Erstellt: 22.12.2025*
