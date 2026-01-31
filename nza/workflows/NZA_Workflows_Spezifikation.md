# NZA n8n Workflows - Spezifikation

**Erstellt:** 2026-01-30
**n8n Server:** http://127.0.0.1:5678
**Credentials:** OSP-n8n-Integration (Microsoft OAuth2)

---

## Übersicht der Workflows

| Workflow | Webhook-Path | Methoden | Priorität |
|----------|--------------|----------|-----------|
| NZA-Prozesse-API | /webhook/nza-prozesse | GET, POST, PATCH | 🔴 |
| NZA-Mitarbeiter-API | /webhook/nza-mitarbeiter | GET | 🔴 |
| NZA-Massnahmen-API | /webhook/nza-massnahmen | GET, POST, PATCH | 🔴 |
| NZA-Notify-Massnahme | /webhook/nza-notify | POST | 🔴 |
| NZA-Bilder-API | /webhook/nza-bilder | GET | 🔴 |
| NZA-Bilder-Upload | /webhook/nza-bilder-upload | POST | 🔴 |
| NZA-Kosten-API | /webhook/nza-kosten | GET, POST | 🔴 |
| NZA-Config-API | /webhook/nza-config | GET | 🟢 |
| NZA-KPIs-API | /webhook/nza-kpis | GET | 🟢 |

---

## 1. NZA-Prozesse-API

### Workflow-Aufbau

```
[Webhook Trigger] → [Switch (Method)] → [GET/POST/PATCH Branch] → [Response]
```

### GET: Liste abrufen

**Request:**
```
GET /api/nza/prozesse
GET /api/nza/prozesse?status=Neu
GET /api/nza/prozesse?kst=1000
GET /api/nza/prozesse?id=NZA-26-0001
```

**SharePoint Query:**
```
GET https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items
?$expand=fields
&$filter=fields/status eq 'Neu'
&$orderby=fields/field_2 desc
&$top=100
```

**Response Transform:**
```javascript
const items = $input.first().json.value || [];

return items.map(item => ({
  id: item.id,
  nzaId: item.fields.Title,
  typ: item.fields.field_1,
  datum: item.fields.field_2,
  artikel: item.fields.field_3,
  verursacher: item.fields.field_7,
  kst: item.fields.field_9,
  beschreibung: item.fields.field_14,
  kategorien: item.fields.field_15,
  status: item.fields.status,
  kostenGesamt: item.fields.kosten_gesamt_neu || 0
}));
```

### POST: Neuen NZA-Vorgang anlegen

**Request:**
```json
POST /api/nza/prozesse
{
  "typ": "Interne Reklamation",
  "datum": "2026-01-30",
  "artikel": "KB-12345",
  "verursacher": "MD",
  "kst": "1000",
  "beschreibung": "Crimpfehler bei 15 Stück",
  "kategorien": ["Crimpfehler"],
  "prozesse": [
    {"prozess": "Nachcrimpen", "werker": "MD", "kst": "1000", "zeit": 30}
  ],
  "kostenMaterial": 5.50,
  "kostenSonstige": 0
}
```

**Workflow Steps:**
1. **Generate NZA-ID:**
   ```javascript
   // Letzte ID aus Config holen
   const counter = $input.item.json.NZA_ID_COUNTER || 0;
   const year = new Date().getFullYear().toString().slice(-2);
   const nextId = (counter + 1).toString().padStart(4, '0');
   return { nzaId: `NZA-${year}-${nextId}` };
   ```

2. **Calculate Costs:**
   ```javascript
   const MINUTENSATZ = {
     '1000': 1.98, '2000': 1.21, '3000': 0.93,
     '4000': 1.02, '5000': 1.02, 'Lager': 1.10, 'Verwaltung': 1.37
   };

   let kostenProzesse = 0;
   const prozesse = $input.item.json.prozesse || [];

   prozesse.forEach((p, i) => {
     const faktor = MINUTENSATZ[p.kst] || 0;
     kostenProzesse += p.zeit * faktor;
   });

   const kostenGesamt = kostenProzesse +
     ($input.item.json.kostenMaterial || 0) +
     ($input.item.json.kostenSonstige || 0);

   return { kostenProzesse, kostenGesamt };
   ```

3. **Create SharePoint Item**

4. **Update Config Counter**

5. **Respond with created item**

### PATCH: Vorgang aktualisieren

**Request:**
```json
PATCH /api/nza/prozesse
{
  "id": "123",
  "status": "Abgeschlossen",
  "abschlussBemerkung": "Nacharbeit erfolgreich"
}
```

---

## 2. NZA-Mitarbeiter-API

### GET: Alle Mitarbeiter

**Request:**
```
GET /api/nza/mitarbeiter
GET /api/nza/mitarbeiter?kst=1000
GET /api/nza/mitarbeiter?aktiv=true
```

**Response Transform:**
```javascript
const items = $input.first().json.value || [];

const mitarbeiter = items
  .filter(item => item.fields.Aktiv === true)
  .map(item => ({
    id: item.id,
    kuerzel: item.fields.Kuerzel,
    name: item.fields.Title,
    abteilung: item.fields.Abteilung,
    kst: item.fields.KST,
    funktion: item.fields.Funktion,
    email: item.fields.Email || ''
  }))
  .sort((a, b) => a.name.localeCompare(b.name));

return { mitarbeiter, count: mitarbeiter.length };
```

