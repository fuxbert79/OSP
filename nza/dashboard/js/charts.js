/**
 * NZA Dashboard - Charts (Chart.js)
 * Schneider Kabelsatzbau GmbH & Co. KG
 */

// Chart Instances
let chartTrend = null;
let chartTyp = null;
let chartKst = null;
let chartKosten = null;

// NZA Farben
const COLORS = {
    primary: '#1565C0',
    primaryLight: '#1976D2',
    accent: '#2196F3',
    success: '#4CAF50',
    warning: '#FF9800',
    danger: '#F44336',
    neutral: '#9E9E9E'
};

const KST_COLORS = {
    '1000': '#1565C0',
    '2000': '#2E7D32',
    '3000': '#F57C00',
    '4000': '#7B1FA2',
    '5000': '#C62828',
    'Lager': '#00838F',
    'Verwaltung': '#455A64'
};

const TYP_COLORS = {
    'Interne Reklamation': COLORS.primary,
    'Kunden Reklamation': COLORS.warning,
    'Lieferanten Reklamation': COLORS.danger
};

/**
 * Initialize all charts
 */
function initCharts(data) {
    if (!data || data.length === 0) {
        console.log('Keine Daten für Charts');
        return;
    }

    initTrendChart(data);
    initTypChart(data);
    initKstChart(data);
    initKostenChart(data);
}

/**
 * NZA pro Monat - Line Chart
 */
function initTrendChart(data) {
    const ctx = document.getElementById('chart-trend');
    if (!ctx) return;

    // Gruppe nach Monat
    const monthlyData = {};
    data.forEach(nza => {
        const date = new Date(nza.datum);
        const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        monthlyData[key] = (monthlyData[key] || 0) + 1;
    });

    // Sortieren und Labels erstellen
    const sortedKeys = Object.keys(monthlyData).sort();
    const labels = sortedKeys.map(k => {
        const [year, month] = k.split('-');
        return `${month}/${year.slice(2)}`;
    });
    const values = sortedKeys.map(k => monthlyData[k]);

    if (chartTrend) chartTrend.destroy();

    chartTrend = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'NZA Anzahl',
                data: values,
                borderColor: COLORS.primary,
                backgroundColor: 'rgba(21, 101, 192, 0.1)',
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
}

/**
 * Typ-Verteilung - Doughnut Chart
 */
function initTypChart(data) {
    const ctx = document.getElementById('chart-typ');
    if (!ctx) return;

    // Gruppe nach Typ
    const typData = {};
    data.forEach(nza => {
        const typ = nza.typ || 'Unbekannt';
        typData[typ] = (typData[typ] || 0) + 1;
    });

    const labels = Object.keys(typData);
    const values = Object.values(typData);
    const colors = labels.map(l => TYP_COLORS[l] || COLORS.neutral);

    if (chartTyp) chartTyp.destroy();

    chartTyp = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { padding: 15 }
                }
            }
        }
    });
}

/**
 * Kostenstellen-Verteilung - Bar Chart
 */
function initKstChart(data) {
    const ctx = document.getElementById('chart-kst');
    if (!ctx) return;

    // Gruppe nach KST
    const kstData = {};
    data.forEach(nza => {
        const kst = nza.kst || 'Unbekannt';
        kstData[kst] = (kstData[kst] || 0) + 1;
    });

    // Sortieren nach Anzahl
    const sorted = Object.entries(kstData).sort((a, b) => b[1] - a[1]);
    const labels = sorted.map(([k]) => k);
    const values = sorted.map(([, v]) => v);
    const colors = labels.map(l => KST_COLORS[l] || COLORS.neutral);

    if (chartKst) chartKst.destroy();

    chartKst = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Anzahl NZA',
                data: values,
                backgroundColor: colors,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
}

/**
 * Kosten pro Monat - Bar Chart
 */
function initKostenChart(data) {
    const ctx = document.getElementById('chart-kosten');
    if (!ctx) return;

    // Gruppe nach Monat
    const monthlyKosten = {};
    data.forEach(nza => {
        const date = new Date(nza.datum);
        const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        monthlyKosten[key] = (monthlyKosten[key] || 0) + (nza.kostenGesamt || 0);
    });

    // Sortieren
    const sortedKeys = Object.keys(monthlyKosten).sort();
    const labels = sortedKeys.map(k => {
        const [year, month] = k.split('-');
        return `${month}/${year.slice(2)}`;
    });
    const values = sortedKeys.map(k => monthlyKosten[k]);

    if (chartKosten) chartKosten.destroy();

    chartKosten = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Kosten (€)',
                data: values,
                backgroundColor: COLORS.primary,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            return new Intl.NumberFormat('de-DE', {
                                style: 'currency',
                                currency: 'EUR'
                            }).format(context.raw);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => value + ' €'
                    }
                }
            }
        }
    });
}

/**
 * Refresh all charts with new data
 */
function refreshCharts(data) {
    initCharts(data);
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initCharts, refreshCharts };
}
