# TM_CRIMP_Crimpdaten_Werkzeuge

## Metadaten

| Attribut | Wert |
|----------|------|
| **Dokument-ID** | TM_CRIMP_001 |
| **Version** | 2.0 |
| **Erstellt** | 2025-12-17 |
| **Aktualisiert** | 2025-12-17 |
| **Autor** | AL (QM-Manager) |
| **Status** | AKTIV |
| **Klassifikation** | L2 (Führung) |
| **OSP-Level** | OSP-PRO |
| **TAGs** | [TM], [WKZ], [QM], [KST] |
| **Cluster** | C4 Support / C3 Kernprozesse |
| **Basis** | TM_CRIMP v1.0 + wkz_crimpdaten_master v3.4-FINAL |

---

## 1. Zweck und Geltungsbereich

Dieses Dokument enthält die vollständigen **Crimpdaten aller Crimpwerkzeuge** der Rainer Schneider Kabelsatzbau GmbH & Co. KG. Es dient als zentrale Referenz für:

- Qualitätssicherung bei der Crimpverarbeitung
- Werkzeugeinstellung und -kalibrierung
- Erstmusterprüfungen und Prozessfreigaben
- Reklamationsanalyse und Fehlersuche

### ⚠️ NULL-FEHLER-POLITIK

> **KRITISCHE WARNUNG:**  
> Falsche Crimphöhen sind **EXISTENZBEDROHEND** für das Unternehmen!  
> Alle Angaben in diesem Dokument wurden aus den Original-Datenblättern extrahiert.  
> Bei Unstimmigkeiten **IMMER** das Original-PDF prüfen!

---

## 2. Dokumentenstruktur

### 2.1 Datenquellen

| Quelle | Beschreibung | Version | Anzahl |
|--------|--------------|---------|--------|
| wkz_crimpdaten_master.json | Konsolidierte Master-Datei | **v3.4-FINAL** | **180 WKZ** |
| kontakt_wkz_crimp_lookup.json | Kontakt→WKZ Lookup | **v2.0** | **49 Kontakte** |
| WKZ XXX.pdf | Original-Datenblätter | - | ~180 PDFs |

### 2.2 Werkzeugbereich

- **WKZ 501 - 729** (mit Lücken)
- **18 Batches** vollständig extrahiert
- **233 Varianten** mit Crimpdaten

### 2.3 Statistik (v3.4-FINAL)

| Kategorie | Anzahl |
|-----------|--------|
| Werkzeuge gesamt | 180 |
| Varianten gesamt | 233 |
| Aktive WKZ | 173 |
| Verschrottete WKZ | 7 |
| Problematische WKZ | 9 |
| Hersteller-Kategorien | 16+ |

---

## 3. Kritische Warnungen

### ⚠️ VERSCHROTTETE WERKZEUGE (7 Einträge)

| WKZ | Kontakt | Status | Datum/Hinweis |
|-----|---------|--------|---------------|
| **705** | 0906 000 9561 | 🗑️ VERSCHROTTET | 2013 |
| **709** | 16-02-0086 | 🗑️ VERSCHROTTET | KW 48/2024 |
| **632** | 179955-2 | 🗑️ VERSCHROTTET | KW 48/2024 |
| **634** | 163081/083 (777-9316S-T3) | 🗑️ VERSCHROTTET | KW 50/2023 |
| **635** | 163085 (777-9320S-T3) | 🗑️ VERSCHROTTET | KW 48/2024 |
| **636** | 39-00-0077 | 🗑️ VERSCHROTTET | Querschnitt 1,50mm² zu groß |
| **640** | 25036 | 🗑️ VERSCHROTTET | Kontakt verschrottet |

### ⚠️ PROZESSWARNUNGEN (3 Einträge)

| WKZ | Kontakt | Warnung |
|-----|---------|---------|
| **614** | Buchsenkontakt KTK | **Bei 125N reißt der Steckbereich des Kontaktes ab!** |
| **713** | EN 0202500431 | **Isolationsdurchmesser bei beiden Litzen zu groß gewählt!** |
| **729** | 505431-1300 | **Nur Isolation von 0.75mm - max. 0.96mm verarbeitbar!** |

---

## 4. Crimpdaten nach Hersteller

### 4.1 GHW / Grote & Hartmann (22 WKZ)

