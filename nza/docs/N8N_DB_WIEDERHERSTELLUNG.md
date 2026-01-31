# n8n Datenbank Wiederherstellung

**Erstellt:** 2026-01-31
**Problem:** SQLite-Datenbank war beschädigt (SQLITE_CORRUPT)

---

## Vorhandene Backups

| Datei | Größe | Status |
|-------|-------|--------|
| `database.sqlite.backup_20260131_133900` | 478 MB | Beschädigt (JSON-Fehler) |
| `database.sqlite.damaged_20260131_134111` | 692 KB | Beschädigt |
| `database.sqlite.damaged2_*` | variabel | Beschädigt |

**Pfad:** `/mnt/HC_Volume_104189729/docker/volumes/osp-n8n-data/_data/`

---

## Exportierte Daten

### Workflows (33 Stück)
**Datei:** `workflows_export.json`

| Typ | Anzahl |
|-----|--------|
| RMS-Workflows | 22 |
| NZA-Workflows | 11 |

### Credentials (4 Stück)
**Datei:** `credentials_export.json`

| ID | Name | Typ |
|----|------|-----|
| Fm3IuAbVYBYDIA4U | Microsoft account | microsoftOAuth2Api |
| 5uLP7Ea6jOpXoiQb | Anthropic account | anthropicApi |
| Ybjb1GAPEge4UD0I | OpenAi account | openAiApi |
| IiKvWNmfpn6etjGG | Microsoft SharePoint account | microsoftSharePointOAuth2Api |

---

## Wiederherstellungsschritte

### Option A: Aus exportierten Daten (empfohlen)

```bash
# 1. n8n stoppen
docker stop n8n

# 2. Alte DB sichern/löschen
cd /mnt/HC_Volume_104189729/docker/volumes/osp-n8n-data/_data/
mv database.sqlite database.sqlite.old_$(date +%Y%m%d_%H%M%S)
rm -f database.sqlite-wal database.sqlite-shm

# 3. n8n starten (erstellt frische DB)
docker start n8n
sleep 30
docker stop n8n

# 4. Credentials importieren
while IFS= read -r line; do
    id=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['id'])")
    name=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['name'])")
    type=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['type'])")
    data=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'])")
    sqlite3 database.sqlite "INSERT OR REPLACE INTO credentials_entity (id, name, type, data, createdAt, updatedAt) VALUES ('$id', '$name', '$type', '$data', datetime('now'), datetime('now'));"
done < credentials_export.json

# 5. Workflows importieren (Python-Script)
python3 << 'PYEOF'
import sqlite3
import json
import uuid

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

with open('workflows_export.json', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            wf = json.loads(line)
            version_id = wf.get('versionId') or str(uuid.uuid4())
            cursor.execute("""
                INSERT OR REPLACE INTO workflow_entity
                (id, name, active, nodes, connections, settings, versionId, createdAt, updatedAt)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (
                wf['id'],
                wf['name'],
                0,  # Erstmal inaktiv
                wf['nodes'],
                wf['connections'],
                wf.get('settings', '{}'),
                version_id
            ))
        except Exception as e:
            print(f"Error: {e}")

conn.commit()
conn.close()
PYEOF

# 6. RMS-Workflows aktivieren
sqlite3 database.sqlite "UPDATE workflow_entity SET active = 1 WHERE name LIKE 'RMS%';"

# 7. n8n starten
docker start n8n
```

### Option B: Aus lokalen JSON-Dateien

Falls die Export-Dateien nicht vorhanden sind, können Workflows aus den lokalen JSON-Dateien importiert werden:

**NZA-Workflows:**
```
/mnt/HC_Volume_104189729/osp/nza/workflows/
```

**RMS-Workflows:**
```
/opt/osp/rms/workflows/
```

**Import über n8n CLI:**
```bash
docker cp /pfad/zu/workflow.json n8n:/tmp/
docker exec n8n n8n import:workflow --input=/tmp/workflow.json
```

---

## Bekannte Probleme

### 1. JSON-Fehler bei Workflow-Aktivierung
**Fehler:** `SyntaxError: Expected property name or '}' in JSON at position 3217`

**Ursache:** Beschädigte Ausführungsdaten in execution_data Tabelle

**Lösung:** Execution-Daten löschen:
```bash
sqlite3 database.sqlite "DELETE FROM execution_data;"
sqlite3 database.sqlite "DELETE FROM execution_entity;"
```

