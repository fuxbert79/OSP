---
formblatt_id: F_QM_14
titel: Korrekturmaßnahme (Interner 8D-Light)
version: 2.0
stand: 2025-12-21
bereich: QM
kategorie: Korrekturmaßnahme / Internes Audit / CAPA
sprache: DE
basis: 8D-Methodik (vereinfacht)

# ═══════════════════════════════════════════════════════════════════
# KONZEPT: 8D-LIGHT FÜR INTERNE ZWECKE
# ═══════════════════════════════════════════════════════════════════
#
# Dieses Formular vereint:
# - Klassische Korrekturmaßnahme (Audit, NC, Verbesserung)
# - Vereinfachte 8D-Methodik für interne Abweichungen
# - CAPA-Ansatz (Corrective and Preventive Action)
#
# 8D-Mapping:
# - D2 = Festgestellte Abweichung
# - D4 = Ursachenanalyse (NEU hinzugefügt)
# - D5 = Vorgesehene Korrekturmaßnahmen
# - D6 = Durchgeführte Korrekturmaßnahmen
# - D7 = Wirksamkeitsprüfung
#
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════
# FELD-DEFINITIONEN
# ═══════════════════════════════════════════════════════════════════

pflichtfelder:
  - km_nr                   # Format: KM-YYYY-NNN (auto-generiert)
  - abteilung               # Enum aus Kostenstellen
  - verantwortlicher        # MA-Kürzel (gegen HR_CORE validieren)
  - audit_leiter_qm         # MA-Kürzel QM
  - abweichung_beschreibung # Min. 30 Zeichen
  - massnahmen_geplant      # Min. 20 Zeichen
  - termin_geplant          # Datum

optionalfelder:
  - quelle                  # Woher kommt die Abweichung?
  - schweregrad             # Kritisch, Major, Minor
  - ursache_beschreibung    # Ursachenanalyse (8D-D4)
  - ursache_kategorie       # Enum Ursachenkategorie
  - massnahmen_durchgefuehrt # Tatsächlich durchgeführt
  - termin_durchgefuehrt    # Datum Durchführung
  - wirksamkeit_beschreibung # Wirksamkeitsprüfung
  - wirksamkeit_bewertung   # Enum: Wirksam/Teilweise/Nicht wirksam
  - verknuepfung_qa         # Link zu QA-Nummer
  - verknuepfung_nza        # Link zu NZA-Nummer
  - folgemassnahme          # Falls Wirksamkeit nicht gegeben

# ═══════════════════════════════════════════════════════════════════
# ENUM-OPTIONEN
# ═══════════════════════════════════════════════════════════════════

quelle_optionen:
  - Internes Audit
  - Externes Audit (Kunde)
  - Externes Audit (Zertifizierung)
  - Prozessbeobachtung
  - Kundenreklamation
  - Lieferantenreklamation
  - Mitarbeiterhinweis
  - Management Review
  - Selbstprüfung
  - Sonstiges

schweregrad_optionen:
  - Kritisch               # Sofortmaßnahme erforderlich
  - Major                  # Zeitnahe Korrektur erforderlich
  - Minor                  # Verbesserungspotenzial
  - Hinweis                # Empfehlung

abteilung_optionen:
  - Fertigung F1 (1000)
  - Fertigung F2 (2000)
  - Fertigung F3 (3000)
  - Prüffeld (5000)
  - Lager
  - Einkauf
  - Vertrieb
  - Verwaltung
  - QM
  - Technik
  - Geschäftsführung

ursache_kategorie_optionen:
  - Mensch                 # Schulung, Erfahrung, Aufmerksamkeit
  - Maschine               # Wartung, Verschleiß, Einstellung
  - Material               # Qualität, Spezifikation
  - Methode                # Arbeitsanweisung, Prozess
  - Milieu                 # Umgebung, Organisation
  - Messung                # Prüfmittel, Toleranz

wirksamkeit_bewertung_optionen:
  - Wirksam                # Abweichung behoben, kein Wiederauftreten
  - Teilweise wirksam      # Verbesserung, aber weiterer Handlungsbedarf
  - Nicht wirksam          # Maßnahme hat nicht gegriffen
  - Noch offen             # Wirksamkeitsprüfung steht aus

