# OSP Navigator - Intelligentes Wissens-Routing

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 2.2 | **TAG:** [OSP][NAV] | **Erstellt:** 2025-12-09 | **Aktualisiert:** 2025-12-23 | **Autor:** AL | **Verantwortlich:** AL (QM/KI-Manager) | **Zugriff:** ðŸŸ¢ L1-Ã–ffentlich | **Status:** âœ… PRODUKTIV (RAG) | **KritikalitÃ¤t:** ðŸ”´ SEHR HOCH

**Ã„nderungen v2.2:** Pipeline-Module dokumentiert, 4-Layer-Architektur hinzugefÃ¼gt, RAM-Korrektur (16GB), Embedding-Update (multilingual-e5-large), ChromaDB 1.3.6, Open WebUI 0.6.43

---

## ðŸŽ¯ ZWECK

Diese Datei ist der **zentrale Wegweiser** im OSP-Wissensbestand. Sie hilft dem KI-System bei:
- Zuordnung von Benutzer-Anfragen zu SchlÃ¼ssel-Dateien
- AuflÃ¶sung von Synonymen und Begriffsvarianten
- Navigation zwischen den 15 OSP-Modulen
- Kombination von Informationen aus mehreren Quellen

**âš ï¸ WICHTIG:** Bei jeder Anfrage diese Datei als Orientierung nutzen!

---

## ðŸ”‘ SCHLÃœSSEL-DATEIEN (Master-Referenzen)

### Personen & Organisation

| Thema | Datei | Inhalt | Anwendung |
|-------|-------|--------|-----------|
| **Mitarbeiter & ZustÃ¤ndigkeiten** | `HR_CORE_Personalstamm.md` | Alle MA, KÃ¼rzel, Namen, Level, TAG-Verantwortung, E-Mail | "Wer ist fÃ¼r X zustÃ¤ndig?", "Wie heiÃŸt X?", "E-Mail von X?" |
| **Organigramm & Hierarchie** | `ORG_ORGA_Unternehmensstruktur.md` | Abteilungen, Berichtslinien, Organisationsaufbau | "Wer leitet X?", "Struktur der Firma?" |
| **Unternehmensleitbild** | `ORG_LEIT_Leitbild_Vision.md` | Vision, Mission, Werte | "Was ist unsere Vision?", "Unternehmensziele?" |

### Technik & Produktion

| Thema | Datei | Inhalt | Anwendung |
|-------|-------|--------|-----------|
| **Maschinen & Anlagen** | `TM_CORE_Maschinen_Anlagen.md` | 14 Produktionsanlagen (Komax, Schleuniger, Brady) | "Welche Maschinen?", "Komax-Automaten?" |
| **Werkzeuge** | `TM_WKZ_Werkzeuge.md` | 70-110 Werkzeuge (Crimppressen, PrÃ¼fmittel, ESD) | "Welche Werkzeuge?", "Crimpzangen?" |
| **Kostenstellen** | `KST_*_*.md` | Produktionsbereiche, MinutensÃ¤tze | "Was kostet KST X?", "Wo wird gecrimpt?" |

### QualitÃ¤t & Management

| Thema | Datei | Inhalt | Anwendung |
|-------|-------|--------|-----------|
| **QualitÃ¤tspolitik** | `QM_CORE_Qualitaetspolitik.md` | QualitÃ¤tsziele, Fehler-Cluster 1-11, MinutensÃ¤tze, KPIs | "QualitÃ¤tsziele?", "Fehlerarten?", "Minutensatz?" |
| **PrÃ¼fmittel** | `QM_PMV_PrÃ¼fmittelverwaltung.md` | 90 PrÃ¼fmittel, Kalibrierung, Wartungsstatus | "Welches PrÃ¼fmittel?", "Kalibrierung fÃ¤llig?", "DrehmomentschlÃ¼ssel?" |
| **Reklamationen** | `QM_REK_Reklamationsmanagement.md` | Reklamationsprozess, Kundenreklamationen, 8D-Report | "Reklamation bearbeiten?", "Kunde beschwert sich?", "8D-Report?" |
| **Nacharbeiten** | `QM_NZA_Nach_Zusatzarbeiten.md` | NZA-Prozess, interne Fehler | "NZA erfassen?", "Interner Fehler?" |

### KI & Kommunikation

| Thema | Datei | Inhalt | Anwendung |
|-------|-------|--------|-----------|
| **KI-Regeln** | `KOM_AIR_KI_Kommunikationsregeln.md` | NULL-FEHLER-POLITIK, Confidence, 4-Phasen-Workflow | "Wie funktioniert die KI?", "Regeln?" |
| **Kommunikationsstil** | `KOM_STIL_Kommunikationsstil.md` | TonalitÃ¤t, Formulierungen | "Wie kommunizieren wir?" |

