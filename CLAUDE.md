# OSP Projekt-Kontext für Claude Code

**Projekt:** OSP (Organisations-System-Prompt)
**Unternehmen:** Rainer Schneider Kabelsatzbau GmbH & Co. KG
**Stack:** Hetzner CX43 (8 vCPU, 32GB RAM) | ChromaDB v1.0.0 | Open WebUI v0.6.41 | Claude API
**Verantwortlich:** AL (Andreas Löhr) - QM-Manager & KI-Manager

---

## ⚠️ NULL-FEHLER-POLITIK (ABSOLUT VERBINDLICH!)

### Die 5 Säulen
1. **TRANSPARENZ-PFLICHT**: Bei JEDER Unstimmigkeit SOFORT melden
2. **NACHFRAGEN VOR RATEN**: NIEMALS Informationen erfinden
3. **TAG-VALIDIERUNG**: Jeden TAG gegen OSP_Navigator prüfen
4. **CONFIDENCE-ANGABE**: (C: XX%) bei JEDER Faktenaussage
5. **KABELKONFEKTION-EXPERTISE**: Bei Crimpdaten IMMER verifizieren

### KRITISCHE WARNUNGEN
- **KEINE FALSCHEN CRIMPHÖHEN** - Existenzbedrohend für das Unternehmen!
- **KEINE ERFUNDENEN MA-KÜRZEL** - Niemals! Immer gegen HR_CORE prüfen!
- **KEINE PHANTASIE-TAGs** - Immer gegen OSP_Navigator validieren!

---

## Verzeichnisstruktur

### Lokal (OneDrive - dieses Verzeichnis)
| Pfad | Inhalt |
|------|--------|
| `Main/` | Alle OSP-Dateien inkl. KERN (in Unterordnern) |
| `Main/OSP_Navigator.md` | Wissens-Routing - KRITISCH! |
| `Lookups/` | KPL JSON-Dateien für exakte Suchen |
| `pipelines/` | Open WebUI Pipeline-Dateien |
| `Analysen/` | RAG-Analysen und Tests |
| `Templates/` | Vorlagen für neue Dateien |
| `Tools/` | Hilfsskripte und Utilities |

### Server (Hetzner CX43 - 8 vCPU, 32GB RAM)
| Pfad | Inhalt |
|------|--------|
| `/opt/osp/documents/` | OSP_KERN (12 MD) - flache Struktur |
| `/opt/osp/documents_erweitert/` | OSP_ERWEITERT (~46 MD) |
| `/opt/osp/lookups/` | KPL JSON-Dateien |
| `/opt/osp/pipelines/` | Aktive Pipelines |
| `/opt/osp/chromadb/` | Vektor-Datenbank |
| `/opt/osp/logs/` | Validierungs-Logs |

---

## RMS (Reklamationsmanagementsystem)

### Übersicht
| Parameter | Wert |
|-----------|------|
| **Status** | 🟡 In Entwicklung |
| **Pfad** | /mnt/HC_Volume_104189729/osp/rms/ |
| **ID-Format** | QA-JJNNN (z.B. QA-26001) |
| **Erwartete Einträge** | ~150/Jahr |
| **Hauptnutzer** | AL, TS, GF (CS, CA, SV) |

### RMS-Verzeichnisse
| Pfad | Inhalt |
|------|--------|
| rms/backend/ | FastAPI Backend (geplant) |
| rms/dashboard/ | HTML-Dashboard für alle MA |
| rms/workflows/ | n8n Workflow-Exports |
| rms/formulare/ | QM-Formblätter (F-QM-02, 03, 04, 14) |
| rms/docs/ | Strategie & Dokumentation |
| rms/prompts/ | RMS-spezifische Prompts |

### RMS-Formblätter
| Formular | Zweck | Dateien |
|----------|-------|---------|
| **F-QM-02** | Qualitätsabweichung (Lieferanten) | .md, .json, RMS_Prompt |
| **F-QM-03** | 8D-Report (extern, vollständig) | .md, .json, RMS_Prompt |
| **F-QM-04** | NZA (Nach-/Zusatzarbeiten) | .md, .json, RMS_Prompt |
| **F-QM-14** | Korrekturmaßnahme (8D-Light, intern) | .md, .json, RMS_Prompt |

