# RMS Workflows - Übersicht

**Stand:** 2026-01-27 (aktualisiert: Phase 3+5)
**Erstellt von:** Claude Code
**Verantwortlich:** AL (QM & KI-Manager)

---

## Workflow-Übersicht

| ID | Name | Status | Trigger | Beschreibung |
|----|------|--------|---------|--------------|
| k3rVSLW6O00dtTBr | RMS-Email-Import-V2 | 🟢 Aktiv | Schedule (5 Min) | Haupt-Workflow: E-Mails verarbeiten, Reklamationen erstellen |
| Eu7T9rCmLub6xO05 | RMS-QA-ID-Generator | 🟢 Aktiv | Schedule (5 Min) | QA-IDs für neue Reklamationen generieren |
| yiR3dlT4AKEZt9ti | RMS-Ordner-Sync | 🟢 Aktiv | Schedule (5 Min) | SharePoint-Ordnerstruktur erstellen |
| Z4D6ChArp86tDKC0 | RMS-Eskalation-Monitor | 🟢 Aktiv | Schedule (tägl. 8 Uhr) | Überfällige Reklamationen melden |
| Aq6gmrE8IX3RKIeF | RMS-Error-Handler | 🟢 Aktiv | Error Trigger | Fehlerbehandlung für alle RMS-Workflows |
| GBASN0mW8Z3NzfPD | RMS-Email-Import | 🟢 Aktiv | Schedule | Legacy-Workflow (V1) |

---

## RMS-Email-Import-V2 (Haupt-Workflow)

**ID:** `k3rVSLW6O00dtTBr`
**Trigger:** Alle 5 Minuten

### Ablauf

```
1. Schedule (5 Min)
   ↓
2. E-Mails abrufen (Graph API: reklamation@schneider-kabelsatzbau.de)
   ↓
3. E-Mails vorhanden? → Nein → Ende
   ↓ Ja
4. E-Mail-Parser (QA-ID, Absender, Betreff extrahieren)
   ↓
5. Spam? → Ja → In Junk verschieben
   ↓ Nein
6. QA-ID gefunden? → Nein → QA-ID generieren
   ↓ Ja
7. Rekla suchen / Config laden
   ↓
8. Rekla existiert? → Merge / Neue QA-ID
   ↓
9. Reklamation erstellen (SharePoint)
   ├──────────────────────────────────┐
   ↓                                  ↓
10. Config updaten?              --- Phase 3 (parallel) ---
   ↓                             17. PDF generieren (localhost:5001)
11. Als gelesen markieren           ↓
   ↓                             18. PDF vorbereiten (Base64 decode)
12. Ins Archiv verschieben          ↓
   ├────────────────────────┐    19. PDF nach SharePoint
   ↓                        ↓
--- Phase 2 ---        --- Phase 5 (parallel) ---
13. Anhänge laden      16. Schriftverkehr erstellen
   ↓
14. SharePoint Upload (/Reklamationen/{Jahr}/{Monat}/{QA-ID}/)
   ↓
15. Teams Benachrichtigung (bei Prioritaet hoch/kritisch)
```

### Nodes mit Credentials

| Node | Credential Type | Phase |
|------|----------------|-------|
| 2. E-Mails abrufen | Microsoft OAuth2 | 1 |
| 5a. In Junk verschieben | Microsoft OAuth2 | 1 |
| 7a. Rekla suchen | Microsoft OAuth2 | 1 |
| 7b. Config laden | Microsoft OAuth2 | 1 |
| 9. Reklamation erstellen | Microsoft OAuth2 | 1 |
| 10a. Config aktualisieren | Microsoft OAuth2 | 1 |
| 11. Als gelesen markieren | Microsoft OAuth2 | 1 |
| 12. Ins Archiv | Microsoft OAuth2 | 1 |
| 13. Anhänge laden | Microsoft OAuth2 | 2 |
| 14. SharePoint Upload | Microsoft OAuth2 | 2 |
| 15. Teams Benachrichtigung | Microsoft OAuth2 | 2 |
| 16. Schriftverkehr erstellen | Microsoft OAuth2 | 5 |
| 17. PDF generieren | - (localhost) | 3 |
| 18. PDF vorbereiten | - (Code) | 3 |
| 19. PDF nach SharePoint | Microsoft OAuth2 | 3 |

---

## RMS-QA-ID-Generator

**ID:** `Eu7T9rCmLub6xO05`
**Trigger:** Alle 5 Minuten

### Ablauf

1. Reklamationen ohne QA-ID aus SharePoint laden
2. RMS-Config laden (für Last_ID)
3. QA-IDs generieren (Format: QA-JJNNN, z.B. QA-26001)
4. QA-ID in SharePoint speichern
5. Last_ID in Config aktualisieren

---

