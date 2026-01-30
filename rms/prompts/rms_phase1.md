# Claude Code Prompt: RMS Phase 1 - Bug-Fixes & UI-Anpassungen

**Datum:** 2026-01-28  
**Ausführung:** Direkt auf Hetzner Server (46.224.102.30)  
**Ziel:** Kritische Bugs fixen + UI vereinfachen

---

## 🔧 SERVER-ZUGANG

```bash
# Server
IP: 46.224.102.30
User: root

# n8n API
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMGFkYS1mMGU5NTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM4MDQxNDQxfQ.Hhqnbitgd-ak_iZruZy1Z_rdHJ75BtcYfv09RO05Rtg"
export N8N_BASE_URL="http://127.0.0.1:5678"

# Pfade
FRONTEND="/var/www/html/rms/"
SCRIPTS="/opt/osp/scripts/"
NGINX_CONF="/etc/nginx/sites-available/osp"
```

---

## 📋 SHAREPOINT REFERENZ

```bash
# Site-ID
SITE_ID="rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"

# Listen-IDs
REKLAMATIONEN_LIST="e9b1d926-085a-4435-a012-114ca9ba59a8"
MASSNAHMEN_LIST="3768f2d8-878c-4a5f-bd52-7486fe93289d"
SCHRIFTVERKEHR_LIST="741c6ae8-88bb-406b-bf85-2e11192a528f"

# n8n Credential für Microsoft OAuth2
CREDENTIAL_ID="Fm3IuAbVYBYDIA4U"
```

---

## 🎯 AUFGABEN PHASE 1

### AUFGABE 1: PDF-Generierung Bug fixen (0 Bytes)

**Problem:** Generierte PDFs haben 0 Bytes / keinen Inhalt

**Analyse-Schritte:**

1. **Formblatt-Service prüfen:**
```bash
# Service Status
systemctl status formblatt-service

# Logs prüfen
journalctl -u formblatt-service -n 50

# Test-Aufruf
curl -X POST http://127.0.0.1:5050/health
```

2. **Scripts prüfen:**
```bash
# fill_xlsx_form.py testen
python3 /opt/osp/scripts/fill_xlsx_form.py --help

# convert_to_pdf.py testen
python3 /opt/osp/scripts/convert_to_pdf.py --help

# LibreOffice testen
libreoffice --headless --version
```

3. **n8n Workflow prüfen:**
   - Workflow-ID: `MN63eCmmUDHzED8G` (RMS-Generate-Formblatt)
   - Prüfe ob Binary-Daten korrekt übergeben werden
   - Prüfe ob Pfade stimmen

4. **Manueller Test:**
```bash
# Temp-Verzeichnis
mkdir -p /tmp/rms-forms

# Test-Template aus SharePoint herunterladen (manuell oder via curl)
# Dann testen:
python3 /opt/osp/scripts/fill_xlsx_form.py \
    /tmp/rms-forms/test_template.xlsx \
    /tmp/rms-forms/test_filled.xlsx \
    --data '{"abweichungs_nr": "QA-26001", "datum": "2026-01-28"}'

# PDF konvertieren
python3 /opt/osp/scripts/convert_to_pdf.py \
    /tmp/rms-forms/test_filled.xlsx \
    /tmp/rms-forms/test_output.pdf

# Ergebnis prüfen
ls -la /tmp/rms-forms/
file /tmp/rms-forms/test_output.pdf
```

**Mögliche Ursachen:**
- Template wird nicht korrekt von SharePoint geladen
- Base64-Konvertierung fehlerhaft
- fill_xlsx_form.py findet keine Felder
- LibreOffice-Konvertierung schlägt fehl
- Upload nach SharePoint fehlerhaft

---

### AUFGABE 2: Detail-View Speichern fixen

**Problem:** Änderungen im Detail-Modal werden nicht gespeichert

**Analyse-Schritte:**

1. **Frontend prüfen:**
```bash
# app.js öffnen
cat /var/www/html/rms/js/app.js | grep -A 50 "saveReklamation"
```

2. **API-Endpunkt testen:**
```bash
# PATCH-Request testen
curl -X PATCH "https://osp.schneider-kabelsatzbau.de/api/rms/update" \
    -H "Content-Type: application/json" \
    -d '{"id": "1", "fields": {"Title": "Test Update"}}'
```

