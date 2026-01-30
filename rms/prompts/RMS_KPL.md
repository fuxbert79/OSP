# Claude Code Prompt: RMS Dashboard - VOLLSTÄNDIGE IMPLEMENTIERUNG

**Datum:** 2026-01-28  
**Ziel:** Alle verbleibenden Features HEUTE fertigstellen  
**Basis:** RMS_Strategie_v5.0, osp-formular-skill v1.1, SERVER_SETUP_2026-01-28.md

---

## 📊 STATUS-ABGLEICH MIT STRATEGIE v5.0

### ✅ BEREITS ERLEDIGT

| Feature | Strategie-Referenz | Status |
|---------|-------------------|--------|
| SharePoint Listen (5x) | Phase 1 | ✅ |
| n8n: E-Mail-Import | MVP | ✅ |
| n8n: QA-ID Generator | MVP | ✅ |
| Dashboard KPI-Cards | MVP | ✅ |
| Dashboard Liste + Filter | MVP | ✅ |
| Detail-Ansicht | MVP | ✅ |
| Edit-Funktionalität | MVP | ✅ |
| Charts (Trend, Typ, KST) | Phase 2 | ✅ |
| Maßnahmen CRUD | Phase 2 | ✅ |

### 🔴 HEUTE NOCH UMZUSETZEN

| Feature | Strategie-Referenz | Priorität |
|---------|-------------------|-----------|
| **Vorkonfigurierte Maßnahmen** | Phase 2 | 🔴 HOCH |
| **Maßnahmen → Person zuweisen + Benachrichtigung** | Phase 2 (Alarm) | 🔴 HOCH |
| **PDF erstellen funktionsfähig** | Phase 2 (Formblatt) | 🔴 HOCH |
| **Fotos/Bilder anzeigen** | Phase 2 | 🔴 HOCH |
| **Dokumente anzeigen + Vorschau** | Phase 2 | 🔴 HOCH |
| **Status-Auto-Refresh** | MVP | 🟡 MITTEL |
| **Formblatt-Workflow Integration** | Phase 2 | 🔴 HOCH |
| **Schriftverkehr laden** | Phase 2 | 🟡 MITTEL |

---

## 🔧 UMGEBUNG

```bash
# Server
IP: 46.224.102.30
User: root

# API Keys
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMmFlMi1mNzQyLTQxZGUtYTY1OS0xNTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5NTM4MTcwLCJleHAiOjE3NzcyNDA4MDB9.NsECcQH9N-UsiCmXrZkMGLg6ioFbGCuNXWW_XaJAUTY"
export N8N_BASE_URL="http://127.0.0.1:5678"

# SharePoint
SITE_ID="rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"
REKLAMATIONEN_LIST="e9b1d926-085a-4435-a012-114ca9ba59a8"
MASSNAHMEN_LIST="3768f2d8-878c-4a5f-bd52-7486fe93289d"
SCHRIFTVERKEHR_LIST="741c6ae8-88bb-406b-bf85-2e11192a528f"
CREDENTIAL_ID="Fm3IuAbVYBYDIA4U"

# SharePoint Dokumentenbibliothek
DRIVE_PATH="/sites/RMS/Freigegebene Dokumente"

# Bestehende Workflows
RMS_DETAIL_API="5jruolIhqcOGu3GQ"
RMS_UPDATE_REKLAMATION="bmEAINTP2lPNORLp"
RMS_UPDATE_MASSNAHME="TAw3Ktjc8xKEd0i7"
RMS_DELETE_MASSNAHME="QHdEILUhV8j4kXeS"

# Dateien
FRONTEND="/var/www/html/rms/"
NGINX_CONF="/etc/nginx/sites-available/osp"
```

---

## BLOCK 1: VORKONFIGURIERTE MASSNAHMEN (1h)

### 1.1 Maßnahmen-Templates definieren

Erstelle `/var/www/html/rms/js/massnahmen-templates.js`:

```javascript
// Vorkonfigurierte Maßnahmen-Templates
const MASSNAHMEN_TEMPLATES = [
    // Sofortmaßnahmen
    {
        kategorie: 'Sofortmaßnahme',
        titel: 'Aktuellen Lagerbestand prüfen',
        beschreibung: 'Bestandsaufnahme der betroffenen Charge im Lager durchführen',
        standardTermin: 1, // Tage ab heute
        empfohlenerVerantwortlicher: null // User wählt
    },
    {
        kategorie: 'Sofortmaßnahme',
        titel: 'Produktion stoppen',
        beschreibung: 'Fertigung mit betroffenen Teilen sofort stoppen',
        standardTermin: 0,
        empfohlenerVerantwortlicher: 'MD'
    },
    {
        kategorie: 'Sofortmaßnahme',
        titel: 'Sperrung betroffener Ware',
        beschreibung: 'Alle betroffenen Teile sperren und kennzeichnen',
        standardTermin: 0,
        empfohlenerVerantwortlicher: null
    },
    {
        kategorie: 'Sofortmaßnahme',
        titel: '100% Prüfung einleiten',
        beschreibung: 'Vollständige Prüfung aller betroffenen Teile',
        standardTermin: 1,
        empfohlenerVerantwortlicher: 'SK'
    },
    
    // Korrekturmaßnahmen
    {
        kategorie: 'Korrekturmaßnahme',
        titel: 'Lieferant informieren',
        beschreibung: 'Reklamation an Lieferant mit Qualitätsabweichung übermitteln',
        standardTermin: 2,
        empfohlenerVerantwortlicher: 'TS'
    },
    {
        kategorie: 'Korrekturmaßnahme',
        titel: 'Ersatzlieferung anfordern',
        beschreibung: 'Ersatzlieferung beim Lieferanten beauftragen',
        standardTermin: 3,
        empfohlenerVerantwortlicher: 'TS'
    },
    {
        kategorie: 'Korrekturmaßnahme',
        titel: 'Gutschrift einfordern',
        beschreibung: 'Gutschrift für fehlerhafte Ware anfordern',
        standardTermin: 7,
        empfohlenerVerantwortlicher: 'TS'
    },
    {
        kategorie: 'Korrekturmaßnahme',
        titel: 'Werkzeug/Maschine prüfen',
        beschreibung: 'Betroffene Anlage auf Fehlerursache untersuchen',
        standardTermin: 2,
        empfohlenerVerantwortlicher: 'MD'
    },
    {
        kategorie: 'Korrekturmaßnahme',
        titel: 'Nacharbeit durchführen',
        beschreibung: 'Fehlerhafte Teile nacharbeiten',
        standardTermin: 3,
        empfohlenerVerantwortlicher: null
    },
    
    // Vorbeugemaßnahmen
    {
        kategorie: 'Vorbeugemaßnahme',
        titel: 'Prüfanweisung anpassen',
        beschreibung: 'Prüfanweisung um neue Prüfpunkte erweitern',
        standardTermin: 7,
        empfohlenerVerantwortlicher: 'AL'
    },
    {
        kategorie: 'Vorbeugemaßnahme',
        titel: 'Mitarbeiterschulung durchführen',
        beschreibung: 'Betroffene Mitarbeiter über Fehler und Vermeidung schulen',
        standardTermin: 14,
        empfohlenerVerantwortlicher: 'AL'
    },
    {
        kategorie: 'Vorbeugemaßnahme',
        titel: 'Lieferantenbewertung anpassen',
        beschreibung: 'Lieferantenbewertung aktualisieren',
        standardTermin: 14,
        empfohlenerVerantwortlicher: 'TS'
    },
    {
        kategorie: 'Vorbeugemaßnahme',
        titel: 'Wareneingangsprüfung verschärfen',
        beschreibung: 'Prüfumfang bei Wareneingang erhöhen',
        standardTermin: 7,
        empfohlenerVerantwortlicher: 'SK'
    },
    
    // 8D-spezifisch
    {
        kategorie: '8D-Report',
        titel: '8D-Report erstellen',
        beschreibung: 'Vollständigen 8D-Report gemäß F-QM-03 erstellen',
        standardTermin: 14,
        empfohlenerVerantwortlicher: 'AL'
    },
    {
        kategorie: '8D-Report',
        titel: 'Root-Cause-Analyse durchführen',
        beschreibung: 'Ursachenanalyse mit 5-Why oder Ishikawa',
        standardTermin: 7,
        empfohlenerVerantwortlicher: 'AL'
    },
    {
        kategorie: '8D-Report',
        titel: 'Wirksamkeitsprüfung',
        beschreibung: 'Wirksamkeit der Maßnahmen nach 30 Tagen prüfen',
        standardTermin: 30,
        empfohlenerVerantwortlicher: 'AL'
    }
];

// Verantwortliche (aus HR_CORE)
const VERANTWORTLICHE = [
    { kuerzel: 'AL', name: 'Andreas Löhr', email: 'a.loehr@schneider-kabelsatzbau.de', rolle: 'QM-Manager' },
    { kuerzel: 'CS', name: 'C. Schneider', email: 'c.schneider@schneider-kabelsatzbau.de', rolle: 'Geschäftsführung' },
    { kuerzel: 'CA', name: 'C. Andres', email: 'c.andres@schneider-kabelsatzbau.de', rolle: 'Geschäftsführung' },
    { kuerzel: 'SV', name: 'S. Vogt', email: 's.vogt@schneider-kabelsatzbau.de', rolle: 'Prokurist' },
    { kuerzel: 'TS', name: 'T. Schäfer', email: 't.schaefer@schneider-kabelsatzbau.de', rolle: 'Einkauf' },
    { kuerzel: 'SK', name: 'S. Kunz', email: 's.kunz@schneider-kabelsatzbau.de', rolle: 'Prüffeld' },
    { kuerzel: 'MD', name: 'M. Döring', email: 'm.doering@schneider-kabelsatzbau.de', rolle: 'Technik' }
];
```

### 1.2 Maßnahmen-Modal mit Templates erweitern

In `app.js` die `showAddMassnahmeModal()` Funktion ersetzen:

```javascript
function showAddMassnahmeModal() {
    // Template-Kategorien gruppieren
    const kategorien = [...new Set(MASSNAHMEN_TEMPLATES.map(t => t.kategorie))];
    
    const templateOptions = kategorien.map(kat => `
        <optgroup label="${kat}">
            ${MASSNAHMEN_TEMPLATES.filter(t => t.kategorie === kat).map((t, idx) => `
                <option value="${MASSNAHMEN_TEMPLATES.indexOf(t)}">${t.titel}</option>
            `).join('')}
        </optgroup>
    `).join('');
    
    const verantwortlichOptions = VERANTWORTLICHE.map(v => `
        <option value="${v.kuerzel}">${v.kuerzel} - ${v.name} (${v.rolle})</option>
    `).join('');
    
    const html = `
        <div class="modal" id="massnahme-modal">
            <div class="modal-content" style="max-width:600px;">
                <span class="close-btn" onclick="closeMassnahmeModal()">&times;</span>
                <h2>➕ Neue Maßnahme</h2>
                
                <div class="form-group">
                    <label>📋 Vorlage wählen (optional)</label>
                    <select id="m-template" class="form-control" onchange="applyMassnahmeTemplate()">
                        <option value="">-- Eigene Maßnahme eingeben --</option>
                        ${templateOptions}
                    </select>
                </div>
                
                <hr style="margin: 20px 0;">
                
                <form id="massnahme-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Typ *</label>
                            <select id="m-typ" class="form-control" required>
                                <option value="Sofortmaßnahme">Sofortmaßnahme</option>
                                <option value="Korrekturmaßnahme">Korrekturmaßnahme</option>
                                <option value="Vorbeugemaßnahme">Vorbeugemaßnahme</option>
                                <option value="8D-Report">8D-Report</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Termin *</label>
                            <input type="date" id="m-termin" class="form-control" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Maßnahme *</label>
                        <input type="text" id="m-title" class="form-control" required placeholder="Bezeichnung der Maßnahme">
                    </div>
                    
                    <div class="form-group">
                        <label>Beschreibung</label>
                        <textarea id="m-beschreibung" class="form-control" rows="3" placeholder="Details zur Maßnahme"></textarea>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Verantwortlich *</label>
                            <select id="m-verantwortlich" class="form-control" required>
                                <option value="">-- Auswählen --</option>
                                ${verantwortlichOptions}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>
                                <input type="checkbox" id="m-benachrichtigen" checked>
                                📧 Per Email/Teams benachrichtigen
                            </label>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary">💾 Speichern</button>
                        <button type="button" class="btn btn-secondary" onclick="closeMassnahmeModal()">Abbrechen</button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', html);
    
    // Standard-Termin: Morgen
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById('m-termin').value = tomorrow.toISOString().split('T')[0];
    
    document.getElementById('massnahme-form').onsubmit = async (e) => {
        e.preventDefault();
        await createMassnahmeWithNotification();
    };
}