### 2. NZA-Workflows verursachen Absturz
**Lösung:** NZA-Workflows deaktiviert lassen:
```bash
sqlite3 database.sqlite "UPDATE workflow_entity SET active = 0 WHERE name LIKE 'NZA%';"
```

### 3. Webhooks nicht registriert
**Ursache:** Workflows müssen einem Benutzer zugeordnet sein

**Lösung:** In n8n-UI einloggen und Workflows manuell aktivieren

---

## Credentials neu einrichten (falls nötig)

Falls die Credentials nicht wiederhergestellt werden können, müssen sie in der n8n-UI neu konfiguriert werden:

1. https://n8n.schneider-kabelsatzbau.de öffnen
2. Settings > Credentials > Add Credential
3. **Microsoft OAuth2 API** mit Azure App-Daten konfigurieren:
   - App: OSP-n8n-Integration
   - Client ID: (aus Azure Portal)
   - Client Secret: (aus Azure Portal)
   - Scopes: `Sites.ReadWrite.All Files.ReadWrite.All Mail.Read offline_access`

---

## Wichtige Umgebungsvariablen

In `/opt/osp/docker-compose.yml` unter n8n:

```yaml
environment:
  - N8N_BLOCK_ENV_ACCESS_IN_NODE=false
  - NZA_SITE_ID=rainerschneiderkabelsatz.sharepoint.com,2a90f256-47e6-4ad1-b0d8-341026f63dc3,83b8240d-ea97-48ed-9d46-b510152e29f9
  - NZA_KPL_LIST_ID=7bea980d-9a33-4db5-a844-5c5401872e20
  - NZA_MITARBEITER_LIST_ID=d6dbfa5c-08b3-4bef-bc4a-e840f254935b
  - NZA_CONFIG_LIST_ID=6e56d7d5-c018-4948-a519-96230e5919bf
  - NZA_MASSNAHMEN_LIST_ID=d59ef6e6-428f-4346-a6e2-9524d61c14bc
  - NZA_BILDER_LIST_ID=60847793-da02-4e12-ad0f-052d6157b51e
```

---

## Workflow-Liste (zur Referenz)

### RMS-Workflows (22)
1. RMS-QA-ID-Generator
2. RMS-Ordner-Sync
3. RMS-Email-Import-V2
4. RMS-Eskalation-Monitor
5. RMS-Error-Handler
6. RMS-KPIs
7. RMS-Reklamationen
8. RMS-Charts
9. RMS-Massnahmen-API
10. RMS-Update-Reklamation
11. RMS-Update-Massnahme
12. RMS-Delete-Massnahme
13. RMS-Detail-API
14. RMS-Notify-Massnahme
15. RMS-Files-API
16. RMS-Create-Massnahme
17. RMS-Generate-Formblatt
18. RMS-Users-API-v2
19. RMS-Stammdaten-API
20. RMS-Create-Reklamation
21. RMS-Send-Email
22. RMS-Tracking-Erinnerung

### NZA-Workflows (11)
1. NZA-Prozesse-API
2. NZA-Mitarbeiter-API
3. NZA-Massnahmen-API
4. NZA-Bilder-API
5. NZA-Bilder-Upload
6. NZA-Notify-API
7. NZA-Kosten-API
8. NZA-Config-API
9. NZA-KPIs-API
10. NZA-Import-Mitarbeiter
11. NZA-Import-Config

---

---

## Wiederherstellung durchgeführt (2026-01-31)

### Erfolgreich wiederhergestellt:
- **33 Workflows** (22 RMS + 11 NZA)
- **4 Credentials** (Microsoft OAuth2, Anthropic, OpenAI, SharePoint)

### Nächster Schritt (MANUELL erforderlich):

**Workflows müssen in der n8n-UI aktiviert werden:**

1. https://n8n.schneider-kabelsatzbau.de öffnen
2. Einloggen
3. Für jeden RMS-Workflow:
   - Workflow öffnen
   - Toggle auf "Active" setzen

**Wichtige RMS-Workflows (Priorität):**
- RMS-Reklamationen (API)
- RMS-Detail-API
- RMS-Massnahmen-API
- RMS-Users-API-v2
- RMS-Email-Import-V2

### Bekanntes Problem:
Die n8n CLI-Aktivierung (`update:workflow --active`) funktioniert nicht mit dem neuen Versionierungssystem. Die Workflows müssen über die Web-UI aktiviert werden.

---

*Dokumentation erstellt: 2026-01-31*
*Wiederherstellung durchgeführt: 2026-01-31 14:xx*
