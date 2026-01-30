# RMS Funktionstest-Prompt

**Erstellt:** 2026-01-30
**Zweck:** Systematischer Test aller RMS-Funktionen
**Voraussetzung:** Test-Datenbank (wird nach Tests zurückgesetzt)

---

## Test-Umgebung

| Parameter | Wert |
|-----------|------|
| Server | localhost:5678 (n8n) |
| SharePoint | rainerschneiderkabelsatz.sharepoint.com |
| Liste | RMS-Reklamationen |
| Test-Dateien | /tmp/rms_test_files/ |

---

## API-Endpunkte (Webhooks)

### Lese-Operationen (GET)
| Endpoint | Funktion |
|----------|----------|
| `/webhook/rms-reklamationen` | Liste aller Reklamationen |
| `/webhook/rms-detail?id={id}` | Detail einer Reklamation |
| `/webhook/rms-files?qaId={qaId}` | Dateien einer Reklamation |
| `/webhook/rms-kpis` | KPI-Dashboard Daten |
| `/webhook/rms-charts` | Chart-Daten |
| `/webhook/rms-stammdaten` | Stammdaten (Kunden, etc.) |
| `/webhook/e8f9a1b2-rms-users` | Benutzer-Liste |

### Schreib-Operationen (POST/PATCH/DELETE)
| Endpoint | Funktion |
|----------|----------|
| `POST /webhook/rms-create` | Neue Reklamation erstellen |
| `PATCH /webhook/rms-update` | Reklamation aktualisieren |
| `POST /webhook/rms-massnahmen` | Maßnahme hinzufügen |
| `PATCH /webhook/rms-update-massnahme` | Maßnahme aktualisieren |
| `DELETE /webhook/rms-delete-massnahme` | Maßnahme löschen |
| `POST /webhook/rms-generate-formblatt` | Formblatt generieren |
| `POST /webhook/rms-send-email` | E-Mail senden |
| `POST /webhook/rms-notify-massnahme` | Benachrichtigung senden |

---

## Testfälle

### TC-01: Reklamationen abrufen
```bash
curl -s "http://localhost:5678/webhook/rms-reklamationen?limit=5"
```
**Erwartung:** JSON mit `value`-Array, Reklamationen mit QA_ID

### TC-02: Einzelne Reklamation abrufen
```bash
curl -s "http://localhost:5678/webhook/rms-detail?id=1"
```
**Erwartung:** Detaildaten einer Reklamation

### TC-03: Neue Reklamation erstellen (Kunde)
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{
    "Title": "Test Kundenreklamation",
    "Rekla_Typ": "Kunde",
    "Prioritaet": "hoch",
    "Beschreibung": "Testfall TC-03: Kabelsatz defekt geliefert",
    "KST": ["Fertigung"],
    "Kunde": "Mustermann GmbH",
    "Artikel": "KS-4711",
    "Menge_Reklamiert": 15,
    "Lieferschein_Nr": "LS-2026-TEST001"
  }' \
  "http://localhost:5678/webhook/rms-create"
```
**Erwartung:** Neue QA-ID (Format: QA-26XXX)

### TC-04: Neue Reklamation erstellen (Lieferant)
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{
    "Title": "Test Lieferantenreklamation",
    "Rekla_Typ": "Lieferant",
    "Prioritaet": "mittel",
    "Beschreibung": "Testfall TC-04: Material nicht spezifikationskonform",
    "KST": ["Wareneingang"],
    "Lieferant": "Lieferant ABC",
    "Artikel": "Stecker-XY-001",
    "Menge_Reklamiert": 500
  }' \
  "http://localhost:5678/webhook/rms-create"
```

### TC-05: Neue Reklamation erstellen (Intern)
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{
    "Title": "Test Interne Reklamation",
    "Rekla_Typ": "Intern",
    "Prioritaet": "niedrig",
    "Beschreibung": "Testfall TC-05: Prozessabweichung dokumentiert",
    "KST": ["Qualitaet"],
    "Fehlerart": "Prozessfehler"
  }' \
  "http://localhost:5678/webhook/rms-create"
```

### TC-06: Reklamation aktualisieren
```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -d '{
    "id": "{ID_AUS_TC03}",
    "Rekla_Status": "In Bearbeitung",
    "Verantwortlich": "AL",
    "Tracking_Status": "Offen"
  }' \
  "http://localhost:5678/webhook/rms-update"