### RMS-Integration mit OSP
- **ChromaDB:** Ähnliche Reklamationen finden (geplant)
- **n8n:** E-Mail-Import, Formblatt-Generator, Alarme
- **HR_CORE:** MA-Kürzel Validierung, KST-Zuordnung
- **SharePoint:** Dokumenten-Ablage (/sites/RMS/)

### Microsoft Graph API Berechtigungen (Azure Portal)

App-Registrierung: **OSP-n8n-Integration**

#### Kalender
| Berechtigung | Typ | Beschreibung |
|--------------|-----|--------------|
| Calendars.Read | Delegiert | Lesezugriff auf Benutzerkalender |
| Calendars.Read | Anwendung | Read calendars in all mailboxes |
| Calendars.ReadBasic.All | Anwendung | Read basic details of calendars in all mailboxes |
| Calendars.ReadWrite | Delegiert | Vollzugriff auf Benutzerkalender |
| Calendars.ReadWrite | Anwendung | Read and write calendars in all mailboxes |

#### Channels & Chat
| Berechtigung | Typ | Beschreibung |
|--------------|-----|--------------|
| Channel.ReadBasic.All | Anwendung | Read the names and descriptions of all channels |
| ChannelMessage.Read.All | Delegiert | Read user channel messages |
| ChannelMessage.Read.All | Anwendung | Read all channel messages |
| Chat.Read | Delegiert | Benutzerchatnachrichten lesen |
| Chat.Read.All | Anwendung | Read all chat messages |
| Chat.ReadWrite.All | Anwendung | Read and write all chat messages |

#### Files & Sites
| Berechtigung | Typ | Beschreibung |
|--------------|-----|--------------|
| Files.Read.All | Anwendung | Read files in all site collections |
| Files.ReadWrite.All | Anwendung | Read and write files in all site collections |
| Sites.Manage.All | Anwendung | Create, edit, and delete items and lists in all site collections |
| Sites.ReadWrite.All | Delegiert | Elemente in allen Websitesammlungen bearbeiten |
| Sites.ReadWrite.All | Anwendung | Read and write items in all site collections |

#### Mail
| Berechtigung | Typ | Beschreibung |
|--------------|-----|--------------|
| Mail.Read | Delegiert | Lesezugriff auf Benutzer-E-Mails |
| Mail.Read | Anwendung | Read mail in all mailboxes |
| Mail.Read.Shared | Delegiert | Benutzer und freigegebene E-Mails lesen |
| Mail.ReadBasic | Delegiert | Grundlegende Benutzer-E-Mail lesen |
| Mail.ReadWrite | Delegiert | Lese- und Schreibzugriff auf Benutzer-E-Mails |
| Mail.ReadWrite.Shared | Delegiert | Benutzer und freigegebene E-Mails lesen und schreiben |
| Mail.Send | Delegiert | E-Mails unter einem anderen Benutzernamen senden |

#### Meetings & Teams
| Berechtigung | Typ | Beschreibung |
|--------------|-----|--------------|
| OnlineMeetings.Read.All | Anwendung | Read online meeting details |
| Team.ReadBasic.All | Anwendung | Get a list of all teams |
| TeamsActivity.Send | Anwendung | Send a teamwork activity to any user |

#### User & Auth
| Berechtigung | Typ | Beschreibung |
|--------------|-----|--------------|
| User.Read | Delegiert | Anmelden und Benutzerprofil lesen |
| User.Read.All | Anwendung | Read all users' full profiles |
| offline_access | Delegiert | Zugriff auf Daten beibehalten |
| openid | Delegiert | Benutzer anmelden |
| profile | Delegiert | Grundlegendes Profil von Benutzern anzeigen |

### n8n Credentials (Stand: 01.02.2026)

| Credential | Typ | ID | Status |
|------------|-----|-----|--------|
| Microsoft SharePoint account | Microsoft SharePoint OAuth2 API | 5ZmmOyK1L7PhkJW2 | ✅ Aktiv |
| Microsoft Drive account | Microsoft Drive OAuth2 API | RFliYFkYUYpnA7ki | ✅ Aktiv |
| Microsoft account | Microsoft OAuth2 API | TY9l0Fx0mOLQHsc8 | ✅ Aktiv |
| Microsoft Outlook Reklamation | Microsoft Outlook OAuth2 API | LfzrHpsvieP4DpIa | ✅ Aktiv |
| Microsoft Outlook NZA | Microsoft Outlook OAuth2 API | y6bC8aYrlgPO6ZsG | ✅ Aktiv |
| Microsoft Teams account | Microsoft Teams OAuth2 API | YckMuDdaL97hqHSG | ✅ Aktiv |