#### Kontakt 25783 (GHW)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Confidence |
|-----|-------------|-----------|-------------|------------|
| 505 | 1.00 mm² | **1.77 mm** | 1.67 mm | 100% |
| 512 | 1.00 mm² | **1.77 mm** | 1.67 mm | 100% |
| 512 | 1.50 mm² | - | - | 80% |
| 516 | 1.00 mm² | **1.77 mm** | 1.67 mm | 100% |
| 516 | 1.50 mm² | - | - | 80% |

#### Kontakt 25787 (GHW)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Confidence |
|-----|-------------|-----------|-------------|------------|
| 515 | 0.75 mm² | **1.33 mm** | 1.56 mm | 100% |
| 515 | 1.00 mm² | **1.34 mm** | 1.56 mm | 100% |

#### Kontakt 25722 (GHW)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 538 | 0.75 mm² | **1.49 mm** | 2.40 mm | 2.61 mm | 3.53 mm | 160 N | 100% |
| 587 | 0.75 mm² | **1.49 mm** | 2.40 mm | 2.61 mm | 3.53 mm | 160 N | 100% |

#### Kontakt 25733 (GHW/Lear)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 569 | 1.00 mm² | **1.75 mm** | 2.90 mm | 3.65 mm | 4.26 mm | 240 N | 100% |
| 569 | 1.50/2.50 mm² | **2.05 mm** | 2.92 mm | 3.94 mm | 4.00 mm | 380 N | 100% |
| 586 | 1.00 mm² | **1.70 mm** | 2.90 mm | 3.65 mm | 4.26 mm | 240 N | 100% |
| 586 | 1.50 mm² | **1.75 mm** | 2.92 mm | 3.94 mm | 4.00 mm | - | 100% |
| 586 | 2.50 mm² | **2.05 mm** | - | - | - | 380 N | 100% |

#### Kontakt 25213-25223 (GHW)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 544 | 1.50 mm² | **2.25 mm** | 3.43 mm | 3.65 mm | 4.52 mm | 300 N | 100% |
| 544 | 2.50 mm² | **2.45 mm** | 3.46 mm | 3.78 mm | 4.54 mm | 450 N | 100% |
| 564 | 1.50 mm² | **2.25 mm** | 3.43 mm | 3.65 mm | 4.52 mm | 300 N | 100% |
| 564 | 2.50 mm² | **2.45 mm** | 3.46 mm | 3.78 mm | 4.54 mm | 450 N | 100% |
| 568 | 1.50 mm² | **2.25 mm** | 3.43 mm | 3.65 mm | 4.52 mm | 300 N | 100% |
| 568 | 2.50 mm² | **2.45 mm** | 3.46 mm | 3.78 mm | 4.54 mm | 450 N | 100% |
| 572 | 1.50 mm² | **2.25 mm** | 3.43 mm | 3.65 mm | 4.52 mm | 300 N | 100% |
| 572 | 2.50 mm² | **2.45 mm** | 3.46 mm | 3.78 mm | 4.54 mm | 450 N | 100% |
| 577 | 1.50 mm² | **2.25 mm** | 3.43 mm | 3.65 mm | 4.52 mm | 300 N | 100% |
| 577 | 2.50 mm² | **2.45 mm** | 3.46 mm | 3.78 mm | 4.54 mm | 450 N | 100% |
| 578 | 1.50 mm² | **2.25 mm** | 3.43 mm | 3.65 mm | 4.52 mm | 300 N | 100% |
| 578 | 2.50 mm² | **2.45 mm** | 3.46 mm | 3.78 mm | 4.54 mm | 450 N | 100% |

#### Kontakt 25231 (GHW)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 545 | 6.00 mm² | **3.35 mm** | 5.20 mm | 5.42 mm | 6.73 mm | 500+ N | 100% |
| 567 | 6.00 mm² | **3.35 mm** | 5.20 mm | 5.42 mm | 6.73 mm | 500+ N | 100% |

#### Kontakt 25131 (GHW)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Confidence |
|-----|-------------|-----------|-------------|------------|
| 649 | 0.50 mm² | **1.10 mm** | 2.15 mm | 95% |
| 649 | 0.75 mm² | **1.20 mm** | 2.15 mm | 95% |
| 649 | 1.00 mm² | **1.30 mm** | 2.15 mm | 95% |

