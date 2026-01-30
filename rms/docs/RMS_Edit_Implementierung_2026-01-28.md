# RMS Dashboard - Edit-Funktionalität Implementierung

**Datum:** 2026-01-28
**Commit:** `1e5d54f feat(rms): Edit-Funktionalität für Dashboard implementiert`
**Status:** Live auf https://osp.schneider-kabelsatzbau.de/rms/

---

## Zusammenfassung

Die Edit-Funktionalität wurde vollständig implementiert, sodass Reklamationen und Maßnahmen direkt im Dashboard bearbeitet werden können. Änderungen werden in Echtzeit an SharePoint übermittelt.

---

## Implementierte Features

### 1. Reklamation bearbeiten

Im Detail-Modal wurde ein "Bearbeiten"-Button hinzugefügt, der ein Formular mit folgenden Feldern öffnet:

| Feld | Typ | Optionen |
|------|-----|----------|
| Typ | Dropdown | Intern, Kunde, Lieferant |
| Status | Dropdown | Neu, In Bearbeitung, Maßnahmen, Abgeschlossen |
| Priorität | Dropdown | Kritisch, Hoch, Mittel, Niedrig |
| KST | Dropdown | F1, F2, F3, QM, EK, VT, IT, VW |
| Verantwortlich | Dropdown | AL, CS, CA, SV, TS, SK, MD |
| Zieldatum | Datepicker | - |
| Titel | Textfeld | - |
| Beschreibung | Textarea | - |

### 2. Maßnahmen Inline-Edit

Die Maßnahmen-Tabelle wurde um Inline-Edit-Funktionalität erweitert:

- **Termin:** Direkt änderbar via Datepicker
- **Status:** Direkt änderbar via Dropdown (Offen, In Arbeit, Erledigt, Wirksamkeit prüfen)
- **Löschen:** Button zum Entfernen einer Maßnahme

---

## Technische Änderungen

### Frontend

#### index.html
- Edit-Button im Detail-Modal Header
- Verstecktes Edit-Formular mit allen Feldern
- Maßnahmen-Tabelle mit Aktion-Spalte

#### app.js
Neue Funktionen:
```javascript
toggleEditMode()      // Wechsel zwischen Ansicht/Bearbeitung
populateEditForm()    // Formular mit aktuellen Daten befüllen
saveReklamation()     // Änderungen an API senden
renderMassnahmenTable() // Maßnahmen mit Inline-Edit rendern
updateMassnahmeField()  // Einzelnes Feld aktualisieren
deleteMassnahme()       // Maßnahme löschen
```

#### style.css
Neue CSS-Klassen:
- `.form-row` - Zwei-Spalten-Layout für Formular
- `.section-header` - Header mit Button
- `.btn-sm`, `.btn-danger` - Button-Styles
- `.form-control-sm` - Kompakte Formular-Elemente
- Responsive Anpassungen für Mobile

### Backend (n8n Workflows)

| Workflow | ID | Webhook | Methode |
|----------|-----|---------|---------|
| RMS-Update-Reklamation | bmEAINTP2lPNORLp | /webhook/rms-update | PATCH |
| RMS-Update-Massnahme | TAw3Ktjc8xKEd0i7 | /webhook/rms-update-massnahme | PATCH |
| RMS-Delete-Massnahme | QHdEILUhV8j4kXeS | /webhook/rms-delete-massnahme | DELETE |
| RMS-Detail-API | 5jruolIhqcOGu3GQ | /webhook/rms-detail | GET |

### Nginx-Routen

Folgende Routen wurden in `/etc/nginx/sites-available/osp` hinzugefügt:

```nginx
location = /api/rms/detail {
    proxy_pass http://127.0.0.1:5678/webhook/rms-detail;
    ...
}

location = /api/rms/update {
    proxy_pass http://127.0.0.1:5678/webhook/rms-update;
    ...
}

location = /api/rms/update-massnahme {
    proxy_pass http://127.0.0.1:5678/webhook/rms-update-massnahme;
    ...
}

location = /api/rms/delete-massnahme {
    proxy_pass http://127.0.0.1:5678/webhook/rms-delete-massnahme;
    ...
}
```

---

## API-Dokumentation

### PATCH /api/rms/update

Aktualisiert eine Reklamation in SharePoint.

**Request:**
```json
{
  "id": "1",
  "fields": {
    "Title": "Neuer Titel",
    "Rekla_Status": "In Bearbeitung",
    "Prioritaet": "hoch"
  }
}
```

**Response:** SharePoint Item-Objekt

### PATCH /api/rms/update-massnahme

Aktualisiert eine Maßnahme in SharePoint.

**Request:**
```json
{
  "id": "5",
  "fields": {
    "Status": "Erledigt",
    "Termin": "2026-02-15"
  }
}
```

### DELETE /api/rms/delete-massnahme?id={id}

Löscht eine Maßnahme aus SharePoint.

### GET /api/rms/detail?id={id}

Lädt Reklamation mit Details.

**Response:**
```json
{
  "reklamation": { ... },
  "massnahmen": [ ... ],
  "schriftverkehr": [],
  "sharePointUrl": "https://..."
}
```

---

## Geänderte Dateien

| Datei | Änderung |
|-------|----------|
| `rms/dashboard/index.html` | Edit-Modal, Formular, Maßnahmen-Tabelle |
| `rms/dashboard/js/app.js` | Edit-Funktionen, API-Calls |
| `rms/dashboard/css/style.css` | Edit-Mode Styles |
| `rms/workflows/RMS-Update-Reklamation.json` | Neuer Workflow |
| `rms/workflows/RMS-Update-Massnahme.json` | Neuer Workflow |
| `rms/workflows/RMS-Delete-Massnahme.json` | Neuer Workflow |
| `rms/docs/SERVER_SETUP_EDIT_2026-01-28.md` | Setup-Dokumentation |
| `/etc/nginx/sites-available/osp` | Neue API-Routen |

---

## Tests

| Test | Ergebnis |
|------|----------|
| API: Reklamationen laden | ✓ 20 Einträge |
| API: Detail laden | ✓ QA-26013 |
| API: Update ausführen | ✓ HTTP 200 |
| Frontend: Edit-Button | ✓ Vorhanden |
| Frontend: Edit-Funktionen | ✓ Vorhanden |
| Frontend: Styles | ✓ Vorhanden |

---

## Nutzung

1. Dashboard öffnen: https://osp.schneider-kabelsatzbau.de/rms/
2. Auf eine Reklamation klicken
3. "Bearbeiten" Button klicken
4. Felder ändern
5. "Speichern" klicken

Für Maßnahmen:
- Termin/Status direkt in der Tabelle ändern
- "X" Button zum Löschen

---

## Bekannte Einschränkungen

- Schriftverkehr wird noch nicht geladen (Liste nicht konfiguriert)
- Maßnahmen-ID muss als Lookup-ID übergeben werden
- Keine Validierung der Eingaben im Frontend

---

## Nächste Schritte

- [ ] Schriftverkehr-Integration
- [ ] Formular-Validierung
- [ ] Neue Maßnahme erstellen (Modal existiert bereits)
- [ ] Erfolgsmeldungen verbessern

---

*Erstellt: 2026-01-28 | Autor: Claude Code*
