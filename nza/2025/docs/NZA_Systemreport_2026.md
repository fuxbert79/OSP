# Nach- und Zusatzarbeiten-System (NZA)

## Systemreport für Geschäftsleitung und QM-Audit

**Dokumenten-Nr.:** NZA-REP-2026-001
**Version:** 1.0
**Datum:** 02.02.2026
**Ersteller:** Andreas Löhr, Qualitätsmanager
**Freigabe:** [Geschäftsleitung]
**Vertraulichkeit:** Intern

---

## 1. Management Summary

Das Nach- und Zusatzarbeiten-System (NZA) ist ein webbasiertes System zur digitalen Erfassung, Kostenberechnung und Auswertung von internen Nacharbeiten, Neufertigungen und Ausschuss. Es wurde im Januar 2026 produktiv eingeführt und ermöglicht erstmals eine vollständige Transparenz über interne Fehlerkosten.

**Kernnutzen:**
- Vollständige Erfassung aller internen Qualitätskosten
- Automatische Kostenberechnung nach Kostenstellen-Minutensätzen
- Verursacher-Zuordnung für gezielte Qualifizierungsmaßnahmen
- Echtzeit-KPIs für Kostencontrolling und kontinuierliche Verbesserung
- ISO 9001:2015 konforme Dokumentation interner Nichtkonformitäten

**Status:** Produktiv seit 30.01.2026

---

## 2. Systembeschreibung

### 2.1 Zweck und Anwendungsbereich

Das NZA-System dient der systematischen Erfassung und Auswertung von:
- **Nacharbeit:** Korrektur fehlerhafter Teile (reparierbar)
- **Neufertigung:** Komplette Neuproduktion (nicht reparierbar)
- **Ausschuss:** Verworfene Teile ohne Nacharbeitsmöglichkeit

**ISO 9001:2015 Bezug:**
- Kapitel 8.7: Steuerung nichtkonformer Ergebnisse
- Kapitel 10.2: Nichtkonformität und Korrekturmaßnahmen
- Kapitel 9.1.3: Analyse und Bewertung (interne Qualitätskosten)

### 2.2 Abgrenzung zu RMS

| Aspekt | RMS (Reklamationen) | NZA (Nacharbeiten) |
|--------|---------------------|---------------------|
| **Ursprung** | Extern (Kunde/Lieferant) | Intern (Fertigung) |
| **Verursacher** | Extern | Intern (Mitarbeiter) |
| **Kostenerfassung** | Optional | Obligatorisch |
| **Mengengerüst** | ~150/Jahr | ~300-500/Jahr |
| **Formblatt** | F-QM-02, 03, 14 | F-QM-04 |

### 2.3 Benutzergruppen

| Rolle | Zugriff | Aufgaben |
|-------|---------|----------|
| QM-Manager | Vollzugriff | Erfassung, Auswertung, Administration |
| Fertigungsleiter | Vollzugriff | Erfassung, Maßnahmen, Kostenüberwachung |
| Geschäftsleitung | Lesezugriff | KPI-Überwachung, Kostencontrolling |
| Schichtführer | Erfassung | NZA-Vorgänge anlegen |
| Mitarbeiter | Dashboard | Einsicht in eigene Vorgänge |

### 2.4 Funktionsumfang

| Funktion | Beschreibung |
|----------|--------------|
| **Erfassung** | NZA-Vorgänge mit Typ, Artikel, Verursacher, Beschreibung |
| **Prozesserfassung** | Bis zu 5 Arbeitsprozesse pro Vorgang mit Zeiten |
| **Kostenberechnung** | Automatisch nach KST-Minutensätzen |
| **Materialkosten** | Zusätzliche Material- und Sonstkosten erfassbar |
| **Fehlerfotos** | Bildupload zur Dokumentation (bis 20 MB) |
| **Maßnahmen** | Korrekturmaßnahmen mit Teams-Benachrichtigung |
| **Dashboard** | Echtzeit-Übersicht mit KPIs und Filteroptionen |
| **Archiv** | Jahresweise Archivierung |