#### Kontakt 25116 (GHW)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Conf |
|-----|-------------|-----------|-------------|----------|------------|------|
| 598 | 0.50 mm² | **1.30 mm** | 2.40 mm | 2.50 mm | 3.60 mm | 100% |
| 598 | 0.75 mm² | **1.40 mm** | 2.40 mm | 2.60 mm | 3.60 mm | 100% |
| 598 | 1.00 mm² | **1.50 mm** | 2.40 mm | 2.70 mm | 3.60 mm | 100% |

#### Kontakt 25568 (GHW)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Conf |
|-----|-------------|-----------|-------------|----------|------------|------|
| 702 | 2.50 mm² | **1.92 mm** | 2.93 mm | 3.42 mm | 4.05 mm | 100% |
| 706 | 2.50 mm² | **1.92 mm** | 2.93 mm | 3.42 mm | 4.05 mm | 100% |

---

### 4.2 AMP / Tyco (13 WKZ)

#### Kontakt 794407 (AMP/Tyco)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 602 | 0.75 mm² | **1.08 mm** | 1.72 mm | 3.01 mm | 2.97 mm | 140 N | 100% |
| 606 | 0.75 mm² | **1.08 mm** | 1.72 mm | 3.01 mm | 2.97 mm | 140 N | 100% |

#### Kontakt 927827 (AMP/Tyco)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 651 | 0.50 mm² | **1.39 mm** | 2.11 mm | 3.14 mm | 3.49 mm | 95 N | 100% |
| 655 | 2x0.50 mm² | **1.55 mm** | 2.12 mm | 3.70 mm | 3.60 mm | 160 N | 100% |

#### Kontakt 160759 (AMP/Tyco)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 653 | 0.80 mm² | **1.60 mm** | 2.40 mm | 3.08 mm | 3.50 mm | 145 N | 100% |
| 653 | 1.50 mm² | **1.80 mm** | 2.43 mm | - | 3.80 mm | - | 95% |

#### Kontakt 0350566 (AMP/Tyco) - MINI AMP-IN
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Conf |
|-----|-------------|-----------|-------------|----------|------------|------|
| 607 | 0.75 mm² | **1.03 mm** | 1.69 mm | 2.52 mm | 2.50 mm | 100% |
| 608 | 0.75 mm² | **1.03 mm** | 1.69 mm | 2.52 mm | 2.50 mm | 100% |

#### Kontakt 925819 (AMP/Tyco) - MINI AMP-IN Sidefeed
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Conf |
|-----|-------------|-----------|-------------|----------|------------|------|
| 609 | 0.33 mm² (AWG 23) | **1.03 mm** | 1.33 mm | 2.39 mm | 2.36 mm | 90% |

#### Kontakt 170 361-1 (Tyco)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Conf |
|-----|-------------|-----------|-------------|------|
| 605 | 0.14 mm² | **0.66 mm** | 1.72 mm | 95% |

#### Kontakt 104505 (AMP/Tyco)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Conf |
|-----|-------------|-----------|-------------|----------|------------|------|
| 717 | 0.14 mm² | **0.72 mm** | 1.11 mm | 1.00 mm | 1.40 mm | 100% |

#### Kontakt 1241396-1 (Tyco)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 697 | 2.50 mm² | **1.95 mm** | 2.73 mm | 4.25 mm | 4.23 mm | 350 N | 100% |

#### Kontakt 1241408 (Tyco)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 698 | 4.00 mm² | **2.50 mm** | 4.05 mm | 4.70 mm | 4.95 mm | >500 N | 100% |

---

### 4.3 Lear (14 WKZ)

#### Kontakt 25744 (Lear)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 539 | 4.00 mm² | **2.45 mm** | 4.01 mm | 4.15 mm | 4.93 mm | >500 N | 100% |
| 539 | 6.00 mm² | **2.65 mm** | 4.05 mm | 4.55 mm | 5.05 mm | >500 N | 100% |
| 539 | 2x2.50 mm² | **2.84 mm** | 4.08 mm | 5.70 mm | 5.07 mm | 400 N | 100% |

#### Kontakt 25361 (Lear)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 565 | 4.00 mm² | **3.25 mm** | 5.15 mm | 5.27 mm | 6.68 mm | >500 N | 100% |
| 566 | 4.00 mm² | **3.25 mm** | 5.15 mm | 5.27 mm | 6.68 mm | >500 N | 100% |

#### Kontakt 25149.122 (Lear)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 571 | 1.50 mm² | **1.70 mm** | 3.05 mm | 3.40 mm | 4.30 mm | 230 N | 100% |
| 574 | 1.50 mm² | **1.70 mm** | 3.05 mm | 3.40 mm | 4.30 mm | 230 N | 100% |

