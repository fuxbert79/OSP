# NZA Integration - Nächste Schritte

**Stand:** 2026-01-30 18:00 Uhr
**Letzte Aktion:** Workflows in n8n importiert mit Microsoft Credentials

---

## Status-Übersicht

| Phase | Beschreibung | Status |
|-------|--------------|--------|
| 1 | Workflows erstellt | ✅ Fertig |
| 2 | Dashboard + Nginx | ✅ Fertig |
| 3 | n8n Import | ✅ Importiert (Aktivierung ausstehend) |
| 4 | Erweiterte APIs | ✅ Fertig |
| 5 | Dashboard-Erweiterung | ⏳ Nach Aktivierung |

---

## Phase 3: n8n Workflow Import (NÄCHSTER SCHRITT)

### 3.1 Workflows in n8n importieren

In n8n unter **Workflows → Import from File** diese Dateien importieren:

**Basis-Workflows (Phase 1):**
```
/mnt/HC_Volume_104189729/osp/nza/workflows/
├── 01_NZA_Setup_Listen.json        # Erstellt 5 SharePoint-Listen
├── 02_NZA_Setup_Spalten_KPL.json   # Fügt 40+ Spalten hinzu
├── 03_NZA_Import_Mitarbeiter.json  # Importiert 53 MA
├── 04_NZA_Import_Config.json       # Importiert Minutensätze etc.
├── 05_NZA_Prozesse_API.json        # Haupt-API (GET/POST/PATCH)
└── 06_NZA_Mitarbeiter_API.json     # Verursacher-Dropdown API
```

**Erweiterte APIs (Phase 4):**
```
├── 07_NZA_Massnahmen_API.json      # Maßnahmen CRUD (GET/POST/PATCH)
├── 08_NZA_Bilder_API.json          # Bilder-Metadaten (GET/POST)
├── 08b_NZA_Bilder_Upload.json      # Bilder-Upload zu SharePoint
├── 09_NZA_Notify_API.json          # Teams + E-Mail Benachrichtigung
├── 10_NZA_Kosten_API.json          # Kostenberechnung mit Minutensätzen
├── 11_NZA_Config_API.json          # Konfiguration abrufen
└── 12_NZA_KPIs_API.json            # KPI-Berechnung für Dashboard
```

### 3.2 Credentials zuweisen

Nach Import in jedem Workflow:
1. Workflow öffnen
2. HTTP Request Nodes anklicken
3. **"Microsoft OAuth2"** auswählen (wie bei RMS)
4. Speichern

### 3.3 Setup-Workflows ausführen (EINMALIG!)

**Reihenfolge wichtig:**
1. `01_NZA_Setup_Listen` → Manuell starten → Wartet bis fertig
2. `02_NZA_Setup_Spalten_KPL` → Manuell starten
3. `03_NZA_Import_Mitarbeiter` → Manuell starten
4. `04_NZA_Import_Config` → Manuell starten

### 3.4 Environment Variables setzen

In n8n unter **Settings → Variables** oder docker-compose.yml:

```env
NZA_SITE_ID=<wird von Workflow 01 ausgegeben>
NZA_KPL_LIST_ID=<List-ID von "NZA Hauptliste">
NZA_MITARBEITER_LIST_ID=<List-ID von "NZA Mitarbeiter">
NZA_CONFIG_LIST_ID=<List-ID von "NZA Konfiguration">
NZA_MASSNAHMEN_LIST_ID=<List-ID von "NZA Maßnahmen">
NZA_BILDER_LIST_ID=<List-ID von "NZA Bilder">
```

### 3.5 API-Workflows aktivieren

**Basis-APIs:**
1. `05_NZA_Prozesse_API` → Toggle ON
2. `06_NZA_Mitarbeiter_API` → Toggle ON

**Erweiterte APIs (Phase 4):**
3. `07_NZA_Massnahmen_API` → Toggle ON
4. `08_NZA_Bilder_API` → Toggle ON
5. `08b_NZA_Bilder_Upload` → Toggle ON
6. `09_NZA_Notify_API` → Toggle ON
7. `10_NZA_Kosten_API` → Toggle ON
8. `11_NZA_Config_API` → Toggle ON
9. `12_NZA_KPIs_API` → Toggle ON

---

## Bereits konfigurierte Nginx-Endpoints

```
/nza/                    → Dashboard (HTML)
/api/nza/prozesse        → Haupt-API (GET/POST/PATCH)
/api/nza/mitarbeiter     → Verursacher-Lookup (GET)
/api/nza/massnahmen      → Maßnahmen-API (GET/POST/PATCH)
/api/nza/notify          → Teams/E-Mail-Benachrichtigung (POST)
/api/nza/bilder          → Bilder abrufen (GET/POST)
/api/nza/bilder-upload   → Bilder hochladen (POST, max 20MB)
/api/nza/kosten          → Kostenberechnung (GET/POST)
/api/nza/config          → Konfiguration (GET)
/api/nza/kpis            → KPI-Daten (GET)
```

---

## API-Dokumentation (Phase 4 Workflows)

### 07_NZA_Massnahmen_API

**GET** `/api/nza/massnahmen?nzaId=NZA-26-0001`
- Lädt alle Maßnahmen zu einem NZA-Vorgang

