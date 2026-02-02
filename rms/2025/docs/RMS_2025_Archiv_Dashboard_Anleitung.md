# RMS 2025 Archiv-Dashboard - Implementierungsbericht

**Erstellt:** 02.02.2026
**Autor:** Claude (Opus 4.5)
**Zweck:** Dokumentation der Vorgehensweise zur Erstellung eines Archiv-Dashboards für abgeschlossene Geschäftsjahre

---

## Übersicht

Das RMS 2025 Archiv-Dashboard wurde erstellt, um die 27 Reklamationen aus dem Geschäftsjahr 2025 in einem read-only Dashboard anzuzeigen. Die Daten sind statisch eingebettet (kein Live-SharePoint-Zugriff), die Dateien verlinken jedoch direkt zu SharePoint.

**Live-URL:** https://osp.schneider-kabelsatzbau.de/rms/2025/

---

## Architektur

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Dashboard     │────▶│   Nginx Proxy   │────▶│   n8n Workflow  │
│   (HTML/JS)     │     │   /api/rms2025  │     │   (Standalone)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                                               │
        │                                               │
        ▼                                               ▼
┌─────────────────┐                           ┌─────────────────┐
│   SharePoint    │                           │  Embedded Data  │
│   (Datei-Links) │                           │  (27 Einträge)  │
└─────────────────┘                           └─────────────────┘
```

**Wichtig:** Der n8n-Workflow enthält alle Daten direkt im JavaScript-Code (Standalone). Kein SharePoint-API-Zugriff nötig, da Archiv-Daten statisch sind.

---

## Schritt 1: Daten sammeln

### 1.1 Reklamationen-Daten

Für jede Reklamation werden folgende Felder benötigt:

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| id | Number | Laufende Nummer (1-27) |
| qa_id | String | QA-ID (z.B. "QA-25001") |
| typ | String | "Kunde" oder "Lieferant" |
| absender | String | Firmenname |
| artikel | String | Artikelnummer |
| datum | String | ISO-Datum (YYYY-MM-DD) |
| formular | String | "NZA", "8D", "QA", "-" etc. |
| status | String | "Abgeschlossen" oder "Offen" |
| fehler | String | Fehlerbeschreibung |
| ordner | String | SharePoint-Ordnername (z.B. "QA-25001 Laserline") |
| dateien | Array | Liste der Dateinamen im Ordner |

### 1.2 KPI-Daten

```javascript
{
  gesamt: 27,           // Gesamtzahl Reklamationen
  kunden: 16,           // Kundenreklamationen
  lieferanten: 11,      // Lieferantenreklamationen
  offen: 1,             // Noch offene
  abgeschlossen: 26,    // Abgeschlossene
  abschlussquote: 96,   // Prozent
  mitNza: 10,           // Mit NZA-Formular
  mit8d: 5,             // Mit 8D-Report
  nzaKosten: 3846.73    // Summe NZA-Kosten
}
```

### 1.3 Chart-Daten

```javascript
{
  monthly: [1,4,0,5,3,2,1,0,1,1,0,0],  // Reklamationen pro Monat (Jan-Dez)
  typ: { Kunde: 16, Lieferant: 11 },
  absender: {
    labels: ['Laserline', 'Püplichhuisen', ...],  // Top-Absender
    values: [6, 3, ...]
  },
  formular: { NZA: 10, '8D': 5, QA: 12, Ohne: 5 }
}
```

---

## Schritt 2: n8n Workflow erstellen

### 2.1 Workflow-Struktur

Datei: `workflows/RMS-2025-Dashboard-API-Standalone.json`

```
Webhook KPIs ─────▶ KPIs Data ─────▶ Response KPIs
Webhook Reklamationen ─▶ Reklamationen Data ─▶ Response Reklamationen
Webhook Charts ───▶ Charts Data ───▶ Response Charts
```

### 2.2 Webhook-Konfiguration

| Webhook | Path | Methode |
|---------|------|---------|
| KPIs | `rms2025/kpis` | GET |
| Reklamationen | `rms2025/reklamationen` | GET |
| Charts | `rms2025/charts` | GET |

**Wichtig:**
- `responseMode: "responseNode"` setzen
- `options: { "allowedOrigins": "*" }` für CORS

### 2.3 Code-Nodes (JavaScript)

Die Daten werden direkt im Code-Node als JavaScript-Array/Object definiert:

```javascript
// KPIs Data Node
return [{json:{
  gesamt:27,
  kunden:16,
  lieferanten:11,
  // ... weitere KPIs
}}];

