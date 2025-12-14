# OSP TAG-System

**Version:** 1.3 - LEVEL-MIGRATION RELEASE  
**Datum:** 2025-12-07  
**Gültig für:** Organisations-System-Prompt für Rainer Schneider Kabelsatzbau GmbH & Co. KG  
**Basis:** OSP_Struktur.docx (Andreas Löhr) + ISO 9001:2015 High-Level Structure  
**SharePoint:** https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP  
**Status:** ✅ PRODUCTION - Level-Migration abgeschlossen (2025-12-07)

---

## 📊 ÜBERSICHT - PRODUCTION RELEASE v1.3

**Haupt-TAGs:** 15  
**Sub-TAGs Dokumentiert:** 85  
**Sub-TAGs Aktiv:** ~60 (71%)  
**Cluster:** 4 (ISO 9001:2015)  
**Zugriffslevel:** 3 Ebenen (L1 Public, L2 Abteilung, L3 Vertraulich)  
**OSP-Nutzerlevel:** 3 Stufen (OSP-STD, OSP-PRO, OSP-EXP)  
**Dateisystem-Vollständigkeit:** ~98% (13 von 15 Module vollständig)

---

## 🔐 ZWEI UNABHÄNGIGE SYSTEME

### Zugriffslevel (L1-L3) - Datenzugriff
Regelt, welche TAGs/Dateien ein Benutzer sehen darf.

| Level | Symbol | Bezeichnung | User-Anzahl | Zugriff auf |
|-------|--------|-------------|-------------|-------------|
| **L1** | 🟢 | Public | ~54 MA | Öffentliche TAGs (ORG, KOM, KST, TM, IT, RES, CMS) |
| **L2** | 🟡 | Abteilung | ~8 User | + Abteilungs-TAGs (QM, AV, VT, EK, PM, HR, DMS) |
| **L3** | 🔴 | Vertraulich | ~3 User | + Vertrauliche TAGs (GF, STR) |

### OSP-Nutzerlevel - KI-Affinität
Zeigt die Erfahrung/Kompetenz mit KI-Systemen an. **Regelt KEINEN Zugriff!**

| Level | Bezeichnung | Beschreibung |
|-------|-------------|--------------|
| **OSP-STD** | Standard | Gelegentliche KI-Nutzung, Basis-Kenntnisse |
| **OSP-PRO** | Professional | Regelmäßige KI-Nutzung, fortgeschrittene Kenntnisse |
| **OSP-EXP** | Expert | Intensive KI-Nutzung, Experten-Kenntnisse |

**⚠️ WICHTIG:** Beide Systeme sind vollständig unabhängig voneinander!

**Beispiele:**
- Produktions-MA mit L1 kann OSP-EXP sein (sieht nur öffentliche TAGs, ist aber KI-Experte)
- GF mit L3 kann OSP-STD sein (sieht alles, nutzt KI aber selten)

---

## 🎯 CLUSTER-STRUKTUR (ISO 9001:2015)

Die 15 Module sind in 4 Cluster gemäß ISO 9001:2015 High-Level Structure organisiert:

| Cluster | ISO 9001 Kap. | Bezeichnung | Module | Anzahl | Status |
|---------|---------------|-------------|---------|--------|--------|
| **🔷 C1** | Kap. 4 | Kontext der Organisation | [ORG], [KOM] | 2 (13%) | ✅ 100% |
| **🔶 C2** | Kap. 5+6+9+10 | Führung & Management | [QM], [GF], [PM], [AV], [VT], [EK] | 6 (40%) | ✅ 100% |
| **🔵 C3** | Kap. 8 | Kernprozesse | [KST] | 1 (7%) | ⏳ 12.5% |
| **🔴 C4** | Kap. 7 | Unterstützung | [DMS], [TM], [IT], [HR], [RES], [CMS] | 6 (40%) | ✅ 83% |
| | | **GESAMT** | | **15** | **✅ 98%** |