---

## ðŸ”„ SYNONYM-MAPPING

### Personen & Rollen

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "QualitÃ¤t zustÃ¤ndig", "QM-Verantwortung", "QualitÃ¤tsmanager" | QM-Manager | HR_CORE â†’ AL |
| "Chef", "GF", "GeschÃ¤ftsfÃ¼hrer", "Leitung" | GeschÃ¤ftsfÃ¼hrung | HR_CORE â†’ CS, CA |
| "Prokurist" | Prokura | HR_CORE â†’ SV |
| "wer ist X", "wer macht X", "zustÃ¤ndig fÃ¼r X" | Personenzuordnung | HR_CORE (TAG-Verantwortung) |
| "wie heiÃŸt X", "Name von X", "voller Name" | NamensauflÃ¶sung | HR_CORE (Name, Vorname) |

### Technik & Maschinen

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "Maschine", "Anlage", "Automat", "GerÃ¤t" | Produktionsanlage | TM_CORE |
| "Werkzeug", "Presse", "Zange", "PrÃ¼fmittel" | Werkzeug | TM_WKZ |
| "Komax", "Alpha", "Gamma", "Kappa" | Komax-Crimpautomaten (NICHT SchweiÃŸen!) | TM_CORE |
| "Schleuniger", "Brady" | Andere Hersteller | TM_CORE |
| "Crimpautomat", "Abisolierautomat" | Spezifische Maschinentypen | TM_CORE |
| "Kompaktieren", "SchweiÃŸen", "SchweiÃŸmaschine" | SchweiÃŸtechnik (Strunk, NIMAK, EWM) | TM_CORE Sektion 5.1 |
| "Thermotechnik", "HeiÃŸschneiden", "Schrumpfen" | Thermotechnik | TM_CORE Sektion 5.2 |

### QualitÃ¤t & Prozesse

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "QM", "QualitÃ¤tsmanagement", "QualitÃ¤t" | QualitÃ¤tsbereich | QM_CORE |
| "Fehler", "Reklamation", "Beschwerde" | QualitÃ¤tsproblem | QM_REK oder QM_NZA |
| "NZA", "Nacharbeit", "Zusatzarbeit", "interner Fehler" | Nach-/Zusatzarbeit | QM_NZA |
| "PrÃ¼ffeld", "PF", "PrÃ¼fung", "Endkontrolle" | PrÃ¼ffeld | KST_PF |
| "Minutensatz", "was kostet", "Kalkulation" | Kostenberechnung | QM_CORE (MinutensÃ¤tze) |
| "8D", "8D-Report", "KorrekturmaÃŸnahme" | 8D-Methodik | QM_REK (8D-Report) |

### PrÃ¼fmittel & Kalibrierung

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "PrÃ¼fmittel", "Messmittel", "Messinstrument" | PrÃ¼fmittelbestand | QM_PMV |
| "Kalibrierung", "kalibrieren", "eichen", "Eichung" | Kalibrierungsstatus | QM_PMV |
| "DrehmomentschlÃ¼ssel", "DM-S", "Nm", "Ncm" | DrehmomentschlÃ¼ssel-Bestand | QM_PMV (DM-S) |
| "Messschieber", "MS", "Schieblehre" | Messschieber-Bestand | QM_PMV (MS) |
| "Auszugstester", "AT", "Zugkraft" | Auszugstester | QM_PMV (AT) |
| "Crimp-HÃ¶henmesser", "CHM", "CrimphÃ¶he" | Crimp-HÃ¶henmesser | QM_PMV (CHM) |
| "PrÃ¼fstand", "Weetech", "Adaptronic" | Elektrische PrÃ¼fstÃ¤nde | QM_PMV (PS-W) |
| "Wartung fÃ¤llig", "Ã¼berfÃ¤llig", "Wartungsstatus" | Wartungsstatus PrÃ¼fmittel | QM_PMV |
| "welches PrÃ¼fmittel fÃ¼r", "womit messen", "womit prÃ¼fen" | PrÃ¼fmittelauswahl | QM_PMV + TM_WKZ |

