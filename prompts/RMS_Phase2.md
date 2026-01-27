
---

## AUFGABE 2: Phase 2 Nodes hinzufügen

Erweitere RMS-Email-Import-V2 um:

### Node 13: Anhänge laden
```
Nach Node 12 (Ins Archiv):
- HTTP Request zu Microsoft Graph API
- GET /messages/{messageId}/attachments
- Credential: Microsoft account (Fm3IuAbVYBYDIA4U)
```

### Node 14: SharePoint Upload
```
- Anhänge nach SharePoint hochladen
- Pfad: /Reklamationen/{Jahr}/{Monat}/{QA-ID}/
- Credential: Microsoft account
```

### Node 15: Teams Benachrichtigung
```
- Bei neuer Reklamation: Teams-Nachricht an QM-Channel
- Nur bei Priorität "hoch" oder "kritisch"
- Credential: Microsoft account
```

**Verwende das Script:**
```bash
python3 /opt/osp/scripts/n8n_workflow_manager.py add-phase2 --id k3rVSLW6O00dtTBr --base-url http://127.0.0.1:5678
```

---

## AUFGABE 3: Weitere RMS-Workflows erstellen

### Workflow: RMS-Ordner-Sync (existiert: yiR3dlT4AKEZt9ti)
Prüfe und konfiguriere:
```bash
python3 /opt/osp/scripts/n8n_workflow_manager.py show --id yiR3dlT4AKEZt9ti --base-url http://127.0.0.1:5678
```

### Workflow: RMS-QA-ID-Generator (existiert: Eu7T9rCmLub6x005)
Prüfe und konfiguriere:
```bash
python3 /opt/osp/scripts/n8n_workflow_manager.py show --id Eu7T9rCmLub6x005 --base-url http://127.0.0.1:5678
```

### NEUER Workflow: RMS-Eskalation-Monitor
Erstelle einen neuen Workflow der:
1. Täglich um 8:00 Uhr läuft (Schedule Trigger)
2. Offene Reklamationen aus SharePoint Liste holt
3. Prüft ob Reklamationen > 7 Tage ohne Update sind
4. Teams-Alert an QM-Manager sendet
5. Optional: Email an Verantwortlichen

**SharePoint Liste Details:**
- Site: rainerschneiderkabelsatz.sharepoint.com
- Liste ID: e9b1d926-085a-4435-a012-114ca9ba59a8
- Felder: QA_ID, Rekla_Status, Erfassungsdatum, Prioritaet

---

## AUFGABE 4: Error Handling Workflow

Erstelle einen Error-Handler Workflow:

1. Name: "RMS-Error-Handler"
2. Trigger: Error Trigger (wird von anderen Workflows aufgerufen)
3. Aktionen:
   - Log Error Details
   - Teams-Nachricht an IT-Channel
   - Optional: Email an AL (QM-Manager)

Dann verknüpfe ihn mit RMS-Email-Import-V2:
- Workflow Settings → Error Workflow → RMS-Error-Handler

---

## AUFGABE 5: Dokumentation aktualisieren

Nach Abschluss:

1. Erstelle/Aktualisiere `/opt/osp/docs/RMS_WORKFLOWS.md` mit:
   - Übersicht aller RMS-Workflows
   - Workflow-IDs und Status
   - Trigger-Beschreibungen
   - Fehlerbehandlung

2. Backup aller Workflows:
```bash
python3 /opt/osp/scripts/n8n_workflow_manager.py backup -o /opt/osp/backups/n8n_$(date +%Y%m%d) --base-url http://127.0.0.1:5678
```

---

## WICHTIGE REFERENZEN

| Resource | Wert |
|----------|------|
| n8n API | http://127.0.0.1:5678/api/v1 |
| Microsoft Credential ID | Fm3IuAbVYBYDIA4U |
| SharePoint Site ID | rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c |
| Reklamations-Liste ID | e9b1d926-085a-4435-a012-114ca9ba59a8 |
| Config-Liste ID | f89562e1-e566-42d7-a58b-917b739c3a38 |
| QM-Manager | AL |
| Email-Postfach | reklamation@schneider-kabelsatzbau.de |

---

## REIHENFOLGE

1. ✅ Aufgabe 1: Workflow testen - erledigt (2026-01-27)
2. ✅ Aufgabe 2: Phase 2 Nodes hinzufügen - erledigt (2026-01-27)
3. ✅ Aufgabe 3: Bestehende Workflows prüfen/konfigurieren - erledigt (2026-01-27)
   - RMS-Ordner-Sync: bereits konfiguriert
   - RMS-QA-ID-Generator: bereits konfiguriert
   - RMS-Eskalation-Monitor: NEU erstellt (ID: Z4D6ChArp86tDKC0)
4. ✅ Aufgabe 4: Error Handler erstellen - erledigt (2026-01-27)
   - RMS-Error-Handler erstellt (ID: Aq6gmrE8IX3RKIeF)
5. ✅ Aufgabe 5: Dokumentation - erledigt (2026-01-27)
   - /opt/osp/docs/RMS_WORKFLOWS.md erstellt
   - Backup: /opt/osp/backups/n8n_20260127/

Starte mit Aufgabe 2 und arbeite dich durch. Bei Fehlern: analysieren, fixen, dokumentieren.