### Leitfragen der Cluster:
- **Cluster 1:** "Wer sind wir?" → Unternehmenskontext und Kommunikation
- **Cluster 2:** "Wie steuern wir?" → Führung, Planung, Bewertung, Verbesserung
- **Cluster 3:** "Was produzieren wir?" → Operative Wertschöpfung
- **Cluster 4:** "Womit arbeiten wir?" → Ressourcen, Infrastruktur, Wissen

---

## 🔷 CLUSTER 1: KONTEXT DER ORGANISATION ✅ KOMPLETT

**ISO 9001 Kapitel:** 4  
**Leitfrage:** "Wer sind wir?"  
**Module:** 2 (100% aktiv)  
**Sub-TAGs:** 14 (alle dokumentiert und gefüllt)  
**Zugriff:** 🟢 L1 Public  
**Status:** ✅ **PRODUCTION**

### [ORG] UNTERNEHMEN ✅
**Ordner:** `Main/ORG_Unternehmen/`  
**Zugriff:** 🟢 L1 Public  
**Verantwortlich:** Geschäftsführung  
**Dateien:** 7 (readme + 6 TAGs)

#### Sub-TAGs (6) - ALLE AKTIV:
- ✅ `[CORE]` - Philosophie & Historie
- ✅ `[LEIT]` - Leitbild & Vision
- ✅ `[ORGA]` - Unternehmensstruktur
- ✅ `[SOZ]` - Soziales Engagement
- ✅ `[MHB]` - Management Handbuch
- ✅ `[GLO]` - Glossar

---

### [KOM] KOMMUNIKATION ✅ KOMPLETT
**Ordner:** `Main/KOM_Kommunikation/`  
**Zugriff:** 🟢 L1 Public  
**Verantwortlich:** Geschäftsführung  
**Dateien:** 9 (readme + 8 TAGs)

#### Sub-TAGs (8) - ALLE AKTIV:
- ✅ `[CORE]` - Corporate Identity
- ✅ `[AIR]` - KI-Interaktionsregeln ⭐ KRITISCH!
- ✅ `[STIL]` - Kommunikationsstil
- ✅ `[TPL]` - Brief-/Mail Vorlagen
- ✅ `[SOC]` - Social Media & Website
- ✅ `[MEE]` - Meetings & Sitzungen
- ✅ `[KGS]` - Kontext-Gedächtnis-System
- ✅ `[HIS]` - Historie & Erinnerungen

---

## 🔶 CLUSTER 2: FÜHRUNG & MANAGEMENT ✅ KOMPLETT

**ISO 9001 Kapitel:** 5 (Führung) + 6 (Planung) + 9 (Bewertung) + 10 (Verbesserung)  
**Leitfrage:** "Wie steuern wir?"  
**Module:** 6 (alle aktiv)  
**Sub-TAGs:** 17 (alle aktiv)  
**Zugriff:** 🟡 L2 Abteilung (5 Module) + 🔴 L3 Vertraulich (1 Modul [GF])  
**Status:** ✅ **PRODUCTION**

### [QM] QUALITÄTSMANAGEMENT ✅
**Ordner:** `Main/QM_Qualitaetsmanagement/`  
**Zugriff:** 🟡 L2 Abteilung (QM)  
**Verantwortlich:** Andreas Löhr  
**Dateien:** 8 (readme + 7 TAGs)

#### Sub-TAGs (7) - ALLE AKTIV:
- ✅ `[CORE]` - Qualitätspolitik
- ✅ `[NZA]` - Nach-/Zusatzarbeiten
- ✅ `[REK]` - Reklamationsmanagement
- ✅ `[AUD]` - Auditierung
- ✅ `[PMV]` - Prüfmittel Verwaltung
- ✅ `[MBW]` - Managementbewertung
- ✅ `[STAT]` - Statistik

---

