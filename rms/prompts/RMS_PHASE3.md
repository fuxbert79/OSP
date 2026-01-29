# Claude Code Prompt: RMS Phase 2 - Verbleibende Roadmap-Punkte

**Datum:** 2026-01-29  
**Arbeitsverzeichnis:** `/mnt/HC_Volume_104189729/osp/`  
**Server:** Hetzner CX43 (46.224.102.30)  
**Ziel:** Alle offenen RMS-Punkte aus der Roadmap abschließen

---

## 🔧 UMGEBUNG

```bash
# Arbeitsverzeichnis Claude Code
cd /mnt/HC_Volume_104189729/osp/

# n8n API
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMmFlMi1mNzQyLTQxZGUtYTY1OS0xNTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5NTM4MTcwLCJleHAiOjE3NzcyNDA4MDB9.NsECcQH9N-UsiCmXrZkMGLg6ioFbGCuNXWW_XaJAUTY"
export N8N_BASE_URL="http://127.0.0.1:5678"

# Pfade
FRONTEND="/var/www/html/rms/"
OSP_DIR="/mnt/HC_Volume_104189729/osp/"
RMS_DIR="/mnt/HC_Volume_104189729/osp/rms/"
SCRIPTS="/opt/osp/scripts/"
```

---

## 📋 SHAREPOINT REFERENZ

```bash
SITE_ID="rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c"
REKLAMATIONEN_LIST="e9b1d926-085a-4435-a012-114ca9ba59a8"
MASSNAHMEN_LIST="3768f2d8-878c-4a5f-bd52-7486fe93289d"
SCHRIFTVERKEHR_LIST="741c6ae8-88bb-406b-bf85-2e11192a528f"
CREDENTIAL_ID="Fm3IuAbVYBYDIA4U"
```

---

## ✅ BEREITS ERLEDIGT (Phase 1)

| Aufgabe | Status |
|---------|--------|
| PDF-Generierung | ✅ Funktioniert |
| Detail-View Speichern | ✅ Funktioniert |
| Header-Text | ✅ Ergänzt |
| Typ-Filter (Kunde/Lieferant) | ✅ Angepasst |
| KST + CSV entfernt | ✅ Erledigt |
| M365-Benutzer Integration | ✅ 35 Benutzer aus Graph API |
| Spalte "Zuletzt bearbeitet" | ✅ Hinzugefügt |

---

## 🎯 AUFGABEN PHASE 2

### AUFGABE 1: Pagination (20 Einträge pro Seite)

**Datei:** `/var/www/html/rms/js/app.js`

**Neue globale Variablen:**
```javascript
// Pagination
const ITEMS_PER_PAGE = 20;
let currentPage = 1;
let totalPages = 1;
```

**Neue Funktion `paginateData()`:**
```javascript
function paginateData(data) {
    totalPages = Math.ceil(data.length / ITEMS_PER_PAGE);
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    return data.slice(start, end);
}
```

**Funktion `updateTable()` anpassen:**
```javascript
function updateTable(data) {
    // Pagination anwenden
    const paginatedData = paginateData(data);
    
    // ... bestehender Table-Rendering-Code mit paginatedData ...
    
    // Pagination-Controls aktualisieren
    renderPaginationControls(data.length);
}
```

**Neue Funktion `renderPaginationControls()`:**
```javascript
function renderPaginationControls(totalItems) {
    const container = document.getElementById('pagination-controls');
    if (!container) return;
    
    totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
    
    let html = '<div class="pagination">';
    
    // Zurück-Button
    html += `<button class="btn btn-sm ${currentPage === 1 ? 'disabled' : ''}" 
             onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
             ← Zurück</button>`;
    
    // Seiten-Anzeige
    html += `<span class="pagination-info">Seite ${currentPage} von ${totalPages} (${totalItems} Einträge)</span>`;
    
    // Vor-Button
    html += `<button class="btn btn-sm ${currentPage === totalPages ? 'disabled' : ''}" 
             onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
             Weiter →</button>`;
    
    html += '</div>';
    
    container.innerHTML = html;
}

function changePage(page) {
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    applyFilters(); // Neu rendern mit aktueller Seite
}
```

