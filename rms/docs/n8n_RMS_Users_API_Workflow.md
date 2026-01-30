# n8n Workflow: RMS-Users-API

**Erstellt:** 2026-01-29
**Zweck:** Laedt M365-Benutzer aus Graph API fuer RMS Dashboard

---

## Workflow-Konfiguration

### Grundeinstellungen
- **Name:** RMS-Users-API
- **Webhook Path:** rms-users
- **Trigger:** GET Request

---

## Nodes

### Node 1: Webhook Trigger

**Typ:** Webhook

**Einstellungen:**
```json
{
  "httpMethod": "GET",
  "path": "rms-users",
  "responseMode": "responseNode"
}
```

---

### Node 2: Get M365 Users

**Typ:** HTTP Request

**Einstellungen:**
```
Method: GET
URL: https://graph.microsoft.com/v1.0/users?$filter=accountEnabled eq true&$select=id,displayName,mail,jobTitle,department&$top=100
Authentication: OAuth2
Credential: Microsoft account (Fm3IuAbVYBYDIA4U)
```

**Wichtig:**
- Das Microsoft OAuth2 Credential muss die Berechtigung `User.Read.All` haben
- Filter: Nur aktive Benutzer (`accountEnabled eq true`)

---

### Node 3: Transform Users

**Typ:** Code

**JavaScript:**
```javascript
const users = $input.item.json.value || [];

// Benutzer transformieren fuer Frontend
const transformedUsers = users
  .filter(u => u.mail) // Nur Benutzer mit E-Mail
  .map(u => ({
    id: u.id,
    displayName: u.displayName || 'Unbekannt',
    mail: u.mail,
    jobTitle: u.jobTitle || '',
    department: u.department || '',
    // Kuerzel aus E-Mail extrahieren (vor dem @)
    kuerzel: u.mail.split('@')[0].substring(0, 2).toUpperCase()
  }))
  .sort((a, b) => a.displayName.localeCompare(b.displayName));

return { users: transformedUsers };
```

---

### Node 4: Respond to Webhook

**Typ:** Respond to Webhook

**Einstellungen:**
```json
{
  "respondWith": "json",
  "responseBody": "={{ $json }}"
}
```

---

## Workflow-Diagramm

```
[Webhook Trigger] --> [HTTP Request: Graph API] --> [Code: Transform] --> [Respond to Webhook]
```

---

## Test

Nach dem Aktivieren des Workflows:

```bash
# Lokaler Test (auf dem Server)
curl -s http://127.0.0.1:5678/webhook/rms-users | python3 -m json.tool

# Externer Test (ueber Nginx)
curl -s https://osp.schneider-kabelsatzbau.de/api/rms/users | python3 -m json.tool
```

**Erwartetes Ergebnis:**
```json
{
  "users": [
    {
      "id": "abc123...",
      "displayName": "Andreas Loehr",
      "mail": "a.loehr@schneider-kabelsatzbau.de",
      "jobTitle": "QM-Manager",
      "department": "Qualitaetsmanagement",
      "kuerzel": "A."
    },
    ...
  ]
}
```

---

## Nginx Route

Die Route wurde bereits in `/etc/nginx/sites-available/osp` hinzugefuegt:

```nginx
location = /api/rms/users {
    proxy_pass http://127.0.0.1:5678/webhook/rms-users;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}
```

---

## Fehlerbehebung

| Problem | Loesung |
|---------|---------|
| 401 Unauthorized | Microsoft OAuth2 Credential pruefen, Token erneuern |
| Leeres users Array | Graph API Filter pruefen, evtl. $top erhoehen |
| Workflow nicht erreichbar | Workflow aktivieren! |
| CORS-Fehler | Nginx Route pruefen |

---

## Fallback

Falls der n8n Workflow nicht verfuegbar ist, verwendet das Frontend die hardcodierte
`VERANTWORTLICHE`-Liste aus `massnahmen-templates.js` als Fallback.

---

*Autor: Claude Code*
*Datum: 2026-01-29*