status_optionen:
  - Offen                  # Abweichung erfasst
  - In Planung             # Maßnahmen werden geplant
  - In Umsetzung           # Maßnahmen werden durchgeführt
  - Wirksamkeitsprüfung    # Prüfung läuft
  - Abgeschlossen          # Wirksam abgeschlossen
  - Eskaliert              # Wirksamkeit nicht gegeben → Folge-KM

# ═══════════════════════════════════════════════════════════════════
# WORKFLOW-PHASEN (4 Signaturen)
# ═══════════════════════════════════════════════════════════════════

phase_1_erfassung:
  beschreibung: "Abweichung feststellen und dokumentieren"
  felder: [abweichung_beschreibung, quelle, schweregrad]
  signatur: audit_leiter_qm
  8d_mapping: D2

phase_2_analyse_planung:
  beschreibung: "Ursache analysieren und Maßnahmen planen"
  felder: [ursache_beschreibung, ursache_kategorie, massnahmen_geplant, termin_geplant]
  signatur: verantwortlicher
  8d_mapping: D4 + D5

phase_3_umsetzung:
  beschreibung: "Maßnahmen durchführen und dokumentieren"
  felder: [massnahmen_durchgefuehrt, termin_durchgefuehrt]
  signatur: verantwortlicher
  8d_mapping: D6

phase_4_wirksamkeit:
  beschreibung: "Wirksamkeit prüfen und bewerten"
  felder: [wirksamkeit_beschreibung, wirksamkeit_bewertung]
  signatur: audit_leiter_qm
  8d_mapping: D7

# ═══════════════════════════════════════════════════════════════════
# EXCEL-MAPPING (Original + Erweiterungen)
# ═══════════════════════════════════════════════════════════════════

excel_mapping:
  sheet: "Tabelle1"
  original_felder:
    km_nr: B2
    abteilung: B4
    verantwortlicher: B6
    audit_leiter_qm: B8
    abweichung_beschreibung: A12:D18
    datum_erfassung: B19
    signatur_qm_1: D19
    massnahmen_geplant: A22:D28
    termin_geplant: B29
    datum_planung: B32
    signatur_verantwortlicher_1: D32
    massnahmen_durchgefuehrt: A35:D40
    datum_umsetzung: B41
    signatur_verantwortlicher_2: D41
    wirksamkeit_beschreibung: A44:D47
    datum_wirksamkeit: B48
    signatur_qm_2: D48
  # Neue Felder (bei Excel-Erweiterung):
  erweiterung_felder:
    quelle: E2
    schweregrad: E4
    ursache_beschreibung: A50:D55
    ursache_kategorie: E50
    wirksamkeit_bewertung: E44

# ═══════════════════════════════════════════════════════════════════
# VALIDIERUNGSREGELN
# ═══════════════════════════════════════════════════════════════════

validierung:
  km_nr:
    pattern: "^KM-\\d{4}-\\d{3}$"
    beispiel: "KM-2025-001"
    auto_generate: true
    
  verantwortlicher:
    typ: ma_kuerzel
    validierung: HR_CORE
    
  audit_leiter_qm:
    typ: ma_kuerzel
    validierung: HR_CORE
    berechtigung: "QM-Funktion"
    
  abweichung_beschreibung:
    min_laenge: 30
    max_laenge: 500
    
  massnahmen_geplant:
    min_laenge: 20
    max_laenge: 500
    
  termin_geplant:
    typ: datum
    constraint: ">= heute"
    
  wirksamkeit_bewertung:
    pflicht_wenn: "status == Wirksamkeitsprüfung"

signatur:
  erforderlich: true
  anzahl: 4
  felder:
    - signatur_qm_erfassung
    - signatur_verantwortlicher_planung
    - signatur_verantwortlicher_umsetzung
    - signatur_qm_wirksamkeit

weiterleitung:
  outlook:
    - qm@schneider-kabelsatzbau.de
  teams_channel: QM-Korrekturmaßnahmen
  sharepoint: Formblätter/Ausgefüllt/QM/Korrekturmaßnahmen

---

# F-QM-14 Korrekturmaßnahme (Interner 8D-Light)

## 📋 Header

| Feld | Wert |
|------|------|
| **KM-Nr.** | {{km_nr*}} |
| **Status** | {{status}} |
| **Quelle** | {{quelle}} |
| **Schweregrad** | {{schweregrad}} |

---

## 🏢 Zuständigkeiten

