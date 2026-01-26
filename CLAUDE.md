# OSP Projekt-Kontext für Claude Code (Server)

**Projekt:** OSP (Organisations-System-Prompt)  
**Unternehmen:** Rainer Schneider Kabelsatzbau GmbH & Co. KG  
**Server:** Hetzner CX33 (46.224.102.30)  
**Stack:** ChromaDB | Open WebUI v0.6.41 | Claude API  
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
- **KEINE FALSCHEN CRIMPHÖHEN** - Existenzbedrohend!
- **KEINE ERFUNDENEN MA-KÜRZEL** - Niemals!
- **KEINE PHANTASIE-TAGs** - Immer prüfen!

---

## Verzeichnisstruktur (Server)

| Pfad | Inhalt |
|------|--------|
| `/opt/osp/documents/` | OSP_KERN (12 MD) - FLACHE Struktur |
| `/opt/osp/documents_erweitert/` | OSP_ERWEITERT (~46 MD) |
| `/opt/osp/lookups/` | KPL JSON-Dateien |
| `/opt/osp/pipelines/` | Open WebUI Pipelines |
| `/opt/osp/chromadb/` | Vektor-Datenbank |
| `/opt/osp/logs/` | Validierungs-Logs |
| `/opt/osp/scripts/` | Python-Scripts |

---

## RMS (Reklamationsmanagementsystem)

### Übersicht
| Parameter | Wert |
|-----------|------|
| **Status** | 🟡 In Entwicklung |
| **Pfad** | `/mnt/HC_Volume_104189729/osp/rms/` |
| **ID-Format** | QA-JJNNN (z.B. QA-26001) |
| **Erwartete Einträge** | ~150/Jahr |
| **Hauptnutzer** | AL, TS, GF (CS, CA, SV) |

### RMS-Verzeichnisse
| Pfad | Inhalt |
|------|--------|
| `rms/backend/` | FastAPI Backend (geplant) |
| `rms/dashboard/` | HTML-Dashboard für alle MA |
| `rms/workflows/` | n8n Workflow-Exports |
| `rms/formulare/` | QM-Formblätter (F-QM-02, 03, 04, 14) |
| `rms/docs/` | Strategie & Dokumentation |
| `rms/prompts/` | RMS-spezifische Prompts |

### RMS-Formblätter
| Formular | Zweck | Dateien |
|----------|-------|---------|
| **F-QM-02** | Qualitätsabweichung (Lieferanten) | .md, .json, RMS_Prompt |
| **F-QM-03** | 8D-Report (extern, vollständig) | .md, .json, RMS_Prompt |
| **F-QM-04** | NZA (Nach-/Zusatzarbeiten) | .md, .json, RMS_Prompt |
| **F-QM-14** | Korrekturmaßnahme (8D-Light, intern) | .md, .json, RMS_Prompt |

### RMS Slash Commands
| Befehl | Beschreibung |
|--------|--------------|
| `/rms-status` | RMS System-Status prüfen |
| `/rms-new [TYP]` | Neue Reklamation anlegen (INTERN/KUNDE/LIEFERANT) |
| `/rms-fill [FORMULAR]` | Formblatt mit KI ausfüllen |
| `/rms-dashboard` | Dashboard-Status prüfen |

### RMS-Integration mit OSP
- **ChromaDB:** Ähnliche Reklamationen finden (geplant)
- **n8n:** E-Mail-Import, Formblatt-Generator, Alarme
- **HR_CORE:** MA-Kürzel Validierung, KST-Zuordnung
- **SharePoint:** Dokumenten-Ablage (/sites/RMS/)

### RMS Phasen
| Phase | Features | Status |
|-------|----------|--------|
| MVP | SharePoint Listen, Power Automate, Dashboard | ⏳ Offen |
| Phase 2 | KI-Formblatt-Generator (n8n + Claude) | ⏳ Offen |
| Phase 3 | Charts, Teams-App, ChromaDB-Suche | ⏳ Offen |

---

## OSP_KERN Dateien (12 Stück)

Alle KERN-Dateien liegen FLACH in `documents/`:

```
documents/HR_CORE_Personalstamm.md       # 54 MA - KRITISCH!
documents/TM_CORE_Maschinen_Anlagen.md   # ~220 Maschinen - KRITISCH!
documents/TM_WKZ_Werkzeuge.md            # ~342 Werkzeuge - KRITISCH!
documents/AV_AGK_Arbeitsgang_Katalog.md
documents/KST_CORE_Layout_Fertigung.md
documents/QM_CORE_Qualitaetspolitik.md
documents/QM_PMV_Prüfmittelverwaltung.md
documents/QM_REK_Reklamationsmanagement.md
documents/KOM_CORE_Corporate_Identity.md
documents/DMS_CORE_Dokumentenstruktur.md
documents/IT_OSP_KI_Chatbot.md
documents/OSP_Navigator.md               # KRITISCH!
```

