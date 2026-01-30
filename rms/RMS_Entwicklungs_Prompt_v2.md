# 🚀 RMS ENTWICKLUNGS-PROMPT v2.0

**Für:** Claude Desktop / Claude Code CLI  
**Stand:** 2025-12-20  
**Entwicklungszeitraum:** Max. 21 Tage  
**Go-Live:** 01.01.2026

---

## SYSTEM-KONTEXT

Du entwickelst das **RMS (Reklamationsmanagement-System)** für die **Rainer Schneider Kabelsatzbau GmbH & Co. KG**.

### Unternehmensprofil
- **Branche:** Kabelkonfektion / Kabelsatzfertigung
- **Mitarbeiter:** ~54
- **Zertifizierung:** ISO 9001:2015
- **Standards:** IPC-WHMA-A-620, DIN 72551

### Bestehende Infrastruktur
- **Server:** Hetzner CX43 (8 vCPU, 32GB RAM, 160GB NVMe)
- **IP:** 46.224.102.30
- **Stack:** Docker, Open WebUI v0.6.41, ChromaDB v0.5.15, n8n
- **Cloud:** Microsoft 365 (SharePoint, Outlook, Teams)
- **OSP-System:** Bestehendes RAG-Wissenssystem (integrieren, nicht duplizieren)

---

## PROJEKTANFORDERUNGEN

### Kernfunktionen

1. **Zentrales Dashboard** mit Live-Bearbeitungs-Status
2. **Detail-Ansicht** pro Reklamation:
   - Strukturierte Stammdaten
   - Foto-Galerie
   - Schriftverkehr-Timeline (E-Mail-Verlauf)
   - Individueller Maßnahmenplan
3. **Automatischer E-Mail-Import** aus Outlook (KI-gestützt)
4. **QM-Board Export** als HTML-Dashboard

### E-Mail-Postfächer
- `reklamation@schneider-kabelsatzbau.de` → Kunden-/Lieferanten-Reklamationen
- `nza@schneider-kabelsatzbau.de` → Interne NZA (Nach-/Zusatzarbeiten)

### Reklamationstypen
| Typ | Beschreibung | Bisherige ID | Neue ID |
|-----|--------------|--------------|---------|
| **INTERN** | NZA (Nach-/Zusatzarbeiten) | NZA-xxx | QA-JJNNN |
| **KUNDE** | Externe Kundenreklamationen | QA-xxx | QA-JJNNN |
| **LIEFERANT** | Lieferantenreklamationen | (neu) | QA-JJNNN |

### ID-System
**Format:** `QA-JJNNN`
- QA = Quality Action
- JJ = Jahr (25, 26, ...)
- NNN = Laufende Nummer (001-999)
- **Reset:** Jährlich am 01.01.

**Beispiele:**
- QA-25087 (letzte Rekla 2025)
- QA-26001 (erste Rekla 2026)

---

## MIGRATIONSPLAN

### Stichtag: 01.01.2026

| Zeitraum | Aktion |
|----------|--------|
| **Bis 31.12.2025** | Alle 2025er Reklas ins neue RMS migrieren |
| **Ab 01.01.2026** | Neues System produktiv, neue IDs ab QA-26001 |

### Migrations-Regeln
- **Bestehende IDs bleiben erhalten** (QA-25xxx, NZA-xxx werden NICHT umbenannt)
- Neue Reklas ab 2026 erhalten QA-26001+
- Das System muss beide ID-Formate unterstützen (Legacy + Neu)

---

## ZUGRIFFSRECHTE

**Management:** Microsoft 365 / Azure AD

| Rolle | Berechtigung | M365-Gruppe |
|-------|--------------|-------------|
| **QM-Manager (AL)** | Vollzugriff | RMS-Admins |
| **Abteilungsleiter** | Lesen + Bearbeiten eigene KST | RMS-Editors |
| **Mitarbeiter** | Nur Lesen (eigene Reklas) | RMS-Viewers |

---

## SHAREPOINT-INTEGRATION

