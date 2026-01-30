# [IT][RAG] RAG-Richtlinie, PDF-Linking & Bilder-Integration

**Version:** 2.5 | **TAG:** [IT][RAG] | **Erstellt:** 2025-11-29 | **Aktualisiert:** 2025-12-23 | **Autor:** AL | **Verantwortlich:** AL (IT & KI-Manager) | **Cluster:** ðŸ”´ C4-Support | **Zugriff:** ðŸ”´ L3-Vertraulich | **Status:** âœ… AKTIV | **Stage:** 2 | **KritikalitÃ¤t:** ðŸŸ¡ MITTEL | **ISO:** 7.5 | **RAG-Version:** 2.5

**Firma:** Rainer Schneider Kabelsatzbau GmbH & Co. KG

| **Primary Keywords:** RAG, ChromaDB, Metadata, PDF-Linking, SharePoint, Bilder-Integration, Logos, Organigramme, Inline-Bilder, Vektordatenbank, Embedding, multilingual-e5-large, Open-WebUI, Claude-API, Dokumentenstruktur, Pipeline, Pre-Processing (25+)

---

## ðŸ”„ MIGRATIONS-HINWEIS (2025-12-10)

> **âš ï¸ DOKUMENTATIONS-UPDATE:**
>
> Diese Datei wurde am **10.12.2025** aktualisiert:
> - âœ… **Querverweise bereinigt** - Aktive vs. Archiv-Referenzen
> - âœ… **Zeitplan aktualisiert** - KW 50/2025 und Q1/2026
> - âœ… **HR_CORE statt BN_CORE** - NamensÃ¤nderung berÃ¼cksichtigt
>
> **Aktive Referenz-Dateien:**
> - `IT_OSP_KI-Chatbot.md` - Haupt-Dokumentation (inkl. System-Prompt)
>
> **Archiv-Referenzen (nur Dokumentation):**
> - `OSP_Regeln.md` - Governance-Dokumentation
> - `OSP_System_Prompt_API.md` - (in IT_OSP migriert)

---

## ZWECK

RAG-Optimierungs-Richtlinie fÃ¼r OSP-Dokumente inkl. SharePoint-PDF-Verlinkung & Bilder-Integration fÃ¼r ChromaDB-Import.

**Scope:**
- Stage 1 â†’ Stage 2 Konvertierung (Markdown-Optimierung)
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
| 0 | MA-Preprocessing | KÃ¼rzel zu kontextreichem String expandieren |
| 1.5 | Keyword-Filter | Kritische Keywords â†’ Dokument direkt laden |
| 2 | Tag-Router | TAGs extrahieren â†’ ChromaDB WHERE-Filter |

### Layer-Architektur

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LAYER 0: OSP_KPL (Dateinamen-Index)                        â”‚
â”‚  â†’ Nur Metadaten fÃ¼r Navigation                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LAYER 1: OSP_KERN (12 Dateien) - DAUERHAFT GELADEN         â”‚
â”‚  â†’ Full-Context Mode fÃ¼r kritische Tabellen                 â”‚
â”‚  â†’ IMMER im RAG-Kontext verfÃ¼gbar                           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LAYER 2: OSP_ERWEITERT (~46 Dateien) - BEI BEDARF          â”‚
â”‚  â†’ Chunked RAG, Routing basierend auf Keywords/TAGs         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LAYER 3: SHAREPOINT (Gelenkte Dokumente)                   â”‚
â”‚  â†’ FormblÃ¤tter (MD): Bidirektional (ausfÃ¼llen+speichern)    â”‚
â”‚  â†’ PDFs/HandbÃ¼cher: Nur Verlinkung                          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Details:** Siehe `IT_OSP_KI_Chatbot.md` â†’ Abschnitt "PIPELINE-ARCHITEKTUR"

---

## PDF-LINKING-STRATEGIE (VEREINFACHT)

### SHAREPOINT-LINKS ZU ORIGINAL-PDFS

