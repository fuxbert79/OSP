# [IT][RAG] RAG-Richtlinie, PDF-Linking & Bilder-Integration

**Version:** 2.4 | **TAG:** [IT][RAG] | **Erstellt:** 2025-11-29 | **Aktualisiert:** 2025-12-15 | **Autor:** AL | **Verantwortlich:** AL (IT & KI-Manager) | **Cluster:** 🔴 C4-Support | **Zugriff:** 🔴 L3-Vertraulich | **Status:** ✅ AKTIV | **Stage:** 2 | **Kritikalität:** 🟡 MITTEL | **ISO:** 7.5 | **RAG-Version:** 2.4

**Firma:** Rainer Schneider Kabelsatzbau GmbH & Co. KG

| **Primary Keywords:** RAG, ChromaDB, Metadata, PDF-Linking, SharePoint, Bilder-Integration, Logos, Organigramme, Inline-Bilder, Vektordatenbank, Embedding, multilingual-e5-large, Open-WebUI, Claude-API, Dokumentenstruktur, Pipeline, Pre-Processing (25+)

---

## 🔄 MIGRATIONS-HINWEIS (2025-12-10)

> **⚠️ DOKUMENTATIONS-UPDATE:**
>
> Diese Datei wurde am **10.12.2025** aktualisiert:
> - ✅ **Querverweise bereinigt** - Aktive vs. Archiv-Referenzen
> - ✅ **Zeitplan aktualisiert** - KW 50/2025 und Q1/2026
> - ✅ **HR_CORE statt BN_CORE** - Namensänderung berücksichtigt
>
> **Aktive Referenz-Dateien:**
> - `IT_OSP_KI-Chatbot.md` - Haupt-Dokumentation (inkl. System-Prompt)
>
> **Archiv-Referenzen (nur Dokumentation):**
> - `OSP_Regeln.md` - Governance-Dokumentation
> - `OSP_System_Prompt_API.md` - (in IT_OSP migriert)

---

## ZWECK

RAG-Optimierungs-Richtlinie für OSP-Dokumente inkl. SharePoint-PDF-Verlinkung & Bilder-Integration für ChromaDB-Import.

**Scope:**
- Stage 1 → Stage 2 Konvertierung (Markdown-Optimierung)
- ChromaDB-Metadata-Schema
- PDF-Original-Verlinkung (SharePoint) - EINFACH & SCHNELL
- **BILDER-Integration (Inline-Rendering)**
- Batch-Processing-Protokolle

**WICHTIG:** Fokus auf EINFACHE Umsetzung - keine Deep-Links, keine manuellen Seitenzahlen!

---

## PIPELINE-ARCHITEKTUR (NEU v2.4)

### Pre-Processing-Module

Seit 15.12.2025 werden Queries durch **4 Pre-Processing-Module** optimiert, bevor sie an ChromaDB gehen:

| Step | Modul | Funktion |
|------|-------|----------|
| -1 | Query-Normalizer | Tippfehler korrigieren, Lowercase |
| 0 | MA-Preprocessing | Kürzel zu kontextreichem String expandieren |
| 1.5 | Keyword-Filter | Kritische Keywords → Dokument direkt laden |
| 2 | Tag-Router | TAGs extrahieren → ChromaDB WHERE-Filter |

