# OSP Navigator - Intelligentes Wissens-Routing

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 1.1 | **TAG:** [OSP][NAV] | **Erstellt:** 2025-12-09 | **Aktualisiert:** 2025-12-11 | **Autor:** AL | **Verantwortlich:** AL (QM/KI-Manager) | **Zugriff:** 🟢 L1-Öffentlich | **Status:** ✅ PRODUKTIV (RAG) | **Kritikalität:** 🔴 SEHR HOCH

**Änderungen v1.1:** QM_PMV und QM_REK integriert, Use-Case-Kombinationen ergänzt, Synonym-Mapping für Prüfmittel hinzugefügt

---

## 🎯 ZWECK

Diese Datei ist der **zentrale Wegweiser** im OSP-Wissensbestand. Sie hilft dem KI-System bei:
- Zuordnung von Benutzer-Anfragen zu Schlüssel-Dateien
- Auflösung von Synonymen und Begriffsvarianten
- Navigation zwischen den 15 OSP-Modulen
- Kombination von Informationen aus mehreren Quellen

**⚠️ WICHTIG:** Bei jeder Anfrage diese Datei als Orientierung nutzen!

---

## 🔑 SCHLÜSSEL-DATEIEN (Master-Referenzen)

### Personen & Organisation

| Thema | Datei | Inhalt | Anwendung |
|-------|-------|--------|-----------|
| **Mitarbeiter & Zuständigkeiten** | `HR_CORE_Personalstamm.md` | Alle MA, Kürzel, Namen, Level, TAG-Verantwortung, E-Mail | "Wer ist für X zuständig?", "Wie heißt X?", "E-Mail von X?" |
| **Organigramm & Hierarchie** | `ORG_ORGA_Unternehmensstruktur.md` | Abteilungen, Berichtslinien, Organisationsaufbau | "Wer leitet X?", "Struktur der Firma?" |
| **Unternehmensleitbild** | `ORG_LEIT_Leitbild_Vision.md` | Vision, Mission, Werte | "Was ist unsere Vision?", "Unternehmensziele?" |

### Technik & Produktion

| Thema | Datei | Inhalt | Anwendung |
|-------|-------|--------|-----------|
| **Maschinen & Anlagen** | `TM_CORE_Maschinen_Anlagen.md` | 14 Produktionsanlagen (Komax, Schleuniger, Brady) | "Welche Maschinen?", "Komax-Automaten?" |
| **Werkzeuge** | `TM_WKZ_Werkzeuge.md` | 70-110 Werkzeuge (Crimppressen, Prüfmittel, ESD) | "Welche Werkzeuge?", "Crimpzangen?" |
| **Kostenstellen** | `KST_*_*.md` | Produktionsbereiche, Minutensätze | "Was kostet KST X?", "Wo wird gecrimpt?" |

### Qualität & Management

| Thema | Datei | Inhalt | Anwendung |
|-------|-------|--------|-----------|
| **Qualitätspolitik** | `QM_CORE_Qualitaetspolitik.md` | Qualitätsziele, Fehler-Cluster 1-11, Minutensätze, KPIs | "Qualitätsziele?", "Fehlerarten?", "Minutensatz?" |
| **Prüfmittel** | `QM_PMV_Prüfmittelverwaltung.md` | 90 Prüfmittel, Kalibrierung, Wartungsstatus | "Welches Prüfmittel?", "Kalibrierung fällig?", "Drehmomentschlüssel?" |
| **Reklamationen** | `QM_REK_Reklamationsmanagement.md` | Reklamationsprozess, Kundenreklamationen, 8D-Report | "Reklamation bearbeiten?", "Kunde beschwert sich?", "8D-Report?" |
| **Nacharbeiten** | `QM_NZA_Nach_Zusatzarbeiten.md` | NZA-Prozess, interne Fehler | "NZA erfassen?", "Interner Fehler?" |

### KI & Kommunikation