function applyMassnahmeTemplate() {
    const idx = document.getElementById('m-template').value;
    if (idx === '') return;
    
    const template = MASSNAHMEN_TEMPLATES[parseInt(idx)];
    
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
```

---

## BLOCK 2: BENACHRICHTIGUNG BEI MASSNAHMEN-ZUWEISUNG (1.5h)

### 2.1 n8n Workflow: RMS-Massnahmen-Notify

Erstelle einen neuen Workflow für Benachrichtigungen.

**Webhook:** POST `/webhook/rms-notify-massnahme`

**Request-Body:**
```json
{
    "qaId": "QA-26013",
    "reklaTitle": "Crimphöhe außerhalb Toleranz",
    "massnahme": {
        "title": "100% Prüfung einleiten",
        "typ": "Sofortmaßnahme",
        "termin": "2026-01-29",
        "beschreibung": "Vollständige Prüfung aller Teile"
    },
    "verantwortlich": {
        "kuerzel": "SK",
        "email": "s.kunz@schneider-kabelsatzbau.de",
        "name": "S. Kunz"
    },
    "ersteller": "AL",
    "dashboardUrl": "https://osp.schneider-kabelsatzbau.de/rms/"
}
```

**Nodes:**

1. **Webhook Trigger**
   - Method: POST
   - Path: `rms-notify-massnahme`

2. **Send Email** (HTTP Request)
```
Method: POST
URL: https://graph.microsoft.com/v1.0/me/sendMail
Authentication: OAuth2 (Microsoft account)
Body:
{
  "message": {
    "subject": "[RMS] Neue Maßnahme zugewiesen: {{ $json.body.massnahme.title }}",
    "body": {
      "contentType": "HTML",
      "content": "<h2>🔔 Neue Maßnahme im RMS</h2><p>Hallo {{ $json.body.verantwortlich.name }},</p><p>Ihnen wurde eine neue Maßnahme zugewiesen:</p><table border='1' cellpadding='8'><tr><td><b>Reklamation</b></td><td>{{ $json.body.qaId }} - {{ $json.body.reklaTitle }}</td></tr><tr><td><b>Maßnahme</b></td><td>{{ $json.body.massnahme.title }}</td></tr><tr><td><b>Typ</b></td><td>{{ $json.body.massnahme.typ }}</td></tr><tr><td><b>Termin</b></td><td>{{ $json.body.massnahme.termin }}</td></tr><tr><td><b>Beschreibung</b></td><td>{{ $json.body.massnahme.beschreibung || '-' }}</td></tr></table><p><a href='{{ $json.body.dashboardUrl }}'>➡️ Zum RMS Dashboard</a></p><p>Erstellt von: {{ $json.body.ersteller }}</p>"
    },
    "toRecipients": [
      { "emailAddress": { "address": "{{ $json.body.verantwortlich.email }}" } }
    ]
  }
}
```

3. **Send Teams Message (optional)** (HTTP Request)
```
Method: POST
URL: https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages
Body:
{
  "body": {
    "contentType": "html",
    "content": "🔔 <b>Neue Maßnahme:</b> {{ $json.body.massnahme.title }}<br>Reklamation: {{ $json.body.qaId }}<br>Verantwortlich: {{ $json.body.verantwortlich.kuerzel }}<br>Termin: {{ $json.body.massnahme.termin }}"
  }
}
```

4. **Respond to Webhook**

### 2.2 Frontend: createMassnahmeWithNotification

```javascript
async function createMassnahmeWithNotification() {
    const reklaData = window.currentReklamationData?.reklamation;
    const verantwortlichKuerzel = document.getElementById('m-verantwortlich').value;
    const benachrichtigen = document.getElementById('m-benachrichtigen').checked;
    
    const massnahmeData = {
        reklaId: window.currentReklamationId,
        title: document.getElementById('m-title').value,
        typ: document.getElementById('m-typ').value,
        termin: document.getElementById('m-termin').value,
        beschreibung: document.getElementById('m-beschreibung').value,
        verantwortlich: verantwortlichKuerzel
    };
    
    try {
        showLoading(true);
        
        // 1. Maßnahme in SharePoint erstellen
        const response = await fetch('/api/rms/massnahmen', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(massnahmeData)
        });
        
        if (!response.ok) throw new Error('Maßnahme konnte nicht erstellt werden');
        
        // 2. Benachrichtigung senden (wenn aktiviert)
        if (benachrichtigen && verantwortlichKuerzel) {
            const verantwortlicher = VERANTWORTLICHE.find(v => v.kuerzel === verantwortlichKuerzel);
            
            if (verantwortlicher?.email) {
                await fetch('/api/rms/notify-massnahme', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        qaId: reklaData?.QA_ID || 'Unbekannt',
                        reklaTitle: reklaData?.Title || 'Unbekannt',
                        massnahme: massnahmeData,
                        verantwortlich: verantwortlicher,
                        ersteller: 'AL', // TODO: Aktueller User
                        dashboardUrl: window.location.href
                    })
                });
            }
        }
        
        closeMassnahmeModal();
        await showDetail(window.currentReklamationId);
        alert('✅ Maßnahme erstellt' + (benachrichtigen ? ' und Benachrichtigung gesendet' : ''));
        
    } catch (error) {
        console.error('Fehler:', error);
        alert('❌ Fehler: ' + error.message);
    } finally {
        showLoading(false);
    }
}
```

### 2.3 Nginx Route

```nginx
location = /api/rms/notify-massnahme {
    proxy_pass http://127.0.0.1:5678/webhook/rms-notify-massnahme;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header Content-Type application/json;
}
```

---

## BLOCK 3: FOTOS & DOKUMENTE ANZEIGEN (2h)

### 3.1 n8n Workflow: RMS-Files-API

Lädt Dateien aus dem SharePoint-Ordner einer Reklamation.

**Webhook:** GET `/webhook/rms-files?qaId=QA-26001&folder=Fotos`

**Nodes:**

1. **Webhook Trigger**
   - Method: GET
   - Path: `rms-files`

2. **Get Folder Contents** (HTTP Request)
```
Method: GET
URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/drive/root:/2026/{{ $json.query.qaId }}/{{ $json.query.folder || '' }}:/children
Authentication: OAuth2
Headers: Prefer: HonorNonIndexedQueriesWarningMayFailRandomly
```

3. **Transform Results** (Code Node)
```javascript
const items = $input.item.json.value || [];

return {
    files: items.map(item => ({
        id: item.id,
        name: item.name,
        size: item.size,
        mimeType: item.file?.mimeType || 'folder',
        isFolder: !item.file,
        webUrl: item.webUrl,
        thumbnailUrl: item.thumbnails?.[0]?.medium?.url || null,
        downloadUrl: item['@microsoft.graph.downloadUrl'] || null,
        createdDateTime: item.createdDateTime,
        lastModifiedDateTime: item.lastModifiedDateTime
    })),
    folder: $json.query.folder || 'root',
    qaId: $json.query.qaId
};
```

4. **Respond to Webhook**

### 3.2 n8n Workflow: RMS-File-Preview

Lädt eine einzelne Datei für Vorschau/Download.

**Webhook:** GET `/webhook/rms-file-preview?fileId={id}`

**Nodes:**

1. **Webhook Trigger**

2. **Get File Content** (HTTP Request)
```
Method: GET
URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/drive/items/{{ $json.query.fileId }}/content
Authentication: OAuth2
Response Format: Binary
```

3. **Respond to Webhook** (Binary Response)

### 3.3 Frontend: Dateien-Sektion im Detail-Modal

Erweitere `index.html`:

```html
<!-- Im Detail-Modal: Neue Sektionen -->

<!-- Fotos -->
<div class="detail-section">
    <div class="section-header">
        <h3>📷 Fotos</h3>
        <button class="btn btn-sm" onclick="refreshFiles('Fotos')">🔄</button>
    </div>
    <div id="detail-fotos" class="file-grid">
        <p class="loading">Lade Fotos...</p>
    </div>
