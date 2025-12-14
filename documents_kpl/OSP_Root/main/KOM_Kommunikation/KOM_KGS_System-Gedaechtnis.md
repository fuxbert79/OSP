# [KOM][KGS] Kontext-Gedächtnis-System

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 2.2 | **TAG:** [KOM][KGS] | **Erstellt:** 2025-11-18 | **Aktualisiert:** 2025-12-05 | **Autor:** AL | **Verantwortlich:** AL (KI-Manager) | **Cluster:** 🔵 C2-Kommunikation | **Zugriff:** 🟢 L1-Öffentlich | **Status:** ✅ PRODUKTIV

---

## ZWECK

KGS = Kollektives Gedächtnis des OSP-Systems:

1. **Team-Erinnerungen** - Entscheidungen, Lessons Learned
2. **System-Gedächtnis** - Querverweise-Tracking, RAG-Import-Protokolle
3. **Change-Log** - Änderungsdokumentation

**Besonderheit:** In ChromaDB importiert → KI kann selbst zugreifen!

---

## INHALTSVERZEICHNIS

1. [Team-Erinnerungen](#1-team-erinnerungen)
2. [System-Gedächtnis](#2-system-gedächtnis)
3. [Change-Log](#3-change-log)
4. [Querverweise](#querverweise)
5. [Änderungshistorie](#änderungshistorie)

---

## 1. TEAM-ERINNERUNGEN

### 1.1 Wichtige Entscheidungen (seit Nov 2025)

| Datum | Entscheidung | Grund | Beteiligte | Auswirkung |
|-------|--------------|-------|------------|------------|
| 14.11 | OSP-Projekt Start | Wissensmanagement systematisieren | CS, AL | 16 Module, 89 Sub-TAGs |
| 18.11 | C5 "Benutzerverwaltung" | BN aus C4 herauslösen | AL | [BN] → C5 |
| 21.11 | SV L2→L3 | Prokura-Vollmacht | AL, CS | SV voller GF-Zugriff |
| 25.11 | Pilot-Phase | 5 User testen | AL, CS, SV, SK, TS | 72% Completion |
| 26.11 | OSPUI Go-Live | KI-Chatbot produktiv | AL | Hetzner CX33 deployed |
| 29.11 | L1-L5 → L1-L3 | Vereinfachung Zugriffslevel | AL | 3 statt 5 Level |
| 29.11 | RAG-Richtlinie | ChromaDB-Import standardisieren | AL | IT_RAG_Richtlinie v1.0 |
| 29.11 | KGS Querverweise | Zentrale Tracking-Matrix | AL | Bidirektionalität sichergestellt |
| 05.12 | BN → HR_CORE | Benutzer-Modul migriert | AL | HR_CORE_Personalstamm.md |
| 05.12 | OSP-Level | OSP-STD/PRO/EXP eingeführt | AL | KI-Funktionsumfang gesteuert |

---

### 1.2 Lessons Learned

**LL-001: Template-First-Approach** (16.11.2025)
- **Problem:** Erste Docs ohne Template → inkonsistente Struktur, viel Nacharbeit
- **Lösung:** Immer erst Template (Phase 1 Import-Flow)
- **Status:** ✅ In IT_RAG_Richtlinie v1.0 verankert

**LL-002: Querverweise bidirektional** (20.11.2025)
- **Problem:** Viele einseitige Querverweise (A→B, aber B→A fehlt) → inkonsistentes Netzwerk
- **Lösung:** Zentrale Tracking-Matrix in KOM_KGS (Sektion 2.1)
- **Status:** ✅ Implementiert (v2.0)

**LL-003: Token-Effizienz** (29.11.2025)
- **Problem:** Große Docs = hohe Embedding-Kosten
- **Lösung:** Token-Effizienz-Regeln (min. -10%)
- **Status:** ✅ In IT_RAG_Richtlinie v1.0 verankert

**LL-004: Confidence-Werte entfernt** (29.11.2025)
- **Problem:** ChromaDB liefert eigene Similarity-Scores → Confidence (C:XX%) redundant
- **Lösung:** Confidence komplett aus RAG-Docs entfernt
- **Status:** ✅ In IT_RAG_Richtlinie v1.0 definiert

**LL-005: OSPUI statt BN für User-Memory** (29.11.2025)
- **Problem:** Open WebUI hat eigenes Memory → BN_XX_PREF.md + BN_XX_LOG.md = Duplikation
- **Lösung:** BN-Modul nach HR_CORE migriert
- **Status:** ✅ Implementiert (BN → HR_CORE)

**LL-006: L1-L5 zu komplex** (05.12.2025)
- **Problem:** 5 Zugriffslevel schwer zu verwalten, Überschneidungen
- **Lösung:** Reduktion auf L1-L3 + separates OSP-Level (STD/PRO/EXP)
- **Status:** ✅ Implementiert (OSP_Regeln v2.0, KOM_AIR v3.0)

---

### 1.3 Projekt-Meilensteine

| Meilenstein | Datum | Status | Beschreibung |
|-------------|-------|--------|--------------|
| **M1: OSP-Konzept** | 14.11.25 | ✅ | 16 Module, 89 Sub-TAGs |
| **M2: Pilot-Start** | 25.11.25 | ✅ | 5 User (AL, CS, SV, SK, TS) |
| **M3: 72% Complete** | 26.11.25 | ✅ | 64/89 Sub-TAGs aktiv |
| **M4: OSPUI Launch** | 26.11.25 | ✅ | Open WebUI auf Hetzner CX33 |
| **M5: RAG-Richtlinie** | 29.11.25 | ✅ | ChromaDB-Import standardisiert |
| **M5a: Level-Migration** | 05.12.25 | ✅ | L1-L5 → L1-L3 + OSP-Level |
| **M6: ChromaDB-Import** | 06.12.25 | ⏳ | Erste RAG-Docs importiert |
| **M7: 100% Complete** | 15.01.26 | ⏳ | Alle 89 Sub-TAGs aktiv |
| **M8: Rollout Phase 2** | 01.02.26 | ⏳ | 20+ User (ganze Teams) |

---

## 2. SYSTEM-GEDÄCHTNIS

### 2.1 QUERVERWEISE-TRACKING-MATRIX

**Zweck:** Zentrale Verwaltung aller bidirektionalen Links (OSP_Regeln.md Regel 22)

**Prozess:**
1. RAG-Import: Querverweise hier eintragen
2. Fehlende Rückverweise als TODO markieren
3. Wöchentliches Review (Mo 08:00): TODOs abarbeiten
4. Auto-Validierung via PowerShell (täglich 07:00)

---

#### 2.1.1 Bidirektionale Links (✅ AKTIV)

**Stand:** 05.12.2025 | **Anzahl:** 12

| Von | Nach | Status | Erstellt | Rückverweis | Verantwortlich |
|-----|------|--------|----------|-------------|----------------|
| IT_DOKU | IT_M365 | ✅ | 29.11 | ✅ | AL |
| IT_M365 | IT_DOKU | ✅ | 29.11 | ✅ | AL |
| IT_M365 | HR_CORE | ✅ | 05.12 | ✅ | AL + CS |
| HR_CORE | IT_M365 | ✅ | 05.12 | ✅ | AL + CS |
| IT_OSP | HR_CORE | ✅ | 05.12 | ✅ | AL |
| HR_CORE | IT_OSP | ✅ | 05.12 | ✅ | AL |
| IT_DOKU | KST_PF | ✅ | 22.11 | ✅ | AL + SK |
| KST_PF | IT_DOKU | ✅ | 22.11 | ✅ | AL + SK |
| IT_OSP | IT_RAG | ✅ | 29.11 | ✅ | AL |
| IT_RAG | IT_OSP | ✅ | 29.11 | ✅ | AL |
| OSP_Regeln | KOM_AIR | ✅ | 05.12 | ✅ | AL |
| KOM_AIR | OSP_Regeln | ✅ | 05.12 | ✅ | AL |

**Legende:** → (unidirektional), ← (Rückverweis), ↔ (bidirektional)

---

#### 2.1.2 Fehlende Rückverweise (⏳ TODO)

**Stand:** 05.12.2025 | **Anzahl:** 4

| Von | Nach | Erstellt | Frist | Verantwortlich | Priorität |
|-----|------|----------|-------|----------------|-----------|
| IT_M365 | QM_REK | 29.11 | 06.12 | AL + MR | 🟡 WICHTIG |
| QM_REK | IT_M365 | - | 06.12 | AL + MR | 🟡 WICHTIG |
| IT_M365 | AV_CORE | 29.11 | 13.12 | AL + SV | 🟢 OPTIONAL |
| AV_CORE | IT_M365 | - | 13.12 | AL + SV | 🟢 OPTIONAL |

**Prioritäten:** 🔴 KRITISCH (sofort), 🟡 WICHTIG (zeitnah), 🟢 OPTIONAL (später)

---

#### 2.1.3 Geplante Querverweise (📅 GEPLANT)

**Stand:** 05.12.2025 | **Anzahl:** 6

| Von | Nach | Priorität | Geplant | Verantwortlich | Begründung |
|-----|------|-----------|---------|----------------|------------|
| KST_PF | QM_NZA | 🔴 | 06.12 | SK + AL | Prüffeld → NZA-Prozess |
| KST_PF | QM_REK | 🔴 | 06.12 | SK + AL | Prüffeld → Reklamationen |
| EK_LIBW | CMS_MC | 🔴 | 15.12 | TS + DU | Lieferanten → Compliance |
| AV_CORE | KST_1000 | 🟡 | Q1 26 | SV + SK | AV → Zuschnitt |
| AV_CORE | KST_2000 | 🟡 | Q1 26 | SV + SK | AV → Halbautomaten |
| VT_CORE | KST_ALLG | 🟡 | Q1 26 | SV | Vertrieb → Kostenstellen |

---

### 2.2 RAG-IMPORT-PROTOKOLLE

#### Import-Protokoll 2025-11-29

**Batch:** IT-Dokumentationen | **Verantwortlich:** AL

| Datei | Chunks | Keywords | Token-Eff. | Tests | Status |
|-------|--------|----------|------------|-------|--------|
| IT_DOKU_v2.1_RAG.md | 19 | 150+ | -15% | ✅ 8/8 | ✅ FREIGEGEBEN |
| IT_M365_v1.2_RAG.md | 12 | 80+ | -16% | ✅ 8/8 | ✅ FREIGEGEBEN |
| IT_OSP_v1.0.md | 15 | 90+ | Neu | ✅ 8/8 | ✅ FREIGEGEBEN |

**Gesamt:** 3 Docs, 46 Chunks, 320+ Keywords, -15,5% Ø Token-Eff., 100% Tests ✅

**ChromaDB-Import:** ⏳ Geplant 06.12.2025

---

#### Import-Protokoll TEMPLATE

```markdown
### Import-Protokoll [DATUM]

**Batch:** [Beschreibung] | **Verantwortlich:** [Kürzel]

| Datei | Chunks | Keywords | Token-Eff. | Tests | Status |
|-------|--------|----------|------------|-------|--------|
| [TAG]_[SUB]_vX.X_RAG.md | XX | XX+ | -XX% | ✅/⏳ X/8 | Status |

**Gesamt:** X Docs, X Chunks, X+ Keywords, -X% Ø Token-Eff., X% Tests ✅

**ChromaDB-Import:** [Status]
```

---

## 3. CHANGE-LOG

### November 2025

| Datum | Änderung | Typ | Datei(en) | Verantwortlich |
|-------|----------|-----|-----------|----------------|
| 14.11 | OSP-Projekt Start | Projekt | OSP_TAG_System.md | AL |
| 18.11 | C5 hinzugefügt | Struktur | OSP_TAG_System.md | AL |
| 21.11 | SV L2→L3 | User-Level | HR_CORE_Personalstamm.md | AL |
| 25.11 | Pilot-Phase Start | Projekt | Alle Module | AL |
| 26.11 | OSPUI Go-Live | Infrastruktur | IT_OSP_KI-Chatbot.md | AL |
| 29.11 | L1-L5 → L1-L3 | Struktur | OSP_Regeln.md, KOM_AIR.md | AL |
| 29.11 | RAG-Richtlinie | Governance | IT_RAG_Richtlinie.md | AL |
| 29.11 | KGS Querverweise | System | KOM_KGS.md | AL |
| 29.11 | IT_OSP Projekt-Doku | Neu | IT_OSP_KI-Chatbot.md | AL |
| 29.11 | KGS RAG-Optimierung | System | KOM_KGS.md v2.1 | AL |

---

### Dezember 2025

| Datum | Änderung | Typ | Datei(en) | Verantwortlich |
|-------|----------|-----|-----------|----------------|
| 05.12 | BN → HR_CORE Migration | Struktur | HR_CORE_Personalstamm.md | AL |
| 05.12 | OSP-Level eingeführt | Governance | OSP_Regeln.md v2.0 | AL |
| 05.12 | L1-L3 in KOM_AIR | Update | KOM_AIR v3.0 | AL |
| 06.12 | ChromaDB-Import (erste Docs) | RAG | IT_DOKU, IT_M365, IT_OSP | AL |
| 13.12 | Rückverweise nachtragen | Querverweise | QM_REK, AV_CORE | AL + Team |
| 19.12 | **Pilot-Ende** - Evaluation | Projekt | Alle Module | AL + CS |

---

## QUERVERWEISE

**Bidirektional (↔):**
- ↔ `IT_RAG_Richtlinie_v1.0.md` - Querverweise-Management-Regeln
- ↔ `IT_OSP_KI-Chatbot_v1.0.md` - Projekt-Meilensteine
- ↔ `OSP_Regeln_v2.0.md` - Regel 22 (Bidirektionalität), Regel 31 (OSP-Level)

**Ausgehend (→):**
- → `HR_CORE_Personalstamm.md` - User-Level-Änderungen
- → `OSP_TAG_System_v1.2.md` - C5 Ergänzung
- → `Implementierungs_monitor.md` - Projekt-Status

**Eingehend (←):**
- ← Alle OSP-Docs: Lessons Learned eintragen
- ← Alle RAG-Imports: Protokollieren

---

## ÄNDERUNGSHISTORIE

### [2.2] - 2025-12-05
**LEVEL-MIGRATION L1-L5 → L1-L3:**
- ✅ **Entscheidungstabelle:** SV L3→L4 korrigiert zu SV L2→L3
- ✅ **Neue Entscheidungen:** BN → HR_CORE, OSP-Level, L1-L3 Migration
- ✅ **LL-006 hinzugefügt:** L1-L5 zu komplex → L1-L3 + OSP-Level
- ✅ **Meilenstein M5a:** Level-Migration dokumentiert
- ✅ **BN_CORE → HR_CORE:** Alle Verweise aktualisiert
- ✅ **Change-Log Dez 2025:** Aktualisiert

**Verantwortlich:** AL (KI-Manager)

---

### [2.1] - 2025-11-29
**RAG-OPTIMIERUNG:**
- ✅ **Header kompaktiert** - Token-optimiert
- ✅ **Token-Effizienz:** v2.0 (8.500 Tokens) → v2.1 (6.800 Tokens) = **-20%**
- ✅ **Tabellen kompaktiert** - Spalten gekürzt

**Verantwortlich:** AL (KI-Manager)

---

### [2.0] - 2025-11-29
**MAJOR UPDATE - System-Gedächtnis erweitert:**
- ✅ Querverweise-Tracking-Matrix (Sektion 2.1)
- ✅ RAG-Import-Protokolle (Sektion 2.2)
- ✅ Erweiterte Lessons Learned

**Verantwortlich:** AL (KI-Manager)

---

### [1.0] - 2025-11-18
**Erstversion:**
- ✅ Team-Erinnerungen (Entscheidungen, Lessons Learned)
- ✅ Projekt-Meilensteine
- ✅ Change-Log initialisiert

**Verantwortlich:** AL (KI-Manager)

---

**Status:** ✅ PRODUKTIV (RAG-optimiert)  
**Nächste Review:** 19.12.2025 (Pilot-Ende)  
**ChromaDB-Import:** ✅ JA (KI kann selbst zugreifen)

---

*Kollektives Gedächtnis des OSP-Systems. Alle Entscheidungen, Lessons Learned und Querverweise zentral dokumentiert und für KI durchsuchbar.*

[OSP]
