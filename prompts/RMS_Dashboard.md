# Claude Code Prompt: RMS Dashboard (Phase 1d-1e)

**Datum:** 2026-01-28 (Morgen)  
**Projekt:** RMS Dashboard, Detail-View, KPIs, KST-Filter, Charts  
**Verantwortlich:** AL (QM & KI-Manager)

---

## 📊 KONTEXT

### Was wurde bereits erledigt?

| Phase | Beschreibung | Status |
|-------|--------------|--------|
| Phase 1a | SharePoint Listen (5 Listen) | ✅ |
| Phase 1b | Formular-Konvertierung (4 Formulare) | ✅ |
| Phase 1c | n8n Workflows (6 Workflows) | ✅ |
| Phase 3 | PDF-Generierung (F-QM-02) | ✅ |
| Phase 5 | Schriftverkehr-Einträge | ✅ |

### Offene Aufgaben (heute zu implementieren)

| Aufgabe | Beschreibung | Priorität |
|---------|--------------|-----------|
| **RMS Dashboard** | Hauptansicht mit KPIs und Tabelle | 🔴 HOCH |
| **RMS Detail-View** | Einzelansicht einer Reklamation | 🔴 HOCH |
| **KPI-Cards** | Offene, Kritische, Überfällige, Ø-Tage | 🔴 HOCH |
| **KST-Filter** | Sichtbarkeit nach Kostenstelle | 🟡 MITTEL |
| **Charts** | Trend-Charts, Typ-Verteilung | 🟡 MITTEL |

---

## 🔧 UMGEBUNG

### Server-Zugang

```bash
# Hetzner Server
IP: 46.224.102.30
User: root

# Umgebungsvariablen setzen
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMGFkYS1mMGU5NTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM4MDQxNDQxfQ.Hhqnbitgd-ak_iZruZy1Z_rdHJ75BtcYfv09RO05Rtg"
export N8N_BASE_URL="http://127.0.0.1:5678"
```

### Vorhandene Verzeichnisse

```
/mnt/HC_Volume_104189729/osp/rms/
├── dashboard/           # ← HIER ARBEITEN
│   ├── index.html       # Basis-Struktur vorhanden
│   ├── css/style.css    # Styling
│   └── js/app.js        # Platzhalter-Logik
├── docs/
├── formulare/
│   ├── f_qm_02_qualitaetsabweichung/
│   ├── f_qm_03_8d_report/
│   ├── f_qm_04_nza/
│   └── f_qm_14_korrekturmassnahmen/
└── frontend/            # Alternative für React (optional)
```

### Vorhandenes Dashboard (Basis)

Die Datei `/mnt/HC_Volume_104189729/osp/rms/dashboard/index.html` existiert bereits mit:
- ✅ KPI-Cards Struktur (4 Cards)
- ✅ Filter-Dropdowns (Typ, Status)
- ✅ Tabellen-Struktur (6 Spalten)
- ❌ Keine SharePoint-Anbindung
- ❌ Keine echten Daten
- ❌ Kein KST-Filter
- ❌ Keine Charts
- ❌ Keine Detail-View

---

## 🎯 AUFGABEN

### Aufgabe 1: Backend-API für Dashboard (n8n Webhook)

Erstelle einen n8n Workflow der als API für das Dashboard dient:

**Workflow: RMS-Dashboard-API**

```
Trigger: Webhook (GET /webhook/rms/dashboard)
    │
    ├─► Endpoint: /kpis
    │   └─► SharePoint: Reklamationen zählen
    │       - Offene (Status != Abgeschlossen)
    │       - Kritische (Priorität = kritisch)
    │       - Überfällige (Zieldatum < heute)
    │       - Durchschnitt berechnen
    │
    ├─► Endpoint: /reklamationen
    │   └─► SharePoint: Alle Reklamationen laden
    │       - Filter: Typ, Status, KST (Query-Parameter)
    │       - Sortierung: Datum DESC
    │       - Limit: 100
    │
    ├─► Endpoint: /reklamation/{id}
    │   └─► SharePoint: Einzelne Reklamation + Maßnahmen + Schriftverkehr
    │
    └─► Endpoint: /charts
        └─► SharePoint: Aggregierte Daten für Charts
            - Reklamationen pro Monat
            - Verteilung nach Typ
            - Verteilung nach KST
```

