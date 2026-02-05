# NZA Phase4 Workflows - Import-Anleitung

**Stand:** 2026-02-05
**Status:** Bereit für Import

---

## Übersicht der Workflows

### Prozesse (Hauptliste nza-kpl)
| Workflow | HTTP | Pfad | Nginx-Endpoint |
|----------|------|------|----------------|
| NZA-Prozesse-List | GET | `/webhook/nza-prozesse` | `/api/nza/prozesse` |
| NZA-Prozesse-Create | POST | `/webhook/nza-prozesse` | `/api/nza/prozesse` |
| NZA-Prozesse-Update | PATCH | `/webhook/nza-prozesse` | `/api/nza/prozesse` |

### Maßnahmen (nza-massnahmen)
| Workflow | HTTP | Pfad | Nginx-Endpoint |
|----------|------|------|----------------|
| NZA-Massnahmen-List | GET | `/webhook/nza-massnahmen` | `/api/nza/massnahmen` |
| NZA-Massnahmen-Create | POST | `/webhook/nza-massnahmen` | `/api/nza/massnahmen` |
| NZA-Massnahmen-Update | PATCH | `/webhook/nza-massnahmen` | `/api/nza/massnahmen` |

### Bilder (nza-bilder)
| Workflow | HTTP | Pfad | Nginx-Endpoint |
|----------|------|------|----------------|
| NZA-Bilder-List | GET | `/webhook/nza-bilder` | `/api/nza/bilder` |

### Kosten
| Workflow | HTTP | Pfad | Nginx-Endpoint |
|----------|------|------|----------------|
| NZA-Kosten-Info | GET | `/webhook/nza-kosten` | `/api/nza/kosten` |
| NZA-Kosten-Berechnen | POST | `/webhook/nza-kosten` | `/api/nza/kosten` |

---

## Import-Anleitung

### Option 1: Über n8n Web-UI

1. Öffne https://n8n.schneider-kabelsatzbau.de/
2. Gehe zu **Workflows** → **Import from File**
3. Importiere die Dateien in dieser Reihenfolge:
   - `NZA-Prozesse-List.json`
   - `NZA-Prozesse-Create.json`
   - `NZA-Prozesse-Update.json`
   - `NZA-Massnahmen-List.json`
   - `NZA-Massnahmen-Create.json`
   - `NZA-Massnahmen-Update.json`
   - `NZA-Bilder-List.json`
   - `NZA-Kosten-Info.json`
   - `NZA-Kosten-Berechnen.json`
4. Aktiviere jeden Workflow nach dem Import (Toggle ON)

### Option 2: Über n8n API

```bash
# Auf dem Server ausführen
cd /mnt/HC_Volume_104189729/osp/nza/workflows/phase4

# API-Key aus n8n holen (Settings → API)
N8N_API_KEY="your-api-key"
N8N_URL="http://localhost:5678"

# Jeden Workflow importieren
for f in *.json; do
  curl -X POST "${N8N_URL}/api/v1/workflows" \
    -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
    -H "Content-Type: application/json" \
    -d @"$f"
  echo "Imported: $f"
done
```

---

## Credentials prüfen

Alle Workflows verwenden:
- **Microsoft SharePoint account** (ID: `5ZmmOyK1L7PhkJW2`)

Falls die Credentials nicht erkannt werden:
1. Workflow öffnen
2. HTTP Request Node auswählen
3. Credential neu zuweisen
4. Speichern

---

## Environment-Variablen

Diese Variablen müssen in n8n konfiguriert sein (docker-compose.yml):

```env
NZA_SITE_ID=rainerschneiderkabelsatz.sharepoint.com,2a90f256-47e6-4ad1-b0d8-341026f63dc3,83b8240d-ea97-48ed-9d46-b510152e29f9
NZA_KPL_LIST_ID=7bea980d-9a33-4db5-a844-5c5401872e20
NZA_MITARBEITER_LIST_ID=d6dbfa5c-08b3-4bef-bc4a-e840f254935b
NZA_CONFIG_LIST_ID=6e56d7d5-c018-4948-a519-96230e5919bf
NZA_MASSNAHMEN_LIST_ID=d59ef6e6-428f-4346-a6e2-9524d61c14bc
NZA_BILDER_LIST_ID=60847793-da02-4e12-ad0f-052d6157b51e
```

---

## Test-URLs

Nach dem Import und Aktivieren:

```bash
# Prozesse
curl https://osp.schneider-kabelsatzbau.de/api/nza/prozesse

# Maßnahmen
curl https://osp.schneider-kabelsatzbau.de/api/nza/massnahmen

# Bilder
curl https://osp.schneider-kabelsatzbau.de/api/nza/bilder

# Kosten (Minutensätze)
curl https://osp.schneider-kabelsatzbau.de/api/nza/kosten
```

---

## Bereits funktionierende Workflows (nicht ersetzen)

Diese Workflows aus der Basis-Installation funktionieren bereits:
- ✅ NZA-Mitarbeiter-API (GET /api/nza/mitarbeiter)
- ✅ NZA-Config-API (GET /api/nza/config)
- ✅ NZA-KPIs-API (GET /api/nza/kpis)
- ✅ NZA-Bilder-Upload (POST /api/nza/bilder-upload)
- ✅ NZA-Notify-API (POST /api/nza/notify)

---

*Erstellt: 2026-02-05*