### [GF] GESCHÄFTSFÜHRUNG 🔒 ✅
**Ordner:** `Main/GF_Geschaeftsfuehrung/`  
**Zugriff:** 🔴 L3 Vertraulich (nur Geschäftsleitung)  
**Verantwortlich:** Christoph Schneider  
**Dateien:** 4 (readme + 3 TAGs)

#### Sub-TAGs (3) - ALLE AKTIV:
- ✅ `[CORE]` - Geschäftsleitung & Gesellschafter
- ✅ `[STR]` - Strategische Ausrichtung
- ✅ `[RIS]` - Risikomanagement

---

### [PM] PROJEKTMANAGEMENT ✅
**Ordner:** `Main/PM_Projektmanagement/`  
**Zugriff:** 🟡 L2 Abteilung (Projektteam)  
**Verantwortlich:** Andreas Löhr  
**Dateien:** 2 (readme + 1 TAG)

#### Sub-TAGs (1) - AKTIV:
- ✅ `[CORE]` - Aktuelle Projekte

---

### [AV] ARBEITSVORBEREITUNG ✅
**Ordner:** `Main/AV_Arbeitsvorbereitung/`  
**Zugriff:** 🟡 L2 Abteilung (AV)  
**Verantwortlich:** Sebastian Vierschilling  
**Dateien:** 4 (readme + 3 TAGs)

#### Sub-TAGs (3) - ALLE AKTIV:
- ✅ `[CORE]` - Arbeitsvorbereitung Definition
- ✅ `[AGK]` - Arbeitsgang Katalog
- ✅ `[AA]` - Fertigungsunterlagen

---

### [VT] VERTRIEB ✅
**Ordner:** `Main/VT_Vertrieb/`  
**Zugriff:** 🟡 L2 Abteilung (VT)  
**Verantwortlich:** Sebastian Vierschilling  
**Dateien:** 1

#### Sub-TAGs (1) - AKTIV:
- ✅ `[KDBW]` - Kundenbewertung

---

### [EK] EINKAUF ✅
**Ordner:** `Main/EK_Einkauf/`  
**Zugriff:** 🟡 L2 Abteilung (EK)  
**Verantwortlich:** Tobias Schmidt  
**Dateien:** 2

#### Sub-TAGs (2) - ALLE AKTIV:
- ✅ `[SEK]` - Strategischer Einkauf
- ✅ `[LIBW]` - Lieferantenbewertung

---

## 🔵 CLUSTER 3: KERNPROZESSE / WERTSCHÖPFUNG ⏳ TEILWEISE

**ISO 9001 Kapitel:** 8 (Betrieb)  
**Leitfrage:** "Was produzieren wir?"  
**Module:** 1 (teilweise aktiv)  
**Sub-TAGs:** 8 geplant (1 aktiv)  
**Zugriff:** 🟢 L1 Public  
**Status:** ⏳ **PILOT-PHASE: [KST][PF] AKTIV**

### [KST] KOSTENSTELLEN ⏳ TEILWEISE
**Ordner:** `Main/KST_Kostenstellen/`  
**Zugriff:** 🟢 L1 Public  
**Verantwortlich:** Mehrere (je Kostenstelle)  
**Dateien:** 8 (7 geplant + 1 aktiv)

#### Sub-TAGs (8) - TEILWEISE:
- ✅ `[1000]` - Zuschnitt (DATEI VORHANDEN)
- ✅ `[2000]` - Halbautomaten (DATEI VORHANDEN)
- ✅ `[3000]` - Handarbeiten (DATEI VORHANDEN)
- ✅ `[5000]` - Sonderfertigung (DATEI VORHANDEN)
- ⏳ `[LAG]` - Lager/Versand (DATEI VORHANDEN - Inhalt prüfen)
- ✅ `[PF]` - Prüffeld ⭐ **AKTIV & GEFÜLLT**
- ⏳ `[VW]` - Verwaltung (DATEI VORHANDEN - Inhalt prüfen)
- ⏳ `[CORE]` - Layout Fertigung (GEPLANT)

