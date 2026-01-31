# NZA SharePoint-Listen Spezifikation

**Site:** /sites/NZA_NEU
**Erstellt:** 2026-01-30
**Status:** Zur Erstellung bereit

---

## 1. Hauptliste: nza-kpl (52 Felder)

### 1.1 Stammdaten (17 Felder)

| # | Display Name | Internal Name | Feldtyp | Pflicht | Beschreibung |
|---|--------------|---------------|---------|---------|--------------|
| 1 | NZA-ID | Title | Text | Ja | Automatisch: NZA-JJ-XXXX |
| 2 | Reklamationstyp | field_1 | Choice | Ja | Interne Reklamation, Kunden Reklamation, Lieferanten Reklamation |
| 3 | Datum | field_2 | DateTime | Ja | Erfassungsdatum |
| 4 | Artikel-Nr. | field_3 | Text | Ja | Betroffener Artikel |
| 5 | Betriebsauftrag | field_4 | Number | Nein | 6-stellig |
| 6 | Prüfmenge | field_5 | Number | Nein | Geprüfte Stückzahl |
| 7 | davon n.i.O. | field_6 | Number | Nein | Ausschuss-Menge |
| 8 | Verursacher | field_7 | Text | Nein | Name des Verursachers |
| 9 | Verursacher Personal-Nr. | field_8 | Number | Nein | Personalnummer |
| 10 | Kostenstelle | field_9 | Choice | Ja | 1000, 2000, 3000, 4000, 5000, Lager, Verwaltung, Lieferant, keine Zuordnung |
| 11 | QA-Nummer | field_10 | Number | Nein | RMS-Bezug (falls vorhanden) |
| 12 | Q-Nr. Kunde/Lieferant | field_11 | Text | Nein | Externe Referenz |
| 13 | Ersatz BA | field_12 | Number | Nein | Ersatz-Betriebsauftrag |
| 14 | Gutschrift/Belastung | field_13 | Text | Nein | Finanzielle Abwicklung |
| 15 | Fehler Beschreibung | field_14 | Note | Ja | Detaillierte Fehlerbeschreibung |
| 16 | Fehler Kategorie | field_15 | MultiChoice | Ja | Crimpfehler, Längenabweichung, Verdrahtungsfehler, etc. |
| 17 | Bemerkungen | field_16 | Note | Nein | Zusätzliche Notizen |

### 1.2 Prozess-Felder (5 Prozesse × 6 Felder = 30 Felder)

Für jeden Prozess (1-5):

| Feldtyp | Prozess 1 | Prozess 2 | Prozess 3 | Prozess 4 | Prozess 5 |
|---------|-----------|-----------|-----------|-----------|-----------|
| Prozess (Text) | field_19 | field_24 | field_29 | field_34 | field_39 |
| Werker (Text) | field_20 | field_25 | field_30 | field_35 | field_40 |
| Kostenstelle (Choice) | kostenstelle_1 | kostenstelle_2 | kostenstelle_3 | kostenstelle_4 | kostenstelle_5 |
| Zeit in Min (Number) | field_22 | field_27 | field_32 | field_37 | field_42 |
| Faktor (Calculated) | kostenstelle_1_faktor | kostenstelle_2_faktor | kostenstelle_3_faktor | kostenstelle_4_faktor | kostenstelle_5_faktor |
| Kosten (Calculated) | kosten_1 | kosten_2 | kosten_3 | kosten_4 | kosten_5 |

### 1.3 Material/Kosten-Felder (5 Felder)

| # | Display Name | Internal Name | Feldtyp | Beschreibung |
|---|--------------|---------------|---------|--------------|
| 48 | kosten_sonstige | field_17 | Currency | Sonstige Kosten |
| 49 | kosten_material | field_65 | Currency | Materialkosten gesamt |
| 50 | kosten_prozesse | kosten_prozesse_neu | Calculated | Summe Prozess 1-5 |
| 51 | kosten_gesamt | kosten_gesamt_neu | Calculated | Prozesse + Material + Sonstige |
| 52 | Status | status | Choice | Neu, In Bearbeitung, Abgeschlossen |

### 1.4 Berechnete Felder (Calculated)

```
kostenstelle_X_faktor =
  IF(kostenstelle_X="1000", 1.98,
  IF(kostenstelle_X="2000", 1.21,
  IF(kostenstelle_X="3000", 0.93,
  IF(kostenstelle_X="4000", 1.02,
  IF(kostenstelle_X="5000", 1.02,
  IF(kostenstelle_X="Lager", 1.10,
  IF(kostenstelle_X="Verwaltung", 1.37, 0)))))))

kosten_X = field_XX (Zeit) * kostenstelle_X_faktor

kosten_prozesse_neu = kosten_1 + kosten_2 + kosten_3 + kosten_4 + kosten_5

kosten_gesamt_neu = kosten_prozesse_neu + field_65 + field_17
```

---

## 2. nza-massnahmen (13 Felder)