---

### 4.4 HS Connectors (8 WKZ)

#### Kontakt 24.359.120 (HS Connectors)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 545 | 4.00 mm² | **2.92 mm** | 5.17 mm | 5.25 mm | 6.70 mm | >500 N | 100% |
| 559 | 4.00 mm² | **2.92 mm** | 5.17 mm | 5.25 mm | 6.70 mm | >500 N | 100% |
| 567 | 4.00 mm² | **2.92 mm** | 5.17 mm | 5.25 mm | 6.70 mm | >500 N | 100% |
| 568 | 4.00 mm² | **2.92 mm** | 5.17 mm | 5.25 mm | 6.70 mm | >500 N | 100% |

#### Kontakt 24.360.110 (HS Connectors)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 563 | 0.75 mm² | **1.65 mm** | 2.69 mm | - | - | - | 90% |
| 563 | 1.00 mm² | **1.75 mm** | 2.70 mm | 3.20 mm | 3.00 mm | 180 N | 100% |
| 571 | 0.75 mm² | **1.65 mm** | 2.69 mm | - | - | - | 90% |
| 571 | 1.00 mm² | **1.75 mm** | 2.70 mm | 3.20 mm | 3.00 mm | 180 N | 100% |

#### Kontakt 26.325.120 (HS)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 665 | 2.50 mm² | **1.96 mm** | 3.08 mm | 3.97 mm | 4.47 mm | 280 N | 100% |

#### Kontakt 91.403.120 (HS)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 720 | 0.34 mm² | **1.02 mm** | 1.28 mm | 1.50 mm | 1.92 mm | 50 N | 100% |

---

### 4.5 Molex / HHC (8 WKZ)

#### Kontakt 43030-0001 (Molex)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 701 | 0.13 mm² (AWG 26) | **0.80 mm** | 1.45 mm | 1.60 mm | 1.84 mm | 30 N | 100% |
| 701 | 0.21 mm² (AWG 24) | **0.85 mm** | 1.45 mm | 1.62 mm | 1.86 mm | 50 N | 100% |
| 724 | 0.13 mm² (AWG 26) | **0.80 mm** | 1.45 mm | - | - | - | 100% |
| 724 | 0.21 mm² (AWG 24) | **0.85 mm** | 1.45 mm | - | - | - | 100% |

#### Kontakt 08-50-0187 (Molex)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 625 | 0.34 mm² | **1.12 mm** | 2.01 mm | 2.70 mm | 2.47 mm | 100 N | 95% |
| 626 | 0.34 mm² | **1.12 mm** | 2.01 mm | 2.70 mm | 2.47 mm | 100 N | 95% |

> ⚠️ **Hinweis:** WKZ 626 ist DUPLIKAT von WKZ 625!

#### Kontakt 76823-0321 (Molex)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Abzug | Conf |
|-----|-------------|-----------|-------------|-------|------|
| 704 | 1.50 mm² | **1.56 mm** | 2.66 mm | 250 N | 100% |

#### Kontakt 505431-1300 (Molex) - Micro-Lock Plus 1.25
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Abzug | Conf |
|-----|-------------|-----------|-------------|-------|------|
| 729 | 0.05 mm² (AWG 30) | **0.46-0.51 mm** | 0.86 mm | 4.9 N | 100% |
| 729 | 0.08 mm² (AWG 28) | **0.49-0.54 mm** | 0.91 mm | 9.8 N | 100% |
| 729 | 0.12 mm² (AWG 26) | **0.54-0.59 mm** | - | 19.6 N | 100% |

> ⚠️ **WARNUNG WKZ 729:** Nur Isolation von 0.75mm - max. 0.96mm verarbeitbar!

---

### 4.6 Stocko (12 WKZ)

#### Kontakt RSB 7791 V-6 (Stocko)
| WKZ | Querschnitt | Bemerkung | Conf |
|-----|-------------|-----------|------|
| 503 | 4.00-6.00 mm² | VT-Satz + 2-fach-Clip Umbausatz | 60% |
| 514 | 4.00-6.00 mm² | VT-Satz, nicht ohne Kontakte crimpen! | 60% |

#### Kontakt RSB 7603 (Stocko)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 555 | 0.75 mm² | **1.35 mm** | 2.24 mm | 2.53 mm | 3.22 mm | 145 N | 100% |

