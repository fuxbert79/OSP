# 📋 NZA-Datenbank - OSP/SharePoint Integration

**Projekt:** Reklamationsprozess-Digitalisierung  
**Organisation:** Rainer Schneider Kabelsatzbau GmbH & Co. KG  
**Version:** 4.0 (n8n + OSP)  
**Erstellt:** 29.01.2026  
**Status:** ✅ Konzept finalisiert

---

## 📑 Inhaltsverzeichnis

1. [Projektziel & Architektur](#1-projektziel--architektur)
2. [Reklamationstypen & ID-Struktur](#2-reklamationstypen--id-struktur)
3. [SharePoint-Liste: fehler_db_template](#3-sharepoint-liste-fehler_db_template)
4. [FQM04 Excel-Formular - Datenextraktion](#4-fqm04-excel-formular---datenextraktion)
5. [Kostenberechnung](#5-kostenberechnung)
6. [n8n Workflow-Architektur](#6-n8n-workflow-architektur)
7. [Fehler-Kategorien](#7-fehler-kategorien)
8. [Validierungsregeln](#8-validierungsregeln)
9. [Technische Referenzen](#9-technische-referenzen)

---

## 1. Projektziel & Architektur

### 1.1 Ziel

Vollständige **Automatisierung des Reklamationsprozesses** bei Schneider Kabelsatzbau:
- Manuelle, handschriftliche FQM04-Formulare → digitale Erfassung
- Automatische Kostenberechnung basierend auf Kostenstellen-Minutensätzen
- Integration in SharePoint Lists als zentrale Datenbank
- Autonome Validierung mit automatischen Rückmeldungen

### 1.2 System-Architektur

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OSP HETZNER SERVER                             │
│                           (46.224.102.30 - CX43)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   n8n       │    │ Open WebUI  │    │  ChromaDB   │    │  Pipelines  │  │
│  │  :5678      │◄──►│   :3000     │◄──►│   :8000     │◄──►│   :9099     │  │
│  └──────┬──────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│         │                                                                   │
│         │ osp-network (Docker Bridge)                                       │
└─────────┼───────────────────────────────────────────────────────────────────┘
          │
          │ HTTPS / OAuth2
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MICROSOFT 365                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  Outlook    │    │ SharePoint  │    │   Teams     │    │  OneDrive   │  │
│  │ nza@...     │    │ NZA-Liste   │    │ QM-Channel  │    │ Archiv      │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Parallelbetrieb mit RMS-System

| System | Funktion | Port | Container |
|--------|----------|------|-----------|
| **NZA-System** | Reklamations-Management | 5678 (n8n) | osp-n8n |
| **RMS-System** | Risk Management | 3000 (WebUI) | open-webui |
| **Gemeinsam** | RAG-Wissensbasis | 8000 | chromadb |

---

## 2. Reklamationstypen & ID-Struktur

### 2.1 Reklamationstypen

| Typ | ID-Format | Zusätzliche IDs | Beschreibung |
|-----|-----------|-----------------|--------------|
| **Interne Reklamation** | `NZA-25-0001` | - | Fehler während der Produktion |
| **Kunden-Reklamation** | `NZA-25-0001` | `QA-25001` + 8D-Report | Fehler beim Kunden erkannt |
| **Lieferanten-Reklamation** | `NZA-25-0001` | `QA-25001` + FQM02 | Fehler bei eingekauftem Material |

### 2.2 ID-Struktur

```
NZA-25-0042
 │   │   │
 │   │   └── Fortlaufende Nummer (4-stellig, mit führenden Nullen)
 │   │
 │   └────── Jahr (2-stellig)
 │
 └────────── Präfix: Nach- und Zusatzarbeit
```

### 2.3 NZA-ID Generierung (n8n)

```javascript
// n8n Code-Node: NZA-ID generieren
const currentYear = new Date().getFullYear().toString().slice(-2);

// Letzte ID aus SharePoint abrufen (via HTTP Request)
const lastId = $input.item.json.lastNzaId || 0;
const nextNumber = (lastId + 1).toString().padStart(4, '0');

const nzaId = `NZA-${currentYear}-${nextNumber}`;

return { json: { nzaId } };
```

---

## 3. SharePoint-Liste: fehler_db_template

### 3.1 Verbindungsdaten

| Eigenschaft | Wert |
|-------------|------|
| **Site URL** | `https://rainerschneiderkabelsatz.sharepoint.com/sites/NZA` |
| **Liste** | `fehler_db_template` |
| **List ID** | `e5e94767-8faf-492f-9f42-3f4551f0aa70` |
| **API Endpoint** | `_api/web/lists(guid'e5e94767-8faf-492f-9f42-3f4551f0aa70')/items` |

### 3.2 Feldstruktur (52 Felder gesamt)

#### Stammdaten (Pflichtfelder ✅)

| # | Display Name | Internal Name | Feldtyp | Excel-Zelle | Transformation | Required |
|---|--------------|---------------|---------|-------------|----------------|----------|
| 1 | **NZA-ID** | Title | Text | - | n8n generiert | ✅ |
| 2 | **Reklamationstyp** | field_1 | Choice | B5 | Normalisieren | ✅ |
| 3 | **Datum** | field_2 | DateTime | E3 | ISO-Format | ✅ |
| 4 | **Artikel-Nr.** | field_3 | Text | B7 | Direkt | ✅ |
| 5 | **Kostenstelle** | field_9 | **Choice** ⚠️ | B13 | **Als STRING!** | ✅ |
| 6 | **Fehler Beschreibung** | field_14 | Note | B19 | Direkt | ✅ |
| 7 | **Fehler Kategorie** | field_15 | **MultiChoice** ⚠️ | B21 | **Als ARRAY!** | ✅ |

#### Optionale Stammdaten

| # | Display Name | Internal Name | Feldtyp | Excel-Zelle |
|---|--------------|---------------|---------|-------------|
| 8 | Betriebsauftrag | field_4 | Number | B9 |
| 9 | Prüfmenge | field_5 | Number | E7 |
| 10 | davon n.i.O. | field_6 | Number | E9 |
| 11 | Verursacher | field_7 | Text | B11 |
| 12 | Verursacher Personal-Nr. | field_8 | Number | E11 |
| 13 | QA-Nummer | field_10 | Number | B15 |
| 14 | Q-Nr. Kunde/Lieferant | field_11 | Text | E15 |
| 15 | Ersatz BA | field_12 | Number | B17 |
| 16 | Gutschrift/Belastung | field_13 | Text | E17 |
| 17 | Bemerkungen | field_16 | Note | B23 |

#### Kosten-Felder

| # | Display Name | Internal Name | Feldtyp | Eingabe |
|---|--------------|---------------|---------|---------|
| 18 | kosten_sonstige | field_17 | Currency | Manuell/n8n |
| 19 | kosten_material | field_65 | Currency | Manuell/n8n |
| 20 | kosten_prozesse | kosten_prozesse_neu | **Calculated** | 🤖 Auto |
| 21 | kosten_gesamt | kosten_gesamt_neu | **Calculated** | 🤖 Auto |

### 3.3 Prozess-Felder (1-5)

Für jeden der 5 möglichen Prozesse gibt es folgende Felder:

| Feldtyp | Prozess 1 | Prozess 2 | Prozess 3 | Prozess 4 | Prozess 5 |
|---------|-----------|-----------|-----------|-----------|-----------|
| **Prozess** (Text) | field_19 | field_24 | field_29 | field_34 | field_39 |
| **Werker** (Text) | field_20 | field_25 | field_30 | field_35 | field_40 |
| **Kostenstelle** (Choice) | kostenstelle_1 | kostenstelle_2 | kostenstelle_3 | kostenstelle_4 | kostenstelle_5 |
| **Zeit in Min** (Number) | field_22 | field_27 | field_32 | field_37 | field_42 |
| **Faktor** 🤖 (Calculated) | kostenstelle_1_faktor | kostenstelle_2_faktor | kostenstelle_3_faktor | kostenstelle_4_faktor | kostenstelle_5_faktor |
| **Kosten** 🤖 (Calculated) | kosten_1 | kosten_2 | kosten_3 | kosten_4 | kosten_5 |

🤖 = Automatisch von SharePoint berechnet

---

## 4. FQM04 Excel-Formular - Datenextraktion

### 4.1 Excel-Struktur

Das FQM04-Formular hat folgende Bereiche:

```
┌─────────────────────────────────────────────────────────────┐
│                    FQM04 - KOPFBEREICH                      │
├─────────────────────────────────────────────────────────────┤
│ A1: "NZA-Nummer:"      │ B3: [NZA-ID]                       │
│ A3: "Datum:"           │ E3: [DATUM]                        │
│ A5: "Reklamationsart:" │ B5: [TYP]                          │
│ A7: "Artikel-Nr.:"     │ B7: [ARTIKEL]    │ E7: [PRÜFMENGE] │
│ A9: "Betriebsauftrag:" │ B9: [BA]         │ E9: [N.I.O.]    │
├─────────────────────────────────────────────────────────────┤
│                    VERURSACHER                              │
├─────────────────────────────────────────────────────────────┤
│ A11: "Verursacher:"    │ B11: [NAME]      │ E11: [PERS-NR]  │
│ A13: "Kostenstelle:"   │ B13: [KS]                          │
├─────────────────────────────────────────────────────────────┤
│                    DOKUMENTATION                            │
├─────────────────────────────────────────────────────────────┤
│ A15: "QA-Nummer:"      │ B15: [QA-NR]     │ E15: [EXT-QNR]  │
│ A17: "Ersatz BA:"      │ B17: [ERSATZ]    │ E17: [GUTSCHR]  │
│ A19: "Fehlerbeschr.:"  │ B19: [BESCHREIBUNG - mehrzeilig]   │
│ A21: "Kategorie:"      │ B21: [KATEGORIE]                   │
│ A23: "Bemerkungen:"    │ B23: [BEMERKUNGEN]                 │
├─────────────────────────────────────────────────────────────┤
│                    AUSGEFÜHRTE ARBEITEN                     │
├─────────────────────────────────────────────────────────────┤
│ Zeile │ Prozess     │ Werker      │ KS   │ Zeit (Min)      │
│  27   │ [PROZESS_1] │ [WERKER_1]  │ [KS] │ [ZEIT_1]        │
│  28   │ [PROZESS_2] │ [WERKER_2]  │ [KS] │ [ZEIT_2]        │
│  29   │ [PROZESS_3] │ [WERKER_3]  │ [KS] │ [ZEIT_3]        │
│  30   │ [PROZESS_4] │ [WERKER_4]  │ [KS] │ [ZEIT_4]        │
│  31   │ [PROZESS_5] │ [WERKER_5]  │ [KS] │ [ZEIT_5]        │
├─────────────────────────────────────────────────────────────┤
│                    KOSTEN                                   │
├─────────────────────────────────────────────────────────────┤
│ A55: "Sonstige Kosten:" │ E55: [KOSTEN_SONSTIGE]            │
│ A57: "Material gesamt:" │ E57: [KOSTEN_MATERIAL]            │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Zellen-Mapping (Komplett)

| Bereich | Excel-Zelle | SharePoint Feld | Internal Name | Typ |
|---------|-------------|-----------------|---------------|-----|
| **Kopf** | B3 | *(wird ignoriert)* | - | - |
| | E3 | Datum | field_2 | DateTime |
| | B5 | Reklamationstyp | field_1 | Choice |
| | B7 | Artikel-Nr. | field_3 | Text |
| | E7 | Prüfmenge | field_5 | Number |
| | B9 | Betriebsauftrag | field_4 | Number |
| | E9 | davon n.i.O. | field_6 | Number |
| **Verursacher** | B11 | Verursacher | field_7 | Text |
| | E11 | Verursacher Personal-Nr. | field_8 | Number |
| | B13 | Kostenstelle | field_9 | Choice |
| **Doku** | B15 | QA-Nummer | field_10 | Number |
| | E15 | Q-Nr. Kunde/Lieferant | field_11 | Text |
| | B17 | Ersatz BA | field_12 | Number |
| | E17 | Gutschrift/Belastung | field_13 | Text |
| | B19 | Fehler Beschreibung | field_14 | Note |
| | B21 | Fehler Kategorie | field_15 | MultiChoice |
| | B23 | Bemerkungen | field_16 | Note |
| **Prozess 1** | A27 | Prozess_1 | field_19 | Text |
| | B27 | Werker_1 | field_20 | Text |
| | C27 | kostenstelle_1 | kostenstelle_1 | Choice |
| | D27 | Zeit_1 | field_22 | Number |
| **Prozess 2-5** | A28:D31 | *(analog)* | *(siehe 3.3)* | - |
| **Kosten** | E55 | kosten_sonstige | field_17 | Currency |
| | E57 | kosten_material | field_65 | Currency |

### 4.3 Datentyp-Transformationen

#### Reklamationstyp normalisieren (field_1)

```javascript
// n8n Code-Node
const input = $input.item.json.reklamationsart.toLowerCase().trim();

let reklamationstyp;
if (input.includes('intern') || input === 'i') {
  reklamationstyp = 'Interne Reklamation';
} else if (input.includes('kunde') || input === 'k') {
  reklamationstyp = 'Kunden Reklamation';
} else if (input.includes('lieferant') || input === 'l') {
  reklamationstyp = 'Lieferanten Reklamation';
} else {
  reklamationstyp = 'Interne Reklamation'; // Fallback
}

return { json: { reklamationstyp } };
```

#### Kostenstelle normalisieren (field_9) ⚠️ KRITISCH

```javascript
// n8n Code-Node
// WICHTIG: field_9 ist Choice (Einfachauswahl) → Als STRING übergeben!

let kostenstelle = $input.item.json.kostenstelle.toString().trim();

// "KS1000" → "1000"
if (kostenstelle.toUpperCase().startsWith('KS')) {
  kostenstelle = kostenstelle.substring(2);
}

// Bei Mehrfach-Angabe nur erste nehmen
if (kostenstelle.includes(',')) {
  kostenstelle = kostenstelle.split(',')[0].trim();
}

// Validierung
const validKostenstellen = ['1000', '2000', '3000', '4000', '5000', 'Lager', 'Verwaltung', 'Lieferant', 'keine Zuordnung'];
if (!validKostenstellen.includes(kostenstelle)) {
  kostenstelle = 'keine Zuordnung';
}

// ✅ Als String zurückgeben
return { json: { kostenstelle } };
```

#### Fehler-Kategorien als Array (field_15) ⚠️ KRITISCH

```javascript
// n8n Code-Node
// WICHTIG: field_15 ist MultiChoice → Als ARRAY übergeben!

const input = $input.item.json.fehler_kategorie.toLowerCase();
const kategorien = [];

const mappings = {
  'crimp': 'Crimpfehler',
  'länge': 'Längenabweichung',
  'verdraht': 'Verdrahtungsfehler',
  'bearbeit': 'Bearbeitungsfehler',
  'druck': 'Druck fehlerhaft',
  'arbeitsanweisung': 'Arbeitsanweisung falsch',
  'aa': 'Arbeitsanweisung falsch',
  'zeichnung': 'Kundenzeichnung falsch',
  'kz': 'Kundenzeichnung falsch',
  'falsches material': 'Falsches Material',
  'materialfehler': 'Materialfehler',
  'werkzeug': 'Werkzeug/Maschinenfehler',
  'maschine': 'Werkzeug/Maschinenfehler',
  'lieferant': 'Lieferantenfehler/Reklamation'
};

for (const [key, value] of Object.entries(mappings)) {
  if (input.includes(key) && !kategorien.includes(value)) {
    kategorien.push(value);
  }
}

// Fallback
if (kategorien.length === 0) {
  kategorien.push('Sonstige');
}

// ✅ Als Array zurückgeben
return { json: { fehler_kategorien: kategorien } };
```

#### Datum formatieren (field_2)

```javascript
// n8n Code-Node
const input = $input.item.json.datum;

// Deutsches Format "DD.MM.YYYY" → ISO "YYYY-MM-DDTHH:mm:ssZ"
let isoDate;

if (input.includes('.')) {
  // Deutsches Format
  const parts = input.split('.');
  const day = parts[0].padStart(2, '0');
  const month = parts[1].padStart(2, '0');
  const year = parts[2].length === 2 ? '20' + parts[2] : parts[2];
  isoDate = `${year}-${month}-${day}T00:00:00Z`;
} else {
  // Bereits ISO oder Excel-Serial
  isoDate = new Date(input).toISOString();
}

return { json: { datum: isoDate } };
```

---

## 5. Kostenberechnung

### 5.1 Minutensätze nach Kostenstelle

| Kostenstelle | Faktor (€/Min) | Stundensatz (€/h) | Beschreibung |
|--------------|----------------|-------------------|--------------|
| **1000** | 1,98 | 118,80 | Fertigung F1 |
| **2000** | 1,21 | 72,60 | Fertigung F2 |
| **3000** | 0,93 | 55,80 | Fertigung F3 |
| **4000** | 1,02 | 61,20 | Fertigung F4 |
| **5000** | 1,02 | 61,20 | Fertigung F5 |
| **Lager** | 1,10 | 66,00 | Lagerbereich |
| **Verwaltung** | 1,37 | 82,20 | Administration |

### 5.2 Berechnungslogik

```
┌─────────────────────────────────────────────────────────────┐
│                    EINGABE (aus FQM04)                      │
├─────────────────────────────────────────────────────────────┤
│ • Zeit_1 bis Zeit_5 (in Minuten)                           │
│ • kostenstelle_1 bis kostenstelle_5 (Auswahl)              │
│ • kosten_material (Gesamtbetrag in €)                      │
│ • kosten_sonstige (Gesamtbetrag in €)                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               n8n BERECHNUNG (vor SharePoint)               │
├─────────────────────────────────────────────────────────────┤
│ 1. Faktor-Ermittlung pro Prozess:                          │
│    faktor_X = MINUTENSATZ_MAP[kostenstelle_X]              │
│                                                             │
│ 2. Kosten pro Prozess:                                      │
│    kosten_X = zeit_X × faktor_X                            │
│                                                             │
│ 3. Summe Prozesskosten:                                     │
│    kosten_prozesse = Σ(kosten_1 + ... + kosten_5)          │
│                                                             │
│ 4. Gesamtkosten:                                            │
│    kosten_gesamt = kosten_prozesse + kosten_material        │
│                    + kosten_sonstige                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│            SharePoint CALCULATED FIELDS (Backup)            │
├─────────────────────────────────────────────────────────────┤
│ SharePoint berechnet die gleichen Werte nochmal zur         │
│ Sicherheit. Bei Abweichung gilt SharePoint-Wert.           │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 n8n Code-Node: Kostenberechnung

```javascript
// n8n Code-Node: Vollständige Kostenberechnung

const MINUTENSATZ = {
  '1000': 1.98,
  '2000': 1.21,
  '3000': 0.93,
  '4000': 1.02,
  '5000': 1.02,
  'Lager': 1.10,
  'Verwaltung': 1.37,
  'Lieferant': 0,
  'keine Zuordnung': 0
};

const data = $input.item.json;

// Prozesskosten berechnen
let kosten_prozesse = 0;
const prozessKosten = [];

for (let i = 1; i <= 5; i++) {
  const zeit = parseFloat(data[`zeit_${i}`]) || 0;
  const ks = data[`kostenstelle_${i}`] || '';
  const faktor = MINUTENSATZ[ks] || 0;
  const kosten = Math.round(zeit * faktor * 100) / 100;
  
  prozessKosten.push({
    prozess: i,
    zeit: zeit,
    kostenstelle: ks,
    faktor: faktor,
    kosten: kosten
  });
  
  kosten_prozesse += kosten;
}

// Material- und Sonstige Kosten
const kosten_material = parseFloat(data.kosten_material) || 0;
const kosten_sonstige = parseFloat(data.kosten_sonstige) || 0;

// Gesamtkosten
const kosten_gesamt = Math.round((kosten_prozesse + kosten_material + kosten_sonstige) * 100) / 100;

return {
  json: {
    prozessKosten: prozessKosten,
    kosten_prozesse: kosten_prozesse,
    kosten_material: kosten_material,
    kosten_sonstige: kosten_sonstige,
    kosten_gesamt: kosten_gesamt
  }
};
```

### 5.4 Beispielberechnung

**Eingabe aus FQM04:**
```
Prozess 1: Nachcrimpen     | KS 1000 | 45 Min
Prozess 2: Sichtprüfung    | KS 2000 | 15 Min
Prozess 3: Verpackung      | Lager   | 10 Min
Material-Kosten: 3,70 €
Sonstige Kosten: 0,00 €
```

**Berechnung:**
```
Prozess 1: 45 Min × 1,98 €/Min = 89,10 €
Prozess 2: 15 Min × 1,21 €/Min = 18,15 €
Prozess 3: 10 Min × 1,10 €/Min = 11,00 €
                                ─────────
Σ kosten_prozesse            = 118,25 €

+ kosten_material            =   3,70 €
+ kosten_sonstige            =   0,00 €
                                ─────────
= kosten_gesamt              = 121,95 €
```

---

## 6. n8n Workflow-Architektur

### 6.1 Workflow-Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WF-02_NZA_KOSTEN (n8n)                               │
│                    Trigger: nza@schneider-kabelsatzbau.de               │
└─────────────────────────────────────────────────────────────────────────┘

        ┌─────────────────────────────────────────────────────────┐
        │ 1. TRIGGER: Microsoft Outlook Trigger                   │
        │    Mailbox: nza@schneider-kabelsatzbau.de               │
        │    Filter: Has Attachment = Yes, *.xlsx                 │
        └────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │ 2. GET ATTACHMENT: Datei-Inhalt extrahieren             │
        │    Prüfen: Ist FQM04.xlsx vorhanden?                    │
        └────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │ 3. EXTRACT: Excel-Daten auslesen                        │
        │    • Spreadsheet File Node                              │
        │    • Alle Zellen gemäß Mapping extrahieren              │
        └────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │ 4. TRANSFORM: Daten transformieren                      │
        │    • Reklamationstyp normalisieren                      │
        │    • Kostenstelle als String                            │
        │    • Fehler-Kategorien als Array                        │
        │    • Datum in ISO-Format                                │
        └────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │ 5. GENERATE NZA-ID: Neue ID erstellen                   │
        │    • Letzte ID aus SharePoint abrufen                   │
        │    • Inkrement + Format NZA-YY-XXXX                     │
        └────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │ 6. CALCULATE: Kosten berechnen                          │
        │    • Minutensätze × Zeit pro Prozess                    │
        │    • Summen bilden                                      │
        └────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │ 7. VALIDATE: Pflichtfelder prüfen                       │
        │    • Title, field_1, field_2, field_3 vorhanden?       │
        │    • field_9 (KS) gültig?                               │
        │    • field_15 (Kategorie) mind. 1?                      │
        │    • Kosten plausibel (> 0)?                            │
        └────────────────────────┬────────────────────────────────┘
                                 │
                       ┌─────────┴─────────┐
                       │                   │
                 Validierung OK?      Validierung FEHLER
                       │                   │
                       ▼                   ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│ 8a. SharePoint: Create Item  │  │ 8b. NOTIFY ERROR             │
│     • Alle Felder übergeben  │  │     • Email an Absender      │
│     • Berechnete auslassen   │  │     • Teams-Nachricht        │
└──────────────┬───────────────┘  │     • Fehlerdetails          │
               │                  │     • Korrektur-Anleitung    │
               ▼                  └──────────────────────────────┘
┌──────────────────────────────┐
│ 9. SharePoint: Update Item   │
│    (Neuberechnung erzwingen) │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ 10. SharePoint: Upload       │
│     • FQM04.xlsx archivieren │
│     • Pfad: /NZA/{Jahr}/     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ 11. NOTIFY SUCCESS           │
│     • Teams an QM (Andreas)  │
│     • Link zur Liste         │
│     • Kostenzusammenfassung  │
└──────────────────────────────┘
```

### 6.2 n8n Nodes - Detailkonfiguration

#### Node 1: Microsoft Outlook Trigger

```yaml
Node: Microsoft Outlook Trigger
Operation: New Email
Credentials: Microsoft OAuth2 (Schneider)
Options:
  Folder: Inbox
  Has Attachments: true
  Filter: Subject contains "FQM04" OR "Reklamation"
```

#### Node 2: Get Attachment Content

```yaml
Node: Microsoft Outlook
Operation: Get Attachment
Message ID: {{ $json.id }}
Attachment ID: {{ $json.attachments[0].id }}
```

#### Node 3: Spreadsheet File

```yaml
Node: Spreadsheet File
Operation: From File
Binary Property: data
File Format: xlsx
Header Row: false (Positionales Auslesen)
```

#### Node 4: Code - Transform

```javascript
// Siehe Abschnitt 4.3 für vollständigen Code
```

#### Node 5: Code - Generate NZA-ID

```javascript
// HTTP Request vorher: Letzte ID aus SharePoint holen
const lastItem = $('HTTP Request').item.json.value[0];
const lastId = lastItem ? parseInt(lastItem.Title.split('-')[2]) : 0;

const currentYear = new Date().getFullYear().toString().slice(-2);
const nextNumber = (lastId + 1).toString().padStart(4, '0');
const nzaId = `NZA-${currentYear}-${nextNumber}`;

return { json: { nzaId } };
```

#### Node 6: Code - Calculate Costs

```javascript
// Siehe Abschnitt 5.3 für vollständigen Code
```

#### Node 7: IF - Validation

```yaml
Node: IF
Conditions (AND):
  - {{ $json.nzaId }} is not empty
  - {{ $json.reklamationstyp }} is not empty
  - {{ $json.datum }} is not empty
  - {{ $json.artikel_nr }} is not empty
  - {{ $json.kostenstelle }} is not empty
  - {{ $json.fehlerbeschreibung }} is not empty
  - {{ $json.fehler_kategorien.length }} > 0
```

#### Node 8a: Microsoft SharePoint - Create Item

```yaml
Node: Microsoft SharePoint
Operation: Create
Site: rainerschneiderkabelsatz.sharepoint.com/sites/NZA
List: fehler_db_template
Fields:
  Title: {{ $json.nzaId }}
  field_1: {{ $json.reklamationstyp }}
  field_2: {{ $json.datum }}
  field_3: {{ $json.artikel_nr }}
  field_4: {{ $json.betriebsauftrag || null }}
  field_5: {{ $json.pruefmenge || null }}
  field_6: {{ $json.davon_nio || null }}
  field_7: {{ $json.verursacher || '' }}
  field_8: {{ $json.personal_nr || null }}
  field_9: {{ $json.kostenstelle }}  # ⚠️ STRING!
  field_14: {{ $json.fehlerbeschreibung }}
  field_15: {{ $json.fehler_kategorien }}  # ⚠️ ARRAY!
  field_17: {{ $json.kosten_sonstige || 0 }}
  field_65: {{ $json.kosten_material || 0 }}
  # Prozess-Felder...
```

#### Node 8b: Error Notification

```yaml
# Email an Absender
Node: Microsoft Outlook
Operation: Send Email
To: {{ $('Trigger').item.json.from.emailAddress.address }}
Subject: ⚠️ FQM04 Validierungsfehler - Korrektur erforderlich
Body: |
  Sehr geehrte/r Kolleg/in,
  
  bei der automatischen Verarbeitung Ihrer FQM04-Einreichung 
  wurden folgende Probleme festgestellt:
  
  {{ $json.validationErrors.join('\n• ') }}
  
  Bitte korrigieren Sie das Formular und senden Sie es erneut an:
  nza@schneider-kabelsatzbau.de
  
  Bei Fragen wenden Sie sich an das QM-Team.
  
  Mit freundlichen Grüßen
  NZA-Automatisierung

# Teams-Nachricht an QM
Node: Microsoft Teams
Operation: Send Message
Team: Schneider Kabelsatzbau
Channel: QM-Alerts
Message: |
  ⚠️ **FQM04 Validierungsfehler**
  
  Absender: {{ $('Trigger').item.json.from.emailAddress.address }}
  Betreff: {{ $('Trigger').item.json.subject }}
  Zeitpunkt: {{ new Date().toLocaleString('de-DE') }}
  
  Fehler:
  {{ $json.validationErrors.join('\n• ') }}
  
  Automatische Rückmeldung wurde an Absender gesendet.
```

#### Node 11: Success Notification

```yaml
Node: Microsoft Teams
Operation: Send Message
Team: Schneider Kabelsatzbau
Channel: QM-Alerts
Message: |
  ✅ **Neue Reklamation erfasst**
  
  **NZA-ID:** {{ $json.nzaId }}
  **Typ:** {{ $json.reklamationstyp }}
  **Artikel:** {{ $json.artikel_nr }}
  **Verursacher:** {{ $json.verursacher || 'Nicht angegeben' }}
  
  **Kosten:**
  • Prozesse: {{ $json.kosten_prozesse.toFixed(2) }} €
  • Material: {{ $json.kosten_material.toFixed(2) }} €
  • Sonstige: {{ $json.kosten_sonstige.toFixed(2) }} €
  • **Gesamt: {{ $json.kosten_gesamt.toFixed(2) }} €**
  
  [📋 In SharePoint öffnen](https://rainerschneiderkabelsatz.sharepoint.com/sites/NZA/Lists/fehler_db_template/DispForm.aspx?ID={{ $json.sharePointItemId }})
```

### 6.3 Validierungsregeln im Detail

```javascript
// n8n Code-Node: Vollständige Validierung

const data = $input.item.json;
const errors = [];

// 1. Pflichtfelder
if (!data.reklamationstyp) {
  errors.push('Reklamationstyp fehlt (Zelle B5)');
}

if (!data.datum) {
  errors.push('Datum fehlt (Zelle E3)');
}

if (!data.artikel_nr) {
  errors.push('Artikel-Nr. fehlt (Zelle B7)');
}

if (!data.kostenstelle) {
  errors.push('Kostenstelle Verursacher fehlt (Zelle B13)');
}

if (!data.fehlerbeschreibung || data.fehlerbeschreibung.length < 10) {
  errors.push('Fehlerbeschreibung fehlt oder zu kurz (Zelle B19)');
}

if (!data.fehler_kategorien || data.fehler_kategorien.length === 0) {
  errors.push('Mindestens eine Fehler-Kategorie erforderlich (Zelle B21)');
}

// 2. Datentyp-Validierung
const validKostenstellen = ['1000', '2000', '3000', '4000', '5000', 'Lager', 'Verwaltung', 'Lieferant', 'keine Zuordnung'];
if (data.kostenstelle && !validKostenstellen.includes(data.kostenstelle)) {
  errors.push(`Ungültige Kostenstelle: "${data.kostenstelle}". Gültig: ${validKostenstellen.join(', ')}`);
}

const validTypen = ['Interne Reklamation', 'Kunden Reklamation', 'Lieferanten Reklamation'];
if (data.reklamationstyp && !validTypen.includes(data.reklamationstyp)) {
  errors.push(`Ungültiger Reklamationstyp: "${data.reklamationstyp}"`);
}

// 3. Logik-Validierung
if (data.davon_nio && data.pruefmenge && data.davon_nio > data.pruefmenge) {
  errors.push(`Ausschuss (${data.davon_nio}) kann nicht größer als Prüfmenge (${data.pruefmenge}) sein`);
}

// 4. Prozess-Validierung
let hatProzess = false;
for (let i = 1; i <= 5; i++) {
  const zeit = parseFloat(data[`zeit_${i}`]) || 0;
  const ks = data[`kostenstelle_${i}`];
  
  if (zeit > 0 && !ks) {
    errors.push(`Prozess ${i}: Zeit angegeben aber keine Kostenstelle`);
  }
  
  if (zeit > 0) hatProzess = true;
}

// Mindestens ein Prozess oder Materialkosten
if (!hatProzess && (!data.kosten_material || data.kosten_material === 0)) {
  errors.push('Mindestens ein Prozess mit Zeit > 0 ODER Materialkosten erforderlich');
}

// 5. Kostenplausibilität
if (data.kosten_gesamt < 0) {
  errors.push('Gesamtkosten können nicht negativ sein');
}

if (data.kosten_gesamt > 10000) {
  errors.push(`Ungewöhnlich hohe Kosten (${data.kosten_gesamt} €) - bitte prüfen`);
}

// Ergebnis
const isValid = errors.length === 0;

return {
  json: {
    ...data,
    isValid: isValid,
    validationErrors: errors
  }
};
```

---

## 7. Fehler-Kategorien

### 7.1 Verfügbare Kategorien (field_15)

| # | Kategorie | Beschreibung | Typische Ursache |
|---|-----------|--------------|------------------|
| 1 | Crimpfehler | Fehler bei Crimpverbindungen | Falsche Crimp-Parameter |
| 2 | Längenabweichung | Kabel zu lang/kurz | Fehler beim Ablängen |
| 3 | Verdrahtungsfehler | Falsche Verdrahtung | Vertauschte Adern |
| 4 | Bearbeitungsfehler | Fehler bei Bearbeitung | Unsachgemäße Handhabung |
| 5 | Druck fehlerhaft | Beschriftung falsch | Druckerfehler/falsches Label |
| 6 | Arbeitsanweisung falsch | Fehler in AA | Dokumentationsfehler |
| 7 | Kundenzeichnung falsch | Fehler in KZ | Zeichnung fehlerhaft |
| 8 | Falsches Material | Falsches Material verwendet | Verwechslung |
| 9 | Materialfehler | Defektes Material | Qualitätsproblem Lieferant |
| 10 | Werkzeug/Maschinenfehler | Technischer Defekt | Verschleiß/Ausfall |
| 11 | Lieferantenfehler/Reklamation | Externer Fehler | Lieferqualität |

### 7.2 Kategorie-Erkennung (Automatisch)

```javascript
// Keyword-Mapping für automatische Erkennung
const KATEGORIE_KEYWORDS = {
  'Crimpfehler': ['crimp', 'crimpen', 'quetsch', 'pressung'],
  'Längenabweichung': ['länge', 'lang', 'kurz', 'ablängen', 'maß'],
  'Verdrahtungsfehler': ['verdraht', 'ader', 'vertauscht', 'verkabelt'],
  'Bearbeitungsfehler': ['bearbeit', 'handling', 'beschädigt'],
  'Druck fehlerhaft': ['druck', 'label', 'beschriftung', 'etikette'],
  'Arbeitsanweisung falsch': ['arbeitsanweisung', 'aa', 'anweisung'],
  'Kundenzeichnung falsch': ['zeichnung', 'kz', 'plan'],
  'Falsches Material': ['falsches material', 'verwechslung'],
  'Materialfehler': ['materialfehler', 'defekt', 'fehlerhaftes material'],
  'Werkzeug/Maschinenfehler': ['werkzeug', 'maschine', 'gerät', 'automat'],
  'Lieferantenfehler/Reklamation': ['lieferant', 'zulieferer', 'extern']
};
```

---

## 8. Validierungsregeln

### 8.1 Pflichtfeld-Prüfung

| Feld | Regel | Fehlermeldung |
|------|-------|---------------|
| Title (NZA-ID) | Wird generiert | - |
| field_1 (Reklamationstyp) | Nicht leer, gültiger Wert | "Reklamationstyp fehlt (Zelle B5)" |
| field_2 (Datum) | Gültiges Datum, nicht in Zukunft | "Datum fehlt oder ungültig (Zelle E3)" |
| field_3 (Artikel-Nr.) | Nicht leer | "Artikel-Nr. fehlt (Zelle B7)" |
| field_9 (Kostenstelle) | Gültiger Wert aus Liste | "Kostenstelle ungültig (Zelle B13)" |
| field_14 (Beschreibung) | Min. 10 Zeichen | "Fehlerbeschreibung zu kurz" |
| field_15 (Kategorie) | Min. 1 Eintrag | "Fehler-Kategorie fehlt" |

### 8.2 Logik-Validierung

| Regel | Bedingung | Aktion |
|-------|-----------|--------|
| Ausschuss ≤ Prüfmenge | field_6 ≤ field_5 | Warnung bei Überschreitung |
| Mind. 1 Prozess oder Material | Zeit > 0 ODER Material > 0 | Fehler wenn beides 0 |
| Kostenstelle bei Zeit | Zeit > 0 → KS erforderlich | Fehler wenn KS fehlt |
| Kosten-Plausibilität | kosten_gesamt < 10.000 € | Warnung bei Überschreitung |

### 8.3 Datentyp-Validierung

| Feld | Erwartet | Validierung |
|------|----------|-------------|
| field_9 | **String** | `typeof === 'string'` |
| field_15 | **Array** | `Array.isArray()` |
| field_4, field_8, field_10, field_12 | Number | 6-stellig (111111-999999) |
| field_17, field_65 | Currency | Positiv, 2 Dezimalstellen |

---

## 9. Technische Referenzen

### 9.1 SharePoint API

```bash
# Liste abfragen
GET https://rainerschneiderkabelsatz.sharepoint.com/sites/NZA/_api/web/lists(guid'e5e94767-8faf-492f-9f42-3f4551f0aa70')/items

# Item erstellen
POST https://rainerschneiderkabelsatz.sharepoint.com/sites/NZA/_api/web/lists(guid'e5e94767-8faf-492f-9f42-3f4551f0aa70')/items
Content-Type: application/json;odata=verbose

# Letzte NZA-ID abrufen
GET .../_api/web/lists(...)/items?$select=Title&$orderby=Created desc&$top=1
```

### 9.2 n8n Server

| Eigenschaft | Wert |
|-------------|------|
| **Server** | Hetzner CX43 |
| **IP** | 46.224.102.30 |
| **n8n Port** | 5678 |
| **Container** | osp-n8n |
| **Netzwerk** | osp-network |

### 9.3 Email-Adressen

| Adresse | Funktion |
|---------|----------|
| `nza@schneider-kabelsatzbau.de` | Trigger für NZA-Workflow |
| `reklamationen@schneider-kabelsatzbau.de` | CC für Dokumentation |
| `a.loehr@schneider-kabelsatzbau.de` | QM-Benachrichtigungen |

### 9.4 Teams-Kanäle

| Team | Channel | Verwendung |
|------|---------|------------|
| Schneider Kabelsatzbau | QM-Alerts | Erfolgs-/Fehlermeldungen |

---

## 📎 Anhang: JSON-Beispiel

### Vollständiger SharePoint-Eintrag

```json
{
  "Title": "NZA-26-0001",
  "field_1": "Interne Reklamation",
  "field_2": "2026-01-29T00:00:00Z",
  "field_3": "KB-98765",
  "field_4": 445566,
  "field_5": 1000,
  "field_6": 12,
  "field_7": "Max Mustermann",
  "field_8": 4567,
  "field_9": "1000",
  "field_10": null,
  "field_11": "",
  "field_12": null,
  "field_13": "",
  "field_14": "Crimpung nicht i.O., 12 Stück nachcrimpen",
  "field_15": ["Crimpfehler"],
  "field_16": "",
  "field_17": 0.00,
  "field_19": "Nachcrimpen",
  "field_20": "M. Mustermann",
  "kostenstelle_1": "1000",
  "field_22": 45,
  "field_24": "Sichtprüfung",
  "field_25": "A. Schmidt",
  "kostenstelle_2": "2000",
  "field_27": 15,
  "field_29": "",
  "field_30": "",
  "kostenstelle_3": null,
  "field_32": 0,
  "field_34": "",
  "field_35": "",
  "kostenstelle_4": null,
  "field_37": 0,
  "field_39": "",
  "field_40": "",
  "kostenstelle_5": null,
  "field_42": 0,
  "field_65": 3.70
}
```

---

**Dokument erstellt:** 29.01.2026  
**Autor:** QM-Team / Claude AI  
**Version:** 4.0 (n8n + OSP Integration)  
**Nächster Review:** Nach Go-Live
