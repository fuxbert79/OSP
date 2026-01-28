# RMS Dashboard - Edit-Funktionalitaet Server-Setup

**Datum:** 2026-01-28
**Status:** Bereit zur Umsetzung

---

## 1. n8n Workflows importieren

### SSH-Verbindung

```bash
ssh root@46.224.102.30
```

### Workflows in n8n importieren

Die Workflow-Dateien liegen unter `/mnt/HC_Volume_104189729/osp/rms/workflows/`:

- `RMS-Update-Reklamation.json`
- `RMS-Update-Massnahme.json`
- `RMS-Delete-Massnahme.json`

**Import-Schritte:**

1. n8n UI oeffnen: http://46.224.102.30:5678
2. Settings > Import from File
3. Jeden Workflow importieren
4. Credential "Microsoft Account" (Fm3IuAbVYBYDIA4U) zuweisen
5. Workflows aktivieren

**Alternative per API:**

```bash
# Workflows auf Server kopieren
scp /mnt/HC_Volume_104189729/osp/rms/workflows/*.json root@46.224.102.30:/tmp/

# SSH und importieren
ssh root@46.224.102.30

# Import via n8n CLI (falls verfuegbar)
cd /tmp
for f in RMS-*.json; do
  curl -X POST "http://127.0.0.1:5678/api/v1/workflows" \
    -H "Content-Type: application/json" \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -d @"$f"
done
```

---

## 2. Nginx Konfiguration erweitern

### Datei bearbeiten

```bash
nano /etc/nginx/sites-available/osp
```

### Folgende Location-Bloecke hinzufuegen

```nginx
# RMS Update APIs (PATCH)
location /api/rms/update {
    proxy_pass http://127.0.0.1:5678/webhook/rms-update;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Content-Type application/json;
}

location /api/rms/update-massnahme {
    proxy_pass http://127.0.0.1:5678/webhook/rms-update-massnahme;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Content-Type application/json;
}

location /api/rms/delete-massnahme {
    proxy_pass http://127.0.0.1:5678/webhook/rms-delete-massnahme;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### Konfiguration pruefen und neu laden

```bash
nginx -t && systemctl reload nginx
```

---

## 3. Frontend-Dateien aktualisieren

Die aktualisierten Dateien muessen auf den Server kopiert werden:

```bash
# Lokale Dateien auf Server kopieren
scp /mnt/HC_Volume_104189729/osp/rms/dashboard/index.html root@46.224.102.30:/var/www/html/rms/
scp /mnt/HC_Volume_104189729/osp/rms/dashboard/js/app.js root@46.224.102.30:/var/www/html/rms/js/
scp /mnt/HC_Volume_104189729/osp/rms/dashboard/css/style.css root@46.224.102.30:/var/www/html/rms/css/
```

---

## 4. Test der Edit-Funktionalitaet

### API-Test (PATCH Reklamation)

```bash
curl -X PATCH "https://osp.schneider-kabelsatzbau.de/api/rms/update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "1",
    "fields": {
      "Rekla_Status": "In Bearbeitung"
    }
  }'
```

### API-Test (PATCH Massnahme)

```bash
curl -X PATCH "https://osp.schneider-kabelsatzbau.de/api/rms/update-massnahme" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "1",
    "fields": {
      "Status": "Erledigt"
    }
  }'
```

### API-Test (DELETE Massnahme)

```bash
curl -X DELETE "https://osp.schneider-kabelsatzbau.de/api/rms/delete-massnahme?id=1"
```

---

## 5. Checkliste

Nach Abschluss pruefen:

- [ ] n8n Workflow "RMS-Update-Reklamation" importiert und aktiv
- [ ] n8n Workflow "RMS-Update-Massnahme" importiert und aktiv
- [ ] n8n Workflow "RMS-Delete-Massnahme" importiert und aktiv
- [ ] Nginx Route /api/rms/update konfiguriert
- [ ] Nginx Route /api/rms/update-massnahme konfiguriert
- [ ] Nginx Route /api/rms/delete-massnahme konfiguriert
- [ ] Frontend-Dateien aktualisiert
- [ ] Edit-Button im Detail-Modal sichtbar
- [ ] Edit-Formular funktioniert
- [ ] Speichern aktualisiert SharePoint
- [ ] Massnahmen-Inline-Edit funktioniert
- [ ] Massnahmen-Loeschen funktioniert

---

## 6. Fehlerbehebung

### Workflow nicht erreichbar

```bash
# n8n Logs pruefen
docker logs n8n --tail 100

# Workflow-Status pruefen
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "http://127.0.0.1:5678/api/v1/workflows"
```

### Nginx-Fehler

```bash
# Nginx Error Log
tail -50 /var/log/nginx/error.log

# Konfiguration testen
nginx -t
```

### CORS-Probleme

Falls CORS-Fehler auftreten, in Nginx hinzufuegen:

```nginx
location /api/rms/ {
    add_header 'Access-Control-Allow-Origin' '*' always;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PATCH, DELETE, OPTIONS' always;
    add_header 'Access-Control-Allow-Headers' 'Content-Type' always;

    if ($request_method = 'OPTIONS') {
        return 204;
    }

    # ... proxy_pass ...
}
```

---

*Erstellt: 2026-01-28 | Ziel: Editierbarkeit im RMS Dashboard*