**n8n Workflow erstellen:**

```bash
# Neuen Workflow erstellen via API
curl -X POST "$N8N_BASE_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RMS-Dashboard-API",
    "nodes": [...],
    "connections": {...},
    "active": true,
    "settings": {}
  }'
```

### Aufgabe 2: Dashboard Frontend erweitern

**Datei:** `/mnt/HC_Volume_104189729/osp/rms/dashboard/index.html`

Erweitere das vorhandene Dashboard um:

#### 2.1 KST-Filter hinzufügen

```html
<!-- Nach den bestehenden Filtern -->
<select id="filter-kst">
    <option value="">Alle Kostenstellen</option>
    <option value="F1">F1 - Fertigung 1</option>
    <option value="F2">F2 - Fertigung 2</option>
    <option value="F3">F3 - Fertigung 3</option>
    <option value="QM">QM - Qualitätsmanagement</option>
    <option value="EK">EK - Einkauf</option>
    <option value="VT">VT - Vertrieb</option>
</select>
```

#### 2.2 Chart-Container hinzufügen

```html
<!-- Nach der Tabelle -->
<section class="charts-section">
    <div class="chart-container">
        <h3>Reklamationen pro Monat</h3>
        <canvas id="chart-trend"></canvas>
    </div>
    <div class="chart-container">
        <h3>Verteilung nach Typ</h3>
        <canvas id="chart-typ"></canvas>
    </div>
    <div class="chart-container">
        <h3>Verteilung nach KST</h3>
        <canvas id="chart-kst"></canvas>
    </div>
</section>
```

#### 2.3 Detail-View Modal hinzufügen

```html
<!-- Modal für Detail-Ansicht -->
<div id="detail-modal" class="modal" style="display: none;">
    <div class="modal-content">
        <span class="close-btn">&times;</span>
        <h2 id="detail-qa-id">QA-XXXXX</h2>
        
        <div class="detail-section">
            <h3>Stammdaten</h3>
            <table id="detail-stammdaten"></table>
        </div>
        
        <div class="detail-section">
            <h3>Beschreibung</h3>
            <p id="detail-beschreibung"></p>
        </div>
        
        <div class="detail-section">
            <h3>Maßnahmen</h3>
            <table id="detail-massnahmen"></table>
        </div>
        
        <div class="detail-section">
            <h3>Schriftverkehr</h3>
            <table id="detail-schriftverkehr"></table>
        </div>
        
        <div class="detail-actions">
            <button onclick="openInSharePoint()">In SharePoint öffnen</button>
            <button onclick="generatePDF()">PDF erstellen</button>
        </div>
    </div>
</div>
```

### Aufgabe 3: JavaScript-Logik (app.js)

**Datei:** `/mnt/HC_Volume_104189729/osp/rms/dashboard/js/app.js`

```javascript
// RMS Dashboard - Schneider Kabelsatzbau
// SharePoint-Integration via n8n API

const API_BASE = 'https://n8n.schneider-kabelsatzbau.de/webhook/rms';

// ============================================
// KONFIGURATION
// ============================================

const CONFIG = {
    refreshInterval: 60000,  // 1 Minute
    dateFormat: 'de-DE',
    priorityColors: {
        kritisch: '#dc3545',
        hoch: '#fd7e14',
        mittel: '#ffc107',
        niedrig: '#28a745'
    },
    statusColors: {
        'Neu': '#17a2b8',
        'In Bearbeitung': '#ffc107',
        'Maßnahmen': '#6f42c1',
        'Abgeschlossen': '#28a745'
    }
};

// ============================================
// API FUNKTIONEN
// ============================================

async function fetchKPIs() {
    try {
        const response = await fetch(`${API_BASE}/kpis`);
        if (!response.ok) throw new Error('KPI-Abruf fehlgeschlagen');
        return await response.json();
    } catch (error) {
        console.error('Fehler beim KPI-Abruf:', error);
        return null;
    }
}

async function fetchReklamationen(filters = {}) {
    try {
        const params = new URLSearchParams();
        if (filters.typ) params.append('typ', filters.typ);
        if (filters.status) params.append('status', filters.status);
        if (filters.kst) params.append('kst', filters.kst);
        
        const url = `${API_BASE}/reklamationen${params.toString() ? '?' + params : ''}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error('Reklamationen-Abruf fehlgeschlagen');
        return await response.json();
    } catch (error) {
        console.error('Fehler beim Reklamationen-Abruf:', error);
        return [];
    }
}