## RMS-Ordner-Sync

**ID:** `yiR3dlT4AKEZt9ti`
**Trigger:** Alle 5 Minuten

### Ablauf

1. Reklamationen mit QA-ID aber ohne Ordner laden
2. Drive-ID holen
3. Ordnerstruktur erstellen:
   - `/Reklamationen/{QA-ID}/`
   - `/Reklamationen/{QA-ID}/Schriftverkehr/`
   - `/Reklamationen/{QA-ID}/Fotos/`
   - `/Reklamationen/{QA-ID}/Dokumente/`
4. Reklamation als erledigt markieren (OrdnerErstellt = true)

---

## RMS-Eskalation-Monitor

**ID:** `Z4D6ChArp86tDKC0`
**Trigger:** Täglich um 8:00 Uhr

### Ablauf

1. Offene Reklamationen aus SharePoint laden (Status != Abgeschlossen)
2. Prüfen ob Reklamation > 7 Tage ohne Update
3. Bei Eskalation: Teams-Alert an QM-Channel

### Eskalations-Kriterien

- Reklamation ist offen (Status != Abgeschlossen)
- Letzte Änderung > 7 Tage

---

## RMS-Error-Handler

**ID:** `Aq6gmrE8IX3RKIeF`
**Trigger:** Error Trigger (von anderen Workflows aufgerufen)

### Ablauf

1. Error Details extrahieren (Workflow, Node, Fehlermeldung)
2. Teams Alert senden (Rot, mit Link zu n8n)
3. Email an AL senden

### Verknüpfung

Um den Error Handler mit einem Workflow zu verknüpfen:
1. Workflow in n8n öffnen
2. Settings → Error Workflow → "RMS-Error-Handler" auswählen
3. Speichern

---

## Credentials

| ID | Name | Typ | Verwendet von |
|----|------|-----|---------------|
| Fm3IuAbVYBYDIA4U | Microsoft account | OAuth2 | Alle RMS-Workflows |

---

## SharePoint-Ressourcen

| Ressource | ID/URL |
|-----------|--------|
| Site | rainerschneiderkabelsatz.sharepoint.com |
| Site ID | 2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c |
| Reklamations-Liste | e9b1d926-085a-4435-a012-114ca9ba59a8 |
| Config-Liste | f89562e1-e566-42d7-a58b-917b739c3a38 |
| Schriftverkehr-Liste | 741c6ae8-88bb-406b-bf85-2e11192a528f |

---

## RMS PDF Generator Service

**Port:** 5001
**Service:** rms-pdf-generator.service
**Pfade:**
- Templates: /opt/osp/templates/
- Output: /opt/osp/output/
- Script: /opt/osp/scripts/rms_pdf_generator.py

### Endpoints

| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| /health | GET | Status pruefen |
| /schema | GET | JSON-Schema abrufen |
| /generate-pdf | POST | PDF generieren |
| /validate | POST | Daten validieren |

### Service-Befehle

```bash
# Status pruefen
systemctl status rms-pdf-generator

# Neustart
systemctl restart rms-pdf-generator

# Logs
journalctl -u rms-pdf-generator -f

# Health Check
curl http://localhost:5001/health
```

---

## Management-Befehle

```bash
# API Key setzen
export N8N_API_KEY="eyJhbGci..."

# Alle Workflows listen
python3 /opt/osp/scripts/n8n_workflow_manager.py list --base-url http://127.0.0.1:5678

# Workflow-Details anzeigen
python3 /opt/osp/scripts/n8n_workflow_manager.py show --id <WORKFLOW_ID> --base-url http://127.0.0.1:5678

# Credentials für RMS-Workflow setzen
python3 /opt/osp/scripts/n8n_workflow_manager.py configure-rms --id k3rVSLW6O00dtTBr --cred-id Fm3IuAbVYBYDIA4U --cred-name "Microsoft account" --base-url http://127.0.0.1:5678

# Alle Workflows exportieren
python3 /opt/osp/scripts/n8n_workflow_manager.py backup -o /opt/osp/backups/n8n_$(date +%Y%m%d) --base-url http://127.0.0.1:5678
```

---

## Fehlerbehandlung

### Häufige Fehler

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| 401 Unauthorized | Token abgelaufen | Microsoft OAuth2 Credential neu authentifizieren |
| 400 Bad Request | Ungültige API-Parameter | Node-Parameter prüfen |
| 404 Not Found | Ressource nicht gefunden | IDs in SharePoint prüfen |

### Logs prüfen

```bash
# n8n Container Logs
docker logs n8n --tail 100

# Letzte Ausführungen
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "http://127.0.0.1:5678/api/v1/executions?workflowId=k3rVSLW6O00dtTBr&limit=10"
```

---

*Erstellt: 2026-01-27 | Teil des OSP-Systems*