| Feld | Wert |
|------|------|
| **Abteilung** | {{abteilung*}} |
| **Verantwortlicher** | {{verantwortlicher*}} |
| **Audit-Leiter / QM** | {{audit_leiter_qm*}} |

---

## 🔗 Verknüpfungen

| Feld | Wert |
|------|------|
| **QA-Nummer** | {{verknuepfung_qa}} |
| **NZA-Nummer** | {{verknuepfung_nza}} |

---

## ═══════════════════════════════════════════════════════════════════
## PHASE 1: ABWEICHUNG ERFASSEN (≙ 8D-D2)
## ═══════════════════════════════════════════════════════════════════

### ⚠️ Festgestellte Abweichung

{{abweichung_beschreibung*}}

---

### ✍️ Signatur Phase 1

| Datum | Unterschrift QM |
|-------|-----------------|
| {{datum_erfassung}} | {{signatur_qm_erfassung}} |

---

## ═══════════════════════════════════════════════════════════════════
## PHASE 2: URSACHE & PLANUNG (≙ 8D-D4 + D5)
## ═══════════════════════════════════════════════════════════════════

### 🔍 Ursachenanalyse (NEU - 8D-D4 Light)

**Ursachenkategorie:** {{ursache_kategorie}}

{{ursache_beschreibung}}

> 💡 **Tipp:** Nutzen Sie die 5-Why-Methode oder prüfen Sie die 6M:
> Mensch | Maschine | Material | Methode | Milieu | Messung

---

### 📋 Vorgesehene Korrekturmaßnahmen

{{massnahmen_geplant*}}

| Feld | Wert |
|------|------|
| **Geplantes Erledigungsdatum** | {{termin_geplant*}} |

---

### ✍️ Signatur Phase 2

| Datum | Unterschrift Verantwortlicher |
|-------|-------------------------------|
| {{datum_planung}} | {{signatur_verantwortlicher_planung}} |

---

## ═══════════════════════════════════════════════════════════════════
## PHASE 3: UMSETZUNG (≙ 8D-D6)
## ═══════════════════════════════════════════════════════════════════

### ✅ Durchgeführte Korrekturmaßnahmen

{{massnahmen_durchgefuehrt}}

| Feld | Wert |
|------|------|
| **Tatsächliches Erledigungsdatum** | {{termin_durchgefuehrt}} |

---

### ✍️ Signatur Phase 3

| Datum | Unterschrift Verantwortlicher |
|-------|-------------------------------|
| {{datum_umsetzung}} | {{signatur_verantwortlicher_umsetzung}} |

---

## ═══════════════════════════════════════════════════════════════════
## PHASE 4: WIRKSAMKEIT (≙ 8D-D7)
## ═══════════════════════════════════════════════════════════════════

### 📊 Wirksamkeitsprüfung

**Bewertung:** {{wirksamkeit_bewertung}}

| Bewertung | Bedeutung |
|-----------|-----------|
| ✅ Wirksam | Abweichung behoben, kein Wiederauftreten erwartet |
| ⚠️ Teilweise wirksam | Verbesserung erkennbar, weiterer Handlungsbedarf |
| ❌ Nicht wirksam | Maßnahme hat nicht gegriffen → Folge-KM erforderlich |

{{wirksamkeit_beschreibung}}

---

### 📌 Folge-Maßnahme (falls nicht wirksam)

{{folgemassnahme}}

---

### ✍️ Signatur Phase 4

| Datum | Unterschrift QM |
|-------|-----------------|
| {{datum_wirksamkeit}} | {{signatur_qm_wirksamkeit}} |

---

## 📊 Zusammenfassung

| Phase | Status | Datum | Signatur |
|-------|--------|-------|----------|
| 1. Erfassung | {{status_phase_1}} | {{datum_erfassung}} | {{signatur_qm_erfassung}} |
| 2. Planung | {{status_phase_2}} | {{datum_planung}} | {{signatur_verantwortlicher_planung}} |
| 3. Umsetzung | {{status_phase_3}} | {{datum_umsetzung}} | {{signatur_verantwortlicher_umsetzung}} |
| 4. Wirksamkeit | {{status_phase_4}} | {{datum_wirksamkeit}} | {{signatur_qm_wirksamkeit}} |

---

*Formblatt-ID: F-QM-14 | Version: 2.0 (8D-Light) | Stand: 2025-12-21*  
*Erstellt durch OSP-System | Schneider Kabelsatzbau*