### Kostenstellen & Bereiche

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "Kostenstelle", "KST", "Abteilung", "Bereich" | Produktionsbereich | KST_*_*.md |
| "KST 1000", "Zuschnitt", "Abisolieren" | Kostenstelle 1000 | KST_1000 |
| "KST 2000", "Halbautomaten", "Crimpen" | Kostenstelle 2000 | KST_2000 |
| "KST 3000", "Handarbeiten", "Montage" | Kostenstelle 3000 | KST_3000 |
| "KST 5000", "Sonderfertigung", "Spezial" | Kostenstelle 5000 | KST_5000 |
| "Lager", "Versand", "Warehousing" | Lagerbereich | KST_LAG |

### Level & Berechtigungen

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "Level", "Berechtigung", "Zugriff" | Zugriffslevel L1-L3 | HR_CORE |
| "OSP-Level", "KI-AffinitÃ¤t", "Erfahrung" | OSP-STD/PRO/EXP | HR_CORE |
| "L1", "Public", "Ã¶ffentlich" | Basiszugriff | HR_CORE |
| "L2", "Abteilung", "FÃ¼hrung" | Erweiterter Zugriff | HR_CORE |
| "L3", "Vertraulich", "Geheim" | Vollzugriff | HR_CORE |

---

## ðŸ·ï¸ TAG-SYSTEM KURZÃœBERSICHT (15 Module)

### Cluster 1: Kontext (ðŸ”·)
| TAG | Modul | Beschreibung | Zugriff |
|-----|-------|--------------|---------|
| **[ORG]** | Unternehmen | Philosophie, Leitbild, Organigramm, Glossar | ðŸŸ¢ L1 |
| **[KOM]** | Kommunikation | KI-Regeln, Corporate Identity, Vorlagen | ðŸŸ¢ L1 |

### Cluster 2: FÃ¼hrung (ðŸ”¶)
| TAG | Modul | Beschreibung | Zugriff |
|-----|-------|--------------|---------|
| **[QM]** | QualitÃ¤tsmanagement | QualitÃ¤tspolitik, NZA, Reklamationen, Audits | ðŸŸ¡ L2 |
| **[GF]** | GeschÃ¤ftsfÃ¼hrung | Strategie, Risikomanagement | ðŸ”´ L3 |
| **[PM]** | Projektmanagement | Aktuelle Projekte | ðŸŸ¡ L2 |
| **[AV]** | Arbeitsvorbereitung | Fertigungsunterlagen, ArbeitsgÃ¤nge | ðŸŸ¡ L2 |
| **[VT]** | Vertrieb | Kundenbewertung | ðŸŸ¡ L2 |
| **[EK]** | Einkauf | Lieferantenbewertung, Strategischer Einkauf | ðŸŸ¡ L2 |

### Cluster 3: Kernprozesse (ðŸ”µ)
| TAG | Modul | Beschreibung | Zugriff |
|-----|-------|--------------|---------|
| **[KST]** | Kostenstellen | Produktionsbereiche 1000-5000, PrÃ¼ffeld, Lager | ðŸŸ¢ L1 |

### Cluster 4: Support (ðŸ”´)
| TAG | Modul | Beschreibung | Zugriff |
|-----|-------|--------------|---------|
| **[DMS]** | Dokumentenmanagement | Anweisungen, Richtlinien | ðŸŸ¢ L1 |
| **[TM]** | Technik & Maschinen | Maschinen, Werkzeuge | ðŸŸ¢ L1 |
| **[IT]** | IT-Infrastruktur | Netzwerk, ERP, Server | ðŸŸ¢ L1 |
| **[HR]** | Human Resources | Personalstamm (MASTER!) | ðŸŸ¡ L2 |
| **[RES]** | Ressourcen & Wissen | Normen, Kabel-Datenbank | ðŸŸ¢ L1 |
| **[CMS]** | Compliance | Material Compliance, RoHS, REACH | ðŸŸ¢ L1 |

---

## â“ HÃ„UFIGE ABFRAGE-MUSTER