---

## 3. NZA-Massnahmen-API + Notify

### POST: Maßnahme anlegen

**Request:**
```json
POST /api/nza/massnahmen
{
  "nzaId": "NZA-26-0001",
  "titel": "Nachschulung Crimpen",
  "typ": "Korrekturmaßnahme",
  "beschreibung": "MA MD erhält Nachschulung",
  "verantwortlichEmail": "m.duetzer@schneider-kabelsatzbau.de",
  "termin": "2026-02-15",
  "notifyTeams": true,
  "notifyEmail": false
}
```

### Teams Notification

**Graph API - Activity Notification:**
```javascript
const payload = {
  topic: {
    source: "text",
    value: `Neue Maßnahme zu ${nzaId}`,
    webUrl: `https://osp.schneider-kabelsatzbau.de/nza/?id=${nzaId}`
  },
  activityType: "taskCreated",
  previewText: {
    content: `${massnahmenTyp}: ${titel}`
  },
  recipient: {
    "@odata.type": "microsoft.graph.aadUserNotificationRecipient",
    userId: verantwortlichId
  }
};
```

**Graph API - Chat Message (Alternative):**
```
POST https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}/messages
{
  "body": {
    "contentType": "html",
    "content": "<b>Neue Maßnahme</b><br>NZA: NZA-26-0001<br>..."
  }
}
```

---

## 4. NZA-Bilder-API + Upload

### GET: Bilder zu einem NZA

**Request:**
```
GET /api/nza/bilder?nzaId=NZA-26-0001
```

### POST: Bild hochladen

**Request:**
```json
POST /api/nza/bilder-upload
{
  "nzaId": "NZA-26-0001",
  "filename": "fehlerbild_001.jpg",
  "kategorie": "Fehlerbild",
  "base64Data": "data:image/jpeg;base64,..."
}
```

**Workflow Steps:**
1. Decode Base64
2. Create folder in SharePoint: `/NZA_Bilder/{Jahr}/{NZA-ID}/`
3. Upload file via Graph API
4. Get sharing link
5. Create entry in nza-bilder list
6. Respond with URLs

---

## 5. NZA-Kosten-API

### Kostenberechnung (Code Node)

```javascript
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

const data = $input.item.json;
let kostenProzesse = 0;
const details = [];

// 5 Prozesse berechnen
for (let i = 1; i <= 5; i++) {
  const zeit = parseFloat(data[`zeit_${i}`]) || 0;
  const kst = data[`kostenstelle_${i}`] || '';
  const faktor = MINUTENSATZ[kst] || 0;
  const kosten = Math.round(zeit * faktor * 100) / 100;

  if (zeit > 0) {
    details.push({
      prozess: i,
      zeit: zeit,
      kst: kst,
      faktor: faktor,
      kosten: kosten
    });
  }
  kostenProzesse += kosten;
}

const kostenMaterial = parseFloat(data.kosten_material) || 0;
const kostenSonstige = parseFloat(data.kosten_sonstige) || 0;
const kostenGesamt = Math.round((kostenProzesse + kostenMaterial + kostenSonstige) * 100) / 100;

return {
  details: details,
  kosten_prozesse: kostenProzesse,
  kosten_material: kostenMaterial,
  kosten_sonstige: kostenSonstige,
  kosten_gesamt: kostenGesamt
};
```

---

## SharePoint Graph API Referenzen

### Site ID ermitteln
```
GET https://graph.microsoft.com/v1.0/sites/rainerschneiderkabelsatz.sharepoint.com:/sites/NZA_NEU
```

### Listen abrufen
```
GET https://graph.microsoft.com/v1.0/sites/{site-id}/lists
```

### Items aus Liste
```
GET https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items?$expand=fields
```

### Item erstellen
```
POST https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items
{
  "fields": {
    "Title": "NZA-26-0001",
    "field_1": "Interne Reklamation",
    ...
  }
}
```

### Item aktualisieren
```
PATCH https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items/{item-id}/fields
{
  "status": "Abgeschlossen"
}
```

---

## Nginx Endpoints (zur Referenz)

```nginx
# Alle NZA-Endpoints
location = /api/nza/prozesse      { proxy_pass http://127.0.0.1:5678/webhook/nza-prozesse; ... }
location = /api/nza/mitarbeiter   { proxy_pass http://127.0.0.1:5678/webhook/nza-mitarbeiter; ... }
location = /api/nza/massnahmen    { proxy_pass http://127.0.0.1:5678/webhook/nza-massnahmen; ... }
location = /api/nza/notify        { proxy_pass http://127.0.0.1:5678/webhook/nza-notify; ... }
location = /api/nza/bilder        { proxy_pass http://127.0.0.1:5678/webhook/nza-bilder; ... }
location = /api/nza/bilder-upload { proxy_pass http://127.0.0.1:5678/webhook/nza-bilder-upload; client_max_body_size 20M; ... }
location = /api/nza/kosten        { proxy_pass http://127.0.0.1:5678/webhook/nza-kosten; ... }
location = /api/nza/config        { proxy_pass http://127.0.0.1:5678/webhook/nza-config; ... }
location = /api/nza/kpis          { proxy_pass http://127.0.0.1:5678/webhook/nza-kpis; ... }
```

---

*Erstellt: 2026-01-30*