### Layer-Architektur (v2.2 - NEU: Layer 1-4)

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: OSP_KERN (12 Dateien) - DAUERHAFT GELADEN         │
│  → Full-Context Mode für kritische Tabellen                 │
│  → IMMER im RAG-Kontext verfügbar                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: OSP_ERWEITERT (~46 Dateien) - BEI BEDARF          │
│  → Chunked RAG, Routing basierend auf Keywords/TAGs         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: OSP_KPL (Dateinamen-Index)                        │
│  → Nur Metadaten für Navigation                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: SHAREPOINT (Gelenkte Dokumente)                   │
│  → Formblätter (MD): Bidirektional (ausfüllen+speichern)    │
│  → PDFs/Handbücher: Nur Verlinkung                          │
└─────────────────────────────────────────────────────────────┘
```

**Details:** Siehe `IT_OSP_KI_Chatbot.md` → Abschnitt "PIPELINE-ARCHITEKTUR"

---

## PDF-LINKING-STRATEGIE (VEREINFACHT)

### SHAREPOINT-LINKS ZU ORIGINAL-PDFS

**Use Cases:**
- Verträge: AVVs, Lieferantenverträge, Rahmenverträge
- Richtlinien: Datenschutz, Arbeitssicherheit, Compliance
- Zertifikate: ISO 9001, UL, Automotive
- Formulare: QM-Formulare, Checklisten
- Policies: Qualitätspolitik, Umweltpolitik
- Normen: ISO 9001, IPC-WHMA-A-620, DIN (Volltext-Zugriff)
- Handbücher: Management-Handbuch, Maschinen-Handbücher

**SharePoint-Basis-URL:**
```
https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/
```

**Ordnerstruktur:**
```
Freigegebene Dokumente/
├── Normen/                    # ISO, DIN, IPC, UL
├── Vertraege/                 # AVVs, Lieferanten, Rahmen
├── Richtlinien/               # DSGVO, Arbeitssicherheit
├── Zertifikate/               # ISO 9001, UL, Automotive
├── Formblaetter/              # QM-Formulare, Checklisten
├── Handbuecher/               # Management-HB, Maschinen-HB
├── Policies/                  # Qualität, Umwelt, Energie
├── Gesetze/                   # DSGVO, BDSG (Volltexte)
└── Icons_Bilder/              # Logos, Organigramme, Diagramme
```

**Markdown-Syntax (Abschnitt am Ende jeder Datei):**
```markdown
## ORIGINAL-DOKUMENTE

**[Kategorie] (SharePoint):**
- [Dokumentname](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/ORDNER/DATEI.pdf) - Kurzbeschreibung
```

**Vorteile:**
- ✅ Einfach umzusetzen (nur Links kopieren)
- ✅ Kein manuelles Seitenzahlen-Ermitteln
- ✅ Trotzdem voller Zugriff auf Original-PDFs
- ✅ User kann selbst navigieren (Strg+F, Bookmarks)
- ✅ RAG-optimiert (Link in Metadata)

---

## BILDER-LINKING-STRATEGIE (INLINE-BILDER)

### SHAREPOINT-BILDER INLINE RENDERN

**Use Cases:**
- **Corporate Identity:** Firmenlogos, OSP-Logo, Partnerlogos
- **Organisation:** Organigramme, Prozessdiagramme
- **Technik:** Maschinenlayouts, Fertigungspläne, Netzwerk-Topologien
- **Qualität:** Flussdiagramme, Prozess-Workflows
- **Compliance:** Zertifikate (visuell), Label-Beispiele

**SharePoint-Ordner:**
```
Icons_Bilder/
├── Logo_OSP.png               # OSP-Projekt-Logo
├── Logo_OSP_Text.png          # OSP mit Text
├── Logo_schneider.png         # Firmenlogo Schneider
├── logo_sas.jpg               # Schneider Automotive Solutions
├── Organigramm.png            # Unternehmensstruktur
└── OSP_Icon_Bibliothek.html   # Icon-Übersicht
```

**Markdown-Syntax (INLINE):**
```markdown
## GRAFIKEN & DIAGRAMME

**Firmenlogo:**
![Schneider Kabelsatzbau Logo](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Logo_schneider.png)

