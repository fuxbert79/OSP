---
formblatt_id: F_QM_02
titel: Qualitätsabweichung / Quality Deviation
version: 1.0
stand: 2025-12-21
bereich: QM
kategorie: Reklamation
sprache: DE/EN (bilingual)

# ═══════════════════════════════════════════════════════════════════
# FELD-DEFINITIONEN
# ═══════════════════════════════════════════════════════════════════

pflichtfelder:
  - abweichungs_nr        # Format: QA-YYYY-NNN
  - datum                 # ISO-Format: YYYY-MM-DD
  - lieferant_firma       # Freitext
  - lieferant_ansprechpartner  # Freitext
  - artikel_nr_schneider  # Schneider-Artikelnummer
  - artikel_bezeichnung   # Freitext
  - lieferschein_nr       # Freitext
  - lieferdatum           # ISO-Format
  - liefermenge           # Numerisch + Einheit
  - beanstandungsmenge    # Numerisch + Einheit
  - beschreibung_abweichung  # Freitext (min. 50 Zeichen)
  - massnahmen_optionen   # Array von Checkbox-Werten

optionalfelder:
  - artikel_nr_lieferant  # Lieferanten-Artikelnummer
  - kontakt_telefon       # Lieferanten-Telefon
  - kontakt_email         # Lieferanten-Email
  - bilder                # Array von Bild-URLs/Pfaden

massnahmen_optionen:      # Mindestens 1 auswählen
  - untersuchung_abstellen    # "Untersuchen Sie Ihren Prozess und stellen Sie die Mängel ab"
  - untersuchung_8d           # "Untersuchen Sie Ihren Prozess mittels 8D-Report"
  - ersatzlieferung           # "Wir benötigen schnellstmöglich eine Ersatzlieferung"
  - ruecksendung_nacharbeit   # "Wir senden die Artikel zur Nacharbeit zurück"
  - gutschrift                # "Wir benötigen eine Gutschrift"

signatur:
  erforderlich: true
  felder:
    - ersteller           # MA-Kürzel des Erstellers
    - freigabe_qm         # Optional: QM-Freigabe

weiterleitung:
  outlook:
    - qm@schneider-kabelsatzbau.de
    - einkauf@schneider-kabelsatzbau.de
  teams_channel: QM-Reklamationen
  sharepoint: Formblätter/Ausgefüllt/QM/Qualitätsabweichungen

excel_mapping:
  sheet: "Seite 1"
  felder:
    abweichungs_nr: I1
    datum: I3
    lieferant_firma: A17:E19     # Merged
    lieferant_ansprechpartner: G17:I19  # Merged
    artikel_nr_schneider: E23
    artikel_nr_lieferant: E24
    artikel_bezeichnung: E25
    lieferschein_nr: E26
    lieferdatum: E27
    liefermenge: E28
    beanstandungsmenge: E29
    beschreibung_abweichung: A33:I42  # Großes Textfeld
  checkboxen:
    untersuchung_abstellen: A47
    untersuchung_8d: A48
    ersatzlieferung: A50
    ruecksendung_nacharbeit: A51
    gutschrift: A52

# ═══════════════════════════════════════════════════════════════════
# VALIDIERUNGSREGELN
# ═══════════════════════════════════════════════════════════════════

validierung:
  abweichungs_nr:
    pattern: "^QA-\\d{4}-\\d{3}$"
    beispiel: "QA-2025-001"
    auto_generate: true
    
  datum:
    typ: datum
    format: "YYYY-MM-DD"
    default: "{{HEUTE}}"
    
  liefermenge:
    typ: numerisch_mit_einheit
    beispiel: "1000 Stk"
    
  beanstandungsmenge:
    typ: numerisch_mit_einheit
    constraint: "<= liefermenge"
    
  beschreibung_abweichung:
    min_laenge: 50
    max_laenge: 2000
    
  massnahmen_optionen:
    min_auswahl: 1
    max_auswahl: 5

---

# F-QM-02 Qualitätsabweichung / Quality Deviation

## 📋 Formular-Header

| Feld | Wert |
|------|------|
| **Abweichungs-Nr.** | {{abweichungs_nr*}} |
| **Datum** | {{datum*}} |

---

## 🏢 Absender (vorausgefüllt)

| Feld | Wert |
|------|------|
| **Firma** | Rainer Schneider Kabelsatzbau & Konfektions GmbH & Co. KG |
| **Adresse** | Alte Hütte 3, 57537 Wissen |
| **Ansprechpartner** | Andreas Löhr, Qualitätsmanager |
| **Telefon** | +49 2742 9336-28 |
| **Email** | a.loehr@schneider-kabelsatzbau.de |

---

## 📦 Lieferant / Supplier

| Feld | Wert |
|------|------|
| **Firma** | {{lieferant_firma*}} |
| **Ansprechpartner** | {{lieferant_ansprechpartner*}} |
| **Telefon** | {{kontakt_telefon}} |
| **Email** | {{kontakt_email}} |

---

## 📝 Artikeldaten / Part Data

| Feld | Wert |
|------|------|
| **Artikel Nr. Schneider** | {{artikel_nr_schneider*}} |
| **Artikel Nr. Lieferant** | {{artikel_nr_lieferant}} |
| **Artikel Bezeichnung** | {{artikel_bezeichnung*}} |
| **Lieferschein Nr.** | {{lieferschein_nr*}} |
| **Lieferdatum** | {{lieferdatum*}} |
| **Liefermenge** | {{liefermenge*}} |
| **Beanstandungsmenge** | {{beanstandungsmenge*}} |

---

## ⚠️ Beschreibung der Qualitätsabweichung / Description of Quality Deviation

{{beschreibung_abweichung*}}

---

## ✅ Geforderte Maßnahmen / Required Actions

Wir bitten um Stellungnahme und fordern Sie zur Nachbesserung auf:

| Auswahl | Maßnahme |
|---------|----------|
| {{☐ untersuchung_abstellen}} | Untersuchen Sie Ihren Prozess und stellen Sie die Mängel ab |
| {{☐ untersuchung_8d}} | Untersuchen Sie Ihren Prozess mittels 8D-Report |
| {{☐ ersatzlieferung}} | Wir benötigen schnellstmöglich eine Ersatzlieferung |
| {{☐ ruecksendung_nacharbeit}} | Wir senden die Artikel zur Nacharbeit zurück |
| {{☐ gutschrift}} | Wir benötigen eine Gutschrift |

---

## 📷 Bilder zur Qualitätsabweichung (Seite 2-3)

{{bilder}}

---

## ✍️ Unterschriften / Signatures

| Rolle | Name | Datum | Signatur |
|-------|------|-------|----------|
| **Ersteller** | {{ersteller*}} | {{datum_ersteller}} | ✓ {{ersteller}} |
| **QM-Freigabe** | {{freigabe_qm}} | {{datum_freigabe}} | {{sig_freigabe}} |

---

## 📤 Weiterleitung / Distribution

- [ ] Email an Lieferant
- [ ] Kopie an Einkauf (TS)
- [ ] Ablage in SharePoint
- [ ] Teams-Benachrichtigung

---

*Formblatt-ID: F-QM-02 | Version: 1.0 | Stand: 2025-12-21*  
*Erstellt durch OSP-System | Schneider Kabelsatzbau*
