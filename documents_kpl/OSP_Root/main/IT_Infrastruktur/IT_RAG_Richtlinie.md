# [IT][RAG] RAG-Richtlinie, PDF-Linking & Bilder-Integration

Version: 2.2 | TAG: [IT][RAG] | Erstellt: 2025-11-29 | Aktualisiert: 2025-11-29 | Autor: AL | Verantwortlich: AL (IT & KI-Manager) | Cluster: C4-Support | Zugriff: L3-Führung | Status: AKTIV | Stage: 2

**Firma:** Rainer Schneider Kabelsatzbau GmbH & Co. KG

---

## ZWECK

RAG-Optimierungs-Richtlinie für OSP-Dokumente inkl. SharePoint-PDF-Verlinkung & Bilder-Integration für ChromaDB-Import.

**Scope:**
- Stage 1 → Stage 2 Konvertierung (Markdown-Optimierung)
- ChromaDB-Metadata-Schema
- PDF-Original-Verlinkung (SharePoint) - EINFACH & SCHNELL
- **BILDER-Integration (Inline-Rendering) - NEU v2.2!**
- Batch-Processing-Protokolle

**WICHTIG:** Fokus auf EINFACHE Umsetzung - keine Deep-Links, keine manuellen Seitenzahlen!

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
├── Verträge/                  # AVVs, Lieferanten, Rahmen
├── Richtlinien/               # DSGVO, Arbeitssicherheit
├── Zertifikate/               # ISO 9001, UL, Automotive
├── Formulare/                 # QM-Formulare, Checklisten
├── Handbücher/                # Management-HB, Maschinen-HB
├── Policies/                  # Qualität, Umwelt, Energie
├── Gesetze/                   # DSGVO, BDSG (Volltexte)
└── Icons_Bilder/              # 🆕 Logos, Organigramme, Diagramme
```

**Markdown-Syntax (Abschnitt am Ende jeder Datei):**
```markdown
## ORIGINAL-DOKUMENTE

**[Kategorie] (SharePoint):**
- [Dokumentname](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/ORDNER/DATEI.pdf) - Kurzbeschreibung
```

**Beispiel in IT_DS_Datenschutz.md:**
```markdown
## ORIGINAL-DOKUMENTE

**Verträge (SharePoint):**
- [AVV Terra Cloud](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/AVV_Terra_Cloud.pdf) - Auftragsverarbeitungsvertrag Backup
- [AVV Gromnitza IT](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/AVV_Gromnitza.pdf) - IT-Support & Beratung

**Richtlinien (SharePoint):**
- [Datenschutz-Richtlinie](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Richtlinien/Datenschutz_Richtlinie.pdf) - Interne Richtlinie

**Normen (SharePoint):**
- [ISO 9001:2015 Volltext](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Normen/ISO_9001_2015.pdf) - ISO 9001:2015 Norm
- [DSGVO Gesetzestext](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Gesetze/DSGVO.pdf) - EU 2016/679
```

**Vorteile:**
- ✅ Einfach umzusetzen (nur Links kopieren)
- ✅ Kein manuelles Seitenzahlen-Ermitteln
- ✅ Trotzdem voller Zugriff auf Original-PDFs
- ✅ User kann selbst navigieren (Strg+F, Bookmarks)
- ✅ RAG-optimiert (Link in Metadata)

---

## 🆕 BILDER-LINKING-STRATEGIE (INLINE-BILDER)

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

**Markdown-Syntax (INLINE - Option A):**
```markdown
## GRAFIKEN & DIAGRAMME

**Firmenlogo:**
![Schneider Kabelsatzbau Logo](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Logo_schneider.png)

**Organigramm:**
![Unternehmensstruktur 2025](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Organigramm.png)
```

**Beispiel in KOM_CORE_Corporate_Identity.md:**
```markdown
## GRAFIKEN & DIAGRAMME

**Corporate Identity - Firmenlogos:**

**Hauptlogo Schneider Kabelsatzbau:**
![Schneider Kabelsatzbau Logo](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Logo_schneider.png)
*Verwendung: Geschäftspapiere, Website, Präsentationen*