#### Azure App
- **App-Name:** OSP-n8n-Integration
- **Client ID:** f99f47af-da3a-493c-aa17-e6b30e3b197c
- **Tenant ID:** 31d02377-b699-4cef-a113-fc66e586df88
- **Redirect URI:** https://n8n.schneider-kabelsatzbau.de/rest/oauth2-credential/callback

#### Shared Mailboxes
- reklamation@schneider-kabelsatzbau.de → Microsoft Outlook Reklamation
- nza@schneider-kabelsatzbau.de → Microsoft Outlook NZA

#### SharePoint
- Subdomain: schneiderkabelsatzbau
- NZA Site: /sites/NZA_NEU

---

## NZA (Nach- und Zusatzarbeiten-System)

### Übersicht
| Parameter | Wert |
|-----------|------|
| **Status** | 🟡 In Entwicklung |
| **Pfad** | /mnt/HC_Volume_104189729/osp/nza/ |
| **ID-Format** | NZA-JJ-XXXX (z.B. NZA-26-0001) |
| **Erwartete Einträge** | ~300-500/Jahr |
| **Hauptnutzer** | AL, MD, BS, SK, DR |

### Abgrenzung RMS vs. NZA
| Aspekt | RMS | NZA |
|--------|-----|-----|
| **Zweck** | Externe Reklamationen | Interne Nacharbeiten/Ausschuss |
| **Typen** | Kunde, Lieferant | Nacharbeit, Neufertigung, Ausschuss |
| **E-Mail** | reklamation@... | nza@schneider-kabelsatzbau.de |
| **SharePoint** | /sites/RMS/ | /sites/NZA_NEU |
| **ID-Format** | QA-JJNNN | NZA-JJ-XXXX |
| **Kostenerfassung** | Nein | Ja (Minutensätze × Zeit) |
| **Verursacher** | Extern | Intern (nza-mitarbeiter) |
| **Dashboard** | https://osp.schneider-kabelsatzbau.de/rms/ | https://osp.schneider-kabelsatzbau.de/nza/ |
| **Bilder** | Optional | Wichtig (Fehlerfotos) |

### Microsoft 365 Ressourcen
| Ressource | Wert |
|-----------|------|
| **SharePoint Site** | /sites/NZA_NEU |
| **M365 Gruppe/Team** | "NZA" |
| **Team-Email** | NZA1@schneider-kabelsatzbau.de |
| **Postfach (Import)** | nza@schneider-kabelsatzbau.de |
| **Credentials** | Gleiche wie RMS (OSP-n8n-Integration) |

### SharePoint-Listen

#### Hauptliste: nza-kpl (52 Felder)
Die Hauptliste setzt sich zusammen aus drei logischen Bereichen:

| Bereich | Felder | Beschreibung |
|---------|--------|--------------|
| **nza-stammdaten** | ~17 | NZA-ID, Datum, Typ, Artikel, Verursacher, KST, Beschreibung |
| **nza-prozesse** | ~30 | 5× (Prozess, Werker, KST, Zeit, Faktor, Kosten) |
| **nza-material** | ~5 | kosten_material, kosten_sonstige, kosten_prozesse, kosten_gesamt |

**Kostenberechnung:** `nza-kosten = nza-prozesse + nza-material`

#### Zusätzliche Listen
| Liste | Zweck | Felder |
|-------|-------|--------|
| nza-massnahmen | Korrekturmaßnahmen + Teams-Notify | 13 |
| nza-bilder | Fehlerfotos (wichtig!) | 8 |
| nza-mitarbeiter | Verursacher-Lookup (53 MA) | 9 |
| nza-config | System-Konfiguration | 5 |
| nza-kpis | Aggregierte Kennzahlen | 7 |

