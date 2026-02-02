# Reklamationsmanagementsystem (RMS)

## Systemreport für Geschäftsleitung und QM-Audit

**Dokumenten-Nr.:** RMS-REP-2026-001
**Version:** 1.0
**Datum:** 02.02.2026
**Ersteller:** Andreas Löhr, Qualitätsmanager
**Freigabe:** [Geschäftsleitung]
**Vertraulichkeit:** Intern

---

## 1. Management Summary

Das Reklamationsmanagementsystem (RMS) ist ein webbasiertes System zur digitalen Erfassung, Bearbeitung und Auswertung von Kunden- und Lieferantenreklamationen. Es wurde im Januar 2026 produktiv eingeführt und ersetzt die bisherige manuelle Ablage in Ordnerstrukturen.

**Kernnutzen:**
- Zentrale, digitale Erfassung aller Reklamationen
- Lückenlose Nachverfolgung von Korrekturmaßnahmen
- Automatisierte Erinnerungen bei Terminüberschreitungen
- Echtzeit-KPIs für Management-Review und kontinuierliche Verbesserung
- ISO 9001:2015 konforme Dokumentation

**Status:** Produktiv seit 27.01.2026

---

## 2. Systembeschreibung

### 2.1 Zweck und Anwendungsbereich

Das RMS dient der systematischen Bearbeitung von:
- **Kundenreklamationen:** Qualitätsbeanstandungen unserer Kunden
- **Lieferantenreklamationen:** Qualitätsabweichungen bei Zulieferteilen

**ISO 9001:2015 Bezug:**
- Kapitel 8.7: Steuerung nichtkonformer Ergebnisse
- Kapitel 10.2: Nichtkonformität und Korrekturmaßnahmen
- Kapitel 9.1.3: Analyse und Bewertung (Kundenzufriedenheit)

### 2.2 Benutzergruppen

| Rolle | Zugriff | Aufgaben |
|-------|---------|----------|
| QM-Manager | Vollzugriff | Erfassung, Bearbeitung, Auswertung, Administration |
| Geschäftsleitung | Lesezugriff | KPI-Überwachung, Management-Review |
| Abteilungsleiter | Lesezugriff + Maßnahmen | Umsetzung von Korrekturmaßnahmen |
| Mitarbeiter | Dashboard | Einsicht in relevante Reklamationen |

### 2.3 Funktionsumfang

| Funktion | Beschreibung |
|----------|--------------|
| **Erfassung** | Neue Reklamationen anlegen mit allen relevanten Daten |
| **Formblatt-Generator** | Automatische Erstellung von QM-Formblättern (F-QM-02, 03, 04, 14) |
| **Maßnahmenverfolgung** | Korrekturmaßnahmen mit Termin und Verantwortlichem |
| **Benachrichtigungen** | E-Mail/Teams-Benachrichtigung bei neuen Maßnahmen |
| **Erinnerungen** | Automatische Erinnerung bei Terminüberschreitung |
| **Dashboard** | Echtzeit-Übersicht mit KPIs und Filteroptionen |
| **Dateianhänge** | Verknüpfung mit SharePoint-Dokumenten |
| **Archiv** | Jahresweise Archivierung abgeschlossener Reklamationen |

### 2.4 Technische Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                      Benutzer (Browser)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Web-Dashboard (HTML/JavaScript)              │
│                 https://osp.schneider-kabelsatzbau.de/rms/   │
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
│                    (API-Endpunkte)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Microsoft 365 / SharePoint Online               │
│     - Reklamationen-2026 (Hauptliste)                       │
│     - RMS-Massnahmen (Maßnahmenliste)                       │
│     - Dokumentenablage (/sites/RMS/)                        │
└─────────────────────────────────────────────────────────────┘
```

**Hosting:** Dedizierter Server (Hetzner CX43, Standort Deutschland)
**Datenhaltung:** Microsoft 365 SharePoint (EU-Rechenzentrum)
**Verschlüsselung:** TLS 1.3, Let's Encrypt Zertifikat

---

## 3. Prozessablauf

### 3.1 Reklamationserfassung

```
E-Mail-Eingang              Manuelle Erfassung
(reklamation@...)           (Dashboard)
        │                          │
        ▼                          ▼
