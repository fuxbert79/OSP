# NZA-System 2026 - Projektübersicht

**Stand:** 2026-02-05 (aktualisiert)
**Letzte Änderung:** Phase 4 - Email-Import-V3 mit Validierung
**Erstellt für:** AL (Andreas Löhr)
**E-Mail:** nza@schneider-kabelsatzbau.de
**Dashboard:** https://osp.schneider-kabelsatzbau.de/nza/

---

## 1. SYSTEM-ÜBERSICHT

### Was ist NZA?
**N**ach- und **Z**usatz**a**rbeiten - System zur Erfassung und Verwaltung von:
- **Nacharbeit:** Korrektur fehlerhafter Teile
- **Neufertigung:** Komplette Neuproduktion
- **Ausschuss:** Nicht reparierbare Teile

### Abgrenzung zu RMS

| Aspekt | RMS | NZA |
|--------|-----|-----|
| **Zweck** | Externe Reklamationen | Interne Nacharbeiten + Ausschuss |
| **E-Mail** | reklamation@schneider-kabelsatzbau.de | nza@schneider-kabelsatzbau.de |
| **ID-Format** | QA-JJNNN (QA-26001) | NZA-JJ-XXXX (NZA-26-0001) |
| **Verursacher** | Extern (Kunde/Lieferant) | Intern (MA aus nza-mitarbeiter) |
| **Kostenerfassung** | Nein | **Ja** (Minutensätze × Zeit) |
| **Bilder** | Optional | **Wichtig** (Fehlerfotos) |
| **SharePoint Site** | /sites/RMS | /sites/NZA_NEU |

### Verknüpfung RMS ↔ NZA
- Ein RMS-Vorgang kann einen NZA-Vorgang auslösen
- Feld `Bezug_RMS` in NZA verknüpft zur RMS QA-ID
- Kostentracking für Weiterbelastung an Lieferanten möglich

---

## 2. AKTUELLER STATUS (02/2026)

### Implementierungsfortschritt

| Phase | Beschreibung | Status |
|-------|--------------|--------|
| 1 | SharePoint-Listen erstellt | ✅ Fertig |
| 2 | n8n Workflows erstellt | ✅ Fertig (16 Workflows) |
| 3 | Dashboard 2026 HTML/CSS/JS | ✅ Fertig |
| 4 | Nginx-Endpoints konfiguriert | ✅ Fertig |
| 5 | n8n Workflows importiert | ⚠️ Teilweise (5/9 aktiv) |
| 6 | E-Mail-Import Workflow | ✅ **V3 fertig** (siehe Phase 4) |
| 7 | Dashboard-Erweiterung | ⏳ Nach API-Fixes |

### Phase 4: E-Mail-Import V3 (NEU - 2026-02-05)

| Feature | Status | Beschreibung |
|---------|--------|--------------|
| **Pflichtfeld-Validierung** | ✅ | Artikel-Nr, BA, Ausschuss, Fehlerbeschreibung, Fehlerkategorie, min. 1 Zusatzarbeit |
| **Duplikatsprüfung** | ✅ | Erkennung bei gleicher Artikel-Nr + Betriebsauftrag |
| **Multi-Attachment** | ✅ | Zusätzliche Dateien werden als Dokumente importiert |
| **Rejection-Email** | ✅ | Automatische Rücksendung bei unvollständigen Formularen |
| **Duplicate-Warning** | ✅ | Hinweis-Email bei möglichen Duplikaten |
| **spreadsheetFile Fix** | ✅ | typeVersion 4.5 → 2, operation toJson → fromFile |

**Workflow:** `nza/workflows/phase4/NZA-Email-Import-V3.json` (31 Nodes, aktiviert)

### n8n Workflow Status

**Funktionierend (5/9):**
| Workflow | Endpoint | Status |
|----------|----------|--------|
| NZA-Mitarbeiter-API | GET /webhook/nza-mitarbeiter | ✅ |
| NZA-Config-API | GET /webhook/nza-config | ✅ |
| NZA-KPIs-API | GET /webhook/nza-kpis | ✅ |
| NZA-Bilder-Upload | POST /webhook/nza-bilder-upload | ✅ |
| NZA-Notify-API | POST /webhook/nza-notify | ✅ |

**Nicht funktionierend (4/9) - MÜSSEN GEFIXT WERDEN:**
| Workflow | Problem |
|----------|---------|
| NZA-Prozesse-API | Webhook nicht registriert |
| NZA-Massnahmen-API | Webhook nicht registriert |
| NZA-Bilder-API | Webhook nicht registriert |
| NZA-Kosten-API | Webhook nicht registriert |

