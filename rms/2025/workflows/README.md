# RMS 2025 Dashboard - Deployment Guide

## Uebersicht

Dieses Verzeichnis enthaelt die n8n-Workflows fuer das RMS 2025 Archiv-Dashboard.

## Workflows

| Workflow | Datei | Zweck |
|----------|-------|-------|
| **RMS-2025-Setup-Liste** | RMS-2025-Setup-Liste.json | Erstellt SharePoint-Liste "Reklamationen-2025" |
| **RMS-2025-Import-Daten** | RMS-2025-Import-Daten.json | Importiert alle 27 Reklamationen in SharePoint |
| **RMS-2025-Dashboard-API** | RMS-2025-Dashboard-API.json | API-Endpunkte fuer das Dashboard |

## Deployment-Schritte

### 1. Workflows in n8n importieren

```bash
# Per CLI (wenn n8n CLI installiert)
n8n import:workflow --input=/mnt/HC_Volume_104189729/osp/rms/2025/workflows/RMS-2025-Setup-Liste.json
n8n import:workflow --input=/mnt/HC_Volume_104189729/osp/rms/2025/workflows/RMS-2025-Import-Daten.json
n8n import:workflow --input=/mnt/HC_Volume_104189729/osp/rms/2025/workflows/RMS-2025-Dashboard-API.json
```

Oder manuell ueber die n8n UI:
1. n8n oeffnen: https://n8n.schneider-kabelsatzbau.de
2. Menu > Import from File
3. Alle 3 JSON-Dateien importieren

### 2. SharePoint-Liste erstellen

**Option A: Per Workflow**
```bash
curl -X POST https://n8n.schneider-kabelsatzbau.de/webhook/rms2025/setup
```

**Option B: Manuell in SharePoint**
1. SharePoint Site /sites/RMS oeffnen
2. Neue Liste "Reklamationen-2025" erstellen
3. Folgende Spalten hinzufuegen:
   - QA_ID (Text)
   - Rekla_Typ (Auswahl: Kunde, Lieferant)
   - Absender (Text)
   - Artikel_Nr (Text)
   - Erfassungsdatum (Datum)
   - Formular (Text)
   - Status (Auswahl: Abgeschlossen, Offen)
   - Fehler_Beschreibung (Mehrzeiliger Text)
   - Dateien (Mehrzeiliger Text)
   - Verursacher (Text)
   - Kostenstelle (Text)
   - NZA_Kosten (Zahl)
   - Q_Nr_Kunde (Text)

### 3. Daten importieren

```bash
# Import-Workflow ausfuehren
curl -X POST https://n8n.schneider-kabelsatzbau.de/webhook/rms2025/import \
  -H "Content-Type: application/json" \
  -d '{"listId": "LISTE-ID-HIER"}'
```

**Hinweis:** Die Liste-ID findest du nach dem Setup in der SharePoint-URL oder in der Workflow-Response.

### 4. API-Workflow aktivieren

1. In n8n den Workflow "RMS-2025-Dashboard-API" oeffnen
2. Credentials pruefen (Microsoft SharePoint account)
3. Liste-ID in allen SharePoint-Nodes anpassen (falls noetig)
4. Workflow aktivieren (Toggle oben rechts)

### 5. Nginx-Konfiguration

Fuege folgende Location-Blöcke zur nginx.conf hinzu:

```nginx
# RMS 2025 Dashboard
location /rms/2025/ {
    alias /mnt/HC_Volume_104189729/osp/rms/2025/dashboard/;
    try_files $uri $uri/ /rms/2025/index.html;
}

# RMS 2025 API
location /api/rms2025/ {
    proxy_pass http://127.0.0.1:5678/webhook/rms2025/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Danach nginx neu laden:
```bash
sudo nginx -t && sudo systemctl reload nginx
```

### 6. Dashboard testen

```bash
# KPIs abrufen
curl https://osp.schneider-kabelsatzbau.de/api/rms2025/kpis

# Reklamationen abrufen
curl https://osp.schneider-kabelsatzbau.de/api/rms2025/reklamationen

# Charts-Daten abrufen
curl https://osp.schneider-kabelsatzbau.de/api/rms2025/charts

# Dashboard im Browser oeffnen
https://osp.schneider-kabelsatzbau.de/rms/2025/
```

## API-Endpunkte

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/rms2025/kpis` | GET | KPI-Kennzahlen |
| `/api/rms2025/reklamationen` | GET | Alle Reklamationen (mit Filter) |
| `/api/rms2025/detail/:id` | GET | Detail-Ansicht einer Reklamation |
| `/api/rms2025/charts` | GET | Chart-Daten (Trend, Typ, Absender) |

### Query-Parameter (Reklamationen)

- `?typ=Kunde` - Filter nach Typ
- `?typ=Lieferant` - Filter nach Typ
- `?search=laserline` - Volltextsuche

## Fallback-Modus

Das Dashboard hat eingebettete Fallback-Daten. Falls die API nicht erreichbar ist:
- KPIs werden mit statischen Werten angezeigt
- Tabelle zeigt alle 27 Reklamationen
- Charts verwenden vordefinierte Daten

## Credentials

Verwendet werden:
- **Microsoft SharePoint OAuth2 API** (ID: 5ZmmOyK1L7PhkJW2)
- Site ID: `rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c`

## Dateien

```
/mnt/HC_Volume_104189729/osp/rms/2025/
├── dashboard/
│   └── index.html          # Dashboard HTML
├── workflows/
│   ├── README.md           # Diese Datei
│   ├── RMS-2025-Setup-Liste.json
│   ├── RMS-2025-Import-Daten.json
│   └── RMS-2025-Dashboard-API.json
├── Reklamationen_2025.md   # Dokumentation aller 27 Reklamationen
└── QA-25XXX/               # Ordner pro Reklamation (27 Stueck)
```

## Support

Bei Fragen: AL (QM-Manager)

---
**Erstellt:** 02.02.2026
**Version:** 1.0
