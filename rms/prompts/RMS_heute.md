# RMS ROADMAP - Heute komplett umsetzen

**Stand:** 2026-01-28, 10:30 Uhr  
**Erstellt für:** AL (QM & KI-Manager)  
**Ziel:** Alle Features HEUTE fertigstellen

---

## 📊 AKTUELLER STATUS

| Komponente | Status |
|------------|--------|
| Dashboard Live | ✅ osp.schneider-kabelsatzbau.de/rms/ |
| KPIs | ✅ 19 offen, 2 kritisch |
| Charts | ✅ Trend, Typ, KST |
| Detail-View | ⚠️ Ohne Maßnahmen/Schriftverkehr |

**KST-Thema:** Manuelle Zuordnung ist OK → Niedrige Priorität

---

## 🎯 HEUTIGE AUFGABEN (in Reihenfolge)

### BLOCK 1: Detail-API komplett (2-3h)

| # | Aufgabe | Beschreibung |
|---|---------|--------------|
| 1.1 | n8n Workflow "RMS-Detail-API" | Reklamation + Maßnahmen + Schriftverkehr laden |
| 1.2 | Nginx Proxy konfigurieren | /api/rms/detail Route |
| 1.3 | Frontend Detail-Modal | Maßnahmen-Tabelle, Schriftverkehr-Tabelle |

### BLOCK 2: Dashboard-Features (2-3h)

| # | Aufgabe | Beschreibung |
|---|---------|--------------|
| 2.1 | KST-Filter funktionsfähig | Dropdown filtert Tabelle |
| 2.2 | Sortierung Tabelle | Klick auf Spaltenheader |
| 2.3 | Suchfeld | Freitext über alle Felder |
| 2.4 | Export CSV | Button für Download |
| 2.5 | Refresh-Button | Manuelle Aktualisierung |
| 2.6 | Loading-States | Spinner während API-Calls |

### BLOCK 3: Charts erweitern (1-2h)

| # | Aufgabe | Beschreibung |
|---|---------|--------------|
| 3.1 | CI-Farben konsistent | Schneider-Blau #003366 |
| 3.2 | Neuer Chart: Status-Verteilung | Pie-Chart |
| 3.3 | Neuer Chart: Priorität | Bar-Chart |
| 3.4 | Tooltips verbessern | Mehr Details beim Hover |

### BLOCK 4: Maßnahmen-Management (2-3h)

| # | Aufgabe | Beschreibung |
|---|---------|--------------|
| 4.1 | Maßnahme erstellen | Button + Modal im Detail-View |
| 4.2 | Maßnahme bearbeiten | Inline-Edit oder Modal |
| 4.3 | n8n Workflow "RMS-Massnahmen-API" | CRUD für Maßnahmen |
| 4.4 | Termin-Alarm Workflow | Überfällige → Teams-Nachricht |

---

## 📋 CLAUDE CODE PROMPT (KOMPLETT)

```markdown
# Claude Code Prompt: RMS Dashboard - Alle Features HEUTE

## KONTEXT

Dashboard läuft: https://osp.schneider-kabelsatzbau.de/rms/
19 Reklamationen in SharePoint, KPIs und Charts funktionieren.
Heute alle verbleibenden Features implementieren.

## UMGEBUNG

```bash
# Server
IP: 46.224.102.30
User: root

# API
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMGFkYS1mMGU5NTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM4MDQxNDQxfQ.Hhqnbitgd-ak_iZruZy1Z_rdHJ75BtcYfv09RO05Rtg"
export N8N_BASE_URL="http://127.0.0.1:5678"

# SharePoint
SITE_ID="rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"
REKLAMATIONEN_LIST="e9b1d926-085a-4435-a012-114ca9ba59a8"
MASSNAHMEN_LIST="3768f2d8-878c-4a5f-bd52-7486fe93289d"
SCHRIFTVERKEHR_LIST="741c6ae8-88bb-406b-bf85-2e11192a528f"
CREDENTIAL_ID="Fm3IuAbVYBYDIA4U"
```

## DATEIEN

- Dashboard: `/var/www/html/rms/`
- n8n Workflows: via API
- Nginx: `/etc/nginx/sites-available/osp`

---

## BLOCK 1: Detail-API (ZUERST)

### 1.1 n8n Workflow erstellen: RMS-Detail-API

Webhook: GET /webhook/rms-detail?id={itemId}

**Nodes:**

1. **Webhook Trigger**
   - Method: GET
   - Path: rms-detail
   - Response Mode: Last Node

2. **Reklamation laden** (HTTP Request)
   - Method: GET
   - URL: `https://graph.microsoft.com/v1.0/sites/${SITE_ID}/lists/${REKLAMATIONEN_LIST}/items/{{ $json.query.id }}?$expand=fields`
   - Authentication: OAuth2
   - Credential: Microsoft account