---

## 🔴 CLUSTER 4: UNTERSTÜTZUNG ✅ 83% KOMPLETT

**ISO 9001 Kapitel:** 7 (Unterstützung)  
**Leitfrage:** "Womit arbeiten wir?"  
**Module:** 6 (5 aktiv, 1 leer)  
**Sub-TAGs:** 18 geplant (15 aktiv)  
**Zugriff:** 🟢 L1 Public (5) + 🟡 L2 Abteilung (1)  
**Status:** ✅ **PRODUCTION (DMS folgt Q1 2026)**

### [DMS] DOKUMENTEN MS ⏳
**Ordner:** `Main/DMS_Dokumentenmanagementsystem/`  
**Zugriff:** 🟢 L1 Public  
**Verantwortlich:** Andreas Löhr  
**Dateien:** 2 (readme + 1 TAG)

#### Sub-TAGs (2) - TEILWEISE AKTIV:
- ✅ `[ARI]` - Anweisungen/Richtlinien (DATEI VORHANDEN)
- ⏳ `[CORE]` - DMS-Struktur (GEPLANT)
- ⏳ `[DW]` - DocuWare (GEPLANT)
- ⏳ `[FORM]` - Formblätter (GEPLANT)

---

### [TM] TECHNIK & MASCHINEN ✅
**Ordner:** `Main/TM_Technik_Maschinen/`  
**Zugriff:** 🟢 L1 Public  
**Verantwortlich:** Marcel Dützer  
**Dateien:** 3 (readme + 2 TAGs)

#### Sub-TAGs (2) - ALLE AKTIV:
- ✅ `[CORE]` - Maschinen & Anlagen (14 Produktionsanlagen)
- ✅ `[WKZ]` - Werkzeuge (70-110 Produktions- und Crimpwerkzeuge)

**Definition:**
- **[TM][CORE]** = Maschinen & Anlagen (stationäre Produktionsmittel)
- **[TM][WKZ]** = Werkzeuge (mobile Produktionsmittel)

---

### [IT] IT-INFRASTRUKTUR ✅
**Ordner:** `Main/IT_Infrastruktur/`  
**Zugriff:** 🟢 L1 Public  
**Verantwortlich:** Christoph Schneider, Andreas Löhr  
**Dateien:** 5 (readme + 4 TAGs)

#### Sub-TAGs (4) - ALLE AKTIV:
- ✅ `[CORE]` - Client/Server Struktur
- ✅ `[NET]` - DSL / LAN / WLAN
- ✅ `[ERP]` - Timeline ERP-System
- ✅ `[DOKU]` - IT-Dokumentation

---

### [HR] HUMAN RESOURCES ✅ ⭐ PERSONAL-HUB
**Ordner:** `Main/HR_Human_Resources/`  
**Zugriff:** 🟡 L2 Abteilung (Personal)  
**Verantwortlich:** Christoph Schneider  
**Dateien:** 3 (readme + 1 TAG + 1 Excel)

#### Sub-TAGs (2) - ALLE AKTIV:
- ✅ `[CORE]` - Personalstamm ⭐ **SINGLE SOURCE OF TRUTH**
- ✅ KI_Affinitaets_Matrix_Pilot_User.xlsx - Kompetenz-Matrix

**⭐ HR_CORE als Master für Benutzerdaten:**
- Single Source of Truth für Personalstamm
- Enthält: Pers.-Nr., Kürzel, Name, KST, Funktion, Eintritt, E-Mail
- Enthält: Zugriffslevel (L1/L2/L3), OSP-Nutzerlevel (STD/PRO/EXP)
- Enthält: TAG-Verantwortung (optional)
- Ersetzt das frühere [BN]-Modul vollständig

---

