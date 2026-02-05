# NZA E-Mail-Import Test-Anleitung

**Stand:** 2026-02-05
**Workflow:** NZA-Email-Import-V2

---

## Test-Dateien

| Datei | Beschreibung |
|-------|--------------|
| `FQM04_TEST.xlsx` | Ausgefuelltes Test-Formular |
| `FQM04.xlsx` | Leere Vorlage |

---

## Test-Daten im Formular

| Feld | Wert |
|------|------|
| Reklamationstyp | Interne Reklamation |
| Datum | (aktuelles Datum) |
| Artikel-Nr. | TEST-12345 |
| Betriebsauftrag | 170001 |
| Losgroesse | 100 |
| Ausschuss | 5 |
| Verursacher | 3000 |
| Kostenstelle | 3000 |
| Ersatz BA | 170002 |
| Fehlerbeschreibung | TEST: Crimp nicht korrekt... |
| Fehlerkategorie | Crimpfehler |

---

## Test durchfuehren

### Option 1: E-Mail senden (empfohlen)

1. **E-Mail erstellen:**
   - An: `nza@schneider-kabelsatzbau.de`
   - Betreff: `TEST NZA Import - FQM04`
   - Anhang: `FQM04_TEST.xlsx`

2. **Warten:** Der Workflow prueft alle 5 Minuten

3. **Ergebnis pruefen:**
   - n8n Executions: https://n8n.schneider-kabelsatzbau.de/executions
   - SharePoint nza-kpl Liste
   - Dashboard: https://osp.schneider-kabelsatzbau.de/nza/2026/

### Option 2: Workflow manuell ausloesen

```bash
# n8n Web-UI oeffnen
https://n8n.schneider-kabelsatzbau.de/

# Workflow "NZA-Email-Import-V2" oeffnen
# "Test workflow" Button klicken
```

### Option 3: Direkt per API testen

```bash
# Letzte NZA-ID abrufen
curl -s "https://osp.schneider-kabelsatzbau.de/api/nza/prozesse" | head -c 200

# Kosten-API testen (sollte funktionieren)
curl -s "https://osp.schneider-kabelsatzbau.de/api/nza/kosten"
```

---

## Erwartetes Ergebnis

Nach erfolgreichem Import:

1. **Neue NZA-ID:** `NZA-26001` (oder naechste freie Nummer)

2. **SharePoint nza-kpl:**
   - Neuer Eintrag mit allen Feldern
   - Status: "Neu"
   - Bemerkung: "Importiert aus E-Mail..."

3. **SharePoint Dokumente:**
   - Ordner: `/NZA-Dokumente/NZA-26001/`
   - Datei: `NZA-26001_Formular_2026-02-05.xlsx`

4. **nza-bilder Liste:**
   - Eintrag mit Dokument-Referenz
   - Kategorie: "Ursprungsformular"

5. **E-Mail:**
   - Als gelesen markiert

6. **Teams (optional):**
   - Benachrichtigung an AL

---

## Fehlersuche

### n8n Execution Logs

```bash
# Letzte Executions anzeigen
docker logs n8n --tail 100 | grep -i "execution\|error"

# Workflow-Status pruefen
docker exec n8n n8n list:workflow --active=true | grep -i email
```

### Haeufige Probleme

| Problem | Loesung |
|---------|---------|
| Workflow nicht aktiv | `docker exec n8n n8n update:workflow --id=R3o19nUoTwNJkMm2 --active=true` |
| Credentials fehlen | n8n Web-UI > Credentials pruefen |
| SharePoint Fehler | Environment-Variablen pruefen |
| E-Mail nicht erkannt | Anhang muss .xlsx sein |

### Environment-Variablen pruefen

```bash
docker exec n8n printenv | grep NZA
```

Erwartete Ausgabe:
```
NZA_SITE_ID=rainerschneiderkabelsatz.sharepoint.com,...
NZA_KPL_LIST_ID=7bea980d-...
NZA_BILDER_LIST_ID=60847793-...
NZA_MITARBEITER_LIST_ID=d6dbfa5c-...
NZA_CONFIG_LIST_ID=6e56d7d5-...
NZA_MASSNAHMEN_LIST_ID=d59ef6e6-...
```

---

## Nach dem Test

1. **Test-Eintrag loeschen** (optional):
   - SharePoint nza-kpl > Eintrag loeschen
   - SharePoint Dokumente > Ordner loeschen

2. **Workflow ueberwachen:**
   - n8n Executions regelmaessig pruefen
   - Bei Fehlern: Error-Handling ergaenzen

---

*Erstellt: 2026-02-05*
