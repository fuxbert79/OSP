// RMS Dashboard - Schneider Kabelsatzbau
// SharePoint-Integration via n8n API
// Version 2.0 - Alle Features

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
        'Massnahmen': '#6f42c1',
        'Abgeschlossen': '#28a745'
    }
};

// ============================================
// GLOBALE VARIABLEN
// ============================================

let allReklamationen = [];  // Cache fuer Filter/Suche/Sort
let currentSort = { field: 'Erfassungsdatum', dir: 'desc' };
let chartTrend, chartTyp, chartKST, chartStatus, chartPriority;

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
        return {
            offen: 12,
            kritisch: 3,
            ueberfaellig: 2,
            durchschnitt: 5.4
        };
    }
}

async function fetchReklamationen() {
    try {
        const response = await fetch(`${API_BASE}/reklamationen`);
        if (!response.ok) throw new Error('Reklamationen-Abruf fehlgeschlagen');
        const data = await response.json();

        // SharePoint-Daten transformieren
        if (data.value && Array.isArray(data.value)) {
            allReklamationen = data.value.map(item => {
                const f = item.fields || {};
                return {
                    id: item.id,
                    QA_ID: f.QA_ID || '',
                    Rekla_Typ: f.Rekla_Typ || 'Kunde',
                    Title: f.Title || 'Ohne Titel',
                    Rekla_Status: f.Rekla_Status || 'Neu',
                    Prioritaet: f.Prioritaet || 'mittel',
                    KST: f.KST || '',
                    Erfassungsdatum: f.Erfassungsdatum || '',
                    Zieldatum: f.Zieldatum || '',
                    Verantwortlich: f.Verantwortlich || '',
                    Beschreibung: f.Beschreibung || ''
                };
            });
        } else if (Array.isArray(data)) {
            allReklamationen = data;
        }

        return allReklamationen;
    } catch (error) {
        console.error('Fehler beim Reklamationen-Abruf:', error);
        allReklamationen = getMockReklamationen();
        return allReklamationen;
    }
}

async function fetchReklamationDetail(id) {
    try {
        // Versuche Detail-API (mit Massnahmen und Schriftverkehr)
        const response = await fetch(`${API_BASE}/detail?id=${id}`);
        if (response.ok) {
            return await response.json();
        }

        // Fallback: Basis-Daten aus Cache + Mock fuer Massnahmen
        const rekla = allReklamationen.find(r => r.id === id);
        if (rekla) {
            return {
                reklamation: rekla,
                massnahmen: [],
                schriftverkehr: [],
                sharePointUrl: `https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS/Lists/Reklamationen/DispForm.aspx?ID=${id}`
            };
        }

        return getMockDetail(id);
    } catch (error) {
        console.error('Fehler beim Detail-Abruf:', error);
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
        return getMockChartData();
    }
}