**OSP-Projekt-Logo:**
![OSP Organisation System Prompt](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Logo_OSP.png)
*Verwendung: OSP-Dokumentation, SharePoint*

**Schneider Automotive Solutions (SAS):**
![SAS Logo](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/logo_sas.jpg)
*Verwendung: Automotive-Kunden, Zertifizierungen*
```

**Beispiel in ORG_ORGA_Unternehmensstruktur.md:**
```markdown
## GRAFIKEN & DIAGRAMME

**Organigramm 2025:**
![Unternehmensstruktur Schneider Kabelsatzbau](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Organigramm.png)

Das Organigramm zeigt die Hierarchie:
- Geschäftsführung (CS)
- Prokurist (SV)
- Abteilungsleiter (AL, TS, MD, etc.)
- Teams & Kostenstellen
```

**Vorteile INLINE-Bilder:**
- ✅ Bilder direkt sichtbar (visuell ansprechend)
- ✅ Alt-Text für Barrierefreiheit & RAG-Metadata
- ✅ Markdown-Standard-Syntax
- ✅ Konsistent mit Dokumentation
- ✅ ChromaDB kann Alt-Text indexieren

**Nachteile vs. Link-Liste:**
- ❌ Keine Kurzbeschreibung (stattdessen Alt-Text)
- ❌ Bild muss laden (kann langsam sein bei großen Dateien)

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
    
    # 🆕 BILDER-FELDER (NEU v2.2)
    "image_assets": [
        {
            "type": "logo",
            "alt_text": "Schneider Kabelsatzbau Logo",
            "url": "https://rainerschneiderkabelsatz.sharepoint.com/.../Icons_Bilder/Logo_schneider.png",
            "category": "corporate_identity",
            "usage": "Geschäftspapiere, Website, Präsentationen"
        },
        {
            "type": "logo",
            "alt_text": "OSP Organisation System Prompt",
            "url": "https://rainerschneiderkabelsatz.sharepoint.com/.../Icons_Bilder/Logo_OSP.png",
            "category": "corporate_identity",
            "usage": "OSP-Dokumentation, SharePoint"
        },
        {
            "type": "diagram",
            "alt_text": "Unternehmensstruktur 2025",
            "url": "https://rainerschneiderkabelsatz.sharepoint.com/.../Icons_Bilder/Organigramm.png",
            "category": "organization",
            "usage": "Organigramm, Hierarchie"
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

**OSPUI-Integration (Zukunft):**
```
User: "Zeige mir das Firmenlogo"
RAG-Antwort: 

![Schneider Kabelsatzbau Logo](SharePoint-URL)

