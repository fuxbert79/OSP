# Claude Code Prompt: RMS Dashboard - Editierbarkeit

**Datum:** 2026-01-28  
**Voraussetzung:** SERVER_SETUP_2026-01-28.md wurde umgesetzt  
**Ziel:** Detail-View editierbar machen (alle Felder inkl. KST)

---

## KONTEXT

### Bereits erledigt:
- ✅ Dashboard live unter https://osp.schneider-kabelsatzbau.de/rms/
- ✅ RMS-Detail-API Workflow aktiviert (Maßnahmen + Schriftverkehr)
- ✅ RMS-Massnahmen-API Workflow aktiviert
- ✅ Nginx-Routen konfiguriert
- ✅ Frontend mit Suche, Filter, Sort, Export, Charts

### Jetzt umzusetzen:
- 🔴 **Reklamation editieren** (alle Felder im Detail-View)
- 🔴 **KST manuell zuweisen** (Dropdown mit Kostenstellen)
- 🔴 **Maßnahmen editieren** (Status ändern, Termin anpassen)
- 🟡 **Inline-Edit oder Edit-Modal** (UX-Entscheidung)

---

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
CREDENTIAL_ID="Fm3IuAbVYBYDIA4U"
```

---

## AUFGABE 1: n8n Workflow - RMS-Update-API

Erstelle einen neuen Workflow für PATCH-Requests zum Aktualisieren von Reklamationen.

### Workflow: RMS-Update-Reklamation

**Webhook:** PATCH `/webhook/rms-update`

**Erwarteter Request-Body:**
```json
{
  "id": "123",
  "fields": {
    "KST": "1000",
    "Rekla_Status": "In Bearbeitung",
    "Prioritaet": "hoch",
    "Verantwortlich": "AL",
    "Zieldatum": "2026-02-15"
  }
}
```

**Nodes:**

1. **Webhook Trigger**
   - Method: PATCH
   - Path: `rms-update`
   - Response Mode: Last Node

2. **Update Reklamation** (HTTP Request)
   ```
   Method: PATCH
   URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/lists/${REKLAMATIONEN_LIST}/items/{{ $json.body.id }}
   Authentication: OAuth2 (Microsoft account - Fm3IuAbVYBYDIA4U)
   Headers:
     Content-Type: application/json
   Body (JSON):
   {
     "fields": {{ JSON.stringify($json.body.fields) }}
   }
   ```

3. **Success Response** (Code Node)
   ```javascript
   return {
     success: true,
     message: 'Reklamation aktualisiert',
     id: $json.id,
     updatedFields: Object.keys($input.item.json.fields || {})
   };
   ```

4. **Respond to Webhook**

### Workflow: RMS-Update-Massnahme

**Webhook:** PATCH `/webhook/rms-update-massnahme`

**Erwarteter Request-Body:**
```json
{
  "id": "456",
  "fields": {
    "Status": "Erledigt",
    "Termin": "2026-02-01",
    "Wirksamkeit": "Ja"
  }
}
```

**Nodes:** (analog zu oben, aber mit MASSNAHMEN_LIST)

---

## AUFGABE 2: Nginx Route hinzufügen

In `/etc/nginx/sites-available/osp`:

```nginx
# Update APIs (PATCH)
location /api/rms/update {
    proxy_pass http://127.0.0.1:5678/webhook/rms-update;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header Content-Type application/json;
}