### 2.5 Technische Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                      Benutzer (Browser)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Web-Dashboard (HTML/JavaScript)              │
│                 https://osp.schneider-kabelsatzbau.de/nza/   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Nginx Reverse Proxy                       │
│                    (SSL/TLS verschlüsselt)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                n8n Workflow-Automatisierung                  │
│                    (12 API-Workflows)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Microsoft 365 / SharePoint Online               │
│     - nza-kpl (Hauptliste, 52 Felder)                       │
│     - nza-massnahmen (Korrekturmaßnahmen)                   │
│     - nza-bilder (Fehlerfotos)                              │
│     - nza-mitarbeiter (53 MA)                               │
│     - nza-config (Systemkonfiguration)                      │
│     - Dokumentenablage (/sites/NZA_NEU/)                    │
└─────────────────────────────────────────────────────────────┘
```

**Hosting:** Dedizierter Server (Hetzner CX43, Standort Deutschland)
**Datenhaltung:** Microsoft 365 SharePoint (EU-Rechenzentrum)
**Verschlüsselung:** TLS 1.3, Let's Encrypt Zertifikat

---

## 3. Kostenmodell

### 3.1 Minutensätze nach Kostenstellen

Die Kostenberechnung basiert auf den kalkulierten Minutensätzen der Kostenstellen:

| Kostenstelle | Bereich | €/Minute | €/Stunde |
|--------------|---------|----------|----------|
| **1000** | Fertigung F1 | 1,98 | 118,80 |
| **2000** | Fertigung F2 | 1,21 | 72,60 |
| **3000** | Fertigung F3 | 0,93 | 55,80 |
| **4000** | Fertigung F4 | 1,02 | 61,20 |
| **5000** | Fertigung F5 | 1,02 | 61,20 |
| **Lager** | Lagerbereich | 1,10 | 66,00 |
| **Verwaltung** | Administration | 1,37 | 82,20 |

### 3.2 Kostenberechnung

```
Prozesskosten = Σ (Zeit_i × Minutensatz_KST_i × Faktor_i)

Gesamtkosten = Prozesskosten + Materialkosten + Sonstige Kosten
```

**Faktoren:**
- Standard: 1,0
- Erhöht (z.B. Sondermaschine): 1,5
- Reduziert (z.B. Lehrling): 0,5

### 3.3 Prozesserfassung (max. 5 pro Vorgang)

| Feld | Beschreibung |
|------|--------------|
| Prozess | Tätigkeit (z.B. "Abisolieren", "Crimpen", "Montage") |
| Werker | Ausführender Mitarbeiter (MA-Kürzel) |
| KST | Kostenstelle der Tätigkeit |
| Zeit | Aufgewendete Zeit in Minuten |
| Faktor | Kostenfaktor (Standard: 1,0) |
| Kosten | Automatisch berechnet |

---

## 4. Prozessablauf

### 4.1 NZA-Erfassung

```
Fehler erkannt                E-Mail-Eingang
(Fertigung)                   (nza@...)
        │                          │
        ▼                          ▼