**Ursache:** Verwendung von `httpMethod: "*"` mit Method-Switch ist mit aktueller n8n-Version inkompatibel.

---

## 3. SHAREPOINT-STRUKTUR

### Site: /sites/NZA_NEU
**Team:** NZA
**Team-Email:** NZA1@schneider-kabelsatzbau.de

### Listen

| Liste | Zweck | Felder |
|-------|-------|--------|
| **nza-kpl** | Hauptliste (52 Spalten) | NZA-ID, Stammdaten, 5× Prozesse, Kosten |
| **nza-massnahmen** | Korrekturmaßnahmen | 13 Felder + Teams-Notify |
| **nza-bilder** | Fehlerfotos | 8 Felder |
| **nza-mitarbeiter** | Verursacher-Lookup | 9 Felder (53 MA) |
| **nza-config** | System-Konfiguration | 5 Felder (Minutensätze) |
| **nza-kpis** | Aggregierte Kennzahlen | 7 Felder |

### Environment-Variablen (docker-compose.yml)
```
NZA_SITE_ID=rainerschneiderkabelsatz.sharepoint.com,2a90f256-47e6-4ad1-b0d8-341026f63dc3,83b8240d-ea97-48ed-9d46-b510152e29f9
NZA_KPL_LIST_ID=7bea980d-9a33-4db5-a844-5c5401872e20
NZA_MITARBEITER_LIST_ID=d6dbfa5c-08b3-4bef-bc4a-e840f254935b
NZA_CONFIG_LIST_ID=6e56d7d5-c018-4948-a519-96230e5919bf
NZA_MASSNAHMEN_LIST_ID=d59ef6e6-428f-4346-a6e2-9524d61c14bc
NZA_BILDER_LIST_ID=60847793-da02-4e12-ad0f-052d6157b51e
```

---

## 4. HAUPTLISTE: nza-kpl (52 Felder)

### Stammdaten (17 Felder)
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| Title (NZA-ID) | Text | Auto: NZA-JJ-XXXX |
| Reklamationstyp | Choice | Interne/Kunden/Lieferanten Reklamation |
| Datum | DateTime | Erfassungsdatum |
| Artikel-Nr. | Text | Betroffener Artikel |
| Betriebsauftrag | Text | BA-Nummer |
| Prüfmenge | Number | Geprüfte Stückzahl |
| davon n.i.O. | Number | Fehlerhafte Stückzahl |
| Verursacher | Text | MA-Kürzel |
| Verursacher Personal-Nr. | Number | Personal-Nummer |
| Kostenstelle | Choice | 1000-5000, Lager, Verwaltung, Lieferant |
| QA-Nummer | Text | RMS-Bezug (QA-JJNNN) |
| Q-Nr. Kunde/Lieferant | Text | Externe Referenz |
| Ersatz BA | Text | Ersatz-Betriebsauftrag |
| Gutschrift/Belastung | Currency | Finanzielle Auswirkung |
| Fehler Beschreibung | Note | Detaillierte Fehlerbeschreibung |
| Fehler Kategorie | MultiChoice | Kategorisierung (12 Optionen) |
| Bemerkungen | Note | Zusätzliche Hinweise |

### Prozesse (30 Felder - 5× Prozess-Blöcke)
Jeder Block enthält:
- Prozess_X (Text)
- Werker_X (Text)
- Kostenstelle_X (Choice)
- Zeit_X_Min (Number)
- Faktor_X (Calculated)
- Kosten_X (Calculated)

### Kosten/Material (5 Felder)
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| kosten_sonstige | Currency | Sonstige Kosten |
| kosten_material | Currency | Materialkosten |
| kosten_prozesse | Calculated | Σ Prozesskosten |
| kosten_gesamt | Calculated | Totalkosten |
| Status | Choice | Bearbeitungsstatus |

---

## 5. KOSTENMODELL

### Minutensätze pro Kostenstelle
| KST | €/Min | €/Stunde |
|-----|-------|----------|
| 1000 | 1,98 | 118,80 |
| 2000 | 1,21 | 72,60 |
| 3000 | 0,93 | 55,80 |
| 4000 | 1,02 | 61,20 |
| 5000 | 1,02 | 61,20 |
| Lager | 1,10 | 66,00 |
| Verwaltung | 1,37 | 82,20 |

