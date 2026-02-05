# E-Mail mit Anhang - Bekanntes Problem

**Stand:** 2026-02-05
**Status:** OFFEN
**Betrifft:** n8n Workflows mit Datei-Anhängen

---

## Problembeschreibung

Das Senden von E-Mails mit Datei-Anhängen über n8n funktioniert nicht zuverlässig. Der `readBinaryFile` oder `readWriteFile` Node blockiert die Workflow-Ausführung ohne Fehlermeldung.

---

## Symptome

1. **Workflow blockiert:** Keine Ausführung nach dem Read-Node
2. **Kein Fehler:** Execution zeigt keinen Error, hängt einfach
3. **Timeout:** Nach 120s Abbruch ohne Ergebnis
4. **E-Mail ohne Anhang funktioniert:** Gleicher Workflow ohne Datei-Read sendet erfolgreich

---

## Getestete Szenarien

### Workflow-Varianten

| Workflow | Node-Typ | Datei-Pfad | Ergebnis |
|----------|----------|------------|----------|
| NZA-Send-V2 | readBinaryFile v1 | `/tmp/nza-test/FQM04_TEST.xlsx` | ❌ Blockiert |
| NZA-Send-Final | readWriteFile v1 | `/tmp/nza-test/FQM04_TEST.xlsx` | ❌ Blockiert |
| NZA-Read-Only | readBinaryFile v1 | `/home/node/nza-test/FQM04_TEST.xlsx` | ❌ Blockiert |
| NZA-Test-Email-NoAttach | (kein Read) | - | ✅ Funktioniert |

### Datei-Berechtigungen

```bash
# Getestete Berechtigungen
-rw-r--r-- 1 node node 12345 FQM04_TEST.xlsx  # ❌ Blockiert
-rw-rw-rw- 1 node node 12345 FQM04_TEST.xlsx  # ❌ Blockiert
-rwxrwxrwx 1 node node 12345 FQM04_TEST.xlsx  # ❌ Blockiert
```

### Pfade

| Pfad | Im Container | Ergebnis |
|------|--------------|----------|
| `/tmp/nza-test/` | Ja (tmpfs) | ❌ Blockiert |
| `/home/node/nza-test/` | Ja | ❌ Blockiert |
| `/data/nza-test/` | Ja (Volume) | Nicht getestet |

---

## Technische Details

### n8n Container-Konfiguration

```yaml
# docker-compose.yml
n8n:
  image: n8nio/n8n:2.6.3
  user: "node"
  volumes:
    - n8n_data:/home/node/.n8n
    - /opt/osp/n8n-local-files:/data
  environment:
    - N8N_USER_FOLDER=/home/node/.n8n
```

### Node-Konfiguration (readBinaryFile)

```json
{
  "parameters": {
    "filePath": "/tmp/nza-test/FQM04_TEST.xlsx"
  },
  "type": "n8n-nodes-base.readBinaryFile",
  "typeVersion": 1
}
```

### Node-Konfiguration (readWriteFile)

```json
{
  "parameters": {
    "operation": "read",
    "fileSelector": "/tmp/nza-test/FQM04_TEST.xlsx",
    "options": {}
  },
  "type": "n8n-nodes-base.readWriteFile",
  "typeVersion": 1
}
```

---

## Vermutete Ursachen

### 1. Docker Security Context
- n8n läuft als `node` User (UID 1000)
- Möglicherweise SELinux/AppArmor Einschränkungen
- Container-Isolation verhindert Dateizugriff

### 2. n8n Filesystem-Sandbox
- n8n hat eingebaute Dateisystem-Einschränkungen
- Nur bestimmte Pfade sind erlaubt
- `/tmp` möglicherweise nicht in der Whitelist

### 3. Volume-Mount fehlt
- Die Test-Verzeichnisse sind nicht als Volume gemountet
- Nur `/data` ist als persistent Volume verfügbar

### 4. Asynchrones I/O Problem
- Node blockiert bei synchronem Dateizugriff
- Keine Timeout-Behandlung im Node

---

## Workarounds (noch nicht getestet)

### Option A: Volume-Mount nutzen

```yaml
# docker-compose.yml erweitern
volumes:
  - /opt/osp/nza/formulare:/home/node/formulare:ro
```

Dann im Workflow:
```json
{
  "filePath": "/home/node/formulare/FQM04/FQM04_TEST.xlsx"
}
```

### Option B: HTTP-Request statt File-Read

Datei über HTTP-Server bereitstellen und per HTTP-Request laden:
```json
{
  "url": "http://host.docker.internal:8080/files/FQM04_TEST.xlsx"
}
```

### Option C: Base64 direkt im Workflow

Datei vorher in Base64 konvertieren und im Workflow als String verwenden (nicht praktikabel für dynamische Dateien).

### Option D: n8n Community Edition upgraden

Prüfen ob neuere n8n Version das Problem behebt.

---

## Test-Workflows (in `/tmp/`)

Die folgenden Test-Workflows wurden erstellt:

| Datei | Zweck | Ergebnis |
|-------|-------|----------|
| `nza-read-only.json` | Nur Datei lesen | ❌ Blockiert |
| `nza-send-v2.json` | Read + E-Mail | ❌ Blockiert |
| `nza-read-test.json` | readWriteFile Test | ❌ Blockiert |
| `nza-send-final.json` | Vollständiger Test | ❌ Blockiert |
| `nza-send-test-attachment.json` | HTTP API Ansatz | ❌ Blockiert |

---

## Nächste Schritte

1. [ ] Volume-Mount `/opt/osp/nza/formulare` → `/home/node/formulare` einrichten
2. [ ] docker-compose.yml anpassen und n8n neu starten
3. [ ] Test mit gemountetem Volume durchführen
4. [ ] n8n Logs während Execution prüfen: `docker logs -f n8n`
5. [ ] Alternative: HTTP-Server für Dateibereitstellung

---

## Referenzen

- [n8n File Nodes Dokumentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.readwritefile/)
- [n8n Docker Security](https://docs.n8n.io/hosting/installation/docker/)
- [GitHub Issue Template](https://github.com/n8n-io/n8n/issues)

---

## Kontakt

Bei Fragen: AL (Andreas Löhr) - QM-Manager & KI-Manager

---

*Erstellt: 2026-02-05*
*Autor: Claude Code für AL*
