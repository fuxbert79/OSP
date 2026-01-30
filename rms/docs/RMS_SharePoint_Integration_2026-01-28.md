# RMS Dashboard - SharePoint Integration

**Datum:** 2026-01-28
**Erstellt von:** Claude Code (Opus 4.5)
**Auftraggeber:** AL (Andreas Löhr)

---

## Zusammenfassung

Die RMS Dashboard APIs wurden von Mock-Daten auf echte SharePoint-Integration umgestellt. Das Dashboard zeigt nun Live-Daten aus der SharePoint-Liste "Reklamationen".

---

## Durchgeführte Arbeiten

### 1. n8n Workflows aktualisiert

Drei bestehende Mock-Workflows wurden auf SharePoint-Integration umgestellt:

| Workflow | ID | Funktion |
|----------|-----|----------|
| **RMS-KPIs** | `ybUNZLNA0YqVJYpu` | Berechnet KPIs aus SharePoint-Daten |
| **RMS-Reklamationen** | `TU48Qxw2nQ638DNg` | Lädt Reklamationen-Liste |
| **RMS-Charts** | `7q0bGtiRYpVmbATe` | Aggregiert Chart-Daten |

#### RMS-KPIs Workflow
- Webhook: `GET /webhook/rms-kpis`
- SharePoint-Abfrage der Reklamationen-Liste
- Code Node berechnet:
  - Offene Reklamationen (Status ≠ Abgeschlossen)
  - Kritische (Priorität = kritisch)
  - Überfällige (Zieldatum < heute)
  - Durchschnittliche Bearbeitungszeit

#### RMS-Reklamationen Workflow
- Webhook: `GET /webhook/rms-reklamationen`
- Gibt SharePoint-Rohdaten zurück
- Transformation erfolgt clientseitig (für bessere Performance)

#### RMS-Charts Workflow
- Webhook: `GET /webhook/rms-charts`
- Aggregiert:
  - Trend: Reklamationen pro Monat (letzte 6 Monate)
  - Typ-Verteilung: Kunde / Lieferant / Intern
  - KST-Verteilung: Top 6 Kostenstellen

### 2. Frontend aktualisiert

**Datei:** `/var/www/html/rms/js/app.js`

Änderungen:
- `fetchReklamationen()`: Transformation der SharePoint-Rohdaten (`value[].fields`)
- `fetchReklamationDetail()`: Lädt Details aus der Reklamationen-Liste
- Client-seitige Filterung nach Typ, Status, KST

### 3. Dokumentation erstellt

**Datei:** `/mnt/HC_Volume_104189729/osp/rms/workflows/rms_dashboard_sharepoint.json`

Enthält die vollständige Workflow-Konfiguration als JSON-Export für Backup/Dokumentation.

---

## Technische Details

### SharePoint-Konfiguration

| Parameter | Wert |
|-----------|------|
| **Site ID** | `rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c` |
| **Reklamationen Liste** | `e9b1d926-085a-4435-a012-114ca9ba59a8` |
| **Maßnahmen Liste** | `3768f2d8-878c-4a5f-bd52-7486fe93289d` |
| **Schriftverkehr Liste** | `741c6ae8-88bb-406b-bf85-2e11192a528f` |
| **OAuth Credentials** | `Fm3IuAbVYBYDIA4U` (Microsoft account) |

### API-Endpoints

| Endpoint | Nginx Proxy | n8n Webhook |
|----------|-------------|-------------|
| `/api/rms/kpis` | `http://127.0.0.1:5678/webhook/ybUNZLNA0YqVJYpu/webhook/rms-kpis` |
| `/api/rms/reklamationen` | `http://127.0.0.1:5678/webhook/TU48Qxw2nQ638DNg/webhook/rms-reklamationen` |
| `/api/rms/charts` | `http://127.0.0.1:5678/webhook/7q0bGtiRYpVmbATe/webhook/rms-charts` |

### Graph API Abfragen

```
GET https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists/{LIST_ID}/items
    ?$expand=fields
    &$top=500
```

---

## Aktuelle Live-Daten (Stand: 2026-01-28 09:15)

```json
{
  "offen": 19,
  "kritisch": 2,
  "ueberfaellig": 0,
  "durchschnitt": 0,
  "gesamt": 19,
  "abgeschlossen": 0
}
```

### Chart-Daten
- **Trend (letzte 6 Monate):** Aug=0, Sep=0, Okt=0, Nov=0, Dez=1, Jan=18
- **Typ-Verteilung:** Kunde=15, Lieferant=1, Intern=3
- **Top KST:** Unbekannt=14, 1000=2, 2000=1, 3000=1, Verwaltung=1

---

## Git Commits

```
00bc052 feat(rms): SharePoint-Integration für Dashboard APIs
1903b9b fix(rms): Korrekten n8n API-Key in Prompt aktualisiert
6b126ba feat(rms): Dashboard Phase 1d-1e - Frontend und n8n API
```

---

## Bekannte Einschränkungen

1. **Reklamationen-Workflow:** Gibt SharePoint-Rohdaten zurück (Code Node führte zu Fehlern). Transformation erfolgt clientseitig.

2. **Detail-Ansicht:** Maßnahmen und Schriftverkehr werden noch nicht aus separaten Listen geladen (TODO).

3. **Durchschnittliche Bearbeitungszeit:** Zeigt 0 Tage, da noch keine Reklamationen abgeschlossen wurden.

---

## Nächste Schritte

- [ ] Maßnahmen-Liste in Detail-View integrieren
- [ ] Schriftverkehr-Liste in Detail-View integrieren
- [ ] KST-Daten bereinigen (viele "Unbekannt")
- [ ] Performance-Optimierung: Caching der SharePoint-Daten

---

## URLs

| Ressource | URL |
|-----------|-----|
| **Dashboard** | https://osp.schneider-kabelsatzbau.de/rms/ |
| **n8n** | http://46.224.102.30:5678 |
| **SharePoint RMS** | https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS |

---

*Bericht erstellt am 2026-01-28 um 09:15 Uhr*