**Organigramm:**
![Unternehmensstruktur 2025](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Organigramm.png)
```

**Vorteile INLINE-Bilder:**
- ✅ Bilder direkt sichtbar (visuell ansprechend)
- ✅ Alt-Text für Barrierefreiheit & RAG-Metadata
- ✅ Markdown-Standard-Syntax
- ✅ ChromaDB kann Alt-Text indexieren

**EMPFEHLUNG:** INLINE für Logos & Organigramme, LINK-LISTE für große technische Diagramme (>5 MB)

---

## CHROMADB-METADATA-SCHEMA (ERWEITERT)

**Metadata-Felder für PDF-Linking + Bilder:**

```python
metadata = {
    # Bestehende Felder
    "source": "KOM_CORE_Corporate_Identity.md",
    "tag": "KOM",
    "sub_tag": "CORE",
    "cluster": "C1",
    "version": "1.1",
    "chunk_id": "CH02",
    "user_level": "L1",
    "keywords": ["Corporate Identity", "Logo", "CI"],
    
    # PDF-Linking-Felder
    "source_type": "markdown_rag",
    "pdf_originals": [
        {
            "title": "CI-Guideline 2025",
            "url": "https://rainerschneiderkabelsatz.sharepoint.com/.../Richtlinien/CI_Guideline.pdf",
            "type": "richtlinie",
            "category": "Richtlinien"
        }
    ],
    
    # BILDER-FELDER
    "image_assets": [
        {
            "type": "logo",
            "alt_text": "Schneider Kabelsatzbau Logo",
            "url": "https://rainerschneiderkabelsatz.sharepoint.com/.../Icons_Bilder/Logo_schneider.png",
            "category": "corporate_identity"
        },
        {
            "type": "diagram",
            "alt_text": "Unternehmensstruktur 2025",
            "url": "https://rainerschneiderkabelsatz.sharepoint.com/.../Icons_Bilder/Organigramm.png",
            "category": "organization"
        }
    ]
}
```

**Bild-Typen:**
- `logo` - Firmenlogos, Partnerlogos
- `diagram` - Organigramme, Prozessdiagramme
- `layout` - Maschinenlayouts, Fertigungspläne
- `flowchart` - Prozess-Workflows, Entscheidungsbäume
- `certificate` - Zertifikate (visuell)
- `screenshot` - UI-Screenshots, System-Ansichten

---

## IMPLEMENTIERUNG (1 PHASE - EINFACH!)

### SHAREPOINT-LINKS EINFÜGEN

**Workflow (5 Schritte):**

**Schritt 1: SharePoint-Ordner vorbereiten**
1. SharePoint öffnen: https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP
2. Ordner erstellen (falls nicht vorhanden)
3. PDFs & Bilder hochladen (richtiger Ordner)
4. Dateinamen prüfen (keine Leerzeichen, keine Umlaute)

**Schritt 2: SharePoint-Links kopieren**
- Methode: PDF/Bild in SharePoint öffnen → Browser-Adresszeile kopieren

**Schritt 3: Markdown-Datei erweitern**
- Abschnitt "## ORIGINAL-DOKUMENTE" für PDFs
- Abschnitt "## GRAFIKEN & DIAGRAMME" für Bilder

**Schritt 4: Testen**
- Link im Browser öffnen
- PDF/Bild sollte in SharePoint öffnen

**Schritt 5: ChromaDB-Import aktualisieren**
- Metadata aus Markdown parsen (Python-Script)
- pdf_originals & image_assets in Metadata einfügen

---

## BETROFFENE MODULE & PRIORITÄT

### PDF-LINKING - PRIORITÄT 1 (5 Module, ~2h)

| Modul | Dateien | PDFs | Aufwand |
|-------|---------|------|---------|
| **IT_DS** | IT_DS_Datenschutz.md | 10-12 | 30 min |
| **QM_CORE** | QM_CORE_Qualitaetspolitik.md | 5-7 | 20 min |
| **CMS_MC** | CMS_MC_Material_Compliance.md | 8-10 | 25 min |
| **TM_CORE** | TM_CORE_Maschinen_Anlagen.md | 6-8 | 20 min |
| **ORG_LEIT** | ORG_LEIT_Leitbild_Vision.md | 2-3 | 10 min |

### PDF-LINKING - PRIORITÄT 2 (6 Module, ~1,5h)

| Modul | Dateien | PDFs | Aufwand |
|-------|---------|------|---------|
| **HR_CORE** | HR_CORE_Personalstamm.md | 4-6 | 15 min |
| **AV_CORE** | AV_CORE_Arbeitsvorbereitung.md | 3-5 | 15 min |
| **VT_CORE** | VT_CORE_Vertrieb_Auftragsabwicklung.md | 2-4 | 10 min |
| **EK_SEK** | EK_SEK_Strategischer_Einkauf.md | 3-5 | 15 min |
| **PM_CORE** | PM_CORE_Aktuelle_Projekte.md | 2-3 | 10 min |
| **GF_STR** | GF_STR_Strategische_Ausrichtung.md | 2-3 | 10 min |

### BILDER-LINKING - PRIORITÄT 1 (2 Module, ~20 min)

| Modul | Bilder | Use Case |
|-------|--------|----------|
| **KOM_CORE** | 3 Logos | Firmenlogos, CI |
| **ORG_ORGA** | 1 Organigramm | Unternehmensstruktur |

### BILDER-LINKING - PRIORITÄT 2 (3 Module, ~30 min)

| Modul | Bilder | Use Case |
|-------|--------|----------|
| **QM_CORE** | 2 Workflows | QM-Prozesse |
| **AV_CORE** | 2 Diagramme | AV-Prozesse |
| **TM_CORE** | 1-2 Layouts | Fertigungslayouts |

**GESAMTAUFWAND:** ~6,5 Stunden

---

## BEST PRACTICES

### 1. DATEINAMEN-KONVENTION

**Format:** `Kategorie_Bezeichnung_Version.ext`

**Regeln:**
- Keine Leerzeichen (verwende `_`)
- Keine Umlaute (ä→ae, ö→oe, ü→ue, ß→ss)
- Keine Sonderzeichen außer `_` und `-`

**Beispiele:**
- ✅ `ISO_9001_2015.pdf`
- ✅ `Logo_schneider.png`
- ❌ `ISO 9001 (2015).pdf`

### 2. LINK-WARTUNG

**Regelmäßige Checks:**
- Quartalsweise: Broken-Link-Check (Python-Script)
- Nach SharePoint-Umstrukturierung: Alle Links validieren

**Python-Script (Broken-Link-Checker):**
```python
import requests
import re