**HTML hinzufügen in `/var/www/html/rms/index.html`:**
```html
<!-- Nach der Tabelle, vor </main> -->
<div id="pagination-controls" class="pagination-container"></div>
```

**CSS in `/var/www/html/rms/css/style.css`:**
```css
/* Pagination */
.pagination-container {
    display: flex;
    justify-content: center;
    padding: 20px 0;
    margin-top: 20px;
}

.pagination {
    display: flex;
    align-items: center;
    gap: 15px;
}

.pagination-info {
    color: #666;
    font-size: 0.9rem;
}

.pagination .btn {
    padding: 8px 16px;
}

.pagination .btn.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
```

---

### AUFGABE 2: E-Mail/Teams Benachrichtigungs-Auswahl

**Datei:** `/var/www/html/rms/index.html`

**Im Maßnahmen-Modal die Checkbox erweitern:**
```html
<div class="form-group">
    <label>Benachrichtigung</label>
    <div class="notification-options">
        <label class="checkbox-inline">
            <input type="checkbox" id="notify-email" checked> Per E-Mail
        </label>
        <label class="checkbox-inline">
            <input type="checkbox" id="notify-teams"> Per Teams
        </label>
    </div>
</div>
```

**Datei:** `/var/www/html/rms/js/app.js`

**Funktion `createMassnahmeWithNotification()` anpassen:**
```javascript
async function createMassnahmeWithNotification() {
    // ... bestehender Code zum Erstellen der Maßnahme ...
    
    const notifyEmail = document.getElementById('notify-email')?.checked || false;
    const notifyTeams = document.getElementById('notify-teams')?.checked || false;
    
    if (notifyEmail || notifyTeams) {
        // Verantwortlichen aus m365Users finden
        const verantwortlichValue = document.getElementById('massnahme-verantwortlich')?.value;
        const verantwortlicher = m365Users.find(u => 
            u.mail === verantwortlichValue || u.displayName === verantwortlichValue
        );
        
        if (verantwortlicher) {
            const notifyPayload = {
                qaId: window.currentReklamationId,
                reklaTitle: window.currentReklamationData?.Title || '',
                massnahme: {
                    title: document.getElementById('massnahme-title')?.value,
                    typ: document.getElementById('massnahme-typ')?.value,
                    termin: document.getElementById('massnahme-termin')?.value,
                    beschreibung: document.getElementById('massnahme-beschreibung')?.value
                },
                verantwortlich: {
                    id: verantwortlicher.id,
                    displayName: verantwortlicher.displayName,
                    mail: verantwortlicher.mail
                },
                notifyEmail: notifyEmail,
                notifyTeams: notifyTeams,
                ersteller: 'System',
                dashboardUrl: window.location.href
            };
            
            try {
                await fetch('/api/rms/notify-massnahme', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(notifyPayload)
                });
            } catch (e) {
                console.error('Benachrichtigung fehlgeschlagen:', e);
            }
        }
    }
    
    // ... Rest der Funktion ...
}
```

**n8n Workflow `RMS-Notify-Massnahme` erweitern:**

Füge einen Branch für Teams-Benachrichtigung hinzu:

**Node: Check Notification Type (Code)**
```javascript
const notifyEmail = $json.body?.notifyEmail || false;
const notifyTeams = $json.body?.notifyTeams || false;

return {
    ...$json.body,
    notifyEmail,
    notifyTeams
};
```

**Node: Send Teams Message (HTTP Request)** - Nur wenn `notifyTeams === true`
```
Method: POST
URL: https://graph.microsoft.com/v1.0/users/{{ $json.verantwortlich.id }}/teamwork/sendActivityNotification
Authentication: OAuth2
Body:
```
```json
{
    "topic": {
        "source": "text",
        "value": "Neue Maßnahme zugewiesen",
        "webUrl": "{{ $json.dashboardUrl }}"
    },
    "activityType": "taskCreated",
    "previewText": {
        "content": "{{ $json.massnahme.title }}"
    },
    "recipient": {
        "@odata.type": "microsoft.graph.aadUserNotificationRecipient",
        "userId": "{{ $json.verantwortlich.id }}"
    }
}
```

