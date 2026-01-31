---
formblatt_id: F_QM_04
titel: Nach- und Zusatzarbeiten (NZA)
version: 1.0
stand: 2025-12-21
bereich: QM
kategorie: Nacharbeit / Reklamation
sprache: DE

# ═══════════════════════════════════════════════════════════════════
# FELD-DEFINITIONEN
# ═══════════════════════════════════════════════════════════════════

pflichtfelder:
  - nza_id                  # Format: NZA-YYYY-NNN (auto-generiert)
  - datum                   # ISO-Format: YYYY-MM-DD
  - reklamationstyp         # Enum aus dropdown
  - artikel_nr              # Schneider-Artikelnummer
  - losgroesse              # Numerisch
  - ausschuss               # Numerisch (Stückzahl)
  - verursacher             # Enum Kostenstelle
  - kostenstelle            # Enum Kostenstelle
  - fehler_beschreibung     # Freitext (min. 20 Zeichen)
  - fehler_kategorie        # Enum aus dropdown

optionalfelder:
  - betriebsauftrag         # BA-Nummer
  - qa_nummer               # Verknüpfung zu F-QM-02
  - q_nr_kunde              # Kunden-Reklamationsnummer
  - ersatz_ba               # Ersatz-Betriebsauftrag
  - gutschrift_belastung    # Buchungsreferenz
  - bemerkungen             # Freitext
  - zusaetzliche_taetigkeiten  # Array (max 5)
  - zusaetzliches_material     # Array (max 5)

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

fehler_kategorie_optionen:
  - Crimpfehler
  - Längenabweichung
  - Verdrahtungsfehler
  - Bearbeitungsfehler
  - Druck fehlerhaft
  - Arbeitsanweisung falsch
  - Kundenzeichnung falsch
  - Falsches Material
  - Materialfehler
  - Werkzeug/Maschinenfehler
  - Lieferantenfehler/Reklamation

einheit_optionen:
  - Meter
  - Millimeter
  - Stück
  - Sonstiges

# ═══════════════════════════════════════════════════════════════════
# TABELLEN-STRUKTUREN
# ═══════════════════════════════════════════════════════════════════

zusaetzliche_taetigkeiten:
  max_eintraege: 5
  felder:
    - prozess               # Freitext (Arbeitsgang)
    - werker                # MA-Kürzel (gegen HR_CORE validieren)
    - kostenstelle          # Enum Kostenstelle
    - zeit_min              # Numerisch (Minuten)

zusaetzliches_material:
  max_eintraege: 5
  felder:
    - artikel_nummer        # Artikelnummer
    - artikel_bezeichnung   # Freitext
    - menge                 # Numerisch
    - einheit               # Enum

signatur:
  erforderlich: false       # NZA wird oft ohne Signatur angelegt
  felder:
    - ersteller             # MA-Kürzel

weiterleitung:
  outlook:
    - produktion@schneider-kabelsatzbau.de
  teams_channel: Produktion-NZA
  sharepoint: Formblätter/Ausgefüllt/QM/NZA

# ═══════════════════════════════════════════════════════════════════
# EXCEL-MAPPING
# ═══════════════════════════════════════════════════════════════════

excel_mapping:
  sheet: "FQM04"
  felder:
    nza_id: D4
    reklamationstyp: C5
    datum: G5
    artikel_nr: D6
    betriebsauftrag: G6
    losgroesse: D7
    ausschuss: G7
    verursacher: D8
    kostenstelle: G8
    qa_nummer: D9
    q_nr_kunde: G9
    ersatz_ba: D10
    gutschrift_belastung: G10
    fehler_beschreibung: A14:E16   # Merged Textbereich
    fehler_kategorie: F15          # Dropdown
    bemerkungen: A18:E21           # Merged Textbereich
  tabellen:
    zusaetzliche_taetigkeiten:
      start_zeile: 26
      end_zeile: 30
      spalten:
        prozess: B
        werker: E
        kostenstelle: F
        zeit_min: G
    zusaetzliches_material:
      start_zeile: 37
      end_zeile: 41
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
    pattern: "^NZA-\\d{4}-\\d{3}$"
    beispiel: "NZA-2025-001"
    auto_generate: true
    
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