| Thema | Datei | Inhalt | Anwendung |
|-------|-------|--------|-----------|
| **KI-Regeln** | `KOM_AIR_KI_Kommunikationsregeln.md` | NULL-FEHLER-POLITIK, Confidence, 4-Phasen-Workflow | "Wie funktioniert die KI?", "Regeln?" |
| **Kommunikationsstil** | `KOM_STIL_Kommunikationsstil.md` | Tonalität, Formulierungen | "Wie kommunizieren wir?" |

---

## 🔄 SYNONYM-MAPPING

### Personen & Rollen

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "Qualität zuständig", "QM-Verantwortung", "Qualitätsmanager" | QM-Manager | HR_CORE → AL |
| "Chef", "GF", "Geschäftsführer", "Leitung" | Geschäftsführung | HR_CORE → CS, CA |
| "Prokurist" | Prokura | HR_CORE → SV |
| "wer ist X", "wer macht X", "zuständig für X" | Personenzuordnung | HR_CORE (TAG-Verantwortung) |
| "wie heißt X", "Name von X", "voller Name" | Namensauflösung | HR_CORE (Name, Vorname) |

### Technik & Maschinen

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "Maschine", "Anlage", "Automat", "Gerät" | Produktionsanlage | TM_CORE |
| "Werkzeug", "Presse", "Zange", "Prüfmittel" | Werkzeug | TM_WKZ |
| "Komax", "Alpha", "Gamma", "Kappa" | Komax-Crimpautomaten (NICHT Schweißen!) | TM_CORE |
| "Schleuniger", "Brady" | Andere Hersteller | TM_CORE |
| "Crimpautomat", "Abisolierautomat" | Spezifische Maschinentypen | TM_CORE |
| "Kompaktieren", "Schweißen", "Schweißmaschine" | Schweißtechnik (Strunk, NIMAK, EWM) | TM_CORE Sektion 5.1 |
| "Thermotechnik", "Heißschneiden", "Schrumpfen" | Thermotechnik | TM_CORE Sektion 5.2 |

### Qualität & Prozesse

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "QM", "Qualitätsmanagement", "Qualität" | Qualitätsbereich | QM_CORE |
| "Fehler", "Reklamation", "Beschwerde" | Qualitätsproblem | QM_REK oder QM_NZA |
| "NZA", "Nacharbeit", "Zusatzarbeit", "interner Fehler" | Nach-/Zusatzarbeit | QM_NZA |
| "Prüffeld", "PF", "Prüfung", "Endkontrolle" | Prüffeld | KST_PF |
| "Minutensatz", "was kostet", "Kalkulation" | Kostenberechnung | QM_CORE (Minutensätze) |
| "8D", "8D-Report", "Korrekturmaßnahme" | 8D-Methodik | QM_REK (8D-Report) |

### Prüfmittel & Kalibrierung

| Benutzer sagt... | Bedeutet... | Ziel-Datei |
|------------------|-------------|------------|
| "Prüfmittel", "Messmittel", "Messinstrument" | Prüfmittelbestand | QM_PMV |
| "Kalibrierung", "kalibrieren", "eichen", "Eichung" | Kalibrierungsstatus | QM_PMV |
| "Drehmomentschlüssel", "DM-S", "Nm", "Ncm" | Drehmomentschlüssel-Bestand | QM_PMV (DM-S) |
| "Messschieber", "MS", "Schieblehre" | Messschieber-Bestand | QM_PMV (MS) |
| "Auszugstester", "AT", "Zugkraft" | Auszugstester | QM_PMV (AT) |
| "Crimp-Höhenmesser", "CHM", "Crimphöhe" | Crimp-Höhenmesser | QM_PMV (CHM) |
| "Prüfstand", "Weetech", "Adaptronic" | Elektrische Prüfstände | QM_PMV (PS-W) |
| "Wartung fällig", "überfällig", "Wartungsstatus" | Wartungsstatus Prüfmittel | QM_PMV |
| "welches Prüfmittel für", "womit messen", "womit prüfen" | Prüfmittelauswahl | QM_PMV + TM_WKZ |

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
| "OSP-Level", "KI-Affinität", "Erfahrung" | OSP-STD/PRO/EXP | HR_CORE |
| "L1", "Public", "öffentlich" | Basiszugriff | HR_CORE |
| "L2", "Abteilung", "Führung" | Erweiterter Zugriff | HR_CORE |
| "L3", "Vertraulich", "Geheim" | Vollzugriff | HR_CORE |