**POST** `/api/nza/massnahmen`
```json
{
  "nzaId": "NZA-26-0001",
  "titel": "Nachschulung Werker",
  "typ": "Korrekturmaßnahme",
  "beschreibung": "Werker muss nachgeschult werden",
  "verantwortlichId": "user-guid",
  "verantwortlichName": "Max Mustermann",
  "verantwortlichEmail": "mm@schneider-kabelsatzbau.de",
  "termin": "2026-02-15",
  "notifyTeams": true,
  "notifyEmail": false
}
```

**PATCH** `/api/nza/massnahmen`
```json
{
  "id": "sharepoint-item-id",
  "status": "Abgeschlossen",
  "wirksamkeit": "Wirksam"
}
```

### 08_NZA_Bilder_API / 08b_NZA_Bilder_Upload

**GET** `/api/nza/bilder?nzaId=NZA-26-0001`
- Lädt alle Bilder zu einem NZA-Vorgang

**POST** `/api/nza/bilder-upload`
```json
{
  "nzaId": "NZA-26-0001",
  "bildData": "base64-encoded-image-data",
  "extension": "jpg",
  "kategorie": "Fehlerbild",
  "titel": "Beschädigte Crimphülse",
  "bemerkung": "Sichtbare Risse",
  "hochgeladenVon": "AL"
}
```

### 09_NZA_Notify_API

**POST** `/api/nza/notify`
```json
{
  "nzaId": "NZA-26-0001",
  "massnahmeId": "sharepoint-item-id",
  "titel": "Sofortmaßnahme zugewiesen",
  "beschreibung": "Bitte prüfen Sie die Charge 12345",
  "typ": "Sofortmaßnahme",
  "termin": "2026-02-01",
  "verantwortlichId": "user-guid",
  "verantwortlichEmail": "mm@schneider-kabelsatzbau.de",
  "verantwortlichName": "Max Mustermann",
  "notifyTeams": true,
  "notifyEmail": true
}
```

### 10_NZA_Kosten_API

**GET** `/api/nza/kosten`
- Gibt Minutensätze zurück

**POST** `/api/nza/kosten`
```json
{
  "nzaId": "NZA-26-0001",
  "prozesse": [
    { "prozess": "Crimpen", "werker": "AB", "kst": "1000", "zeit": 30 },
    { "prozess": "Prüfen", "werker": "CD", "kst": "5000", "zeit": 15 }
  ],
  "kostenMaterial": 25.50,
  "kostenSonstige": 0
}
```

**Response:**
```json
{
  "berechnung": {
    "prozesse": [
      { "nr": 1, "prozess": "Crimpen", "kst": "1000", "zeit": 30, "minutensatz": 1.98, "kosten": 59.40 },
      { "nr": 2, "prozess": "Prüfen", "kst": "5000", "zeit": 15, "minutensatz": 1.02, "kosten": 15.30 }
    ],
    "kostenProzesse": 74.70,
    "kostenMaterial": 25.50,
    "kostenSonstige": 0,
    "kostenGesamt": 100.20
  }
}
```

### 11_NZA_Config_API

**GET** `/api/nza/config`
- Lädt alle Konfigurationswerte

**GET** `/api/nza/config?key=NZA_ID_COUNTER`
- Lädt einen spezifischen Wert

### 12_NZA_KPIs_API

**GET** `/api/nza/kpis`
**GET** `/api/nza/kpis?year=2026`
- Berechnet KPIs für Dashboard

**Response:**
```json
{
  "filter": { "year": 2026 },
  "kpis": {
    "offeneNza": 12,
    "anzahlYtd": 45,
    "anzahlMtd": 8,
    "kostenYtd": 3450.80,
    "kostenMtd": 620.50
  },
  "charts": {
    "typVerteilung": { "Nacharbeit": 25, "Neufertigung": 12, "Ausschuss": 8 },
    "topKst": [{ "kst": "1000", "anzahl": 15 }],
    "topFehlerursachen": [{ "ursache": "Maschine", "anzahl": 10 }],
    "monatsTrend": [{ "monat": "2026-01", "anzahl": 8, "kosten": 620.50 }]
  }
}
```

---

## Test-URLs

```bash
# Dashboard
https://osp.schneider-kabelsatzbau.de/nza/

# APIs (nach n8n Aktivierung)
curl https://osp.schneider-kabelsatzbau.de/api/nza/mitarbeiter
curl https://osp.schneider-kabelsatzbau.de/api/nza/prozesse
curl https://osp.schneider-kabelsatzbau.de/api/nza/config
curl https://osp.schneider-kabelsatzbau.de/api/nza/kpis
curl https://osp.schneider-kabelsatzbau.de/api/nza/kosten
```

---

## Wichtige Dateien

| Pfad | Beschreibung |
|------|--------------|
| `/var/www/html/nza/` | Dashboard (deployed) |
| `/etc/nginx/sites-available/osp` | Nginx Config (Zeilen 201-321) |
| `/mnt/HC_Volume_104189729/osp/nza/workflows/` | n8n Workflow JSONs |
| `/mnt/HC_Volume_104189729/osp/nza/docs/` | Dokumentation |

---

## Phase 5: Dashboard-Erweiterung (NÄCHSTER SCHRITT nach n8n Import)

Nach erfolgreicher Aktivierung der APIs:
- [ ] Dashboard um Maßnahmen-Tab erweitern
- [ ] Bilder-Galerie mit Upload-Funktion
- [ ] KPI-Charts einbinden
- [ ] Kostenberechnung im Formular

---

*Erstellt: 2026-01-30*
*Aktualisiert: 2026-01-30 17:15*
