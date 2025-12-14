# OSP-Regeln und Governance

**Version:** 2.0  
**Erstellt:** 2025-11-09  
**Zuletzt aktualisiert:** 2025-12-05  
**Gültig für:** Organisations-System-Prompt (OSP) für Rainer Schneider Kabelsatzbau GmbH & Co. KG  
**Basis:** OSP_TAG_System.md v1.0 + OSP_Ordner_Struktur.md v1.0 + ISO 9001:2015  
**SharePoint:** https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP  
**Status:** ✅ ERWEITERT MIT OSP-NUTZERLEVEL (v2.0)  

---

## 🔄 MIGRATIONS-HINWEIS (2025-12-07)

> **⚠️ WICHTIG - ARCHITEKTUR-MIGRATION:**
>
> Folgende Regeln wurden am **07.12.2025** in die neue OSP-Architektur migriert:
>
> | Regel | Ziel-Datei | Status |
> |-------|------------|--------|
> | **Regel 16** (Dateibenennungs-Standard) | `API_System_Prompt_KONSOLIDIERT.md` | ✅ Migriert |
> | **Regel 30** (KI-Chatbot-Workflow) | `API_System_Prompt_KONSOLIDIERT.md` | ✅ Migriert |
> | **Regel 31** (OSP-Nutzerlevel) | `OpenWebUI_Users_Config.yaml` | ✅ Migriert |
> | **Regel 27** (NULL-FEHLER-POLITIK) | `API_System_Prompt_KONSOLIDIERT.md` | ✅ Migriert |
> | **Regel 28** (Doppel-Kennzeichnung) | `API_System_Prompt_KONSOLIDIERT.md` | ✅ Migriert |
>
> **Neue Architektur:**
> - **Frontend:** Open WebUI (46.224.102.30:3000)
> - **RAG:** ChromaDB (46.224.102.30:8000)
> - **KI-Backend:** Claude API mit konsolidiertem System-Prompt
>
> **Dieses Dokument dient weiterhin als:**
> - 📋 **Governance-Referenz** für Mitarbeiter
> - 📊 **Audit-Dokumentation** (ISO 9001)
> - 🔍 **RAG-Quelle** (ChromaDB-indiziert)
>
> **Migrations-Dateien (auf Hetzner Server):**
> - `API_System_Prompt_KONSOLIDIERT.md` (~6.500 Tokens)
> - `ChromaDB_Config_Schema.yaml`
> - `OpenWebUI_Users_Config.yaml` (18 User)
> - `RAG_Metadata_Schema.yaml`
> - `ChromaDB_Wissen_Collections/` (3 YAML-Dateien)
>
> **Migration durchgeführt von:** AL (QM & KI-Manager)

---

## 📑 INHALTSVERZEICHNIS