---

## 🏷️ TAG-SYSTEM KURZÜBERSICHT (15 Module)

### Cluster 1: Kontext (🔷)
| TAG | Modul | Beschreibung | Zugriff |
|-----|-------|--------------|---------|
| **[ORG]** | Unternehmen | Philosophie, Leitbild, Organigramm, Glossar | 🟢 L1 |
| **[KOM]** | Kommunikation | KI-Regeln, Corporate Identity, Vorlagen | 🟢 L1 |

### Cluster 2: Führung (🔶)
| TAG | Modul | Beschreibung | Zugriff |
|-----|-------|--------------|---------|
| **[QM]** | Qualitätsmanagement | Qualitätspolitik, NZA, Reklamationen, Audits | 🟡 L2 |
| **[GF]** | Geschäftsführung | Strategie, Risikomanagement | 🔴 L3 |
| **[PM]** | Projektmanagement | Aktuelle Projekte | 🟡 L2 |
| **[AV]** | Arbeitsvorbereitung | Fertigungsunterlagen, Arbeitsgänge | 🟡 L2 |
| **[VT]** | Vertrieb | Kundenbewertung | 🟡 L2 |
| **[EK]** | Einkauf | Lieferantenbewertung, Strategischer Einkauf | 🟡 L2 |

### Cluster 3: Kernprozesse (🔵)
| TAG | Modul | Beschreibung | Zugriff |
|-----|-------|--------------|---------|
| **[KST]** | Kostenstellen | Produktionsbereiche 1000-5000, Prüffeld, Lager | 🟢 L1 |

### Cluster 4: Support (🔴)
| TAG | Modul | Beschreibung | Zugriff |
|-----|-------|--------------|---------|
| **[DMS]** | Dokumentenmanagement | Anweisungen, Richtlinien | 🟢 L1 |
| **[TM]** | Technik & Maschinen | Maschinen, Werkzeuge | 🟢 L1 |
| **[IT]** | IT-Infrastruktur | Netzwerk, ERP, Server | 🟢 L1 |
| **[HR]** | Human Resources | Personalstamm (MASTER!) | 🟡 L2 |
| **[RES]** | Ressourcen & Wissen | Normen, Kabel-Datenbank | 🟢 L1 |
| **[CMS]** | Compliance | Material Compliance, RoHS, REACH | 🟢 L1 |

---

## ❓ HÄUFIGE ABFRAGE-MUSTER

| Frage-Muster | Schlüssel-Datei(en) | Beispiel-Antwort |
|--------------|---------------------|------------------|
| "Wer ist für X zuständig?" | HR_CORE (TAG-Verantwortung) | "AL ist für QM zuständig" |
| "Wie heißt X mit vollem Namen?" | HR_CORE (Name, Vorname) | "CS = Christoph Schneider" |
| "Welche Maschinen haben wir?" | TM_CORE | "6 Komax-Maschinen: Alpha 355S, 530, 550, 356S, Gamma 333, bt 711" |
| "Was kostet Minute in KST X?" | QM_CORE (Minutensätze) | "KST 2000: 1,21 €/min" |
| "Wer leitet Abteilung X?" | HR_CORE + ORG_ORGA | "MD leitet KST 1000" |
| "E-Mail von X?" | HR_CORE (E-Mail) | "a.loehr@schneider-kabelsatzbau.de" |
| "Welches Level hat X?" | HR_CORE (Level, OSP) | "AL: L2, OSP-EXP" |
| "Was sind unsere Qualitätsziele?" | QM_CORE | "6 Dimensionen: Kundenorientierung, KVP, ..." |
| "Welche Fehlerarten gibt es?" | QM_CORE (Cluster 1-11) | "11 Cluster: Crimp, Länge, Verpolung, ..." |
| "Welches Prüfmittel für Wartung?" | QM_PMV + TM_CORE | "Für Komax Alpha 550: DM-S07 (0,3-1,2 Nm), MS-03" |
| "Ist Kalibrierung fällig?" | QM_PMV (Wartungsstatus) | "DM-S02 ist überfällig seit 2025-12-09" |
| "Wie erstelle ich 8D-Report?" | QM_REK (8D-Methodik) | "8 Schritte: D1-D8, siehe Vorlage FQM03" |
| "Wie rüste ich WKZ X ein?" | TM_WKZ + QM_PMV | "WKZ 627: VT-Set verwenden, Crimphöhe mit CHM-01 prüfen" |