---

### AUFGABE 3: E-Mail-Spam-Filter verbessern

**n8n Workflow:** `RMS-Email-Import` (bestehend)

**Im E-Mail-Parser Node erweitern:**
```javascript
const subject = $json.subject?.toLowerCase() || '';
const from = $json.from?.toLowerCase() || '';
const body = $json.bodyPreview?.toLowerCase() || '';

// Spam-Keywords
const spamKeywords = [
    'newsletter', 'unsubscribe', 'abmelden', 'werbung', 'angebot', 
    'rabatt', 'gutschein', 'gewinnspiel', 'lottery', 'winner',
    'viagra', 'casino', 'bitcoin', 'crypto', 'investment opportunity',
    'click here', 'act now', 'limited time', 'free gift',
    'no obligation', 'risk free', 'satisfaction guaranteed'
];

// Whitelist-Domains (immer durchlassen)
const whitelistDomains = [
    'schneider-kabelsatzbau.de',
    'wuerth.de', 'wuerth.com',
    'te.com', 'teconnectivity.com',
    'wago.com', 'weidmueller.com',
    'phoenix-contact.com'
    // Weitere wichtige Lieferanten/Kunden hinzufügen
];

// Blacklist-Domains (immer blockieren)
const blacklistDomains = [
    'spam.com', 'marketing.com', 'promo.com'
];

// Prüfung
const fromDomain = from.split('@')[1] || '';

// Whitelist hat Vorrang
const isWhitelisted = whitelistDomains.some(d => fromDomain.includes(d));

// Blacklist prüfen
const isBlacklisted = blacklistDomains.some(d => fromDomain.includes(d));

// Spam-Keywords prüfen
const hasSpamKeyword = spamKeywords.some(kw => 
    subject.includes(kw) || body.includes(kw)
);

// Reklamations-Keywords (positiv)
const reklaKeywords = ['reklamation', 'beschwerde', 'mangel', 'fehler', 'defekt', 
                       'qualität', 'qa-', 'rücksendung', 'ersatz', 'gutschrift'];
const hasReklaKeyword = reklaKeywords.some(kw => 
    subject.includes(kw) || body.includes(kw)
);

// Entscheidung
let isSpam = false;
let reason = '';

if (isWhitelisted) {
    isSpam = false;
    reason = 'Whitelisted domain';
} else if (isBlacklisted) {
    isSpam = true;
    reason = 'Blacklisted domain';
} else if (hasSpamKeyword && !hasReklaKeyword) {
    isSpam = true;
    reason = 'Spam keyword detected';
} else {
    isSpam = false;
    reason = 'Passed checks';
}

return {
    ...$json,
    isSpam,
    spamReason: reason,
    fromDomain
};
```

---

### AUFGABE 4: Lieferanten-Reklamation über Dashboard erfassen

**Neue Sektion im Dashboard oder Modal für "Neue Reklamation"**

**Datei:** `/var/www/html/rms/index.html`

**Button im Header hinzufügen:**
```html
<button id="btn-neue-rekla" class="btn btn-primary" onclick="showNeueReklamationModal()">
    + Neue Reklamation
</button>
```