async function fetchReklamationDetail(id) {
    try {
        const response = await fetch(`${API_BASE}/reklamation/${id}`);
        if (!response.ok) throw new Error('Detail-Abruf fehlgeschlagen');
        return await response.json();
    } catch (error) {
        console.error('Fehler beim Detail-Abruf:', error);
        return null;
    }
}

async function fetchChartData() {
    try {
        const response = await fetch(`${API_BASE}/charts`);
        if (!response.ok) throw new Error('Chart-Daten-Abruf fehlgeschlagen');
        return await response.json();
    } catch (error) {
        console.error('Fehler beim Chart-Daten-Abruf:', error);
        return null;
    }
}

// ============================================
// UI FUNKTIONEN
// ============================================

function updateKPIs(data) {
    if (!data) return;
    
    document.getElementById('kpi-offen').textContent = data.offen || 0;
    document.getElementById('kpi-kritisch').textContent = data.kritisch || 0;
    document.getElementById('kpi-ueberfaellig').textContent = data.ueberfaellig || 0;
    document.getElementById('kpi-durchschnitt').textContent = 
        (data.durchschnitt || 0).toFixed(1) + ' Tage';
    
    // Farbliche Hervorhebung bei kritischen Werten
    const kritischEl = document.getElementById('kpi-kritisch').parentElement;
    if (data.kritisch > 0) {
        kritischEl.classList.add('pulse');
    }
}

function updateTable(reklamationen) {
    const tbody = document.querySelector('#reklamationen-table tbody');
    
    if (!reklamationen || reklamationen.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">Keine Reklamationen gefunden</td></tr>';
        return;
    }
    
    tbody.innerHTML = reklamationen.map(r => `
        <tr onclick="showDetail('${r.id}')" style="cursor: pointer;">
            <td><strong>${r.QA_ID || '--'}</strong></td>
            <td><span class="badge badge-${r.Rekla_Typ?.toLowerCase()}">${r.Rekla_Typ || '--'}</span></td>
            <td>${r.Title || '--'}</td>
            <td><span class="status status-${r.Rekla_Status?.replace(/\s/g, '-')}">${r.Rekla_Status || '--'}</span></td>
            <td><span class="priority priority-${r.Prioritaet?.toLowerCase()}">${r.Prioritaet || '--'}</span></td>
            <td>${formatDate(r.Erfassungsdatum)}</td>
        </tr>
    `).join('');
}

function formatDate(dateStr) {
    if (!dateStr) return '--';
    const date = new Date(dateStr);
    return date.toLocaleDateString(CONFIG.dateFormat);
}

// ============================================
// DETAIL-VIEW
// ============================================