### Neue Teamwebsite: "RMS Reklamationsmanagement"

**Struktur:**
```
RMS-Reklamationsmanagement/
├── Dokumente/
│   ├── 2025/
│   │   ├── QA-25001/
│   │   │   ├── Fotos/
│   │   │   ├── Schriftverkehr/
│   │   │   └── 8D-Report.pdf
│   │   └── QA-25002/
│   └── 2026/
│       └── QA-26001/
├── Listen/
│   └── Reklamationen (SharePoint List für Backup/Sync)
└── Seiten/
    ├── Dashboard.aspx (HTML-Embed)
    └── Anleitung.aspx
```

### Automatische Ordner-Erstellung
Bei jeder neuen Reklamation:
1. Jahr-Ordner prüfen/erstellen
2. QA-ID-Ordner erstellen
3. Unterordner: Fotos/, Schriftverkehr/

---

## E-MAIL-IMPORT (KI-gestützt)

### Workflow
```
Neue E-Mail → n8n Webhook → KI-Analyse → RMS-API → SharePoint
```

### KI-Analyse extrahiert:
| Feld | Extraktion aus |
|------|----------------|
| **Typ** | Absender-Domain, Betreff-Keywords |
| **Priorität** | "dringend", "sofort", Eskalationswörter |
| **Artikel-Nr.** | Regex: [A-Z]{2,3}-[0-9]{5,8} |
| **Auftrag-Nr.** | Regex: AU-[0-9]{6} |
| **Beschreibung** | E-Mail-Body (erste 500 Zeichen) |
| **Anhänge** | Automatisch nach SharePoint |

### Klassifizierung
| Postfach | Standard-Typ | Überschreibbar |
|----------|--------------|----------------|
| reklamation@ | KUNDE | Ja, wenn Lieferant erkannt |
| nza@ | INTERN | Nein |

---

## INTEGRATIONEN

### 1. OSP-System (bestehendes RAG)
- **Keine neue ChromaDB-Instanz** - bestehende nutzen
- WKZ-Lookup: Kontakt-Nr. → Werkzeug-Info
- HR-Lookup: MA-Kürzel validieren
- QM-Wissen: Fehlercluster, 8D-Hilfe

### 2. Microsoft 365
- **Outlook:** Graph API für E-Mail-Import
- **Teams:** Benachrichtigungen bei neuen Reklas
- **Kalender:** Maßnahmen-Termine synchronisieren

### 3. n8n
- E-Mail-Import Workflow
- Termin-Reminder
- Status-Benachrichtigungen

### 4. Timeline ERP (später)
- Artikel-Stammdaten
- Auftrags-Verknüpfung

---

## TECH-STACK

| Komponente | Technologie | Begründung |
|------------|-------------|------------|
| **Frontend** | React 18 + shadcn/ui + Tailwind | Dashboard-Komplexität |
| **Backend** | Python FastAPI + SQLAlchemy 2.0 | Async, OSP-kompatibel |
| **Datenbank** | PostgreSQL 16 | Relational, ACID |
| **Queue** | Redis (optional) | Für E-Mail-Processing |
| **Hosting** | Docker auf Hetzner CX43 | Bestehende Infrastruktur |

### CI-Farben (VERBINDLICH)
```css
--schneider-blau: #003366;
--schneider-blau-hell: #0055A4;
--schneider-grau: #6B7280;
--success: #22C55E;
--warning: #F59E0B;
--error: #EF4444;
```

---

## DATENMODELL

### Haupt-Entitäten