</div>

<!-- Dokumente -->
<div class="detail-section">
    <div class="section-header">
        <h3>📄 Dokumente / Formulare</h3>
        <button class="btn btn-sm" onclick="refreshFiles('Dokumente')">🔄</button>
    </div>
    <div id="detail-dokumente" class="file-list">
        <p class="loading">Lade Dokumente...</p>
    </div>
</div>

<!-- Datei-Vorschau Modal -->
<div id="file-preview-modal" class="modal" style="display:none;">
    <div class="modal-content modal-large">
        <span class="close-btn" onclick="closeFilePreview()">&times;</span>
        <h2 id="preview-filename">Datei</h2>
        <div id="preview-content">
            <!-- Wird dynamisch befüllt -->
        </div>
        <div class="preview-actions">
            <a id="preview-download" href="#" class="btn btn-primary" target="_blank">⬇️ Herunterladen</a>
            <a id="preview-sharepoint" href="#" class="btn btn-secondary" target="_blank">📂 In SharePoint öffnen</a>
        </div>
    </div>
</div>
```

### 3.4 JavaScript: Dateien laden und anzeigen

```javascript
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
}

function renderFotos(files) {
    const container = document.getElementById('detail-fotos');
    
    if (!files || files.length === 0) {
        container.innerHTML = '<p class="empty-state">Keine Fotos vorhanden</p>';
        return;
    }
    
    container.innerHTML = files.map(file => `
        <div class="file-thumbnail" onclick="showFilePreview('${file.id}', '${file.name}', '${file.webUrl}', '${file.downloadUrl || ''}', '${file.mimeType}')">
            ${file.thumbnailUrl 
                ? `<img src="${file.thumbnailUrl}" alt="${file.name}">`
                : `<div class="file-icon">📷</div>`
            }
            <span class="file-name">${truncateFilename(file.name, 20)}</span>
        </div>
    `).join('');
}

function renderDokumente(files) {
    const container = document.getElementById('detail-dokumente');
    
    if (!files || files.length === 0) {
        container.innerHTML = '<p class="empty-state">Keine Dokumente vorhanden</p>';
        return;
    }
    
    // Nach Typ gruppieren
    const formblattFiles = files.filter(f => f.name.startsWith('F_QM_') || f.name.startsWith('F-QM-'));
    const otherFiles = files.filter(f => !f.name.startsWith('F_QM_') && !f.name.startsWith('F-QM-'));
    
    let html = '';
    
    if (formblattFiles.length > 0) {
        html += '<h4>📋 Formblätter</h4>';
        html += formblattFiles.map(f => renderFileRow(f)).join('');
    }
    
    if (otherFiles.length > 0) {
        html += '<h4>📎 Sonstige Dokumente</h4>';
        html += otherFiles.map(f => renderFileRow(f)).join('');
    }
    
    container.innerHTML = html;
}