┌─────────────────────────────────────────┐
│         Reklamation anlegen             │
│  - QA-ID vergeben (QA-JJNNN)           │
│  - Typ: Kunde / Lieferant              │
│  - Absender, Artikel, Fehlerbeschreibung│
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Formblatt generieren               │
│  - F-QM-02 (Qualitätsabweichung)       │
│  - F-QM-03 (8D-Report)                 │
│  - F-QM-04 (NZA)                       │
│  - F-QM-14 (Korrekturmaßnahme)         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Maßnahmen definieren               │
│  - Sofortmaßnahme                       │
│  - Abstellmaßnahme                      │
│  - Termin + Verantwortlicher           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Wirksamkeitsprüfung               │
│  - Maßnahme umgesetzt?                 │
│  - Wiederholungsfehler ausgeschlossen? │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Abschluss                       │
│  - Status: Abgeschlossen               │
│  - Archivierung zum Jahresende         │
└─────────────────────────────────────────┘
```

### 3.2 Kennzahlen (KPIs)

| KPI | Beschreibung | Zielwert |
|-----|--------------|----------|
| **Abschlussquote** | Anteil abgeschlossener Reklamationen | > 90% |
| **Reaktionszeit** | Zeit bis zur ersten Maßnahme | < 5 Arbeitstage |
| **Reklamationsquote** | Reklamationen / 1000 Lieferungen | < 1,0 |
| **Wiederholungsrate** | Gleicher Fehler innerhalb 12 Monate | 0% |
| **8D-Quote** | Anteil mit vollständigem 8D-Report | > 50% (Kunden) |

---

## 4. Vorteile des Systems

### 4.1 Qualitätsmanagement

| Vorteil | Beschreibung |
|---------|--------------|
| **Lückenlose Dokumentation** | Jede Reklamation erhält eindeutige ID, alle Änderungen nachvollziehbar |
| **Standardisierte Formblätter** | Automatische Generierung normkonformer QM-Dokumente |
| **Maßnahmenverfolgung** | Termine und Verantwortlichkeiten transparent |
| **Eskalation** | Automatische Erinnerungen verhindern Terminüberschreitungen |
| **Audit-Readiness** | Alle Daten jederzeit abrufbar und filterbar |

### 4.2 Effizienz

| Vorteil | Beschreibung |
|---------|--------------|
| **Zeitersparnis** | Formblätter in Sekunden statt manueller Erstellung |
| **Zentrale Ablage** | Keine Suche in Ordnerstrukturen mehr |
| **Echtzeit-Übersicht** | Dashboard zeigt aktuellen Stand sofort |
| **Filterung** | Schnelles Finden nach Kunde, Artikel, Zeitraum |
| **Archivierung** | Automatische Jahresarchive für vergangene Perioden |

### 4.3 Transparenz

| Vorteil | Beschreibung |
|---------|--------------|
| **Management-Dashboard** | KPIs auf einen Blick für Führungskräfte |
| **Trendanalysen** | Monatliche Entwicklung sichtbar |
| **Top-Verursacher** | Identifikation von Schwerpunkten |
| **Abteilungsübergreifend** | Alle relevanten MA haben Zugriff |

---

## 5. Einschränkungen und Risiken

### 5.1 Technische Einschränkungen

| Einschränkung | Beschreibung | Maßnahme |
|---------------|--------------|----------|
| **Internetabhängig** | System erfordert Internetverbindung | Keine Offline-Nutzung möglich |
| **Microsoft 365** | Abhängigkeit von M365-Verfügbarkeit | SLA von Microsoft (99,9%) |
| **Browser-basiert** | Nur über Webbrowser nutzbar | Moderne Browser erforderlich |

### 5.2 Organisatorische Einschränkungen

| Einschränkung | Beschreibung | Maßnahme |
|---------------|--------------|----------|
| **Schulungsbedarf** | Benutzer müssen eingewiesen werden | Schulungsunterlagen erstellen |
| **Disziplin** | Konsequente Nutzung erforderlich | Prozessanweisung verbindlich |
| **Single Point of Contact** | QM-Manager als Hauptanwender | Vertretungsregelung definieren |

### 5.3 Risiken

| Risiko | Eintrittswahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
|--------|----------------------------|------------|---------------|
| Systemausfall | Gering | Mittel | Fallback auf manuelle Erfassung |
| Datenverlust | Sehr gering | Hoch | SharePoint-Backup durch Microsoft |
| Fehlbedienung | Mittel | Gering | Schulung, Benutzerhandbuch |
| Unbefugter Zugriff | Gering | Mittel | M365-Authentifizierung, HTTPS |

---

## 6. ISO 9001:2015 Konformität

### 6.1 Erfüllte Normforderungen

| Kapitel | Anforderung | Umsetzung im RMS |
|---------|-------------|------------------|
| **8.7** | Steuerung nichtkonformer Ergebnisse | Erfassung, Kennzeichnung (QA-ID), Dokumentation |
| **10.2.1** | Reaktion auf Nichtkonformitäten | Sofort- und Abstellmaßnahmen, Ursachenanalyse |
| **10.2.2** | Dokumentierte Information | Formblätter, Maßnahmenprotokoll, Archivierung |
| **9.1.2** | Kundenzufriedenheit | Auswertung Kundenreklamationen, Trendanalyse |
| **9.1.3** | Analyse und Bewertung | KPI-Dashboard, Management-Review-Daten |
| **7.5** | Dokumentierte Information | Lenkung, Aufbewahrung, Schutz gewährleistet |

### 6.2 Nachweisführung für Audits

Das System ermöglicht die sofortige Bereitstellung folgender Nachweise:

- Liste aller Reklamationen (filterbar nach Zeitraum, Typ, Status)
- Einzelne Reklamationsakten mit vollständiger Historie
- Maßnahmenprotokolle mit Terminen und Verantwortlichen
- Wirksamkeitsnachweise (Status der Maßnahmen)
- Statistische Auswertungen (KPIs, Trends, Pareto)
- Formblätter im Original (SharePoint-Dokumente)

---

## 7. Kennzahlen 2025 (Referenz)

Zur Veranschaulichung die Kennzahlen des abgeschlossenen Geschäftsjahres 2025:

| KPI | Wert | Bewertung |
|-----|------|-----------|
| Gesamtzahl Reklamationen | 27 | - |
| Kundenreklamationen | 16 (59%) | - |
| Lieferantenreklamationen | 11 (41%) | - |
| Abschlussquote | 96% | Ziel erreicht |
| Mit NZA-Dokumentation | 10 (37%) | - |
| Mit 8D-Report | 5 (19%) | - |
| NZA-Kosten gesamt | 3.846,73 EUR | - |

**Top-Absender 2025:**
1. Laserline (6 Reklamationen)
2. Püplichhuisen (3 Reklamationen)
3. Saurer (3 Reklamationen)

---

## 8. Ausblick und Weiterentwicklung

### 8.1 Geplante Erweiterungen

| Funktion | Priorität | Geplant |
|----------|-----------|---------|
| NZA-Integration | Hoch | Q1/2026 |
| Automatischer E-Mail-Import | Mittel | Q2/2026 |
| Lieferantenbewertung | Mittel | Q2/2026 |
| Mobile App | Niedrig | Q3/2026 |

### 8.2 Nächste Schritte

1. Erstellung Verfahrensanweisung (VA-QM-XX)
2. Schulung der Abteilungsleiter
3. Integration in Management-Review-Prozess
4. Jahresauswertung für Qualitätsbericht

---

## 9. Anlagen

- **Anlage A:** Bildschirmfotos Dashboard
- **Anlage B:** Formblatt-Muster (F-QM-02, 03, 04, 14)
- **Anlage C:** Benutzerhandbuch (in Erstellung)
- **Anlage D:** Verfahrensanweisung (in Erstellung)

---

## 10. Freigabe

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