async function showDetail(id) {
    const data = await fetchReklamationDetail(id);
    if (!data) {
        alert('Fehler beim Laden der Details');
        return;
    }
    
    // Modal befüllen
    document.getElementById('detail-qa-id').textContent = data.QA_ID || 'Unbekannt';
    
    // Stammdaten
    document.getElementById('detail-stammdaten').innerHTML = `
        <tr><td>Typ:</td><td>${data.Rekla_Typ || '--'}</td></tr>
        <tr><td>Status:</td><td>${data.Rekla_Status || '--'}</td></tr>
        <tr><td>Priorität:</td><td>${data.Prioritaet || '--'}</td></tr>
        <tr><td>KST:</td><td>${data.KST || '--'}</td></tr>
        <tr><td>Erfasst:</td><td>${formatDate(data.Erfassungsdatum)}</td></tr>
        <tr><td>Zieldatum:</td><td>${formatDate(data.Zieldatum)}</td></tr>
        <tr><td>Verantwortlich:</td><td>${data.Verantwortlich || '--'}</td></tr>
    `;
    
    // Beschreibung
    document.getElementById('detail-beschreibung').textContent = 
        data.Beschreibung || 'Keine Beschreibung vorhanden';
    
    // Maßnahmen (falls vorhanden)
    if (data.massnahmen && data.massnahmen.length > 0) {
        document.getElementById('detail-massnahmen').innerHTML = 
            '<tr><th>Maßnahme</th><th>Termin</th><th>Status</th></tr>' +
            data.massnahmen.map(m => `
                <tr>
                    <td>${m.Title || '--'}</td>
                    <td>${formatDate(m.Termin)}</td>
                    <td>${m.Status || '--'}</td>
                </tr>
            `).join('');
    } else {
        document.getElementById('detail-massnahmen').innerHTML = 
            '<tr><td colspan="3">Keine Maßnahmen erfasst</td></tr>';
    }
    
    // Schriftverkehr (falls vorhanden)
    if (data.schriftverkehr && data.schriftverkehr.length > 0) {
        document.getElementById('detail-schriftverkehr').innerHTML = 
            '<tr><th>Datum</th><th>Typ</th><th>Betreff</th></tr>' +
            data.schriftverkehr.map(s => `
                <tr>
                    <td>${formatDate(s.Datum)}</td>
                    <td>${s.Typ || '--'}</td>
                    <td>${s.Betreff || '--'}</td>
                </tr>
            `).join('');
    } else {
        document.getElementById('detail-schriftverkehr').innerHTML = 
            '<tr><td colspan="3">Kein Schriftverkehr erfasst</td></tr>';
    }
    
    // Modal anzeigen
    document.getElementById('detail-modal').style.display = 'block';
    
    // Speichere aktuelle ID für Actions
    window.currentReklamationId = id;
    window.currentReklamationData = data;
}

function closeDetail() {
    document.getElementById('detail-modal').style.display = 'none';
}

function openInSharePoint() {
    const data = window.currentReklamationData;
    if (data && data.sharePointUrl) {
        window.open(data.sharePointUrl, '_blank');
    } else {
        // Fallback: SharePoint-Site öffnen
        window.open('https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS', '_blank');
    }
}

async function generatePDF() {
    const data = window.currentReklamationData;
    if (!data) return;
    
    try {
        const response = await fetch('http://localhost:5001/generate-pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                abweichungs_nr: data.QA_ID,
                datum: new Date().toISOString().split('T')[0],
                lieferant_firma: data.Absender || 'Unbekannt',
                artikel_bezeichnung: data.Title,
                beschreibung: data.Beschreibung || 'Keine Beschreibung',
                massnahmen: ['untersuchung_abstellen'],
                ersteller: 'Dashboard'
            })
        });
        
        const result = await response.json();
        if (result.success) {
            alert(`PDF erstellt: ${result.filename}`);
        } else {
            alert('PDF-Erstellung fehlgeschlagen');
        }
    } catch (error) {
        console.error('PDF-Fehler:', error);
        alert('PDF-Erstellung fehlgeschlagen');
    }
}

// ============================================
// CHARTS (Chart.js)
// ============================================

let chartTrend, chartTyp, chartKST;

