// RMS Dashboard - Vorkonfigurierte Massnahmen-Templates
// Version 1.0 - 2026-01-28

// ============================================
// MASSNAHMEN TEMPLATES
// ============================================

const MASSNAHMEN_TEMPLATES = [
    // Sofortmassnahmen
    {
        kategorie: 'Sofortmassnahme',
        titel: 'Aktuellen Lagerbestand pruefen',
        beschreibung: 'Bestandsaufnahme der betroffenen Charge im Lager durchfuehren',
        standardTermin: 1,
        empfohlenerVerantwortlicher: null
    },
    {
        kategorie: 'Sofortmassnahme',
        titel: 'Produktion stoppen',
        beschreibung: 'Fertigung mit betroffenen Teilen sofort stoppen',
        standardTermin: 0,
        empfohlenerVerantwortlicher: 'MD'
    },
    {
        kategorie: 'Sofortmassnahme',
        titel: 'Sperrung betroffener Ware',
        beschreibung: 'Alle betroffenen Teile sperren und kennzeichnen',
        standardTermin: 0,
        empfohlenerVerantwortlicher: null
    },
    {
        kategorie: 'Sofortmassnahme',
        titel: '100% Pruefung einleiten',
        beschreibung: 'Vollstaendige Pruefung aller betroffenen Teile',
        standardTermin: 1,
        empfohlenerVerantwortlicher: 'SK'
    },

    // Korrekturmassnahmen
    {
        kategorie: 'Korrekturmassnahme',
        titel: 'Lieferant informieren',
        beschreibung: 'Reklamation an Lieferant mit Qualitaetsabweichung uebermitteln',
        standardTermin: 2,
        empfohlenerVerantwortlicher: 'TS'
    },
    {
        kategorie: 'Korrekturmassnahme',
        titel: 'Ersatzlieferung anfordern',
        beschreibung: 'Ersatzlieferung beim Lieferanten beauftragen',
        standardTermin: 3,
        empfohlenerVerantwortlicher: 'TS'
    },
    {
        kategorie: 'Korrekturmassnahme',
        titel: 'Gutschrift einfordern',
        beschreibung: 'Gutschrift fuer fehlerhafte Ware anfordern',
        standardTermin: 7,
        empfohlenerVerantwortlicher: 'TS'
    },
    {
        kategorie: 'Korrekturmassnahme',
        titel: 'Werkzeug/Maschine pruefen',
        beschreibung: 'Betroffene Anlage auf Fehlerursache untersuchen',
        standardTermin: 2,
        empfohlenerVerantwortlicher: 'MD'
    },
    {
        kategorie: 'Korrekturmassnahme',
        titel: 'Nacharbeit durchfuehren',
        beschreibung: 'Fehlerhafte Teile nacharbeiten',
        standardTermin: 3,
        empfohlenerVerantwortlicher: null
    },

    // Vorbeugemassnahmen
    {
        kategorie: 'Vorbeugemassnahme',
        titel: 'Pruefanweisung anpassen',
        beschreibung: 'Pruefanweisung um neue Pruefpunkte erweitern',
        standardTermin: 7,
        empfohlenerVerantwortlicher: 'AL'
    },
    {
        kategorie: 'Vorbeugemassnahme',
        titel: 'Mitarbeiterschulung durchfuehren',
        beschreibung: 'Betroffene Mitarbeiter ueber Fehler und Vermeidung schulen',
        standardTermin: 14,
        empfohlenerVerantwortlicher: 'AL'
    },
    {
        kategorie: 'Vorbeugemassnahme',
        titel: 'Lieferantenbewertung anpassen',
        beschreibung: 'Lieferantenbewertung aktualisieren',
        standardTermin: 14,
        empfohlenerVerantwortlicher: 'TS'
    },
    {
        kategorie: 'Vorbeugemassnahme',
        titel: 'Wareneingangspruefung verschaerfen',
        beschreibung: 'Pruefumfang bei Wareneingang erhoehen',
        standardTermin: 7,
        empfohlenerVerantwortlicher: 'SK'
    },

    // 8D-spezifisch
    {
        kategorie: '8D-Report',
        titel: '8D-Report erstellen',
        beschreibung: 'Vollstaendigen 8D-Report gemaess F-QM-03 erstellen',
        standardTermin: 14,
        empfohlenerVerantwortlicher: 'AL'
    },
    {
        kategorie: '8D-Report',
        titel: 'Root-Cause-Analyse durchfuehren',
        beschreibung: 'Ursachenanalyse mit 5-Why oder Ishikawa',
        standardTermin: 7,
        empfohlenerVerantwortlicher: 'AL'
    },
    {
        kategorie: '8D-Report',
        titel: 'Wirksamkeitspruefung',
        beschreibung: 'Wirksamkeit der Massnahmen nach 30 Tagen pruefen',
        standardTermin: 30,
        empfohlenerVerantwortlicher: 'AL'
    }
];

// ============================================
// VERANTWORTLICHE (aus HR_CORE)
// ============================================

const VERANTWORTLICHE = [
    { kuerzel: 'AL', name: 'Andreas Loehr', email: 'a.loehr@schneider-kabelsatzbau.de', rolle: 'QM-Manager' },
    { kuerzel: 'CS', name: 'C. Schneider', email: 'c.schneider@schneider-kabelsatzbau.de', rolle: 'Geschaeftsfuehrung' },
    { kuerzel: 'CA', name: 'C. Andres', email: 'c.andres@schneider-kabelsatzbau.de', rolle: 'Geschaeftsfuehrung' },
    { kuerzel: 'SV', name: 'S. Vogt', email: 's.vogt@schneider-kabelsatzbau.de', rolle: 'Prokurist' },
    { kuerzel: 'TS', name: 'T. Schaefer', email: 't.schaefer@schneider-kabelsatzbau.de', rolle: 'Einkauf' },
    { kuerzel: 'SK', name: 'S. Kunz', email: 's.kunz@schneider-kabelsatzbau.de', rolle: 'Prueffeld' },
    { kuerzel: 'MD', name: 'M. Doering', email: 'm.doering@schneider-kabelsatzbau.de', rolle: 'Technik' }
];

// ============================================
// HELPER FUNCTIONS
// ============================================

function getTemplatesByKategorie(kategorie) {
    return MASSNAHMEN_TEMPLATES.filter(t => t.kategorie === kategorie);
}

function getVerantwortlicherByKuerzel(kuerzel) {
    return VERANTWORTLICHE.find(v => v.kuerzel === kuerzel);
}

function getAllKategorien() {
    return [...new Set(MASSNAHMEN_TEMPLATES.map(t => t.kategorie))];
}