| Frage-Muster | SchlÃ¼ssel-Datei(en) | Beispiel-Antwort |
|--------------|---------------------|------------------|
| "Wer ist fÃ¼r X zustÃ¤ndig?" | HR_CORE (TAG-Verantwortung) | "AL ist fÃ¼r QM zustÃ¤ndig" |
| "Wie heiÃŸt X mit vollem Namen?" | HR_CORE (Name, Vorname) | "CS = Christoph Schneider" |
| "Welche Maschinen haben wir?" | TM_CORE | "6 Komax-Maschinen: Alpha 355S, 530, 550, 356S, Gamma 333, bt 711" |
| "Was kostet Minute in KST X?" | QM_CORE (MinutensÃ¤tze) | "KST 2000: 1,21 â‚¬/min" |
| "Wer leitet Abteilung X?" | HR_CORE + ORG_ORGA | "MD leitet KST 1000" |
| "E-Mail von X?" | HR_CORE (E-Mail) | "a.loehr@schneider-kabelsatzbau.de" |
| "Welches Level hat X?" | HR_CORE (Level, OSP) | "AL: L2, OSP-EXP" |
| "Was sind unsere QualitÃ¤tsziele?" | QM_CORE | "6 Dimensionen: Kundenorientierung, KVP, ..." |
| "Welche Fehlerarten gibt es?" | QM_CORE (Cluster 1-11) | "11 Cluster: Crimp, LÃ¤nge, Verpolung, ..." |
| "Welches PrÃ¼fmittel fÃ¼r Wartung?" | QM_PMV + TM_CORE | "FÃ¼r Komax Alpha 550: DM-S07 (0,3-1,2 Nm), MS-03" |
| "Ist Kalibrierung fÃ¤llig?" | QM_PMV (Wartungsstatus) | "DM-S02 ist Ã¼berfÃ¤llig seit 2025-12-09" |
| "Wie erstelle ich 8D-Report?" | QM_REK (8D-Methodik) | "8 Schritte: D1-D8, siehe Vorlage FQM03" |
| "Wie rÃ¼ste ich WKZ X ein?" | TM_WKZ + QM_PMV | "WKZ 627: VT-Set verwenden, CrimphÃ¶he mit CHM-01 prÃ¼fen" |

---

## ðŸ”— KOMBINATIONS-LOGIK

Bei komplexen Anfragen mehrere Dateien kombinieren:

| Anfrage-Typ | Kombination |
|-------------|-------------|
| "Wer prÃ¼ft im PrÃ¼ffeld?" | HR_CORE (Personen) + KST_PF (Prozesse) |
| "Maschinen in KST 1000?" | TM_CORE (Maschinen) + KST_1000 (Zuordnung) |
| "QualitÃ¤tsziele und Verantwortliche?" | QM_CORE (Ziele) + HR_CORE (Verantwortliche) |
| "Organigramm mit Namen?" | ORG_ORGA (Struktur) + HR_CORE (Namen) |

### ðŸŽ¯ USE-CASE KOMBINATIONEN (Demo-relevant)

| Use-Case | Dateien-Kombination | Beispiel-Anfrage |
|----------|--------------------|-----------------|
| **UC1: Wartungs-Workflow** | TM_CORE + QM_PMV + HR_CORE + F_QM_37 | "Wartung Komax Alpha 550 - was brauche ich?" |
| **UC2: Meeting-Protokoll** | HR_CORE + F_PM_01 | "Protokoll erstellen, Teilnehmer: CS, AL, SV" |
| **UC3: WKZ-Einstellung** | TM_WKZ + QM_PMV | "WKZ 627 fÃ¼r Kontakt 0-0282110-1 einrichten" |
| **UC4: Revisions-Kontext** | QM_REK | "Ã„nderung aufgrund Reklamation?" |

---

## âš ï¸ WICHTIGE HINWEISE

1. **HR_CORE ist MASTER** fÃ¼r alle Personendaten - immer dort nachschlagen
2. **TM_CORE fÃ¼r Maschinen**, TM_WKZ fÃ¼r Werkzeuge - nicht verwechseln
3. **QM_PMV fÃ¼r PrÃ¼fmittel** - 90 GerÃ¤te mit Kalibrierungsstatus
4. **QM_REK fÃ¼r Reklamationen** - inkl. 8D-Report Prozess
5. **QM_CORE enthÃ¤lt MinutensÃ¤tze** - nicht nur in KST-Dateien suchen
6. **Bei Unsicherheit:** Explizit nachfragen, keinesfalls raten/mutmaÃŸen
7. **KÃ¼rzel-Nutzung:** Extern nur KÃ¼rzel (AL, CS), intern auch Namen erlaubt
8. **Wartungs-Workflow:** Immer TM_CORE + QM_PMV kombinieren!

---

## ðŸ“‚ LAYER-ARCHITEKTUR

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LAYER 0: OSP_KPL (Dateinamen-Index)                        â”‚
â”‚  â†’ Nur Metadaten fÃ¼r Navigation                             â”‚
â”‚  â†’ Siehe: /opt/osp/lookups/osp_kpl_index.json               â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LAYER 1: OSP_KERN (12 Dateien) - DAUERHAFT GELADEN         â”‚
â”‚  â†’ Full-Context Mode fÃ¼r kritische Tabellen                 â”‚
â”‚  â†’ IMMER im RAG-Kontext verfÃ¼gbar                           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LAYER 2: OSP_ERWEITERT (~46 Dateien) - BEI BEDARF          â”‚
â”‚  â†’ Chunked RAG, Routing basierend auf Keywords/TAGs         â”‚
â”‚  â†’ Wird nur geladen wenn Query relevant                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LAYER 3: SHAREPOINT (Gelenkte Dokumente)                   â”‚
â”‚  â†’ FormblÃ¤tter (MD): Bidirektional (ausfÃ¼llen+speichern)    â”‚
â”‚  â†’ PDFs/HandbÃ¼cher: Nur Verlinkung                          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ”„ PIPELINE-MODULE (NEU 15.12.2025)