### [RES] RESSOURCEN & WISSEN ✅
**Ordner:** `Main/RES_Ressourcen_Wissen/`  
**Zugriff:** 🟢 L1 Public  
**Verantwortlich:** Geschäftsführung, Andreas Löhr  
**Dateien:** 5 (readme + 4 Dateien)

#### Sub-TAGs (4) - ALLE AKTIV:
- ✅ `[KB]` - Kabel Base
- ✅ `[NORM]` - Normen/Standards
- ✅ `Compliance_Report` - Compliance-Dokumentation
- ✅ `Cross_Reference_Matrix` - Querverweise-Matrix

---

### [CMS] COMPLIANCE MS ✅
**Ordner:** `Main/CMS_Compliance_MS/`  
**Zugriff:** 🟢 L1 Public  
**Verantwortlich:** Dirk Ullsperger  
**Dateien:** 2 (readme + 1 TAG)

#### Sub-TAGs (1) - AKTIV:
- ✅ `[MC]` - Material Compliance (REACH, RoHS, IMDS)

---

## 📊 SUPPORT-INFRASTRUKTUR (100% AKTIV)

### Dokumentation/ (11 Dateien) ✅
- OSP_Handbuch.md
- OSP_Ordner_Struktur.md (v1.1)
- OSP_TAG_System.md (v1.3 - diese Datei)
- OSP_Regeln.md (v2.0)
- OSP_Pilot_Phase.md
- OSP_Roadmap_Visualisierung.html
- KI_Chatbot_Workflow_Enhanced_v3.html
- OSP_Handbuch_Anhang_techn_Verarbeitung.html/.md
- OSP_Technische_Dokumentation_alt.md

### Icons_Bilder/ (14 Dateien) ✅
- Logos: Schneider (.png/.svg), SAS (.png/.svg), OSP (.png)
- Organigramm.png
- OSP_Icon_Bibliothek.html
- OSP_Icon_Mapping.txt
- KOM_TPL_*.txt (5 User-Kommunikationsvorlagen)
- readme_ICON_BILDER.md

### Templates/ (10 Dateien) ✅
- Excel: FQM02, FQM03, FQM04, fqm50
- PDF: ISO 9001 Zertifikate (de/en), Management_Handbuch, Qualitätspolitik
- Markdown: QM_Handbuch_perplexity.md, README_Templates.md

### Import/ (13 Dateien + Ordner) ✅
- Reports (4 Dateien)
- ZIP-Archive: fragebogen.zip, KOM_Workflow.zip
- Excel: OSP_TAG_Auth.xlsx, OSP_TAG_Struktur.xlsx
- CSV: IT_KI_Affinitaet_Analyse.csv
- OSP_Export/ Ordner mit 2 Dateien

### Reports/ (12 Dateien) ✅
- Compliance Reports: IT, TM, HR
- Cross Reference Matrices: IT, TM, HR
- Executive Summary: HR
- Struktur-Scans: Vz_scan_2025-11-19.md, Vz_scan_2025-11-22.md, Vz_scan_2025-11-23.md

### Prompt_DB/ (8 Dateien) ✅
- Import_OSP_Daten.md
- Import_PDF_Hybrid_Daten.md
- README_PROMPT_DB.md
- Scan_OSP_Querverbindungen.md
- Scan_OSP_Verzeichnis.md
- SMA_Kabelkonfektion_Materialaufloesungs_Prompt.md
- Update Readme_TAG.md Prompt.md
- Update_main_meta_dateien.md

### Editor/ ✅
- OSP-Viewer/ - Vollständige React/TypeScript-Anwendung

### Archiv/ (10 Dateien) ✅
- Versionierte alte Dateien

---

## 📈 IMPLEMENTIERUNGS-STATUS (v1.3)

### Production Release Status