#### Kontakt S0.106.604 (Stocko)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 650 | 0.75-1.00 mm² | **1.27 mm** | 1.62 mm | 2.88 mm | 2.91 mm | 145 N | 100% |

#### Kontakt RFB 7808 (Stocko)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 700 | 0.14 mm² | **0.80 mm** | 1.45 mm | 1.45 mm | 1.97 mm | 35 N | 100% |
| 700 | 0.25 mm² | **0.85 mm** | 1.46 mm | 1.45 mm | 1.97 mm | - | 100% |
| 700 | 0.50 mm² | **0.98 mm** | 1.47 mm | 1.45 mm | 1.97 mm | - | 100% |

---

### 4.7 Amphenol (5 WKZ)

#### Kontakt TNO1/0201600021 (Amphenol)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 616 | 0.50 mm² | **1.25 mm** | 2.23 mm | 2.87 mm | 3.22 mm | 95 N | 95% |
| 616 | 0.75 mm² | **1.31 mm** | 2.24 mm | 3.07 mm | 3.27 mm | 140 N | 95% |
| 616 | 1.50 mm² | **1.50 mm** | 2.28 mm | 3.46 mm | 3.38 mm | 210 N | 95% |

#### Kontakt TTN 01/0201600021 (Amphenol)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 703 | 0.50 mm² | **1.25 mm** | 2.23 mm | 2.87 mm | 3.22 mm | 100 N | 100% |
| 703 | 0.75 mm² | **1.31 mm** | 2.24 mm | - | - | - | 95% |
| 703 | 1.50 mm² | **1.48 mm** | 2.28 mm | - | - | - | 95% |

#### Kontakt EN 0202500431 (Amphenol) ⚠️
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 713 | 5.67 mm² | **2.55 mm** | 2.72 mm | 4.63 mm | 4.50 mm | 300 N | 100% |
| 713 | 4.25 mm² | **2.75 mm** | 2.72 mm | 3.78 mm | 4.60 mm | 350 N | 100% |

> ⚠️ **WARNUNG WKZ 713:** Isolationsdurchmesser bei beiden Litzen zu groß gewählt!

---

### 4.8 Deutsch (2 WKZ)

#### Kontakt 1060-16-0622 (Deutsch)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 581 | 0.75 mm² | **1.25 mm** | 2.07 mm | 2.40 mm | 2.54 mm | 140 N | 100% |
| 581 | 1.00 mm² | **1.30 mm** | 2.08 mm | 2.40 mm | 2.54 mm | 170 N | 100% |

#### Kontakt 1062-12-0166 (Deutsch)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 581 | 2.50 mm² | **1.92 mm** | 3.20 mm | 3.52 mm | 4.15 mm | 350 N | 100% |

---

### 4.9 Harting (1 WKZ)

#### Kontakt 0 905 000 9562 (Harting)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 656 | 0.36 mm² | **1.40 mm** | 2.35 mm | 2.60 mm | 2.84 mm | 130 N | 100% |
| 656 | 0.75 mm² | **1.40 mm** | 2.35 mm | 2.85 mm | 2.85 mm | 130 N | 100% |
| 656 | 1.50 mm² | **1.65 mm** | 2.38 mm | 2.75 mm | 2.85 mm | 260 N | 100% |

---

### 4.10 Kostal (3 WKZ)

#### Kontakt 32124734000 (Kostal)
| WKZ | Querschnitt | Crimphöhe | Conf |
|-----|-------------|-----------|------|
| 726 | 0.25 mm² | **0.82 mm** | 95% |

#### Kontakt 32124734010 (Kostal)
| WKZ | Querschnitt | Crimphöhe | Conf |
|-----|-------------|-----------|------|
| 727 | 0.35 mm² | **0.78 mm** | 95% |

#### Kontakt 32124734020 (Kostal)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Conf |
|-----|-------------|-----------|-------------|------|
| 728 | 0.50 mm² | **0.92 mm** | 1.65 mm | 100% |

---

### 4.11 Hirose (1 WKZ)

#### Kontakt DF3-2428-SCF (Hirose)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Conf |
|-----|-------------|-----------|-------------|----------|------|
| 716 | 0.14 mm² | **0.65 mm** | 1.22 mm | 1.60 mm | 100% |
| 716 | 0.25 mm² | **0.70 mm** | 1.22 mm | 1.60 mm | 100% |

---

### 4.12 LAT / HS (4 WKZ)

