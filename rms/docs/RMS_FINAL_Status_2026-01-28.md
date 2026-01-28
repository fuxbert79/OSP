# RMS Finalisierung - Status-Bericht

**Datum:** 2026-01-28
**Autor:** Claude Code

---

## Erledigte Aufgaben

### 1. Scripts erstellt

| Script | Pfad | Status |
|--------|------|--------|
| fill_xlsx_form.py | /opt/osp/scripts/fill_xlsx_form.py | ✅ Erstellt |
| convert_to_pdf.py | /opt/osp/scripts/convert_to_pdf.py | ✅ Erstellt |
| formblatt_service.py | /opt/osp/scripts/formblatt_service.py | ✅ Erstellt |

### 2. Systemd Service

```
Service: formblatt-service
Port: 5050
Status: Aktiv (running)
Endpoints: /health, /fill-xlsx, /convert-pdf, /generate
```

### 3. RMS-Detail-API erweitert

Der Workflow `5jruolIhqcOGu3GQ` wurde erweitert um:
- Massnahmen laden (SharePoint Liste: 3768f2d8-878c-4a5f-bd52-7486fe93289d)
- Schriftverkehr laden (SharePoint Liste: 741c6ae8-88bb-406b-bf85-2e11192a528f)
- Sequentielle Verarbeitung mit Code-Nodes

**Test erfolgreich:**
```json
{
  "reklamation": { "QA_ID": "QA-26013", "Title": "Test-Reklamation (Demo)" },
  "massnahmen": [{ "Title": "TEST - Produktion stoppen" }],
  "schriftverkehr": []
}
```

### 4. RMS-Generate-Formblatt aktualisiert

Der Workflow `MN63eCmmUDHzED8G` wurde aktualisiert:
- 10 Nodes (statt 2 Platzhalter)
- Verwendet lokalen Formblatt-Service (http://172.19.0.1:5050)
- Download Template von SharePoint
- Fill XLSX + Convert PDF via HTTP-Service
- Upload zu SharePoint

---

## Bekannte Probleme

### 1. PDF-Generierung Timeout

Der Formblatt-Workflow hat ein Timeout bei der Ausfuehrung. Moegliche Ursachen:
- SharePoint Template-Download schlaegt fehl
- Pfad `/Formular-Vorlagen/f_qm_02_qualitaetsabweichung/FQM02_Qualitaetsabweichung.xlsx` nicht gefunden

**Loesung:**
1. In SharePoint pruefen, ob die Templates korrekt hochgeladen sind
2. Pfade in n8n anpassen falls noetig
3. Alternativ: Templates lokal auf Server speichern

### 2. SharePoint Template-Pfade

Die Templates muessen in SharePoint unter folgendem Pfad liegen:
```
/sites/RMS/Freigegebene Dokumente/Formular-Vorlagen/
├── f_qm_02_qualitaetsabweichung/
│   └── FQM02_Qualitaetsabweichung.xlsx
├── f_qm_03_8D_Report/
│   └── FQM03_8D_Report.xlsx
├── f_qm_04_nza/
│   └── FQM04_NZA.xlsx
└── f_qm_14_korrekturmassnahme/
    └── FQM14_Korrekturmassnahmen.xlsx
```

---

## Naechste Schritte

1. **SharePoint Templates pruefen**
   - Pfade in SharePoint verifizieren
   - Bei Bedarf Templates hochladen

2. **Workflow testen**
   - In n8n Web-UI manuell testen
   - Fehler-Nodes identifizieren

3. **Alternative: Lokale Templates**
   - Templates auf Server unter `/opt/osp/templates/` ablegen
   - Workflow anpassen um lokale Dateien zu verwenden

---

## API-Dokumentation

### Detail-API (funktioniert)

```bash
GET /api/rms/detail?id=1
```

Response:
```json
{
  "reklamation": { "QA_ID": "...", "Title": "..." },
  "massnahmen": [...],
  "schriftverkehr": [...],
  "sharePointUrl": "..."
}
```

### Generate-Formblatt-API (in Arbeit)

```bash
POST /api/rms/generate-formblatt
Content-Type: application/json

{
  "qaId": "QA-26013",
  "formularTyp": "F_QM_02",
  "reklamationsDaten": { ... },
  "ersteller": "AL"
}
```

---

## Technische Details

### Docker-Netzwerk
- n8n Container: n8n
- Gateway IP: 172.19.0.1
- Formblatt-Service lauscht auf 0.0.0.0:5050

### n8n API Key
```
N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjkxMmFlMi1mNzQyLTQxZGUtYTY1OS0xNTQ3YjBjMGU5OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5NTM4MTcwLCJleHAiOjE3NzcyNDA4MDB9.NsECcQH9N-UsiCmXrZkMGLg6ioFbGCuNXWW_XaJAUTY"
```

### SharePoint
- Site ID: rainerschneiderkabelsatz.sharepoint.com,2881519a-a447-45b1-a870-9df715ee7313,b5136f46-5d8e-45ef-9a99-fa2e6fb58b5c
- Reklamationen Liste: e9b1d926-085a-4435-a012-114ca9ba59a8
- Massnahmen Liste: 3768f2d8-878c-4a5f-bd52-7486fe93289d
- Schriftverkehr Liste: 741c6ae8-88bb-406b-bf85-2e11192a528f

---

*Erstellt: 2026-01-28 19:30 UTC*
