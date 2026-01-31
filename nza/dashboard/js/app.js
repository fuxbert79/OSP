/**
 * NZA Dashboard - Main Application
 * Schneider Kabelsatzbau GmbH & Co. KG
 */

// API Base URL
const API_BASE = '/api/nza';

// Minutensätze für Kostenberechnung
const MINUTENSATZ = {
    '1000': 1.98,
    '2000': 1.21,
    '3000': 0.93,
    '4000': 1.02,
    '5000': 1.02,
    'Lager': 1.10,
    'Verwaltung': 1.37,
    'Lieferant': 0,
    'keine Zuordnung': 0
};

// State
let nzaData = [];
let mitarbeiterData = [];
let currentPage = 1;
let itemsPerPage = 20;
let currentNzaId = null;
let prozessCount = 1;

// ==================== Initialization ====================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    // Set default date
    document.getElementById('create-datum').valueAsDate = new Date();

    // Load data
    await Promise.all([
        loadMitarbeiter(),
        loadNzaData()
    ]);

    // Setup event listeners
    setupEventListeners();

    // Initialize charts
    if (typeof initCharts === 'function') {
        initCharts(nzaData);
    }
}

// ==================== Data Loading ====================

async function loadNzaData() {
    try {
        const response = await fetch(`${API_BASE}/prozesse`);
        if (!response.ok) throw new Error('API nicht erreichbar');

        const data = await response.json();
        nzaData = data.items || data || [];

        updateKPIs();
        renderTable();
        updateTableCount();
    } catch (error) {
        console.error('Fehler beim Laden der NZA-Daten:', error);
        showToast('Fehler beim Laden der Daten', 'error');

        // Demo-Daten für Entwicklung
        nzaData = getDemoData();
        updateKPIs();
        renderTable();
        updateTableCount();
    }
}

async function loadMitarbeiter() {
    try {
        const response = await fetch(`${API_BASE}/mitarbeiter`);
        if (!response.ok) throw new Error('Mitarbeiter-API nicht erreichbar');

        const data = await response.json();
        mitarbeiterData = data.mitarbeiter || data || [];

        populateMitarbeiterDropdowns();
    } catch (error) {
        console.error('Fehler beim Laden der Mitarbeiter:', error);

        // Fallback Demo-Daten
        mitarbeiterData = [
            { kuerzel: 'MD', name: 'Dützer, Marcel', kst: '1000' },
            { kuerzel: 'DS', name: 'Schwarz, David', kst: '1000' },
            { kuerzel: 'BS', name: 'Stieber, Bettina', kst: '2000/3000' },
            { kuerzel: 'SK', name: 'Kandorfer, Stefan', kst: '5000' },
            { kuerzel: 'DR', name: 'Reuber, Daniela', kst: '5000' },
            { kuerzel: 'OK', name: 'Kuh, Olaf', kst: 'Lager' }
        ];
        populateMitarbeiterDropdowns();
    }
}

function populateMitarbeiterDropdowns() {
    const dropdowns = document.querySelectorAll('#create-verursacher, .prozess-werker');

    dropdowns.forEach(dropdown => {
        const currentValue = dropdown.value;
        dropdown.innerHTML = '<option value="">-- Auswählen --</option>';

        mitarbeiterData.forEach(ma => {
            const option = document.createElement('option');
            option.value = ma.kuerzel;
            option.textContent = `${ma.kuerzel} - ${ma.name}`;
            dropdown.appendChild(option);
        });

        dropdown.value = currentValue;
    });
}

// ==================== Event Listeners ====================

function setupEventListeners() {
    // Search
    document.getElementById('search-input').addEventListener('input', debounce(filterAndRender, 300));

    // Filters
    ['filter-typ', 'filter-status', 'filter-kst', 'filter-zeitraum'].forEach(id => {
        document.getElementById(id).addEventListener('change', filterAndRender);
    });

    // Form submission
    document.getElementById('form-create-nza').addEventListener('submit', handleCreateNza);

    // Kosten inputs
    document.getElementById('create-kosten-material').addEventListener('input', updateKostenSumme);
    document.getElementById('create-kosten-sonstige').addEventListener('input', updateKostenSumme);

    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tabId = e.target.dataset.tab;
            switchTab(tabId);
        });
    });

    // Table sorting
    document.querySelectorAll('th[data-sort]').forEach(th => {
        th.addEventListener('click', () => sortTable(th.dataset.sort));
    });

    // Escape key to close modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeCreateModal();
            closeDetailModal();
            closeLightbox();
        }
    });
}