async function initCharts() {
    const data = await fetchChartData();
    if (!data) return;
    
    // Trend-Chart (Linie)
    const ctxTrend = document.getElementById('chart-trend')?.getContext('2d');
    if (ctxTrend) {
        chartTrend = new Chart(ctxTrend, {
            type: 'line',
            data: {
                labels: data.trend?.labels || [],
                datasets: [{
                    label: 'Reklamationen',
                    data: data.trend?.values || [],
                    borderColor: '#003366',
                    backgroundColor: 'rgba(0, 51, 102, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });
    }
    
    // Typ-Chart (Donut)
    const ctxTyp = document.getElementById('chart-typ')?.getContext('2d');
    if (ctxTyp) {
        chartTyp = new Chart(ctxTyp, {
            type: 'doughnut',
            data: {
                labels: ['Kunde', 'Lieferant', 'Intern'],
                datasets: [{
                    data: data.typ || [0, 0, 0],
                    backgroundColor: ['#003366', '#fd7e14', '#28a745']
                }]
            },
            options: { responsive: true }
        });
    }
    
    // KST-Chart (Bar)
    const ctxKST = document.getElementById('chart-kst')?.getContext('2d');
    if (ctxKST) {
        chartKST = new Chart(ctxKST, {
            type: 'bar',
            data: {
                labels: data.kst?.labels || [],
                datasets: [{
                    label: 'Reklamationen',
                    data: data.kst?.values || [],
                    backgroundColor: '#003366'
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });
    }
}

// ============================================
// FILTER
// ============================================

function applyFilters() {
    const filters = {
        typ: document.getElementById('filter-typ')?.value,
        status: document.getElementById('filter-status')?.value,
        kst: document.getElementById('filter-kst')?.value
    };
    
    loadData(filters);
}

// ============================================
// INITIALISIERUNG
// ============================================

async function loadData(filters = {}) {
    // KPIs laden
    const kpis = await fetchKPIs();
    updateKPIs(kpis);
    
    // Tabelle laden
    const reklamationen = await fetchReklamationen(filters);
    updateTable(reklamationen);
}

document.addEventListener('DOMContentLoaded', async function() {
    console.log('RMS Dashboard wird initialisiert...');
    
    // Event-Listener für Filter
    document.getElementById('filter-typ')?.addEventListener('change', applyFilters);
    document.getElementById('filter-status')?.addEventListener('change', applyFilters);
    document.getElementById('filter-kst')?.addEventListener('change', applyFilters);
    
    // Modal schließen
    document.querySelector('.close-btn')?.addEventListener('click', closeDetail);
    window.onclick = function(event) {
        const modal = document.getElementById('detail-modal');
        if (event.target === modal) {
            closeDetail();
        }
    };
    
    // Daten laden
    await loadData();
    
    // Charts initialisieren (wenn Chart.js geladen)
    if (typeof Chart !== 'undefined') {
        await initCharts();
    }
    
    // Auto-Refresh
    setInterval(() => loadData(), CONFIG.refreshInterval);
    
    console.log('RMS Dashboard bereit');
});
```

### Aufgabe 4: CSS-Styling erweitern

**Datei:** `/mnt/HC_Volume_104189729/osp/rms/dashboard/css/style.css`

```css
/* RMS Dashboard - Schneider Kabelsatzbau
   Corporate Design: Blau #003366 */

:root {
    --primary: #003366;
    --primary-light: #004080;
    --danger: #dc3545;
    --warning: #fd7e14;
    --success: #28a745;
    --info: #17a2b8;
    --gray: #6c757d;
    --light: #f8f9fa;
    --white: #ffffff;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: var(--light);
    color: #333;
    line-height: 1.6;
}

/* Header */
header {
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    color: var(--white);
    padding: 20px;
    text-align: center;
}

header h1 {
    font-size: 1.8rem;
    margin-bottom: 5px;
}

header p {
    opacity: 0.8;
    font-size: 0.9rem;
}

/* Main */
main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

/* KPI Cards */
.kpi-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.kpi-card {
    background: var(--white);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.kpi-card h3 {
    color: var(--gray);
    font-size: 0.9rem;
    font-weight: normal;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--primary);
}

.kpi-critical .kpi-value {
    color: var(--danger);
}

.kpi-warning .kpi-value {
    color: var(--warning);
}

.kpi-card.pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    50% { box-shadow: 0 2px 20px rgba(220, 53, 69, 0.4); }
}

/* Filter Section */
.filter-section {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.filter-section select {
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 0.95rem;
    min-width: 150px;
    background: var(--white);
    cursor: pointer;
}

.filter-section select:focus {
    outline: none;
    border-color: var(--primary);
}

/* Table Section */
.table-section {
    background: var(--white);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 30px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th {
    background: var(--primary);
    color: var(--white);
    padding: 15px;
    text-align: left;
    font-weight: 500;
}

td {
    padding: 12px 15px;
    border-bottom: 1px solid #eee;
}

tbody tr:hover {
    background: #f5f5f5;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.badge-kunde { background: #e3f2fd; color: #1565c0; }
.badge-lieferant { background: #fff3e0; color: #e65100; }
.badge-intern { background: #e8f5e9; color: #2e7d32; }

/* Status */
.status {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 5px;
    font-size: 0.8rem;
}

.status-Neu { background: var(--info); color: white; }
.status-In-Bearbeitung { background: var(--warning); color: white; }
.status-Maßnahmen { background: #6f42c1; color: white; }
.status-Abgeschlossen { background: var(--success); color: white; }

/* Priority */
.priority {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 5px;
    font-size: 0.8rem;
    font-weight: bold;
}

.priority-kritisch { background: var(--danger); color: white; }
.priority-hoch { background: var(--warning); color: white; }
.priority-mittel { background: #ffc107; color: #333; }
.priority-niedrig { background: var(--success); color: white; }

/* Charts Section */
.charts-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.chart-container {
    background: var(--white);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chart-container h3 {
    color: var(--primary);
    margin-bottom: 15px;
    font-size: 1rem;
}

/* Modal */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: var(--white);
    border-radius: 10px;
    max-width: 800px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    padding: 30px;
    position: relative;
}

.close-btn {
    position: absolute;
    top: 15px;
    right: 20px;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--gray);
}

.close-btn:hover {
    color: var(--danger);
}

.modal-content h2 {
    color: var(--primary);
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--primary);
}

.detail-section {
    margin-bottom: 25px;
}

.detail-section h3 {
    color: var(--primary);
    font-size: 1rem;
    margin-bottom: 10px;
}

.detail-section table {
    width: 100%;
}

.detail-section td {
    padding: 8px;
    border-bottom: 1px solid #eee;
}

.detail-section td:first-child {
    font-weight: 500;
    width: 150px;
    color: var(--gray);
}

.detail-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}

.detail-actions button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.95rem;
    transition: background 0.2s;
}

.detail-actions button:first-child {
    background: var(--primary);
    color: white;
}

.detail-actions button:first-child:hover {
    background: var(--primary-light);
}

.detail-actions button:last-child {
    background: var(--gray);
    color: white;
}

/* Footer */
footer {
    text-align: center;
    padding: 20px;
    color: var(--gray);
    font-size: 0.85rem;
}

/* Responsive */
@media (max-width: 768px) {
    .kpi-cards {
        grid-template-columns: 1fr 1fr;
    }
    
    .filter-section {
        flex-direction: column;
    }
    
    .filter-section select {
        width: 100%;
    }
    
    .charts-section {
        grid-template-columns: 1fr;
    }
}
```

### Aufgabe 5: n8n Dashboard-API Workflow

Erstelle das Script `/opt/osp/scripts/create_dashboard_api.py`:

```python
#!/usr/bin/env python3
"""
Erstellt den RMS-Dashboard-API Workflow in n8n
"""

import json
import urllib.request
import os

N8N_BASE_URL = os.environ.get('N8N_BASE_URL', 'http://127.0.0.1:5678')
N8N_API_KEY = os.environ.get('N8N_API_KEY', '')

SITE_ID = "rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"
REKLAMATIONEN_LIST_ID = "e9b1d926-085a-4435-a012-114ca9ba59a8"
MASSNAHMEN_LIST_ID = "3768f2d8-878c-4a5f-bd52-7486fe93289d"
SCHRIFTVERKEHR_LIST_ID = "741c6ae8-88bb-406b-bf85-2e11192a528f"
KPI_LIST_ID = "f66e805e-8315-4714-a18e-5c59a05d631f"

workflow = {
    "name": "RMS-Dashboard-API",
    "nodes": [
        {
            "parameters": {
                "httpMethod": "GET",
                "path": "rms/dashboard",
                "responseMode": "responseNode",
                "options": {}
            },
            "id": "webhook-1",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [250, 300],
            "webhookId": "rms-dashboard"
        },
        {
            "parameters": {
                "conditions": {
                    "options": {
                        "caseSensitive": True,
                        "leftValue": "",
                        "typeValidation": "strict"
                    },
                    "conditions": [
                        {
                            "id": "kpis",
                            "leftValue": "={{ $json.query.endpoint }}",
                            "rightValue": "kpis",
                            "operator": {
                                "type": "string",
                                "operation": "equals"
                            }
                        }
                    ],
                    "combinator": "or"
                },
                "options": {}
            },
            "id": "switch-1",
            "name": "Route Endpoint",
            "type": "n8n-nodes-base.switch",
            "typeVersion": 3,
            "position": [450, 300]
        },
        # Weitere Nodes für KPIs, Reklamationen, etc.
        # ... (hier würden die HTTP Request Nodes für SharePoint kommen)
    ],
    "connections": {
        "Webhook": {
            "main": [[{"node": "Route Endpoint", "type": "main", "index": 0}]]
        }
    },
    "active": True,
    "settings": {
        "executionOrder": "v1"
    }
}

def create_workflow():
    url = f"{N8N_BASE_URL}/api/v1/workflows"
    data = json.dumps(workflow).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-N8N-API-KEY', N8N_API_KEY)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Workflow erstellt: {result.get('id')}")
            return result
    except urllib.error.HTTPError as e:
        print(f"❌ Fehler: {e.code} - {e.read().decode('utf-8')}")
        return None

if __name__ == "__main__":
    create_workflow()
```

---

## 📋 ZUSAMMENFASSUNG DER AUFGABEN

| # | Aufgabe | Beschreibung | Prio |
|---|---------|--------------|------|
| 1 | **n8n Dashboard-API** | Webhook-Workflow für API-Endpoints | 🔴 |
| 2 | **index.html erweitern** | KST-Filter, Charts, Modal | 🔴 |
| 3 | **app.js neu schreiben** | SharePoint-Anbindung via API | 🔴 |
| 4 | **style.css erweitern** | Modal, Charts, Responsive | 🟡 |
| 5 | **Deployment** | Dashboard auf Hetzner deployen | 🟡 |

---

## ⚡ EMPFOHLENE REIHENFOLGE

1. **Erst n8n Dashboard-API erstellen** (sonst keine Daten im Frontend)
2. **Dann Frontend erweitern** (HTML, JS, CSS)
3. **Deployment & Test**

---

## 🔧 DEPLOYMENT

Nach Fertigstellung das Dashboard deployen:

```bash
# Dashboard nach Nginx kopieren
cp -r /mnt/HC_Volume_104189729/osp/rms/dashboard/* /var/www/html/rms/

# Oder als Docker Container
# (falls noch kein Nginx läuft)

# Nginx Config erstellen
cat > /etc/nginx/sites-available/rms << 'EOF'
server {
    listen 80;
    server_name rms.schneider-kabelsatzbau.de;
    
    root /var/www/html/rms;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location /api/ {
        proxy_pass http://localhost:5678/webhook/rms/;
        proxy_set_header Host $host;
    }
}
EOF

# Aktivieren
ln -sf /etc/nginx/sites-available/rms /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

---

## 📚 REFERENZEN

| Resource | Wert |
|----------|------|
| n8n API | http://127.0.0.1:5678 |
| PDF Generator | http://localhost:5001 |
| Dashboard Pfad | /mnt/HC_Volume_104189729/osp/rms/dashboard/ |
| SharePoint Site ID | rainerschneiderkabelsatz.sharepoint.com,... |
| Reklamationen Liste | e9b1d926-085a-4435-a012-114ca9ba59a8 |
| Maßnahmen Liste | 3768f2d8-878c-4a5f-bd52-7486fe93289d |
| Schriftverkehr Liste | 741c6ae8-88bb-406b-bf85-2e11192a528f |
| KPIs Liste | f66e805e-8315-4714-a18e-5c59a05d631f |

---

*Erstellt: 2026-01-27 | Für: 2026-01-28 | Teil des OSP-Systems*
