# NZA Integration - Fortsetzungs-Prompt

**Stand:** 2026-01-30 18:00 Uhr
**Letzte Session:** Phase 4 Workflows erstellt + in n8n importiert

---

## Aktueller Status

### Erledigt
- [x] Phase 1-2: Basis-Workflows (01-06) erstellt
- [x] Phase 4: Erweiterte API-Workflows (07-12) erstellt
- [x] Alle Workflows haben `active: false` und `versionId`
- [x] Microsoft OAuth2 Credentials (`Fm3IuAbVYBYDIA4U`) in allen Workflows eingetragen
- [x] Alle 13 Workflows in n8n importiert
- [x] Dashboard + Nginx bereits konfiguriert (Phase 2)

### Offen
- [ ] Duplikate in n8n löschen (ältere Workflows ohne korrekte Credentials)
- [ ] Setup-Workflow 01 "NZA-Setup-Listen" ausführen (erstellt SharePoint-Listen)
- [ ] Setup-Workflows 02-04 ausführen
- [ ] Environment Variables in n8n setzen
- [ ] API-Workflows 05-12 aktivieren (Toggle ON)
- [ ] Dashboard JavaScript für neue APIs erweitern

---

## Workflow-Dateien

Pfad: `/mnt/HC_Volume_104189729/osp/nza/workflows/`

| Datei | Zweck | Priorität |
|-------|-------|-----------|
| 01_NZA_Setup_Listen.json | Erstellt 5 SharePoint-Listen | Setup |
| 02_NZA_Setup_Spalten_KPL.json | Fügt 40+ Spalten hinzu | Setup |
| 03_NZA_Import_Mitarbeiter.json | Importiert 53 MA | Setup |
| 04_NZA_Import_Config.json | Importiert Minutensätze | Setup |
| 05_NZA_Prozesse_API.json | Haupt-API (GET/POST/PATCH) | API |
| 06_NZA_Mitarbeiter_API.json | Verursacher-Dropdown | API |
| 07_NZA_Massnahmen_API.json | Maßnahmen CRUD | API |
| 08_NZA_Bilder_API.json | Bilder-Metadaten | API |
| 08b_NZA_Bilder_Upload.json | Bilder zu SharePoint | API |
| 09_NZA_Notify_API.json | Teams + E-Mail | API |
| 10_NZA_Kosten_API.json | Kostenberechnung | API |
| 11_NZA_Config_API.json | Konfiguration | API |
| 12_NZA_KPIs_API.json | Dashboard KPIs | API |

---

## n8n Workflow IDs (neue Version mit Credentials)

```
4UxTgP9oB3d84H5T | NZA-Setup-Listen
qb4TZt4Rk9CZaGPx | NZA-Setup-Spalten-KPL
w2ZyCRMiaxQRzaKH | NZA-Import-Mitarbeiter
LDetjPMPVZOogLfo | NZA-Import-Config
WnpFuELKUKNw79ds | NZA-Prozesse-API
ZvJpRq0wdhC4YfBW | NZA-Mitarbeiter-API
2xOO0YUC5l9LfMGR | NZA-Massnahmen-API
UJ7RJD0DeFXxuxA8 | NZA-Bilder-API
y91eVjGIxl3swsrC | NZA-Bilder-Upload
Rr5Q1MOC9OqnmIn8 | NZA-Notify-API
p39KiN09ymLc4At0 | NZA-Kosten-API
gZGILPeWxpE9jkWJ | NZA-Config-API
qlxm6EhO1fldQBgw | NZA-KPIs-API
```

### Zu löschende Duplikate (alte Version ohne Credentials)
```
JpnsrTrYghu6C754 | NZA-Setup-Listen
1eLV8SqCbh4MDpzk | NZA-Setup-Listen
0b088ww1ZqTTD3GZ | NZA-Setup-Spalten-KPL
CaAAvXXWPXFjJ1SM | NZA-Import-Mitarbeiter
CXv0ILdewQK1u2EI | NZA-Import-Config
jvTeauNg0dCT8CFp | NZA-Prozesse-API
CO5Zp3ARaj5pngHx | NZA-Mitarbeiter-API
hmV9lfwZLeQNU3un | NZA-Massnahmen-API
PM5Wn1HTp09mh207 | NZA-Bilder-API
cP4W5XwATwYZZeCx | NZA-Bilder-Upload
qOkB2tBL3BUDHICx | NZA-Notify-API
jcEQPyz3jizsgCIz | NZA-Kosten-API
DTldZij54w6edxgc | NZA-Config-API
cmTL7WDGEvg1fSnK | NZA-KPIs-API
```

---

## Environment Variables (nach Setup-Workflow 01)

In n8n unter Settings → Variables setzen:

```env
NZA_SITE_ID=<wird von Workflow 01 ausgegeben>
NZA_KPL_LIST_ID=<List-ID von "NZA Hauptliste">
NZA_MITARBEITER_LIST_ID=<List-ID von "NZA Mitarbeiter">
NZA_CONFIG_LIST_ID=<List-ID von "NZA Konfiguration">
NZA_MASSNAHMEN_LIST_ID=<List-ID von "NZA Maßnahmen">
NZA_BILDER_LIST_ID=<List-ID von "NZA Bilder">
```

---

## Nächste Schritte für Claude Code

### Wenn Workflows aktiviert sind:

1. **Dashboard erweitern** (`/var/www/html/nza/`)
   - Maßnahmen-Tab mit Teams-Benachrichtigung
   - Bilder-Galerie mit Upload
   - KPI-Charts einbinden
   - Kostenberechnung im Formular

2. **APIs testen**
   ```bash
   curl https://osp.schneider-kabelsatzbau.de/api/nza/mitarbeiter
   curl https://osp.schneider-kabelsatzbau.de/api/nza/config
   curl https://osp.schneider-kabelsatzbau.de/api/nza/kpis
   ```

3. **Phase 5: Dashboard-Erweiterung**
   - js/massnahmen.js erstellen
   - js/bilder.js erstellen
   - js/charts.js für KPIs
   - Detail-Modal mit Tabs

---

## Wichtige Referenzen

| Resource | Wert |
|----------|------|
| Server | 46.224.102.30 |
| n8n UI | http://127.0.0.1:5678 |
| n8n Container | `n8n` |
| Microsoft Credential ID | Fm3IuAbVYBYDIA4U |
| SharePoint Site | /sites/NZA_NEU |
| Dashboard URL | https://osp.schneider-kabelsatzbau.de/nza/ |
| Workflow-Verzeichnis | /mnt/HC_Volume_104189729/osp/nza/workflows/ |
| Dokumentation | /mnt/HC_Volume_104189729/osp/nza/docs/ |

---

## Prompt für Fortsetzung

```
Ich möchte die NZA-Integration fortsetzen.

Aktueller Stand:
- Workflows sind in n8n importiert (mit Credentials)
- Duplikate müssen noch gelöscht werden
- Setup-Workflows müssen ausgeführt werden
- API-Workflows müssen aktiviert werden

Lies /mnt/HC_Volume_104189729/osp/nza/docs/CLAUDE_PROMPT_FORTSETZUNG.md für Details.

[Dann je nach Fortschritt:]
- "Die Workflows sind jetzt aktiviert, erweitere das Dashboard"
- "Teste die APIs"
- "Setup-Workflow 01 hat diese Ausgabe: [Site-ID, List-IDs einfügen]"
```

---

*Erstellt: 2026-01-30 18:00*
