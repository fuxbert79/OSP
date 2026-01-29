# RMS Phase 2 - Tracking & Jahresfilter Implementation Report

**Datum:** 2026-01-29
**Autor:** Claude Code
**Status:** Abgeschlossen

---

## Zusammenfassung

Erweiterung des RMS-Dashboards um erweiterte Tracking-Funktionalitaet fuer Lieferantenreklamationen sowie einen Jahresfilter zur besseren Navigation.

---

## Implementierte Features

### 1. Erweiterte Tracking-Sektion

**Dateien:** `index.html`, `app.js`, `style.css`

Die Tracking-Sektion fuer Lieferantenreklamationen wurde vollstaendig ueberarbeitet:

| Tracking-Punkt | Icon | Felder |
|----------------|------|--------|
| Ersatzlieferung | 📦 | Checkbox + Datum |
| Ruecksendung | ↩️ | Checkbox + Datum |
| Gutschrift | 💰 | Checkbox + Datum + Betrag (EUR) |

**Funktionsweise:**
- Beim Aktivieren einer Checkbox erscheint das zugehoerige Datumsfeld
- Datum dient als Erinnerungstermin
- Alle Daten werden in SharePoint gespeichert

### 2. Tracking-Icons in Dashboard-Tabelle

**Neue Spalte:** "Track" (nach NZA)

| Status | Darstellung |
|--------|-------------|
| Inaktiv | Grau/transparent |
| Aktiv | Volle Deckkraft |
| Ueberfaellig | Blinkend (CSS Animation) |

**Tooltip:** Zeigt Datum und ggf. Betrag an

### 3. Jahresfilter

**Position:** Header, neben "Neue Reklamation" Button

**Optionen:**
- 2026 (Standard/vorausgewaehlt)
- 2025
- 2024
- Alle Jahre (leer)

**Filter-Logik:** Basiert auf `Erfassungsdatum` der Reklamation

### 4. Automatische Erinnerungen (n8n Workflow)

**Workflow:** `RMS-Tracking-Erinnerung`
**ID:** `0UupmQ8VzknBG5fJ`

**Zeitplan:** Mo-Fr, 08:00 Uhr

**Ablauf:**
1. Liest alle Reklamationen aus SharePoint
2. Filtert Lieferanten-Reklamationen mit aktiven Tracking-Punkten
3. Prueft ob Tracking-Datum <= heute
4. Gruppiert nach Verantwortlichem
5. Sendet E-Mail-Erinnerung via Microsoft Graph API

**E-Mail-Inhalt:**
- Liste aller faelligen/ueberfaelligen Termine
- Status-Markierung (heute faellig / ueberfaellig)
- Gutschrift-Betrag falls vorhanden
- Link zum Dashboard

---

## Neue SharePoint-Spalten

| Spaltenname | Typ | Beschreibung |
|-------------|-----|--------------|
| `Tracking_Ersatz_Datum` | DateTime | Erinnerungsdatum Ersatzlieferung |
| `Tracking_Rueck_Datum` | DateTime | Erinnerungsdatum Ruecksendung |
| `Tracking_Gut_Datum` | DateTime | Erinnerungsdatum Gutschrift |

Diese Spalten wurden zur bestehenden RMS-Reklamationen Liste hinzugefuegt.

---

## Geaenderte Dateien

### Frontend

| Datei | Aenderungen |
|-------|-------------|
| `index.html` | Tracking-Sektion HTML, Jahresfilter, Track-Spalte |
| `js/app.js` | Tracking-Funktionen, Jahresfilter, Icon-Rendering |
| `css/style.css` | Tracking-Grid, Header-Actions, Icon-Styles |

### n8n Workflows

| Workflow | ID | Status |
|----------|-----|--------|
| RMS-Tracking-Erinnerung | `0UupmQ8VzknBG5fJ` | Aktiv |
| RMS-Add-Tracking-Date-Columns | `lVaPBw5RstS2Zj1r` | Einmalig ausgefuehrt |
| RMS-Reklamationen | `TU48Qxw2nQ638DNg` | Repariert (webhookId) |
| RMS-KPIs | `ybUNZLNA0YqVJYpu` | Repariert (webhookId) |
| RMS-Charts | `7q0bGtiRYpVmbATe` | Repariert (webhookId) |

### Nginx

| Datei | Aenderungen |
|-------|-------------|
| `/etc/nginx/sites-available/osp` | Korrigierte Proxy-URLs fuer RMS APIs |

---

## Behobene Fehler

1. **OAuth Token abgelaufen** - Manueller Reconnect in n8n erforderlich
2. **Fehlende webhookId** - RMS-Reklamationen, KPIs, Charts Workflows repariert
3. **Falsche Proxy-URLs** - nginx Konfiguration korrigiert
4. **Stammdaten-API 403** - Workflow auf RMS-Liste umgestellt (Fallback implementiert)

---

## Testhinweise

### Tracking testen
1. Dashboard oeffnen: https://osp.schneider-kabelsatzbau.de/rms/
2. Lieferanten-Reklamation auswaehlen (z.B. QA-26017)
3. Tracking-Sektion sollte sichtbar sein
4. Checkbox aktivieren -> Datumsfeld erscheint
5. Datum setzen und "Tracking speichern" klicken
6. In Tabelle: Track-Spalte zeigt aktive Icons

### Jahresfilter testen
1. Dropdown im Header auf "2025" stellen
2. Tabelle zeigt nur Reklamationen aus 2025
3. "Alle Jahre" zeigt alle Eintraege

### Erinnerungs-Workflow testen
1. n8n UI oeffnen: https://n8n.schneider-kabelsatzbau.de
2. Workflow "RMS-Tracking-Erinnerung" oeffnen
3. "Execute Workflow" klicken
4. Ausgabe pruefen

---

## Offene Punkte / Empfehlungen

1. **Verantwortlichen-Mapping:** Aktuell werden E-Mails an AL gesendet. Fuer produktiven Einsatz sollte das Mapping Verantwortlicher -> E-Mail implementiert werden.

2. **Teams-Benachrichtigung:** Alternativ/zusaetzlich zu E-Mail koennte eine Teams-Nachricht gesendet werden.

3. **Absender-Stammdaten:** Die Absender-Felder in den Reklamationen sollten gepflegt werden, damit das Autocomplete funktioniert.

---

## Dashboard-URL

**Produktion:** https://osp.schneider-kabelsatzbau.de/rms/

---

*Report erstellt am 2026-01-29 um 23:30 Uhr*
