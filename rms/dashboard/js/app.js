// RMS Dashboard - Schneider Kabelsatzbau
// SharePoint-Integration via n8n API

const API_BASE = '/api/rms';

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
        // Fallback: Mock-Daten zurückgeben
        return {
            offen: 12,
            kritisch: 3,
            ueberfaellig: 2,
            durchschnitt: 5.4
        };
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
        // Fallback: Mock-Daten
        return getMockReklamationen(filters);
    }
}

async function fetchReklamationDetail(id) {
    try {
        const response = await fetch(`${API_BASE}/reklamation/${id}`);
        if (!response.ok) throw new Error('Detail-Abruf fehlgeschlagen');
        return await response.json();
    } catch (error) {
        console.error('Fehler beim Detail-Abruf:', error);
        // Fallback: Mock-Detail
        return getMockDetail(id);
    }
}

async function fetchChartData() {
    try {
        const response = await fetch(`${API_BASE}/charts`);
        if (!response.ok) throw new Error('Chart-Daten-Abruf fehlgeschlagen');
        return await response.json();
    } catch (error) {
        console.error('Fehler beim Chart-Daten-Abruf:', error);
        // Fallback: Mock-Charts
        return getMockChartData();
    }
}

// ============================================
// MOCK-DATEN (Fallback wenn API nicht verfügbar)
// ============================================

function getMockReklamationen(filters = {}) {
    const mockData = [
        { id: '1', QA_ID: 'QA-26001', Rekla_Typ: 'KUNDE', Title: 'Falsche Steckerlänge geliefert', Rekla_Status: 'Neu', Prioritaet: 'hoch', KST: 'F1', Erfassungsdatum: '2026-01-26' },
        { id: '2', QA_ID: 'QA-26002', Rekla_Typ: 'LIEFERANT', Title: 'Materialqualität mangelhaft', Rekla_Status: 'In Bearbeitung', Prioritaet: 'kritisch', KST: 'EK', Erfassungsdatum: '2026-01-25' },
        { id: '3', QA_ID: 'QA-26003', Rekla_Typ: 'INTERN', Title: 'Crimphöhe außerhalb Toleranz', Rekla_Status: 'Maßnahmen', Prioritaet: 'mittel', KST: 'F2', Erfassungsdatum: '2026-01-24' },
        { id: '4', QA_ID: 'QA-26004', Rekla_Typ: 'KUNDE', Title: 'Beschädigung beim Transport', Rekla_Status: 'Abgeschlossen', Prioritaet: 'niedrig', KST: 'VT', Erfassungsdatum: '2026-01-20' },
        { id: '5', QA_ID: 'QA-26005', Rekla_Typ: 'INTERN', Title: 'Prüfprotokoll fehlerhaft', Rekla_Status: 'Neu', Prioritaet: 'hoch', KST: 'QM', Erfassungsdatum: '2026-01-27' }
    ];

    return mockData.filter(r => {
        if (filters.typ && r.Rekla_Typ !== filters.typ) return false;
        if (filters.status && r.Rekla_Status !== filters.status) return false;
        if (filters.kst && r.KST !== filters.kst) return false;
        return true;
    });
}

function getMockDetail(id) {
    return {
        id: id,
        QA_ID: 'QA-26001',
        Rekla_Typ: 'KUNDE',
        Title: 'Falsche Steckerlänge geliefert',
        Rekla_Status: 'Neu',
        Prioritaet: 'hoch',
        KST: 'F1',
        Erfassungsdatum: '2026-01-26',
        Zieldatum: '2026-02-02',
        Verantwortlich: 'AL',
        Beschreibung: 'Kunde meldet, dass die gelieferten Kabelsätze 15cm kürzer sind als spezifiziert. Betrifft Auftrag A-2026-0142.',
        massnahmen: [
            { Title: 'Ursachenanalyse durchführen', Termin: '2026-01-28', Status: 'Offen' },
            { Title: 'Nachlieferung veranlassen', Termin: '2026-01-30', Status: 'Offen' }
        ],
        schriftverkehr: [
            { Datum: '2026-01-26', Typ: 'E-Mail Eingang', Betreff: 'Reklamation Auftrag A-2026-0142' }
        ],
        sharePointUrl: 'https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS'
    };
}

function getMockChartData() {
    return {
        trend: {
            labels: ['Aug', 'Sep', 'Okt', 'Nov', 'Dez', 'Jan'],
            values: [8, 12, 6, 15, 9, 12]
        },
        typ: [5, 4, 3],  // Kunde, Lieferant, Intern
        kst: {
            labels: ['F1', 'F2', 'F3', 'QM', 'EK', 'VT'],
            values: [4, 3, 2, 1, 1, 1]
        }
    };
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
    kritischEl.classList.remove('pulse');
    if (data.kritisch > 0) {
        kritischEl.classList.add('pulse');
    }

    const ueberfaelligEl = document.getElementById('kpi-ueberfaellig').parentElement;
    ueberfaelligEl.classList.remove('pulse');
    if (data.ueberfaellig > 0) {
        ueberfaelligEl.classList.add('pulse');
    }
}