```python
class Reklamation:
    id: UUID
    qa_id: str              # QA-26001 oder Legacy: NZA-xxx
    typ: Enum               # INTERN | KUNDE | LIEFERANT
    status: Enum            # NEU | IN_BEARBEITUNG | MASSNAHMEN | ABGESCHLOSSEN
    prioritaet: Enum        # NIEDRIG | MITTEL | HOCH | KRITISCH
    
    titel: str
    beschreibung: str
    
    erstellt_am: datetime
    erstellt_von: str       # MA-Kürzel
    verantwortlich: str     # Default: AL
    
    verursacher: Optional[str]
    betroffene_kst: Optional[str]
    artikel_nr: Optional[str]
    auftrag_nr: Optional[str]
    
    sharepoint_ordner: str  # /sites/RMS/Dokumente/2026/QA-26001
    
    abgeschlossen_am: Optional[datetime]
    root_cause: Optional[str]

class Korrespondenz:
    rekla_id: UUID
    datum: datetime
    richtung: Enum          # EINGANG | AUSGANG
    betreff: str
    inhalt: str
    absender: str
    empfaenger: str
    outlook_message_id: str
    anhang_pfade: List[str]

class Massnahme:
    rekla_id: UUID
    typ: Enum               # SOFORT | KORREKTUR | PRAEVENTION
    beschreibung: str
    verantwortlich: str
    termin: date
    status: Enum            # OFFEN | IN_ARBEIT | ABGESCHLOSSEN | UEBERFAELLIG
    wirksamkeit_geprueft: bool

class Anhang:
    rekla_id: UUID
    dateiname: str
    sharepoint_pfad: str
    typ: Enum               # FOTO | DOKUMENT | MESSUNG
    hochgeladen_von: str
```

---

## STATUS-WORKFLOW

```
┌───────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  NEU  │ ──▶ │ IN_BEARBEIT- │ ──▶ │  MASSNAHMEN   │ ──▶ │ ABGESCHLOSSEN│
│       │     │     UNG      │     │               │     │              │
└───────┘     └──────────────┘     └───────────────┘     └──────────────┘
    │               │                     │                      │
E-Mail Import   Analyse              Maßnahmen             Wirksamkeit
Auto-Erstellung D1-D4 (8D)           D5-D7                 D8 bestätigt
```

---

## QM-BOARD (HTML-Dashboard)

### KPIs
| KPI | Berechnung | Ziel |
|-----|------------|------|
| Offene Reklas | Status != ABGESCHLOSSEN | <15 |
| Kritische | Priorität = KRITISCH | 0 |
| Überfällige Maßnahmen | Termin < heute & Status != ABGESCHLOSSEN | 0 |
| Durchlaufzeit Ø | AVG(abgeschlossen_am - erstellt_am) | <14 Tage |
| 8D-Quote | Abgeschlossene 8D / Kunden-Reklas | 100% |

### Visualisierungen
- Trend-Chart (12 Monate)
- Pareto (Fehlercluster)
- Status-Verteilung (Donut)

---

## ZEITPLAN (21 Tage)

| Tag | Phase | Deliverables |
|-----|-------|--------------|
| 1-3 | **Setup** | Docker, PostgreSQL, FastAPI Skeleton |
| 4-7 | **Backend Core** | Models, Schemas, CRUD-Routes |
| 8-11 | **Frontend** | React Dashboard + Detail-Ansicht |
| 12-14 | **Integration** | Outlook-Import, SharePoint-Sync |
| 15-17 | **Features** | Maßnahmen, Fotos, QM-Board |
| 18-19 | **Migration** | 2025er Daten importieren |
| 20-21 | **Testing & Go-Live** | UAT, Deployment, Dokumentation |

---

## NULL-FEHLER-REGELN

⚠️ **KRITISCH:**
- KEINE erfundenen MA-Kürzel
- KEINE Beispieldaten ohne Kennzeichnung
- DSGVO: Nur Kürzel, keine vollen Namen
- Alle IDs validieren vor Speicherung

---

## OUTPUT-ERWARTUNG

Bei jeder Entwicklungsaufgabe:
1. **Architektur-Begründung** - Warum diese Lösung?
2. **Vollständiger Code** - Lauffähig, dokumentiert
3. **Docker-Setup** - docker-compose.yml
4. **Tests** - Mindestens Happy-Path
5. **Deployment-Anleitung** - Für Hetzner

---

**Erstellt:** 2025-12-20 | **Version:** 2.0 | **Autor:** AL (QM & KI-Manager)