Queries werden durch **4 Pre-Processing-Module** optimiert:

| Step | Modul | Funktion | Verbesserung |
|------|-------|----------|--------------|
| -1 | Query-Normalizer | Tippfehler korrigieren | 70% â†’ 90%+ |
| 0 | MA-Preprocessing | KÃ¼rzel expandieren | 0% â†’ 100% |
| 1.5 | Keyword-Filter | Kritische Keywords direkt laden | 70% â†’ 95%+ |
| 2 | Tag-Router | ChromaDB WHERE-Filter | 70% â†’ 100% |

**Details:** Siehe `IT_OSP_KI_Chatbot.md` â†’ Abschnitt "PIPELINE-ARCHITEKTUR"

---

## ðŸ–¥ï¸ SERVER-REFERENZ

| Komponente | Wert |
|------------|------|
| **Server** | Hetzner CX43 (8 vCPU, 16GB RAM) |
| **IP** | 46.224.102.30 |
| **Open WebUI** | v0.6.43, Port 3000 |
| **ChromaDB** | v1.3.6, Port 8000 |
| **Embedding-Modell** | multilingual-e5-large (1024 Dim.) |
| **LLM** | Claude API via LiteLLM (Port 4000) |
| **Pipeline-Module** | 4 aktiv (Query-Norm, MA-Pre, Keyword, Tag-Router) |

---

## ðŸ“Š STATISTIK

- **15 Module** in 4 Clustern
- **85 Sub-TAGs** dokumentiert
- **~60 Sub-TAGs** aktiv gefÃ¼llt
- **~51 MD-Dateien** im RAG-Wissensbestand (inkl. QM_PMV, QM_REK)
- **6 Pilot-User** aktiv (AL, CS, SV, TS, SK, MD)
- **4 Demo Use-Cases** konfiguriert (UC1-UC4)
- **4 Pipeline-Module** aktiv (Query-Norm, MA-Pre, Keyword, Tag-Router)

---

## Ã„NDERUNGSHISTORIE

### [2.2] - 2025-12-23 - STACK-UPDATE
**Quelle:** Server-Erhebung 2025-12-23

**Korrekturen:**
- ❌ RAM: 32GB → ✅ 16GB (Dokumentationsfehler)
- ✅ Open WebUI: 0.6.41 → 0.6.43
- ✅ ChromaDB: 0.5.15 → 1.3.6 (Major Update)
- ✅ Embedding: all-MiniLM-L6-v2 → multilingual-e5-large
- ✅ LLM: Ollama entfernt → Claude API via LiteLLM

**Verantwortlich:** AL (QM & KI-Manager)

---

### [2.1] - 2025-12-23
**Pipeline-Module & Hardware-Update:**
- âœ… Layer-Architektur aktualisiert (4 Layer inkl. OSP_KPL)
- âœ… Server-Referenz aktualisiert (CX33 â†’ CX43, 8 vCPU, 16GB RAM)
- âœ… Neuer Abschnitt "PIPELINE-MODULE" hinzugefÃ¼gt
- âœ… Open WebUI Version: v0.6.41

**Verantwortlich:** AL (QM & KI-Manager)

### [1.1] - 2025-12-11
**QM-Module Integration:**
- QM_PMV und QM_REK integriert
- Use-Case-Kombinationen ergÃ¤nzt
- Synonym-Mapping fÃ¼r PrÃ¼fmittel hinzugefÃ¼gt

### [1.0] - 2025-12-09
**Erstversion:**
- Governance-Struktur definiert (System-Prompt + Navigator)
- OSP_KERN (12 Dateien) explizit dokumentiert
- Server-Pfade (Hetzner) hinzugefÃ¼gt
- Statistik korrigiert (58 MD-Dateien)

---

*Diese Datei ist die zentrale Navigations-Hilfe fÃ¼r das OSP-Wissensmanagement. Bei jeder Anfrage als Orientierung nutzen!*

(C: 100%) [OSP]