---

## 🔗 KOMBINATIONS-LOGIK

Bei komplexen Anfragen mehrere Dateien kombinieren:

| Anfrage-Typ | Kombination |
|-------------|-------------|
| "Wer prüft im Prüffeld?" | HR_CORE (Personen) + KST_PF (Prozesse) |
| "Maschinen in KST 1000?" | TM_CORE (Maschinen) + KST_1000 (Zuordnung) |
| "Qualitätsziele und Verantwortliche?" | QM_CORE (Ziele) + HR_CORE (Verantwortliche) |
| "Organigramm mit Namen?" | ORG_ORGA (Struktur) + HR_CORE (Namen) |

### 🎯 USE-CASE KOMBINATIONEN (Demo-relevant)

| Use-Case | Dateien-Kombination | Beispiel-Anfrage |
|----------|--------------------|-----------------|
| **UC1: Wartungs-Workflow** | TM_CORE + QM_PMV + HR_CORE + F_QM_37 | "Wartung Komax Alpha 550 - was brauche ich?" |
| **UC2: Meeting-Protokoll** | HR_CORE + F_PM_01 | "Protokoll erstellen, Teilnehmer: CS, AL, SV" |
| **UC3: WKZ-Einstellung** | TM_WKZ + QM_PMV | "WKZ 627 für Kontakt 0-0282110-1 einrichten" |
| **UC4: Revisions-Kontext** | QM_REK | "Änderung aufgrund Reklamation?" |

---

## ⚠️ WICHTIGE HINWEISE

1. **HR_CORE ist MASTER** für alle Personendaten - immer dort nachschlagen
2. **TM_CORE für Maschinen**, TM_WKZ für Werkzeuge - nicht verwechseln
3. **QM_PMV für Prüfmittel** - 90 Geräte mit Kalibrierungsstatus
4. **QM_REK für Reklamationen** - inkl. 8D-Report Prozess
5. **QM_CORE enthält Minutensätze** - nicht nur in KST-Dateien suchen
6. **Bei Unsicherheit:** Explizit nachfragen, keinesfalls raten/mutmaßen
7. **Kürzel-Nutzung:** Extern nur Kürzel (AL, CS), intern auch Namen erlaubt
8. **Wartungs-Workflow:** Immer TM_CORE + QM_PMV kombinieren!

---

## 📊 STATISTIK

- **15 Module** in 4 Clustern
- **85 Sub-TAGs** dokumentiert
- **~60 Sub-TAGs** aktiv gefüllt
- **~51 MD-Dateien** im RAG-Wissensbestand (inkl. QM_PMV, QM_REK)
- **6 Pilot-User** aktiv (AL, CS, SV, TS, SK, MD)
- **4 Demo Use-Cases** konfiguriert (UC1-UC4)

---

*Diese Datei ist die zentrale Navigations-Hilfe für das OSP-Wissensmanagement. Bei jeder Anfrage als Orientierung nutzen!*

(C: 100%) [OSP]