function renderFileRow(file) {
    const icon = getFileIcon(file.mimeType, file.name);
    const size = formatFileSize(file.size);
    const date = formatDate(file.lastModifiedDateTime);
    
    return `
        <div class="file-row" onclick="showFilePreview('${file.id}', '${file.name}', '${file.webUrl}', '${file.downloadUrl || ''}', '${file.mimeType}')">
            <span class="file-icon">${icon}</span>
            <span class="file-name">${file.name}</span>
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
    if (name.length <= maxLen) return name;
    const ext = name.split('.').pop();
    return name.substring(0, maxLen - ext.length - 4) + '...' + ext;
}

// ============================================
// DATEI-VORSCHAU
// ============================================

function showFilePreview(fileId, filename, webUrl, downloadUrl, mimeType) {
    const modal = document.getElementById('file-preview-modal');
    const content = document.getElementById('preview-content');
    
    document.getElementById('preview-filename').textContent = filename;
    document.getElementById('preview-download').href = downloadUrl || webUrl;
    document.getElementById('preview-sharepoint').href = webUrl;
    
    // Vorschau basierend auf Dateityp
    if (mimeType?.startsWith('image/')) {
        content.innerHTML = `<img src="${downloadUrl}" alt="${filename}" style="max-width:100%; max-height:70vh;">`;
    } else if (filename.endsWith('.pdf')) {
        content.innerHTML = `<iframe src="${downloadUrl}#toolbar=0" style="width:100%; height:70vh; border:none;"></iframe>`;
    } else {
        // Keine Vorschau möglich
        content.innerHTML = `
            <div class="no-preview">
                <span style="font-size:64px;">${getFileIcon(mimeType, filename)}</span>
                <p>Keine Vorschau verfügbar</p>
                <p>Klicken Sie auf "Herunterladen" oder "In SharePoint öffnen"</p>
            </div>
        `;
    }
    
    modal.style.display = 'block';
}

function closeFilePreview() {
    document.getElementById('file-preview-modal').style.display = 'none';
    document.getElementById('preview-content').innerHTML = '';
}

async function refreshFiles(folder) {
    const qaId = window.currentReklamationData?.reklamation?.QA_ID;
    if (!qaId) return;
    
    if (folder === 'Fotos') {
        const data = await loadFiles(qaId, 'Fotos');
        renderFotos(data.files || []);
    } else {
        const data = await loadFiles(qaId, folder);
        renderDokumente(data.files || []);
    }
}
```

### 3.5 CSS für Dateien-Anzeige

```css
/* Datei-Grid für Fotos */
.file-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
    padding: 10px 0;
}

.file-thumbnail {
    cursor: pointer;
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    transition: background 0.2s;
}

.file-thumbnail:hover {
    background: #f0f0f0;
}

.file-thumbnail img {
    width: 100%;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
}

.file-thumbnail .file-icon {
    font-size: 48px;
    line-height: 80px;
}

.file-thumbnail .file-name {
    display: block;
    font-size: 0.75rem;
    color: #666;
    margin-top: 5px;
    word-break: break-word;
}

/* Datei-Liste für Dokumente */
.file-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.file-list h4 {
    margin: 15px 0 10px;
    color: var(--primary);
    font-size: 0.9rem;
}

.file-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 15px;
    background: #f8f9fa;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
}

.file-row:hover {
    background: #e9ecef;
}

.file-row .file-icon {
    font-size: 1.5rem;
}

.file-row .file-name {
    flex: 1;
    font-weight: 500;
}

.file-row .file-meta {
    color: #888;
    font-size: 0.8rem;
}

/* Vorschau Modal */
.modal-large {
    max-width: 900px;
    max-height: 90vh;
}

.no-preview {
    text-align: center;
    padding: 40px;
    color: #888;
}

.preview-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #eee;
}

.empty-state {
    color: #888;
    font-style: italic;
    padding: 20px;
    text-align: center;
}
```

### 3.6 Nginx Routen

```nginx
location = /api/rms/files {
    proxy_pass http://127.0.0.1:5678/webhook/rms-files;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}

location = /api/rms/file-preview {
    proxy_pass http://127.0.0.1:5678/webhook/rms-file-preview;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}
```

---

## BLOCK 4: PDF ERSTELLEN (FORMBLATT-WORKFLOW) (2h)

### 4.1 n8n Workflow: RMS-Generate-Formblatt

Gemäß osp-formular-skill v1.1: XLSX → PDF

**Webhook:** POST `/webhook/rms-generate-formblatt`

**Request-Body:**
```json
{
    "qaId": "QA-26013",
    "formularTyp": "F_QM_02",
    "reklamationsDaten": {
        "Title": "Crimphöhe außerhalb Toleranz",
        "Rekla_Typ": "Lieferant",
        "Beschreibung": "Bei der WE-Prüfung festgestellt...",
        "Lieferant": "Würth GmbH",
        "Artikel": "Stecker Typ B12",
        ...
    }
}
```

**Nodes:**

1. **Webhook Trigger**
   - Method: POST
   - Path: `rms-generate-formblatt`

2. **Load XLSX Template** (HTTP Request)
```
Method: GET
URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/drive/root:/Formular-Vorlagen/{{ $json.body.formularTyp }}.xlsx:/content
Authentication: OAuth2
Response Format: Binary
```

3. **Save Template locally** (Write Binary File)
```
Path: /tmp/template_{{ $json.body.qaId }}.xlsx
```

4. **Call Claude API** (HTTP Request)
```
Method: POST
URL: http://localhost:8080/v1/messages
Headers: 
  Content-Type: application/json
  x-api-key: ${ANTHROPIC_API_KEY}
Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Extrahiere die Felddaten für das Formblatt {{ $json.body.formularTyp }} aus folgenden Reklamationsdaten und gib sie als JSON zurück:\n\n{{ JSON.stringify($json.body.reklamationsDaten, null, 2) }}\n\nFormat: { \"feld1\": \"wert1\", \"feld2\": \"wert2\" }"
  }]
}
```

5. **Fill XLSX** (Execute Command)
```bash
python3 /opt/osp/scripts/fill_xlsx_form.py \
    /tmp/template_{{ $json.body.qaId }}.xlsx \
    /tmp/output_{{ $json.body.qaId }}.xlsx \
    --data '{{ $json.claudeResponse }}'
```

6. **Convert to PDF** (Execute Command)
```bash
libreoffice --headless --convert-to pdf --outdir /tmp/ /tmp/output_{{ $json.body.qaId }}.xlsx
```

7. **Upload PDF to SharePoint** (HTTP Request)
```
Method: PUT
URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/drive/root:/2026/{{ $json.body.qaId }}/{{ $json.body.formularTyp }}_{{ $json.body.qaId }}.pdf:/content
Authentication: OAuth2
Body: Binary (PDF file)
```

8. **Upload XLSX to SharePoint** (HTTP Request)
```
Method: PUT
URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/drive/root:/2026/{{ $json.body.qaId }}/{{ $json.body.formularTyp }}_{{ $json.body.qaId }}.xlsx:/content
```

9. **Cleanup** (Execute Command)
```bash
rm /tmp/*_{{ $json.body.qaId }}.*
```

10. **Respond to Webhook**
```json
{
  "success": true,
  "pdfUrl": "https://...",
  "xlsxUrl": "https://..."
}
```

### 4.2 Frontend: PDF erstellen Button funktionsfähig machen

```javascript
async function generatePDF() {
    const data = window.currentReklamationData;
    if (!data?.reklamation) {
        alert('Keine Reklamation geladen');
        return;
    }
    
    // Formular-Typ auswählen
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
            alert(`✅ ${formularTyp} wurde erstellt!\n\nPDF: ${result.pdfUrl}`);
            // Dokumente neu laden
            await loadAllFilesForDetail(data.reklamation.QA_ID);
        } else {
            alert('❌ Fehler: ' + (result.error || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('❌ Fehler bei der PDF-Erstellung');
    } finally {
        showLoading(false);
    }
}

function showFormularTypeDialog() {
    return new Promise((resolve) => {
        const html = `
            <div class="modal" id="formular-dialog">
                <div class="modal-content" style="max-width:400px;">
                    <h2>📋 Formular erstellen</h2>
                    <div class="form-group">
                        <label>Formular-Typ wählen:</label>
                        <select id="formular-typ-select" class="form-control">
                            <option value="F_QM_02">F-QM-02 Qualitätsabweichung</option>
                            <option value="F_QM_03">F-QM-03 8D-Report</option>
                            <option value="F_QM_04">F-QM-04 NZA</option>
                            <option value="F_QM_14">F-QM-14 Korrekturmaßnahme</option>
                        </select>
                    </div>
                    <div class="form-actions">
                        <button class="btn btn-primary" onclick="selectFormular()">Erstellen</button>
                        <button class="btn btn-secondary" onclick="cancelFormular()">Abbrechen</button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', html);
        
        window.selectFormular = () => {
            const typ = document.getElementById('formular-typ-select').value;
            document.getElementById('formular-dialog').remove();
            resolve(typ);
        };
        
        window.cancelFormular = () => {
            document.getElementById('formular-dialog').remove();
            resolve(null);
        };
    });
}
```

### 4.3 Nginx Route

```nginx
location = /api/rms/generate-formblatt {
    proxy_pass http://127.0.0.1:5678/webhook/rms-generate-formblatt;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header Content-Type application/json;
    proxy_read_timeout 120s;  # Längeres Timeout für PDF-Generierung
}
```

---

## BLOCK 5: STATUS AUTO-REFRESH & SCHRIFTVERKEHR (1h)

### 5.1 Auto-Refresh für Dashboard

```javascript
// In app.js: Auto-Refresh Konfiguration

