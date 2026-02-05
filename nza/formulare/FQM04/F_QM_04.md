---
formblatt_id: F_QM_04
titel: Nach- und Zusatzarbeiten (NZA)
version: 2.0
stand: 2026-02-05
bereich: QM
kategorie: Nacharbeit / Reklamation
sprache: DE

# ═══════════════════════════════════════════════════════════════════
# FELD-DEFINITIONEN (Version 2.0)
# ═══════════════════════════════════════════════════════════════════

pflichtfelder:
  # WICHTIG: nza_id ist NICHT im Formular - wird vom System generiert!
  - datum                   # ISO-Format: YYYY-MM-DD
  - reklamationstyp         # Enum aus dropdown
  - artikel_nr              # Schneider-Artikelnummer
  - losgroesse              # Numerisch
  - ausschuss               # Numerisch (Stueckzahl)
  - verursacher             # Enum Kostenstelle
  - kostenstelle            # Enum Kostenstelle
  - fehler_beschreibung     # Freitext (min. 20 Zeichen)
  - fehler_kategorie        # Enum aus dropdown

optionalfelder:
  - betriebsauftrag         # BA-Nummer
  - qa_nummer               # Verknuepfung zu F-QM-02
  - q_nr_kunde              # Kunden-Reklamationsnummer
  - ersatz_ba               # Ersatz-Betriebsauftrag
  - gutschrift_belastung    # Buchungsreferenz
  - bemerkungen             # Freitext
  - zusaetzliche_taetigkeiten  # Array (max 5)
  - zusaetzliches_material     # Array (max 7) - GEAENDERT!

# ═══════════════════════════════════════════════════════════════════
# DROPDOWN-OPTIONEN (aus Excel Data Validation)
# ═══════════════════════════════════════════════════════════════════

reklamationstyp_optionen:
  - Interne Reklamation
  - Kunden Reklamation
  - Lieferanten Reklamation

kostenstelle_optionen:
  - "1000"                  # KST F1
  - "2000"                  # KST F2
  - "3000"                  # KST F3
  - "4000"                  # KST 4
  - "5000"                  # KST 5
  - Lager
  - Verwaltung
  - Lieferant
  - "keine Zuordnung"

# ACHTUNG: Im Excel haben die Kategorien Zeilenumbrueche!
# Diese muessen beim Parsen entfernt/normalisiert werden.
fehler_kategorie_optionen:
  - Crimpfehler
  - Laengenabweichung           # Excel: "Laengen- abweichung"
  - Verdrahtungsfehler          # Excel: "Verdrahtungs- fehler"
  - Bearbeitungsfehler          # Excel: "Bearbeitungs- fehler"
  - Druck fehlerhaft
  - Arbeitsanweisung falsch
  - Kundenzeichnung falsch
  - Falsches Material
  - Materialfehler
  - Werkzeug/Maschinenfehler    # Excel: "Werkzeug/ Maschinenfehler"
  - Lieferantenfehler/Reklamation  # Excel: "Lieferantenfehler/ Reklamation"

# Mapping Excel-Wert -> Normalisierter Wert
fehler_kategorie_mapping:
  "Laengen- abweichung": "Laengenabweichung"
  "Verdrahtungs- fehler": "Verdrahtungsfehler"
  "Bearbeitungs- fehler": "Bearbeitungsfehler"
  "Werkzeug/ Maschinenfehler": "Werkzeug/Maschinenfehler"
  "Lieferantenfehler/ Reklamation": "Lieferantenfehler/Reklamation"

einheit_optionen:
  - Meter
  - Millimeter
  - Stueck
  - Sonstiges

# ═══════════════════════════════════════════════════════════════════
# TABELLEN-STRUKTUREN
# ═══════════════════════════════════════════════════════════════════

zusaetzliche_taetigkeiten:
  max_eintraege: 5
  felder:
    - prozess               # Freitext (Arbeitsgang)
    - werker                # MA-Kuerzel (gegen HR_CORE validieren)
    - kostenstelle          # Enum Kostenstelle
    - zeit_min              # Numerisch (Minuten)

zusaetzliches_material:
  max_eintraege: 7          # GEAENDERT: War 5, jetzt 7!
  felder:
    - artikel_nummer        # Artikelnummer
    - artikel_bezeichnung   # Freitext
    - menge                 # Numerisch
    - einheit               # Enum

signatur:
  erforderlich: false       # NZA wird oft ohne Signatur angelegt
  felder:
    - ersteller             # MA-Kuerzel

weiterleitung:
  outlook:
    - produktion@schneider-kabelsatzbau.de
  teams_channel: Produktion-NZA
  sharepoint: /sites/NZA_NEU/nza-bilder

# ═══════════════════════════════════════════════════════════════════
# EXCEL-MAPPING (Version 2.0 - WICHTIGE AENDERUNGEN!)
# ═══════════════════════════════════════════════════════════════════

excel_mapping:
  sheet: "FQM04"
  felder:
    # WICHTIG: Keine nza_id im Formular! Wird vom System generiert.
    reklamationstyp: C4       # Dropdown
    datum: F4
    artikel_nr: C5
    betriebsauftrag: F5
    losgroesse: C6
    ausschuss: F6
    verursacher: C7           # Dropdown
    kostenstelle: F7          # Dropdown
    qa_nummer: C10
    q_nr_kunde: F10
    ersatz_ba: C11
    gutschrift_belastung: F11
    fehler_beschreibung: A15:E20   # Merged Textbereich
    fehler_kategorie: G16          # Dropdown (ACHTUNG: Zeilenumbrueche!)
  tabellen:
    zusaetzliche_taetigkeiten:
      start_zeile: 27
      end_zeile: 31
      spalten:
        prozess: B-D
        werker: E
        kostenstelle: F
        zeit_min: G
    zusaetzliches_material:
      start_zeile: 37
      end_zeile: 43           # GEAENDERT: War 41, jetzt 43 (7 Zeilen)
      spalten:
        artikel_nummer: B-C
        artikel_bezeichnung: D-E
        menge: F
        einheit: G