┌─────────────────────────────────────────┐
│           NZA anlegen                    │
│  - NZA-ID vergeben (NZA-JJ-XXXX)        │
│  - Typ: Nacharbeit/Neufertigung/Ausschuss│
│  - Artikel, Menge, Verursacher          │
│  - Fehlerbeschreibung                   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│        Fehlerfotos hochladen            │
│  - Dokumentation des Fehlerbildes       │
│  - Max. 20 MB pro Bild                  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│        Prozesse erfassen                │
│  - Tätigkeiten mit Zeiten              │
│  - Automatische Kostenberechnung       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Maßnahmen definieren               │
│  - Korrekturmaßnahme                   │
│  - Termin + Verantwortlicher           │
│  - Teams-Benachrichtigung              │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Abschluss                       │
│  - Status: Abgeschlossen               │
│  - Kosten in KPI aggregiert            │
└─────────────────────────────────────────┘
```

### 4.2 Kennzahlen (KPIs)

| KPI | Beschreibung | Zielwert |
|-----|--------------|----------|
| **Gesamtkosten/Monat** | Summe aller NZA-Kosten | < Budget |
| **Kosten/KST** | Aufschlüsselung nach Kostenstellen | Trend sinkend |
| **Vorgänge/Monat** | Anzahl NZA-Vorgänge | Trend sinkend |
| **Ø Kosten/Vorgang** | Durchschnittliche Kosten | < 100 EUR |
| **Top-Verursacher** | MA mit häufigsten NZA | Schulungsbedarf |
| **Top-Fehlerarten** | Häufigste Fehlerursachen | Prozessoptimierung |
| **Ausschussquote** | Anteil Ausschuss an Gesamt | < 10% |

---

## 5. Vorteile des Systems

### 5.1 Kostencontrolling

| Vorteil | Beschreibung |
|---------|--------------|
| **Vollständige Erfassung** | Erstmals alle internen Fehlerkosten transparent |
| **Automatische Berechnung** | Keine manuellen Kalkulationen mehr nötig |
| **KST-Auswertung** | Kosten pro Kostenstelle sofort sichtbar |
| **Budgetüberwachung** | Monatliche Entwicklung verfolgbar |
| **Verursacherprinzip** | Kosten dem Entstehungsort zuordenbar |

### 5.2 Qualitätsverbesserung

| Vorteil | Beschreibung |
|---------|--------------|
| **Fehleranalyse** | Systematische Auswertung von Fehlerarten |
| **Verursacher-Tracking** | Gezielte Qualifizierungsmaßnahmen möglich |
| **Maßnahmenverfolgung** | Korrekturmaßnahmen mit Terminkontrolle |
| **Fotodokumentation** | Fehlerbilder für Schulungen nutzbar |
| **Trendanalysen** | Entwicklung über Zeit erkennbar |

### 5.3 Effizienz

| Vorteil | Beschreibung |
|---------|--------------|
| **Schnelle Erfassung** | Intuitive Oberfläche, wenige Klicks |
| **Verursacher-Lookup** | 53 Mitarbeiter mit Autovervollständigung |
| **Teams-Integration** | Automatische Benachrichtigungen |
| **Zentrale Ablage** | Alle Daten an einem Ort |
| **Echtzeit-Dashboard** | Keine manuelle Auswertung nötig |

---

## 6. Einschränkungen und Risiken

### 6.1 Technische Einschränkungen

| Einschränkung | Beschreibung | Maßnahme |
|---------------|--------------|----------|
| **Internetabhängig** | System erfordert Internetverbindung | Keine Offline-Erfassung |
| **Microsoft 365** | Abhängigkeit von M365-Verfügbarkeit | SLA von Microsoft (99,9%) |
| **Bildgröße** | Max. 20 MB pro Foto | Komprimierung vor Upload |

### 6.2 Organisatorische Einschränkungen

| Einschränkung | Beschreibung | Maßnahme |
|---------------|--------------|----------|
| **Disziplin** | Konsequente Erfassung aller NZA erforderlich | Prozessanweisung verbindlich |
| **Zeiterfassung** | Zeiten müssen realistisch geschätzt werden | Schulung der Erfasser |
| **Minutensätze** | Jährliche Aktualisierung erforderlich | Controlling einbinden |

### 6.3 Risiken

| Risiko | Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|--------|-------------------|------------|---------------|
| Unvollständige Erfassung | Mittel | Hoch | Stichprobenkontrollen |
| Falsche Zeitangaben | Mittel | Mittel | Plausibilitätsprüfungen |
| Verursacher-Widerstand | Mittel | Gering | Konstruktive Kommunikation |
| Systemausfall | Gering | Mittel | Manuelle Nacherfassung |

---

## 7. ISO 9001:2015 Konformität

### 7.1 Erfüllte Normforderungen

| Kapitel | Anforderung | Umsetzung im NZA |
|---------|-------------|------------------|
| **8.7** | Steuerung nichtkonformer Ergebnisse | Erfassung, Kennzeichnung, Dokumentation |
| **10.2.1** | Reaktion auf Nichtkonformitäten | Korrekturmaßnahmen, Ursachenanalyse |
| **10.2.2** | Dokumentierte Information | NZA-Protokoll, Fotos, Maßnahmen |
| **9.1.3** | Analyse und Bewertung | KPI-Dashboard, Kostenauswertung |
| **7.1.4** | Prozessumgebung | Fehlerfotos dokumentieren Umgebung |

### 7.2 Nachweisführung für Audits

Das System ermöglicht die sofortige Bereitstellung folgender Nachweise:

- Liste aller NZA-Vorgänge (filterbar nach Zeitraum, Typ, KST, Verursacher)
- Einzelne NZA-Akten mit vollständiger Dokumentation
- Fehlerfotos als Bildnachweis
- Kostenauswertungen nach verschiedenen Kriterien
- Maßnahmenprotokolle mit Status
- Statistische Auswertungen (KPIs, Trends, Pareto)

---

## 8. Mitarbeiter-Stammdaten

### 8.1 Übersicht nach Kostenstellen

| Kostenstelle | Bereich | Anzahl MA | Fertigungsleiter |
|--------------|---------|-----------|------------------|
| **Verwaltung** | Administration | 9 | - |
| **1000** | Fertigung F1 | 5 | MD (Stv.: DS) |
| **2000** | Fertigung F2 | 9 | BS |
| **3000** | Fertigung F3 | 13 | BS (Stv.: IB) |
| **5000** | Fertigung F5 | 12 | DR (Stv.: SK) |
| **Lager** | Lagerbereich | 3 | OK |
| **Gesamt** | | **53** | |

### 8.2 Verursacher-Zuordnung

Jeder Mitarbeiter ist im System mit folgenden Daten hinterlegt:
- MA-Kürzel (2 Buchstaben)
- Vollständiger Name
- Kostenstelle
- Abteilung
- Funktion (Werker, Schichtführer, Fertigungsleiter)

---

## 9. Kennzahlen-Erwartung 2026

Basierend auf historischen Daten und dem Mengengerüst:

| KPI | Erwartung 2026 | Zielwert |
|-----|----------------|----------|
| NZA-Vorgänge gesamt | 300-500 | < 400 |
| Gesamtkosten | 30.000-50.000 EUR | < 40.000 EUR |
| Ø Kosten/Vorgang | 80-120 EUR | < 100 EUR |
| Nacharbeit-Anteil | 60-70% | - |
| Neufertigung-Anteil | 20-30% | - |
| Ausschuss-Anteil | 5-15% | < 10% |

---

## 10. Ausblick und Weiterentwicklung

### 10.1 Geplante Erweiterungen

| Funktion | Priorität | Geplant |
|----------|-----------|---------|
| RMS-Verknüpfung | Hoch | Q1/2026 |
| Automatischer E-Mail-Import | Mittel | Q2/2026 |
| F-QM-04 PDF-Generator | Mittel | Q2/2026 |
| Barcode-Erfassung | Niedrig | Q3/2026 |
| Mobile Erfassung | Niedrig | Q4/2026 |

### 10.2 Nächste Schritte

1. Erstellung Verfahrensanweisung (VA-QM-XX)
2. Schulung der Fertigungsleiter und Schichtführer
3. Pilotphase in KST 2000/3000
4. Rollout auf alle Kostenstellen
5. Integration in Management-Review-Prozess

---

## 11. API-Endpunkte (Technische Referenz)

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/nza/prozesse` | GET/POST/PATCH | CRUD für NZA-Vorgänge |
| `/api/nza/massnahmen` | GET/POST/PATCH | Korrekturmaßnahmen |
| `/api/nza/bilder` | GET | Fehlerfotos abrufen |
| `/api/nza/bilder-upload` | POST | Foto hochladen (max 20MB) |
| `/api/nza/mitarbeiter` | GET | Verursacher-Lookup |
| `/api/nza/kosten` | GET/POST | Kostenerfassung |
| `/api/nza/config` | GET | Systemkonfiguration |
| `/api/nza/kpis` | GET | Aggregierte Kennzahlen |
| `/api/nza/notify` | POST | Teams-Benachrichtigung |

---

## 12. Anlagen

- **Anlage A:** Bildschirmfotos Dashboard
- **Anlage B:** Formblatt F-QM-04 (NZA-Protokoll)
- **Anlage C:** Mitarbeiterliste mit KST-Zuordnung
- **Anlage D:** Minutensatz-Kalkulation
- **Anlage E:** Benutzerhandbuch (in Erstellung)
- **Anlage F:** Verfahrensanweisung (in Erstellung)

---

## 13. Freigabe

| Funktion | Name | Datum | Unterschrift |
|----------|------|-------|--------------|
| Ersteller | Andreas Löhr | 02.02.2026 | |
| Geprüft | | | |
| Freigegeben (GF) | | | |

---

**Dokumentenhistorie:**

| Version | Datum | Änderung | Autor |
|---------|-------|----------|-------|
| 1.0 | 02.02.2026 | Erstversion | AL |

---

*Dieses Dokument ist Eigentum der Rainer Schneider Kabelsatzbau GmbH & Co. KG und unterliegt dem internen Dokumentenmanagement.*