### Kostenberechnung
```
Kosten_Prozess_X = Zeit_X_Min × Minutensatz_KST × Faktor_X
Kosten_Prozesse = Σ(Kosten_Prozess_1..5)
Kosten_Gesamt = Kosten_Prozesse + Kosten_Material + Kosten_Sonstige
```

---

## 6. MITARBEITER (nza-mitarbeiter)

**53 aktive Mitarbeiter:**

| KST | Anzahl | Wichtige MA |
|-----|--------|-------------|
| Verwaltung | 9 | CS, CA, SV, AL, TS |
| 1000 | 5 | MD (FL), DS (Stv.) |
| 2000 | 9 | BS (FL 2000/3000), JR |
| 3000 | 13 | IB (Stv. FL) |
| 5000 | 12 | SK, DR (FL), WK |
| Lager | 3 | OK (Lagerleiter) |

**Datenquelle:** `/mnt/HC_Volume_104189729/osp/nza/daten/nza_mitarbeiter.csv`

---

## 7. E-MAIL-IMPORT (✅ IMPLEMENTIERT - V3)

### Postfach
- **E-Mail:** nza@schneider-kabelsatzbau.de
- **n8n Credential:** Microsoft Outlook NZA (y6bC8aYrlgPO6ZsG)

### E-Mail-Format
E-Mails enthalten ein ausgefülltes NZA-Formular (F-QM-04) als:
- Excel-Anhang (FQM04*.xlsx) - **primäre Methode**
- oder strukturierter E-Mail-Body

### Pflichtfelder (Validierung)
| Feld | Beschreibung | Fehler bei leer |
|------|--------------|-----------------|
| Artikel-Nr. | Betroffener Artikel | Rejection-Email |
| Betriebsauftrag | BA-Nummer | Rejection-Email |
| Ausschuss | davon n.i.O. Menge | Rejection-Email |
| Fehler Beschreibung | Detaillierte Beschreibung | Rejection-Email |
| Fehler Kategorie | Mind. 1 Kategorie | Rejection-Email |
| Zusatzarbeit | Mind. 1 Prozess-Zeile | Rejection-Email |

### Workflow-Logik (NZA-Email-Import-V3)
```
1. Schedule Trigger (alle 5 Min)
2. Microsoft Outlook: Get Messages (unread, nza@)
3. Filter: Nur E-Mails mit Excel-Anhang
4. Parse: Excel mit spreadsheetFile v2 (fromFile)
5. Validate: 6 Pflichtfelder prüfen
   ├── FAIL → Rejection-Email an Absender
   └── OK → weiter
6. Duplicate Check: Artikel-Nr + BA in SharePoint
   ├── FOUND → Warning-Email + trotzdem importieren
   └── NOT FOUND → weiter
7. Multi-Attachment: Zusätzliche Dateien → nza-bilder
8. Create: SharePoint-Item in nza-kpl
9. Generate: NZA-ID (NZA-JJ-XXXX)
10. Notify: Teams an Verantwortlichen
11. Mark as Read: Original-E-Mail
```

### Workflow-Dateien (Phase 4)
| Datei | Zweck |
|-------|-------|
| `NZA-Email-Import-V3.json` | Haupt-Workflow (31 Nodes) |
| `NZA-Validation-V2.json` | Standalone Validierung |
| `NZA-Import-Test-Validation.json` | Test-Workflow |

### Bekannte Probleme
- **E-Mail mit Anhang senden:** Docker-Dateizugriff-Problem in n8n (siehe `MAIL_ERROR.md`)

---

## 8. DASHBOARD 2026

### URL & Pfade
- **Produktiv:** https://osp.schneider-kabelsatzbau.de/nza/
- **Server:** /var/www/html/nza/
- **Entwicklung:** /mnt/HC_Volume_104189729/osp/nza/dashboard/

### Dateien
```
dashboard/
├── index.html      # Hauptseite (~58 KB)
├── css/
│   └── style.css   # Styling (OSP-CI)
├── js/
│   ├── app.js      # Haupt-Logik (~24 KB)
│   └── charts.js   # Chart.js Integration (~7 KB)
└── img/
    └── logo.png    # Schneider Logo
```

### KPI-Kacheln
1. **Offene NZA** - Status ≠ Abgeschlossen
2. **Kosten MTD** - Month-to-Date
3. **Kosten YTD** - Year-to-Date
4. **Ø Bearbeitungszeit** - Tage bis Abschluss

### Filter
- Suchfeld (NZA-ID, Artikel, Beschreibung)
- Typ (Nacharbeit, Neufertigung, Ausschuss)
- Status (Neu, In Bearbeitung, Abgeschlossen)
- Kostenstelle (1000-5000, Lager, Verwaltung)
- Zeitraum (Heute, Woche, Monat, Jahr)
- **Fehlerkategorie** (neu für 2026)

