# F-QM-04 NZA (Nach- und Zusatzarbeiten) - Version 2026

**Formblatt-ID:** F-QM-04
**Version:** 2.0
**Stand:** 2026-02-05
**Anwendung:** Interne Reklamationen / Nacharbeiten

---

## Changelog gegenueber Version 1.0 (fqm04_nza)

| Aenderung | Alt (v1.0) | Neu (v2.0) |
|-----------|------------|------------|
| NZA-ID | Im Formular (D4) | **Nicht im Formular** - wird vom System generiert |
| Material-Zeilen | 5 Zeilen (37-41) | **7 Zeilen** (37-43) |
| Header-Layout | NZA-ID in Zeile 4 | Reklamationstyp in Zeile 4 |
| Fehler-Kategorien | Ohne Zeilenumbruch | Mit Zeilenumbruch im Dropdown |

---

## Dateien in diesem Verzeichnis

| Datei | Beschreibung |
|-------|--------------|
| `FQM04.xlsx` | Excel-Formular (Master) |
| `F_QM_04.md` | Feld-Definitionen und Mapping |
| `F_QM_04_Schema.json` | JSON-Schema fuer Validierung |
| `RMS_Prompt_F_QM_04.md` | KI-Prompt fuer Formular-Assistent |
| `README.md` | Diese Datei |

---

## Typische Anwendungsfaelle

- Produktionsfehler dokumentieren
- Nacharbeit erforderlich
- Ausschuss erfassen
- Prozessabweichungen melden
- Kosten fuer Nach-/Zusatzarbeiten berechnen

---

## Excel-Struktur

### Header (Zeile 4-11)
```
Zeile 4:  Reklamationstyp (C4) | Datum (F4)
Zeile 5:  Artikel-Nr. (C5)     | Betriebsauftrag (F5)
Zeile 6:  Losgroesse (C6)      | Ausschuss (F6)
Zeile 7:  Verursacher (C7)     | Kostenstelle (F7)
Zeile 10: QA-Nr. RMS (C10)     | Q-Nr. Kunde (F10)
Zeile 11: Ersatz BA (C11)      | Gutschrift/Belastung (F11)
```

### Fehler (Zeile 14-21)
```
Zeile 14-20: Fehler Beschreibung (A15:E20, merged)
Zeile 16-20: Fehler Kategorie (G16, Dropdown)
```

### Zusaetzliche Taetigkeiten (Zeile 24-31)
```
5 Zeilen fuer Prozess | Werker | Kostenstelle | Zeit (Min.)
```

### Zusaetzliches Material (Zeile 34-43)
```
7 Zeilen fuer Artikel-Nummer | Artikel-Bezeichnung | Menge | Einheit
```

---

## Integration

### E-Mail-Import
- Postfach: nza@schneider-kabelsatzbau.de
- Credential: Microsoft Outlook NZA
- NZA-ID wird automatisch generiert: NZA-26-XXXX

### SharePoint
- Site: /sites/NZA_NEU
- Liste: nza-kpl (Hauptliste)
- Bilder: nza-bilder

### Dashboard
- URL: https://osp.schneider-kabelsatzbau.de/nza/2026/

---

*Erstellt: 2026-02-05*
*Autor: AL (via Claude Code)*