**Use Cases:**
- VertrÃ¤ge: AVVs, LieferantenvertrÃ¤ge, RahmenvertrÃ¤ge
- Richtlinien: Datenschutz, Arbeitssicherheit, Compliance
- Zertifikate: ISO 9001, UL, Automotive
- Formulare: QM-Formulare, Checklisten
- Policies: QualitÃ¤tspolitik, Umweltpolitik
- Normen: ISO 9001, IPC-WHMA-A-620, DIN (Volltext-Zugriff)
- HandbÃ¼cher: Management-Handbuch, Maschinen-HandbÃ¼cher

**SharePoint-Basis-URL:**
```
https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/
```

**Ordnerstruktur:**
```
Freigegebene Dokumente/
â”œâ”€â”€ Normen/                    # ISO, DIN, IPC, UL
â”œâ”€â”€ Vertraege/                 # AVVs, Lieferanten, Rahmen
â”œâ”€â”€ Richtlinien/               # DSGVO, Arbeitssicherheit
â”œâ”€â”€ Zertifikate/               # ISO 9001, UL, Automotive
â”œâ”€â”€ Formblaetter/              # QM-Formulare, Checklisten
â”œâ”€â”€ Handbuecher/               # Management-HB, Maschinen-HB
â”œâ”€â”€ Policies/                  # QualitÃ¤t, Umwelt, Energie
â”œâ”€â”€ Gesetze/                   # DSGVO, BDSG (Volltexte)
â””â”€â”€ Icons_Bilder/              # Logos, Organigramme, Diagramme
```

**Markdown-Syntax (Abschnitt am Ende jeder Datei):**
```markdown
## ORIGINAL-DOKUMENTE

**[Kategorie] (SharePoint):**
- [Dokumentname](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/ORDNER/DATEI.pdf) - Kurzbeschreibung
```

**Vorteile:**
- âœ… Einfach umzusetzen (nur Links kopieren)
- âœ… Kein manuelles Seitenzahlen-Ermitteln
- âœ… Trotzdem voller Zugriff auf Original-PDFs
- âœ… User kann selbst navigieren (Strg+F, Bookmarks)
- âœ… RAG-optimiert (Link in Metadata)

---

## BILDER-LINKING-STRATEGIE (INLINE-BILDER)

### SHAREPOINT-BILDER INLINE RENDERN

**Use Cases:**
- **Corporate Identity:** Firmenlogos, OSP-Logo, Partnerlogos
- **Organisation:** Organigramme, Prozessdiagramme
- **Technik:** Maschinenlayouts, FertigungsplÃ¤ne, Netzwerk-Topologien
- **QualitÃ¤t:** Flussdiagramme, Prozess-Workflows
- **Compliance:** Zertifikate (visuell), Label-Beispiele

