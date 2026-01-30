---
formblatt_id: F_QM_03
titel: Fehleranalyse 8D-Report
version: 1.0
stand: 2025-12-21
bereich: QM
kategorie: Reklamation / Problemlösung
sprache: DE/EN (bilingual)
methodik: 8D (Eight Disciplines Problem Solving)

# ═══════════════════════════════════════════════════════════════════
# FELD-DEFINITIONEN
# ═══════════════════════════════════════════════════════════════════

pflichtfelder:
  - vorgangs_nr            # Format: QA-YYYY-NNN (Verknüpfung zu F-QM-02)
  - status                 # Enum: Eröffnet, In Bearbeitung, Abgeschlossen
  - verfasser              # Name des Erstellers
  - verfasser_telefon      # Kontakt-Telefon
  - verfasser_email        # Kontakt-Email
  - lieferant_kunde        # Firmenname (Lieferant oder Kunde)
  - d2_problembeschreibung # Detaillierte Fehlerbeschreibung (min. 50 Zeichen)
  - d4_fehlerursache       # Root Cause Analyse (min. 30 Zeichen)

optionalfelder:
  - kunde_nr               # Kundennummer
  - artikel_nr             # Artikelnummer
  - artikel_bezeichnung    # Artikelbezeichnung
  - lieferschein_nr        # Lieferscheinnummer
  - lieferdatum            # Datum der Lieferung
  - menge_geliefert        # Gesamtmenge
  - menge_reklamiert       # Reklamierte Menge
  - reklamations_nr        # Externe Reklamationsnummer
  - d1_team                # Bearbeitungsteam (Array)
  - d3_sofortmassnahmen    # Sofortmaßnahmen (Array mit Wer/Wann)
  - d5_geplante_massnahmen # Geplante Abstellmaßnahmen (Array)
  - d6_eingefuehrte_massnahmen  # Eingeführte Maßnahmen (Array)
  - d7_praevention         # Präventionsmaßnahmen (Array)
  - d8_abschluss           # Abschluss-Kommentar

# ═══════════════════════════════════════════════════════════════════
# STATUS-OPTIONEN
# ═══════════════════════════════════════════════════════════════════

status_optionen:
  - Eröffnet / Open
  - In Bearbeitung / In Progress
  - Abgeschlossen / Closed

# ═══════════════════════════════════════════════════════════════════
# 8D-STRUKTUR
# ═══════════════════════════════════════════════════════════════════

d1_team:
  beschreibung: "Bearbeitungsteam / Editors"
  max_eintraege: 5
  felder:
    - name                 # Name des Teammitglieds
    - funktion             # Rolle/Position

d3_sofortmassnahmen:
  beschreibung: "Sofortmaßnahmen / Containment Actions"
  max_eintraege: 5
  felder:
    - massnahme            # Beschreibung der Maßnahme
    - wer                  # Verantwortlicher (MA-Kürzel)
    - wann                 # Termin (Datum)

d5_geplante_massnahmen:
  beschreibung: "Geplante Abstellmaßnahmen / Planned Corrective Actions"
  max_eintraege: 5
  felder:
    - massnahme            # Beschreibung
    - wer                  # Verantwortlicher
    - wann                 # Termin

d6_eingefuehrte_massnahmen:
  beschreibung: "Eingeführte Abstellmaßnahmen / Implemented Corrective Actions"
  max_eintraege: 5
  felder:
    - massnahme            # Beschreibung
    - wer                  # Verantwortlicher
    - wann                 # Umsetzungsdatum

d7_praevention:
  beschreibung: "Fehlerwiederholung verhindern / Prevent Error Recurrence"
  max_eintraege: 5
  felder:
    - massnahme            # Präventionsmaßnahme
    - wer                  # Verantwortlicher
    - wann                 # Termin

signatur:
  erforderlich: true
  felder:
    - verfasser            # Ersteller/Verfasser
    - ort                  # Ort (Standard: Wissen)
    - datum                # Abschlussdatum

weiterleitung:
  outlook:
    - qm@schneider-kabelsatzbau.de
  cc_lieferant: true       # Automatisch an Lieferanten-Email
  teams_channel: QM-8D-Reports
  sharepoint: Formblätter/Ausgefüllt/QM/8D-Reports

# ═══════════════════════════════════════════════════════════════════
# EXCEL-MAPPING
# ═══════════════════════════════════════════════════════════════════

excel_mapping:
  sheet: "8D"
  felder:
    status: A3
    vorgangs_nr: D4
    verfasser: D5
    verfasser_telefon: D6
    verfasser_email: D7
    lieferant_kunde: A10:C16      # Merged Bereich
    kunde_nr: B17
    artikel_nr: E10
    artikel_bezeichnung: E12
    lieferschein_nr: E15
    lieferdatum: E17
    menge_geliefert: H10
    menge_reklamiert: H12
    reklamations_nr: H14
  d_schritte:
    d1_team:
      bereich: A20:C22
    d2_problembeschreibung:
      bereich: A24:H28
    d3_sofortmassnahmen:
      bereich: A30:E33
      wer: F30:F33
      wann: G30:G33
    d4_fehlerursache:
      bereich: A35:H38
    d5_geplante_massnahmen:
      bereich: A40:F43
      wer: G40:G43
      wann: H40:H43
    d6_eingefuehrte_massnahmen:
      bereich: A45:E48
      wer: F45:F48
      wann: G45:G48
    d7_praevention:
      bereich: A50:E52
      wer: F50:F52
      wann: G50:G52
    d8_abschluss:
      bereich: A54:H58
  signatur:
    ort: A56
    verfasser: C57
    datum: E57

