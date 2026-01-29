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
let m365Users = [];  // M365 Benutzer aus Graph API

// Pagination
const ITEMS_PER_PAGE = 20;
let currentPage = 1;
let totalPages = 1;

// ============================================
// M365 BENUTZER
// ============================================

async function loadM365Users() {
    try {
        const response = await fetch('/api/rms/users');
        if (!response.ok) {
            console.warn('M365-Benutzer API nicht verfuegbar, verwende Fallback');
            // Fallback: Verwende VERANTWORTLICHE aus massnahmen-templates.js falls vorhanden
            if (typeof VERANTWORTLICHE !== 'undefined') {
                m365Users = VERANTWORTLICHE.map(v => ({
                    id: v.kuerzel,
                    displayName: v.name,
                    mail: v.email,
                    jobTitle: v.rolle,
                    kuerzel: v.kuerzel
                }));
                console.log(`${m365Users.length} Benutzer aus Fallback geladen`);
            }
            return m365Users;
        }
        const data = await response.json();
        m365Users = data.users || [];
        console.log(`${m365Users.length} M365-Benutzer geladen`);
        return m365Users;
    } catch (error) {
        console.error('M365-Benutzer laden fehlgeschlagen:', error);
        // Fallback bei Fehler
        if (typeof VERANTWORTLICHE !== 'undefined') {
            m365Users = VERANTWORTLICHE.map(v => ({
                id: v.kuerzel,
                displayName: v.name,
                mail: v.email,
                jobTitle: v.rolle,
                kuerzel: v.kuerzel
            }));
        }
        return m365Users;
    }
}

function populateUserDropdown(selectElementId, selectedValue = '') {
    const select = document.getElementById(selectElementId);
    if (!select) return;

    // Bestehende Optionen loeschen (ausser Platzhalter)
    select.innerHTML = '<option value="">-- Auswaehlen --</option>';

    // M365-Benutzer als Optionen hinzufuegen
    m365Users.forEach(user => {
        const option = document.createElement('option');
        // Verwende E-Mail als Wert (fuer Benachrichtigungen) oder Kuerzel als Fallback
        option.value = user.mail || user.kuerzel || user.id;
        option.textContent = `${user.displayName}${user.jobTitle ? ' (' + user.jobTitle + ')' : ''}`;
        option.dataset.id = user.id;
        option.dataset.displayName = user.displayName;
        option.dataset.mail = user.mail || '';

        // Selektion pruefen (nach E-Mail, DisplayName oder Kuerzel)
        if (selectedValue && (
            selectedValue === user.mail ||
            selectedValue === user.displayName ||
            selectedValue === user.kuerzel ||
            selectedValue === user.id
        )) {
            option.selected = true;
        }

        select.appendChild(option);
    });
}

// ============================================
// STAMMDATEN (Kunden/Lieferanten)
// ============================================

let stammdatenCache = { kunden: [], lieferanten: [], alle: [] };

async function loadStammdaten() {
    try {
        const response = await fetch('/api/rms/stammdaten');
        if (!response.ok) {
            console.warn('Stammdaten API nicht verfuegbar');
            return [];
        }
        const data = await response.json();
        const stammdaten = data.stammdaten || [];

        // Cache aufteilen
        stammdatenCache.alle = stammdaten;
        stammdatenCache.kunden = stammdaten.filter(s => s.typ === 'Kunde');
        stammdatenCache.lieferanten = stammdaten.filter(s => s.typ === 'Lieferant');

        console.log(`Stammdaten geladen: ${stammdaten.length} (${stammdatenCache.kunden.length} Kunden, ${stammdatenCache.lieferanten.length} Lieferanten)`);
        return stammdaten;
    } catch (error) {
        console.error('Stammdaten laden fehlgeschlagen:', error);
        return [];
    }
}

function setupStammdatenAutocomplete(inputId, datalistId, typ = null) {
    const input = document.getElementById(inputId);
    const datalist = document.getElementById(datalistId);

    if (!input || !datalist) return;

    // Stammdaten basierend auf Typ waehlen
    let stammdaten = stammdatenCache.alle;
    if (typ === 'Kunde' || typ === 'KUNDE') {
        stammdaten = stammdatenCache.kunden;
    } else if (typ === 'Lieferant' || typ === 'LIEFERANT') {
        stammdaten = stammdatenCache.lieferanten;
    }

    // Datalist befuellen - sowohl Name als auch DebKredNr als Suchoptionen
    // Jeder Eintrag kann über Name ODER DebKredNr gefunden werden
    let options = [];
    stammdaten.forEach(s => {
        // Option mit Name als Wert
        options.push(`<option value="${escapeHtml(s.name)}" data-id="${s.id}" data-debkred="${s.debKredNr}">${s.debKredNr || ''} - ${escapeHtml(s.name)}</option>`);
        // Option mit DebKredNr als Wert (falls vorhanden)
        if (s.debKredNr) {
            options.push(`<option value="${s.debKredNr}" data-id="${s.id}" data-name="${escapeHtml(s.name)}">${s.debKredNr} - ${escapeHtml(s.name)}</option>`);
        }
    });
    datalist.innerHTML = options.join('');

    // Bei Auswahl zusaetzliche Daten setzen
    input.addEventListener('change', (e) => {
        const value = e.target.value;
        // Suche nach Name ODER DebKredNr
        const selected = stammdaten.find(s => s.name === value || s.debKredNr === value);
        if (selected) {
            // Wenn DebKredNr eingegeben wurde, setze den Namen ins Feld
            if (selected.debKredNr === value) {
                input.value = selected.name;
            }
            // Felder mit ID/DebKredNr fuellen
            const hiddenId = document.getElementById(inputId + '-id');
            const nrField = document.getElementById(inputId + '-nr');
            if (hiddenId) hiddenId.value = selected.id;
            if (nrField) nrField.value = selected.debKredNr || '';

            // Optional: Adressdaten in separate Felder
            const adresseField = document.getElementById(inputId + '-adresse');
            if (adresseField && selected.adresse) {
                adresseField.value = `${selected.adresse}, ${selected.plz} ${selected.ort}`;
            }
        }
    });
}