### Anpassungen für 2026 (aus daash.md)
1. ✅ OSP-CI-Design
2. ✅ Logo im Header
3. ⏳ KPIs reagieren auf Filter
4. ⏳ Fehlerkategorie-Filter
5. ✅ ID-Format: NZA-JJ-XXXX
6. ⏳ Nur Personalnummern anzeigen (keine Namen)
7. ✅ Max 20 Einträge pro Seite
8. ⏳ Fehlerbeschreibung oben im Detail-View
9. ⏳ Materialkosten editierbar
10. ⏳ KPI-Kachel "NZA-Kennzahl" statt "Top Kostenstelle"

---

## 9. API-ENDPOINTS

### Nginx-Konfiguration (osp.schneider-kabelsatzbau.de)

| Endpoint | Methode | Zweck | Status |
|----------|---------|-------|--------|
| /nza/ | - | Dashboard HTML | ✅ |
| /api/nza/prozesse | GET/POST/PATCH | Hauptliste CRUD | ❌ Fix needed |
| /api/nza/mitarbeiter | GET | Verursacher-Dropdown | ✅ |
| /api/nza/massnahmen | GET/POST/PATCH | Maßnahmen CRUD | ❌ Fix needed |
| /api/nza/notify | POST | Teams/E-Mail Notify | ✅ |
| /api/nza/bilder | GET | Bilder-Metadaten | ❌ Fix needed |
| /api/nza/bilder-upload | POST | Upload (max 20MB) | ✅ |
| /api/nza/kosten | GET/POST | Kostenberechnung | ❌ Fix needed |
| /api/nza/config | GET | Konfiguration | ✅ |
| /api/nza/kpis | GET | Dashboard-KPIs | ✅ |

---

## 10. FEHLERKATEGORIEN

MultiChoice-Feld mit 12 Optionen:
1. Crimpfehler
2. Längenabweichung
3. Verdrahtungsfehler
4. Bearbeitungsfehler
5. Druck fehlerhaft
6. Arbeitsanweisung falsch
7. Kundenzeichnung falsch
8. Falsches Material
9. Materialfehler
10. Werkzeug/Maschinenfehler
11. Lieferantenfehler/Reklamation
12. Sonstige

---

## 11. FORMBLATT F-QM-04

### Dateien
```
formulare/fqm04_nza/
├── F_QM_04_NZA.md              # Template-Dokumentation
├── F_QM_04_Schema.json         # JSON-Schema
├── FQM04_NZA.xlsx              # Excel-Vorlage
├── README.md                   # Anleitung
└── RMS_Prompt_F_QM_04_NZA.md   # KI-Prompt
```

### Zweck
- Interne Dokumentation von Fehlern/Nacharbeiten
- ISO 9001:2015 Kapitel 8.7 konform
- Eingabe-Formular für E-Mail an nza@

---

## 12. MICROSOFT 365 CREDENTIALS

| Credential | ID | Typ |
|------------|-----|-----|
| Microsoft SharePoint account | 5ZmmOyK1L7PhkJW2 | SharePoint OAuth2 |
| Microsoft Outlook NZA | y6bC8aYrlgPO6ZsG | Outlook OAuth2 |
| Microsoft Teams account | YckMuDdaL97hqHSG | Teams OAuth2 |
| Microsoft Drive account | RFliYFkYUYpnA7ki | Drive OAuth2 |

**Azure App:** OSP-n8n-Integration
**Client ID:** f99f47af-da3a-493c-aa17-e6b30e3b197c
**Tenant ID:** 31d02377-b699-4cef-a113-fc66e586df88

---

## 13. VERZEICHNISSTRUKTUR