// ==================== KPIs ====================

function updateKPIs() {
    const now = new Date();
    const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
    const yearStart = new Date(now.getFullYear(), 0, 1);

    // Offene NZA
    const offene = nzaData.filter(n => n.status !== 'Abgeschlossen').length;
    document.getElementById('kpi-offen').textContent = offene;

    // Kosten MTD
    const kostenMtd = nzaData
        .filter(n => new Date(n.datum) >= monthStart)
        .reduce((sum, n) => sum + (n.kostenGesamt || 0), 0);
    document.getElementById('kpi-kosten-mtd').textContent = formatCurrency(kostenMtd);

    // Kosten YTD
    const kostenYtd = nzaData
        .filter(n => new Date(n.datum) >= yearStart)
        .reduce((sum, n) => sum + (n.kostenGesamt || 0), 0);
    document.getElementById('kpi-kosten-ytd').textContent = formatCurrency(kostenYtd);

    // Durchschnittliche Bearbeitungszeit
    const abgeschlossen = nzaData.filter(n => n.status === 'Abgeschlossen' && n.abschlussDatum);
    if (abgeschlossen.length > 0) {
        const avgDays = abgeschlossen.reduce((sum, n) => {
            const start = new Date(n.datum);
            const end = new Date(n.abschlussDatum);
            return sum + Math.ceil((end - start) / (1000 * 60 * 60 * 24));
        }, 0) / abgeschlossen.length;
        document.getElementById('kpi-bearbeitungszeit').textContent = `${Math.round(avgDays)} Tage`;
    } else {
        document.getElementById('kpi-bearbeitungszeit').textContent = '-';
    }
}

// ==================== Table ====================

function renderTable() {
    const tbody = document.getElementById('nza-table-body');
    const filtered = getFilteredData();
    const paginated = paginate(filtered, currentPage, itemsPerPage);

    if (paginated.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" class="loading-row">Keine Einträge gefunden</td></tr>';
        return;
    }

    tbody.innerHTML = paginated.map(nza => `
        <tr onclick="openDetailModal('${nza.nzaId}')" style="cursor: pointer;">
            <td><strong>${nza.nzaId}</strong></td>
            <td>${formatDate(nza.datum)}</td>
            <td>${nza.typ || '-'}</td>
            <td>${nza.artikel || '-'}</td>
            <td>${nza.verursacher || '-'}</td>
            <td>${nza.kst || '-'}</td>
            <td>${(nza.kategorien || []).slice(0, 2).join(', ')}${(nza.kategorien || []).length > 2 ? '...' : ''}</td>
            <td>${formatCurrency(nza.kostenGesamt || 0)}</td>
            <td><span class="status-badge status-${getStatusClass(nza.status)}">${nza.status || 'Neu'}</span></td>
            <td>
                <button class="btn btn-sm btn-secondary" onclick="event.stopPropagation(); editNza('${nza.nzaId}')">Bearbeiten</button>
            </td>
        </tr>
    `).join('');

    renderPagination(filtered.length);
}

function getFilteredData() {
    const search = document.getElementById('search-input').value.toLowerCase();
    const typ = document.getElementById('filter-typ').value;
    const status = document.getElementById('filter-status').value;
    const kst = document.getElementById('filter-kst').value;
    const zeitraum = document.getElementById('filter-zeitraum').value;

    return nzaData.filter(nza => {
        // Search
        if (search && !matchesSearch(nza, search)) return false;

        // Typ
        if (typ && nza.typ !== typ) return false;

        // Status
        if (status && nza.status !== status) return false;

        // KST
        if (kst && nza.kst !== kst) return false;

        // Zeitraum
        if (zeitraum !== 'alle' && !matchesZeitraum(nza.datum, zeitraum)) return false;

        return true;
    });
}

function matchesSearch(nza, search) {
    const searchFields = [nza.nzaId, nza.artikel, nza.beschreibung, nza.verursacher].join(' ').toLowerCase();
    return searchFields.includes(search);
}