// Reklamationen Data Node
const r = [
  {id:1, qa_id:'QA-25001', typ:'Kunde', absender:'Laserline', ...},
  {id:2, qa_id:'QA-25002', ...},
  // ... alle 27 Einträge
];
// Optional: Filter-Logik
const query = $input.first().json.query || {};
let result = r;
if (query.typ) result = result.filter(x => x.typ === query.typ);
if (query.search) { /* Suchlogik */ }
return [{json:{data:result, count:result.length}}];
```

**WICHTIG:** Response muss Object sein, nicht Array!
- Falsch: `return [{json: arrayData}]`
- Richtig: `return [{json: {data: arrayData, count: arrayData.length}}]`

### 2.4 Response-Nodes

```javascript
{
  "respondWith": "json",
  "responseBody": "={{ $json }}",
  "options": {
    "responseHeaders": {
      "entries": [
        { "name": "Access-Control-Allow-Origin", "value": "*" },
        { "name": "Content-Type", "value": "application/json" }
      ]
    }
  }
}
```

---

## Schritt 3: Nginx konfigurieren

Datei: `/etc/nginx/sites-available/osp`

### 3.1 Dashboard-Location

```nginx
# Dashboard statische Dateien
location /rms/2025/ {
    alias /var/www/html/rms/2025/;
    index index.html;
    try_files $uri $uri/ =404;
}
```

### 3.2 API-Endpoints

```nginx
location = /api/rms2025/kpis {
    proxy_pass http://127.0.0.1:5678/webhook/rms2025/kpis;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

location = /api/rms2025/reklamationen {
    proxy_pass http://127.0.0.1:5678/webhook/rms2025/reklamationen;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

location = /api/rms2025/charts {
    proxy_pass http://127.0.0.1:5678/webhook/rms2025/charts;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}
```

### 3.3 Nginx neu laden

```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## Schritt 4: Dashboard HTML erstellen

Datei: `/var/www/html/rms/2025/index.html`

### 4.1 Grundstruktur

- Header mit Titel und "ARCHIV 2025" Badge
- KPI-Cards (8 Karten)
- Filter-Sektion (Suche + Typ-Filter)
- Tabelle mit allen Reklamationen
- Charts (Trend, Typ-Verteilung, Top-Absender)
- Detail-Modal mit Datei-Liste
- Footer

### 4.2 SharePoint-Datei-Links

```javascript
const SP_BASE = 'https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS/Freigegebene%20Dokumente/2025/';

function buildSharePointUrl(ordner, datei) {
    return SP_BASE + encodeURIComponent(ordner) + '/' + encodeURIComponent(datei);
}
```

**WICHTIG:** SharePoint-Subdomain ist `rainerschneiderkabelsatz` (nicht `schneiderkabelsatzbau`!)

### 4.3 API-Aufrufe

```javascript
const API_BASE = '/api/rms2025';

async function fetchAPI(endpoint) {
    const response = await fetch(`${API_BASE}/${endpoint}`);
    return response.json();
}

async function loadReklamationen() {
    const response = await fetchAPI('reklamationen');
    allReklamationen = response.data || response;  // Handle both formats
    renderTable(allReklamationen);
}
```

### 4.4 Fallback-Daten

Das Dashboard enthält eingebettete Fallback-Daten, falls die API nicht erreichbar ist.

---

## Schritt 5: Deployment

### 5.1 Workflow in n8n importieren

1. n8n öffnen: https://n8n.schneider-kabelsatzbau.de
2. Menu → Import from File
3. `RMS-2025-Dashboard-API-Standalone.json` importieren
4. **Workflow aktivieren** (Toggle oben rechts!)

### 5.2 Dashboard deployen

```bash
# Dashboard in Webroot kopieren
cp /mnt/HC_Volume_104189729/osp/rms/2025/dashboard/index.html /var/www/html/rms/2025/
```

### 5.3 Testen

```bash
# API testen
curl https://osp.schneider-kabelsatzbau.de/api/rms2025/kpis
curl https://osp.schneider-kabelsatzbau.de/api/rms2025/reklamationen
curl https://osp.schneider-kabelsatzbau.de/api/rms2025/charts

# Dashboard im Browser
https://osp.schneider-kabelsatzbau.de/rms/2025/
```

---

## Anpassung für NZA 2025

### Unterschiede zu RMS

| Aspekt | RMS | NZA |
|--------|-----|-----|
| ID-Format | QA-25XXX | NZA-25-XXXX |
| Typen | Kunde, Lieferant | Nacharbeit, Neufertigung, Ausschuss |
| Felder | Absender, Artikel, Fehler | Verursacher, KST, Prozesse, Kosten |
| KPIs | Abschlussquote, NZA-Kosten | Gesamtkosten, Kosten/KST, Kosten/Typ |
| SharePoint | /sites/RMS/...2025/ | /sites/NZA_NEU/...2025/ |

### Zu ändernde Elemente

1. **Webhook-Paths:** `nza2025/kpis`, `nza2025/prozesse`, `nza2025/charts`
2. **Nginx-Locations:** `/api/nza2025/...`, `/nza/2025/`
3. **SharePoint-URL:** `https://rainerschneiderkabelsatz.sharepoint.com/sites/NZA_NEU/...`
4. **KPI-Cards:** Anpassen an NZA-Metriken (Kosten, Verursacher, etc.)
5. **Tabellen-Spalten:** Verursacher, KST, Typ, Kosten statt Absender, Artikel, Formular
6. **Charts:** Kosten pro Monat, Kosten pro KST, Top-Verursacher

### NZA-spezifische Felder

```javascript
{
  id: 1,
  nza_id: 'NZA-25-0001',
  typ: 'Nacharbeit',           // Nacharbeit, Neufertigung, Ausschuss
  artikel: '123456',
  verursacher: 'MK',           // MA-Kürzel
  kst: '2000',                 // Kostenstelle
  datum: '2025-01-15',
  beschreibung: 'Fehlertext',
  kosten_prozesse: 45.50,
  kosten_material: 12.00,
  kosten_gesamt: 57.50,
  ordner: 'NZA-25-0001',
  dateien: ['Foto1.jpg', 'NZA-25-0001.xlsx']
}
```

---

## Dateien

```
/mnt/HC_Volume_104189729/osp/rms/2025/
├── dashboard/
│   └── index.html                              # Dashboard HTML
├── workflows/
│   ├── RMS-2025-Dashboard-API-Standalone.json  # n8n Workflow
│   ├── RMS-2025-Setup-Liste.json               # (nicht verwendet)
│   └── README.md                               # Deployment-Anleitung
├── docs/
│   └── RMS_2025_Archiv_Dashboard_Anleitung.md  # Diese Datei
└── QA-25XXX/                                   # Reklamations-Ordner (27x)

/var/www/html/rms/2025/
└── index.html                                  # Deployed Dashboard

/etc/nginx/sites-available/osp                  # Nginx-Konfiguration
```

---

## Bekannte Einschränkungen

1. **Keine iframe-Vorschau:** SharePoint blockiert Embedding von externen Domains (CSP: frame-ancestors)
2. **Statische Daten:** Änderungen erfordern Workflow-Update und Re-Import
3. **Keine Authentifizierung:** Dashboard ist öffentlich zugänglich

---

## Checkliste für neue Archiv-Dashboards

- [ ] Daten aus SharePoint/System exportieren
- [ ] KPIs berechnen
- [ ] Chart-Daten aggregieren
- [ ] n8n Workflow mit embedded Data erstellen
- [ ] Workflow in n8n importieren und aktivieren
- [ ] Nginx-Locations hinzufügen
- [ ] Nginx neu laden
- [ ] Dashboard HTML anpassen (Titel, Felder, SharePoint-URL)
- [ ] Dashboard deployen
- [ ] API-Endpoints testen
- [ ] Dashboard im Browser testen
- [ ] Datei-Links zu SharePoint testen

---

**Erstellt:** 02.02.2026
**System:** OSP | RMS | Reklamationsmanagementsystem
**Autor:** Andreas Löhr | Qualitätsmanager