**SharePoint-Ordner:**
```
Icons_Bilder/
â”œâ”€â”€ Logo_OSP.png               # OSP-Projekt-Logo
â”œâ”€â”€ Logo_OSP_Text.png          # OSP mit Text
â”œâ”€â”€ Logo_schneider.png         # Firmenlogo Schneider
â”œâ”€â”€ logo_sas.jpg               # Schneider Automotive Solutions
â”œâ”€â”€ Organigramm.png            # Unternehmensstruktur
â””â”€â”€ OSP_Icon_Bibliothek.html   # Icon-Ãœbersicht
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
- âœ… Bilder direkt sichtbar (visuell ansprechend)
- âœ… Alt-Text fÃ¼r Barrierefreiheit & RAG-Metadata
- âœ… Markdown-Standard-Syntax
- âœ… ChromaDB kann Alt-Text indexieren

**EMPFEHLUNG:** INLINE fÃ¼r Logos & Organigramme, LINK-LISTE fÃ¼r groÃŸe technische Diagramme (>5 MB)

---

## CHROMADB-METADATA-SCHEMA (ERWEITERT)

**Metadata-Felder fÃ¼r PDF-Linking + Bilder:**

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
- `layout` - Maschinenlayouts, FertigungsplÃ¤ne
- `flowchart` - Prozess-Workflows, EntscheidungsbÃ¤ume
- `certificate` - Zertifikate (visuell)
- `screenshot` - UI-Screenshots, System-Ansichten

---

## IMPLEMENTIERUNG (1 PHASE - EINFACH!)

### SHAREPOINT-LINKS EINFÃœGEN

**Workflow (5 Schritte):**

**Schritt 1: SharePoint-Ordner vorbereiten**
1. SharePoint Ã¶ffnen: https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP
2. Ordner erstellen (falls nicht vorhanden)
3. PDFs & Bilder hochladen (richtiger Ordner)
4. Dateinamen prÃ¼fen (keine Leerzeichen, keine Umlaute)

**Schritt 2: SharePoint-Links kopieren**
- Methode: PDF/Bild in SharePoint Ã¶ffnen â†’ Browser-Adresszeile kopieren

**Schritt 3: Markdown-Datei erweitern**
- Abschnitt "## ORIGINAL-DOKUMENTE" fÃ¼r PDFs
- Abschnitt "## GRAFIKEN & DIAGRAMME" fÃ¼r Bilder

**Schritt 4: Testen**
- Link im Browser Ã¶ffnen
- PDF/Bild sollte in SharePoint Ã¶ffnen

**Schritt 5: ChromaDB-Import aktualisieren**
- Metadata aus Markdown parsen (Python-Script)
- pdf_originals & image_assets in Metadata einfÃ¼gen

---

## BETROFFENE MODULE & PRIORITÃ„T

### PDF-LINKING - PRIORITÃ„T 1 (5 Module, ~2h)

| Modul | Dateien | PDFs | Aufwand |
|-------|---------|------|---------|
| **IT_DS** | IT_DS_Datenschutz.md | 10-12 | 30 min |
| **QM_CORE** | QM_CORE_Qualitaetspolitik.md | 5-7 | 20 min |
| **CMS_MC** | CMS_MC_Material_Compliance.md | 8-10 | 25 min |
| **TM_CORE** | TM_CORE_Maschinen_Anlagen.md | 6-8 | 20 min |
| **ORG_LEIT** | ORG_LEIT_Leitbild_Vision.md | 2-3 | 10 min |

### PDF-LINKING - PRIORITÃ„T 2 (6 Module, ~1,5h)

| Modul | Dateien | PDFs | Aufwand |
|-------|---------|------|---------|
| **HR_CORE** | HR_CORE_Personalstamm.md | 4-6 | 15 min |
| **AV_CORE** | AV_CORE_Arbeitsvorbereitung.md | 3-5 | 15 min |
| **VT_CORE** | VT_CORE_Vertrieb_Auftragsabwicklung.md | 2-4 | 10 min |
| **EK_SEK** | EK_SEK_Strategischer_Einkauf.md | 3-5 | 15 min |
| **PM_CORE** | PM_CORE_Aktuelle_Projekte.md | 2-3 | 10 min |
| **GF_STR** | GF_STR_Strategische_Ausrichtung.md | 2-3 | 10 min |

### BILDER-LINKING - PRIORITÃ„T 1 (2 Module, ~20 min)

| Modul | Bilder | Use Case |
|-------|--------|----------|
| **KOM_CORE** | 3 Logos | Firmenlogos, CI |
| **ORG_ORGA** | 1 Organigramm | Unternehmensstruktur |

### BILDER-LINKING - PRIORITÃ„T 2 (3 Module, ~30 min)

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
- Keine Umlaute (Ã¤â†’ae, Ã¶â†’oe, Ã¼â†’ue, ÃŸâ†’ss)
- Keine Sonderzeichen auÃŸer `_` und `-`

**Beispiele:**
- âœ… `ISO_9001_2015.pdf`
- âœ… `Logo_schneider.png`
- âŒ `ISO 9001 (2015).pdf`

### 2. LINK-WARTUNG

**RegelmÃ¤ÃŸige Checks:**
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

## NÃ„CHSTE SCHRITTE

### SOFORT (KW 50/2025)

1. â³ **PDFs hochladen:** PrioritÃ¤t 1 Module
2. â³ **KOM_CORE:** Abschnitt "GRAFIKEN & DIAGRAMME" (3 Logos)
3. â³ **ORG_ORGA:** Organigramm einbinden

### Kurzfristig (Jan 2026)

4. â³ **PrioritÃ¤t 1 komplett:** Alle 5 Module mit PDF-Links
5. â³ **PrioritÃ¤t 2 starten:** HR, AV, VT, EK, PM, GF
6. â³ **Link-Validierung:** Python-Script testen

### Mittelfristig (Q1 2026)

7. â³ **PrioritÃ¤t 3:** RES, KST, DMS, KOM
8. â³ **ChromaDB-Import erweitern:** pdf_originals + image_assets
9. â³ **Quartalsweise Link-Validierung** automatisieren

---

## QUERVERWEISE

**Bidirektional (â†”):**
- â†” `IT_OSP_KI-Chatbot.md` - Haupt-Dokumentation, ChromaDB-Konfiguration, System-Prompt
- â†” `IT_DOKU_IT-Dokumentation.md` - Server-Infrastruktur

**Ausgehend (â†’):**
- â†’ `KOM_CORE_Corporate_Identity.md` - Firmenlogos, CI-Guideline
- â†’ `ORG_ORGA_Unternehmensstruktur.md` - Organigramm
- â†’ `HR_CORE_Personalstamm.md` - Berechtigungen

**Archiv-Referenzen (nur Dokumentation):**
- â† `OSP_Regeln.md` - Governance-Regeln (historisch)
- â† `OSP_TAG_System.md` - TAG-System (historisch)

**Extern:**
- SharePoint OSP: https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP

---

## Ã„NDERUNGSHISTORIE

### [2.4] - 2025-12-23 - PIPELINE-ARCHITEKTUR

**Ã„nderungen:**
- âœ… Neuer Abschnitt "PIPELINE-ARCHITEKTUR" hinzugefÃ¼gt
- âœ… Pre-Processing-Module dokumentiert (Query-Normalizer, MA-Preprocessing, Keyword-Filter, Tag-Router)
- âœ… Layer-Architektur aktualisiert (4 Layer inkl. OSP_KPL)
- âœ… Verweis auf IT_OSP_KI-Chatbot.md fÃ¼r Details

**Verantwortlich:** AL (QM & KI-Manager)

---

### [2.3] - 2025-12-10 - DOKUMENTATIONS-UPDATE

**Ã„nderungen:**
- âœ… **Querverweise bereinigt** - Aktive vs. Archiv-Referenzen
- âœ… **IT_OSP_KI-Chatbot.md** als Haupt-Referenz
- âœ… **HR_CORE statt BN_CORE** - NamensÃ¤nderung
- âœ… **Zeitplan aktualisiert** - KW 50/2025 und Q1/2026
- âœ… **Migrations-Hinweis hinzugefÃ¼gt**
- âœ… **Dokument gestrafft** - Redundanzen entfernt

**Verantwortlich:** AL (QM & KI-Manager)

---

### [2.2] - 2025-11-29 - BILDER-INTEGRATION (INLINE)

- âœ… Bilder-Linking-Strategie hinzugefÃ¼gt
- âœ… ChromaDB-Metadata: image_assets Feld
- âœ… Python-Scripts: extract_image_assets()

---

### [2.1] - 2025-11-29 - VEREINFACHUNG

- âŒ Deep-Links ENTFERNT
- âœ… Fokus auf SharePoint-Links

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

**RAG-Version:** 2.5  
**Primary Keywords:** RAG, ChromaDB, Metadata, PDF-Linking, SharePoint, Bilder-Integration, Logos, Organigramme, Open-WebUI, Claude-API, multilingual-e5-large

**Secondary Keywords:** ISO 9001, IPC-WHMA-A-620, DSGVO, Link-Validierung, pdf_originals, image_assets

**User-Level:** L3 (Vertraulich)  
**Chunk-Anzahl:** ~10 Chunks  
**Chunk-GrÃ¶ÃŸe:** 800-1200 Tokens

---

**Status:** âœ… AKTIV  
**KritikalitÃ¤t:** ðŸŸ¡ MITTEL  
**Aufwand Gesamt:** ~6,5 Stunden  
**NÃ¤chste Review:** Jan 2026

---

*RAG-Richtlinie fÃ¼r SharePoint-PDF-Linking & Bilder-Integration. Einfache Umsetzung ohne Deep-Links.*

(C: 100%) [OSP]