function updateTable(reklamationen) {
    const tbody = document.querySelector('#reklamationen-table tbody');

    if (!reklamationen || reklamationen.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="no-data">Keine Reklamationen gefunden</td></tr>';
        return;
    }

    tbody.innerHTML = reklamationen.map(r => `
        <tr onclick="showDetail('${r.id}')" class="clickable-row">
            <td><strong>${escapeHtml(r.QA_ID || '--')}</strong></td>
            <td><span class="badge badge-${(r.Rekla_Typ || '').toLowerCase()}">${escapeHtml(r.Rekla_Typ || '--')}</span></td>
            <td>${escapeHtml(r.Title || '--')}</td>
            <td><span class="status status-${(r.Rekla_Status || '').replace(/\s/g, '-')}">${escapeHtml(r.Rekla_Status || '--')}</span></td>
            <td><span class="priority priority-${(r.Prioritaet || '').toLowerCase()}">${escapeHtml(r.Prioritaet || '--')}</span></td>
            <td>${formatDate(r.Erfassungsdatum)}</td>
        </tr>
    `).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    if (!dateStr) return '--';
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return '--';
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
        <tr><td>Typ:</td><td>${escapeHtml(data.Rekla_Typ || '--')}</td></tr>
        <tr><td>Status:</td><td>${escapeHtml(data.Rekla_Status || '--')}</td></tr>
        <tr><td>Priorität:</td><td>${escapeHtml(data.Prioritaet || '--')}</td></tr>
        <tr><td>KST:</td><td>${escapeHtml(data.KST || '--')}</td></tr>
        <tr><td>Erfasst:</td><td>${formatDate(data.Erfassungsdatum)}</td></tr>
        <tr><td>Zieldatum:</td><td>${formatDate(data.Zieldatum)}</td></tr>
        <tr><td>Verantwortlich:</td><td>${escapeHtml(data.Verantwortlich || '--')}</td></tr>
    `;

    // Beschreibung
    document.getElementById('detail-beschreibung').textContent =
        data.Beschreibung || 'Keine Beschreibung vorhanden';

    // Maßnahmen
    const massnahmenTbody = document.querySelector('#detail-massnahmen tbody');
    if (data.massnahmen && data.massnahmen.length > 0) {
        massnahmenTbody.innerHTML = data.massnahmen.map(m => `
            <tr>
                <td>${escapeHtml(m.Title || '--')}</td>
                <td>${formatDate(m.Termin)}</td>
                <td>${escapeHtml(m.Status || '--')}</td>
            </tr>
        `).join('');
    } else {
        massnahmenTbody.innerHTML = '<tr><td colspan="3" class="no-data">Keine Maßnahmen erfasst</td></tr>';
    }

    // Schriftverkehr
    const schriftverkehrTbody = document.querySelector('#detail-schriftverkehr tbody');
    if (data.schriftverkehr && data.schriftverkehr.length > 0) {
        schriftverkehrTbody.innerHTML = data.schriftverkehr.map(s => `
            <tr>
                <td>${formatDate(s.Datum)}</td>
                <td>${escapeHtml(s.Typ || '--')}</td>
                <td>${escapeHtml(s.Betreff || '--')}</td>
            </tr>
        `).join('');
    } else {
        schriftverkehrTbody.innerHTML = '<tr><td colspan="3" class="no-data">Kein Schriftverkehr erfasst</td></tr>';
    }

    // Modal anzeigen
    document.getElementById('detail-modal').style.display = 'flex';

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
        alert('PDF-Erstellung fehlgeschlagen (Server nicht erreichbar)');
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
        if (chartTrend) chartTrend.destroy();
        chartTrend = new Chart(ctxTrend, {
            type: 'line',
            data: {
                labels: data.trend?.labels || [],
                datasets: [{
                    label: 'Reklamationen',
                    data: data.trend?.values || [],
                    borderColor: '#0080C9',
                    backgroundColor: 'rgba(0, 128, 201, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    // Typ-Chart (Donut)
    const ctxTyp = document.getElementById('chart-typ')?.getContext('2d');
    if (ctxTyp) {
        if (chartTyp) chartTyp.destroy();
        chartTyp = new Chart(ctxTyp, {
            type: 'doughnut',
            data: {
                labels: ['Kunde', 'Lieferant', 'Intern'],
                datasets: [{
                    data: data.typ || [0, 0, 0],
                    backgroundColor: ['#0080C9', '#DC500F', '#28a745']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // KST-Chart (Bar)
    const ctxKST = document.getElementById('chart-kst')?.getContext('2d');
    if (ctxKST) {
        if (chartKST) chartKST.destroy();
        chartKST = new Chart(ctxKST, {
            type: 'bar',
            data: {
                labels: data.kst?.labels || [],
                datasets: [{
                    label: 'Reklamationen',
                    data: data.kst?.values || [],
                    backgroundColor: '#0080C9'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
}

// ============================================
// FILTER
// ============================================

function getFilters() {
    return {
        typ: document.getElementById('filter-typ')?.value || '',
        status: document.getElementById('filter-status')?.value || '',
        kst: document.getElementById('filter-kst')?.value || ''
    };
}

function applyFilters() {
    loadData(getFilters());
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

    // Refresh-Button
    document.getElementById('btn-refresh')?.addEventListener('click', function() {
        this.classList.add('spinning');
        loadData(getFilters()).then(() => {
            initCharts();
            setTimeout(() => this.classList.remove('spinning'), 500);
        });
    });

    // Modal schließen
    document.querySelector('.close-btn')?.addEventListener('click', closeDetail);
    window.onclick = function(event) {
        const modal = document.getElementById('detail-modal');
        if (event.target === modal) {
            closeDetail();
        }
    };

    // ESC-Taste zum Schließen
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeDetail();
        }
    });

    // Daten laden
    await loadData();

    // Charts initialisieren
    if (typeof Chart !== 'undefined') {
        await initCharts();
    } else {
        console.warn('Chart.js nicht geladen - Charts werden nicht angezeigt');
    }

    // Auto-Refresh
    setInterval(() => loadData(getFilters()), CONFIG.refreshInterval);

    console.log('RMS Dashboard bereit');
});