**Modal für neue Reklamation:**
```html
<!-- Modal: Neue Reklamation -->
<div id="modal-neue-rekla" class="modal" style="display: none;">
    <div class="modal-content modal-large">
        <div class="modal-header">
            <h2>Neue Reklamation erfassen</h2>
            <button class="close-btn" onclick="closeNeueReklamationModal()">&times;</button>
        </div>
        <div class="modal-body">
            <form id="form-neue-rekla">
                <!-- Typ -->
                <div class="form-group">
                    <label for="neue-rekla-typ">Reklamationstyp *</label>
                    <select id="neue-rekla-typ" class="form-control" required onchange="toggleReklaFields()">
                        <option value="">-- Auswählen --</option>
                        <option value="Lieferant">Lieferantenreklamation</option>
                        <option value="Kunde">Kundenreklamation</option>
                    </select>
                </div>
                
                <!-- Absender (Autocomplete aus Stammdaten) -->
                <div class="form-group">
                    <label for="neue-rekla-absender">Lieferant / Kunde *</label>
                    <input type="text" id="neue-rekla-absender" class="form-control" 
                           list="stammdaten-datalist" placeholder="Name eingeben..." required>
                    <datalist id="stammdaten-datalist"></datalist>
                </div>
                
                <!-- Titel -->
                <div class="form-group">
                    <label for="neue-rekla-titel">Titel / Betreff *</label>
                    <input type="text" id="neue-rekla-titel" class="form-control" 
                           placeholder="Kurzbeschreibung des Problems" required>
                </div>
                
                <!-- Beschreibung -->
                <div class="form-group">
                    <label for="neue-rekla-beschreibung">Beschreibung *</label>
                    <textarea id="neue-rekla-beschreibung" class="form-control" rows="5" 
                              placeholder="Detaillierte Fehlerbeschreibung..." required></textarea>
                </div>
                
                <!-- Priorität -->
                <div class="form-group">
                    <label for="neue-rekla-prioritaet">Priorität</label>
                    <select id="neue-rekla-prioritaet" class="form-control">
                        <option value="mittel">Mittel</option>
                        <option value="niedrig">Niedrig</option>
                        <option value="hoch">Hoch</option>
                        <option value="kritisch">Kritisch</option>
                    </select>
                </div>
                
                <!-- Verantwortlich -->
                <div class="form-group">
                    <label for="neue-rekla-verantwortlich">Verantwortlich</label>
                    <select id="neue-rekla-verantwortlich" class="form-control">
                        <option value="">-- Auswählen --</option>
                        <!-- Wird dynamisch mit M365-Benutzern befüllt -->
                    </select>
                </div>
                
                <!-- Lieferanten-spezifische Felder -->
                <div id="lieferant-fields" style="display: none;">
                    <hr>
                    <h4>Lieferanten-Details</h4>
                    
                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label for="neue-rekla-lieferschein">Lieferschein-Nr.</label>
                            <input type="text" id="neue-rekla-lieferschein" class="form-control">
                        </div>
                        <div class="form-group col-md-6">
                            <label for="neue-rekla-lieferdatum">Lieferdatum</label>
                            <input type="date" id="neue-rekla-lieferdatum" class="form-control">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label for="neue-rekla-artikel">Artikel-Nr.</label>
                            <input type="text" id="neue-rekla-artikel" class="form-control">
                        </div>
                        <div class="form-group col-md-6">
                            <label for="neue-rekla-menge">Beanstandete Menge</label>
                            <input type="number" id="neue-rekla-menge" class="form-control">
                        </div>
                    </div>
                </div>
                
                <!-- Buttons -->
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeNeueReklamationModal()">Abbrechen</button>
                    <button type="submit" class="btn btn-primary">Reklamation anlegen</button>
                </div>
            </form>
        </div>
    </div>
</div>
```

**JavaScript-Funktionen in `/var/www/html/rms/js/app.js`:**