async function createMassnahme(data) {
    try {
        const response = await fetch(`${API_BASE}/massnahmen`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('Massnahme konnte nicht erstellt werden');
        return await response.json();
    } catch (error) {
        console.error('Fehler beim Erstellen der Massnahme:', error);
        throw error;
    }
}

// ============================================
// MOCK-DATEN (Fallback wenn API nicht verfuegbar)
// ============================================

function getMockReklamationen() {
    return [
        { id: '1', QA_ID: 'QA-26001', Rekla_Typ: 'KUNDE', Title: 'Falsche Steckerlaenge geliefert', Rekla_Status: 'Neu', Prioritaet: 'hoch', KST: 'F1', Erfassungsdatum: '2026-01-26', Beschreibung: 'Kunde meldet, dass die gelieferten Kabelsaetze 15cm kuerzer sind als spezifiziert.' },
        { id: '2', QA_ID: 'QA-26002', Rekla_Typ: 'LIEFERANT', Title: 'Materialqualitaet mangelhaft', Rekla_Status: 'In Bearbeitung', Prioritaet: 'kritisch', KST: 'EK', Erfassungsdatum: '2026-01-25', Beschreibung: 'Isoliermaterial weist Risse auf.' },
        { id: '3', QA_ID: 'QA-26003', Rekla_Typ: 'INTERN', Title: 'Crimphoehe ausserhalb Toleranz', Rekla_Status: 'Massnahmen', Prioritaet: 'mittel', KST: 'F2', Erfassungsdatum: '2026-01-24', Beschreibung: 'Crimphoehe bei Kontakt 123456 ausserhalb der Spezifikation.' },
        { id: '4', QA_ID: 'QA-26004', Rekla_Typ: 'KUNDE', Title: 'Beschaedigung beim Transport', Rekla_Status: 'Abgeschlossen', Prioritaet: 'niedrig', KST: 'VT', Erfassungsdatum: '2026-01-20', Beschreibung: 'Verpackung beschaedigt, Ware unbeschaedigt.' },
        { id: '5', QA_ID: 'QA-26005', Rekla_Typ: 'INTERN', Title: 'Pruefprotokoll fehlerhaft', Rekla_Status: 'Neu', Prioritaet: 'hoch', KST: 'QM', Erfassungsdatum: '2026-01-27', Beschreibung: 'Pruefprotokoll nicht vollstaendig ausgefuellt.' }
    ];
}

function getMockDetail(id) {
    return {
        reklamation: {
            id: id,
            QA_ID: 'QA-26001',
            Rekla_Typ: 'KUNDE',
            Title: 'Falsche Steckerlaenge geliefert',
            Rekla_Status: 'Neu',
            Prioritaet: 'hoch',
            KST: 'F1',
            Erfassungsdatum: '2026-01-26',
            Zieldatum: '2026-02-02',
            Verantwortlich: 'AL',
            Beschreibung: 'Kunde meldet, dass die gelieferten Kabelsaetze 15cm kuerzer sind als spezifiziert. Betrifft Auftrag A-2026-0142.'
        },
        massnahmen: [
            { Title: 'Ursachenanalyse durchfuehren', Typ: 'Sofortmassnahme', Termin: '2026-01-28', Status: 'Offen' },
            { Title: 'Nachlieferung veranlassen', Typ: 'Korrekturmassnahme', Termin: '2026-01-30', Status: 'Offen' }
        ],
        schriftverkehr: [
            { Datum: '2026-01-26', Typ: 'E-Mail', Betreff: 'Reklamation Auftrag A-2026-0142', Richtung: 'Eingang' }
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
        typ: [5, 4, 3],
        kst: {
            labels: ['F1', 'F2', 'F3', 'QM', 'EK', 'VT'],
            values: [4, 3, 2, 1, 1, 1]
        },
        status: [3, 4, 2, 3],
        priority: [2, 3, 4, 3]
    };
}

// ============================================
// UI FUNKTIONEN
// ============================================

function showLoading(show = true) {
    const loader = document.getElementById('loading-overlay');
    if (loader) {
        loader.style.display = show ? 'flex' : 'none';
    }
}

function updateKPIs(data) {
    if (!data) return;

    document.getElementById('kpi-offen').textContent = data.offen || 0;
    document.getElementById('kpi-kritisch').textContent = data.kritisch || 0;
    document.getElementById('kpi-ueberfaellig').textContent = data.ueberfaellig || 0;
    document.getElementById('kpi-durchschnitt').textContent =
        (data.durchschnitt || 0).toFixed(1) + ' Tage';

    // Farbliche Hervorhebung bei kritischen Werten
    const kritischEl = document.getElementById('kpi-kritisch').parentElement;
    kritischEl.classList.toggle('pulse', data.kritisch > 0);

    const ueberfaelligEl = document.getElementById('kpi-ueberfaellig').parentElement;
    ueberfaelligEl.classList.toggle('pulse', data.ueberfaellig > 0);
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
            <td><span class="status status-${(r.Rekla_Status || '').replace(/\s/g, '-').replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue')}">${escapeHtml(r.Rekla_Status || '--')}</span></td>
            <td><span class="priority priority-${(r.Prioritaet || '').toLowerCase()}">${escapeHtml(r.Prioritaet || '--')}</span></td>
            <td>${formatDate(r.Erfassungsdatum)}</td>
        </tr>
    `).join('');
}

function updateFilteredCount(filtered, total) {
    const countEl = document.getElementById('filtered-count');
    if (countEl) {
        countEl.textContent = filtered === total
            ? `${total} Eintraege`
            : `${filtered} von ${total}`;
    }
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
// FILTER, SUCHE & SORTIERUNG
// ============================================

function getFilters() {
    return {
        typ: document.getElementById('filter-typ')?.value || '',
        status: document.getElementById('filter-status')?.value || '',
        kst: document.getElementById('filter-kst')?.value || ''
    };
}

function applyFilters() {
    let filtered = [...allReklamationen];
    const filters = getFilters();

    // Typ-Filter
    if (filters.typ) {
        filtered = filtered.filter(r =>
            (r.Rekla_Typ || '').toLowerCase() === filters.typ.toLowerCase()
        );
    }

    // Status-Filter
    if (filters.status) {
        filtered = filtered.filter(r =>
            (r.Rekla_Status || '').toLowerCase() === filters.status.toLowerCase()
        );
    }

    // KST-Filter
    if (filters.kst) {
        filtered = filtered.filter(r =>
            (r.KST || '').toLowerCase() === filters.kst.toLowerCase()
        );
    }

    // Suchfeld
    const search = document.getElementById('search-input')?.value?.toLowerCase().trim();
    if (search) {
        filtered = filtered.filter(r =>
            (r.QA_ID || '').toLowerCase().includes(search) ||
            (r.Title || '').toLowerCase().includes(search) ||
            (r.Beschreibung || '').toLowerCase().includes(search) ||
            (r.Rekla_Typ || '').toLowerCase().includes(search) ||
            (r.KST || '').toLowerCase().includes(search) ||
            (r.Verantwortlich || '').toLowerCase().includes(search)
        );
    }

    // Sortierung anwenden
    filtered = sortData(filtered);

    updateTable(filtered);
    updateFilteredCount(filtered.length, allReklamationen.length);
}

function sortData(data) {
    return [...data].sort((a, b) => {
        let valA = a[currentSort.field] || '';
        let valB = b[currentSort.field] || '';

        // Datum-Felder
        if (currentSort.field.toLowerCase().includes('datum')) {
            valA = new Date(valA || '1970-01-01');
            valB = new Date(valB || '1970-01-01');
        } else {
            valA = String(valA).toLowerCase();
            valB = String(valB).toLowerCase();
        }

        if (currentSort.dir === 'asc') {
            return valA > valB ? 1 : valA < valB ? -1 : 0;
        } else {
            return valA < valB ? 1 : valA > valB ? -1 : 0;
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

// ============================================
// CSV EXPORT
// ============================================

function exportCSV() {
    const headers = ['QA-ID', 'Typ', 'Titel', 'Status', 'Prioritaet', 'KST', 'Erfasst', 'Zieldatum', 'Verantwortlich'];
    const rows = allReklamationen.map(r => [
        r.QA_ID || '',
        r.Rekla_Typ || '',
        (r.Title || '').replace(/[";]/g, ' '),
        r.Rekla_Status || '',
        r.Prioritaet || '',
        r.KST || '',
        formatDate(r.Erfassungsdatum),
        formatDate(r.Zieldatum),
        r.Verantwortlich || ''
    ]);

    const csv = [headers.join(';'), ...rows.map(r => r.join(';'))].join('\n');
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `RMS_Export_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
}

// ============================================
// DETAIL-VIEW
// ============================================

async function showDetail(id) {
    showLoading(true);

    // Edit-Modus zuruecksetzen
    isEditMode = false;
    document.getElementById('detail-view-mode').style.display = 'block';
    document.getElementById('detail-edit-mode').style.display = 'none';
    document.getElementById('btn-edit-toggle').textContent = 'Bearbeiten';

    try {
        const data = await fetchReklamationDetail(id);
        if (!data) {
            alert('Fehler beim Laden der Details');
            return;
        }

        const r = data.reklamation || data;

        // Modal befuellen
        document.getElementById('detail-qa-id').textContent = r.QA_ID || 'Unbekannt';

        // Stammdaten
        document.getElementById('detail-stammdaten').innerHTML = `
            <tr><td>Typ:</td><td>${escapeHtml(r.Rekla_Typ || '--')}</td></tr>
            <tr><td>Status:</td><td><span class="status status-${(r.Rekla_Status || '').replace(/\s/g, '-')}">${escapeHtml(r.Rekla_Status || '--')}</span></td></tr>
            <tr><td>Prioritaet:</td><td><span class="priority priority-${(r.Prioritaet || '').toLowerCase()}">${escapeHtml(r.Prioritaet || '--')}</span></td></tr>
            <tr><td>KST:</td><td>${escapeHtml(r.KST || '--')}</td></tr>
            <tr><td>Erfasst:</td><td>${formatDate(r.Erfassungsdatum)}</td></tr>
            <tr><td>Zieldatum:</td><td>${formatDate(r.Zieldatum)}</td></tr>
            <tr><td>Verantwortlich:</td><td>${escapeHtml(r.Verantwortlich || '--')}</td></tr>
        `;

        // Beschreibung
        document.getElementById('detail-beschreibung').textContent =
            r.Beschreibung || 'Keine Beschreibung vorhanden';

        // Massnahmen (mit Inline-Edit)
        const massnahmenTbody = document.querySelector('#detail-massnahmen tbody');
        const massnahmen = data.massnahmen || [];
        massnahmenTbody.innerHTML = renderMassnahmenTable(massnahmen);

        // Schriftverkehr
        const schriftverkehrTbody = document.querySelector('#detail-schriftverkehr tbody');
        const schriftverkehr = data.schriftverkehr || [];
        if (schriftverkehr.length > 0) {
            schriftverkehrTbody.innerHTML = schriftverkehr.map(s => `
                <tr>
                    <td>${formatDate(s.Datum)}</td>
                    <td>${escapeHtml(s.Typ || '--')}</td>
                    <td>${escapeHtml(s.Betreff || s.Title || '--')}</td>
                    <td>${escapeHtml(s.Richtung || '--')}</td>
                </tr>
            `).join('');
        } else {
            schriftverkehrTbody.innerHTML = '<tr><td colspan="4" class="no-data">Kein Schriftverkehr erfasst</td></tr>';
        }

        // Modal anzeigen
        document.getElementById('detail-modal').style.display = 'flex';

        // Speichere aktuelle ID fuer Actions
        window.currentReklamationId = id;
        window.currentReklamationData = data;
    } finally {
        showLoading(false);
    }
}

function closeDetail() {
    document.getElementById('detail-modal').style.display = 'none';
}

function openInSharePoint() {
    const data = window.currentReklamationData;
    if (data && data.sharePointUrl) {
        window.open(data.sharePointUrl, '_blank');
    } else {
        window.open('https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS', '_blank');
    }
}

async function generatePDF() {
    const data = window.currentReklamationData;
    if (!data) return;

    const r = data.reklamation || data;

    try {
        const response = await fetch('/api/rms/pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                abweichungs_nr: r.QA_ID,
                datum: new Date().toISOString().split('T')[0],
                artikel_bezeichnung: r.Title,
                beschreibung: r.Beschreibung || 'Keine Beschreibung',
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
// MASSNAHMEN-MANAGEMENT
// ============================================

function showMassnahmeModal() {
    // Standard-Termin auf heute + 7 Tage setzen
    const defaultDate = new Date();
    defaultDate.setDate(defaultDate.getDate() + 7);
    document.getElementById('m-termin').value = defaultDate.toISOString().split('T')[0];

    // Form zuruecksetzen
    document.getElementById('massnahme-form').reset();
    document.getElementById('m-termin').value = defaultDate.toISOString().split('T')[0];

    // Modal anzeigen
    document.getElementById('massnahme-modal').style.display = 'flex';
}

function closeMassnahmeModal() {
    document.getElementById('massnahme-modal').style.display = 'none';
}

async function handleMassnahmeSubmit(e) {
    e.preventDefault();

    const data = {
        reklaId: window.currentReklamationId,
        title: document.getElementById('m-title').value,
        typ: document.getElementById('m-typ').value,
        termin: document.getElementById('m-termin').value,
        verantwortlich: document.getElementById('m-verantwortlich').value
    };

    showLoading(true);

    try {
        await createMassnahme(data);
        closeMassnahmeModal();
        // Detail-View aktualisieren
        await showDetail(window.currentReklamationId);
        alert('Massnahme erfolgreich erstellt!');
    } catch (error) {
        alert('Fehler beim Erstellen der Massnahme: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// ============================================
// CHARTS (Chart.js)
// ============================================

async function initCharts() {
    const data = await fetchChartData();
    if (!data) return;

    const ciBlue = '#0080C9';
    const ciDark = '#003366';

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
                    borderColor: ciBlue,
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
                    backgroundColor: [ciBlue, '#DC500F', '#28a745']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                                const pct = total > 0 ? Math.round(ctx.raw / total * 100) : 0;
                                return `${ctx.label}: ${ctx.raw} (${pct}%)`;
                            }
                        }
                    }
                }
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
                    backgroundColor: ciBlue
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

    // Status-Chart (Pie) - NEU
    const ctxStatus = document.getElementById('chart-status')?.getContext('2d');
    if (ctxStatus) {
        if (chartStatus) chartStatus.destroy();
        chartStatus = new Chart(ctxStatus, {
            type: 'pie',
            data: {
                labels: ['Neu', 'In Bearbeitung', 'Massnahmen', 'Abgeschlossen'],
                datasets: [{
                    data: data.status || [0, 0, 0, 0],
                    backgroundColor: ['#17a2b8', '#ffc107', '#6f42c1', '#28a745']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                                const pct = total > 0 ? Math.round(ctx.raw / total * 100) : 0;
                                return `${ctx.label}: ${ctx.raw} (${pct}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Prioritaet-Chart (Bar horizontal) - NEU
    const ctxPriority = document.getElementById('chart-priority')?.getContext('2d');
    if (ctxPriority) {
        if (chartPriority) chartPriority.destroy();
        chartPriority = new Chart(ctxPriority, {
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
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { beginAtZero: true }
                }
            }
        });
    }
}

// ============================================
// EDIT MODE
// ============================================

let isEditMode = false;

function toggleEditMode() {
    isEditMode = !isEditMode;

    document.getElementById('detail-view-mode').style.display = isEditMode ? 'none' : 'block';
    document.getElementById('detail-edit-mode').style.display = isEditMode ? 'block' : 'none';
    document.getElementById('btn-edit-toggle').textContent = isEditMode ? 'Abbrechen' : 'Bearbeiten';

    if (isEditMode) {
        populateEditForm();
    }
}

function populateEditForm() {
    const data = window.currentReklamationData?.reklamation;
    if (!data) return;

    // Felder befuellen
    document.getElementById('edit-typ').value = data.Rekla_Typ || 'Kunde';
    document.getElementById('edit-status').value = data.Rekla_Status || 'Neu';
    document.getElementById('edit-prioritaet').value = (data.Prioritaet || 'mittel').toLowerCase();
    document.getElementById('edit-kst').value = data.KST || '';
    document.getElementById('edit-verantwortlich').value = data.Verantwortlich || '';
    document.getElementById('edit-zieldatum').value = data.Zieldatum?.split('T')[0] || '';
    document.getElementById('edit-title').value = data.Title || '';
    document.getElementById('edit-beschreibung').value = data.Beschreibung || '';
}

async function saveReklamation(event) {
    event.preventDefault();

    const id = window.currentReklamationId;
    if (!id) {
        alert('Keine Reklamation ausgewaehlt');
        return;
    }

    const fields = {
        Rekla_Typ: document.getElementById('edit-typ').value,
        Rekla_Status: document.getElementById('edit-status').value,
        Prioritaet: document.getElementById('edit-prioritaet').value,
        KST: document.getElementById('edit-kst').value,
        Verantwortlich: document.getElementById('edit-verantwortlich').value,
        Zieldatum: document.getElementById('edit-zieldatum').value || null,
        Title: document.getElementById('edit-title').value,
        Beschreibung: document.getElementById('edit-beschreibung').value
    };

    // Leere Felder entfernen (optional)
    Object.keys(fields).forEach(key => {
        if (fields[key] === '' || fields[key] === null) {
            delete fields[key];
        }
    });

    try {
        showLoading(true);

        const response = await fetch('/api/rms/update', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id, fields })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            alert('Reklamation gespeichert!');
            toggleEditMode();
            // Detail-View neu laden
            await showDetail(id);
            // Tabelle aktualisieren
            await loadData();
        } else {
            alert('Fehler: ' + (result.error || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('Save error:', error);
        alert('Fehler beim Speichern: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// ============================================
// MASSNAHMEN EDIT
// ============================================

function renderMassnahmenTable(massnahmen) {
    if (!massnahmen || massnahmen.length === 0) {
        return '<tr><td colspan="5" class="no-data">Keine Massnahmen erfasst</td></tr>';
    }

    return massnahmen.map(m => `
        <tr data-massnahme-id="${m.id}">
            <td>${escapeHtml(m.Title || '--')}</td>
            <td>${escapeHtml(m.Typ || '--')}</td>
            <td>
                <input type="date" class="form-control-sm"
                       value="${m.Termin?.split('T')[0] || ''}"
                       onchange="updateMassnahmeField(${m.id}, 'Termin', this.value)">
            </td>
            <td>
                <select class="form-control-sm" onchange="updateMassnahmeField(${m.id}, 'Status', this.value)">
                    <option value="Offen" ${m.Status === 'Offen' ? 'selected' : ''}>Offen</option>
                    <option value="In Arbeit" ${m.Status === 'In Arbeit' ? 'selected' : ''}>In Arbeit</option>
                    <option value="Erledigt" ${m.Status === 'Erledigt' ? 'selected' : ''}>Erledigt</option>
                    <option value="Wirksamkeit pruefen" ${m.Status === 'Wirksamkeit pruefen' ? 'selected' : ''}>Wirksamkeit pruefen</option>
                </select>
            </td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="deleteMassnahme(${m.id})" title="Loeschen">X</button>
            </td>
        </tr>
    `).join('');
}

async function updateMassnahmeField(massnahmeId, field, value) {
    try {
        const response = await fetch('/api/rms/update-massnahme', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id: massnahmeId,
                fields: { [field]: value }
            })
        });

        if (!response.ok) {
            throw new Error('Update fehlgeschlagen');
        }

        console.log(`Massnahme ${massnahmeId}: ${field} = ${value}`);
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Aktualisieren der Massnahme');
    }
}

async function deleteMassnahme(massnahmeId) {
    if (!confirm('Massnahme wirklich loeschen?')) return;

    try {
        const response = await fetch(`/api/rms/delete-massnahme?id=${massnahmeId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            // Detail-View neu laden
            await showDetail(window.currentReklamationId);
        } else {
            alert('Fehler beim Loeschen');
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Loeschen');
    }
}

// ============================================
// DATEN LADEN
// ============================================

async function loadData() {
    // KPIs laden
    const kpis = await fetchKPIs();
    updateKPIs(kpis);

    // Reklamationen laden
    await fetchReklamationen();
    applyFilters();
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
// INITIALISIERUNG
// ============================================

document.addEventListener('DOMContentLoaded', async function() {
    console.log('RMS Dashboard wird initialisiert...');

    // Event-Listener fuer Filter
    document.getElementById('filter-typ')?.addEventListener('change', applyFilters);
    document.getElementById('filter-status')?.addEventListener('change', applyFilters);
    document.getElementById('filter-kst')?.addEventListener('change', applyFilters);

    // Suchfeld mit Debounce
    let searchTimeout;
    document.getElementById('search-input')?.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(applyFilters, 300);
    });

    // Sortierung
    document.querySelectorAll('th[data-sort]').forEach(th => {
        th.addEventListener('click', () => handleSort(th.dataset.sort));
    });

    // Refresh-Button
    document.getElementById('btn-refresh')?.addEventListener('click', function() {
        this.classList.add('spinning');
        refreshData().then(() => {
            setTimeout(() => this.classList.remove('spinning'), 500);
        });
    });

    // Export-Button
    document.getElementById('btn-export')?.addEventListener('click', exportCSV);

    // Modal schliessen
    document.querySelector('#detail-modal .close-btn')?.addEventListener('click', closeDetail);
    window.onclick = function(event) {
        const detailModal = document.getElementById('detail-modal');
        const massnahmeModal = document.getElementById('massnahme-modal');
        if (event.target === detailModal) closeDetail();
        if (event.target === massnahmeModal) closeMassnahmeModal();
    };

    // ESC-Taste zum Schliessen
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeDetail();
            closeMassnahmeModal();
        }
    });

    // Massnahme hinzufuegen
    document.getElementById('btn-add-massnahme')?.addEventListener('click', showMassnahmeModal);
    document.getElementById('massnahme-form')?.addEventListener('submit', handleMassnahmeSubmit);

    // Edit-Form
    document.getElementById('edit-reklamation-form')?.addEventListener('submit', saveReklamation);

    // Initiale Sortierung markieren
    document.querySelector(`th[data-sort="${currentSort.field}"]`)?.classList.add('sort-desc');

    // Daten laden
    showLoading(true);
    try {
        await loadData();

        // Charts initialisieren
        if (typeof Chart !== 'undefined') {
            await initCharts();
        } else {
            console.warn('Chart.js nicht geladen - Charts werden nicht angezeigt');
        }
    } finally {
        showLoading(false);
    }

    // Auto-Refresh
    setInterval(() => loadData(), CONFIG.refreshInterval);

    console.log('RMS Dashboard bereit');
});