function matchesZeitraum(datum, zeitraum) {
    const date = new Date(datum);
    const now = new Date();

    switch (zeitraum) {
        case 'heute':
            return date.toDateString() === now.toDateString();
        case 'woche':
            const weekStart = new Date(now);
            weekStart.setDate(now.getDate() - now.getDay());
            return date >= weekStart;
        case 'monat':
            return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear();
        case 'jahr':
            return date.getFullYear() === now.getFullYear();
        default:
            return true;
    }
}

function filterAndRender() {
    currentPage = 1;
    renderTable();
    updateTableCount();
}

function updateTableCount() {
    const count = getFilteredData().length;
    document.getElementById('table-count').textContent = `${count} Einträge`;
}

function sortTable(field) {
    nzaData.sort((a, b) => {
        const valA = a[field] || '';
        const valB = b[field] || '';

        if (typeof valA === 'number') return valB - valA;
        return valA.toString().localeCompare(valB.toString());
    });

    renderTable();
}

// ==================== Pagination ====================

function paginate(data, page, perPage) {
    const start = (page - 1) * perPage;
    return data.slice(start, start + perPage);
}

function renderPagination(total) {
    const totalPages = Math.ceil(total / itemsPerPage);
    const pagination = document.getElementById('pagination');

    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let html = '';

    if (currentPage > 1) {
        html += `<button onclick="goToPage(${currentPage - 1})">«</button>`;
    }

    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            html += `<button class="${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            html += '<span>...</span>';
        }
    }

    if (currentPage < totalPages) {
        html += `<button onclick="goToPage(${currentPage + 1})">»</button>`;
    }

    pagination.innerHTML = html;
}

function goToPage(page) {
    currentPage = page;
    renderTable();
}

// ==================== Create Modal ====================

function openCreateModal() {
    document.getElementById('modal-create').classList.add('active');
    prozessCount = 1;
}

function closeCreateModal() {
    document.getElementById('modal-create').classList.remove('active');
    document.getElementById('form-create-nza').reset();
    document.getElementById('create-datum').valueAsDate = new Date();

    // Reset Prozess-Rows
    const container = document.getElementById('prozesse-container');
    container.innerHTML = `
        <div class="prozess-row" data-prozess="1">
            <input type="text" placeholder="Prozess (z.B. Nachcrimpen)" class="prozess-name">
            <select class="prozess-werker"><option value="">Werker</option></select>
            <select class="prozess-kst">
                <option value="">KST</option>
                <option value="1000">1000</option>
                <option value="2000">2000</option>
                <option value="3000">3000</option>
                <option value="4000">4000</option>
                <option value="5000">5000</option>
                <option value="Lager">Lager</option>
            </select>
            <input type="number" placeholder="Min" class="prozess-zeit" min="0">
            <span class="prozess-kosten">0,00 €</span>
        </div>
    `;
    prozessCount = 1;
    populateMitarbeiterDropdowns();
    updateKostenSumme();
}

function addProzessRow() {
    if (prozessCount >= 5) {
        showToast('Maximal 5 Prozesse möglich', 'error');
        return;
    }

    prozessCount++;
    const container = document.getElementById('prozesse-container');

    const row = document.createElement('div');
    row.className = 'prozess-row';
    row.dataset.prozess = prozessCount;
    row.innerHTML = `
        <input type="text" placeholder="Prozess" class="prozess-name">
        <select class="prozess-werker"><option value="">Werker</option></select>
        <select class="prozess-kst">
            <option value="">KST</option>
            <option value="1000">1000</option>
            <option value="2000">2000</option>
            <option value="3000">3000</option>
            <option value="4000">4000</option>
            <option value="5000">5000</option>
            <option value="Lager">Lager</option>
        </select>
        <input type="number" placeholder="Min" class="prozess-zeit" min="0">
        <span class="prozess-kosten">0,00 €</span>
    `;

    container.appendChild(row);
    populateMitarbeiterDropdowns();

    // Add event listener for cost calculation
    row.querySelector('.prozess-zeit').addEventListener('input', updateKostenSumme);
    row.querySelector('.prozess-kst').addEventListener('change', updateKostenSumme);
}

function updateKostenSumme() {
    let kostenProzesse = 0;

    document.querySelectorAll('.prozess-row').forEach(row => {
        const zeit = parseFloat(row.querySelector('.prozess-zeit').value) || 0;
        const kst = row.querySelector('.prozess-kst').value;
        const faktor = MINUTENSATZ[kst] || 0;
        const kosten = zeit * faktor;

        row.querySelector('.prozess-kosten').textContent = formatCurrency(kosten);
        kostenProzesse += kosten;
    });

    const kostenMaterial = parseFloat(document.getElementById('create-kosten-material').value) || 0;
    const kostenSonstige = parseFloat(document.getElementById('create-kosten-sonstige').value) || 0;
    const kostenGesamt = kostenProzesse + kostenMaterial + kostenSonstige;

    document.getElementById('summe-prozesse').textContent = formatCurrency(kostenProzesse);
    document.getElementById('summe-gesamt').textContent = formatCurrency(kostenGesamt);
}

async function handleCreateNza(e) {
    e.preventDefault();

    // Collect kategorien
    const kategorien = [];
    document.querySelectorAll('#create-kategorien input:checked').forEach(cb => {
        kategorien.push(cb.value);
    });

    if (kategorien.length === 0) {
        showToast('Mindestens eine Fehler-Kategorie auswählen', 'error');
        return;
    }

    // Collect prozesse
    const prozesse = [];
    document.querySelectorAll('.prozess-row').forEach(row => {
        const name = row.querySelector('.prozess-name').value;
        const zeit = parseFloat(row.querySelector('.prozess-zeit').value) || 0;

        if (name && zeit > 0) {
            prozesse.push({
                prozess: name,
                werker: row.querySelector('.prozess-werker').value,
                kst: row.querySelector('.prozess-kst').value,
                zeit: zeit
            });
        }
    });

    const payload = {
        typ: document.getElementById('create-typ').value,
        datum: document.getElementById('create-datum').value,
        artikel: document.getElementById('create-artikel').value,
        betriebsauftrag: document.getElementById('create-ba').value || null,
        verursacher: document.getElementById('create-verursacher').value,
        kst: document.getElementById('create-kst').value,
        beschreibung: document.getElementById('create-beschreibung').value,
        kategorien: kategorien,
        prozesse: prozesse,
        kostenMaterial: parseFloat(document.getElementById('create-kosten-material').value) || 0,
        kostenSonstige: parseFloat(document.getElementById('create-kosten-sonstige').value) || 0
    };

    try {
        const response = await fetch(`${API_BASE}/prozesse`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Fehler beim Erstellen');

        const result = await response.json();
        showToast(`NZA ${result.nzaId} erfolgreich angelegt`, 'success');
        closeCreateModal();
        await loadNzaData();
    } catch (error) {
        console.error('Fehler:', error);
        showToast('Fehler beim Anlegen der NZA', 'error');
    }
}

// ==================== Detail Modal ====================

async function openDetailModal(nzaId) {
    currentNzaId = nzaId;
    const nza = nzaData.find(n => n.nzaId === nzaId);

    if (!nza) {
        showToast('NZA nicht gefunden', 'error');
        return;
    }

    document.getElementById('detail-title').textContent = nzaId;
    document.getElementById('modal-detail').classList.add('active');

    // Render Übersicht Tab
    renderUebersichtTab(nza);

    // Switch to first tab
    switchTab('uebersicht');
}

function closeDetailModal() {
    document.getElementById('modal-detail').classList.remove('active');
    currentNzaId = null;
}

function renderUebersichtTab(nza) {
    const tab = document.getElementById('tab-uebersicht');

    tab.innerHTML = `
        <div class="detail-grid">
            <div class="detail-section">
                <h4>Stammdaten</h4>
                <table class="detail-table">
                    <tr><th>NZA-ID</th><td>${nza.nzaId}</td></tr>
                    <tr><th>Typ</th><td>${nza.typ}</td></tr>
                    <tr><th>Datum</th><td>${formatDate(nza.datum)}</td></tr>
                    <tr><th>Artikel</th><td>${nza.artikel || '-'}</td></tr>
                    <tr><th>Verursacher</th><td>${nza.verursacher || '-'}</td></tr>
                    <tr><th>Kostenstelle</th><td>${nza.kst || '-'}</td></tr>
                    <tr><th>Status</th><td><span class="status-badge status-${getStatusClass(nza.status)}">${nza.status || 'Neu'}</span></td></tr>
                </table>
            </div>
            <div class="detail-section">
                <h4>Kosten</h4>
                <div class="kosten-summary">
                    <div class="kosten-item">
                        <span class="kosten-label">Prozesskosten</span>
                        <span class="kosten-value">${formatCurrency(nza.kostenProzesse || 0)}</span>
                    </div>
                    <div class="kosten-item">
                        <span class="kosten-label">Materialkosten</span>
                        <span class="kosten-value">${formatCurrency(nza.kostenMaterial || 0)}</span>
                    </div>
                    <div class="kosten-item">
                        <span class="kosten-label">Sonstige</span>
                        <span class="kosten-value">${formatCurrency(nza.kostenSonstige || 0)}</span>
                    </div>
                    <div class="kosten-item kosten-total">
                        <span class="kosten-label">Gesamt</span>
                        <span class="kosten-value">${formatCurrency(nza.kostenGesamt || 0)}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="detail-section full-width">
            <h4>Fehlerbeschreibung</h4>
            <p>${nza.beschreibung || '-'}</p>
        </div>
        <div class="detail-section full-width">
            <h4>Kategorien</h4>
            <div class="tags">
                ${(nza.kategorien || []).map(k => `<span class="tag">${k}</span>`).join('')}
            </div>
        </div>
    `;
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabId);
    });

    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `tab-${tabId}`);
    });
}

// ==================== Bilder ====================

function openBildUpload() {
    // TODO: Implementieren
    showToast('Bilder-Upload wird implementiert', 'info');
}

function closeLightbox() {
    document.getElementById('lightbox').style.display = 'none';
}

// ==================== Maßnahmen ====================

function openMassnahmeModal() {
    // TODO: Implementieren
    showToast('Maßnahmen-Modal wird implementiert', 'info');
}

// ==================== Utilities ====================

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('de-DE');
}

function formatCurrency(value) {
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR'
    }).format(value || 0);
}

function getStatusClass(status) {
    switch (status) {
        case 'Neu': return 'neu';
        case 'In Bearbeitung': return 'bearbeitung';
        case 'Abgeschlossen': return 'abgeschlossen';
        default: return 'neu';
    }
}

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => toast.remove(), 3000);
}

function editNza(nzaId) {
    openDetailModal(nzaId);
}

// ==================== Demo Data ====================

function getDemoData() {
    return [
        {
            nzaId: 'NZA-26-0001',
            typ: 'Interne Reklamation',
            datum: '2026-01-28',
            artikel: 'KB-12345',
            verursacher: 'MD',
            kst: '1000',
            beschreibung: 'Crimpfehler bei 15 Stück, Nacharbeit erforderlich',
            kategorien: ['Crimpfehler'],
            status: 'In Bearbeitung',
            kostenProzesse: 89.10,
            kostenMaterial: 5.50,
            kostenSonstige: 0,
            kostenGesamt: 94.60
        },
        {
            nzaId: 'NZA-26-0002',
            typ: 'Interne Reklamation',
            datum: '2026-01-29',
            artikel: 'KB-67890',
            verursacher: 'DS',
            kst: '1000',
            beschreibung: 'Längenabweichung 5mm zu kurz',
            kategorien: ['Längenabweichung'],
            status: 'Neu',
            kostenProzesse: 0,
            kostenMaterial: 0,
            kostenSonstige: 0,
            kostenGesamt: 0
        },
        {
            nzaId: 'NZA-26-0003',
            typ: 'Kunden Reklamation',
            datum: '2026-01-25',
            artikel: 'KB-11111',
            verursacher: 'BS',
            kst: '2000',
            beschreibung: 'Verdrahtung vertauscht, Kunde reklamiert',
            kategorien: ['Verdrahtungsfehler'],
            status: 'Abgeschlossen',
            abschlussDatum: '2026-01-27',
            kostenProzesse: 145.20,
            kostenMaterial: 12.30,
            kostenSonstige: 0,
            kostenGesamt: 157.50
        }
    ];
}