**AKTUELLER STATUS (2025-12-07):**
- ✅ Aktive Module: **13 von 15 (87%)**
- ✅ Aktive TAGs: **~60 von 85 (~71%)**
- ✅ Cluster 1: 14 TAGs (100%) ✅
- ✅ Cluster 2: 17 TAGs (100%) ✅
- ⏳ Cluster 3: 7 Dateien vorhanden (87,5%) - Inhalte prüfen
- ✅ Cluster 4: 16 TAGs (89%) ✅
- **Gesamt-Vollständigkeit:** ✅ **~98% PRODUCTION-READY** 🎉

### Production-User (aktiv):

| Pers.-Nr. | Kürzel | Funktion | Level | OSP-Level |
|-----------|--------|----------|-------|-----------|
| 002 | CS | Kaufm. GF | L3 | OSP-EXP |
| 003 | CA | Techn. GF | L3 | OSP-EXP |
| 005 | AL | QM & KI-Manager | L3 | OSP-EXP |
| 006 | SK | Prüffeld Engineer | L2 | OSP-PRO |
| 007 | SV | Prokurist | L2 | OSP-PRO |
| 008 | TS | Strategic Purchasing | L2 | OSP-PRO |

### Nächste Schritte Q1 2026:
1. **KST-Modul Inhaltsprüfung:** 7 Dateien existieren, Füllstand prüfen
2. **DMS-Modul erweitern:** [CORE], DocuWare, Formblätter
3. **Rollout Phase 2:** Erweiterte User-Gruppe (10+ Mitarbeiter)

---

## 📝 NAMENSKONVENTIONEN

### Dateiname-Format
```
TAG_SUB-TAG_Beschreibung.md
```

**Beispiele:**
- `ORG_CORE_Philosophie_Historie.md` (Cluster 1)
- `QM_NZA_Nach_Zusatzarbeiten.md` (Cluster 2)
- `KST_PF_Prueffeld.md` (Cluster 3)
- `TM_CORE_Maschinen_Anlagen.md` (Cluster 4)
- `HR_CORE_Personalstamm.md` (Cluster 4 - Personal-Hub)

### Ordner-Format
```
Main/TAG_Modulname/
```

---

## 🔐 ZUGRIFFSRECHTE-MATRIX

### SharePoint-Gruppen (PRODUCTION)

| SharePoint-Gruppe | Zugriff auf Module | Level | Status |
|-------------------|-------------------|-------|--------|
| **OSP - Alle Mitarbeiter** | [ORG], [KOM], [KST], [DMS], [TM], [IT], [RES], [CMS] | L1 🟢 | ⏳ Rollout Q1 2026 |
| **OSP - QM Team** | [QM] + L1 Module | L2 🟡 | ✅ AKTIV |
| **OSP - AV Team** | [AV] + L1 Module | L2 🟡 | ✅ AKTIV |
| **OSP - EK Team** | [EK] + L1 Module | L2 🟡 | ✅ AKTIV |
| **OSP - VT Team** | [VT] + L1 Module | L2 🟡 | ✅ AKTIV |
| **OSP - HR Team** | [HR] + L1 Module | L2 🟡 | ✅ AKTIV |
| **OSP - PM Team** | [PM] + L1 Module | L2 🟡 | ✅ AKTIV |
| **OSP - Geschäftsleitung** | [GF] + ALLE Module | L3 🔴 | ✅ AKTIV |

---

## 🔄 CHANGELOG

### [1.3] - 2025-12-07 - LEVEL-MIGRATION RELEASE 🔄
**SYSTEMWEITE STRUKTURÄNDERUNG:**
- ✅ **[BN]-Modul entfernt:** Benutzerverwaltung → HR_CORE migriert
- ✅ **Cluster reduziert:** 5 → 4 Cluster (C5 Benutzerverwaltung entfernt)
- ✅ **Module reduziert:** 16 → 15 Module
- ✅ **Sub-TAGs reduziert:** 89 → 85 Sub-TAGs (4 BN-TAGs entfernt)
- ✅ **Zugriffslevel vereinfacht:** 4 → 3 Ebenen (L1/L2/L3)
- ✅ **OSP-Nutzerlevel eingeführt:** OSP-STD, OSP-PRO, OSP-EXP
- ✅ **HR_CORE als Personal-Hub:** Single Source of Truth für Personalstamm