Verwendung: Geschäftspapiere, Website, Präsentationen
Quelle: KOM_CORE_Corporate_Identity.md (CH02)
```

---

## IMPLEMENTIERUNG (1 PHASE - EINFACH!)

### SHAREPOINT-LINKS EINFÜGEN (SOFORT UMSETZBAR)

**Workflow (5 Schritte):**

**Schritt 1: SharePoint-Ordner vorbereiten**
1. SharePoint öffnen: https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP
2. Ordner erstellen (falls nicht vorhanden):
   - `/Freigegebene Dokumente/Normen/`
   - `/Freigegebene Dokumente/Verträge/`
   - `/Freigegebene Dokumente/Richtlinien/`
   - `/Freigegebene Dokumente/Zertifikate/`
   - `/Freigegebene Dokumente/Formulare/`
   - `/Freigegebene Dokumente/Handbücher/`
   - `/Freigegebene Dokumente/Policies/`
   - `/Freigegebene Dokumente/Gesetze/`
   - `/Dokumente/Icons_Bilder/` ✅ **BEREITS VORHANDEN!**

3. PDFs & Bilder hochladen (richtiger Ordner)
4. Dateinamen prüfen (keine Leerzeichen, keine Umlaute)

**Schritt 2: SharePoint-Links kopieren**

**Methode 1 (Permanenter Link):**
1. Rechtsklick auf PDF/Bild → "Link teilen"
2. "Personen in Ihrer Organisation mit dem Link können anzeigen" → "Kopieren"

**Methode 2 (Direkter Link - EMPFOHLEN):**
1. PDF/Bild in SharePoint öffnen
2. Browser-Adresszeile kopieren
3. Link sieht aus wie: `https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Logo_schneider.png`

**Schritt 3: Markdown-Datei erweitern**

**Für PDFs (LINK-LISTE):**
1. Markdown-Datei öffnen (z.B. IT_DS_Datenschutz.md)
2. Vor "## QUERVERWEISE" einfügen:
   ```markdown
   ---
   
   ## ORIGINAL-DOKUMENTE
   
   **Verträge (SharePoint):**
   - [AVV Terra Cloud](URL-hier-einfügen) - Kurzbeschreibung
   
   ---
   ```

**Für Bilder (INLINE):**
1. Markdown-Datei öffnen (z.B. KOM_CORE_Corporate_Identity.md)
2. Nach "## ORIGINAL-DOKUMENTE" einfügen:
   ```markdown
   ---
   
   ## GRAFIKEN & DIAGRAMME
   
   **Firmenlogo:**
   ![Schneider Logo](URL-hier-einfügen)
   
   ---
   ```

3. URLs einfügen
4. Speichern

**Schritt 4: Testen**
1. Link im Browser öffnen
2. PDF/Bild sollte in SharePoint öffnen
3. Inline-Bild sollte in Markdown-Renderer angezeigt werden

**Schritt 5: ChromaDB-Import aktualisieren**
1. Metadata aus Markdown parsen (Python-Script)
2. pdf_originals & image_assets in Metadata einfügen

---

## BETROFFENE MODULE & PRIORITÄT

### PDF-LINKING - PRIORITÄT 1-3 (v2.1)

*(Wie in v2.1 definiert - siehe unten)*

---

### BILDER-LINKING - PRIORITÄT (NEU v2.2)

**PRIORITÄT 1 - SOFORT (2 Module, ~20 min):**

| Modul | Dateien | Bilder | Use Case | Aufwand |
|-------|---------|--------|----------|---------|
| **KOM_CORE** | KOM_CORE_Corporate_Identity.md | 3 Logos (Schneider, OSP, SAS) | Firmenlogos, CI | 10 min |
| **ORG_ORGA** | ORG_ORGA_Unternehmensstruktur.md | 1 Organigramm | Unternehmensstruktur | 10 min |

**Gesamt:** ~20 Minuten für Priorität 1 (BILDER)

---

**PRIORITÄT 2 - KURZFRISTIG (3 Module, ~30 min):**

| Modul | Dateien | Bilder | Use Case | Aufwand |
|-------|---------|--------|----------|---------|
| **QM_CORE** | QM_CORE_Qualitaetspolitik.md | 2 Prozess-Workflows | QM-Prozesse | 10 min |
| **AV_CORE** | AV_CORE_Arbeitsvorbereitung.md | 2 Workflow-Diagramme | AV-Prozesse | 10 min |
| **TM_CORE** | TM_CORE_Maschinen_Anlagen.md | 1-2 Maschinenlayouts | Fertigungslayouts | 10 min |

**Gesamt:** ~30 Minuten für Priorität 2 (BILDER)

---

**PRIORITÄT 3 - OPTIONAL (2 Module, ~20 min):**

| Modul | Dateien | Bilder | Use Case | Aufwand |
|-------|---------|--------|----------|---------|
| **IT_CORE** | IT_CORE_Client-Server-Struktur.md | 1 Netzwerk-Topologie | IT-Infrastruktur | 10 min |
| **KST_PF** | KST_PF_Prueffeld.md | 1 Prüffeld-Layout | Kostenstellen-Layout | 10 min |

**Gesamt:** ~20 Minuten für Priorität 3 (BILDER)

---

**GESAMTAUFWAND BILDER:** ~1,5 Stunden für alle 7 Module

---

### PDF-LINKING - PRIORITÄT 1 - SOFORT (5 Module)

| Modul | Dateien | PDFs | Aufwand |
|-------|---------|------|---------|
| **IT_DS** | IT_DS_Datenschutz.md | 10-12 (AVVs, DSGVO, ISO 9001) | 30 min |
| **QM_CORE** | QM_CORE_Qualitaetspolitik.md | 5-7 (Zertifikate, Policies, Formulare) | 20 min |
| **CMS_MC** | CMS_MC_Material_Compliance.md | 8-10 (RoHS, REACH, IMDS) | 25 min |
| **TM_CORE** | TM_CORE_Maschinen_Anlagen.md | 6-8 (Maschinen-Handbücher) | 20 min |
| **ORG_LEIT** | ORG_LEIT_Leitbild_Vision.md | 2-3 (Leitbild, Vision) | 10 min |

**Gesamt:** ~2 Stunden für Priorität 1 (PDFs)

---

### PDF-LINKING - PRIORITÄT 2 - KURZFRISTIG (6 Module)

| Modul | Dateien | PDFs | Aufwand |
|-------|---------|------|---------|
| **HR_CORE** | HR_CORE_Personalstamm.md | 4-6 (Arbeitsverträge, BV) | 15 min |
| **AV_CORE** | AV_CORE_Arbeitsvorbereitung.md | 3-5 (Standards, Richtlinien) | 15 min |
| **VT_CORE** | VT_CORE_Vertrieb_Auftragsabwicklung.md | 2-4 (Vertriebsrichtlinien) | 10 min |
| **EK_SEK** | EK_SEK_Strategischer_Einkauf.md | 3-5 (Rahmenverträge, Policies) | 15 min |
| **PM_CORE** | PM_CORE_Aktuelle_Projekte.md | 2-3 (Projekthandbücher) | 10 min |
| **GF_STR** | GF_STR_Strategische_Ausrichtung.md | 2-3 (Strategiepapiere) | 10 min |

**Gesamt:** ~1,5 Stunden für Priorität 2 (PDFs)

---

### PDF-LINKING - PRIORITÄT 3 - OPTIONAL (5 Module)

| Modul | Dateien | PDFs | Aufwand |
|-------|---------|------|---------|
| **RES_NORM** | RES_NORM_Normen_Standards.md | 10+ (Alle Normen) | 30 min |
| **KST_PF** | KST_PF_Prueffeld.md | 3-5 (Prüfrichtlinien) | 15 min |
| **DMS_ARI** | DMS_ARI_Anweisungen_Richtlinien.md | 5-7 (DMS-Policies) | 20 min |
| **KOM_CORE** | KOM_CORE_Corporate_Identity.md | 2-3 (CI-Guideline) | 10 min |
| **BN_CORE** | BN_CORE_Identitaet.md | 1-2 (Berechtigungskonzept) | 5 min |

**Gesamt:** ~1,5 Stunden für Priorität 3 (PDFs)

---

**GESAMTAUFWAND PDFs:** ~5 Stunden für alle 16 Module  
**GESAMTAUFWAND BILDER:** ~1,5 Stunden für 7 Module  
**GESAMTAUFWAND GESAMT:** ~6,5 Stunden

---

## BEST PRACTICES

### 1. PDF-DATEINAMEN-KONVENTION

**Format:** `Kategorie_Bezeichnung_Version.pdf`

**Beispiele:**
- ✅ `ISO_9001_2015.pdf`
- ✅ `AVV_Terra_Cloud_2025.pdf`
- ✅ `Komax_Alpha_550_Manual_v3.2.pdf`
- ❌ `ISO 9001 (2015).pdf` (Leerzeichen, Sonderzeichen)
- ❌ `avv terra cloud.pdf` (Kleinbuchstaben, Leerzeichen)

**Regeln:**
- Keine Leerzeichen (verwende `_`)
- Keine Umlaute (ä→ae, ö→oe, ü→ue, ß→ss)
- Keine Sonderzeichen außer `_` und `-`
- CamelCase oder snake_case
- Version optional am Ende (`_vX.Y` oder `_YYYY`)

---

### 2. BILD-DATEINAMEN-KONVENTION (NEU v2.2)

**Format:** `Typ_Bezeichnung_Version.ext`

**Beispiele:**
- ✅ `Logo_schneider.png`
- ✅ `Organigramm_2025.png`
- ✅ `Layout_Fertigung_KST1000.pdf`
- ✅ `Workflow_AV_Prozess.svg`
- ❌ `logo schneider.png` (Leerzeichen, Kleinbuchstaben)
- ❌ `Organigramm (alt).png` (Sonderzeichen)

**Dateitypen:**
- Logos: `.png` (transparent) oder `.svg` (vektorisiert)
- Diagramme: `.png` oder `.svg`
- Fotos: `.jpg` (komprimiert)
- Technische Zeichnungen: `.pdf` (hochauflösend)

---

### 3. LINK-WARTUNG

**Regelmäßige Checks:**
- Quartalsweise: Broken-Link-Check (Python-Script)
- Nach SharePoint-Umstrukturierung: Alle Links validieren
- Nach PDF-Upload: Link sofort testen

**Python-Script (Broken-Link-Checker):**
```python
import requests
import re