#### Kontakt 24810 (LAT/HS)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 549 | 0.50 mm² | **1.30 mm** | 2.27 mm | 2.70 mm | 3.30 mm | 95 N | 100% |
| 549 | 0.75 mm² | **1.38 mm** | 2.28 mm | 2.75 mm | 3.33 mm | 135 N | 100% |
| 549 | 1.00 mm² | **1.46 mm** | 2.29 mm | 3.00 mm | 3.33 mm | 185 N | 100% |

#### Kontakt 22818127 (LAT/HS)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 621 | 0.34 mm² | **0.92 mm** | 1.36 mm | 1.55 mm | 1.95 mm | 80 N | 95% |

#### Kontakt 21107 (LAT)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Conf |
|-----|-------------|-----------|-------------|----------|------------|------|
| 583 | 0.14 mm² | **1.01 mm** | 1.61 mm | 1.68 mm | 2.01 mm | 100% |
| 583 | 0.22 mm² | **1.05 mm** | 1.62 mm | 1.70 mm | 2.02 mm | 100% |
| 583 | 0.34 mm² | **1.12 mm** | 1.63 mm | 1.80 mm | 2.03 mm | 100% |

#### Kontakt 21600 (LAT/HSH)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Conf |
|-----|-------------|-----------|-------------|------|
| 589 | 10.00 mm² | **4.30 mm** | 4.87 mm | 100% |

---

### 4.13 Inarca (2 WKZ)

#### Kontakt 0011332101 (Inarca)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 588 | 1.00 mm² | **1.35 mm** | 2.35 mm | 2.80 mm | 3.48 mm | 185 N | 100% |

#### Kontakt 0011116101 (Inarca)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 658 | 1.00 mm² | **1.30 mm** | 2.55 mm | 2.80 mm | 3.72 mm | 190 N | 100% |

---

### 4.14 APTIV (2 WKZ)

#### Kontakt 35072391 (APTIV)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 695 | 0.50 mm² | **0.85 mm** | 1.53 mm | 1.30 mm | 1.85 mm | 90 N | 100% |

#### Kontakt 962943 (APTIV)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 695 | 1.00 mm² | **1.51 mm** | 2.02 mm | 2.22 mm | 2.52 mm | 120 N | 100% |

#### Kontakt 35088739 (APTIV)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 696 | 0.50 mm² | **0.89 mm** | 1.54 mm | 1.85 mm | 1.73 mm | 90 N | 100% |

---

### 4.15 HATKO/KM (1 WKZ)

#### Kontakt TMHTC009K2J001956 (HATKO/KM)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Abzug | Conf |
|-----|-------------|-----------|-------------|-------|------|
| 619 | 1.00 mm² | **1.50 mm** | 3.10 mm | 18.63 N | 95% |
| 619 | 1.50 mm² | **1.60 mm** | 3.10 mm | 29.04 N | 95% |
| 619 | 2.50 mm² | **1.80 mm** | 3.10 mm | 32.62 N | 95% |

---

### 4.16 KTK / Alexander Herter (4 WKZ)

#### Kontakt 0010129005 (KTK)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Conf |
|-----|-------------|-----------|-------------|----------|------------|------|
| 532 | 2.40 mm² | **2.02 mm** | 3.00 mm | 3.60 mm | 4.20 mm | 95% |

#### Kontakt Buchsenkontakt (KTK)
| WKZ | Querschnitt | Crimphöhe | Conf | Warnung |
|-----|-------------|-----------|------|---------|
| 614 | 0.50-1.00 mm² | **1.30-1.50 mm** | 80% | ⚠️ Bei 125N reißt Steckbereich ab! |
| 725 | 1.75 mm² | - | 60% | Doppelcrimp 0.75 + 1.00 mm² |

---

### 4.17 AWM Weidner (4 WKZ)

#### Kontakt 25258 (G+H via AWM)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 546 | 2.50 mm² | **2.05 mm** | 3.50 mm | 4.20 mm | 4.80 mm | 380 N | 95% |

#### Kontakt 26305.110 (Hans Schatz via AWM)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 537 | 0.25 mm² | **1.32 mm** | 1.80 mm | 2.10 mm | 2.50 mm | 50 N | 100% |

#### Kontakt 25775 (AWM)
| WKZ | Querschnitt | Crimphöhe | Conf |
|-----|-------------|-----------|------|
| 721 | - | - | 50% |

> ⚠️ **HINWEIS WKZ 721, 723:** Crimptabellen nicht extrahierbar - manuelle Prüfung erforderlich