```javascript
// ============================================
// NEUE REKLAMATION ERFASSEN
// ============================================

function showNeueReklamationModal() {
    const modal = document.getElementById('modal-neue-rekla');
    if (modal) {
        modal.style.display = 'flex';
        // Verantwortlich-Dropdown befüllen
        populateUserDropdown('neue-rekla-verantwortlich');
        // Stammdaten-Datalist befüllen
        populateStammdatenDatalist();
        // Formular zurücksetzen
        document.getElementById('form-neue-rekla')?.reset();
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
    populateStammdatenDatalist(typ);
}

function populateStammdatenDatalist(typ = '') {
    const datalist = document.getElementById('stammdaten-datalist');
    if (!datalist) return;
    
    // Aus Cache filtern (falls Stammdaten geladen)
    let filtered = [];
    if (typ === 'Kunde') {
        filtered = stammdatenCache.kunden || [];
    } else if (typ === 'Lieferant') {
        filtered = stammdatenCache.lieferanten || [];
    } else {
        filtered = [...(stammdatenCache.kunden || []), ...(stammdatenCache.lieferanten || [])];
    }
    
    datalist.innerHTML = filtered.map(s => 
        `<option value="${s.name}">${s.name} (${s.debKredNr})</option>`
    ).join('');
}

// Formular absenden
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-neue-rekla');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await createNeueReklamation();
        });
    }
});

async function createNeueReklamation() {
    const payload = {
        Rekla_Typ: document.getElementById('neue-rekla-typ')?.value,
        Absender: document.getElementById('neue-rekla-absender')?.value,
        Title: document.getElementById('neue-rekla-titel')?.value,
        Beschreibung: document.getElementById('neue-rekla-beschreibung')?.value,
        Prioritaet: document.getElementById('neue-rekla-prioritaet')?.value || 'mittel',
        Verantwortlich: document.getElementById('neue-rekla-verantwortlich')?.value,
        Rekla_Status: 'Neu',
        Erfassungsdatum: new Date().toISOString().split('T')[0]
    };
    
    // Lieferanten-Felder hinzufügen falls vorhanden
    if (payload.Rekla_Typ === 'Lieferant') {
        payload.Lieferschein_Nr = document.getElementById('neue-rekla-lieferschein')?.value;
        payload.Lieferdatum = document.getElementById('neue-rekla-lieferdatum')?.value;
        payload.Artikel_Nr = document.getElementById('neue-rekla-artikel')?.value;
        payload.Beanstandete_Menge = document.getElementById('neue-rekla-menge')?.value;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch('/api/rms/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            alert(`✅ Reklamation ${result.qaId} erfolgreich angelegt!`);
            closeNeueReklamationModal();
            await loadData(); // Dashboard aktualisieren
        } else {
            alert('❌ Fehler: ' + (result.error || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('Reklamation erstellen fehlgeschlagen:', error);
        alert('❌ Fehler: ' + error.message);
    } finally {
        showLoading(false);
    }
}
```

**n8n Workflow erstellen:** `RMS-Create-Reklamation`

**Webhook:** POST `/webhook/rms-create`

**Nodes:**
1. Webhook Trigger
2. Load Config (QA-ID Zähler)
3. Generate QA-ID
4. Create SharePoint Item
5. Update Config
6. Create Folder (in SharePoint)
7. Respond

**Nginx Route hinzufügen:**
```nginx
location = /api/rms/create {
    proxy_pass http://127.0.0.1:5678/webhook/rms-create;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}
```

---

### AUFGABE 5: Antwort-E-Mail generieren + versenden

**Button im Detail-Modal hinzufügen:**
```html
<button id="btn-antwort-email" class="btn btn-secondary" onclick="showAntwortEmailModal()">
    📧 Antwort-E-Mail
</button>
```

**Modal für Antwort-E-Mail:**
```html
<!-- Modal: Antwort-E-Mail -->
<div id="modal-antwort-email" class="modal" style="display: none;">
    <div class="modal-content modal-large">
        <div class="modal-header">
            <h2>Antwort-E-Mail generieren</h2>
            <button class="close-btn" onclick="closeAntwortEmailModal()">&times;</button>
        </div>
        <div class="modal-body">
            <div class="form-group">
                <label for="email-empfaenger">Empfänger</label>
                <input type="email" id="email-empfaenger" class="form-control" placeholder="E-Mail-Adresse">
            </div>
            
            <div class="form-group">
                <label for="email-betreff">Betreff</label>
                <input type="text" id="email-betreff" class="form-control">
            </div>
            
            <div class="form-group">
                <label for="email-vorlage">Vorlage</label>
                <select id="email-vorlage" class="form-control" onchange="applyEmailTemplate()">
                    <option value="">-- Vorlage wählen --</option>
                    <option value="eingangsbestaetigung">Eingangsbestätigung</option>
                    <option value="nachfrage">Nachfrage / Rückfrage</option>
                    <option value="ersatzlieferung">Ersatzlieferung anfordern</option>
                    <option value="gutschrift">Gutschrift anfordern</option>
                    <option value="ruecksendung">Rücksendung ankündigen</option>
                    <option value="abschluss">Abschlussmeldung</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="email-text">Nachricht</label>
                <textarea id="email-text" class="form-control" rows="12"></textarea>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" id="email-anhang-formular"> F-QM-02 als Anhang
                </label>
            </div>
            
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeAntwortEmailModal()">Abbrechen</button>
                <button type="button" class="btn btn-primary" onclick="sendAntwortEmail()">📤 E-Mail senden</button>
            </div>
        </div>
    </div>
</div>
```