const AUTO_REFRESH_INTERVAL = 60000; // 60 Sekunden
let autoRefreshTimer = null;

function startAutoRefresh() {
    if (autoRefreshTimer) clearInterval(autoRefreshTimer);
    
    autoRefreshTimer = setInterval(async () => {
        console.log('Auto-Refresh...');
        await loadData();
        
        // Charts nur alle 5 Minuten aktualisieren
        if (Date.now() % (5 * 60000) < AUTO_REFRESH_INTERVAL) {
            await initCharts();
        }
    }, AUTO_REFRESH_INTERVAL);
}

function stopAutoRefresh() {
    if (autoRefreshTimer) {
        clearInterval(autoRefreshTimer);
        autoRefreshTimer = null;
    }
}

// Bei Seitenverlassen stoppen
window.addEventListener('beforeunload', stopAutoRefresh);

// Bei DOMContentLoaded starten
document.addEventListener('DOMContentLoaded', () => {
    // ... bestehender Code ...
    startAutoRefresh();
});
```

### 5.2 RMS-Detail-API um Schriftverkehr erweitern

Der bestehende Workflow RMS-Detail-API (5jruolIhqcOGu3GQ) sollte bereits Schriftverkehr laden. Falls nicht funktioniert, prüfen ob die Lookup-Spalte korrekt konfiguriert ist.

**Prüfung:**
```bash
curl "https://osp.schneider-kabelsatzbau.de/api/rms/detail?id=1" | jq '.schriftverkehr'
```

Falls leer, den Workflow anpassen:

```javascript
// Im Merge Results Code Node:
const schriftverkehr = $('Schriftverkehr laden').item.json;

// Debug: Falls value undefined
const svItems = schriftverkehr?.value || [];

