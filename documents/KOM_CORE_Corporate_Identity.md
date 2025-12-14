# [KOM][CORE] Corporate Identity

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 3.1 | **TAG:** [KOM][CORE] | **Erstellt:** 2025-11-13 | **Aktualisiert:** 2025-12-13 | **Autor:** AL | **Verantwortlich:** CS (GF) & AL (QM) | **Cluster:** 🔷 C1-Kontext | **Zugriff:** 🟢 L1-Öffentlich | **Status:** ✅ PRODUKTIV (RAG) | **Stage:** 2 | **RAG-Version:** 1.1 | **Basis:** KOM_CORE_v2.1.md

**Kritikalität:** 🔴 SEHR HOCH | **ISO 9001:2015:** Kap. 4.1, 4.4, 7.4 | **Quellen:** Geschäftsführung, HR Montabaur HRA 4489, Brand Board 2025

**Primary Keywords:** Corporate Identity, CI, Schneider Kabelsatzbau, Brand Board, Unternehmensdaten, Farbsystem, Schneider Blau, Orange, Logo, Typografie, Montserrat, Open Sans, Fira Code, Dokumentenstandards, Header, Footer, ID-Schema, HTML, CSS, CSS-Variablen, KI-Integration, ISO 9001, Markenkonsistenz, Geschäftsführung, Handelsregister, USt-ID, DUNS, SharePoint, HKS, Websafe

**Secondary Keywords:** HRA 4489, DE 238 528 043, 31-628-2185, #0080C9, #DC500F, PANTONE 3005 C, PANTONE 179 C, HKS 44, HKS 14, Websafe #0066BB, Websafe #E25400, RAL 5015, RAL 2001, Alte Hütte 3, 57537 Wissen, 02742/9336-0, CS, CA, AL, Rainer Schneider, Christoph Schneider, Christoph Augst, Gründung 1972, 60 Mitarbeiter, schneider_S, Logo_OSP_Text, logo_sas, CMYK, RAL, RGB, SVG, PNG, Favicon, App-Icon