**JavaScript-Funktionen:**
```javascript
// E-Mail-Vorlagen
const EMAIL_TEMPLATES = {
    eingangsbestaetigung: {
        betreff: 'Eingangsbestätigung Ihrer Reklamation {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

wir bestätigen den Eingang Ihrer Reklamation und haben diese unter der Nummer {QA_ID} erfasst.

Betreff: {TITEL}

Wir werden die Angelegenheit prüfen und uns schnellstmöglich bei Ihnen melden.

Mit freundlichen Grüßen
Qualitätsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    },
    ersatzlieferung: {
        betreff: 'Anforderung Ersatzlieferung zu {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

bezugnehmend auf unsere Reklamation {QA_ID} bitten wir um schnellstmögliche Ersatzlieferung.

Betroffener Artikel: {ARTIKEL}
Menge: {MENGE}

Bitte bestätigen Sie den Liefertermin.

Mit freundlichen Grüßen
Qualitätsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    },
    gutschrift: {
        betreff: 'Anforderung Gutschrift zu {QA_ID}',
        text: `Sehr geehrte Damen und Herren,

bezugnehmend auf unsere Reklamation {QA_ID} bitten wir um Ausstellung einer Gutschrift.

Begründung: {BESCHREIBUNG}

Mit freundlichen Grüßen
Qualitätsmanagement
Rainer Schneider Kabelsatzbau GmbH & Co. KG`
    },
    // Weitere Vorlagen...
};

function showAntwortEmailModal() {
    const modal = document.getElementById('modal-antwort-email');
    if (!modal) return;
    
    const rekla = window.currentReklamationData;
    if (!rekla) {
        alert('Keine Reklamation ausgewählt');
        return;
    }
    
    // Felder vorbelegen
    document.getElementById('email-betreff').value = `Re: ${rekla.QA_ID} - ${rekla.Title}`;
    document.getElementById('email-empfaenger').value = rekla.Absender_Email || '';
    
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
    const rekla = window.currentReklamationData || {};
    
    // Platzhalter ersetzen
    let betreff = template.betreff
        .replace('{QA_ID}', rekla.QA_ID || '')
        .replace('{TITEL}', rekla.Title || '');
    
    let text = template.text
        .replace(/{QA_ID}/g, rekla.QA_ID || '')
        .replace(/{TITEL}/g, rekla.Title || '')
        .replace(/{BESCHREIBUNG}/g, rekla.Beschreibung || '')
        .replace(/{ARTIKEL}/g, rekla.Artikel_Nr || '')
        .replace(/{MENGE}/g, rekla.Beanstandete_Menge || '');
    
    document.getElementById('email-betreff').value = betreff;
    document.getElementById('email-text').value = text;
}

async function sendAntwortEmail() {
    const payload = {
        qaId: window.currentReklamationData?.QA_ID,
        empfaenger: document.getElementById('email-empfaenger')?.value,
        betreff: document.getElementById('email-betreff')?.value,
        text: document.getElementById('email-text')?.value,
        anhangFormular: document.getElementById('email-anhang-formular')?.checked
    };
    
    if (!payload.empfaenger || !payload.betreff || !payload.text) {
        alert('Bitte alle Felder ausfüllen');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch('/api/rms/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            alert('✅ E-Mail erfolgreich gesendet!');
            closeAntwortEmailModal();
        } else {
            alert('❌ Fehler: ' + (result.error || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('E-Mail senden fehlgeschlagen:', error);
        alert('❌ Fehler: ' + error.message);
    } finally {
        showLoading(false);
    }
}
```

**n8n Workflow erstellen:** `RMS-Send-Email`

**Webhook:** POST `/webhook/rms-send-email`