3. **Maßnahmen laden** (HTTP Request)
   - Method: GET
   - URL: `https://graph.microsoft.com/v1.0/sites/${SITE_ID}/lists/${MASSNAHMEN_LIST}/items?$expand=fields&$filter=fields/Rekla_IDLookupId eq {{ $json.query.id }}`
   - Headers: `Prefer: HonorNonIndexedQueriesWarningMayFailRandomly`
   - Authentication: OAuth2

4. **Schriftverkehr laden** (HTTP Request)
   - Method: GET
   - URL: `https://graph.microsoft.com/v1.0/sites/${SITE_ID}/lists/${SCHRIFTVERKEHR_LIST}/items?$expand=fields&$filter=fields/QA_IDLookupId eq {{ $json.query.id }}`
   - Headers: `Prefer: HonorNonIndexedQueriesWarningMayFailRandomly`
   - Authentication: OAuth2

5. **Merge Results** (Code Node)
```javascript
const rekla = $('Reklamation laden').item.json;
const massnahmen = $('Maßnahmen laden').item.json;
const schriftverkehr = $('Schriftverkehr laden').item.json;

return {
  reklamation: rekla.fields || rekla,
  massnahmen: massnahmen.value?.map(m => m.fields) || [],
  schriftverkehr: schriftverkehr.value?.map(s => s.fields) || [],
  sharePointUrl: `https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS/Lists/Reklamationen/DispForm.aspx?ID=${rekla.id}`
};
```

6. **Respond to Webhook**

### 1.2 Nginx Proxy erweitern

```bash
# In /etc/nginx/sites-available/osp hinzufügen:

location /api/rms/detail {
    proxy_pass http://127.0.0.1:5678/webhook/rms-detail;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}
```

### 1.3 Frontend Detail-Modal erweitern

In `/var/www/html/rms/js/app.js`:

```javascript
async function fetchReklamationDetail(id) {
    try {
        const response = await fetch(`/api/rms/detail?id=${id}`);
        if (!response.ok) throw new Error('Detail-Abruf fehlgeschlagen');
        return await response.json();
    } catch (error) {
        console.error('Fehler:', error);
        return null;
    }
}

async function showDetail(id) {
    const data = await fetchReklamationDetail(id);
    if (!data) {
        alert('Fehler beim Laden');
        return;
    }
    
    const r = data.reklamation;
    
    // Header
    document.getElementById('detail-qa-id').textContent = r.QA_ID || 'Unbekannt';
    
    // Stammdaten
    document.getElementById('detail-stammdaten').innerHTML = `
        <tr><td>Typ:</td><td>${r.Rekla_Typ || '--'}</td></tr>
        <tr><td>Status:</td><td>${r.Rekla_Status || '--'}</td></tr>
        <tr><td>Priorität:</td><td>${r.Prioritaet || '--'}</td></tr>
        <tr><td>KST:</td><td>${r.KST || '--'}</td></tr>
        <tr><td>Erfasst:</td><td>${formatDate(r.Erfassungsdatum)}</td></tr>
        <tr><td>Zieldatum:</td><td>${formatDate(r.Zieldatum)}</td></tr>
        <tr><td>Verantwortlich:</td><td>${r.Verantwortlich || '--'}</td></tr>
    `;
    
    // Beschreibung
    document.getElementById('detail-beschreibung').textContent = 
        r.Beschreibung || 'Keine Beschreibung';
    
    // Maßnahmen
    const massnahmenHtml = data.massnahmen.length > 0
        ? '<tr><th>Maßnahme</th><th>Typ</th><th>Termin</th><th>Status</th></tr>' +
          data.massnahmen.map(m => `
            <tr>
                <td>${m.Title || '--'}</td>
                <td>${m.Typ || '--'}</td>
                <td>${formatDate(m.Termin)}</td>
                <td><span class="status status-${m.Status?.replace(/\s/g,'-')}">${m.Status || '--'}</span></td>
            </tr>
          `).join('')
        : '<tr><td colspan="4">Keine Maßnahmen erfasst</td></tr>';
    document.getElementById('detail-massnahmen').innerHTML = massnahmenHtml;
    
    // Schriftverkehr
    const svHtml = data.schriftverkehr.length > 0
        ? '<tr><th>Datum</th><th>Typ</th><th>Betreff</th><th>Richtung</th></tr>' +
          data.schriftverkehr.map(s => `
            <tr>
                <td>${formatDate(s.Datum)}</td>
                <td>${s.Typ || '--'}</td>
                <td>${s.Betreff || s.Title || '--'}</td>
                <td>${s.Richtung || '--'}</td>
            </tr>
          `).join('')
        : '<tr><td colspan="4">Kein Schriftverkehr</td></tr>';
    document.getElementById('detail-schriftverkehr').innerHTML = svHtml;
    
    // SharePoint Link speichern
    window.currentSharePointUrl = data.sharePointUrl;
    window.currentReklamationId = id;
    window.currentReklamationData = data;
    
    // Modal anzeigen
    document.getElementById('detail-modal').style.display = 'block';
}
```

