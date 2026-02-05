# Formular-Vorbereitung für n8n Import

**Stand:** 2026-02-05
**Autor:** Claude Code für AL

---

## Übersicht

Diese Dokumentation beschreibt den Prozess zur Vorbereitung von Excel-Formularen für den automatischen Import via n8n Workflows.

---

## Unterstützte Formulare

| Formular | System | Pfad | Status |
|----------|--------|------|--------|
| F-QM-04 (FQM04) | NZA | `nza/formulare/FQM04/` | ✅ Fertig |
| F-QM-02 | RMS | `rms/formulare/` | ⏳ Geplant |
| F-QM-03 | RMS | `rms/formulare/` | ⏳ Geplant |
| F-QM-14 | RMS | `rms/formulare/` | ⏳ Geplant |

---

## Formular-Struktur (Standard)

Jedes Formular-Verzeichnis enthält:

```
formulare/FQMXX/
├── FQMXX.xlsx              # Original-Vorlage (leer)
├── FQMXX_TEST.xlsx         # Test-Datei mit Beispieldaten
├── F_QM_XX.md              # Dokumentation (Felder, Regeln)
├── F_QM_XX_Schema.json     # JSON-Schema für Validierung
├── README.md               # Kurzanleitung
├── RMS_Prompt_F_QM_XX.md   # KI-Prompt für Ausfüllung
└── TEST_ANLEITUNG.md       # Anleitung für Tests
```

---

## Schritt 1: Excel-Vorlage analysieren

### 1.1 Struktur identifizieren

```bash
# Voraussetzung: openpyxl oder pandas installiert
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('FORMULAR.xlsx')
for sheet in wb.sheetnames:
    print(f'Sheet: {sheet}')
    ws = wb[sheet]
    print(f'  Zeilen: {ws.max_row}, Spalten: {ws.max_column}')
"
```

### 1.2 Felder dokumentieren

| Zelle | Feldname | Typ | Pflicht | Validierung |
|-------|----------|-----|---------|-------------|
| B3 | Artikel-Nr. | Text | ✅ | max. 50 Zeichen |
| B4 | Betriebsauftrag | Text | ✅ | Format: 6-stellig |
| ... | ... | ... | ... | ... |

### 1.3 Pflichtfelder definieren

Liste aller Felder, die vor Import vorhanden sein müssen:
- Wird im Workflow für Validierung genutzt
- Bei fehlendem Pflichtfeld → Rejection-Email

---

## Schritt 2: JSON-Schema erstellen

### 2.1 Schema-Struktur

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "F-QM-XX Schema",
  "type": "object",
  "required": ["artikelNr", "betriebsauftrag"],
  "properties": {
    "artikelNr": {
      "type": "string",
      "maxLength": 50,
      "description": "Artikel-Nummer"
    },
    "betriebsauftrag": {
      "type": "string",
      "pattern": "^[0-9]{6}$",
      "description": "6-stellige BA-Nummer"
    }
  }
}
```

### 2.2 Validierungsregeln

| Regel | JSON-Schema | Beispiel |
|-------|-------------|----------|
| Pflichtfeld | `"required": ["feld"]` | Artikel-Nr. muss vorhanden sein |
| Max. Länge | `"maxLength": 50` | Text max. 50 Zeichen |
| Pattern | `"pattern": "^[0-9]{6}$"` | Genau 6 Ziffern |
| Enum | `"enum": ["A", "B", "C"]` | Nur erlaubte Werte |
| Min/Max | `"minimum": 0, "maximum": 100` | Zahlenbereich |

---

## Schritt 3: Test-Datei erstellen

### 3.1 Testdaten eintragen

Die Test-Datei (`FQMXX_TEST.xlsx`) enthält:
- Vollständige, valide Beispieldaten
- Alle Pflichtfelder ausgefüllt
- Realistische Werte aus dem Produktivbetrieb

### 3.2 FQM04 Test-Beispiel

| Feld | Testwert |
|------|----------|
| Artikel-Nr. | TEST-12345 |
| Betriebsauftrag | 170001 |
| Losgröße | 100 |
| Ausschuss | 5 |
| Kostenstelle | 3000 |
| Fehlerkategorie | Crimpfehler |
| Fehlerbeschreibung | Crimphöhe außerhalb Toleranz |

---

## Schritt 4: n8n Workflow anpassen

### 4.1 spreadsheetFile Node

**WICHTIG:** n8n 2.6.3 unterstützt nur `typeVersion: 2`

```json
{
  "parameters": {
    "operation": "fromFile",
    "options": {}
  },
  "type": "n8n-nodes-base.spreadsheetFile",
  "typeVersion": 2
}
```

**NICHT verwenden:**
- `typeVersion: 4.5` (existiert nicht in n8n 2.6.3)
- `operation: "toJson"` (alte Syntax)

### 4.2 Feld-Mapping

Excel-Spalten werden zu JSON-Keys:
- `Artikel-Nr.` → `artikelNr` (CamelCase)
- `Fehler Beschreibung` → `fehlerBeschreibung`
- Umlaute: `ä` → `ae`, `ö` → `oe`, `ü` → `ue`

### 4.3 Validierung im Code-Node

```javascript
// Pflichtfeld-Validierung
const required = ['artikelNr', 'betriebsauftrag', 'ausschuss',
                  'fehlerBeschreibung', 'fehlerKategorie'];