# ═══════════════════════════════════════════════════════════════════
# VALIDIERUNGSREGELN
# ═══════════════════════════════════════════════════════════════════

validierung:
  nza_id:
    pattern: "^NZA-\\d{5}$"
    beispiel: "NZA-26001"
    auto_generate: true        # WICHTIG: Wird vom System generiert!

  datum:
    typ: datum
    format: "YYYY-MM-DD"
    default: "{{HEUTE}}"

  losgroesse:
    typ: numerisch
    min: 1

  ausschuss:
    typ: numerisch
    min: 0
    constraint: "<= losgroesse"

  fehler_beschreibung:
    min_laenge: 20
    max_laenge: 500

  werker:
    typ: ma_kuerzel
    validierung: HR_CORE

  zeit_min:
    typ: numerisch
    min: 1
    einheit: "Minuten"

---

# F-QM-04 Nach- und Zusatzarbeiten (NZA)

## Formular-Header

| Feld | Wert |
|------|------|
| **NZA-ID** | {{nza_id*}} _(auto-generiert)_ |
| **Datum** | {{datum*}} |

---

## Reklamations-Daten

| Feld | Wert |
|------|------|
| **Reklamationstyp** | {{reklamationstyp*}} |
| **Artikel-Nr.** | {{artikel_nr*}} |
| **Betriebsauftrag** | {{betriebsauftrag}} |
| **Losgroesse** | {{losgroesse*}} |
| **Ausschuss** | {{ausschuss*}} |
| **Verursacher** | {{verursacher*}} |
| **Kostenstelle** | {{kostenstelle*}} |

---

## Verknuepfungen

| Feld | Wert |
|------|------|
| **QA-Nummer RMS** | {{qa_nummer}} |
| **Q-Nr. Kunde** | {{q_nr_kunde}} |
| **Ersatz BA** | {{ersatz_ba}} |
| **Gutschrift/Belastung** | {{gutschrift_belastung}} |

---

## Fehler

### Fehler Beschreibung
{{fehler_beschreibung*}}

### Fehler Kategorie
**{{fehler_kategorie*}}**

Optionen:
- Crimpfehler
- Laengenabweichung
- Verdrahtungsfehler
- Bearbeitungsfehler
- Druck fehlerhaft
- Arbeitsanweisung falsch
- Kundenzeichnung falsch
- Falsches Material
- Materialfehler
- Werkzeug/Maschinenfehler
- Lieferantenfehler/Reklamation

---

## Zusaetzliche Taetigkeiten

| # | Prozess | Werker | Kostenstelle | Zeit (Min.) |
|---|---------|--------|--------------|-------------|
| (1) | {{taetigkeit_1_prozess}} | {{taetigkeit_1_werker}} | {{taetigkeit_1_kst}} | {{taetigkeit_1_zeit}} |
| (2) | {{taetigkeit_2_prozess}} | {{taetigkeit_2_werker}} | {{taetigkeit_2_kst}} | {{taetigkeit_2_zeit}} |
| (3) | {{taetigkeit_3_prozess}} | {{taetigkeit_3_werker}} | {{taetigkeit_3_kst}} | {{taetigkeit_3_zeit}} |
| (4) | {{taetigkeit_4_prozess}} | {{taetigkeit_4_werker}} | {{taetigkeit_4_kst}} | {{taetigkeit_4_zeit}} |
| (5) | {{taetigkeit_5_prozess}} | {{taetigkeit_5_werker}} | {{taetigkeit_5_kst}} | {{taetigkeit_5_zeit}} |

**Gesamt-Zeit:** {{gesamt_zeit_min}} Minuten

---

## Zusaetzliches Material (7 Zeilen)

| # | Artikel-Nummer | Artikel-Bezeichnung | Menge | Einheit |
|---|----------------|---------------------|-------|---------|
| (1) | {{material_1_artnr}} | {{material_1_bez}} | {{material_1_menge}} | {{material_1_einheit}} |
| (2) | {{material_2_artnr}} | {{material_2_bez}} | {{material_2_menge}} | {{material_2_einheit}} |
| (3) | {{material_3_artnr}} | {{material_3_bez}} | {{material_3_menge}} | {{material_3_einheit}} |
| (4) | {{material_4_artnr}} | {{material_4_bez}} | {{material_4_menge}} | {{material_4_einheit}} |
| (5) | {{material_5_artnr}} | {{material_5_bez}} | {{material_5_menge}} | {{material_5_einheit}} |
| (6) | {{material_6_artnr}} | {{material_6_bez}} | {{material_6_menge}} | {{material_6_einheit}} |
| (7) | {{material_7_artnr}} | {{material_7_bez}} | {{material_7_menge}} | {{material_7_einheit}} |

---

## Erstellt von

| Ersteller | Datum |
|-----------|-------|
| {{ersteller}} | {{datum}} |

---

*Formblatt-ID: F-QM-04 | Version: 2.0 | Stand: 2026-02-05*
*Erstellt durch OSP-System | Schneider Kabelsatzbau*