location /api/rms/update-massnahme {
    proxy_pass http://127.0.0.1:5678/webhook/rms-update-massnahme;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header Content-Type application/json;
}
```

```bash
nginx -t && systemctl reload nginx
```

---

## AUFGABE 3: Frontend - Edit-Modus im Detail-View

### 3.1 Detail-Modal erweitern (index.html)

Ersetze die statischen Felder durch editierbare Inputs:

```html
<!-- Im Detail-Modal: Stammdaten-Sektion ersetzen -->
<div class="detail-section">
    <div class="section-header">
        <h3>📋 Stammdaten</h3>
        <button id="btn-edit-toggle" class="btn btn-sm" onclick="toggleEditMode()">
            ✏️ Bearbeiten
        </button>
    </div>
    
    <div id="detail-view-mode">
        <table id="detail-stammdaten"></table>
    </div>
    
    <div id="detail-edit-mode" style="display:none;">
        <form id="edit-reklamation-form">
            <div class="form-row">
                <div class="form-group">
                    <label>Typ</label>
                    <select id="edit-typ" class="form-control">
                        <option value="Intern">Intern</option>
                        <option value="Kunde">Kunde</option>
                        <option value="Lieferant">Lieferant</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <select id="edit-status" class="form-control">
                        <option value="Neu">Neu</option>
                        <option value="In Bearbeitung">In Bearbeitung</option>
                        <option value="Maßnahmen">Maßnahmen</option>
                        <option value="Abgeschlossen">Abgeschlossen</option>
                    </select>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Priorität</label>
                    <select id="edit-prioritaet" class="form-control">
                        <option value="kritisch">Kritisch</option>
                        <option value="hoch">Hoch</option>
                        <option value="mittel">Mittel</option>
                        <option value="niedrig">Niedrig</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Kostenstelle (KST)</label>
                    <select id="edit-kst" class="form-control">
                        <option value="">-- Auswählen --</option>
                        <option value="1000">1000 - Vertrieb</option>
                        <option value="2000">2000 - Einkauf</option>
                        <option value="3000">3000 - Produktion</option>
                        <option value="3100">3100 - F1 Fertigung</option>
                        <option value="3200">3200 - F2 Fertigung</option>
                        <option value="3300">3300 - F3 Fertigung</option>
                        <option value="4000">4000 - QM</option>
                        <option value="5000">5000 - Verwaltung</option>
                        <option value="6000">6000 - IT</option>
                    </select>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Verantwortlich</label>
                    <select id="edit-verantwortlich" class="form-control">
                        <option value="">-- Auswählen --</option>
                        <option value="AL">AL - Andreas Löhr</option>
                        <option value="CS">CS - Geschäftsführung</option>
                        <option value="SV">SV - Prokurist</option>
                        <option value="TS">TS - Einkauf</option>
                        <option value="SK">SK - Prüffeld</option>
                        <option value="MD">MD - Technik</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Zieldatum</label>
                    <input type="date" id="edit-zieldatum" class="form-control">
                </div>
            </div>
            
            <div class="form-group">
                <label>Titel</label>
                <input type="text" id="edit-title" class="form-control">
            </div>
            
            <div class="form-group">
                <label>Beschreibung</label>
                <textarea id="edit-beschreibung" class="form-control" rows="4"></textarea>
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">💾 Speichern</button>
                <button type="button" class="btn btn-secondary" onclick="toggleEditMode()">Abbrechen</button>
            </div>
        </form>
    </div>
</div>
```

### 3.2 JavaScript für Edit-Modus (app.js)

```javascript
// ============================================
// EDIT MODE
// ============================================

let isEditMode = false;

function toggleEditMode() {
    isEditMode = !isEditMode;
    
    document.getElementById('detail-view-mode').style.display = isEditMode ? 'none' : 'block';
    document.getElementById('detail-edit-mode').style.display = isEditMode ? 'block' : 'none';
    document.getElementById('btn-edit-toggle').textContent = isEditMode ? '❌ Abbrechen' : '✏️ Bearbeiten';
    
    if (isEditMode) {
        populateEditForm();
    }
}

function populateEditForm() {
    const data = window.currentReklamationData?.reklamation;
    if (!data) return;
    
    // Felder befüllen
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
        alert('Keine Reklamation ausgewählt');
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
            alert('✅ Reklamation gespeichert!');
            toggleEditMode();
            // Detail-View neu laden
            await showDetail(id);
            // Tabelle aktualisieren
            await loadData();
        } else {
            alert('❌ Fehler: ' + (result.error || 'Unbekannter Fehler'));
        }
    } catch (error) {
        console.error('Save error:', error);
        alert('❌ Fehler beim Speichern: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// Event-Listener für Edit-Form
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('edit-reklamation-form')?.addEventListener('submit', saveReklamation);
});
```

### 3.3 Maßnahmen editierbar machen

```javascript
// ============================================
// MASSNAHMEN EDIT
// ============================================