# ═══════════════════════════════════════════════════════════════════
# VALIDIERUNGSREGELN
# ═══════════════════════════════════════════════════════════════════

validierung:
  vorgangs_nr:
    pattern: "^QA-\\d{4}-\\d{3}$"
    beispiel: "QA-2025-001"
    verknuepfung: "F_QM_02"   # Muss zu bestehender QA passen
    
  verfasser_email:
    typ: email
    pattern: "^[a-z.]+@schneider-kabelsatzbau\\.de$"
    
  d2_problembeschreibung:
    min_laenge: 50
    max_laenge: 1000
    
  d4_fehlerursache:
    min_laenge: 30
    max_laenge: 1000
    methoden_hinweis: "5-Why, Ishikawa, Pareto empfohlen"

---

# F-QM-03 Fehleranalyse 8D-Report

## 📋 Header

| Feld | Wert |
|------|------|
| **Status** | {{status*}} |
| **Vorgangs-Nr.** | {{vorgangs_nr*}} |

---

## 👤 Verfasser / Author

| Feld | Wert |
|------|------|
| **Name** | {{verfasser*}} |
| **Telefon** | {{verfasser_telefon*}} |
| **Email** | {{verfasser_email*}} |

---

## 🏢 Lieferant / Kunde

{{lieferant_kunde*}}

| Feld | Wert |
|------|------|
| **Kd.-Nr.** | {{kunde_nr}} |

---

## 📦 Lieferdaten / Delivery Data

| Feld | Wert |
|------|------|
| **Artikel-Nr.** | {{artikel_nr}} |
| **Bezeichnung** | {{artikel_bezeichnung}} |
| **LS-Nr.** | {{lieferschein_nr}} |
| **Lieferdatum** | {{lieferdatum}} |

---

## ⚠️ Reklamationsdaten / Complaint Data

| Feld | Wert |
|------|------|
| **Menge geliefert** | {{menge_geliefert}} |
| **Menge reklamiert** | {{menge_reklamiert}} |
| **Reklamations-Nr.** | {{reklamations_nr}} |

---

## 📊 8D-PROZESS

### D1: Bearbeitungsteam / Editors

| Name | Funktion |
|------|----------|
| {{d1_name_1}} | {{d1_funktion_1}} |
| {{d1_name_2}} | {{d1_funktion_2}} |
| {{d1_name_3}} | {{d1_funktion_3}} |

---

### D2: Problembeschreibung / Problem Description

{{d2_problembeschreibung*}}

---

### D3: Sofortmaßnahmen / Containment Actions

| Maßnahme | Wer | Wann |
|----------|-----|------|
| {{d3_massnahme_1}} | {{d3_wer_1}} | {{d3_wann_1}} |
| {{d3_massnahme_2}} | {{d3_wer_2}} | {{d3_wann_2}} |
| {{d3_massnahme_3}} | {{d3_wer_3}} | {{d3_wann_3}} |

---

### D4: Fehlerursache / Root Cause

{{d4_fehlerursache*}}

> 💡 **Methoden-Empfehlung:** 5-Why-Analyse, Ishikawa-Diagramm, Pareto-Analyse

---

### D5: Geplante Abstellmaßnahmen / Planned Corrective Actions

| Maßnahme | Wer | Wann |
|----------|-----|------|
| {{d5_massnahme_1}} | {{d5_wer_1}} | {{d5_wann_1}} |
| {{d5_massnahme_2}} | {{d5_wer_2}} | {{d5_wann_2}} |
| {{d5_massnahme_3}} | {{d5_wer_3}} | {{d5_wann_3}} |

---

### D6: Eingeführte Abstellmaßnahmen / Implemented Corrective Actions

| Maßnahme | Wer | Wann |
|----------|-----|------|
| {{d6_massnahme_1}} | {{d6_wer_1}} | {{d6_wann_1}} |
| {{d6_massnahme_2}} | {{d6_wer_2}} | {{d6_wann_2}} |
| {{d6_massnahme_3}} | {{d6_wer_3}} | {{d6_wann_3}} |

---

### D7: Fehlerwiederholung verhindern / Prevent Error Recurrence

| Maßnahme | Wer | Wann |
|----------|-----|------|
| {{d7_massnahme_1}} | {{d7_wer_1}} | {{d7_wann_1}} |
| {{d7_massnahme_2}} | {{d7_wer_2}} | {{d7_wann_2}} |
| {{d7_massnahme_3}} | {{d7_wer_3}} | {{d7_wann_3}} |

---

### D8: Abschluss / Conclusion

{{d8_abschluss}}

---

## ✍️ Unterschrift / Signature

| Ort | Datum | Verfasser |
|-----|-------|-----------|
| {{ort}} | {{datum_abschluss}} | {{verfasser}} |

---

*Formblatt-ID: F-QM-03 | Version: 1.0 | Stand: 2025-12-21*  
*Erstellt durch OSP-System | Schneider Kabelsatzbau*