```

### TC-07: Maßnahme hinzufügen
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{
    "qaId": "{QA_ID_AUS_TC03}",
    "Massnahme_Typ": "Sofortmassnahme",
    "Beschreibung": "Sperrung der betroffenen Charge",
    "Verantwortlich": "AL",
    "Faellig_Am": "2026-02-05"
  }' \
  "http://localhost:5678/webhook/rms-massnahmen"
```

### TC-08: Maßnahme aktualisieren
```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -d '{
    "id": "{MASSNAHME_ID}",
    "Status": "Erledigt",
    "Erledigt_Am": "2026-01-30",
    "Bemerkung": "Charge gesperrt und gekennzeichnet"
  }' \
  "http://localhost:5678/webhook/rms-update-massnahme"
```

### TC-09: Tracking-Felder setzen
```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -d '{
    "id": "{ID_AUS_TC04}",
    "Tracking_Status": "Ersatzlieferung angefordert",
    "Tracking_Ersatzlieferung": true,
    "Tracking_Bemerkung": "Ersatzlieferung bei Lieferant angefordert"
  }' \
  "http://localhost:5678/webhook/rms-update"
```

### TC-10: KPIs abrufen
```bash
curl -s "http://localhost:5678/webhook/rms-kpis"
```
**Erwartung:** Statistiken (Anzahl offen, geschlossen, nach Typ, etc.)

### TC-11: Charts abrufen
```bash
curl -s "http://localhost:5678/webhook/rms-charts"
```
**Erwartung:** Daten für Dashboard-Charts

### TC-12: Dateien einer Reklamation abrufen
```bash
curl -s "http://localhost:5678/webhook/rms-files?qaId={QA_ID}"
```

### TC-13: Formblatt generieren
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{
    "qaId": "{QA_ID}",
    "formblatt": "F-QM-14"
  }' \
  "http://localhost:5678/webhook/rms-generate-formblatt"
```

### TC-14: Benutzer abrufen
```bash
curl -s "http://localhost:5678/webhook/e8f9a1b2-rms-users"
```

### TC-15: Stammdaten abrufen
```bash
curl -s "http://localhost:5678/webhook/rms-stammdaten"
```

### TC-16: Reklamation abschließen
```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -d '{
    "id": "{ID}",
    "Rekla_Status": "Abgeschlossen",
    "Tracking_Status": "Abgeschlossen",
    "Abschlussdatum": "2026-01-30"
  }' \
  "http://localhost:5678/webhook/rms-update"
```

---

## Test-Daten

### Fiktive Kunden
- Mustermann GmbH (DebKredNr: 10001)
- Beispiel AG (DebKredNr: 10002)
- Test Automotive GmbH (DebKredNr: 10003)

### Fiktive Lieferanten
- Lieferant ABC (DebKredNr: 70001)
- Zulieferer XYZ (DebKredNr: 70002)

### Fiktive Artikel
- KS-4711: Kabelsatz Motor
- KS-4712: Kabelsatz Tür
- Stecker-XY-001: Steckverbinder 12-polig

### Test-Dateien
- `/tmp/rms_test_files/fehler_foto_1.png`
- `/tmp/rms_test_files/fehler_foto_2.png`
- `/tmp/rms_test_files/Lieferschein_TEST001.txt`
- `/tmp/rms_test_files/Reklamationsschreiben_TEST.txt`

---

## Ausführung

```bash
# Alle Tests ausführen
cd /mnt/HC_Volume_104189729/osp
python3 scripts/rms_funktionstest.py

# Einzelnen Test ausführen
python3 scripts/rms_funktionstest.py --test TC-03
```

---

## Erwartete Ergebnisse

| Test | Status | Beschreibung |
|------|--------|--------------|
| TC-01 | - | Reklamationen abrufbar |
| TC-02 | - | Detail abrufbar |
| TC-03 | - | Kundenreklamation erstellt |
| TC-04 | - | Lieferantenreklamation erstellt |
| TC-05 | - | Interne Reklamation erstellt |
| TC-06 | - | Reklamation aktualisiert |
| TC-07 | - | Maßnahme hinzugefügt |
| TC-08 | - | Maßnahme aktualisiert |
| TC-09 | - | Tracking-Felder gesetzt |
| TC-10 | - | KPIs verfügbar |
| TC-11 | - | Charts verfügbar |
| TC-12 | - | Dateien abrufbar |
| TC-13 | - | Formblatt generiert |
| TC-14 | - | Benutzer abrufbar |
| TC-15 | - | Stammdaten abrufbar |
| TC-16 | - | Reklamation abgeschlossen |

---

## Nach den Tests

```bash
# Datenbank zurücksetzen (SharePoint-Liste leeren)
# ACHTUNG: Nur auf Test-System!
```