def validate_pdf_links(markdown_file):
    """Validiert alle PDF-Links in Markdown-Datei"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Finde alle Links (PDFs + Bilder)
    links = re.findall(r'\((https://.*?\.(?:pdf|png|jpg|svg|jpeg).*?)\)', content)
    
    for link in links:
        try:
            response = requests.head(link, timeout=5)
            if response.status_code == 200:
                print(f"✅ OK: {link}")
            else:
                print(f"❌ BROKEN: {link} (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ ERROR: {link} ({e})")

# Verwendung
validate_pdf_links("KOM_CORE_Corporate_Identity.md")
```

---

### 4. CHROMADB-IMPORT ERWEITERN

**Python-Beispiel (PDF + Bilder aus Markdown extrahieren):**
```python
import re

def extract_pdf_originals(markdown_content):
    """Extrahiert PDF-Links aus Markdown-Abschnitt ORIGINAL-DOKUMENTE"""
    
    originals = []
    
    # Finde Abschnitt "## ORIGINAL-DOKUMENTE"
    original_section = re.search(
        r'## ORIGINAL-DOKUMENTE.*?(?=##|\Z)', 
        markdown_content, 
        re.DOTALL
    )
    
    if original_section:
        # Finde alle Links im Format [Title](URL)
        links = re.findall(
            r'\[(.*?)\]\((https://.*?\.pdf)\)\s*-\s*(.*?)(?:\n|$)', 
            original_section.group()
        )
        
        for title, url, description in links:
            # Kategorie aus URL extrahieren
            category_match = re.search(r'Dokumente/([^/]+)/', url)
            category = category_match.group(1) if category_match else "Sonstiges"
            
            # Typ bestimmen
            if "Verträge" in category or "AVV" in title:
                doc_type = "vertrag"
            elif "Normen" in category or "ISO" in title or "IPC" in title:
                doc_type = "norm"
            elif "Richtlinien" in category:
                doc_type = "richtlinie"
            elif "Zertifikate" in category:
                doc_type = "zertifikat"
            elif "Gesetze" in category:
                doc_type = "gesetz"
            else:
                doc_type = "sonstiges"
            
            originals.append({
                "title": title.strip(),
                "url": url.strip(),
                "description": description.strip(),
                "type": doc_type,
                "category": category
            })
    
    return originals

def extract_image_assets(markdown_content):
    """Extrahiert Bilder aus Markdown-Abschnitt GRAFIKEN & DIAGRAMME"""
    
    images = []
    
    # Finde Abschnitt "## GRAFIKEN & DIAGRAMME"
    image_section = re.search(
        r'## GRAFIKEN & DIAGRAMME.*?(?=##|\Z)', 
        markdown_content, 
        re.DOTALL
    )
    
    if image_section:
        # Finde alle Inline-Bilder im Format ![Alt](URL)
        links = re.findall(
            r'!\[(.*?)\]\((https://.*?\.(?:png|jpg|svg|jpeg))\)', 
            image_section.group()
        )
        
        for alt_text, url in links:
            # Typ bestimmen
            if "Logo" in alt_text or "logo" in url.lower():
                img_type = "logo"
            elif "Organigramm" in alt_text or "organigramm" in url.lower():
                img_type = "diagram"
            elif "Layout" in alt_text or "layout" in url.lower():
                img_type = "layout"
            elif "Workflow" in alt_text or "workflow" in url.lower():
                img_type = "flowchart"
            else:
                img_type = "other"
            
            # Kategorie aus URL
            if "Icons_Bilder" in url:
                category = "corporate_identity"
            else:
                category = "technical"
            
            images.append({
                "type": img_type,
                "alt_text": alt_text.strip(),
                "url": url.strip(),
                "category": category,
                "usage": ""  # Optional manuell ergänzen
            })
    
    return images

# Bei ChromaDB-Import
markdown_content = read_markdown_file("KOM_CORE_Corporate_Identity.md")
pdf_originals = extract_pdf_originals(markdown_content)
image_assets = extract_image_assets(markdown_content)

metadata = {
    "source": "KOM_CORE_Corporate_Identity.md",
    "tag": "KOM",
    "sub_tag": "CORE",
    "pdf_originals": pdf_originals,   # PDFs
    "image_assets": image_assets,      # 🆕 Bilder
    # ... andere Metadata
}

collection.add(
    documents=[chunk_text],
    metadatas=[metadata],
    ids=[chunk_id]
)
```

---

## MARKDOWN-TEMPLATE

**Quick-Start Template (Copy & Paste):**

```markdown
---

## ORIGINAL-DOKUMENTE

**Verträge (SharePoint):**
- [Dokumentname](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/DATEI.pdf) - Kurzbeschreibung

**Richtlinien (SharePoint):**
- [Dokumentname](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Richtlinien/DATEI.pdf) - Kurzbeschreibung

**Normen (SharePoint):**
- [Dokumentname](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Normen/DATEI.pdf) - Kurzbeschreibung

---

## GRAFIKEN & DIAGRAMME

**[Kategorie-Name]:**
![Alt-Text Beschreibung](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/DATEI.png)
*Verwendung: [Beschreibung]*

---
```

**Kategorien PDFs:**
- Verträge
- Richtlinien
- Normen
- Zertifikate
- Formulare
- Handbücher
- Policies
- Gesetze

**Kategorien Bilder (NEU):**
- Firmenlogos
- Organigramme
- Prozessdiagramme
- Maschinenlayouts
- Workflow-Diagramme
- Netzwerk-Topologien
- Zertifikate (visuell)

---

## BATCH-PROCESSING-INTEGRATION

**Erweiterte Batch-Protokolle (Stage 1 → Stage 2):**

```markdown
### PHASE 7: PDF-LINKING

**Original-Dokumente verlinkt:**
- 3 Verträge (AVV Terra Cloud, Gromnitza, INWX)
- 2 Richtlinien (Datenschutz, IT-Sicherheit)
- 2 Normen (ISO 9001:2015, DSGVO)
- 1 Zertifikat (ISO 9001 Zertifikat)

**Metadata erweitert:**
- pdf_originals: 8 Dokumente
- Kategorien: Verträge (3), Richtlinien (2), Normen (2), Zertifikate (1)

**Aufwand:** 15 Minuten
**Status:** ✅ Phase 7 abgeschlossen

---

### 🆕 PHASE 8: BILDER-INTEGRATION (NEU v2.2)

**Grafiken & Diagramme integriert:**
- 2 Firmenlogos (Schneider, OSP)
- 1 Organigramm (Unternehmensstruktur 2025)

**Metadata erweitert:**
- image_assets: 3 Bilder
- Typen: Logos (2), Diagramme (1)

**Aufwand:** 10 Minuten
**Status:** ✅ Phase 8 abgeschlossen
```

---

## NÄCHSTE SCHRITTE

### SOFORT (KW 49/2025)

1. ⏳ **PDFs hochladen:** Priorität 1 Module (IT_DS, QM_CORE, CMS_MC, TM_CORE, ORG_LEIT)
2. ⏳ **IT_DS_Datenschutz.md:** Abschnitt "ORIGINAL-DOKUMENTE" einfügen (10-12 PDFs)
3. ⏳ **QM_CORE_Qualitaetspolitik.md:** Abschnitt einfügen (5-7 PDFs)
4. 🆕 **KOM_CORE_Corporate_Identity.md:** Abschnitt "GRAFIKEN & DIAGRAMME" einfügen (3 Logos)
5. 🆕 **ORG_ORGA_Unternehmensstruktur.md:** Organigramm einbinden (1 Bild)

### Kurzfristig (Dez 2025)

6. ⏳ **Priorität 1 komplett:** Alle 5 Module mit PDF-Links (CMS, TM, ORG)
7. ⏳ **Priorität 2 starten:** HR, AV, VT, EK, PM, GF (6 Module)
8. ⏳ **Link-Validierung:** Python-Script testen
9. 🆕 **Bilder-Integration Priorität 2:** QM, AV, TM (3 Module)

### Mittelfristig (Q1 2026)

10. ⏳ **Priorität 3:** RES, KST, DMS, KOM, BN (5 Module)
11. ⏳ **ChromaDB-Import:** Python-Script erweitern (pdf_originals + image_assets)
12. ⏳ **OSPUI-Integration:** PDF-Links & Bilder im Chat anzeigen
13. ⏳ **Quartalsweise Link-Validierung:** Broken-Link-Check automatisieren

---

## QUERVERWEISE

**Ausgehend (→):**
- → `IT_DOKU_IT-Dokumentation.md` - ChromaDB-Konfiguration, Import-Workflow
- → `IT_OSP_KI-Chatbot.md` - OSPUI-Konfiguration, RAG-Einstellungen
- → `OSP_TAG_System.md` - TAG-System, Cluster-Struktur
- → `OSP_Regeln.md` - Governance, Versionierung, Querverweise
- → `KOM_CORE_Corporate_Identity.md` - Firmenlogos, CI-Guideline
- → `ORG_ORGA_Unternehmensstruktur.md` - Organigramm

**Extern:**
- SharePoint OSP: https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP
- Icons_Bilder Ordner: https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder

---

## ÄNDERUNGSHISTORIE

### [2.2] - 2025-11-29 - BILDER-INTEGRATION (INLINE)

**Änderungen:**
- ✅ **Bilder-Linking-Strategie hinzugefügt** - INLINE-Bilder (Option A)
- ✅ **SharePoint-Ordnerstruktur erweitert:** Icons_Bilder/ dokumentiert
- ✅ **ChromaDB-Metadata erweitert:** image_assets Feld mit Alt-Text, URL, Typ, Kategorie
- ✅ **Markdown-Template erweitert:** Abschnitt "## GRAFIKEN & DIAGRAMME"
- ✅ **Betroffene Module dokumentiert:** 7 Module (3 Prioritätslevels)
- ✅ **Python-Scripts erweitert:** extract_image_assets() Funktion
- ✅ **Best Practices:** Bild-Dateinamen-Konvention
- ✅ **Aufwandsschätzung:** ~1,5 Stunden für alle Bilder
- ✅ **Batch-Processing:** Phase 8 "Bilder-Integration" definiert

**Use Cases:**
- Corporate Identity: Firmenlogos (KOM_CORE)
- Organisation: Organigramme (ORG_ORGA)
- Qualität: Prozess-Workflows (QM_CORE)
- Technik: Maschinenlayouts (TM_CORE, KST_PF)
- Arbeitsvorbereitung: Workflow-Diagramme (AV_CORE)

**Motivation:** User-Request - Firmenlogos & Organigramme verlinken

**Umfang:** +30% Funktionalität (Bilder zusätzlich zu PDFs)

**Verantwortlich:** AL (Andreas Löhr)

---

### [2.1] - 2025-11-29 - VEREINFACHUNG (NUR SHAREPOINT-LINKS)

**Änderungen:**
- ❌ **Deep-Links ENTFERNT** (Phase 2) - zu aufwändig, manuell nicht praktikabel
- ✅ **Fokus auf SharePoint-Links** (Phase 1) - einfach, schnell, trotzdem wertvoll
- ✅ **Priorisierung:** 3 Prioritätslevels (Sofort, Kurzfristig, Optional)
- ✅ **Aufwandsschätzung:** ~5 Stunden für alle 16 Module
- ✅ **Tools vereinfacht:** Nur Link-Validierung (kein PDFtk, PyPDF2 mehr nötig)
- ✅ **Metadata vereinfacht:** Nur pdf_originals (kein pdf_deeplinks)

**Motivation:** User-Feedback - Deep-Links zu aufwändig, nicht manuell durchführbar

**Umfang:** -50% Komplexität, +100% Umsetzbarkeit

**Verantwortlich:** AL

---

### [2.0] - 2025-11-29 - PDF-LINKING-STRATEGIE

**Neue Inhalte:**
- SharePoint-Links zu Original-PDFs
- Deep-Links in umfangreiche PDFs (ENTFERNT in v2.1)
- ChromaDB-Metadata-Schema erweitert
- 3-Phasen-Implementierung (REDUZIERT auf 1 Phase in v2.1)

**Motivation:** User-Request - Original-PDFs verlinken für bessere RAG-Nutzbarkeit

**Verantwortlich:** AL

---

### [1.0] - 2025-11-23 - ERSTVERSION

**Inhalte:**
- RAG-Optimierungs-Workflow (Stage 1 → Stage 2)
- YAML-Header-Schema
- Metadata-Schema (ChromaDB)
- Batch-Processing-Protokolle

**Verantwortlich:** AL

---

## RAG-METADATA

**Primary Keywords:** RAG, ChromaDB, Metadata, PDF-Linking, SharePoint, Original-Dokumente, Verträge, AVV, Richtlinien, Normen, Zertifikate, Handbücher, Batch-Processing, Stage 2, OSPUI, YAML, Bilder-Integration, Logos, Organigramme, Inline-Bilder, Corporate Identity

**Secondary Keywords:** ISO 9001, IPC-WHMA-A-620, DSGVO, Link-Validierung, Broken-Link, Permanente Links, pdf_originals, image_assets, Dateinamen-Konvention, Komax, Schunk, Timeline, DocuWare, Alt-Text, SVG, PNG, Workflow-Diagramme

**User-Level:** L3-L4 (Führung + IT/KI-Manager)

**Chunk-Anzahl:** ~12 Chunks  
**Test-Queries:**
1. "Wie verlinke ich Original-PDFs in Markdown?" → Abschnitt 2
2. "Wie binde ich Firmenlogos inline ein?" → Abschnitt 3 (NEU v2.2)
3. "Welche Metadata-Felder für PDF-Links?" → Abschnitt 4
4. "Welche Metadata-Felder für Bilder?" → Abschnitt 4 (NEU v2.2)
5. "Wie validiere ich Broken Links?" → Abschnitt 8.3
6. "Welche Module brauchen PDF-Links?" → Abschnitt 6 (Prioritäten)
7. "Welche Module brauchen Bilder?" → Abschnitt 6 (NEU v2.2)
8. "Wie lange dauert PDF-Linking für alle Module?" → Abschnitt 6 (~5 Stunden)
9. "Wie extrahiere ich Bilder aus Markdown?" → Abschnitt 8.4 (NEU v2.2)
10. "Zeige mir Beispiel für Organigramm-Einbindung" → Abschnitt 3

---

**Status:** ✅ AKTIV - Bereit für Implementierung (EINFACH!)  
**Kritikalität:** MITTEL (verbessert RAG-Nutzbarkeit erheblich)  
**Aufwand PDFs:** ~5 Stunden für alle 16 Module  
**Aufwand Bilder:** ~1,5 Stunden für 7 Module  
**Aufwand Gesamt:** ~6,5 Stunden  
**Nächste Review:** Nach Priorität 1 Ausrollung (Dez 2025)

---

*Diese Richtlinie definiert SharePoint-PDF-Linking-Strategien & Bilder-Integration für RAG-optimierte Markdown-Dokumente. Original-PDFs werden über einfache SharePoint-Links referenziert, Bilder inline gerendert - KEINE Deep-Links, KEIN manuelles Seitenzahlen-Ermitteln. Fokus auf schnelle, pragmatische Umsetzung.*

[OSP]