| # | Display Name | Internal Name | Feldtyp | Beschreibung |
|---|--------------|---------------|---------|--------------|
| 1 | Title | Title | Text | Maßnahmen-Titel |
| 2 | NZA_ID | NZA_ID | Text | Referenz zur Hauptliste |
| 3 | Massnahme_Typ | Massnahme_Typ | Choice | Sofortmaßnahme, Korrekturmaßnahme, Vorbeugemaßnahme |
| 4 | Beschreibung | Beschreibung | Note | Maßnahmenbeschreibung |
| 5 | Verantwortlich_ID | Verantwortlich_ID | Text | M365-User-ID |
| 6 | Verantwortlich_Name | Verantwortlich_Name | Text | Anzeigename |
| 7 | Verantwortlich_Email | Verantwortlich_Email | Text | E-Mail-Adresse |
| 8 | Termin | Termin | Date | Fälligkeitsdatum |
| 9 | Status | Status | Choice | Offen, In Bearbeitung, Abgeschlossen, Überfällig |
| 10 | Erledigt_Am | Erledigt_Am | Date | Abschlussdatum |
| 11 | Wirksamkeit | Wirksamkeit | Choice | Nicht geprüft, Wirksam, Nicht wirksam |
| 12 | Benachrichtigung_Teams | Benachrichtigung_Teams | Boolean | Teams-Nachricht gesendet? |
| 13 | Benachrichtigung_Email | Benachrichtigung_Email | Boolean | E-Mail gesendet? |

---

## 3. nza-bilder (8 Felder)

| # | Display Name | Internal Name | Feldtyp | Beschreibung |
|---|--------------|---------------|---------|--------------|
| 1 | Title | Title | Text | Bildbeschreibung |
| 2 | NZA_ID | NZA_ID | Text | Referenz zur Hauptliste |
| 3 | Bild_URL | Bild_URL | URL | SharePoint-Link zum Bild |
| 4 | Bild_Thumbnail | Bild_Thumbnail | URL | Thumbnail-URL |
| 5 | Hochgeladen_Von | Hochgeladen_Von | Text | Uploader |
| 6 | Hochgeladen_Am | Hochgeladen_Am | DateTime | Upload-Zeitstempel |
| 7 | Kategorie | Kategorie | Choice | Fehlerbild, Vorher, Nachher, Dokumentation |
| 8 | Bemerkung | Bemerkung | Text | Zusätzliche Notizen |

---

## 4. nza-mitarbeiter (9 Felder)

| # | Display Name | Internal Name | Feldtyp | Beschreibung |
|---|--------------|---------------|---------|--------------|
| 1 | Name | Title | Text | Vollständiger Name |
| 2 | Kuerzel | Kuerzel | Text | 2-3 Buchstaben (z.B. "MD") |
| 3 | Personalnummer | Personalnummer | Text | Personal-Nr. |
| 4 | Abteilung | Abteilung | Choice | Verwaltung, 1000, 2000, 3000, 5000, Lager |
| 5 | KST | KST | Text | Kostenstelle |
| 6 | Funktion | Funktion | Text | Stellenbezeichnung |
| 7 | Email | Email | Text | E-Mail-Adresse (falls vorhanden) |
| 8 | Aktiv | Aktiv | Boolean | Noch beschäftigt? |
| 9 | OSP_User | OSP_User | Boolean | Hat OSP-Zugang? |

**Import-Quelle:** `/mnt/HC_Volume_104189729/osp/nza/daten/nza_mitarbeiter.csv`

---

## 5. nza-config (5 Felder)

| # | Display Name | Internal Name | Feldtyp | Beschreibung |
|---|--------------|---------------|---------|--------------|
| 1 | Key | Title | Text | Config-Schlüssel |
| 2 | Wert | Wert | Text | Config-Wert |
| 3 | Typ | Typ | Choice | String, Number, Boolean, JSON |
| 4 | Beschreibung | Beschreibung | Text | Erklärung |
| 5 | Gruppe | Gruppe | Choice | System, Kosten, Benachrichtigung, UI |

### Initiale Config-Werte

| Key | Wert | Typ | Gruppe |
|-----|------|-----|--------|
| NZA_ID_COUNTER | 0 | Number | System |
| NZA_ID_YEAR | 26 | Number | System |
| MINUTENSATZ_1000 | 1.98 | Number | Kosten |
| MINUTENSATZ_2000 | 1.21 | Number | Kosten |
| MINUTENSATZ_3000 | 0.93 | Number | Kosten |
| MINUTENSATZ_4000 | 1.02 | Number | Kosten |
| MINUTENSATZ_5000 | 1.02 | Number | Kosten |
| MINUTENSATZ_LAGER | 1.10 | Number | Kosten |
| MINUTENSATZ_VERWALTUNG | 1.37 | Number | Kosten |
| TEAMS_NOTIFY_ENABLED | true | Boolean | Benachrichtigung |
| EMAIL_NOTIFY_ENABLED | true | Boolean | Benachrichtigung |

---

## 6. nza-kpis (7 Felder)

| # | Display Name | Internal Name | Feldtyp | Beschreibung |
|---|--------------|---------------|---------|--------------|
| 1 | KPI_Name | Title | Text | z.B. "OFFENE_NZA" |
| 2 | Datum | Datum | Date | Berechnungsdatum |
| 3 | Periode | Periode | Choice | Tag, Woche, Monat, Jahr |
| 4 | Wert | Wert | Number | KPI-Wert |
| 5 | Einheit | Einheit | Text | EUR, Stück, %, Stunden |
| 6 | KST | KST | Text | Kostenstelle (optional) |
| 7 | NZA_Typ | NZA_Typ | Text | Reklamationstyp (optional) |

---

## Fehler-Kategorien (field_15 - MultiChoice)

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
- Sonstige

---

## Kostenstellen (Choice-Werte)

- 1000
- 2000
- 3000
- 4000
- 5000
- Lager
- Verwaltung
- Lieferant
- keine Zuordnung

---

*Erstellt: 2026-01-30*