---

## Docker-Befehle

```bash
# Status prüfen
docker ps

# Logs anzeigen
docker-compose logs -f open-webui
docker-compose logs -f chromadb

# Neustart
docker-compose restart open-webui
docker-compose restart chromadb

# Alle Services neustarten
docker-compose down && docker-compose up -d
```

---

## ChromaDB Befehle

```bash
# Collections auflisten
curl http://localhost:8000/api/v1/collections

# Collection-Details
curl http://localhost:8000/api/v1/collections/osp_kern

# Healthcheck
curl http://localhost:8000/api/v1/heartbeat

# Python-Zugriff
python3 -c "
import chromadb
client = chromadb.HttpClient(host='localhost', port=8000)
print(client.list_collections())
"
```

---

## RAG-Validierung

```bash
# Vollständige Validierung
python3 scripts/validate_rag.py

# Einzelne Query testen
python3 scripts/validate_rag.py -q "Wer ist AL?"

# Performance-Test
time curl -X POST http://localhost:3000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Wer ist AL?"}]}'
```

---

## Code Style

### Python
- Python 3.11+
- Type Hints
- Docstrings (Google Style)
- `logging` statt `print()`

### Markdown
- UTF-8 (ohne BOM)
- YAML Frontmatter
- `[TAG]` Notation

---

## Corporate Identity

| Element | Wert |
|---------|------|
| **Primär-Blau** | `#0080C9` |
| **Akzent-Orange** | `#DC500F` |
| **Headlines** | Montserrat Bold |
| **Fließtext** | Open Sans |

---

## TAG-System (15 Module)

| Cluster | TAGs |
|---------|------|
| C1 Kontext | [ORG], [KOM] |
| C2 Führung | [QM], [GF], [PM], [AV], [VT], [EK] |
| C3 Kernprozesse | [KST] |
| C4 Support | [DMS], [TM], [IT], [HR], [RES], [CMS] |

---

## Berechtigungssystem

| Level | Zugriff |
|-------|---------|
| L1 🟢 | Öffentlich (alle MA) |
| L2 🟡 | Führung (~10) |
| L3 🔴 | GF + Prokura (CS, CA, SV) |

---

## Schlüsselpersonen

| Kürzel | Rolle | Level |
|--------|-------|-------|
| AL | QM-Manager & KI-Manager | L3, OSP-EXP |
| CS | Kaufmännischer GF | L3 |
| CA | Technischer GF | L3 |
| SV | Prokurist | L3 |
| MD | Technik/Maschinen | L2 |

---

## Wichtige Regeln

1. **VOR Änderungen:** Backup erstellen
2. **NIEMALS** erfinden → NACHFRAGEN!
3. **IMMER** technische Daten verifizieren
4. **Nach Änderungen:** RAG-Validierung!
5. **Docker** nach Pipeline-Änderungen neustarten

---

## Quick Commands

```bash
# KERN-Dateien zählen
ls -la documents/*.md | wc -l

# Dateigröße prüfen
du -h documents/

# Logs der letzten Stunde
journalctl --since "1 hour ago" | grep -i osp

# Backup erstellen
tar -czvf backup_$(date +%Y%m%d).tar.gz documents/

# ChromaDB Collection neu indizieren
python3 scripts/reindex_chromadb.py
```

---

## Häufige Tasks

### KERN-Datei bearbeiten
```bash
# 1. Backup
cp documents/HR_CORE_Personalstamm.md documents/HR_CORE_Personalstamm.md.bak

# 2. Bearbeiten
nano documents/HR_CORE_Personalstamm.md

# 3. Validieren
python3 scripts/validate_rag.py -q "Wer ist AL?"

# 4. Bei Erfolg: Backup löschen
rm documents/HR_CORE_Personalstamm.md.bak
```

### Pipeline ändern
```bash
# 1. Backup
cp pipelines/osp_rag.py pipelines/osp_rag.py.bak

# 2. Bearbeiten
nano pipelines/osp_rag.py

# 3. Docker neustarten
docker-compose restart open-webui

# 4. Testen
curl -X POST http://localhost:3000/api/chat ...
```

---

*Bei JEDER Unsicherheit → NACHFRAGEN!*  
*Bei JEDER Unstimmigkeit → TRANSPARENT MACHEN!*

---

**Erstellt:** 2025-12-14  
**Version:** 1.0 (Server)