1. [🎯 KRITISCHE ÄNDERUNGEN V2.0](#-kritische-änderungen-v20)
2. [🏛️ GRUNDPRINZIPIEN](#️-grundprinzipien)
3. [🔄 MIGRATION UND VERIFIZIERUNG](#-migration-und-verifizierung)
4. [📁 NEUE OSP-KOMPONENTEN](#-neue-osp-komponenten)
5. [📄 AUTOMATISCHE UPDATES UND SYNCHRONISATION](#-automatische-updates-und-synchronisation)
6. [📅 PERIODISCHE WARTUNGSZYKLEN](#-periodische-wartungszyklen)
7. [📋 OSP-SPEZIFISCHE ZUSATZREGELN](#-osp-spezifische-zusatzregeln)
8. [🔍 QUALITÄTSSICHERUNG](#-qualitätssicherung)
9. [🚨 ESKALATIONSPFADE](#-eskalationspfade)
10. [📊 REPORTING-STANDARDS](#-reporting-standards)
11. [📝 ÄNDERUNGSHISTORIE](#-änderungshistorie)
12. [📋 DEFINITIONS-GLOSSAR](#-definitions-glossar-meta-dateien-und-main-dateien)

---

## 🎯 KRITISCHE ÄNDERUNGEN V2.0

### Neue Erweiterung implementiert (v2.0):
- ✅ **REGEL 31 NEU:** OSP-Nutzerlevel (OSP-STD, OSP-PRO, OSP-EXP)
- ✅ **Abgrenzung definiert:** OSP-Level vs. Zugriffslevel (L1-L3)
- ✅ **HR_CORE-Integration:** Personalstamm mit OSP-Level-Spalte

### Regeln aus V1.9:
- ✅ **REGEL 30:** KI-Chatbot-Workflow-Governance (4 Phasen, 11 Schritte)
- ✅ **Berechtigungsmatrix:** L1-L5 Kompetenz-Level definiert
- ✅ **Benutzererkennung:** Integration mit HR_CORE
- ✅ **TAG-Validierung:** Phantasie-TAG-Detection implementiert
- ✅ **NULL-FEHLER-POLITIK:** Erweitert um Punkt 5 "Validieren > Erfinden"
- ✅ **Performance-KPIs:** Zielwerte und kritische Schwellen
- ✅ **Monitoring:** Real-Time und wöchentliche Reports
- ✅ **Eskalationspfade:** 4-stufiges System
- ✅ **Querverweise:** Zu KOM_AIR_KI_Kommunikationsregeln.md v2.7

### Regeln aus V1.8:
- ✅ **Rückverweise:** zu  HR-Modul etabliert

### Regeln aus V1.7:
- ✅ **TM-MODUL AKTIVIERT:** [TM][CORE] Maschinen & Anlagen + [TM][WKZ] Werkzeuge
- ✅ **Gesamt Sub-TAGs:** 86 → 89 (+3 durch Cluster 5 v1.0)
- ✅ **Aktive Sub-TAGs:** 20 → 22 (+2 durch TM-Modul)

### Regeln aus V1.6:
- ✅ **Regel 16 KOMPLETT REWRITTEN:** Dateibenennungs-Konvention TAG_SUB-TAG_Name.md
- ✅ Standardisierte Namensschema für alle OSP-Markdown-Dateien
- ✅ Umlaut-Konvertierung (ä→ae, ö→oe, ü→ue) definiert
- ✅ Migrationsleitfaden für bestehende Dateien

### Regeln aus V1.5:
- ✅ **Regel 29:** Definitions-Glossar für Meta-Dateien und Main-Dateien

### Regeln aus V1.4:
- ✅ **Regel 23 ERWEITERT:** Chat-Reset-Prävention für Claude Desktop (2er-Pakete-Strategie)

---

## 🏛️ GRUNDPRINZIPIEN

### 1. Hierarchie
**Autoritative Dokumente (in absteigender Priorität):**
1. OSP_TAG_System.md (aktuelle Version) - Single Source of Truth für TAGs
2. OSP_Ordner_Struktur.md - Definitive Struktur
3. OSP_Regeln.md (dieses Dokument) - Governance-Regeln
4. Main-Ordner Dateien - Operative Inhalte
5. Upload-/Import-Dateien - Nur Entwürfe

### 2. Multi-User-Konformität
- 60 Mitarbeiter gesamt, 20 PC-Arbeitsplätze (max. 20 OSP-Nutzer)
- SharePoint-Integration zwingend
- Berechtigungsstufen beachten
- DSGVO-Compliance erforderlich

### 3. Versionskonsistenz
- Semantic Versioning (Major.Minor.Patch)
- Changelog bei jeder Änderung
- Keine lokalen Abweichungen
- Git-ähnliche Kontrolle

### 4. Audit-Trail
- Jede Änderung dokumentiert
- Verantwortlicher genannt
- Zeitstempel vorhanden
- Grund der Änderung

### 5. Automatisierung vor Manuell
- PowerShell-Scripts nutzen
- SharePoint-Workflows
- Scheduled Tasks
- Minimale manuelle Eingriffe

---

## 🔄 MIGRATION UND VERIFIZIERUNG

### 6. Migration PSP → OSP
**Prozess:**
1. Regel aus PSP identifizieren
2. Multi-User-Tauglichkeit prüfen
3. OSP-spezifisch anpassen
4. In OSP_Regeln.md integrieren
5. Pilot-Test mit 5 Usern
6. Rollout auf max. 20 OSP-Nutzer (PC-Arbeitsplätze)

**Nicht übertragbar aus PSP:**
- Persönliche Präferenzen
- Single-User-Workflows
- Private Notizen
- Lokale Pfade

### 7. Verifizierung neuer Regeln
**Checkliste vor Implementierung:**
- [ ] ISO 9001:2015 konform?
- [ ] DSGVO-konform?
- [ ] SharePoint-kompatibel?
- [ ] Multi-User-tauglich?
- [ ] Automatisierbar?
- [ ] Messbare KPIs definiert?
- [ ] Eskalationspfad vorhanden?

---

## 📁 NEUE OSP-KOMPONENTEN

### 8. Index.md
**Zweck:** Zentrale Navigation aller Module
**Inhalt:**
- Komplette Modul-Übersicht (16 Module)
- Sub-TAG-Liste (89 Sub-TAGs)
- Recent Updates
- Quick Links
**Update:** Bei jeder Strukturänderung

### 9. Implementierungs_monitor.md
**Zweck:** Fortschritts-Tracking
**Inhalt:**
- Module-Status (Draft/Review/Active)
- Completion-Percentage
- Blockaden
- Next Actions
**Update:** Wöchentlich

### 10. OSP_Netz.md
**Zweck:** Querverweise-Visualisierung
**Inhalt:**
- Multi-Layer-Netzwerk
- Bidirektionale Links
- Cluster-Verbindungen
- YAML-Export für Tools
**Update:** Bei jedem neuen Querverweis

### 11. readme_[SUB-TAG].md
**Zweck:** Lokale Dokumentation pro Sub-TAG
**Inhalt:**
- Datei-Liste im Sub-TAG
- Kurzbeschreibungen
- Querverweise lokal
- Verantwortlicher
**Update:** Bei Content-Änderungen

---

## 📄 AUTOMATISCHE UPDATES UND SYNCHRONISATION

### 12. SharePoint-Sync
**Frequenz:** Real-time (OneDrive)
**Backup:** Täglich 23:00
**Versionierung:** Automatisch (30 Tage History)
**Konflikt-Lösung:** Neueste Version gewinnt

### 13. Cross-Referenz-Check
**Tool:** PowerShell-Script
**Frequenz:** Täglich 06:00
**Output:** Broken-Links-Report
**Auto-Fix:** Einseitige Links → Bidirektional

### 14. Compliance-Monitoring
**ISO 9001:** Quartalsweise Audit
**DSGVO:** Monatlich
**Zugriffsrechte:** Wöchentlich
**Logs:** 5 Jahre Aufbewahrung

---

## 📅 PERIODISCHE WARTUNGSZYKLEN

| Zyklus | Aufgabe | Verantwortlich | Tool |
|--------|---------|----------------|------|
| **Täglich** | Backup, Link-Check | System | PowerShell |
| **Wöchentlich** | PSP-OSP-Sync, KGS-Aggregation | System | Scheduled Task |
| **Monatlich** | DSGVO-Check, Success-Patterns | QM | Manual + Script |
| **Quartal** | ISO-Audit, Struktur-Review | QM | Checkliste |
| **Jährlich** | Komplett-Review, Archivierung | Management | Workshop |

---

## 📋 OSP-SPEZIFISCHE ZUSATZREGELN

### 15. Versionierung und Change-Log
**Format:** Semantic Versioning (X.Y.Z)
- **X (Major):** Strukturelle Änderungen
- **Y (Minor):** Neue Module/TAGs
- **Z (Patch):** Korrektionen

**Change-Log-Template:**
```markdown
### [Version] - YYYY-MM-DD
**Änderungen:**
- Beschreibung der Änderung
**Grund:** Warum wurde geändert?
**Auswirkung:** Was bedeutet das für User?
**Verantwortlich:** Name
```

### 16. Namenskonventionen für Markdown-Dateien im OSP

**WICHTIG:** Diese Regel definiert die standardisierte Benennungskonvention für ALLE Markdown-Dateien im OSP-Projekt.

#### Standard-Format:
```
TAG_SUB-TAG_Beschreibung.md
```

**Beispiele (KORREKT):**
- `QM_CORE_Qualitaetspolitik.md`
- `KOM_AIR_KI_Kommunikationsregeln.md`
- `KST_PF_Prueffeld.md`
- `ORG_LEIT_Leitbild_Vision.md`
- `IT_DS_Datenschutz.md`
- `CMS_MC_Material_Compliance.md`
- `VT_KDBW_Kundenbewertung.md`
- `TM_CORE_Maschinen_Anlagen.md`
- `TM_WKZ_Werkzeuge.md`

#### Benennungsregeln (Detailliert):

| Aspekt | Regel | Beispiel | ❌ FALSCH |
|--------|-------|---------|----------|
| **TAG** | GROSSBUCHSTABEN, 2-3 Zeichen | `QM_` | `Qm_` oder `qm_` |
| **SUB-TAG** | GROSSBUCHSTABEN, 2-4 Zeichen | `_CORE_` | `_Core_` oder `_core_` |
| **Trennung** | Unterstriche `_` zwischen Komponenten | `QM_CORE_` | `QM-CORE_` oder `[QM][CORE]_` |
| **Beschreibung** | Aussagekräftig, CamelCase oder _Unterstriche | `Qualitaetspolitik` | `xyz` oder `q_p` |
| **Umlaute** | Konvertiert (ä→ae, ö→oe, ü→ue) | `Qualitaetspolitik` | `Qualitätspolitik` |
| **Eckige Klammern** | ❌ NICHT verwenden | `TAG_SUB_` | `[TAG][SUB]_` |
| **Version im Name** | ❌ NICHT verwenden | `QM_CORE_...md` | `QM_CORE_v2.1.md` |
| **Ordner** | `Main/TAG_Modulname/` | `Main/QM_Qualitaetsmanagement/` | `Main/[QM]` oder `Main/01_QM` |

#### Umlaut-Konvertierung (Vollständig):
- ä → ae
- ö → oe  
- ü → ue
- ß → ss

**Praktische Umlaut-Beispiele:**
- `Qualitätspolitik` → `QM_CORE_Qualitaetspolitik.md`
- `Prüffeld` → `KST_PF_Prueffeld.md`
- `Überblick` → `TAG_SUB_Ueberblick.md`
- `Größe` → `TAG_SUB_Groesse.md`

#### Versionierung (NICHT im Dateinamen):

**❌ FALSCH:**
- `QM_CORE_Qualitaetspolitik_v2.1.md`
- `KOM_AIR_Kommunikationsregeln_v1.md`
- `[QM][CORE]_Qualitaetspolitik_2.5.md`

**✅ KORREKT:**
Versionstand gehört in den **Datei-Header** (YAML-Format am Anfang jeder Datei):
```markdown
# [QM][CORE] Qualitätspolitik

**Version:** 2.1  
**Erstellt:** 2025-11-09  
**Zuletzt aktualisiert:** 2025-11-17  
**Status:** ✅ Production-Ready
```

Versionshistorie wird über:
- **SharePoint-Versionierung** (automatisch)
- **CHANGELOG.md** (manuell pro Modul)
- **Git** (sofern implementiert)

verwaltet.

#### Migration bestehender Dateien:

Dateien mit altem `[TAG][SUB]`-Format werden umbenannt:

| Alter Name | Neuer Name |
|-----------|-----------|
| `[QM][CORE]_Qualitaetspolitik.md` | `QM_CORE_Qualitaetspolitik.md` |
| `[KOM][AIR]_KI_Kommunikationsregeln.md` | `KOM_AIR_KI_Kommunikationsregeln.md` |
| `[KST][PF]_Prueffeld.md` | `KST_PF_Prueffeld.md` |
| `[ORG][LEIT]_Leitbild_Vision.md` | `ORG_LEIT_Leitbild_Vision.md` |
| `[IT][DS]_Datenschutz.md` | `IT_DS_Datenschutz.md` |
| `[TM][CORE]_Maschinen_Anlagen.md` | `TM_CORE_Maschinen_Anlagen.md` |
| `[TM][WKZ]_Werkzeuge.md` | `TM_WKZ_Werkzeuge.md` |

**Migrationsprozess (PowerShell):**
- Batch-Umbenennung mit Validierung
- Link-Update in cross-references
- SharePoint-Sync nach Migration
- Audit-Trail dokumentieren

#### Ordner-Format (BLEIBT UNVERÄNDERT):
```
Main/TAG_Modulname/
```

**Regeln:**
- **Keine Nummerierung** (❌ nicht: `01_QM_Qualitaetsmanagement/`)
- **Nur durch TAG-Präfix identifizieren**
- **Format:** `Main/TAG_Modulname/`

**Beispiele:**
- `Main/QM_Qualitaetsmanagement/`
- `Main/KOM_Kommunikation/`
- `Main/KST_Kostenstellen/`
- `Main/ORG_Unternehmen/`
- `Main/TM_Technik_Maschinen/`

#### Automatische Validierung (PowerShell-Script):

Ein PowerShell-Validator (siehe Schritt 4) überprüft:
- ✅ Dateiname folgt `TAG_SUB-TAG_Beschreibung.md`?
- ✅ TAG in GROSSBUCHSTABEN?
- ✅ SUB-TAG in GROSSBUCHSTABEN?
- ✅ Keine eckigen Klammern `[ ]`?
- ✅ Keine Versionsnummern im Namen?
- ✅ Umlaute korrekt konvertiert?
- ✅ Ordner folgt `Main/TAG_Modulname/`?

---

### 17. Konsistenzprüfung
**Vor jedem Commit:**
1. TAG-Struktur valide? (89 Sub-TAGs)
2. Alle Links bidirektional?
3. Versionsnummer erhöht?
4. Changelog aktualisiert?
5. Index.md synchron?
6. **Dateinamen validiert?** (Regel 16)

### 18. Kritische Dateien-Hierarchie
**Priorität 1 (niemals ändern ohne GF-Freigabe):**
- OSP_TAG_System.md
- OSP_Ordner_Struktur.md
- OSP_Regeln.md

**Priorität 2 (Änderung mit QM-Freigabe):**
- Index.md
- Implementierungs_monitor.md
- KOM_AIR_KI_Kommunikationsregeln.md

**Priorität 3 (Änderung durch Modulverantwortliche):**
- Modul-spezifische Inhalte
- readme_[SUB-TAG].md

### 19. Zugriffsrechte-Enforcement
**SharePoint-Gruppen strikt einhalten:**
- 🟢 L1 (Public): Alle Mitarbeiter (~54 User)
- 🟡 L2 (Abteilung): Führungskräfte, Spezialisten (~8 User)
- 🔴 L3 (Vertraulich): Geschäftsleitung (~3 User)

### 20. Migration-Tracking
**Bei jeder PSP→OSP Übertragung:**
```markdown
## Migration-Log
- **Quelle:** PSP [Bereich][TAG] v1.2
- **Ziel:** OSP [Modul][TAG]
- **Datum:** YYYY-MM-DD
- **Anpassungen:** Was wurde geändert?
- **Tester:** 5 Pilot-User
- **Status:** Draft/Active
```

### 21. OSP-Kontext-Kennzeichnung
**Regel:** Claude kennzeichnet Antworten mit [OSP], wenn Informationen aus dem OSP-Projekt stammen.

**Kennzeichnungs-Schema:**
```
Antwort nutzt OSP-Projekt-Dateien → [OSP] am Ende
Antwort nutzt kein OSP → Kein Symbol
```

**Was zählt als OSP-Kontext:**
- ✅ Informationen aus SharePoint-Dateien (16 Module, 89 Sub-TAGs)
- ✅ TAG-Struktur und Governance-Regeln
- ✅ Prozesse aus OSP-Modulen
- ✅ KGS-Daten (HR_CORE)
- ✅ Cross-User-Learning-Patterns

### 22. Bidirektionale Querverweise

**Regel:** Alle Querverweise zwischen OSP-Modulen MÜSSEN bidirektional gepflegt werden.

**Prinzip:** Symmetrische Referenzierung - jeder Link hat einen Rücklink

**Implementierung:**
- Bei jedem neuen Querverweis: Automatisch Gegenseite prüfen und ergänzen
- Format: `[MODUL][SUBTAG] → [MODUL][SUBTAG]` und zurück
- Dokumentation in OSP_Netz.md (Multi-Layer-Struktur)
- Validierung via PowerShell-Script (wöchentlich)

**Beispiel:**
```markdown
# In QM_NZA_Nach_Zusatzarbeiten.md:
## 📎 Querverweise
- → KST_PF_Prueffeld.md - Prüfung von NZA
- → VT_KDBW_Kundenbewertung.md - Reklamationshandling

# In KST_PF_Prueffeld.md:
## 📎 Querverweise  
- ← QM_NZA_Nach_Zusatzarbeiten.md - NZA-Prüfprozess
```

**Monitoring:**
- Reports/KGS/bidirektionalitaet_check_[KW].md
- Asymmetrische Links: Automatische Korrektur oder TODO-Flag
- Audit-Relevanz: ISO 9001 Kap. 4.4 Prozessverknüpfungen

### 23. Standardisierter 7-Schritte Update-Workflow

**Regel:** JEDER Content-Update folgt diesem strukturierten Prozess

**Pre-Check (Schritt 0):**
```
📋 VOR START:
1. SharePoint-Backup erstellt? [Ja/Nein]
2. Welcher Cluster betroffen? [C1-C5]
3. Update-Scope: [Modul only | Komplett-Update]
4. KGS-Relevanz? [Team-Pattern erkannt?]
5. Benutzervereinbarung unterschrieben? [Ja/Nein]
```

**Workflow-Schritte:**

| Schritt | Aktion | Output | Verantwortlich |
|---------|--------|--------|----------------|
| 1 | Dateien lesen | Liste gelesener Dateien | System |
| 2 | readme_[TAG].md aktualisieren | Bestätigung | Autor |
| 3 | Querverweise bidirektional sync | Link-Report | System |
| 4 | index.md aktualisieren | Status | Autor |
| 5 | Implementierungs_monitor.md | Progress | QM |
| 6 | OSP_Netz.md validieren | Netzwerk-Stats | System |
| 7 | SharePoint-Sync + Verifizierung | Sync-Report | IT |
| 8 | KGS-Pattern-Check | Team-Relevanz | System |

**Post-Workflow-Validation:**
- [ ] Alle Module erfolgreich
- [ ] Bidirektionalität gewährleistet  
- [ ] KGS-Kontext aktualisiert
- [ ] ISO 9001 konform
- [ ] [OSP]-Kennzeichnung korrekt
- [ ] Confidence-Werte (C: XX%) angegeben
- [ ] **Dateinamen validiert?** (Regel 16)

---

**ERWEITERUNG v1.4: Chat-Reset-Prävention (Claude Desktop)**

**Problemstellung:**
Bei der Erstellung vieler großer Dateien (>40 KB) in Claude Desktop kommt es zu Chat-Resets. Ursache ist wahrscheinlich ein **Filesystem-Operation-Burst** in Kombination mit OneDrive-Synchronisation.

**Evidenz:**
- Reset tritt nach 6+ großen Datei-Operationen auf
- Systemübergreifend (verschiedene PC-Arbeitsplätze)
- Dateigröße: 39-53 KB pro Datei
- Token-Nutzung: Nur 35-45% (Token-Limit ist NICHT das Problem)
- Analyse dokumentiert in: Reports/Claude_Desktop_Reset_Analyse.md

**LÖSUNG 1: 2er-Pakete-Strategie (EMPFOHLEN)**

```
CHAT-PAKET 1: Dateien 1-2
├─ Datei 1 erstellen (40-50 KB)
├─ Datei 2 erstellen (40-50 KB)
└─ ✅ Checkpoint: "2 Dateien fertig, OneDrive synchronisiert"

⏸️ PAUSE: 2-5 Minuten (OneDrive-Sync abwarten)

CHAT-PAKET 2: Dateien 3-4
├─ Datei 3 erstellen (40-50 KB)
├─ Datei 4 erstellen (40-50 KB)
└─ ✅ Checkpoint: "4 Dateien gesamt fertig"

⏸️ PAUSE: 2-5 Minuten

CHAT-PAKET 3: Dateien 5-6
├─ Datei 5 erstellen (40-50 KB)
├─ Datei 6 erstellen (40-50 KB)
└─ ✅ Checkpoint: "Alle 6 Dateien komplett"
```

**Vorteile:**
- ✅ Reduziert Operation-Burst (max. 2 statt 6 gleichzeitig)
- ✅ OneDrive kann Sync-Operationen abschließen
- ✅ Electron-App (Claude Desktop) kann Memory freigeben
- ✅ Falls Reset: Max. 2 Dateien müssen neu erstellt werden
- ✅ Kein manueller Eingriff nötig

**LÖSUNG 2: OneDrive pausieren (Alternative)**

```
1. OneDrive PAUSIEREN (Rechtsklick Taskleiste-Icon)
2. Alle Dateien erstellen (schnell, ohne Sync-Konflikte)
3. OneDrive FORTSETZEN (Sync läuft im Hintergrund)
```

**Anwendung:**
- **Immer:** Bei 3+ großen Dateien (>40 KB)
- **Immer:** Bei Batch-Updates über mehrere Module
- **Immer:** Bei Migration größerer Datenmengen ins OSP

**Monitoring:**
- Reset-Häufigkeit dokumentieren (wöchentlich)
- Pattern erkennen (Anzahl Dateien, Größe, Timing)
- Continuous Improvement

**Querverweise:**
- → [KOM][AIR] v2.5 - Abschnitt "Claude Desktop - Chat-Management"
- → Reports/Claude_Desktop_Reset_Analyse.md (Technische Tiefenanalyse)

### 24. Kontext-Gedächtnis-System (KGS) Integration

**Regel:** Das KGS sammelt und teilt TEAM-RELEVANTE Prozesserkenntnisse und Lösungsmuster

**Architektur (v2.0 - HR_CORE-Struktur):**
```
OSP/Main/HR_Human_Resources/
├── HR_CORE_Personalstamm.md     # Zentrale Mitarbeiterdaten
│   └── Spalten: Pers.-Nr. | Kürzel | Vorname Name | KST | Funktion | 
│                Eintritt | E-Mail | Level | TAG-Verantwortung | OSP Level
└── _KGS_Reports/
    ├── weekly_patterns.md        # Wöchentliche Success-Patterns
    └── process_improvements.md   # Prozessverbesserungen

Reports/KGS/                      # Anonymisierte Aggregate
├── logs/                         # Team-Erkenntnisse
└── success_patterns/             # Bewährte Lösungen
```

**Änderung v2.0:**
- BN_Benutzer-Modul nach HR_CORE migriert
- Personalstamm mit erweiterter Spaltenstruktur
- OSP-Level-Spalte für Nutzerlevel-Zuordnung

**KGS-NUTZERVEREINBARUNG (zur Unterschrift):**
```
Hiermit stimme ich zu, dass:
1. Meine PROZESS-relevanten Interaktionen anonymisiert erfasst werden
2. TEAM-NÜTZLICHE Erkenntnisse nach 30 Tagen geteilt werden können
3. Persönliche Daten NICHT weitergegeben werden
4. Nur Success-Patterns mit >80% Team-Relevanz geteilt werden
5. Ich jederzeit Opt-Out beantragen kann

_____________________    _____________________
Datum                    Unterschrift
```

**Was wird GETEILT (anonymisiert):**
- ✅ Erfolgreiche Crimp-Parameter-Lösungen
- ✅ Bewährte Prüfverfahren
- ✅ Effiziente Timeline-Workflows
- ✅ Häufige Normenfragen mit Antworten
- ✅ Prozessverbesserungen

**Was wird NICHT geteilt:**
- ❌ Persönliche Präferenzen
- ❌ Individuelle Fehler
- ❌ Gehaltsdaten
- ❌ Private Kommentare
- ❌ Kundenkritische Details

**Automatisierung (PowerShell):**
- **Täglich:** Erfassung relevanter Patterns
- **Wöchentlich:** Aggregation & Anonymisierung  
- **Monatlich:** Success-Pattern-Verteilung
- **90 Tage:** Retention für personenbezogene Rohdaten

### 25. PSP-OSP Docking Point

**Regel:** Wöchentliche bidirektionale Synchronisation zwischen PSP und OSP

**Docking Points:**
- **OSP-Seite:** `HR_CORE` - Benutzer-Kernidentität
- **PSP-Seite:** `[PROF][OSP]` - OSP-Verknüpfung im persönlichen System

**Sync-Prozess (wöchentlich, Montag 6:00):**
```powershell
# PSP_OSP_Weekly_Sync.ps1
1. PSP → OSP Transfer:
   - Bewährte persönliche Workflows → Team-Standards
   - Erfolgreiche Problemlösungen → Success-Patterns
   - Optimierte Prozesse → [RES][BP]

2. OSP → PSP Rückfluss:
   - Team-Success-Patterns → Persönliche Nutzung
   - Neue Governance-Regeln → PSP-Integration
   - KGS-Insights → PSP-Verbesserung

3. Konfliktlösung:
   - Bei Widersprüchen: OSP hat Vorrang im Unternehmenskontext
   - Persönliche Anpassungen bleiben in PSP erhalten
```

### 26. System-Konnektoren

**Aktive Integrationen:**
- **M365:** SharePoint, Teams, Outlook
- **Claude API:** Direktanbindung für KI
- **n8n/Zapier:** Workflow-Automation
- **Timeline ERP:** Datenaustausch

**Neue Konnektoren nur mit:**
- IT-Security-Check
- DSGVO-Prüfung  
- GF-Freigabe
- Dokumentation in [IT][DS]

### 27. Quellen-Hierarchie und Verifizierungspflicht (NULL-FEHLER-POLITIK)

**Regel:** Bei widersprüchlichen Informationen gilt IMMER diese Hierarchie - mit TRANSPARENZ-PFLICHT

**QUELLEN-PRIORITÄT (absteigend):**
```
STUFE 1: AUTORITATIVE QUELLEN (Immer Vorrang)
├── OSP_TAG_System.md (aktuelle Version - 89 Sub-TAGs)
├── OSP_Ordner_Struktur.md (16 Module)
├── OSP_Regeln.md (diese Datei)
└── Freigegebene SharePoint-Dokumente in /Main/

STUFE 2: ERGÄNZENDE QUELLEN (Bei Nicht-Widerspruch)
├── Import-Ordner (Entwürfe, Vorschläge)
├── Upload-Dateien von Usern
├── Meeting-Protokolle
└── E-Mail-Anhänge

STUFE 3: ZU VERIFIZIEREN (Immer gegenchecken)
├── Mündliche Anweisungen
├── Chat-Verläufe
├── Externe Quellen
└── KI-generierte Vorschläge
```

**🔍 TRANSPARENZ-PFLICHT:**
Bei JEDER Unstimmigkeit SOFORT melden:
```
"⚠️ DISKREPANZ ERKANNT:
- Quelle A (Upload): [TAG][CTX]
- Quelle B (OSP_TAG_System): [TAG][USER-ID]
- Verwende: OSP_TAG_System → [TAG][USER-ID]
- Bitte bestätigen oder korrigieren!"
```

**NULL-FEHLER-GRUNDSÄTZE:**
- **Transparenz > Geschwindigkeit** (Lieber melden als verschweigen)
- **Nachfragen > Annahmen** (Lieber fragen als raten)
- **Verifizieren > Vertrauen** (Immer gegenchecken)
- **Lernen > Vergessen** (Jeden Fehler dokumentieren)

### 28. Parallele Kennzeichnungs-Systeme (C: XX%) + [OSP]

**Regel:** BEIDE Systeme parallel verwenden - sie haben unterschiedliche Funktionen

**System-Übersicht:**

| System | Zweck | Wann | Beispiel |
|--------|-------|------|----------|
| **(C: XX%)** | Zeigt SICHERHEIT der Info | IMMER bei Fakten | "100% sicher" |
| **[OSP]** | Zeigt QUELLE (OSP-Projekt) | Bei OSP-Nutzung | "Aus OSP-Dateien" |

**Korrekte Anwendung:**
```markdown
✅ "In [QM][NZA] sind NZA-Prozesse definiert. (C: 100%)" [OSP]
✅ "Crimphöhe für FLRY 0.35mm² ist 1.6±0.05mm. (C: 100%)" 
✅ "Vermutlich nutzen 15 User das System aktiv. (C: 75%)" [OSP]
✅ "ISO 9001 hat 10 Kapitel. (C: 100%)"  ← Kein [OSP], da Allgemeinwissen
```

**Confidence-Level-Definition:**
- **(C: 100%)** = Verifiziert, dokumentiert, keine Zweifel
- **(C: 80-99%)** = Sehr wahrscheinlich, minimal unsicher
- **(C: 60-79%)** = Wahrscheinlich, moderate Unsicherheit
- **(C: <60%)** = Unsicher, mit ⚠️ WARNUNG kennzeichnen!

**NIEMALS:**
- ❌ Information ohne C-Wert bei Faktenaussagen
- ❌ [OSP] ohne C-Wert bei OSP-basierten Aussagen
- ❌ Unsicherheit verschweigen (immer transparent!)

### 29. Definitions-Glossar: Meta-Dateien und Main-Dateien

**Regel:** Klare Definition für Befehle wie "aktualisiere die Meta-Dateien" oder "ergänze xy in den Main-Dateien"

**META-DATEIEN (Dokumentation & Governance):**
```
📍 Pfad: C:\Users\andre\OneDrive - Rainer Schneider Kabelsatzbau und Konfektion
         \Kommunikationswebsite - OSP Schneider Kabelsatzbau\Dokumentation

📄 Dateien:
1. OSP_Ordner_Struktur.md    → Definiert die 16 Module + 89 Sub-TAGs
2. OSP_Regeln.md             → Governance-Regeln (DIESES DOKUMENT)
3. OSP_TAG_System.md         → TAG-Definitionen + Verwendungskontext

🎯 Zweck: Struktur- und Governance-Dokumentation
⚠️  Änderungen: Nur mit QM-Freigabe (Regel 18 - Priorität 1)
```

**MAIN-DATEIEN (Operative Inhalte & Implementierung):**
```
📍 Pfad: C:\Users\andre\OneDrive - Rainer Schneider Kabelsatzbau und Konfektion
         \Kommunikationswebsite - OSP Schneider Kabelsatzbau\Main

📄 Dateien:
1. index.md                        → Zentrale Navigation aller 16 Module
2. OSP_Netz.md                    → Bidirektionale Querverweise & Vernetzung
3. implementierungs_monitor.md    → Fortschritts-Tracking & Status-Updates

🎯 Zweck: Operative Implementierung & Tracking
⚠️  Änderungen: Mit QM-Freigabe (Regel 18 - Priorität 2)
```

**PRAKTISCHE ANWENDUNG:**

Wenn Andreas sagt: **"Aktualisiere die Meta-Dateien"**
→ Lesezugriff & Änderungen in `/Dokumentation/` (OSP_Ordner_Struktur.md, OSP_Regeln.md, OSP_TAG_System.md)

Wenn Andreas sagt: **"Ergänze XY in den Main-Dateien"**
→ Änderungen in `/Main/` (index.md, OSP_Netz.md, implementierungs_monitor.md)

Wenn Andreas sagt: **"Synchronisiere beide Systeme"**
→ Beide Ordner betroffen, wechselseitige Konsistenz erforderlich

**Synchronisierungs-Reihenfolge (Standard):**
```
1. Meta-Dateien lesen (Quelle der Wahrheit)
2. Main-Dateien aktualisieren (basierend auf Meta-Dateien)
3. Querverweise in OSP_Netz.md bidirektional sync
4. index.md aktualisieren
5. Implementierungs_monitor.md Status aktualisieren
6. Verifizierung: Alle Links gültig?
```

### 30. KI-Chatbot-Workflow-Governance

**Regel:** Alle KI-gestützten Anfragen im OSP-System folgen dem standardisierten 4-Phasen-Workflow mit 11 Schritten

**Workflow-Referenz:** `Main/KOM_Kommunikation/KOM_AIR_KI_Kommunikationsregeln.md` v2.7

**Prinzip:** Strukturierte Verarbeitung mit mehrstufiger Validierung und Berechtigungskontrolle

**Implementierung:**

#### 4-Phasen-Struktur:
```
PHASE 1: INITIALISIERUNG (Schritte 0-3)
├── Schritt 0: Start
├── Schritt 1: Benutzer-Anfrage
├── Schritt 2: System-Load + BENUTZERERKENNUNG ⚠️ KRITISCH
│   ├── Laden von KI-Regeln & OSP_Regeln
│   ├── Benutzer-ID aus Session extrahieren
│   ├── Zugriffsprofil aus HR_CORE
│   └── Zugriffslevel (L1-L3) + OSP-Level bestimmen
└── Schritt 3: OSP-Dokumente laden ⚠️ KRITISCH

PHASE 2: ANALYSE (Schritte 4-6)
├── Schritt 4: Anfrage analysieren & clustern
├── Schritt 5: TAG zuordnen + VALIDIERUNG + BERECHTIGUNG ⚠️ KRITISCH
│   ├── TAG-Validierung gegen OSP_TAG_System.md
│   ├── Phantasie-TAG-Detection
│   ├── Berechtigungsprüfung (Level-basiert)
│   └── 30-Sekunden-Timeout bei fehlenden Rechten
├── Schritt 6: TAG-Kontext laden
└── Schritt 7: [ENTFÄLLT - in Schritt 2 integriert]

PHASE 3: OPTIMIERUNG & AUSFÜHRUNG (Schritte 8-9)
├── Schritt 8: Prompt strukturieren & optimieren
│   └── Level-angepasste Antworttiefe (L1→L3)
└── Schritt 9: Prompt ausführen ⚠️ KRITISCH

PHASE 4: OUTPUT (Schritte 10-11)
├── Schritt 10: Ergebnis anzeigen + CONFIDENCE-CHECK
│   └── Warnung bei Confidence <90%
└── Schritt 11: Ende + KGS-Update
```

#### Kritische Kontrollpunkte:

| Kontrollpunkt | Schritt | Aktion bei Fehler |
|--------------|---------|-------------------|
| **Benutzererkennung** | 2 | Gastmodus (nur öffentliche TAGs) |
| **OSP-Dokumente** | 3 | Fallback auf Cache |
| **TAG-Validierung** | 5 | Prozess-Stop bei Phantasie-TAG |
| **Berechtigung** | 5 | 30-Sek-Timeout → Auto-Skip |
| **API-Ausführung** | 9 | 3 Retries → Fallback |
| **Confidence <90%** | 10 | Warnung an Benutzer |

#### Berechtigungsmatrix (Level-basiert):

| Level | Bezeichnung | Zugriff | Beispiel-TAGs | DSGVO-Prüfung |
|-------|------------|---------|---------------|---------------|
| **L1** | Public | 🟢 Basis | [ORG][LEIT] | Nein |
| **L2** | Abteilung | 🟡 Erweitert | + [KST][PF], [QM][DOK] | Optional |
| **L3** | Vertraulich | 🔴 Voll | Alle TAGs | IMMER |

#### NULL-FEHLER-POLITIK-Erweiterung:

**Punkt 5: Validieren > Erfinden**
- Keine Phantasie-TAGs akzeptieren
- Alle TAGs gegen OSP_TAG_System.md (89 Sub-TAGs) prüfen
- Bei unbekannten TAGs: Prozess stoppen
- Ähnliche TAGs vorschlagen (Levenshtein-Distanz)
- Dokumentation fehlerhafter TAG-Anfragen

#### Compliance-Anforderungen:

- ✅ ISO 9001:2015 konform (Prozessdokumentation)
- ✅ DSGVO-konform mit Audit-Trail
- ✅ IPC-WHMA-A-620 (technische Standards)
- ✅ NULL-FEHLER-POLITIK vollständig integriert
- ✅ Level-basierte Antworttiefe (L1-L3)
- ✅ Phantasie-TAG-Validierung

#### Performance-KPIs:

| KPI | Zielwert | Kritisch ab |
|-----|----------|-------------|
| **Durchlaufzeit** | <4s | >6s |
| **TAG-Validierung** | 100% | <100% |
| **Phantasie-TAGs/h** | 0 | >5 |
| **Confidence ≥90%** | >85% | <75% |
| **DSGVO-Compliance** | 100% | <100% |

#### Monitoring & Reporting:

**Real-Time Monitoring:**
- Durchlaufzeit pro Phase
- Auth-Timeouts pro Stunde
- Phantasie-TAG-Detections
- Confidence-Level-Verteilung
- DSGVO-Zugriffe (vollständiger Log)

**Wöchentliche Reports:**
- Performance-Statistiken
- TAG-Validierungs-Audit
- Berechtigungs-Verstöße
- Level-Verteilung der Anfragen
- Success-Patterns für KGS

#### Eskalation bei Verstößen:

```
Level 1: Phantasie-TAG erkannt → Automatische Ablehnung + Log
         ↓ (>5/Stunde)
Level 2: Modul-Owner informieren → Prüfung auf Schulungsbedarf
         ↓ (>10/Stunde)
Level 3: QM-Team → Prozess-Review
         ↓ (Systematisch)
Level 4: Geschäftsführung → Governance-Anpassung
```

#### Implementierungs-Checkliste:

- [ ] Workflow-Engine auf 11 Schritte konfiguriert
- [ ] HR_CORE-Integration aktiviert
- [ ] TAG-Validator gegen OSP_TAG_System.md aktiv
- [ ] 30-Sekunden-Timeout implementiert
- [ ] Confidence-Warnung bei <90% aktiv
- [ ] Level-basierte Antworten konfiguriert (L1-L3)
- [ ] Audit-Trail für DSGVO aktiviert
- [ ] Monitoring-Dashboard eingerichtet
- [ ] Eskalationspfade definiert
- [ ] Team-Schulung durchgeführt

#### Querverweise:

- → `KOM_AIR_KI_Kommunikationsregeln.md` v2.7
- → `HR_CORE` (Benutzer-Identität & Kompetenz-Level)
- → `OSP_TAG_System.md` v1.0
- → `OSP_Ordner_Struktur.md` v1.0
- ← Alle Module nutzen diesen Workflow

**Verantwortlich:** Andreas Löhr (QM-Manager & KI-Manager)  
**Review:** Monatlich  
**Audit:** Quartalsweise  

### 31. OSP-Nutzerlevel (OSP-STD, OSP-PRO, OSP-EXP)

**Regel:** Alle OSP-Nutzer werden einem von drei Nutzerlevel zugeordnet.

**Level-Definition:**

| OSP-Level | Bezeichnung | Beschreibung | Typische Nutzer |
|-----------|-------------|--------------|-----------------|
| **OSP-STD** | Standard | Basis-Zugriff auf öffentliche Module, Lesen von Dokumenten, einfache KI-Interaktionen | Produktionsmitarbeiter, Sachbearbeiter |
| **OSP-PRO** | Professional | Erweiterter Zugriff, Bearbeitung von Dokumenten, erweiterte KI-Funktionen, Modul-spezifische Berechtigungen | Abteilungsleiter, Fachspezialisten, Prokurist |
| **OSP-EXP** | Expert | Vollzugriff, Administration, System-Konfiguration, alle KI-Funktionen | Geschäftsführung, QM-Manager, KI-Manager |

**Zuordnung:**
- OSP-Level wird bei User-Onboarding festgelegt
- Änderungen nur durch QM-Leitung oder GF
- Dokumentation in HR_CORE (Personalstamm)

**Zusammenhang mit Zugriffslevel (L1-L3):**

| OSP-Level | Zugriffslevel | Module |
|-----------|---------------|--------|
| OSP-STD | L1 (Public) | ORG, KOM (teilweise), RES (teilweise) |
| OSP-PRO | L2 (Abteilung) | + QM, KST, VT, EK, AV, TM, PM |
| OSP-EXP | L3 (Vertraulich) | + GF, FIN, HR, IT (alle), STR |

**Abgrenzung OSP-Level vs. Zugriffslevel:**

| Aspekt | OSP-Level | Zugriffslevel (L1-L3) |
|--------|-----------|----------------------|
| **Zweck** | KI-Funktionsumfang | Datenzugriff/Sichtbarkeit |
| **Steuert** | Was kann der User mit dem KI-System tun? | Welche Daten kann der User sehen? |
| **Beispiel** | OSP-PRO kann erweiterte Analysen nutzen | L2 sieht Abteilungsdaten |

**Querverweise:**
- → HR_CORE (Personalstamm mit OSP-Level-Spalte)
- → Regel 30 (KI-Chatbot-Workflow mit Level-Prüfung)
- → KOM_AIR_KI_Kommunikationsregeln.md

**Verantwortlich:** Andreas Löhr (QM-Manager & KI-Manager)

---

## 🔍 QUALITÄTSSICHERUNG

### QS-Metriken

| Metrik | Ziel | Aktuell | Status |
|--------|------|---------|--------|
| Broken Links | <2% | - | ⏳ |
| Update-Zeit/Modul | <20 Min | - | ⏳ |
| Bidirektionale Konsistenz | >95% | - | ⏳ |
| Automatisierungsgrad | >60% | - | ⏳ |
| User-Adoption | >80% | - | ⏳ |

### Audit-Checkliste
- [ ] Alle 89 Sub-TAGs dokumentiert (86+3 durch TM-Modul)
- [ ] Alle Links bidirektional
- [ ] SharePoint-Sync aktiv
- [ ] KGS funktionsfähig
- [ ] ISO 9001 konform
- [ ] DSGVO compliant
- [ ] Null-Fehler-Politik befolgt
- [ ] **Dateinamen nach Regel 16 konform?**
- [ ] **KI-Chatbot-Workflow implementiert?**
- [ ] **OSP-Nutzerlevel zugeordnet?** (Regel 31)

---

## 🚨 ESKALATIONSPFADE

### Level 1: Operative Ebene
**Problem:** Broken Link, fehlende Datei
**Lösung:** PowerShell-Script Auto-Fix
**Eskalation nach:** 24h ohne Fix

### Level 2: Modul-Verantwortliche
**Problem:** Inhaltliche Unstimmigkeiten
**Lösung:** Modul-Owner klärt
**Eskalation nach:** 48h ohne Klärung

### Level 3: QM-Team
**Problem:** Prozess-/Compliance-Themen
**Lösung:** Andreas Löhr entscheidet
**Eskalation nach:** 72h ohne Lösung

### Level 4: Geschäftsführung
**Problem:** Strukturelle Änderungen
**Lösung:** GF-Entscheidung
**Eskalation:** Sofort bei kritischen Themen

---

## 📊 REPORTING-STANDARDS

### Wöchentlich
- Broken-Links-Report
- KGS-Pattern-Summary
- PSP-OSP-Sync-Status
- User-Activity-Dashboard
- **Dateiname-Validierungs-Report** (Regel 16)
- **KI-Workflow-Performance-Report** (Regel 30)

### Monatlich
- Compliance-Status
- Success-Pattern-Distribution
- Automatisierungs-KPIs
- User-Adoption-Rate

### Quartalsweise
- ISO 9001 Audit-Report
- Struktur-Review
- Lessons-Learned
- Improvement-Roadmap

---

## 📝 ÄNDERUNGSHISTORIE

### [2.0] - 2025-12-05
**OSP-STRUKTURÄNDERUNGEN PHASE 1:**
- ✅ **Regel 31 hinzugefügt:** OSP-Nutzerlevel (OSP-STD, OSP-PRO, OSP-EXP)
- ✅ **Abgrenzung definiert:** OSP-Level vs. Zugriffslevel (L1-L3)
- ✅ **HR_CORE-Integration:** Personalstamm mit OSP-Level-Spalte
- ✅ **Regel 19 aktualisiert:** Zugriffslevel auf L1-L3 (statt L1-L5)
- ✅ **Regel 24 aktualisiert:** KGS-Architektur auf HR_CORE umgestellt
- ✅ **Regel 30 aktualisiert:** Berechtigungsmatrix auf L1-L3

**Grund:**
Einführung eines 3-stufigen OSP-Nutzerlevel-Systems zur Steuerung des KI-Funktionsumfangs. Trennung von Datenzugriff (L1-L3) und KI-Funktionen (OSP-STD/PRO/EXP). Migration von BN_Benutzer nach HR_CORE.

**Auswirkung:**
- Alle Nutzer erhalten OSP-Level-Zuordnung
- KI-Funktionen sind level-abhängig
- HR_CORE dokumentiert OSP-Level
- Zugriffslevel vereinfacht auf 3 Stufen

**Verantwortlich:** Andreas Löhr (QM-Manager & KI-Manager)

---

### [1.9] - 2025-11-22
**KI-CHATBOT-WORKFLOW-GOVERNANCE IMPLEMENTIERT:**
- ✅ **Regel 30 hinzugefügt:** Standardisierter 4-Phasen-Workflow mit 11 Schritten
- ✅ **Berechtigungsmatrix:** L1-L5 Kompetenz-Level definiert
- ✅ **Benutzererkennung:** Integration mit BN_CORE
- ✅ **TAG-Validierung:** Phantasie-TAG-Detection implementiert
- ✅ **NULL-FEHLER-POLITIK:** Erweitert um Punkt 5 "Validieren > Erfinden"
- ✅ **Performance-KPIs:** Zielwerte und kritische Schwellen definiert
- ✅ **Monitoring:** Real-Time und wöchentliche Reports
- ✅ **Eskalationspfade:** 4-stufiges Eskalations-System
- ✅ **Querverweise:** Zu KOM_AIR_KI_Kommunikationsregeln.md v2.7

**Grund:**
Standardisierung aller KI-gestützten Anfragen im OSP-System. Gewährleistet einheitliche Verarbeitung, mehrstufige Validierung, Berechtigungskontrolle und vollständige Compliance mit ISO 9001:2015 und DSGVO.

**Auswirkung:**
- Alle KI-Anfragen folgen strukturiertem Prozess
- Phantasie-TAGs werden verhindert
- Level-basierte Zugriffskontrolle aktiv
- Confidence-Levels bei allen Antworten
- Vollständiger Audit-Trail für DSGVO
- Messbare Performance-KPIs

**Verantwortlich:** Andreas Löhr (QM-Manager & KI-Manager)

---

### [1.8] - 2025-11-21
**RÜCKVERWEISE HINZUGEFÜGT:**
- ✅ **Rückverweise zu BN-Modul:** README_BN_AL.md (Andreas Löhr als System-Architekt)
- ✅ **Bidirektionalität:** Verweis von BN zu OSP-Governance etabliert
**Verantwortlich:** Andreas Löhr (QM-Manager)

---

### [1.7] - 2025-11-21
**TM-MODUL AKTIVIERUNG & VOLLSTÄNDIGE SYNCHRONISATION:**
- ✅ **TM-Modul aktiviert:** [TM][CORE] und [TM][WKZ] in Betrieb
- ✅ **Statistik-Update:**
  - Gesamt Sub-TAGs: 86 → 89 (+3)
  - Aktive Sub-TAGs: 20 → 22 (+2)  
  - Module mit Inhalt: 5 → 6
  - Cluster 4: 3% → 9,7% (3 von 32)
  - Gesamt-Fortschritt: 22,5% → 24,7%
- ✅ **[TM][CORE] definiert:** 14 Produktionsanlagen (Maschinen & Anlagen)
  - Abisolierautomaten: Komax Kappa 310, Gamma 255, Zeta 630
  - Crimpautomaten: Komax Alpha 530, Schleuniger CS4580
  - Mess-/Prüftechnik: Adaptronic, TSK
  - Beschriftung: Brady IP Printers, BMP61
- ✅ **[TM][WKZ] definiert:** 70-110 Produktions- und Crimpwerkzeuge
  - Crimppressen: AMP, Wezag, Stocko, Lumberg
  - Prüfmittel: DGUV-Prüfer, Prüfadapter, ESD-Station
  - Werkzeuge: Messschieber, Crimpzangen, Spezialwerkzeuge
- ✅ **Abgrenzung präzisiert:**
  - [TM][CORE] = "Was steht fest an einem Platz und kostet viel Geld"
  - [TM][WKZ] = "Was ich in die Hand nehmen oder transportieren kann"
- ✅ **Basis-Dokumente spezifiziert:** OSP_TAG_System.md v1.0, OSP_Ordner_Struktur.md v1.0
- ✅ **Audit-Checkliste aktualisiert:** 85 → 89 Sub-TAGs
- ✅ **Synchronisation durchgeführt:** Alle Meta-Dateien konsistent

**Grund:**
Integration der TM-Module in den produktiven Betrieb. Cluster 4 (Unterstützung) von 3% auf 9,7% ausgebaut. Vollständige Dokumentation aller Produktionsanlagen und Werkzeuge für operative Nutzung.

**Auswirkung:**
- Cluster 4 deutlich fortgeschrittener (9,7% statt 3%)
- Technische Dokumentation produktionsreif
- Maschinendatenbank vollständig integriert
- Werkzeugverwaltung zentral verfügbar
- Wartungs-Workflows können aufgebaut werden
- Produktions-Tracking möglich

**Verantwortlich:** Andreas Löhr (QM-Manager), Marcel Dützer (Technik)

---

### [1.6] - 2025-11-17
**DATEIBENENNUNGS-KONVENTION IMPLEMENTIERT:**
- ✅ **Regel 16 KOMPLETT NEU:** TAG_SUB-TAG_Beschreibung.md Format
- ✅ Keine eckigen Klammern `[ ]` mehr in Dateinamen
- ✅ Großbuchstaben für TAG und SUB-TAG
- ✅ Umlaut-Konvertierung (ä→ae, ö→oe, ü→ue) definiert
- ✅ Version gehört in Datei-Header, NICHT in Dateinamen
- ✅ Migration-Plan für bestehende Dateien
- ✅ PowerShell-Validator Script (Schritt 4)
- ✅ Audit-Checkliste in Konsistenzprüfung ergänzt

**Grund:**
Standardisierung der Dateibenennungskonvention für alle OSP-Markdown-Dateien. Dies vermeidet Chaos, ermöglicht automatische Validierung und macht das System konsistenter.

**Auswirkung:**
- Neue Dateien folgen sofort dem neuen Format
- Bestehende Dateien können schrittweise migriert werden
- PowerShell-Automation validiert Einhaltung
- Cross-Platform-Kompatibilität verbessert (Eckige Klammern sind in Pfaden problematisch)

**Verantwortlich:** Andreas Löhr (QM-Manager)

---

### [1.5] - 2025-11-17
**DEFINITIONS-GLOSSAR FÜR META-DATEIEN UND MAIN-DATEIEN:**
- ✅ **Regel 29 hinzugefügt:** Klare Definition für Befehle wie "aktualisiere die Meta-Dateien"

### [1.4] - 2025-11-17
**CHAT-RESET-PRÄVENTION FÜR CLAUDE DESKTOP:**
- ✅ **Regel 23 ERWEITERT:** 2er-Pakete-Strategie implementiert

### [1.3] - 2025-11-16
**GROSSE ERWEITERUNG - PSP-Transfer & KGS & NULL-FEHLER:**
- ✅ **Regel 22:** Bidirektionale Querverweise (aus PSP)
- ✅ **Regel 23:** 7-Schritte Update-Workflow
- ✅ **Regel 24:** KGS-Integration mit Nutzervereinbarung
- ✅ **Regel 25:** PSP-OSP Docking Point
- ✅ **Regel 26:** System-Konnektoren
- ✅ **Regel 27:** NULL-FEHLER-POLITIK mit Transparenz
- ✅ **Regel 28:** Parallele Kennzeichnung (C: XX%) + [OSP]

### [1.2] - 2025-11-16
**OSP-KENNZEICHNUNG IMPLEMENTIERT:**
- ✅ **Regel 21 hinzugefügt:** OSP-Kontext-Kennzeichnung
- ✅ **[OSP]-Symbol** für Transparenz definiert

### [1.1] - 2025-11-14
**ERWEITERUNG für vollständige OSP-Implementierung:**
- ✅ Inhaltsverzeichnis hinzugefügt
- ✅ Index.md, Implementierungs_monitor.md, OSP_Netz.md definiert
- ✅ readme_[SUB-TAG].md Template
- ✅ Migration-Erfolgsmetriken

### [1.0] - 2025-11-09
- Initiale Erstellung basierend auf PSP_Regeln.md
- Multi-User-Unterstützung
- SharePoint-Integration

---

**Status:** ✅ **OSP-REGELN v2.0 MIT OSP-NUTZERLEVEL**  

**Neue Features v2.0:**
- Regel 31: OSP-Nutzerlevel (OSP-STD, OSP-PRO, OSP-EXP)
- Abgrenzung OSP-Level vs. Zugriffslevel (L1-L3)
- HR_CORE-Integration für Personalstamm
- Zugriffslevel vereinfacht auf L1-L3

**Features v1.9:**
- Regel 30: KI-Chatbot-Workflow (4 Phasen, 11 Schritte)
- Berechtigungsmatrix L1-L3 definiert
- HR_CORE Integration für Benutzererkennung
- Phantasie-TAG-Detection aktiviert
- NULL-FEHLER-POLITIK erweitert
- Performance-KPIs und Monitoring
- 4-stufige Eskalationspfade

**Features v1.8:**
- Rückverweise zu BN-Modul etabliert

**Features v1.7:**
- TM-Modul aktiviert: [CORE] + [WKZ]
- 22 von 89 Sub-TAGs aktiv (24,7%)
- 6 Module mit Inhalt

**Features v1.6:**
- Regel 16: TAG_SUB-TAG_Beschreibung.md Format
- Umlaut-Konvertierung definiert
- PowerShell-Validator-Script

**Features v1.5:** 
- Regel 29: Definitions-Glossar für Meta-Dateien und Main-Dateien

**Features v1.4:** 
- 2er-Pakete-Strategie für Claude Desktop

**Features v1.3:**
- Bidirektionale Querverweise (Regel 22)
- KGS mit Team-Learning (Regel 24)  
- PSP ↔ OSP Sync wöchentlich (Regel 25)
- Transparenz-Pflicht (Regel 27)
- Parallele Kennzeichnung (Regel 28)

**Kompatibilität:** OSP_TAG_System.md v1.0 + OSP_Ordner_Struktur.md v1.0 + KOM_AIR_KI_Kommunikationsregeln.md v2.7  
**Bereit für:** Pilot-Phase mit 5 Usern → Rollout auf max. 20 OSP-Nutzer  
**Kritisch:** NULL-FEHLER durch Transparenz und Verifizierung!

---

*Dieses Dokument ist die autoritative Governance-Referenz für das OSP-System der Rainer Schneider Kabelsatzbau GmbH & Co. KG. Bei Unstimmigkeiten immer nachfragen!*

(C: 100%) [OSP]