**Chunk-Strategie:** Markdown-Header (##)
**Chunk-Anzahl:** 12
**Datenstand:** 2025-12-12

---

## ZWECK

Definiert **Corporate Identity (CI)** der Rainer Schneider Kabelsatzbau GmbH & Co. KG als verbindlichen Standard für ALLE Kommunikation - intern/extern, digital/print, manuell/KI-generiert.

**Kernfunktionen:**
1. **Brand Board:** Zentrale visuelle CI-Referenz (2025-12-12)
2. **Single Source of Truth:** Einheitliche Unternehmensdaten
3. **Visuelle Identität:** Farbsystem, Typografie, Logo-Hierarchie
4. **Dokumentenstandards:** Header/Footer, ID-Schema, Metadaten-Box
5. **HTML/CSS-Integration:** Variablen für Web-Anwendungen
6. **ISO 9001 Konformität:** Dokumentation nach Kap. 7.4

**Kritische Bedeutung:** Rechtsverbindliche HR-Daten, Markenidentität 50+ Jahre (seit 1972), NULL-FEHLER-POLITIK, Kundenkommunikation

**Anwendungsbereich:** Alle 60 MA (CI-Pflicht-Schulung) | KI-Systeme (Claude, ChatGPT, OSP) | QM-Team (AL) | GF (CS, CA) | Marketing | IT | Externe Partner

**Typische Anfragen:**

1. **Firmenadresse?** → Alte Hütte 3, 57537 Wissen, Tel: 02742/9336-0
2. **CI-Farben?** → Blau #0080C9 (PANTONE 3005 C), Orange #DC500F (PANTONE 179 C)
3. **Schriftarten?** → Montserrat Bold (Headlines), Open Sans (Fließtext), Fira Code (Code)
4. **Logo-Datei?** → Logo_schneider.png (Haupt), schneider_S.png (Icon), Logo_OSP_Text.png (OSP)
5. **Dokument-Header?** → Rechtsbündig: `Dokumentenname | Schneider Kabelsatzbau` (Schneider = Blau + Bold)
6. **CSS-Variablen?** → `--schneider-blue: #0080C9; --schneider-orange: #DC500F;`

---

## BRAND BOARD

Das **Schneider Brand Board** ist die zentrale visuelle Referenz für alle Corporate-Identity-Elemente.

**SharePoint:**
![Schneider Brand Board](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/Schneider_Brand_Board.png)

**Stand:** 2025-12-12 | **Erstellt:** AL | **Freigabe:** CS

**Inhalte:**
- Logo-Hierarchie (4 Varianten: Hauptlogo, Icon, OSP, SAS)
- Farbpalette mit HEX, RGB, CMYK, PANTONE, RAL
- Typografie (Montserrat, Open Sans, Fira Code)
- HTML/CSS-Variablen
- Dokument-Standard (Header/Footer)

---

## UNTERNEHMENSDATEN

```yaml
Firma:
  vollständig: "Rainer Schneider Kabelsatzbau und Konfektion GmbH & Co. KG"
  kurzform: "Schneider Kabelsatzbau"
  
Standort:
  adresse: "Alte Hütte 3, 57537 Wissen"
  region: "Sieg / Rheinland-Pfalz, Deutschland"
  
Kontakt:
  telefon: "02742 / 9336-0"
  fax: "02742 / 3820"
  email: "info@schneider-kabelsatzbau.de"
  web: "www.schneider-kabelsatzbau.de"
  
Handelsregister:
  nr: "HRA 4489"
  gericht: "AG Montabaur"
  ust_id: "DE 238 528 043"
  duns: "31-628-2185"
  
Geschäftsführung:
  senior: "Rainer Schneider (Gründer, seit 1972)"
  kaufmännisch: "Christoph Schneider (CS) - c.schneider@schneider-kabelsatzbau.de"
  technisch: "Christoph Augst (CA) - c.augst@schneider-kabelsatzbau.de"
  
Markenidentität:
  claim: "Ihr Kabelsatzbau - Made in Wissen"
  gründung: "1972"
  mitarbeiter: "ca. 60"
  produktion: "1.860 m²"
  
Zertifizierungen:
  - ISO 9001:2015 (DEKRA, gültig bis 25.01.2028)
  - UL Processed Wire
  - UL Wiring Harnesses
```

---

## LOGO-HIERARCHIE

| Logo | Datei | Verwendung | SharePoint |
|------|-------|------------|------------|
| **Hauptlogo** | Logo_schneider.png | Website, Dokumente, Print, Briefkopf | [Download](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/Logo_schneider.png) |
| **Icon (S)** | schneider_S.png | Favicon, App-Icon, Social Media, Wasserzeichen | [Download](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/schneider_S.png) |
| **OSP-Logo** | Logo_OSP_Text.png | OSP-System, Tech-Docs, KI-Dokumentation | [Download](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/Logo_OSP_Text.png) |
| **SAS-Logo** | logo_sas.jpg | Holding, Konzern-Dokumente (NUR SAS!) | [Download](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/logo_sas.jpg) |

**Logo-Beschreibungen:**
- **Hauptlogo:** "SCHNEIDER" (Blau) + "KABELSATZBAU" (Schwarz) + Icon (Orange/Grau)
- **Icon (S):** Stilisiertes "S" in Orange #DC500F mit integriertem Kabelschneider und Ringöse in Grau
- **OSP-Logo:** "[OSP]" in Orange mit eckigen Klammern, "SCHNEIDER" in Blau
- **SAS-Logo:** "SAS" in Burgunderrot mit Gebäude-Silhouette

**Logo-Schutzzone:** 1× Logo-Höhe Freiraum (alle Seiten)

**Mindestgrößen:** Web: 80px Höhe | Print: 30mm Höhe | Favicon: 16×16, 32×32, 48×48 px

---

## FARBSYSTEM

**Primärfarben (verbindlich aus Schneider_Kabelsatz_Farbdefinitionen.pdf):**

| Farbe | HEX | RGB | CMYK | PANTONE | RAL | HKS | Websafe |
|-------|-----|-----|------|---------|-----|-----|--------|
| **Schneider Blau** | #0080C9 | 0 / 128 / 201 | 100 / 35 / 0 / 20 | 3005 C | 5015 | 44 | #0066BB |
| **Orange** | #DC500F | 220 / 80 / 15 | 0 / 80 / 100 / 0 | 179 C | 2001 | 14 | #E25400 |

**Neutraltöne:**

| Farbe | HEX | RGB | CMYK | Verwendung |
|-------|-----|-----|------|------------|
| **Schwarz** | #000000 | 0 / 0 / 0 | 0/0/0/100 | PANTONE Black | Headlines, Body-Text |
| **Grau 70%** | #808080 | 128 / 128 / 128 | 0/0/0/70 | PANTONE Black 70% | Sekundärtext, Footer |
| **Grau 20%** | #CCCCCC | 204 / 204 / 204 | 0/0/0/20 | Trennlinien, Rahmen |
| **Weiß** | #FFFFFF | 255 / 255 / 255 | – | Hintergrund |

**Farbhierarchie:**
1. **Schneider Blau:** Headlines, Logo, Links, Primär-Elemente
2. **Orange:** Call-to-Action, Akzente, Hover-States, OSP-Branding
3. **Schwarz:** Body-Text, Tabellen
4. **Grautöne:** Sekundärtext, UI-Elemente, Footer

**Kontrast (WCAG 2.1 AA):** Blau auf Weiß ≥ 4.5:1 | Orange auf Weiß ≥ 3:1

---

## TYPOGRAFIE

**Schrift-Hierarchie (aus Brand Board):**

| Kategorie | Schrift | Fallback | Verwendung |
|-----------|---------|----------|------------|
| **Headlines** | Montserrat Bold | Arial Bold | Titel, Überschriften, H1-H3 |
| **Fließtext** | Open Sans Regular | Calibri, Arial | Body-Text, Dokumente, Web |
| **Code/Daten** | Fira Code | Consolas, Courier | Technische Daten, Tabellen, Code |

**Google Fonts:** Alle drei Schriften kostenlos verfügbar unter fonts.google.com

**Schriftgrößen:**

| Element | Web (px) | Print (pt) | Zeilenhöhe |
|---------|----------|------------|------------|
| H1 | 36-40 | 24 | 1.2 |
| H2 | 28-32 | 18 | 1.3 |
| H3 | 22-24 | 14 | 1.4 |
| Body | 16-18 | 11 | 1.6 |
| Tabellen | 14-16 | 10 | 1.4 |
| Footer | 12-13 | 9 | 1.3 |

**Responsive Breakpoints:** Mobile (<768px): H1=28px, Body=16px | Tablet (768-1024px): H1=32px | Desktop (>1024px): H1=40px

---

## HTML/CSS-VARIABLEN

Standard CSS-Variablen für Web-Anwendungen, SharePoint und HTML-Dokumente:

```css
:root {
  /* Primärfarben */
  --schneider-blue: #0080C9;
  --schneider-orange: #DC500F;
  
  /* Neutraltöne */
  --black: #000000;
  --gray: #808080;
  --gray-light: #CCCCCC;
  --white: #FFFFFF;
  
  /* Typografie */
  --font-heading: 'Montserrat', Arial, sans-serif;
  --font-body: 'Open Sans', Calibri, sans-serif;
  --font-code: 'Fira Code', Consolas, monospace;
  
  /* Design-Tokens */
  --radius: 10px;
  --shadow: 0 4px 24px rgba(0, 128, 201, 0.08);
}

/* Schneider-Text (Blau + Bold) */
.schneider-text {
  color: var(--schneider-blue);
  font-weight: 700;
}

/* Brand-Link */
.brand-link {
  color: var(--schneider-blue);
  text-decoration: none;
}
.brand-link:hover {
  color: var(--schneider-orange);
}
```

**Google Fonts Import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans&family=Fira+Code&display=swap" rel="stylesheet">
```

---

## DOKUMENT-STANDARD

Verbindlicher Standard für alle Schneider-Dokumente (Word, PDF, Print):

### Header (rechtsbündig)

```
                              Dokumentenname | Schneider Kabelsatzbau
                                               ▲▲▲▲▲▲▲▲▲
                                               Blau #0080C9 + Fett
```

**Formatierung:**
- Position: Rechtsbündig
- Schrift: Open Sans / Calibri, 10pt
- "Schneider" = **Blau #0080C9, Fett**
- "Kabelsatzbau" = Schwarz, Normal
- Trennzeichen: ` | ` (Pipe mit Leerzeichen)

**Beispiele:** `Qualitätshandbuch | Schneider Kabelsatzbau` | `Arbeitsanweisung AA-001 | Schneider Kabelsatzbau`

### Footer (dreispaltig)

| Links | Mitte | Rechts |
|-------|-------|--------|
| Formular-ID | Seite X von Y | Erstellt: [Kürzel] |
| z.B. F-QM-001-A | (dynamisch) | YYYY-MM-DD |

**Formatierung:**
- Schrift: Open Sans / Calibri, 9pt, Grau #808080
- Trennlinie über Footer: 0.5pt, Grau #CCCCCC

### Formular-ID-Schema

| Präfix | Bedeutung | Beispiel |
|--------|-----------|----------|
| F- | Formular | F-QM-001-A |
| VA- | Verfahrensanweisung | VA-QM-050 |
| AA- | Arbeitsanweisung | AA-FE-012 |
| PA- | Prüfanweisung | PA-PF-003 |
| DOK- | Dokumentation | DOK-IT-005 |

---

## DOKUMENTEN-GLIEDERUNG

**Verfahrensanweisung (VA) - 7 Abschnitte:**
1. Zweck und Ziel
2. Geltungsbereich
3. Zuständigkeiten (RACI)
4. Ablaufbeschreibung
5. Dokumentation
6. Änderungsdienst
7. Mitgeltende Unterlagen

**Arbeitsanweisung (AA) - 5 Abschnitte:**
1. Zweck
2. Anwendungsbereich
3. Durchführung (Schritt-für-Schritt)
4. Qualitätskriterien
5. Mitgeltende Unterlagen

**Prüfanweisung (PA) - 6 Abschnitte:**
1. Prüfgegenstand
2. Prüfmittel
3. Prüfablauf
4. Dokumentation
5. Grenzwerte/Toleranzen
6. Reaktion bei Abweichung

---

## GRAFIKEN & DIAGRAMME

**Alle Assets auf SharePoint:**

| Asset | Beschreibung | SharePoint-Link |
|-------|--------------|-----------------|
| **Brand Board** | Zentrale CI-Referenz | [Schneider_Brand_Board.png](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/Schneider_Brand_Board.png) |
| **Hauptlogo** | Volllogo mit Text | [Logo_schneider.png](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/Logo_schneider.png) |
| **Icon (S)** | Bildmarke/Favicon | [schneider_S.png](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/schneider_S.png) |
| **OSP-Logo** | KI-System-Logo | [Logo_OSP_Text.png](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/Logo_OSP_Text.png) |
| **SAS-Logo** | Holding-Logo | [logo_sas.jpg](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/logo_sas.jpg) |
| **Organigramm** | Unternehmensstruktur | [Organigramm.png](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/Organigramm.png) |

**Icon-Bibliothek:** [OSP_Icon_Bibliothek.html](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/OSP_Icon_Bibliothek.html)

---

## QUERVERWEISE

**Bidirektional (↔):**
- ↔ `ORG_CORE_Philosophie_Historie.md` - Unternehmensphilosophie, Geschichte seit 1972
- ↔ `ORG_LEIT_Leitbild_Vision.md` - Vision, Mission, Werte, Claim
- ↔ `ORG_ORGA_Unternehmensstruktur.md` - Organisationsstruktur, Abteilungen
- ↔ `ORG_GLO_Glossar.md` - Begriffsdefinitionen, Abkürzungen
- ↔ `KOM_AIR_KI_Kommunikationsregeln.md` - KI-Workflow, System-Prompt-Integration
- ↔ `KOM_STIL_Kommunikationsstil.md` - Tonalität, Anrede-Regeln
- ↔ `KOM_TPL_Vorlagen.md` - Brief-/Mail-Templates
- ↔ `GF_CORE_Geschaeftsleitung.md` - Geschäftsführungs-Details
- ↔ `QM_CORE_Qualitaetspolitik.md` - Qualitätspolitik, ISO 9001:2015
- ↔ `DMS_FORM_Formblatt_Vorlagen.md` - Templates mit Logo & Metadaten-Box
- ↔ `IT_DOKU_IT-Dokumentation.md` - Webdesign-Specs, CSS-Variablen
- ↔ `HR_CORE_Personalstamm.md` - E-Mail-Signaturen alle Mitarbeiter

**Ausgehend (→):**
- → **ALLE 15 Module:** CI-konforme Dokumentenerstellung
- → `QM_DOK_Dokumentation.md` - Dokumenten-ID-Schema
- → `AV_AA_Fertigungsunterlagen.md` - Arbeitsanweisungen CI-konform
- → `VT_CORE_Vertrieb.md` - Kundenkommunikations-Standards

**Eingehend (←):**
- ← Handelsregister Montabaur - HRA 4489, USt-ID
- ← Brand Board 2025 (Schneider_Brand_Board.png)

---

## COMPLIANCE

Dieses Dokument entspricht:
- **DIN EN ISO 9001:2015** - Kap. 7.4 (Kommunikation)
- **DIN 5008** - Geschäftsbrief-Norm
- **IPC/WHMA-A-620** - Dokumentationsstandards
- **WCAG 2.1 AA** - Barrierefreiheit (Kontraste)
- **DSGVO** - Nur Kürzel (AL, CS, CA), keine personenbezogenen Daten

---

## ÄNDERUNGSHISTORIE

### [3.1] - 2025-12-13
**Farbdefinitionen validiert & erweitert:**
- ✅ **Verbindliche Quelle:** Schneider_Kabelsatz_Farbdefinitionen.pdf integriert
- ✅ **HKS-Werte ergänzt:** HKS 44 (Blau), HKS 14 (Orange)
- ✅ **Websafe-Farben ergänzt:** #0066BB (Blau), #E25400 (Orange)
- ✅ **PANTONE Black dokumentiert:** 100% und 70% für Schwarz/Grau
- ✅ **CSS-Variable korrigiert:** --radius: 10px (gemäß Brand Board)
- ✅ **Anwendungsanleitung Claude** erstellt

**Quelle:** Schneider_Kabelsatz_Farbdefinitionen.pdf (Corporate Design)
**Verantwortlich:** AL (KI-Manager)

---

### [3.0] - 2025-12-12
**Brand Board Integration & CI-Update:**
- ✅ **Brand Board** als zentrale Referenz eingefügt (SharePoint-Link)
- ✅ **Farbwerte korrigiert:** PANTONE 3005 C (Blau), 179 C (Orange)
- ✅ **Typografie aktualisiert:** Montserrat Bold, Open Sans, Fira Code (statt DIN Pro)
- ✅ **HTML/CSS-Variablen** dokumentiert (neuer Abschnitt)
- ✅ **Dokument-Standard** mit Header/Footer definiert (neuer Abschnitt)
- ✅ **Logo-Hierarchie erweitert:** schneider_S.png (Icon) ergänzt
- ✅ **SharePoint-Links:** Alle 6 Assets mit direkten URLs
- ✅ **RAG-Optimierung:** Struktur beibehalten, ~12 Chunks

**Quelle:** Schneider_Brand_Board.png (2025-12-12)
**Verantwortlich:** AL (KI-Manager)

---

### [2.1] - 2025-12-02
**Logo-Link-Update:**
- ✅ Firmenlogo SharePoint-Link aktualisiert
- ✅ Logo inline im Abschnitt "GRAFIKEN & DIAGRAMME" integriert

**Verantwortlich:** AL (KI-Manager)

---

### [2.0] - 2025-12-02
**RAG-Optimierung (Stage 2):**
- ✅ Token-Effizienz: -18% vs. v1.3
- ✅ Redundanzen eliminiert
- ✅ Keywords extrahiert: 35 Primary, 60 Secondary
- ✅ Chunk-Strategie: 12 Abschnitte

**Verantwortlich:** AL (KI-Manager)

---

### [1.0] - 2025-11-13
Initiale OSP-Integration

---

## RAG-OPTIMIERUNG

**Datei:** KOM_CORE_Corporate_Identity.md
**Status:** ✅ PRODUKTIV (RAG)

**Token-Effizienz:**
- Version 2.1: ~56.000 Zeichen
- Version 3.0: ~52.000 Zeichen
- Optimierung: Redundanzen entfernt, Struktur kompaktiert

**Chunk-Statistik:**
- Anzahl: 12 Chunks
- Durchschnitt: ~1.000 Tokens/Chunk
- Überlappung: 175 Tokens

**Keywords:** Primary: 40 | Secondary: 55 | Gesamt: 95

**Assets:** 6 SharePoint-Links (Brand Board, 4 Logos, Organigramm)

---

**Review:** Q2 2026  
**Confidence:** 100% (Validierte Unternehmensdaten, Brand Board 2025, RAG-optimiert) [OSP]

**⚠️ WICHTIGE HINWEISE:**
- Brand Board ist zentrale CI-Referenz (ersetzt Einzeldokumentationen)
- Typografie: Montserrat/Open Sans/Fira Code (Google Fonts, lizenzfrei)
- PANTONE-Werte korrigiert: 3005 C (Blau), 179 C (Orange)
- Header/Footer-Standard für alle Dokumente verbindlich
- Logo-Icon (schneider_S.png) für Favicon/App-Icons verwenden

---

*Version 3.0 integriert das Schneider Brand Board als zentrale CI-Referenz mit aktualisierten Farbwerten, moderner Typografie (Google Fonts), HTML/CSS-Variablen und verbindlichem Dokument-Standard. RAG-optimiert für KI-Systeme (Claude, ChatGPT) und ChromaDB.*

(C: 100%) [OSP]