```
/mnt/HC_Volume_104189729/osp/nza/
├── NZA.md                              # Diese Datei
├── NZA_System_Kontext.md               # Detaillierte Systemspezifikation
├── NZA_Datenbank_OSP_Integration.md    # Technische Details
├── API.md                              # API-Dokumentation
├── chat_claude_desktop.md              # Entwicklungs-Chat
├── daten/
│   ├── nza_mitarbeiter.csv             # 53 MA
│   └── nza_mitarbeiter.json            # JSON-Version
├── dashboard/
│   ├── index.html                      # Dashboard 2026
│   ├── css/style.css
│   ├── js/app.js
│   └── js/charts.js
├── docs/
│   ├── NZA_Systemreport_2026.md        # Audit-Report
│   ├── SharePoint_Listen_Spezifikation.md
│   ├── N8N_STATUS_20260131.md          # Workflow-Status
│   ├── NAECHSTE_SCHRITTE.md            # Aktionsplan
│   └── ...
├── formulare/fqm04_nza/
│   ├── F_QM_04_NZA.md
│   ├── FQM04_NZA.xlsx
│   └── ...
├── prompts/
│   └── NZA_N8N_INTEGRATION.md
├── workflows/
│   ├── 01_NZA_Setup_Listen.json        # Setup (einmalig)
│   ├── 02_NZA_Setup_Spalten_KPL_v2.json
│   ├── 03_NZA_Import_Mitarbeiter_v2.json
│   ├── 04_NZA_Import_Config_v2.json
│   ├── 05_NZA_Prozesse_API.json        # ❌ Fix needed
│   ├── 06_NZA_Mitarbeiter_API.json     # ✅
│   ├── 07_NZA_Massnahmen_API.json      # ❌ Fix needed
│   ├── 08_NZA_Bilder_API.json          # ❌ Fix needed
│   ├── 08b_NZA_Bilder_Upload.json      # ✅
│   ├── 09_NZA_Notify_API.json          # ✅
│   ├── 10_NZA_Kosten_API.json          # ❌ Fix needed
│   ├── 11_NZA_Config_API.json          # ✅
│   ├── 12_NZA_KPIs_API.json            # ✅
│   ├── phase4/                         # Optimierte Versionen
│   └── ...
└── 2025/
    ├── NZA_DB_2025.xlsx                # 2025er Daten (Archiv)
    ├── dashboard/
    │   ├── index.html                  # Dashboard 2025
    │   └── data.js                     # Statische Daten
    └── daash.md                        # Anpassungs-Anforderungen
```

---

## 14. ERWARTETE KPIs 2026

| Metrik | Erwartung | Ziel |
|--------|-----------|------|
| NZA-Vorgänge gesamt | 300-500 | < 400 |
| Gesamtkosten | 30.000-50.000 € | < 40.000 € |
| Ø Kosten/Vorgang | 80-120 € | < 100 € |
| Nacharbeit-Anteil | 60-70% | - |
| Neufertigung-Anteil | 20-30% | - |
| Ausschuss-Anteil | 5-15% | < 10% |

---

## 15. ISO 9001:2015 COMPLIANCE

| Kapitel | Anforderung | NZA-Umsetzung |
|---------|-------------|---------------|
| 8.7 | Lenkung nichtkonformer Ergebnisse | NZA-Erfassung + Klassifizierung |
| 10.2 | Nichtkonformität und Korrekturmaßnahmen | Maßnahmen-Tracking + Teams-Notify |
| 9.1.3 | Analyse und Bewertung | KPI-Dashboard + Kostenauswertung |

---

## NÄCHSTE SCHRITTE - ROADMAP

### Phase A: API-Fixes (PRIORITÄT 1)
1. [ ] NZA-Prozesse-API fixen (separate GET/POST/PATCH Workflows)
2. [ ] NZA-Massnahmen-API fixen
3. [ ] NZA-Bilder-API fixen
4. [ ] NZA-Kosten-API fixen

### Phase B: E-Mail-Import (✅ FERTIG - 2026-02-05)
5. [x] NZA-Email-Import-V3 Workflow erstellt
6. [x] Excel-Parser für F-QM-04 (spreadsheetFile v2)
7. [x] Auto-Generierung NZA-ID
8. [x] Teams-Benachrichtigung bei neuer NZA
9. [x] Pflichtfeld-Validierung (6 Felder)
10. [x] Duplikatsprüfung (Artikel-Nr + BA)
11. [x] Multi-Attachment-Handling
12. [x] Rejection-Email bei unvollständigen Formularen

### Phase C: Dashboard-Erweiterung (PRIORITÄT 2)
13. [ ] KPIs reagieren auf Filter
14. [ ] Fehlerkategorie-Filter
15. [ ] Personalnummern statt Namen
16. [ ] Detail-View optimieren
17. [ ] Materialkosten editierbar

### Phase D: Integration (PRIORITÄT 3)
18. [ ] RMS ↔ NZA Verknüpfung testen
19. [ ] Formblatt-Generator (F-QM-04 PDF)
20. [ ] End-to-End Tests
21. [ ] E-Mail mit Anhang senden fixen (siehe MAIL_ERROR.md)

---

*Erstellt: 2026-02-05*
*Autor: Claude Code für AL*