## 📋 Formular-Header

| Feld | Wert |
|------|------|
| **NZA-ID** | {{nza_id*}} |
| **Datum** | {{datum*}} |

---

## 📊 Reklamations-Daten

| Feld | Wert |
|------|------|
| **Reklamationstyp** | {{reklamationstyp*}} |
| **Artikel-Nr.** | {{artikel_nr*}} |
| **Betriebsauftrag** | {{betriebsauftrag}} |
| **Losgröße** | {{losgroesse*}} |
| **Ausschuss** | {{ausschuss*}} |
| **Verursacher** | {{verursacher*}} |
| **Kostenstelle** | {{kostenstelle*}} |

---

## 🔗 Verknüpfungen

| Feld | Wert |
|------|------|
| **QA-Nummer** | {{qa_nummer}} |
| **Q-Nr. Kunde** | {{q_nr_kunde}} |
| **Ersatz BA** | {{ersatz_ba}} |
| **Gutschrift/Belastung** | {{gutschrift_belastung}} |

---

## ⚠️ Fehler

### Fehler Beschreibung
{{fehler_beschreibung*}}

### Fehler Kategorie
**{{fehler_kategorie*}}**

Optionen:
- ☐ Crimpfehler
- ☐ Längenabweichung
- ☐ Verdrahtungsfehler
- ☐ Bearbeitungsfehler
- ☐ Druck fehlerhaft
- ☐ Arbeitsanweisung falsch
- ☐ Kundenzeichnung falsch
- ☐ Falsches Material
- ☐ Materialfehler
- ☐ Werkzeug/Maschinenfehler
- ☐ Lieferantenfehler/Reklamation

---

## 📝 Bemerkungen

{{bemerkungen}}

---

## 🔧 Zusätzliche Tätigkeiten

| # | Prozess | Werker | Kostenstelle | Zeit (Min.) |
|---|---------|--------|--------------|-------------|
| (1) | {{taetigkeit_1_prozess}} | {{taetigkeit_1_werker}} | {{taetigkeit_1_kst}} | {{taetigkeit_1_zeit}} |
| (2) | {{taetigkeit_2_prozess}} | {{taetigkeit_2_werker}} | {{taetigkeit_2_kst}} | {{taetigkeit_2_zeit}} |
| (3) | {{taetigkeit_3_prozess}} | {{taetigkeit_3_werker}} | {{taetigkeit_3_kst}} | {{taetigkeit_3_zeit}} |
| (4) | {{taetigkeit_4_prozess}} | {{taetigkeit_4_werker}} | {{taetigkeit_4_kst}} | {{taetigkeit_4_zeit}} |
| (5) | {{taetigkeit_5_prozess}} | {{taetigkeit_5_werker}} | {{taetigkeit_5_kst}} | {{taetigkeit_5_zeit}} |

**Gesamt-Zeit:** {{gesamt_zeit_min}} Minuten

---

## 📦 Zusätzliches Material

| # | Artikel-Nummer | Artikel-Bezeichnung | Menge | Einheit |
|---|----------------|---------------------|-------|---------|
| (1) | {{material_1_artnr}} | {{material_1_bez}} | {{material_1_menge}} | {{material_1_einheit}} |
| (2) | {{material_2_artnr}} | {{material_2_bez}} | {{material_2_menge}} | {{material_2_einheit}} |
| (3) | {{material_3_artnr}} | {{material_3_bez}} | {{material_3_menge}} | {{material_3_einheit}} |
| (4) | {{material_4_artnr}} | {{material_4_bez}} | {{material_4_menge}} | {{material_4_einheit}} |
| (5) | {{material_5_artnr}} | {{material_5_bez}} | {{material_5_menge}} | {{material_5_einheit}} |

---

## ✍️ Erstellt von

| Ersteller | Datum |
|-----------|-------|
| {{ersteller}} | {{datum}} |

---

*Formblatt-ID: F-QM-04 | Version: 1.0 | Stand: 2025-12-21*  
*Erstellt durch OSP-System | Schneider Kabelsatzbau*