3. **n8n Workflow prüfen:**
   - Workflow-ID: `bmEAINTP2lPNORLp` (RMS-Update-Reklamation)
   - Prüfe ob PATCH korrekt verarbeitet wird

4. **Browser Console prüfen:**
   - Netzwerk-Tab: Wird der Request gesendet?
   - Console: Gibt es JavaScript-Fehler?

**Frontend-Fix (falls nötig):**
```javascript
// In /var/www/html/rms/js/app.js
// Funktion saveReklamation() prüfen/korrigieren

async function saveReklamation(event) {
    if (event) event.preventDefault();
    
    const id = window.currentReklamationId;
    if (!id) {
        console.error('Keine Reklamation-ID');
        alert('Fehler: Keine Reklamation ausgewählt');
        return;
    }
    
    // Felder sammeln
    const fields = {};
    
    // Nur geänderte/vorhandene Felder hinzufügen
    const typ = document.getElementById('edit-typ')?.value;
    if (typ) fields.Rekla_Typ = typ;
    
    const status = document.getElementById('edit-status')?.value;
    if (status) fields.Rekla_Status = status;
    
    const prioritaet = document.getElementById('edit-prioritaet')?.value;
    if (prioritaet) fields.Prioritaet = prioritaet;
    
    const kst = document.getElementById('edit-kst')?.value;
    if (kst) fields.KST = kst;
    
    const verantwortlich = document.getElementById('edit-verantwortlich')?.value;
    if (verantwortlich) fields.Verantwortlich = verantwortlich;
    
    const zieldatum = document.getElementById('edit-zieldatum')?.value;
    if (zieldatum) fields.Zieldatum = zieldatum;
    
    const title = document.getElementById('edit-title')?.value;
    if (title) fields.Title = title;
    
    const beschreibung = document.getElementById('edit-beschreibung')?.value;
    if (beschreibung) fields.Beschreibung = beschreibung;
    
    console.log('Speichere Reklamation:', id, fields);
    
    try {
        showLoading(true);
        
        const response = await fetch('/api/rms/update', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: String(id), fields })
        });
        
        console.log('Response Status:', response.status);
        
        const result = await response.json();
        console.log('Response Body:', result);
        
        if (response.ok) {
            alert('✅ Änderungen gespeichert!');
            toggleEditMode();
            await showDetail(id);
            await loadData();
        } else {
            alert('❌ Fehler beim Speichern: ' + (result.error || JSON.stringify(result)));
        }
    } catch (error) {
        console.error('Speichern fehlgeschlagen:', error);
        alert('❌ Fehler: ' + error.message);
    } finally {
        showLoading(false);
    }
}
```

---

### AUFGABE 3: Header-Text ergänzen

**Änderung:** Beschreibung im Header hinzufügen

```bash
# In /var/www/html/rms/index.html
# Finde den Header-Bereich und ergänze:
```

```html
<header class="dashboard-header">
    <div class="header-content">
        <h1>RMS Dashboard</h1>
        <p class="header-subtitle">QM-Tool zur Bearbeitung/Visualisierung von externen Reklamationen</p>
    </div>
    <!-- Rest des Headers -->
</header>
```

**CSS ergänzen:**
```css
/* In /var/www/html/rms/css/style.css */
.header-subtitle {
    font-size: 0.9rem;
    color: #666;
    margin-top: 5px;
    font-weight: normal;
}
```

---

### AUFGABE 4: Typ-Filter auf Kunde/Lieferant beschränken

**Änderung:** "Intern" aus Dropdown entfernen (Intern → NZA-System)

```bash
# In /var/www/html/rms/index.html
# Filter-Dropdown anpassen:
```

```html
<select id="filter-typ" class="form-control">
    <option value="">Alle Typen</option>
    <option value="Kunde">Kunde</option>
    <option value="Lieferant">Lieferant</option>
    <!-- ENTFERNT: <option value="Intern">Intern</option> -->
</select>
```

**Auch im Edit-Modal anpassen:**
```html
<select id="edit-typ" class="form-control">
    <option value="Kunde">Kunde</option>
    <option value="Lieferant">Lieferant</option>
    <!-- ENTFERNT: <option value="Intern">Intern</option> -->
</select>
```