---

### 4.18 Lumberg (1 WKZ)

#### Kontakt 3111 03 G (Lumberg)
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Conf |
|-----|-------------|-----------|-------------|------|
| 637 | 0.14 mm² | **0.78 mm** | 1.20 mm | 95% |
| 637 | 0.22 mm² | **0.85 mm** | 1.22 mm | 95% |
| 637 | 0.34 mm² | **0.89 mm** | 1.24 mm | 95% |

---

### 4.19 Schäfer/APST Batch 16-18 (Ergänzungen)

#### Kontakt 25787 (GHW/Lear) - BATCH 16-17 Ergänzung
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 501 | 1.00 mm² | **1.34 mm** | 1.56 mm | 2.40 mm | 2.80 mm | 185 N | 100% |
| 517 | 1.00 mm² | **1.34 mm** | 1.56 mm | 2.40 mm | 2.80 mm | 185 N | 100% |
| 528 | 1.00 mm² | **1.34 mm** | 1.56 mm | 2.40 mm | 2.80 mm | 185 N | 100% |

#### Kontakt 25077 (Leer) - BATCH 16
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 522 | 2.50 mm² | **2.15 mm** | 3.30 mm | 4.00 mm | 4.50 mm | 350 N | 95% |

#### Kontakt 26.325.120 (HS) - BATCH 17
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Abzug | Conf |
|-----|-------------|-----------|-------------|----------|------------|-------|------|
| 535 | 2.50 mm² | **1.96 mm** | 3.20 mm | 3.80 mm | 4.30 mm | 350 N | 95% |

#### Kontakt RSB 8178.258 (Stocko) - BATCH 17
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Conf |
|-----|-------------|-----------|-------------|------|
| 533 | 1.50 mm² | **2.02 mm** | 3.00 mm | 90% |

#### Kontakt S0.106.604 (Stocko) - BATCH 18
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Conf |
|-----|-------------|-----------|-------------|------|
| 630 | 0.75+0.25 mm² | **1.27 mm** | 2.10 mm | 95% |

#### Kontakt 927827/AMP (APST) - BATCH 18
| WKZ | Querschnitt | Crimphöhe | Crimpbreite | Iso-Höhe | Iso-Breite | Conf |
|-----|-------------|-----------|-------------|----------|------------|------|
| 629 | 0.50 mm² | **1.55 mm** | 2.12 mm | 3.14 mm | 3.50 mm | 95% |

---

## 5. Werkzeuge mit unvollständigen Daten

### 5.1 PDF nicht vorhanden (12 WKZ)

| WKZ | Status |
|-----|--------|
| 562, 582, 591, 593, 594 | PDF fehlt im Archiv |
| 612, 613, 620, 622, 623, 628 | PDF fehlt im Archiv |
| 666-694 | Historische Lücke (29 WKZ) |

### 5.2 Manuelle Nacharbeit erforderlich (24 WKZ)

| WKZ | Batch | Problem | Status |
|-----|-------|---------|--------|
| 509 | 1 | OCR-Qualität unzureichend | manuell_nachtragen |
| 600, 601 | 8 | Schäfer-Anleitung ohne Crimpdaten | manuell_nachtragen |
| 610 | 9 | Crimpdaten teilweise beschädigt | manuell_nachtragen |
| 611 | 9 | Zuordnung Querschnitt/Crimphöhe unklar | manuell_nachtragen |
| 615, 617 | 9 | Crimpdaten-Felder leer | manuell_nachtragen |
| 652 | 11 | Kontakt 25036 verschrottet | manuell_nachtragen |
| 657 | 11 | PDF fragmentiert | manuell_nachtragen |
| 659-661 | 12 | Crimpdaten auf externem Datenblatt | datenblatt_pruefen |
| 662 | 12 | Kontakt verschrottet | pruefen_ob_aktiv |
| 698, 699 | 13 | Crimpbreite/PDF-Encoding problematisch | manuell_nachtragen |
| 708, 711, 714 | 14 | Crimptabelle nicht lesbar | manuell_nachtragen |
| 718 | 15 | VT-Satz für 7 Kontakte, keine Crimpdaten | datenblatt_pruefen |
| 721, 723 | 15 | AWM Weidner Tabelle nicht lesbar | manuell_nachtragen |
| 722 | 15 | Tyco Applicator ohne Crimpdaten | tyco_doku_anfordern |
| 725 | 15 | Doppelcrimp unvollständig | manuell_nachtragen |
| 508 | 16 | HANKE-Format nicht lesbar | manuell_nachtragen |
| 519, 521 | 16 | Crimphöhen nicht angegeben | manuell_nachtragen |
| 523, 524 | 16 | AWM Weidner nicht extrahierbar | manuell_nachtragen |
| 526 | 16 | Crimphöhen fehlen | manuell_nachtragen |
| 529, 534 | 17 | PDF-Qualität schlecht / Format anders | manuell_pruefen |
| 530, 531 | 17 | PDF komplett unleserlich | kritisch_pruefen |
| 631, 633 | 18 | Crimphöhen nicht im Dokument / schlecht lesbar | manuell_nachtragen |
| 643, 647, 648 | 18 | Nur Ersatzteillisten, keine Crimpdaten | ersatzteile |