---

## BLOCK 2: Dashboard-Features

### 2.1-2.6 Alle Features in app.js

```javascript
// ============================================
// GLOBALE VARIABLEN
// ============================================

let allReklamationen = [];  // Cache für Filter/Suche/Sort
let currentSort = { field: 'Erfassungsdatum', dir: 'desc' };

// ============================================
// FILTER & SUCHE
// ============================================

function applyFilters() {
    let filtered = [...allReklamationen];
    
    // Typ-Filter
    const typ = document.getElementById('filter-typ')?.value;
    if (typ) filtered = filtered.filter(r => r.Rekla_Typ === typ);
    
    // Status-Filter
    const status = document.getElementById('filter-status')?.value;
    if (status) filtered = filtered.filter(r => r.Rekla_Status === status);
    
    // KST-Filter
    const kst = document.getElementById('filter-kst')?.value;
    if (kst) filtered = filtered.filter(r => r.KST === kst);
    
    // Suchfeld
    const search = document.getElementById('search-input')?.value?.toLowerCase();
    if (search) {
        filtered = filtered.filter(r => 
            (r.QA_ID || '').toLowerCase().includes(search) ||
            (r.Title || '').toLowerCase().includes(search) ||
            (r.Beschreibung || '').toLowerCase().includes(search) ||
            (r.Rekla_Typ || '').toLowerCase().includes(search)
        );
    }
    
    // Sortierung anwenden
    filtered = sortData(filtered);
    
    updateTable(filtered);
    updateFilteredCount(filtered.length, allReklamationen.length);
}

function sortData(data) {
    return data.sort((a, b) => {
        let valA = a[currentSort.field] || '';
        let valB = b[currentSort.field] || '';
        
        // Datum-Felder
        if (currentSort.field.includes('datum') || currentSort.field.includes('Datum')) {
            valA = new Date(valA || 0);
            valB = new Date(valB || 0);
        }
        
        if (currentSort.dir === 'asc') {
            return valA > valB ? 1 : -1;
        } else {
            return valA < valB ? 1 : -1;
        }
    });
}

function handleSort(field) {
    if (currentSort.field === field) {
        currentSort.dir = currentSort.dir === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.field = field;
        currentSort.dir = 'desc';
    }
    
    // Header-Icons aktualisieren
    document.querySelectorAll('th[data-sort]').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
        if (th.dataset.sort === field) {
            th.classList.add(currentSort.dir === 'asc' ? 'sort-asc' : 'sort-desc');
        }
    });
    
    applyFilters();
}

function updateFilteredCount(filtered, total) {
    const countEl = document.getElementById('filtered-count');
    if (countEl) {
        countEl.textContent = filtered === total 
            ? `${total} Einträge` 
            : `${filtered} von ${total} Einträgen`;
    }
}

// ============================================
// CSV EXPORT
// ============================================

function exportCSV() {
    const headers = ['QA-ID', 'Typ', 'Titel', 'Status', 'Priorität', 'KST', 'Erfasst', 'Zieldatum'];
    const rows = allReklamationen.map(r => [
        r.QA_ID || '',
        r.Rekla_Typ || '',
        (r.Title || '').replace(/[";]/g, ''),
        r.Rekla_Status || '',
        r.Prioritaet || '',
        r.KST || '',
        formatDate(r.Erfassungsdatum),
        formatDate(r.Zieldatum)
    ]);
    
    const csv = [headers.join(';'), ...rows.map(r => r.join(';'))].join('\n');
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `RMS_Export_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    
    URL.revokeObjectURL(url);
}

