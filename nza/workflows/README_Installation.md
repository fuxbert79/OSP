# NZA n8n Workflows - Installationsanleitung

## Voraussetzungen

1. **Microsoft OAuth2 Credentials** in n8n konfiguriert (Name: "Microsoft OAuth2")
2. **SharePoint Site** `/sites/NZA_NEU` existiert
3. **Berechtigungen:** Sites.ReadWrite.All, Lists.ReadWrite.All

---

## Installation - Schritt für Schritt

### Schritt 1: Workflows importieren

In n8n unter **Workflows → Import from File** die JSONs in dieser Reihenfolge importieren:

| # | Datei | Beschreibung |
|---|-------|--------------|
| 1 | `01_NZA_Setup_Listen.json` | Erstellt die 5 SharePoint-Listen |
| 2 | `02_NZA_Setup_Spalten_KPL.json` | Fügt 40+ Spalten zur Hauptliste hinzu |
| 3 | `03_NZA_Import_Mitarbeiter.json` | Importiert 53 Mitarbeiter |
| 4 | `04_NZA_Import_Config.json` | Importiert Konfiguration (Minutensätze etc.) |
| 5 | `05_NZA_Prozesse_API.json` | API für Dashboard (GET/POST/PATCH) |
| 6 | `06_NZA_Mitarbeiter_API.json` | API für Verursacher-Dropdown |

### Schritt 2: Credentials zuweisen

Nach dem Import in jedem Workflow:
1. Workflow öffnen
2. HTTP Request Nodes anklicken
3. Credentials "Microsoft OAuth2" auswählen
4. Speichern

### Schritt 3: Setup-Workflows ausführen (EINMALIG!)

**Wichtig:** Diese Workflows nur EINMAL ausführen!

1. **01_NZA_Setup_Listen** → Manuell starten → Erstellt Listen
2. Warten bis abgeschlossen
3. **02_NZA_Setup_Spalten_KPL** → Manuell starten → Erstellt Spalten
4. **03_NZA_Import_Mitarbeiter** → Manuell starten → 53 MA importiert
5. **04_NZA_Import_Config** → Manuell starten → Konfiguration importiert

### Schritt 4: Environment Variables setzen

In n8n Settings → Variables oder in docker-compose.yml:

```env
NZA_SITE_ID=<aus Schritt 1 Output>
NZA_KPL_LIST_ID=<List-ID von "NZA Hauptliste">
NZA_MITARBEITER_LIST_ID=<List-ID von "NZA Mitarbeiter">
NZA_CONFIG_LIST_ID=<List-ID von "NZA Konfiguration">
NZA_MASSNAHMEN_LIST_ID=<List-ID von "NZA Maßnahmen">
NZA_BILDER_LIST_ID=<List-ID von "NZA Bilder">
```

**Site-ID ermitteln:**
```bash
curl -H "Authorization: Bearer <TOKEN>" \
  "https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com:/sites/NZA_NEU" \
  | jq '.id'
```

**List-IDs ermitteln:**
```bash
curl -H "Authorization: Bearer <TOKEN>" \
  "https://graph.microsoft.com/v1.0/sites/<SITE_ID>/lists" \
  | jq '.value[] | {name: .displayName, id: .id}'
```

### Schritt 5: API-Workflows aktivieren

1. **05_NZA_Prozesse_API** → Aktivieren (Toggle ON)
2. **06_NZA_Mitarbeiter_API** → Aktivieren (Toggle ON)

Webhook-URLs werden angezeigt, z.B.:
- `https://n8n.example.com/webhook/nza-prozesse`
- `https://n8n.example.com/webhook/nza-mitarbeiter`

---

## Nginx-Konfiguration

In `/etc/nginx/sites-available/osp` ergänzen:

```nginx
# NZA API Endpoints
location = /api/nza/prozesse {
    proxy_pass http://127.0.0.1:5678/webhook/nza-prozesse;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
    add_header Access-Control-Allow-Methods "GET, POST, PATCH, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Content-Type" always;
    if ($request_method = OPTIONS) { return 204; }
}

location = /api/nza/mitarbeiter {
    proxy_pass http://127.0.0.1:5678/webhook/nza-mitarbeiter;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

# NZA Dashboard
location /nza/ {
    alias /var/www/html/nza/;
    try_files $uri $uri/ /nza/index.html;
}
```

Danach: `sudo nginx -t && sudo systemctl reload nginx`

---

## Test

### API testen

```bash
# Mitarbeiter laden
curl http://localhost/api/nza/mitarbeiter | jq

# NZA-Liste laden
curl http://localhost/api/nza/prozesse | jq

# Neuen NZA anlegen
curl -X POST http://localhost/api/nza/prozesse \
  -H "Content-Type: application/json" \
  -d '{
    "typ": "Interne Reklamation",
    "datum": "2026-01-30",
    "artikel": "KB-TEST-001",
    "kst": "1000",
    "beschreibung": "Test-NZA",
    "kategorien": ["Crimpfehler"],
    "prozesse": [{"prozess": "Nachcrimpen", "kst": "1000", "zeit": 30}]
  }' | jq
```

---

## Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| "Site not found" | Site-URL prüfen, evtl. `/sites/NZA_NEU` statt `/sites/nza` |
| "401 Unauthorized" | OAuth Token abgelaufen, neu authentifizieren |
| "List not found" | Liste noch nicht erstellt, Workflow 01 ausführen |
| Spalten fehlen | Workflow 02 erneut ausführen |

---

*Erstellt: 2026-01-30*