def validate_links(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    links = re.findall(r'\((https://.*?\.(?:pdf|png|jpg|svg).*?)\)', content)
    
    for link in links:
        try:
            response = requests.head(link, timeout=5)
            status = "OK" if response.status_code == 200 else f"BROKEN ({response.status_code})"
            print(f"{status}: {link}")
        except Exception as e:
            print(f"ERROR: {link} ({e})")
```

---

## MARKDOWN-TEMPLATE

**Quick-Start Template (Copy & Paste):**

```markdown
---

## ORIGINAL-DOKUMENTE

**Vertraege (SharePoint):**
- [Dokumentname](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Vertraege/DATEI.pdf) - Kurzbeschreibung

**Richtlinien (SharePoint):**
- [Dokumentname](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Richtlinien/DATEI.pdf) - Kurzbeschreibung

---

## GRAFIKEN & DIAGRAMME

**[Kategorie-Name]:**
![Alt-Text](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/DATEI.png)
*Verwendung: [Beschreibung]*

---
```

---

## NÄCHSTE SCHRITTE

### SOFORT (KW 50/2025)

1. ⏳ **PDFs hochladen:** Priorität 1 Module
2. ⏳ **KOM_CORE:** Abschnitt "GRAFIKEN & DIAGRAMME" (3 Logos)
3. ⏳ **ORG_ORGA:** Organigramm einbinden

### Kurzfristig (Jan 2026)

4. ⏳ **Priorität 1 komplett:** Alle 5 Module mit PDF-Links
5. ⏳ **Priorität 2 starten:** HR, AV, VT, EK, PM, GF
6. ⏳ **Link-Validierung:** Python-Script testen

### Mittelfristig (Q1 2026)

7. ⏳ **Priorität 3:** RES, KST, DMS, KOM
8. ⏳ **ChromaDB-Import erweitern:** pdf_originals + image_assets
9. ⏳ **Quartalsweise Link-Validierung** automatisieren

---

## QUERVERWEISE

**Bidirektional (↔):**
- ↔ `IT_OSP_KI-Chatbot.md` - Haupt-Dokumentation, ChromaDB-Konfiguration, System-Prompt
- ↔ `IT_DOKU_IT-Dokumentation.md` - Server-Infrastruktur

**Ausgehend (→):**
- → `KOM_CORE_Corporate_Identity.md` - Firmenlogos, CI-Guideline
- → `ORG_ORGA_Unternehmensstruktur.md` - Organigramm
- → `HR_CORE_Personalstamm.md` - Berechtigungen

**Archiv-Referenzen (nur Dokumentation):**
- ← `OSP_Regeln.md` - Governance-Regeln (historisch)
- ← `OSP_TAG_System.md` - TAG-System (historisch)

**Extern:**
- SharePoint OSP: https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP

---

## ÄNDERUNGSHISTORIE

### [2.4] - 2025-12-15 - PIPELINE-ARCHITEKTUR

**Änderungen:**
- ✅ Neuer Abschnitt "PIPELINE-ARCHITEKTUR" hinzugefügt
- ✅ Pre-Processing-Module dokumentiert (Query-Normalizer, MA-Preprocessing, Keyword-Filter, Tag-Router)
- ✅ Layer-Architektur aktualisiert (4 Layer inkl. OSP_KPL)
- ✅ Verweis auf IT_OSP_KI-Chatbot.md für Details

**Verantwortlich:** AL (QM & KI-Manager)

---

### [2.3] - 2025-12-10 - DOKUMENTATIONS-UPDATE

**Änderungen:**
- ✅ **Querverweise bereinigt** - Aktive vs. Archiv-Referenzen
- ✅ **IT_OSP_KI-Chatbot.md** als Haupt-Referenz
- ✅ **HR_CORE statt BN_CORE** - Namensänderung
- ✅ **Zeitplan aktualisiert** - KW 50/2025 und Q1/2026
- ✅ **Migrations-Hinweis hinzugefügt**
- ✅ **Dokument gestrafft** - Redundanzen entfernt

**Verantwortlich:** AL (QM & KI-Manager)

---

### [2.2] - 2025-11-29 - BILDER-INTEGRATION (INLINE)

- ✅ Bilder-Linking-Strategie hinzugefügt
- ✅ ChromaDB-Metadata: image_assets Feld
- ✅ Python-Scripts: extract_image_assets()

---

### [2.1] - 2025-11-29 - VEREINFACHUNG

- ❌ Deep-Links ENTFERNT
- ✅ Fokus auf SharePoint-Links

---

### [2.0] - 2025-11-29 - PDF-LINKING-STRATEGIE

- SharePoint-Links zu Original-PDFs
- ChromaDB-Metadata-Schema erweitert

---

### [1.0] - 2025-11-23 - ERSTVERSION

- RAG-Optimierungs-Workflow
- Batch-Processing-Protokolle

---

## RAG-METADATA

**RAG-Version:** 2.4  
**Primary Keywords:** RAG, ChromaDB, Metadata, PDF-Linking, SharePoint, Bilder-Integration, Logos, Organigramme, Open-WebUI, Claude-API, multilingual-e5-large

**Secondary Keywords:** ISO 9001, IPC-WHMA-A-620, DSGVO, Link-Validierung, pdf_originals, image_assets

**User-Level:** L3 (Vertraulich)  
**Chunk-Anzahl:** ~10 Chunks  
**Chunk-Größe:** 800-1200 Tokens

---

**Status:** ✅ AKTIV  
**Kritikalität:** 🟡 MITTEL  
**Aufwand Gesamt:** ~6,5 Stunden  
**Nächste Review:** Jan 2026

---

*RAG-Richtlinie für SharePoint-PDF-Linking & Bilder-Integration. Einfache Umsetzung ohne Deep-Links.*

(C: 100%) [OSP]