return {
  // ...
  schriftverkehr: svItems.map(s => ({
    id: s.id,
    ...s.fields,
    Datum: s.fields?.Datum,
    Typ: s.fields?.Typ,
    Betreff: s.fields?.Betreff || s.fields?.Title,
    Richtung: s.fields?.Richtung
  }))
};
```

### 5.3 Schriftverkehr im Detail-Modal anzeigen

```javascript
function renderSchriftverkehr(items) {
    const container = document.getElementById('detail-schriftverkehr');
    
    if (!items || items.length === 0) {
        container.innerHTML = '<tr><td colspan="4">Kein Schriftverkehr vorhanden</td></tr>';
        return;
    }
    
    container.innerHTML = `
        <tr>
            <th>Datum</th>
            <th>Typ</th>
            <th>Betreff</th>
            <th>Richtung</th>
        </tr>
        ${items.map(s => `
            <tr>
                <td>${formatDate(s.Datum)}</td>
                <td>${s.Typ || '--'}</td>
                <td>${s.Betreff || s.Title || '--'}</td>
                <td><span class="badge badge-${s.Richtung === 'Eingehend' ? 'incoming' : 'outgoing'}">${s.Richtung || '--'}</span></td>
            </tr>
        `).join('')}
    `;
}
```

---

## BLOCK 6: INTEGRATION showDetail() (30min)

### 6.1 showDetail() Funktion komplett aktualisieren

```javascript
async function showDetail(id) {
    showLoading(true);
    
    try {
        const data = await fetchReklamationDetail(id);
        if (!data) {
            alert('Fehler beim Laden der Details');
            return;
        }
        
        const r = data.reklamation;
        
        // Header
        document.getElementById('detail-qa-id').textContent = r.QA_ID || 'Unbekannt';
        
        // Stammdaten (View Mode)
        document.getElementById('detail-stammdaten').innerHTML = `
            <tr><td>Typ:</td><td><span class="badge badge-${(r.Rekla_Typ || '').toLowerCase()}">${r.Rekla_Typ || '--'}</span></td></tr>
            <tr><td>Status:</td><td><span class="status status-${(r.Rekla_Status || '').replace(/\s/g, '-')}">${r.Rekla_Status || '--'}</span></td></tr>
            <tr><td>Priorität:</td><td><span class="priority priority-${(r.Prioritaet || '').toLowerCase()}">${r.Prioritaet || '--'}</span></td></tr>
            <tr><td>KST:</td><td>${r.KST || '--'}</td></tr>
            <tr><td>Erfasst:</td><td>${formatDate(r.Erfassungsdatum)}</td></tr>
            <tr><td>Zieldatum:</td><td>${formatDate(r.Zieldatum)}</td></tr>
            <tr><td>Verantwortlich:</td><td>${r.Verantwortlich || '--'}</td></tr>
        `;
        
        // Beschreibung
        document.getElementById('detail-beschreibung').textContent = 
            r.Beschreibung || 'Keine Beschreibung vorhanden';
        
        // Maßnahmen (mit Inline-Edit)
        document.getElementById('detail-massnahmen').innerHTML = 
            renderMassnahmenTable(data.massnahmen || []);
        
        // Schriftverkehr
        renderSchriftverkehr(data.schriftverkehr || []);
        
        // Fotos & Dokumente laden
        if (r.QA_ID) {
            await loadAllFilesForDetail(r.QA_ID);
        }
        
        // Speichern für Edit/Actions
        window.currentReklamationId = id;
        window.currentReklamationData = data;
        window.currentSharePointUrl = data.sharePointUrl;
        
        // Edit-Mode zurücksetzen
        isEditMode = false;
        document.getElementById('detail-view-mode').style.display = 'block';
        document.getElementById('detail-edit-mode').style.display = 'none';
        document.getElementById('btn-edit-toggle').textContent = '✏️ Bearbeiten';
        
        // Modal anzeigen
        document.getElementById('detail-modal').style.display = 'block';
        
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Laden der Details');
    } finally {
        showLoading(false);
    }
}
```

---

## ✅ CHECKLISTE

Nach Abschluss prüfen:

### Block 1: Vorkonfigurierte Maßnahmen
- [ ] massnahmen-templates.js erstellt
- [ ] Template-Dropdown im Modal
- [ ] applyMassnahmeTemplate() funktioniert
- [ ] Termin wird automatisch gesetzt

### Block 2: Benachrichtigungen
- [ ] n8n Workflow RMS-Massnahmen-Notify erstellt
- [ ] Email wird gesendet
- [ ] Checkbox "Benachrichtigen" funktioniert
- [ ] Nginx Route konfiguriert

### Block 3: Fotos & Dokumente
- [ ] n8n Workflow RMS-Files-API erstellt
- [ ] Fotos werden als Thumbnails angezeigt
- [ ] Dokumente werden aufgelistet
- [ ] Vorschau-Modal funktioniert
- [ ] PDF-Vorschau im iFrame

### Block 4: PDF erstellen
- [ ] n8n Workflow RMS-Generate-Formblatt erstellt
- [ ] XLSX-Templates in SharePoint vorhanden
- [ ] LibreOffice headless installiert
- [ ] fill_xlsx_form.py vorhanden
- [ ] PDF wird in SharePoint gespeichert
- [ ] Formular-Auswahl-Dialog funktioniert

### Block 5: Auto-Refresh
- [ ] Dashboard aktualisiert sich alle 60s
- [ ] Schriftverkehr wird geladen

### Block 6: Integration
- [ ] showDetail() lädt alle Daten
- [ ] Alle Sektionen werden angezeigt

---

## 📚 REFERENZEN

| Resource | Wert |
|----------|------|
| Dashboard | https://osp.schneider-kabelsatzbau.de/rms/ |
| n8n | http://46.224.102.30:5678 |
| SharePoint RMS | https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS |
| anthropic-proxy | http://localhost:8080 |
| LibreOffice | `/usr/bin/libreoffice` |
| Scripts | `/opt/osp/scripts/` |

---

## 🔧 VORAUSSETZUNGEN PRÜFEN

```bash
# LibreOffice installiert?
which libreoffice || apt-get install -y libreoffice-calc libreoffice-writer

# Python-Pakete
pip install openpyxl python-docx --break-system-packages

# Scripts vorhanden?
ls /opt/osp/scripts/fill_xlsx_form.py
ls /opt/osp/scripts/convert_to_pdf.py

# Falls nicht, aus osp-formular-skill kopieren
```

---

*Erstellt: 2026-01-28 | Basierend auf: RMS_Strategie_v5.0, osp-formular-skill v1.1*