**Nodes:**
1. Webhook Trigger
2. Code: Prepare Email
3. HTTP Request: Send via Graph API (Mail.Send)
4. Code: Create Schriftverkehr Entry
5. HTTP Request: Create Schriftverkehr Item
6. Respond

---

### AUFGABE 6: Tracking (Ersatzmaterial / Rücksendung / Gutschrift)

**SharePoint-Liste "RMS-Reklamationen" erweitern:**

Neue Spalten (falls nicht vorhanden):
- `Tracking_Status` (Choice): Offen, Ersatzlieferung angefordert, Rücksendung, Gutschrift angefordert, Abgeschlossen
- `Tracking_Ersatzlieferung` (Boolean)
- `Tracking_Ruecksendung` (Boolean)
- `Tracking_Gutschrift` (Boolean)
- `Tracking_Gutschrift_Betrag` (Number)
- `Tracking_Bemerkung` (Multiline Text)

**Im Detail-Modal Tracking-Sektion hinzufügen:**
```html
<!-- Tracking-Sektion (nur für Lieferanten-Reklas) -->
<div id="tracking-section" class="detail-section" style="display: none;">
    <h4>📦 Tracking</h4>
    <div class="tracking-options">
        <label class="checkbox-inline">
            <input type="checkbox" id="tracking-ersatz" onchange="updateTracking()"> 
            Ersatzlieferung angefordert
        </label>
        <label class="checkbox-inline">
            <input type="checkbox" id="tracking-ruecksendung" onchange="updateTracking()"> 
            Rücksendung
        </label>
        <label class="checkbox-inline">
            <input type="checkbox" id="tracking-gutschrift" onchange="updateTracking()"> 
            Gutschrift
        </label>
    </div>
    <div id="gutschrift-betrag-container" style="display: none;">
        <label for="tracking-gutschrift-betrag">Gutschrift-Betrag (€)</label>
        <input type="number" id="tracking-gutschrift-betrag" class="form-control" step="0.01">
    </div>
    <div class="form-group">
        <label for="tracking-bemerkung">Bemerkung</label>
        <textarea id="tracking-bemerkung" class="form-control" rows="2"></textarea>
    </div>
    <button class="btn btn-sm btn-primary" onclick="saveTracking()">Tracking speichern</button>
</div>
```

---

## ✅ CHECKLISTE

### Pagination
- [ ] Globale Variablen hinzugefügt
- [ ] `paginateData()` Funktion erstellt
- [ ] `updateTable()` angepasst
- [ ] `renderPaginationControls()` erstellt
- [ ] HTML-Container hinzugefügt
- [ ] CSS-Styles hinzugefügt
- [ ] Test: 20 Einträge pro Seite

### Benachrichtigungen
- [ ] Checkboxen für E-Mail/Teams im Modal
- [ ] `createMassnahmeWithNotification()` erweitert
- [ ] n8n Workflow für Teams-Nachricht

### Spam-Filter
- [ ] Whitelist-Domains definiert
- [ ] Blacklist-Domains definiert
- [ ] Spam-Keywords erweitert
- [ ] n8n E-Mail-Import Workflow aktualisiert

### Lieferanten-Erfassung
- [ ] Button "Neue Reklamation" im Header
- [ ] Modal für neue Reklamation
- [ ] JavaScript-Funktionen
- [ ] n8n Workflow `RMS-Create-Reklamation`
- [ ] Nginx Route `/api/rms/create`

### Antwort-E-Mail
- [ ] Button im Detail-Modal
- [ ] Modal für E-Mail-Erstellung
- [ ] E-Mail-Vorlagen
- [ ] n8n Workflow `RMS-Send-Email`
- [ ] Nginx Route `/api/rms/send-email`

### Tracking
- [ ] SharePoint-Spalten hinzufügen (falls nötig)
- [ ] Tracking-Sektion im Detail-Modal
- [ ] JavaScript-Funktionen

---

## 📝 REPORT

Nach Abschluss Report erstellen:
`/mnt/HC_Volume_104189729/osp/rms/docs/RMS_Phase2_Report_2026-01-29.md`

---

*Erstellt: 2026-01-29*