// ============================================
// REFRESH & LOADING
// ============================================

function showLoading(show = true) {
    const loader = document.getElementById('loading-overlay');
    if (loader) loader.style.display = show ? 'flex' : 'none';
}

async function refreshData() {
    showLoading(true);
    try {
        await loadData();
        await initCharts();
    } finally {
        showLoading(false);
    }
}

// ============================================
// INITIALISIERUNG ERWEITERN
// ============================================

document.addEventListener('DOMContentLoaded', async function() {
    // Filter Event-Listener
    ['filter-typ', 'filter-status', 'filter-kst'].forEach(id => {
        document.getElementById(id)?.addEventListener('change', applyFilters);
    });
    
    // Suchfeld mit Debounce
    const searchInput = document.getElementById('search-input');
    let searchTimeout;
    searchInput?.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(applyFilters, 300);
    });
    
    // Sortierung
    document.querySelectorAll('th[data-sort]').forEach(th => {
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => handleSort(th.dataset.sort));
    });
    
    // Export-Button
    document.getElementById('btn-export')?.addEventListener('click', exportCSV);
    
    // Refresh-Button
    document.getElementById('btn-refresh')?.addEventListener('click', refreshData);
    
    // Modal schließen
    document.querySelector('.close-btn')?.addEventListener('click', closeDetail);
    window.onclick = e => {
        if (e.target === document.getElementById('detail-modal')) closeDetail();
    };
    
    // Daten laden
    showLoading(true);
    await loadData();
    await initCharts();
    showLoading(false);
    
    // Auto-Refresh alle 60 Sekunden
    setInterval(() => loadData(), 60000);
});

// fetchReklamationen anpassen um Cache zu füllen
async function fetchReklamationen(filters = {}) {
    try {
        const response = await fetch('/api/rms/reklamationen');
        if (!response.ok) throw new Error('Fehler');
        const data = await response.json();
        
        // Transformation und Cache
        allReklamationen = (data.value || data).map(item => ({
            id: item.id,
            ...item.fields
        }));
        
        return allReklamationen;
    } catch (error) {
        console.error('Fehler:', error);
        return [];
    }
}
```

### HTML-Erweiterungen für index.html

```html
<!-- Loading Overlay (nach <body>) -->
<div id="loading-overlay" style="display:none;">
    <div class="spinner"></div>
</div>

<!-- Suchfeld und Buttons (in filter-section) -->
<section class="filter-section">
    <input type="text" id="search-input" placeholder="🔍 Suchen..." class="search-input">
    
    <select id="filter-typ">
        <option value="">Alle Typen</option>
        <option value="Intern">Intern</option>
        <option value="Kunde">Kunde</option>
        <option value="Lieferant">Lieferant</option>
    </select>
    
    <select id="filter-status">
        <option value="">Alle Status</option>
        <option value="Neu">Neu</option>
        <option value="In Bearbeitung">In Bearbeitung</option>
        <option value="Maßnahmen">Maßnahmen</option>
        <option value="Abgeschlossen">Abgeschlossen</option>
    </select>
    
    <select id="filter-kst">
        <option value="">Alle KST</option>
        <option value="1000">1000</option>
        <option value="2000">2000</option>
        <option value="3000">3000</option>
        <option value="Verwaltung">Verwaltung</option>
    </select>
    
    <button id="btn-refresh" class="btn btn-secondary" title="Aktualisieren">🔄</button>
    <button id="btn-export" class="btn btn-secondary" title="CSV Export">📥 Export</button>
    
    <span id="filtered-count" class="count-badge"></span>
</section>