function getStammdatenByTyp(typ) {
    if (typ === 'Kunde' || typ === 'KUNDE') {
        return stammdatenCache.kunden;
    } else if (typ === 'Lieferant' || typ === 'LIEFERANT') {
        return stammdatenCache.lieferanten;
    }
    return stammdatenCache.alle;
}

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
                    Beschreibung: f.Beschreibung || '',
                    Absender: f.Absender || '',
                    DebKredNr: f.DebKredNr || '',
                    hasNZA: f.hasNZA || false,
                    Modified: item.lastModifiedDateTime || f.Modified || ''
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
        tbody.innerHTML = '<tr><td colspan="8" class="no-data">Keine Reklamationen gefunden</td></tr>';
        return;
    }

    tbody.innerHTML = reklamationen.map(r => `
        <tr onclick="showDetail('${r.id}')" class="clickable-row">
            <td><strong>${escapeHtml(r.QA_ID || '--')}</strong></td>
            <td><span class="badge badge-${(r.Rekla_Typ || '').toLowerCase()}">${escapeHtml(r.Rekla_Typ || '--')}</span></td>
            <td>${escapeHtml(r.DebKredNr || '--')}</td>
            <td>${escapeHtml(r.Title || '--')}</td>
            <td><span class="status status-${(r.Rekla_Status || '').replace(/\s/g, '-').replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue')}">${escapeHtml(r.Rekla_Status || '--')}</span></td>
            <td><span class="priority priority-${(r.Prioritaet || '').toLowerCase()}">${escapeHtml(r.Prioritaet || '--')}</span></td>
            <td>${r.hasNZA ? '<span class="badge badge-nza" title="NZA-Formular vorhanden">NZA</span>' : ''}</td>
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
        status: document.getElementById('filter-status')?.value || ''
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

    // Pagination anwenden
    const paginatedData = paginateData(filtered);

    updateTable(paginatedData);
    updateFilteredCount(filtered.length, allReklamationen.length);
    renderPaginationControls(filtered.length);
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

// ============================================
// PAGINATION
// ============================================

function paginateData(data) {
    totalPages = Math.ceil(data.length / ITEMS_PER_PAGE);
    if (currentPage > totalPages) currentPage = totalPages || 1;
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    return data.slice(start, end);
}

function renderPaginationControls(totalItems) {
    const container = document.getElementById('pagination-controls');
    if (!container) return;

    totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = '<div class="pagination">';

    // Zurueck-Button
    html += `<button class="btn btn-sm ${currentPage === 1 ? 'disabled' : ''}"
             onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
             &larr; Zurueck</button>`;

    // Seiten-Anzeige
    html += `<span class="pagination-info">Seite ${currentPage} von ${totalPages} (${totalItems} Eintraege)</span>`;

    // Vor-Button
    html += `<button class="btn btn-sm ${currentPage === totalPages ? 'disabled' : ''}"
             onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
             Weiter &rarr;</button>`;

    html += '</div>';

    container.innerHTML = html;
}

function changePage(page) {
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    applyFilters(); // Neu rendern mit aktueller Seite
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
            <tr><td>Absender:</td><td>${escapeHtml(r.Absender || '--')}</td></tr>
            <tr><td>Deb./Kred.-Nr.:</td><td>${escapeHtml(r.DebKredNr || '--')}</td></tr>
            <tr><td>Status:</td><td><span class="status status-${(r.Rekla_Status || '').replace(/\s/g, '-')}">${escapeHtml(r.Rekla_Status || '--')}</span></td></tr>
            <tr><td>Prioritaet:</td><td><span class="priority priority-${(r.Prioritaet || '').toLowerCase()}">${escapeHtml(r.Prioritaet || '--')}</span></td></tr>
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

        // Speichere aktuelle ID fuer Actions
        window.currentReklamationId = id;
        window.currentReklamationData = data;

        // Tracking-Sektion anzeigen (nur fuer Lieferanten-Reklas)
        showTrackingSection(r);

        // Modal anzeigen
        document.getElementById('detail-modal').style.display = 'flex';

        // Fotos & Dokumente laden (async im Hintergrund)
        if (r.QA_ID) {
            loadAllFilesForDetail(r.QA_ID).catch(err => {
                console.warn('Dateien konnten nicht geladen werden:', err);
            });
        }
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
    if (!data?.reklamation) {
        alert('Keine Reklamation geladen');
        return;
    }

    // Formular-Dialog anzeigen
    const formularTyp = await showFormularTypeDialog();
    if (!formularTyp) return;

    try {
        showLoading(true);

        const response = await fetch('/api/rms/generate-formblatt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                qaId: data.reklamation.QA_ID,
                formularTyp: formularTyp,
                reklamationsDaten: data.reklamation
            })
        });

        const result = await response.json();

        if (result.success) {
            // Wenn NZA-Formular (F-QM-04) erstellt wurde, hasNZA setzen
            if (formularTyp === 'F_QM_04' || formularTyp === 'F-QM-04') {
                try {
                    await fetch('/api/rms/update', {
                        method: 'PATCH',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            id: window.currentReklamationId,
                            fields: { hasNZA: true }
                        })
                    });
                    console.log('hasNZA auf true gesetzt');
                } catch (e) {
                    console.warn('hasNZA konnte nicht gesetzt werden:', e);
                }
            }

            alert(`${formularTyp} wurde erstellt!\n\nPDF: ${result.pdfUrl || 'Wird generiert...'}`);
            // Dokumente neu laden
            if (data.reklamation.QA_ID) {
                await loadAllFilesForDetail(data.reklamation.QA_ID);
            }
            // Tabelle aktualisieren um NZA-Badge anzuzeigen
            await loadData();
        } else {
            alert('Fehler: ' + (result.error || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('PDF-Fehler:', error);
        alert('PDF-Erstellung fehlgeschlagen (Server nicht erreichbar)');
    } finally {
        showLoading(false);
    }
}

function showFormularTypeDialog() {
    return new Promise((resolve) => {
        const modal = document.getElementById('formular-dialog');
        modal.style.display = 'flex';

        window.selectFormular = () => {
            const typ = document.getElementById('formular-typ-select').value;
            modal.style.display = 'none';
            resolve(typ);
        };

        window.cancelFormular = () => {
            modal.style.display = 'none';
            resolve(null);
        };
    });
}

// ============================================
// DATEIEN & FOTOS
// ============================================

async function loadFiles(qaId, folder = '') {
    try {
        const response = await fetch(`/api/rms/files?qaId=${qaId}&folder=${folder}`);
        if (!response.ok) return { files: [] };
        return await response.json();
    } catch (error) {
        console.error('Fehler beim Laden der Dateien:', error);
        return { files: [] };
    }
}

async function loadAllFilesForDetail(qaId) {
    // Fotos laden
    const fotosData = await loadFiles(qaId, 'Fotos');
    renderFotos(fotosData.files || []);

    // Dokumente laden (Root + Schriftverkehr)
    const docsData = await loadFiles(qaId, '');
    const svData = await loadFiles(qaId, 'Schriftverkehr');

    const allDocs = [
        ...(docsData.files || []).filter(f => !f.isFolder),
        ...(svData.files || [])
    ];
    renderDokumente(allDocs);

    // NZA-Formular pruefen (F-QM-04)
    const hasNZA = allDocs.some(f =>
        f.name && (f.name.includes('F-QM-04') || f.name.includes('F_QM_04') || f.name.toLowerCase().includes('nza'))
    );
    updateNZAStatus(hasNZA);
}

function updateNZAStatus(hasNZA) {
    // NZA-Status im Detail-View anzeigen
    const qaIdEl = document.getElementById('detail-qa-id');
    if (qaIdEl) {
        // Entferne altes Badge falls vorhanden
        const oldBadge = qaIdEl.querySelector('.nza-badge');
        if (oldBadge) oldBadge.remove();

        // Fuege Badge hinzu wenn NZA vorhanden
        if (hasNZA) {
            const badge = document.createElement('span');
            badge.className = 'nza-badge';
            badge.style.cssText = 'margin-left: 10px; background: #fff8e1; color: #f57c00; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;';
            badge.textContent = 'NZA';
            badge.title = 'NZA-Formular (F-QM-04) vorhanden';
            qaIdEl.appendChild(badge);
        }
    }
}

function renderFotos(files) {
    const container = document.getElementById('detail-fotos');
    if (!container) return;

    if (!files || files.length === 0) {
        container.innerHTML = '<p class="empty-state">Keine Fotos vorhanden</p>';
        return;
    }

    container.innerHTML = files.map(file => `
        <div class="file-thumbnail" onclick="showFilePreview('${file.id}', '${escapeHtml(file.name)}', '${file.webUrl}', '${file.downloadUrl || ''}', '${file.mimeType}')">
            ${file.thumbnailUrl
                ? `<img src="${file.thumbnailUrl}" alt="${escapeHtml(file.name)}">`
                : `<div class="file-icon">📷</div>`
            }
            <span class="file-name">${truncateFilename(file.name, 20)}</span>
        </div>
    `).join('');
}

function renderDokumente(files) {
    const container = document.getElementById('detail-dokumente');
    if (!container) return;

    if (!files || files.length === 0) {
        container.innerHTML = '<p class="empty-state">Keine Dokumente vorhanden</p>';
        return;
    }

    // Nach Typ gruppieren
    const formblattFiles = files.filter(f => f.name.startsWith('F_QM_') || f.name.startsWith('F-QM-'));
    const otherFiles = files.filter(f => !f.name.startsWith('F_QM_') && !f.name.startsWith('F-QM-'));

    let html = '';

    if (formblattFiles.length > 0) {
        html += '<h4>Formblaetter</h4>';
        html += formblattFiles.map(f => renderFileRow(f)).join('');
    }

    if (otherFiles.length > 0) {
        html += '<h4>Sonstige Dokumente</h4>';
        html += otherFiles.map(f => renderFileRow(f)).join('');
    }

    container.innerHTML = html;
}

function renderFileRow(file) {
    const icon = getFileIcon(file.mimeType, file.name);
    const size = formatFileSize(file.size);
    const date = formatDate(file.lastModifiedDateTime);

    return `
        <div class="file-row" onclick="showFilePreview('${file.id}', '${escapeHtml(file.name)}', '${file.webUrl}', '${file.downloadUrl || ''}', '${file.mimeType}')">
            <span class="file-icon">${icon}</span>
            <span class="file-name">${escapeHtml(file.name)}</span>
            <span class="file-meta">${size} • ${date}</span>
        </div>
    `;
}

function getFileIcon(mimeType, filename) {
    if (filename.endsWith('.pdf')) return '📕';
    if (filename.endsWith('.xlsx') || filename.endsWith('.xls')) return '📊';
    if (filename.endsWith('.docx') || filename.endsWith('.doc')) return '📘';
    if (mimeType?.startsWith('image/')) return '🖼️';
    return '📄';
}

function formatFileSize(bytes) {
    if (!bytes) return '';
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function truncateFilename(name, maxLen) {
    if (!name || name.length <= maxLen) return name || '';
    const ext = name.split('.').pop();
    return name.substring(0, maxLen - ext.length - 4) + '...' + ext;
}

// ============================================
// DATEI-VORSCHAU
// ============================================

function showFilePreview(fileId, filename, webUrl, downloadUrl, mimeType) {
    const modal = document.getElementById('file-preview-modal');
    const content = document.getElementById('preview-content');
    if (!modal || !content) return;

    document.getElementById('preview-filename').textContent = filename;
    document.getElementById('preview-download').href = downloadUrl || webUrl;
    document.getElementById('preview-sharepoint').href = webUrl;

    // Vorschau basierend auf Dateityp
    if (mimeType?.startsWith('image/') && downloadUrl) {
        content.innerHTML = `<img src="${downloadUrl}" alt="${escapeHtml(filename)}" style="max-width:100%; max-height:70vh;">`;
    } else if (filename.endsWith('.pdf') && downloadUrl) {
        content.innerHTML = `<iframe src="${downloadUrl}#toolbar=0" style="width:100%; height:70vh; border:none;"></iframe>`;
    } else {
        // Keine Vorschau moeglich
        content.innerHTML = `
            <div class="no-preview">
                <span style="font-size:64px;">${getFileIcon(mimeType, filename)}</span>
                <p>Keine Vorschau verfuegbar</p>
                <p>Klicken Sie auf "Herunterladen" oder "In SharePoint oeffnen"</p>
            </div>
        `;
    }

    modal.style.display = 'flex';
}

function closeFilePreview() {
    const modal = document.getElementById('file-preview-modal');
    if (modal) {
        modal.style.display = 'none';
        document.getElementById('preview-content').innerHTML = '';
    }
}

async function refreshFiles(folder) {
    const qaId = window.currentReklamationData?.reklamation?.QA_ID;
    if (!qaId) return;

    if (folder === 'Fotos') {
        const data = await loadFiles(qaId, 'Fotos');
        renderFotos(data.files || []);
    } else {
        await loadAllFilesForDetail(qaId);
    }
}

// ============================================
// MASSNAHMEN-MANAGEMENT (erweitert mit Templates)
// ============================================

function showMassnahmeModal() {
    // Form zuruecksetzen
    document.getElementById('massnahme-form').reset();

    // Template-Dropdown befuellen
    const templateSelect = document.getElementById('m-template');
    if (typeof MASSNAHMEN_TEMPLATES !== 'undefined') {
        const kategorien = getAllKategorien();
        templateSelect.innerHTML = '<option value="">-- Eigene Massnahme eingeben --</option>';

        kategorien.forEach(kat => {
            const optgroup = document.createElement('optgroup');
            optgroup.label = kat;
            MASSNAHMEN_TEMPLATES.forEach((t, idx) => {
                if (t.kategorie === kat) {
                    const opt = document.createElement('option');
                    opt.value = idx;
                    opt.textContent = t.titel;
                    optgroup.appendChild(opt);
                }
            });
            templateSelect.appendChild(optgroup);
        });
    }

    // Verantwortliche-Dropdown befuellen (dynamisch aus M365)
    populateUserDropdown('m-verantwortlich');

    // Standard-Termin: Morgen
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById('m-termin').value = tomorrow.toISOString().split('T')[0];

    // Modal anzeigen
    document.getElementById('massnahme-modal').style.display = 'flex';
}

function applyMassnahmeTemplate() {
    const idx = document.getElementById('m-template').value;
    if (idx === '' || typeof MASSNAHMEN_TEMPLATES === 'undefined') return;

    const template = MASSNAHMEN_TEMPLATES[parseInt(idx)];
    if (!template) return;

    document.getElementById('m-title').value = template.titel;
    document.getElementById('m-beschreibung').value = template.beschreibung;
    document.getElementById('m-typ').value = template.kategorie === '8D-Report' ? '8D-Report' : template.kategorie;

    // Termin berechnen
    const termin = new Date();
    termin.setDate(termin.getDate() + template.standardTermin);
    document.getElementById('m-termin').value = termin.toISOString().split('T')[0];

    // Verantwortlichen vorbelegen
    if (template.empfohlenerVerantwortlicher) {
        document.getElementById('m-verantwortlich').value = template.empfohlenerVerantwortlicher;
    }
}

function closeMassnahmeModal() {
    document.getElementById('massnahme-modal').style.display = 'none';
}

async function handleMassnahmeSubmit(e) {
    e.preventDefault();
    await createMassnahmeWithNotification();
}

async function createMassnahmeWithNotification() {
    const reklaData = window.currentReklamationData?.reklamation;
    const verantwortlichValue = document.getElementById('m-verantwortlich').value;
    const notifyEmail = document.getElementById('notify-email')?.checked || false;
    const notifyTeams = document.getElementById('notify-teams')?.checked || false;

    // Verantwortlichen aus m365Users finden
    const verantwortlicher = m365Users.find(u =>
        u.mail === verantwortlichValue ||
        u.kuerzel === verantwortlichValue ||
        u.id === verantwortlichValue
    );

    const massnahmeData = {
        reklaId: window.currentReklamationId,
        title: document.getElementById('m-title').value,
        typ: document.getElementById('m-typ').value,
        termin: document.getElementById('m-termin').value,
        beschreibung: document.getElementById('m-beschreibung')?.value || '',
        verantwortlich: verantwortlicher?.displayName || verantwortlichValue
    };

    try {
        showLoading(true);

        // 1. Massnahme in SharePoint erstellen
        await createMassnahme(massnahmeData);

        // 2. Benachrichtigung senden (wenn aktiviert)
        if ((notifyEmail || notifyTeams) && verantwortlicher) {
            try {
                await fetch('/api/rms/notify-massnahme', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        qaId: reklaData?.QA_ID || 'Unbekannt',
                        reklaTitle: reklaData?.Title || 'Unbekannt',
                        massnahme: {
                            title: massnahmeData.title,
                            typ: massnahmeData.typ,
                            termin: massnahmeData.termin,
                            beschreibung: massnahmeData.beschreibung
                        },
                        verantwortlich: {
                            id: verantwortlicher.id,
                            name: verantwortlicher.displayName,
                            email: verantwortlicher.mail,
                            rolle: verantwortlicher.jobTitle || ''
                        },
                        notifyEmail: notifyEmail,
                        notifyTeams: notifyTeams,
                        ersteller: 'AL',
                        dashboardUrl: window.location.href
                    })
                });
            } catch (notifyError) {
                console.warn('Benachrichtigung konnte nicht gesendet werden:', notifyError);
            }
        }

        closeMassnahmeModal();
        await showDetail(window.currentReklamationId);

        let notifyMsg = '';
        if (notifyEmail && notifyTeams) notifyMsg = ' E-Mail + Teams Benachrichtigung gesendet.';
        else if (notifyEmail) notifyMsg = ' E-Mail Benachrichtigung gesendet.';
        else if (notifyTeams) notifyMsg = ' Teams Benachrichtigung gesendet.';

        alert('Massnahme erfolgreich erstellt!' + notifyMsg);

    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Erstellen der Massnahme: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// ============================================
// TRACKING (Ersatz/Ruecksendung/Gutschrift)
// ============================================

function showTrackingSection(rekla) {
    const trackingSection = document.getElementById('tracking-section');
    if (!trackingSection) return;

    // Nur fuer Lieferanten-Reklamationen anzeigen
    if (rekla.Rekla_Typ === 'Lieferant' || rekla.Rekla_Typ === 'LIEFERANT') {
        trackingSection.style.display = 'block';

        // Tracking-Werte aus Reklamation laden
        document.getElementById('tracking-ersatz').checked = rekla.Tracking_Ersatzlieferung || false;
        document.getElementById('tracking-ruecksendung').checked = rekla.Tracking_Ruecksendung || false;
        document.getElementById('tracking-gutschrift').checked = rekla.Tracking_Gutschrift || false;
        document.getElementById('tracking-gutschrift-betrag').value = rekla.Tracking_Gutschrift_Betrag || '';
        document.getElementById('tracking-bemerkung').value = rekla.Tracking_Bemerkung || '';

        // Gutschrift-Betrag-Feld anzeigen wenn Gutschrift aktiviert
        updateTrackingVisibility();
    } else {
        trackingSection.style.display = 'none';
    }
}

function updateTrackingVisibility() {
    const gutschriftChecked = document.getElementById('tracking-gutschrift')?.checked;
    const betragContainer = document.getElementById('gutschrift-betrag-container');
    if (betragContainer) {
        betragContainer.style.display = gutschriftChecked ? 'block' : 'none';
    }
}

async function saveTracking() {
    const id = window.currentReklamationId;
    if (!id) {
        alert('Keine Reklamation ausgewaehlt');
        return;
    }

    const ersatz = document.getElementById('tracking-ersatz')?.checked || false;
    const ruecksendung = document.getElementById('tracking-ruecksendung')?.checked || false;
    const gutschrift = document.getElementById('tracking-gutschrift')?.checked || false;
    const betrag = parseFloat(document.getElementById('tracking-gutschrift-betrag')?.value) || null;
    const bemerkung = document.getElementById('tracking-bemerkung')?.value || '';

    // Tracking-Status ermitteln
    let trackingStatus = 'Offen';
    if (ersatz) trackingStatus = 'Ersatzlieferung angefordert';
    else if (ruecksendung) trackingStatus = 'Ruecksendung';
    else if (gutschrift) trackingStatus = 'Gutschrift angefordert';

    const fields = {
        Tracking_Status: trackingStatus,
        Tracking_Ersatzlieferung: ersatz,
        Tracking_Ruecksendung: ruecksendung,
        Tracking_Gutschrift: gutschrift,
        Tracking_Gutschrift_Betrag: betrag,
        Tracking_Bemerkung: bemerkung
    };

    try {
        showLoading(true);

        const response = await fetch('/api/rms/update', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id, fields })
        });

        const result = await response.json();

        if (response.ok && (result.success || result.id || result['@odata.etag'])) {
            alert('Tracking gespeichert!');
            // Detail-View aktualisieren
            await showDetail(id);
        } else {
            alert('Fehler: ' + (result.error || result.message || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('Tracking speichern fehlgeschlagen:', error);
        alert('Fehler: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// ============================================
// E-MAIL VORLAGEN & VERSAND
// ============================================

const EMAIL_TEMPLATES = {
    eingangsbestaetigung: {
        betreff: 'Eingangsbestaetigung Ihrer Reklamation {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

wir bestaetigen den Eingang Ihrer Reklamation und haben diese unter der Nummer {QA_ID} erfasst.

Betreff: {TITEL}

Wir werden die Angelegenheit pruefen und uns schnellstmoeglich bei Ihnen melden.

Mit freundlichen Gruessen
Qualitaetsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    },
    nachfrage: {
        betreff: 'Rueckfrage zu Ihrer Reklamation {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

bezugnehmend auf Ihre Reklamation {QA_ID} bitten wir um folgende Informationen:

[Bitte ergaenzen Sie hier Ihre Fragen]

Vielen Dank fuer Ihre Unterstuetzung.

Mit freundlichen Gruessen
Qualitaetsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    },
    ersatzlieferung: {
        betreff: 'Anforderung Ersatzlieferung zu {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

bezugnehmend auf unsere Reklamation {QA_ID} bitten wir um schnellstmoegliche Ersatzlieferung.

Betroffener Artikel: {ARTIKEL}
Menge: {MENGE}

Bitte bestaetigen Sie den Liefertermin.

Mit freundlichen Gruessen
Qualitaetsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    },
    gutschrift: {
        betreff: 'Anforderung Gutschrift zu {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

bezugnehmend auf unsere Reklamation {QA_ID} bitten wir um Ausstellung einer Gutschrift.

Begruendung:
{BESCHREIBUNG}

Mit freundlichen Gruessen
Qualitaetsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    },
    ruecksendung: {
        betreff: 'Ankuendigung Ruecksendung zu {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

bezugnehmend auf unsere Reklamation {QA_ID} moechten wir die betroffene Ware zuruecksenden.

Bitte teilen Sie uns mit:
- Ihre Ruecksende-Adresse
- Eine Referenznummer fuer die Sendung
- Ob Sie einen Abholtermin vereinbaren moechten

Mit freundlichen Gruessen
Qualitaetsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    },
    abschluss: {
        betreff: 'Abschluss Reklamation {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

wir moechten Ihnen mitteilen, dass die Reklamation {QA_ID} abgeschlossen wurde.

{BESCHREIBUNG}

Vielen Dank fuer Ihre Zusammenarbeit.

Mit freundlichen Gruessen
Qualitaetsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    }
};

function showAntwortEmailModal() {
    const modal = document.getElementById('modal-antwort-email');
    if (!modal) return;

    const rekla = window.currentReklamationData?.reklamation;
    if (!rekla) {
        alert('Keine Reklamation ausgewaehlt');
        return;
    }

    // Felder vorbelegen
    document.getElementById('email-betreff').value = `Re: ${rekla.QA_ID} - ${rekla.Title}`;
    document.getElementById('email-empfaenger').value = rekla.Absender_Email || '';
    document.getElementById('email-text').value = '';
    document.getElementById('email-vorlage').value = '';
    document.getElementById('email-anhang-formular').checked = false;

    modal.style.display = 'flex';
}

function closeAntwortEmailModal() {
    const modal = document.getElementById('modal-antwort-email');
    if (modal) modal.style.display = 'none';
}

function applyEmailTemplate() {
    const templateKey = document.getElementById('email-vorlage')?.value;
    if (!templateKey || !EMAIL_TEMPLATES[templateKey]) return;

    const template = EMAIL_TEMPLATES[templateKey];
    const rekla = window.currentReklamationData?.reklamation || {};

    // Platzhalter ersetzen
    let betreff = template.betreff
        .replace(/{QA_ID}/g, rekla.QA_ID || '')
        .replace(/{TITEL}/g, rekla.Title || '');

    let text = template.text
        .replace(/{QA_ID}/g, rekla.QA_ID || '')
        .replace(/{TITEL}/g, rekla.Title || '')
        .replace(/{BESCHREIBUNG}/g, rekla.Beschreibung || '')
        .replace(/{ARTIKEL}/g, rekla.Artikel_Nr || '[Artikelnummer]')
        .replace(/{MENGE}/g, rekla.Beanstandete_Menge || '[Menge]');

    document.getElementById('email-betreff').value = betreff;
    document.getElementById('email-text').value = text;
}

async function sendAntwortEmail() {
    const empfaenger = document.getElementById('email-empfaenger')?.value?.trim();
    const betreff = document.getElementById('email-betreff')?.value?.trim();
    const text = document.getElementById('email-text')?.value?.trim();
    const anhangFormular = document.getElementById('email-anhang-formular')?.checked;

    if (!empfaenger || !betreff || !text) {
        alert('Bitte alle Pflichtfelder ausfuellen');
        return;
    }

    // E-Mail-Validierung
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(empfaenger)) {
        alert('Bitte eine gueltige E-Mail-Adresse eingeben');
        return;
    }

    const payload = {
        qaId: window.currentReklamationData?.reklamation?.QA_ID,
        reklamationId: window.currentReklamationId,
        empfaenger: empfaenger,
        betreff: betreff,
        text: text,
        anhangFormular: anhangFormular
    };

    try {
        showLoading(true);

        const response = await fetch('/api/rms/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            alert('E-Mail erfolgreich gesendet!');
            closeAntwortEmailModal();
            // Detail-View aktualisieren (Schriftverkehr)
            await showDetail(window.currentReklamationId);
        } else {
            alert('Fehler: ' + (result.error || result.message || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('E-Mail senden fehlgeschlagen:', error);
        alert('Fehler: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// ============================================
// NEUE REKLAMATION ERFASSEN
// ============================================

function showNeueReklamationModal() {
    const modal = document.getElementById('modal-neue-rekla');
    if (modal) {
        modal.style.display = 'flex';
        // Verantwortlich-Dropdown befuellen
        populateUserDropdown('neue-rekla-verantwortlich');
        // Formular zuruecksetzen
        document.getElementById('form-neue-rekla')?.reset();
        // Lieferant-Felder ausblenden
        document.getElementById('lieferant-fields').style.display = 'none';
        // Stammdaten-Datalist befuellen (alle)
        populateNeueReklaStammdaten();
    }
}

function closeNeueReklamationModal() {
    const modal = document.getElementById('modal-neue-rekla');
    if (modal) modal.style.display = 'none';
}

function toggleReklaFields() {
    const typ = document.getElementById('neue-rekla-typ')?.value;
    const lieferantFields = document.getElementById('lieferant-fields');

    if (lieferantFields) {
        lieferantFields.style.display = typ === 'Lieferant' ? 'block' : 'none';
    }

    // Stammdaten-Filter aktualisieren
    populateNeueReklaStammdaten(typ);
}

function populateNeueReklaStammdaten(typ = '') {
    const datalist = document.getElementById('neue-rekla-stammdaten');
    const input = document.getElementById('neue-rekla-absender');
    if (!datalist) return;

    // Aus Cache filtern (falls Stammdaten geladen)
    let filtered = [];
    if (typ === 'Kunde') {
        filtered = stammdatenCache.kunden || [];
    } else if (typ === 'Lieferant') {
        filtered = stammdatenCache.lieferanten || [];
    } else {
        filtered = stammdatenCache.alle || [];
    }

    // Datalist mit Name UND DebKredNr als Suchoptionen
    let options = [];
    filtered.forEach(s => {
        options.push(`<option value="${escapeHtml(s.name)}" data-debkred="${s.debKredNr}">${s.debKredNr || ''} - ${escapeHtml(s.name)}</option>`);
        if (s.debKredNr) {
            options.push(`<option value="${s.debKredNr}" data-name="${escapeHtml(s.name)}">${s.debKredNr} - ${escapeHtml(s.name)}</option>`);
        }
    });
    datalist.innerHTML = options.join('');

    // Event-Listener fuer Autocomplete
    if (input && !input.dataset.listenerAdded) {
        input.addEventListener('change', handleNeueReklaAbsenderChange);
        input.dataset.listenerAdded = 'true';
    }
}

function handleNeueReklaAbsenderChange(e) {
    const value = e.target.value;
    const typ = document.getElementById('neue-rekla-typ')?.value;
    let stammdaten = stammdatenCache.alle;
    if (typ === 'Kunde') stammdaten = stammdatenCache.kunden;
    else if (typ === 'Lieferant') stammdaten = stammdatenCache.lieferanten;

    const selected = stammdaten.find(s => s.name === value || s.debKredNr === value);
    if (selected) {
        // Wenn DebKredNr eingegeben wurde, setze den Namen ins Feld
        if (selected.debKredNr === value) {
            document.getElementById('neue-rekla-absender').value = selected.name;
        }
        // DebKredNr-Feld fuellen
        document.getElementById('neue-rekla-debkred').value = selected.debKredNr || '';
        document.getElementById('neue-rekla-absender-id').value = selected.id || '';
    }
}

async function createNeueReklamation(e) {
    e.preventDefault();

    const verantwortlichSelect = document.getElementById('neue-rekla-verantwortlich');
    const verantwortlichOption = verantwortlichSelect?.selectedOptions[0];

    const payload = {
        Rekla_Typ: document.getElementById('neue-rekla-typ')?.value,
        Absender: document.getElementById('neue-rekla-absender')?.value,
        DebKredNr: document.getElementById('neue-rekla-debkred')?.value,
        Title: document.getElementById('neue-rekla-titel')?.value,
        Beschreibung: document.getElementById('neue-rekla-beschreibung')?.value,
        Prioritaet: document.getElementById('neue-rekla-prioritaet')?.value || 'mittel',
        Verantwortlich: verantwortlichOption?.dataset?.displayName || verantwortlichSelect?.value || '',
        Rekla_Status: 'Neu',
        Erfassungsdatum: new Date().toISOString().split('T')[0]
    };

    // Lieferanten-Felder hinzufuegen falls vorhanden
    if (payload.Rekla_Typ === 'Lieferant') {
        const lieferschein = document.getElementById('neue-rekla-lieferschein')?.value;
        const lieferdatum = document.getElementById('neue-rekla-lieferdatum')?.value;
        const artikel = document.getElementById('neue-rekla-artikel')?.value;
        const menge = document.getElementById('neue-rekla-menge')?.value;

        if (lieferschein) payload.Lieferschein_Nr = lieferschein;
        if (lieferdatum) payload.Lieferdatum = lieferdatum;
        if (artikel) payload.Artikel_Nr = artikel;
        if (menge) payload.Beanstandete_Menge = parseInt(menge);
    }

    try {
        showLoading(true);

        const response = await fetch('/api/rms/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok && (result.success || result.qaId || result.QA_ID)) {
            const qaId = result.qaId || result.QA_ID || 'Unbekannt';
            alert(`Reklamation ${qaId} erfolgreich angelegt!`);
            closeNeueReklamationModal();
            await loadData(); // Dashboard aktualisieren
        } else {
            alert('Fehler: ' + (result.error || result.message || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('Reklamation erstellen fehlgeschlagen:', error);
        alert('Fehler: ' + error.message);
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

    // Verantwortlich-Dropdown dynamisch befuellen
    populateUserDropdown('edit-verantwortlich', data.Verantwortlich || '');

    // Felder befuellen
    document.getElementById('edit-typ').value = data.Rekla_Typ || 'Kunde';
    document.getElementById('edit-status').value = data.Rekla_Status || 'Neu';
    document.getElementById('edit-prioritaet').value = (data.Prioritaet || 'mittel').toLowerCase();
    document.getElementById('edit-kst').value = data.KST || '';
    // edit-verantwortlich wird oben durch populateUserDropdown befuellt
    document.getElementById('edit-zieldatum').value = data.Zieldatum?.split('T')[0] || '';
    document.getElementById('edit-title').value = data.Title || '';
    document.getElementById('edit-beschreibung').value = data.Beschreibung || '';

    // Absender-Autocomplete basierend auf Typ initialisieren
    const typ = data.Rekla_Typ || 'Kunde';
    setupStammdatenAutocomplete('edit-absender', 'absender-datalist', typ);
    document.getElementById('edit-absender').value = data.Absender || '';
    document.getElementById('edit-absender-nr').value = data.DebKredNr || '';

    // Bei Typ-Aenderung Autocomplete neu laden
    document.getElementById('edit-typ').onchange = function() {
        setupStammdatenAutocomplete('edit-absender', 'absender-datalist', this.value);
    };
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
        Beschreibung: document.getElementById('edit-beschreibung').value,
        Absender: document.getElementById('edit-absender').value,
        DebKredNr: document.getElementById('edit-absender-nr')?.value || ''
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

        // SharePoint gibt das aktualisierte Item zurueck (mit id) oder success:true
        if (response.ok && (result.success || result.id || result['@odata.etag'])) {
            alert('Reklamation gespeichert!');
            toggleEditMode();
            // Detail-View neu laden
            await showDetail(id);
            // Tabelle aktualisieren
            await loadData();
        } else {
            alert('Fehler: ' + (result.error || result.message || 'Unbekannter Fehler'));
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

    // M365-Benutzer laden BEVOR andere Initialisierung
    await loadM365Users();

    // Stammdaten laden (Kunden/Lieferanten fuer Autocomplete)
    await loadStammdaten();

    // Event-Listener fuer Filter
    document.getElementById('filter-typ')?.addEventListener('change', applyFilters);
    document.getElementById('filter-status')?.addEventListener('change', applyFilters);

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

    // CSV-Export entfernt (Aufgabe 5)

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

    // Neue Reklamation Form
    document.getElementById('form-neue-rekla')?.addEventListener('submit', createNeueReklamation);

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