### 5.3 Verschrottete Werkzeuge (7 WKZ) - NICHT VERWENDEN

| WKZ | Kontakt | Batch | Verschrottungsdatum |
|-----|---------|-------|---------------------|
| 632 | 179955-2 | 18 | KW 48/2024 |
| 634 | 163081/083 | 18 | KW 50/2023 |
| 635 | 163085 | 18 | KW 48/2024 |
| 636 | 39-00-0077 | 18 | - (Querschnitt zu groß) |
| 640 | 25036 | 18 | - |
| 705 | 0906 000 9561 | 14 | 2013 |
| 709 | 16-02-0086 | 14 | KW 48/2024 |

---

## 6. Querverweise

### 6.1 Verwandte Dokumente

| Dokument | Beschreibung |
|----------|--------------|
| TM_WKZ_Werkzeuge.md | Werkzeug-Stammdaten |
| TM_CORE_Maschinen_Anlagen.md | Maschinen-Inventar |
| QM_PMV_Prüfmittelverwaltung.md | Prüfmittel, Kalibrierung |
| QM_REK_Reklamationsmanagement.md | 8D-Reports |

### 6.2 Lookup-Dateien

| Datei | Version | Zweck |
|-------|---------|-------|
| wkz_crimpdaten_master.json | **v3.4-FINAL** | Master-Datei (180 WKZ, 233 Varianten) |
| kontakt_wkz_crimp_lookup.json | **v2.0** | Kontakt→WKZ Suche (49 Kontakte) |

---

## 7. Änderungshistorie

| Version | Datum | Autor | Änderung |
|---------|-------|-------|----------|
| **2.0** | **2025-12-17** | **AL** | **MAJOR UPDATE: Batch 16-18 integriert, v3.4-FINAL** |
| 1.0 | 2025-12-17 | AL | Erstversion - 15 Batches konsolidiert |

### Details Version 2.0:

**Neue Daten aus wkz_crimpdaten_master.json v3.4-FINAL:**
- ✅ **+39 neue Werkzeuge:** Batch 16 (13), Batch 17 (11), Batch 18 (15)
- ✅ **Statistik aktualisiert:** 180 WKZ, 233 Varianten, 49 Kontakte
- ✅ **Verschrottete WKZ erweitert:** 2 → 7 Einträge (632, 634, 635, 636, 640)
- ✅ **Neue Hersteller-Sektionen:** 4.16 KTK, 4.17 AWM Weidner, 4.18 Lumberg, 4.19 APST Batch 16-18
- ✅ **Problematische WKZ aktualisiert:** Liste aus Master übernommen
- ✅ **Querverweise aktualisiert:** Master v3.4-FINAL, Lookup v2.0

**Datenquellen:**
- wkz_crimpdaten_master_v3.4_FINAL.json (Batch 1-18, 180 WKZ)
- kontakt_wkz_crimp_lookup_v2.0.json (49 Kontakte)

---

## 8. Verantwortlichkeiten

| Rolle | Person | Aufgabe |
|-------|--------|---------|
| QM-Manager | AL | Dokumentenpflege, Freigabe |
| Technik | MD | Werkzeugdaten-Pflege |
| Prüffeld | SK | Crimpdaten-Validierung |

---

*Dokument erstellt gemäß NULL-FEHLER-POLITIK der Rainer Schneider Kabelsatzbau GmbH & Co. KG*

**[OSP] [TM] [WKZ] [QM] [KST]** | (C: 100%) | Version 2.0 | Basis: wkz_crimpdaten_master v3.4-FINAL