---

### AUFGABE 5: Such-Zeile überarbeiten

**Änderungen:**
- Suchfeld: BEIBEHALTEN
- Typ-Filter: Nur Kunde/Lieferant (siehe Aufgabe 4)
- Status-Filter: BEIBEHALTEN
- Kostenstellen-Filter: ENTFERNEN
- CSV-Export: ENTFERNEN

```bash
# In /var/www/html/rms/index.html
# Filter-Section anpassen:
```

```html
<section class="filter-section">
    <!-- Suchfeld -->
    <input type="text" id="search-input" placeholder="🔍 Suchen..." class="search-input">
    
    <!-- Typ-Filter (nur Kunde/Lieferant) -->
    <select id="filter-typ" class="form-control">
        <option value="">Alle Typen</option>
        <option value="Kunde">Kunde</option>
        <option value="Lieferant">Lieferant</option>
    </select>
    
    <!-- Status-Filter -->
    <select id="filter-status" class="form-control">
        <option value="">Alle Status</option>
        <option value="Neu">Neu</option>
        <option value="In Bearbeitung">In Bearbeitung</option>
        <option value="Maßnahmen">Maßnahmen</option>
        <option value="Abgeschlossen">Abgeschlossen</option>
    </select>
    
    <!-- ENTFERNT: KST-Filter -->
    <!-- ENTFERNT: CSV-Export Button -->
    
    <!-- Refresh-Button beibehalten -->
    <button id="btn-refresh" class="btn btn-secondary" title="Aktualisieren">🔄</button>
    
    <!-- Einträge-Anzeige -->
    <span id="filtered-count" class="count-badge"></span>
</section>
```

**In app.js: KST-Filter-Logik entfernen:**
```javascript
// In applyFilters() - KST-Filter entfernen:
function applyFilters() {
    let filtered = [...allReklamationen];
    
    // Typ-Filter
    const typ = document.getElementById('filter-typ')?.value;
    if (typ) filtered = filtered.filter(r => r.Rekla_Typ === typ);
    
    // Status-Filter
    const status = document.getElementById('filter-status')?.value;
    if (status) filtered = filtered.filter(r => r.Rekla_Status === status);
    
    // ENTFERNT: KST-Filter
    
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
    
    // Sortierung
    filtered = sortData(filtered);
    
    updateTable(filtered);
    updateFilteredCount(filtered.length, allReklamationen.length);
}
```

---

## ✅ CHECKLISTE NACH ABSCHLUSS

### Bug-Fixes
- [ ] PDF-Generierung getestet - PDFs haben Inhalt
- [ ] Detail-View Speichern funktioniert
- [ ] Browser Console zeigt keine Fehler

### UI-Anpassungen
- [ ] Header zeigt "QM-Tool zur Bearbeitung/Visualisierung von externen Reklamationen"
- [ ] Typ-Filter zeigt nur "Kunde" und "Lieferant"
- [ ] Kostenstellen-Filter entfernt
- [ ] CSV-Export entfernt
- [ ] Suchfeld funktioniert

### Tests
```bash
# Frontend-Dateien prüfen
ls -la /var/www/html/rms/

# Nginx-Syntax prüfen
nginx -t

# Nginx neu laden (falls Config geändert)
systemctl reload nginx

# Formblatt-Service Status
systemctl status formblatt-service
```

---

## 🔗 REFERENZEN

| Resource | URL/Pfad |
|----------|----------|
| Dashboard | https://osp.schneider-kabelsatzbau.de/rms/ |
| n8n | http://46.224.102.30:5678 |
| Frontend | /var/www/html/rms/ |
| Scripts | /opt/osp/scripts/ |
| SharePoint RMS | https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS |

---

## 📝 WICHTIGE HINWEISE

1. **Vor Änderungen Backup erstellen:**
```bash
cp -r /var/www/html/rms/ /var/www/html/rms_backup_$(date +%Y%m%d_%H%M%S)/
```

2. **Nach Frontend-Änderungen Browser-Cache leeren** (Ctrl+Shift+R)

3. **Bei n8n-Workflow-Änderungen:** Workflow deaktivieren → ändern → testen → aktivieren

---

*Erstellt: 2026-01-28*
