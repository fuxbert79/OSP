# Claude Anwendungsanleitung: Schneider Corporate Identity

**Version:** 1.0 | **Datum:** 2025-12-13 | **Autor:** AL  
**TAG:** [KOM][CORE] | **Zugriff:** 🟢 L1-Öffentlich

---

## 🎯 ZWECK

Diese Anleitung definiert, wie Claude (Desktop, API, Open WebUI) die Corporate Identity der Rainer Schneider Kabelsatzbau GmbH & Co. KG korrekt anwendet.

---

## 🎨 VERBINDLICHE FARBDEFINITIONEN

**Quelle:** Schneider_Kabelsatz_Farbdefinitionen.pdf (Single Source of Truth)

### Primärfarben

| Farbe | HEX | Verwendung |
|-------|-----|------------|
| **Schneider Blau** | `#0080C9` | Headlines, Links, Logo, Primär-Elemente |
| **Schneider Orange** | `#DC500F` | Akzente, CTA, Hover, Warnungen |

### Vollständige Farbspezifikation

```yaml
Schneider_Blau:
  HEX: "#0080C9"
  RGB: "0 / 128 / 201"
  CMYK: "100 / 35 / 0 / 20"
  PANTONE: "3005 C"
  RAL: "5015"
  HKS: "44"
  Websafe: "#0066BB"

Schneider_Orange:
  HEX: "#DC500F"
  RGB: "220 / 80 / 15"
  CMYK: "0 / 80 / 100 / 0"
  PANTONE: "179 C"
  RAL: "2001"
  HKS: "14"
  Websafe: "#E25400"

Schwarz:
  HEX: "#000000"
  PANTONE: "Black"
  CMYK: "0 / 0 / 0 / 100"

Grau_70:
  HEX: "#808080"
  PANTONE: "Black 70%"
  CMYK: "0 / 0 / 0 / 70"
```

---

## 📝 CSS-VARIABLEN (Copy & Paste Ready)

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

.schneider-text {
  color: var(--schneider-blue);
  font-weight: 700;
}

.schneider-accent {
  color: var(--schneider-orange);
}
```

---

## 🔤 TYPOGRAFIE

| Kategorie | Schrift | Fallback | Verwendung |
|-----------|---------|----------|------------|
| **Headlines** | Montserrat Bold | Arial Bold | H1-H3, Titel |
| **Fließtext** | Open Sans Regular | Calibri | Body, Dokumente |
| **Code/Daten** | Fira Code | Consolas | Technische Daten |

**Google Fonts Import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans&family=Fira+Code&display=swap" rel="stylesheet">
```

---

## 📄 DOKUMENT-STANDARD

### Header (rechtsbündig)
```
Dokumentenname | Schneider Kabelsatzbau
                 ▲▲▲▲▲▲▲▲▲
                 Blau #0080C9 + Bold
```

### Footer (dreispaltig)
| Links | Mitte | Rechts |
|-------|-------|--------|
| F-QM-001-A | Seite X von Y | Erstellt: AL 2025-12-13 |

---

## 🖼️ LOGO-HIERARCHIE

| Logo | Dateiname | Verwendung |
|------|-----------|------------|
| **Hauptlogo** | Logo_schneider.png | Web, Docs, Print |
| **Icon (S)** | schneider_S.png | Favicon, App |
| **OSP-Logo** | Logo_OSP_Text.png | KI-System, Tech-Docs |
| **SAS-Logo** | logo_sas.jpg | Nur Holding-Dokumente |

**SharePoint-Basis-URL:**
```
https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Icons_Bilder/
```

---

## ✅ CLAUDE ANWENDUNGSREGELN

### Bei HTML/React-Artefakten:
1. **IMMER** CSS-Variablen aus Abschnitt oben verwenden
2. **IMMER** `--schneider-blue: #0080C9` (nicht #0080C8!)
3. **IMMER** `--schneider-orange: #DC500F` (nicht #0C000F!)
4. **IMMER** `--radius: 10px` verwenden
5. **IMMER** Google Fonts einbinden (Montserrat, Open Sans, Fira Code)

### Bei Dokumenten:
1. Header: `Dokumentenname | Schneider Kabelsatzbau` (Schneider = Blau + Bold)
2. Footer: Formular-ID links, Seite Mitte, Ersteller rechts
3. Schriftart: Open Sans für Fließtext, Montserrat für Headlines

### Bei Farbangaben:
1. **Primär:** HEX-Werte angeben (#0080C9, #DC500F)
2. **Print:** PANTONE oder RAL angeben (3005 C, 179 C / 5015, 2001)
3. **Web Legacy:** Websafe-Werte angeben (#0066BB, #E25400)

---

## ⚠️ HÄUFIGE FEHLER VERMEIDEN

| ❌ FALSCH | ✅ RICHTIG | Erklärung |
|-----------|-----------|-----------|
| `#0080C8` | `#0080C9` | Ein Digit Unterschied! |
| `#0C000F` | `#DC500F` | Tippfehler im Brand Board |
| `--radius: 16px` | `--radius: 10px` | Brand Board definiert 10px |
| `DIN Pro` | `Montserrat` | Alte Schrift ersetzt |
| `Calibri` als Primär | `Open Sans` | Calibri nur Fallback |

---

## 🔧 QUICK-REFERENCE (Claude-Prompt)

Für schnelle CI-konforme Ausgaben diesen Block in Prompts nutzen:

```markdown
## CI-VORGABEN (Schneider Kabelsatzbau)
- Blau: #0080C9 (PANTONE 3005 C, RAL 5015)
- Orange: #DC500F (PANTONE 179 C, RAL 2001)
- Fonts: Montserrat Bold (Headlines), Open Sans (Body), Fira Code (Code)
- Radius: 10px
- Header: "Titel | Schneider Kabelsatzbau" (Schneider = Blau + Bold)
```

---

## 📋 VALIDIERUNGS-CHECKLISTE

Bei CI-relevanten Outputs prüfen:

- [ ] Blau = `#0080C9` (nicht C8!)
- [ ] Orange = `#DC500F` (nicht 0C000F!)
- [ ] Schrift = Montserrat/Open Sans/Fira Code
- [ ] Radius = 10px
- [ ] Header-Format korrekt
- [ ] "Schneider" = Blau + Bold
- [ ] Logo korrekt gewählt (Haupt/Icon/OSP/SAS)

---

## 📚 QUELLEN

| Dokument | Inhalt | Priorität |
|----------|--------|-----------|
| **Schneider_Kabelsatz_Farbdefinitionen.pdf** | Verbindliche Farbwerte | 🔴 HÖCHSTE |
| **Schneider_Brand_Board.png** | Visuelle Referenz | 🟡 HOCH |
| **KOM_CORE_Corporate_Identity.md** | Vollständige CI-Doku | 🟢 STANDARD |

---

**NULL-FEHLER-POLITIK:** AKTIV  
**Confidence:** (C: 100%) [KOM][CORE]

*Bei Unsicherheit: KOM_CORE_Corporate_Identity.md konsultieren oder nachfragen!*
