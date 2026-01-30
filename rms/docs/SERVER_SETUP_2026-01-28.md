# RMS Dashboard - Server Setup Anleitung

**Datum:** 2026-01-28
**Status:** Frontend vollstaendig aktualisiert
**Naechste Schritte:** Server-Konfiguration

---

## 1. Dashboard-Dateien auf Server kopieren

```bash
# Auf lokaler Maschine (oder via SCP)
scp -r /mnt/HC_Volume_104189729/osp/rms/dashboard/* root@46.224.102.30:/var/www/html/rms/
```

---

## 2. Nginx Konfiguration erweitern

In `/etc/nginx/sites-available/osp` die RMS API-Routen hinzufuegen:

```nginx
# RMS API Proxy (n8n Webhooks)
location /api/rms/reklamationen {
    proxy_pass http://127.0.0.1:5678/webhook/rms-reklamationen;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /api/rms/kpis {
    proxy_pass http://127.0.0.1:5678/webhook/rms-kpis;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}

location /api/rms/charts {
    proxy_pass http://127.0.0.1:5678/webhook/rms-charts;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}

# NEU: Detail-API fuer Massnahmen und Schriftverkehr
location /api/rms/detail {
    proxy_pass http://127.0.0.1:5678/webhook/rms-detail;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}

# NEU: Massnahmen API (POST)
location /api/rms/massnahmen {
    proxy_pass http://127.0.0.1:5678/webhook/rms-massnahmen;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header Content-Type application/json;
}

# NEU: PDF Generator
location /api/rms/pdf {
    proxy_pass http://127.0.0.1:5678/webhook/rms-pdf;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header Content-Type application/json;
}
```

Nach Aenderung:
```bash
nginx -t && systemctl reload nginx
```

---

## 3. n8n Workflows erstellen

### 3.1 RMS-Detail-API Workflow

**Webhook:** GET `/webhook/rms-detail?id={itemId}`

**Nodes:**

1. **Webhook Trigger**
   - Method: GET
   - Path: `rms-detail`
   - Response Mode: Last Node

2. **Reklamation laden** (HTTP Request)
   ```
   Method: GET
   URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/lists/e9b1d926-085a-4435-a012-114ca9ba59a8/items/{{ $json.query.id }}?$expand=fields
   Authentication: OAuth2 (Microsoft account)
   ```

3. **Massnahmen laden** (HTTP Request)
   ```
   Method: GET
   URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/lists/3768f2d8-878c-4a5f-bd52-7486fe93289d/items?$expand=fields&$filter=fields/Rekla_IDLookupId eq {{ $json.query.id }}
   Headers: Prefer: HonorNonIndexedQueriesWarningMayFailRandomly
   ```

4. **Schriftverkehr laden** (HTTP Request)
   ```
   Method: GET
   URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/lists/741c6ae8-88bb-406b-bf85-2e11192a528f/items?$expand=fields&$filter=fields/QA_IDLookupId eq {{ $json.query.id }}
   Headers: Prefer: HonorNonIndexedQueriesWarningMayFailRandomly
   ```

5. **Merge Results** (Code Node)
   ```javascript
   const rekla = $('Reklamation laden').item.json;
   const massnahmen = $('Massnahmen laden').item.json;
   const schriftverkehr = $('Schriftverkehr laden').item.json;

   return {
     reklamation: rekla.fields || rekla,
     massnahmen: massnahmen.value?.map(m => m.fields) || [],
     schriftverkehr: schriftverkehr.value?.map(s => s.fields) || [],
     sharePointUrl: `https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS/Lists/Reklamationen/DispForm.aspx?ID=${rekla.id}`
   };
   ```

6. **Respond to Webhook**

---

### 3.2 RMS-Massnahmen-API Workflow

**Webhook:** POST `/webhook/rms-massnahmen`

**Nodes:**

1. **Webhook Trigger**
   - Method: POST
   - Path: `rms-massnahmen`
   - Response Mode: Last Node

2. **Create Massnahme** (HTTP Request)
   ```
   Method: POST
   URL: https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c/lists/3768f2d8-878c-4a5f-bd52-7486fe93289d/items
   Authentication: OAuth2 (Microsoft account)
   Body (JSON):
   {
     "fields": {
       "Title": "{{ $json.body.title }}",
       "Rekla_IDLookupId": {{ $json.body.reklaId }},
       "Typ": "{{ $json.body.typ }}",
       "Termin": "{{ $json.body.termin }}",
       "Status": "Offen",
       "Verantwortlich": "{{ $json.body.verantwortlich }}"
     }
   }
   ```

3. **Respond to Webhook**

---

### 3.3 RMS-Charts Workflow erweitern

Im bestehenden RMS-Charts Workflow den Code Node erweitern:

```javascript
const items = $input.all();

// Status zaehlen
const statusCounts = { Neu: 0, 'In Bearbeitung': 0, Massnahmen: 0, Abgeschlossen: 0 };
const priorityCounts = { kritisch: 0, hoch: 0, mittel: 0, niedrig: 0 };

items.forEach(item => {
    const status = item.json.fields?.Rekla_Status || 'Neu';
    const prio = (item.json.fields?.Prioritaet || 'mittel').toLowerCase();

    if (statusCounts[status] !== undefined) statusCounts[status]++;
    if (priorityCounts[prio] !== undefined) priorityCounts[prio]++;
});

return {
    // ... bestehende Daten (trend, typ, kst) ...
    status: [statusCounts.Neu, statusCounts['In Bearbeitung'], statusCounts.Massnahmen, statusCounts.Abgeschlossen],
    priority: [priorityCounts.kritisch, priorityCounts.hoch, priorityCounts.mittel, priorityCounts.niedrig]
};
```

---

## 4. SharePoint Listen-IDs (Referenz)

| Liste | ID |
|-------|-----|
| **Reklamationen** | `e9b1d926-085a-4435-a012-114ca9ba59a8` |
| **Massnahmen** | `3768f2d8-878c-4a5f-bd52-7486fe93289d` |
| **Schriftverkehr** | `741c6ae8-88bb-406b-bf85-2e11192a528f` |
| **Site ID** | `rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c` |
| **Credential ID** | `Fm3IuAbVYBYDIA4U` |

---

## 5. Neue Features im Frontend

### Implementiert:
- [x] Loading-Spinner waehrend API-Calls
- [x] Suchfeld (durchsucht QA-ID, Titel, Beschreibung, KST, Verantwortlich)
- [x] Sortierung per Klick auf Spaltenheader
- [x] CSV-Export Button
- [x] Status-Chart (Pie)
- [x] Prioritaet-Chart (Bar horizontal)
- [x] Detail-API vorbereitet (Massnahmen + Schriftverkehr)
- [x] Massnahmen-Modal zum Erstellen neuer Massnahmen

### Benoetigt Server-Setup:
- [ ] Detail-API n8n Workflow
- [ ] Massnahmen-API n8n Workflow
- [ ] Charts-Workflow erweitern (Status/Prioritaet)
- [ ] Nginx-Routen aktualisieren

---

## 6. Test nach Deployment

```bash
# Dashboard erreichbar?
curl -s https://osp.schneider-kabelsatzbau.de/rms/

# APIs erreichbar?
curl -s https://osp.schneider-kabelsatzbau.de/api/rms/reklamationen | head
curl -s https://osp.schneider-kabelsatzbau.de/api/rms/kpis
curl -s "https://osp.schneider-kabelsatzbau.de/api/rms/detail?id=1"
```

---

*Erstellt: 2026-01-28 | AL (via Claude Code)*