<!-- Tabellen-Header mit Sortierung -->
<thead>
    <tr>
        <th data-sort="QA_ID">QA-ID ↕</th>
        <th data-sort="Rekla_Typ">Typ ↕</th>
        <th data-sort="Title">Titel ↕</th>
        <th data-sort="Rekla_Status">Status ↕</th>
        <th data-sort="Prioritaet">Priorität ↕</th>
        <th data-sort="Erfassungsdatum">Erstellt ↕</th>
    </tr>
</thead>
```

---

## BLOCK 3: Charts erweitern

### Neue Charts hinzufügen

```javascript
// In initCharts() erweitern:

async function initCharts() {
    const data = await fetchChartData();
    if (!data) return;
    
    const ciBlue = '#003366';
    const ciOrange = '#fd7e14';
    
    // Bestehendes: Trend, Typ, KST...
    
    // NEU: Status-Verteilung (Pie)
    const ctxStatus = document.getElementById('chart-status')?.getContext('2d');
    if (ctxStatus && data.status) {
        new Chart(ctxStatus, {
            type: 'pie',
            data: {
                labels: ['Neu', 'In Bearbeitung', 'Maßnahmen', 'Abgeschlossen'],
                datasets: [{
                    data: data.status || [0, 0, 0, 0],
                    backgroundColor: ['#17a2b8', '#ffc107', '#6f42c1', '#28a745']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        callbacks: {
                            label: ctx => `${ctx.label}: ${ctx.raw} (${Math.round(ctx.raw/ctx.dataset.data.reduce((a,b)=>a+b,0)*100)}%)`
                        }
                    }
                }
            }
        });
    }
    
    // NEU: Priorität-Verteilung (Bar horizontal)
    const ctxPrio = document.getElementById('chart-priority')?.getContext('2d');
    if (ctxPrio && data.priority) {
        new Chart(ctxPrio, {
            type: 'bar',
            data: {
                labels: ['Kritisch', 'Hoch', 'Mittel', 'Niedrig'],
                datasets: [{
                    data: data.priority || [0, 0, 0, 0],
                    backgroundColor: ['#dc3545', '#fd7e14', '#ffc107', '#28a745']
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });
    }
}
```

### n8n RMS-Charts Workflow erweitern

Status- und Prioritäts-Aggregation im Code-Node hinzufügen:

```javascript
// Bestehende Daten + neue Aggregationen
const items = $input.all();

// Status zählen
const statusCounts = { Neu: 0, 'In Bearbeitung': 0, Maßnahmen: 0, Abgeschlossen: 0 };
const priorityCounts = { kritisch: 0, hoch: 0, mittel: 0, niedrig: 0 };

items.forEach(item => {
    const status = item.json.fields?.Rekla_Status || 'Neu';
    const prio = item.json.fields?.Prioritaet || 'mittel';
    
    if (statusCounts[status] !== undefined) statusCounts[status]++;
    if (priorityCounts[prio] !== undefined) priorityCounts[prio]++;
});

return {
    // ... bestehende Daten (trend, typ, kst) ...
    status: [statusCounts.Neu, statusCounts['In Bearbeitung'], statusCounts.Maßnahmen, statusCounts.Abgeschlossen],
    priority: [priorityCounts.kritisch, priorityCounts.hoch, priorityCounts.mittel, priorityCounts.niedrig]
};
```

### HTML: Neue Chart-Container

```html
<section class="charts-section">
    <div class="chart-container">
        <h3>📈 Trend (6 Monate)</h3>
        <canvas id="chart-trend"></canvas>
    </div>
    <div class="chart-container">
        <h3>📊 Nach Typ</h3>
        <canvas id="chart-typ"></canvas>
    </div>
    <div class="chart-container">
        <h3>🏭 Nach KST</h3>
        <canvas id="chart-kst"></canvas>
    </div>
    <div class="chart-container">
        <h3>📋 Nach Status</h3>
        <canvas id="chart-status"></canvas>
    </div>
    <div class="chart-container">
        <h3>⚠️ Nach Priorität</h3>
        <canvas id="chart-priority"></canvas>
    </div>
</section>
```

---

## BLOCK 4: Maßnahmen-Management

### 4.1 n8n Workflow: RMS-Massnahmen-API

Webhook: POST/PUT/DELETE /webhook/rms-massnahmen

```javascript
// POST: Neue Maßnahme erstellen
// Body: { reklaId, title, typ, termin, verantwortlich }

// Node: HTTP Request
// Method: POST
// URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/lists/${MASSNAHMEN_LIST}/items
// Body:
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

### 4.2 Frontend: Maßnahme erstellen Modal

```javascript
// Button im Detail-Modal
function showAddMassnahmeModal() {
    const html = `
        <div class="modal" id="massnahme-modal">
            <div class="modal-content" style="max-width:500px;">
                <span class="close-btn" onclick="closeMassnahmeModal()">&times;</span>
                <h2>Neue Maßnahme</h2>
                <form id="massnahme-form">
                    <div class="form-group">
                        <label>Maßnahme *</label>
                        <input type="text" id="m-title" required>
                    </div>
                    <div class="form-group">
                        <label>Typ *</label>
                        <select id="m-typ">
                            <option value="Sofortmaßnahme">Sofortmaßnahme</option>
                            <option value="Korrekturmaßnahme">Korrekturmaßnahme</option>
                            <option value="Vorbeugemaßnahme">Vorbeugemaßnahme</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Termin *</label>
                        <input type="date" id="m-termin" required>
                    </div>
                    <div class="form-group">
                        <label>Verantwortlich</label>
                        <input type="text" id="m-verantwortlich">
                    </div>
                    <button type="submit" class="btn btn-primary">Speichern</button>
                </form>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);
    
    document.getElementById('massnahme-form').onsubmit = async (e) => {
        e.preventDefault();
        await createMassnahme();
    };
}

async function createMassnahme() {
    const data = {
        reklaId: window.currentReklamationId,
        title: document.getElementById('m-title').value,
        typ: document.getElementById('m-typ').value,
        termin: document.getElementById('m-termin').value,
        verantwortlich: document.getElementById('m-verantwortlich').value
    };
    
    try {
        const response = await fetch('/api/rms/massnahmen', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            closeMassnahmeModal();
            showDetail(window.currentReklamationId); // Refresh
            alert('Maßnahme erstellt!');
        } else {
            alert('Fehler beim Erstellen');
        }
    } catch (error) {
        console.error(error);
        alert('Fehler: ' + error.message);
    }
}

function closeMassnahmeModal() {
    document.getElementById('massnahme-modal')?.remove();
}
```

### 4.3 Button im Detail-Modal hinzufügen

```html
<!-- Im Detail-Modal, nach Maßnahmen-Tabelle -->
<button onclick="showAddMassnahmeModal()" class="btn btn-primary">
    + Maßnahme hinzufügen
</button>
```

### 4.4 Termin-Alarm Workflow (Optional heute, sonst morgen)

```
Workflow: RMS-Termin-Alarm
Trigger: Schedule (täglich 8:00)

1. SharePoint: Maßnahmen laden mit Status="Offen" und Termin < heute
2. Filter: Nur überfällige
3. Für jeden: Teams-Nachricht an Verantwortlichen
```

---

## ✅ CHECKLISTE

Nach Abschluss prüfen:

- [ ] Detail-Modal zeigt Maßnahmen
- [ ] Detail-Modal zeigt Schriftverkehr
- [ ] Suchfeld funktioniert
- [ ] KST-Filter funktioniert
- [ ] Sortierung funktioniert
- [ ] CSV-Export funktioniert
- [ ] Refresh-Button funktioniert
- [ ] Loading-Spinner erscheint
- [ ] Status-Chart vorhanden
- [ ] Priorität-Chart vorhanden
- [ ] Maßnahme erstellen funktioniert

---

## 📚 REFERENZEN

| Resource | Wert |
|----------|------|
| Dashboard | https://osp.schneider-kabelsatzbau.de/rms/ |
| n8n | http://46.224.102.30:5678 |
| Reklamationen | e9b1d926-085a-4435-a012-114ca9ba59a8 |
| Maßnahmen | 3768f2d8-878c-4a5f-bd52-7486fe93289d |
| Schriftverkehr | 741c6ae8-88bb-406b-bf85-2e11192a528f |
| Credential | Fm3IuAbVYBYDIA4U |
```

---

*Erstellt: 2026-01-28 | Ziel: HEUTE komplett umsetzen*