function renderMassnahmenTable(massnahmen) {
    if (!massnahmen || massnahmen.length === 0) {
        return '<tr><td colspan="5">Keine Maßnahmen erfasst</td></tr>';
    }
    
    const header = '<tr><th>Maßnahme</th><th>Typ</th><th>Termin</th><th>Status</th><th>Aktion</th></tr>';
    
    const rows = massnahmen.map(m => `
        <tr data-massnahme-id="${m.id}">
            <td>${m.Title || '--'}</td>
            <td>${m.Typ || '--'}</td>
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
                    <option value="Wirksamkeit prüfen" ${m.Status === 'Wirksamkeit prüfen' ? 'selected' : ''}>Wirksamkeit prüfen</option>
                </select>
            </td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="deleteMassnahme(${m.id})" title="Löschen">🗑️</button>
            </td>
        </tr>
    `).join('');
    
    return header + rows;
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
        
        console.log(`Maßnahme ${massnahmeId}: ${field} = ${value}`);
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Aktualisieren der Maßnahme');
    }
}

async function deleteMassnahme(massnahmeId) {
    if (!confirm('Maßnahme wirklich löschen?')) return;
    
    try {
        const response = await fetch(`/api/rms/delete-massnahme?id=${massnahmeId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            // Detail-View neu laden
            await showDetail(window.currentReklamationId);
        } else {
            alert('Fehler beim Löschen');
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Löschen');
    }
}

// In showDetail() die Maßnahmen-Tabelle mit der neuen Funktion rendern:
// document.getElementById('detail-massnahmen').innerHTML = renderMassnahmenTable(data.massnahmen);
```

### 3.4 CSS für Edit-Mode

```css
/* Edit Mode Styles */
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-bottom: 15px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    font-weight: 500;
    margin-bottom: 5px;
    color: var(--primary);
}

.form-control {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.95rem;
}

.form-control:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(0, 51, 102, 0.1);
}

.form-control-sm {
    padding: 4px 8px;
    font-size: 0.85rem;
    border: 1px solid #ddd;
    border-radius: 3px;
}

.form-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #eee;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.section-header h3 {
    margin: 0;
}

.btn-sm {
    padding: 4px 10px;
    font-size: 0.85rem;
}

.btn-danger {
    background: #dc3545;
    color: white;
    border: none;
}

.btn-danger:hover {
    background: #c82333;
}

/* Responsive */
@media (max-width: 600px) {
    .form-row {
        grid-template-columns: 1fr;
    }
}
```

---

## AUFGABE 4: Optional - Delete Maßnahme Workflow

Falls Löschen gewünscht ist:

**Webhook:** DELETE `/webhook/rms-delete-massnahme?id={id}`

```
Method: DELETE
URL: https://graph.microsoft.com/v1.0/sites/${SITE_ID}/lists/${MASSNAHMEN_LIST}/items/{{ $json.query.id }}
```

Nginx Route:
```nginx
location /api/rms/delete-massnahme {
    proxy_pass http://127.0.0.1:5678/webhook/rms-delete-massnahme;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}
```

---

## ✅ CHECKLISTE

Nach Abschluss prüfen:

- [ ] n8n Workflow "RMS-Update-Reklamation" erstellt und aktiv
- [ ] n8n Workflow "RMS-Update-Massnahme" erstellt und aktiv
- [ ] Nginx Routen für /api/rms/update und /api/rms/update-massnahme
- [ ] Edit-Button im Detail-Modal
- [ ] Edit-Formular mit allen Feldern (inkl. KST-Dropdown)
- [ ] Speichern funktioniert
- [ ] Maßnahmen-Status direkt änderbar
- [ ] Maßnahmen-Termin direkt änderbar
- [ ] Nach Speichern: Detail-View aktualisiert sich
- [ ] Nach Speichern: Tabelle aktualisiert sich

---

## 📚 REFERENZEN

| Resource | Wert |
|----------|------|
| Dashboard | https://osp.schneider-kabelsatzbau.de/rms/ |
| n8n | http://46.224.102.30:5678 |
| Frontend | /var/www/html/rms/ |
| Nginx Config | /etc/nginx/sites-available/osp |
| Reklamationen Liste | e9b1d926-085a-4435-a012-114ca9ba59a8 |
| Maßnahmen Liste | 3768f2d8-878c-4a5f-bd52-7486fe93289d |
| Credential | Fm3IuAbVYBYDIA4U |

---

## 🔧 GRAPH API PATCH FORMAT

Wichtig für SharePoint-Updates via Graph API:

```http
PATCH https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items/{item-id}
Content-Type: application/json

{
  "fields": {
    "FieldName1": "NewValue1",
    "FieldName2": "NewValue2"
  }
}
```

**Hinweis:** Nur die zu ändernden Felder im `fields`-Objekt senden!

---

*Erstellt: 2026-01-28 | Ziel: Editierbarkeit im RMS Dashboard*