### Minutensätze (Kostenberechnung)
| Kostenstelle | €/Min | €/h | Beschreibung |
|--------------|-------|-----|--------------|
| 1000 | 1,98 | 118,80 | Fertigung F1 |
| 2000 | 1,21 | 72,60 | Fertigung F2 |
| 3000 | 0,93 | 55,80 | Fertigung F3 |
| 4000 | 1,02 | 61,20 | Fertigung F4 |
| 5000 | 1,02 | 61,20 | Fertigung F5 |
| Lager | 1,10 | 66,00 | Lagerbereich |
| Verwaltung | 1,37 | 82,20 | Administration |

### NZA-Verzeichnisse
| Pfad | Inhalt |
|------|--------|
| nza/docs/ | Strategie & Dokumentation |
| nza/prompts/ | NZA-spezifische Prompts |
| nza/formulare/ | F-QM-04 Template |
| nza/workflows/ | n8n Workflow-Exports |
| nza/daten/ | Stammdaten (CSV-Imports) |

### NZA-Mitarbeiter (aus nza_mitarbeiter.csv)
| KST | Anzahl | Wichtige MA |
|-----|--------|-------------|
| Verwaltung | 9 | CS, CA, SV, AL, TS |
| 1000 | 5 | MD (FL), DS (Stv.) |
| 2000 | 9 | BS (FL 2000/3000), JR |
| 3000 | 13 | IB (Stv. FL) |
| 5000 | 12 | SK, DR (FL), WK |
| Lager | 3 | OK (Lagerleiter) |
| **Gesamt** | **53** | |

### n8n Workflows (NZA)
| Workflow | Trigger | Priorität |
|----------|---------|-----------|
| NZA-Prozesse-API | Webhook GET/POST/PATCH | 🔴 |
| NZA-Massnahmen-API | Webhook + Teams-Notify | 🔴 |
| NZA-Bilder-API | Webhook (Upload bis 20MB) | 🔴 |
| NZA-Mitarbeiter-API | Webhook GET | 🔴 |
| NZA-Kosten-API | Webhook + Auto-Berechnung | 🔴 |
| NZA-Email-Import | Schedule (5 Min) | 🟡 |
| NZA-KPI-Update | Schedule (Täglich) | 🟢 |
| NZA-Generate-Formblatt | Webhook (F-QM-04 PDF) | ⏸️ Später |

### RMS ↔ NZA Integration
- **Getrennte Systeme** mit Dashboard-Wechsel möglich
- **RMS:** Externe Reklamationen (Kunden, Lieferanten)
- **NZA:** Interne Nacharbeiten und Ausschuss
- **Verknüpfung:** NZA kann RMS-Bezug haben (QA-ID in Feld `Bezug_RMS`)
- **F-QM-04 PDF:** Später implementieren

### Nginx-Endpoints (osp.schneider-kabelsatzbau.de)

**RMS Dashboards & APIs:**
```
/rms/                         → Dashboard 2026 (aktuell)
/rms/2025/                    → Dashboard 2025 (Archiv)
/api/rms/reklamationen        → Liste aller Reklamationen
/api/rms/kpis                 → KPI-Daten
/api/rms/charts               → Chart-Daten
/api/rms/detail               → Einzelne Reklamation
/api/rms/create               → Neue Reklamation
/api/rms/update               → Reklamation aktualisieren
/api/rms/massnahmen           → Maßnahmen CRUD
/api/rms/files                → Dateien-Liste
/api/rms/generate-formblatt   → PDF-Generierung
/api/rms/send-email           → E-Mail senden
/api/rms/users                → M365-Benutzer
/api/rms/stammdaten           → Stammdaten
```

**NZA Dashboards & APIs:**
```
/nza/                         → Dashboard
/api/nza/prozesse             → CRUD Hauptliste
/api/nza/massnahmen           → Maßnahmen + Notify
/api/nza/bilder               → Bilder-Galerie
/api/nza/bilder-upload        → Upload (20MB max)
/api/nza/mitarbeiter          → Verursacher-Lookup
/api/nza/kosten               → Kostenerfassung
/api/nza/config               → Konfiguration
/api/nza/kpis                 → Kennzahlen
/api/nza/notify               → Teams-Benachrichtigung
```

---

## OSP_KERN Dateien (12 Stück)

Die KERN-Dateien liegen in Unterordnern von `Main/`:

```
Main/HR_Human_Resources/HR_CORE_Personalstamm.md       # 54 MA - KRITISCH!
Main/TM_Technik_Maschinen/TM_CORE_Maschinen_Anlagen.md # ~220 Maschinen - KRITISCH!
Main/TM_Technik_Maschinen/TM_WKZ_Werkzeuge.md          # ~342 Werkzeuge - KRITISCH!
Main/AV_Arbeitsvorbereitung/AV_AGK_Arbeitsgang_Katalog.md
Main/KST_Kostenstellen/KST_CORE_Layout_Fertigung.md
Main/QM_Qualitaetsmanagement/QM_CORE_Qualitaetspolitik.md
Main/QM_Qualitaetsmanagement/QM_PMV_Prüfmittelverwaltung.md
Main/QM_Qualitaetsmanagement/QM_REK_Reklamationsmanagement.md
Main/KOM_Kommunikation/KOM_CORE_Corporate_Identity.md
Main/DMS_Dokumentenmanagement/DMS_CORE_Dokumentenstruktur.md
Main/IT_Infrastruktur/IT_OSP_KI_Chatbot.md
Main/OSP_Navigator.md                                   # KRITISCH!
```

**Hinweis:** Auf dem Server liegen die Dateien FLACH in `/opt/osp/documents/` (ohne Unterordner).

---

## Custom Slash Commands

Verfügbare Befehle in `.claude/commands/`:

| Befehl | Beschreibung |
|--------|--------------|
| `/kern-check` | Alle 12 KERN-Dateien prüfen |
| `/validate-rag` | RAG-Validierung (7 Query-Typen) |
| `/analyze-file [DATEI]` | Datei analysieren |
| `/kst-update [BATCH]` | KST-Querverweise updaten |
| `/formblatt-fill [QM-XX]` | Formblatt ausfüllen |
| `/navigator-validate [TAG]` | TAG validieren |
| `/sync-server` | Dateien auf Server synchronisieren |

---

## Server-Befehle (SSH auf Hetzner)

```bash
# SSH-Verbindung
ssh root@46.224.102.30

# Docker Services
docker-compose -f /opt/osp/docker-compose.yml logs -f open-webui
docker-compose -f /opt/osp/docker-compose.yml restart open-webui

# RAG Validierung
cd /opt/osp && python3 scripts/validate_rag.py

# ChromaDB Status (v1.0.0 - NEUE API!)
./scripts/chromadb_status.sh           # Übersicht
./scripts/chromadb_status.sh count     # Document Counts
./scripts/chromadb_status.sh details   # Detaillierte Infos

# ChromaDB REST API (v1.0.0)
# WICHTIG: /api/v1/ ist DEPRECATED! Nutze /api/v2/ mit Tenant/Database Pfad:
curl -s "http://localhost:8000/api/v2/heartbeat"
curl -s "http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections" | python3 -m json.tool

# Dokumente importieren
python3 scripts/import_to_chromadb.py --collection osp_kern --path /opt/osp/documents
python3 scripts/import_to_chromadb.py --collection osp_erweitert --path /opt/osp/documents_erweitert --clear

# Logs prüfen
tail -100 /opt/osp/logs/validation_latest.md
```

---

## Code Style

### Python
- Python 3.11+
- Type Hints für alle Funktionen
- Docstrings (Google Style)
- `logging` statt `print()` in Produktion
- UTF-8 Encoding

### Markdown (OSP-Dateien)
- UTF-8 Encoding (ohne BOM)
- YAML Frontmatter für Metadaten
- `[TAG]` Notation für Modul-Zuordnung
- Tabellen für strukturierte Daten
- Keine Leerzeilen in Tabellen

### Dateinamen
- Format: `MODULE_BEREICH_Beschreibung.md`
- Beispiel: `QM_PMV_Prüfmittelverwaltung.md`
- Keine Umlaute, keine Leerzeichen

---

## Corporate Identity

Bei HTML, React oder Dokumenten beachten:

| Element | Wert |
|---------|------|
| **Primär-Blau** | `#0080C9` |
| **Akzent-Orange** | `#DC500F` |
| **Headlines** | Montserrat Bold |
| **Fließtext** | Open Sans |
| **Code** | Fira Code |
| **Border-Radius** | 10px |

---

## TAG-System (15 Module)