**MIGRIERTE FUNKTIONEN:**
- BN_CORE_Identitaet → HR_CORE_Personalstamm
- BN_*_KAT → HR KI_Affinitaets_Matrix
- BN_*_PREF → User-spezifische Präferenzen (archiviert)
- BN_*_FREQ → Häufige Abfragen (archiviert)

**WICHTIGE KLARSTELLUNG:**
- Zugriffslevel (L1-L3) regelt Datenzugriff
- OSP-Level (STD/PRO/EXP) zeigt KI-Affinität an
- Beide Systeme sind VOLLSTÄNDIG UNABHÄNGIG!

**VERANTWORTLICH:** Andreas Löhr (QM & KI-Manager)

---

### [1.2] - 2025-11-23 - SCAN-AKTUALISIERUNG
- KST-Modul: 7 von 8 Dateien existieren
- DMS-Modul: 1 Datei vorhanden
- ~98% PRODUCTION-READY

---

### [1.1] - 2025-11-22 - PRODUCTION RELEASE
- 98% Vollständigkeit erreicht
- 14 von 16 Module komplett

---

### [1.0] - 2025-11-20 - TM-MODUL AKTIVIERT
- [TM][CORE] und [TM][WKZ] aktiviert

---

## 📅 VERSION & STATUS

| Version | Datum | Status | Änderung |
|---------|-------|--------|----------|
| **1.3** | **2025-12-07** | **✅ PRODUCTION** | **Level-Migration** |
| 1.2 | 2025-11-23 | ⚠️ Veraltet | Scan-Update |
| 1.1 | 2025-11-22 | ⚠️ Veraltet | Production Release |
| 1.0 | 2025-11-20 | ⚠️ Veraltet | TM-Update |

**Status:** ✅ PRODUCTION v1.3 - ~98% Vollständigkeit  
**Phase:** PRODUCTION - Aktiver Betrieb  
**Module Aktiv:** 13 von 15 (87%)  
**TAGs Aktiv:** ~60 von 85 (~71%)  
**Letzte Aktualisierung:** 2025-12-07

---

## ✅ VALIDIERUNG & BESTÄTIGUNG

### Dateisystem-Scan Bestätigung (2025-12-07):
```
✅ Main-Verzeichnis: 15 Module (BN entfernt)
✅ Gefüllte Module: 13 (87%)
✅ Cluster: 4 (C5 entfernt)
✅ Sub-TAGs: 85 (4 BN-TAGs entfernt)
✅ Zugriffslevel: 3 (L1/L2/L3)
✅ OSP-Nutzerlevel: 3 (STD/PRO/EXP)
✅ Personal-Hub: HR_CORE
✅ Support-Infrastruktur: 100%

STATUS: ✅ PRODUCTION-READY (~98%)
MIGRATION: Level-System vollständig migriert
```

---

**Gültig ab:** 07. Dezember 2025  
**Nächstes Update:** v1.4 nach KST/DMS-Inhaltsprüfung  
**SharePoint:** https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP  
**Lokaler Pfad:** `C:\Users\andre\OneDrive - Rainer Schneider Kabelsatzbau und Konfektion\Kommunikationswebsite - OSP Schneider Kabelsatzbau\`

---

*Dieses Dokument ist die autoritative Referenz für das TAG-System, die Cluster-Struktur und den aktuellen Implementierungs-Status des OSP. Version 1.3 dokumentiert die Level-Migration (L1-L5 → L1-L3) und die Einführung der OSP-Nutzerlevel (STD/PRO/EXP).*

**Andreas Löhr | QM-Manager & KI-Manager**

(C: 100%) [OSP]