const missing = required.filter(field => !$input.item.json[field]);

if (missing.length > 0) {
  return {
    valid: false,
    missing: missing,
    message: `Pflichtfelder fehlen: ${missing.join(', ')}`
  };
}

return { valid: true };
```

---

## Schritt 5: Dateien bereitstellen

### 5.1 Auf Server kopieren

```bash
# Test-Datei für n8n bereitstellen
docker cp FQMXX_TEST.xlsx n8n:/tmp/
docker exec n8n chown node:node /tmp/FQMXX_TEST.xlsx
```

### 5.2 Volume-Mount (persistent)

In `docker-compose.yml`:
```yaml
volumes:
  - /opt/osp/nza/formulare:/home/node/formulare:ro
```

---

## Schritt 6: Tests durchführen

### 6.1 Validierung testen

```bash
# Webhook aufrufen
curl -X POST https://n8n.schneider-kabelsatzbau.de/webhook/nza-validate \
  -H "Content-Type: application/json" \
  -d '{
    "artikelNr": "TEST-12345",
    "betriebsauftrag": "170001",
    "ausschuss": 5,
    "fehlerBeschreibung": "Test",
    "fehlerKategorie": "Crimpfehler",
    "zusatzarbeit": "Nachcrimpen"
  }'
```

### 6.2 Erwartete Responses

**Erfolg:**
```json
{
  "valid": true,
  "message": "Alle Pflichtfelder vorhanden"
}
```

**Fehler:**
```json
{
  "valid": false,
  "missing": ["fehlerKategorie", "zusatzarbeit"],
  "message": "Pflichtfelder fehlen: fehlerKategorie, zusatzarbeit"
}
```

---

## Checkliste für neue Formulare

- [ ] Excel-Vorlage analysieren
- [ ] Felder in Markdown dokumentieren
- [ ] JSON-Schema erstellen
- [ ] Test-Datei mit Beispieldaten erstellen
- [ ] README.md schreiben
- [ ] RMS_Prompt für KI-Ausfüllung erstellen
- [ ] TEST_ANLEITUNG.md erstellen
- [ ] n8n Workflow anpassen/erstellen
- [ ] Validierung im Code-Node implementieren
- [ ] Tests durchführen
- [ ] Dokumentation aktualisieren

---

## Bekannte Probleme

### n8n spreadsheetFile Versionen

| n8n Version | spreadsheetFile | Operation |
|-------------|-----------------|-----------|
| 2.6.3 | v1, v2 | `fromFile` |
| 2.x (älter) | v1 | `toJson` |
| neuere | v4.5+ | `toJson` |

**Fix:** Bei Aktivierungsfehler `Cannot read properties of undefined (reading 'execute')` → `typeVersion: 2` verwenden.

### Docker-Dateizugriff

n8n im Docker-Container hat eingeschränkten Dateizugriff. Details siehe `MAIL_ERROR.md`.

---

*Erstellt: 2026-02-05*
*Autor: Claude Code für AL*