| Cluster | Module |
|---------|--------|
| C1 Kontext | [ORG], [KOM] |
| C2 Führung | [QM], [GF], [PM], [AV], [VT], [EK] |
| C3 Kernprozesse | [KST] |
| C4 Support | [DMS], [TM], [IT], [HR], [RES], [CMS] |

**Wichtig:** Vor Verwendung eines TAGs IMMER gegen `Main/OSP_Navigator.md` validieren!

---

## Berechtigungssystem

| Level | Zugriff | Beschreibung |
|-------|---------|--------------|
| L1 🟢 | Öffentlich | Alle MA (~54) |
| L2 🟡 | Führung | Abteilungsleiter (~10) |
| L3 🔴 | Vertraulich | GF + Prokura (CS, CA, SV) |

**OSP-Level (KI-Kompetenz):** STD, PRO, EXP

---

## Testing

### RAG-Validierung (7 Query-Typen)
1. MA-Lookup: "Wer ist AL?"
2. Maschinen: "Komax Alpha 530"
3. Werkzeuge: "WKZ für Kontakt 1234"
4. Qualität: "NULL-FEHLER-POLITIK"
5. Kombination: "Welche Maschinen betreut MD?"
6. Negativ: "Gibt es MA XY?" (darf nicht erfinden!)
7. Performance: Response < 10s

### Lokale Tests
```bash
# Markdown-Syntax prüfen
find Main/ -name "*.md" -exec markdownlint {} \;

# UTF-8 prüfen
find Main/ -name "*.md" -exec file -i {} \; | grep -v utf-8

# KERN-Dateien zählen
find Main/ -name "*CORE*.md" -o -name "*WKZ*.md" -o -name "*AGK*.md" -o -name "*PMV*.md" -o -name "*REK*.md" -o -name "OSP_Navigator.md" | wc -l
```

---

## KST-Querverweise Update Status

| Batch | Module | Status |
|-------|--------|--------|
| 1-4 | QM_NZA, QM_REK, AV_CORE, AV_AGK | ✅ DONE |
| 5 | VT | 🔄 NÄCHSTER |
| 6 | EK | ⏳ GEPLANT |
| 7-8 | HR/FIN/IT/CMS/PM/ORG/STR/KOM/BN/RES | ⏳ GEPLANT |

---

## Schlüsselpersonen

| Kürzel | Rolle | Level |
|--------|-------|-------|
| AL | QM-Manager & KI-Manager | L3, OSP-EXP |
| CS | Kaufmännischer GF | L3 |
| CA | Technischer GF | L3 |
| SV | Prokurist | L3 |
| MD | Technik/Maschinen | L2 |
| SK | Prüffeld | L2 |
| TS | Einkauf | L2 |

---

## Links & Ressourcen

| Ressource | URL/Pfad |
|-----------|----------|
| **RMS Dashboard 2026** | https://osp.schneider-kabelsatzbau.de/rms/ |
| **RMS Dashboard 2025** (Archiv) | https://osp.schneider-kabelsatzbau.de/rms/2025/ |
| **NZA Dashboard** | https://osp.schneider-kabelsatzbau.de/nza/ |
| n8n Workflow-Editor | https://n8n.schneider-kabelsatzbau.de/ |
| Open WebUI | https://osp.schneider-kabelsatzbau.de/ |
| ChromaDB API | http://46.224.102.30:8000 |
| Server Logs | /opt/osp/logs/ |
| Claude API Docs | https://docs.anthropic.com |
| OSP-RAG-Skill | Claude Desktop Project |

---

## Wichtige Regeln für Claude Code

1. **VOR jeder Änderung** an KERN-Dateien: Backup erstellen
2. **NIEMALS** erfinden wenn unsicher → NACHFRAGEN!
3. **IMMER** bei technischen Daten (Crimphöhen, Inventar-Nr.) verifizieren
4. **UTF-8** ohne BOM für alle Markdown-Dateien
5. **Validierung** vor jedem Commit durchführen

---

*Bei JEDER Unsicherheit → NACHFRAGEN!*  
*Bei JEDER Unstimmigkeit → TRANSPARENT MACHEN!*

---

**Erstellt:** 2025-12-14
**Version:** 1.5
**Autor:** AL (via Claude)
**Änderung:** Dashboard-URLs aktualisiert (osp.schneider-kabelsatzbau.de), Nginx-Endpoints für RMS und NZA dokumentiert
