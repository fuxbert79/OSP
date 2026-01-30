# OSP Server-Erhebung 2025-12-23

**Datum:** 2025-12-23
**Server:** osp-webui (46.224.102.30)
**Durchgeführt von:** Claude Code

---

## Erhobene Werte

| Parameter | Dokumentiert (15.12.2025) | Aktuell (23.12.2025) | Geändert? |
|-----------|---------------------------|----------------------|-----------|
| **Server** | Hetzner CX43 | Hetzner CX43 | - |
| **RAM** | 16GB | 15Gi (~16GB) | ❌ |
| **vCPU** | 8 | 8 (Intel Xeon Skylake) | ❌ |
| **Docker** | 27.3.1 | **28.2.2** | ✅ GEÄNDERT |
| **Open WebUI** | v0.6.43 | v0.6.43 | ❌ |
| **ChromaDB** | 0.5.15 (Doku) / 1.0.0 (docker-compose) | **1.3.6** | ✅ GEÄNDERT |
| **Ollama** | latest | **ENTFERNT** | ✅ KRITISCH |
| **n8n** | latest | latest | ❌ |
| **Disk Root** | 160GB | 38GB (14GB genutzt, 37%) | ❌ |
| **Disk Volume** | - | 59GB (32GB genutzt, 57%) | - |

---

## Aktuelle Container-Übersicht

| Container | Image | Status | Erstellt |
|-----------|-------|--------|----------|
| open-webui | ghcr.io/open-webui/open-webui:v0.6.43 | Up (healthy) | 2025-12-23 10:17 |
| chromadb | chromadb/chroma:1.3.6 | Up | 2025-12-23 21:52 |
| n8n | docker.n8n.io/n8nio/n8n:latest | Up | 2025-12-23 21:41 |
| portainer | portainer/portainer-ce:latest | Up | 2025-12-23 10:28 |
| osp-doccompare | doccompare-doccompare | Up (healthy) | 2025-12-22 16:35 |
| anthropic-proxy | ghcr.io/berriai/litellm:main-latest | Up (unhealthy) | 2025-12-15 15:57 |

---

## Identifizierte Änderungen seit 15.12.2025

### 1. Docker Engine Update
- **Alt:** Docker 27.3.1
- **Neu:** Docker 28.2.2
- **Auswirkung:** Keine funktionalen Änderungen erwartet

### 2. ChromaDB Major Update
- **Alt:** 0.5.15 (Dokumentation) / 1.0.0 (docker-compose.yml)
- **Neu:** 1.3.6
- **Auswirkung:** API-Änderungen möglich, Performance-Verbesserungen
- **HINWEIS:** docker-compose.yml zeigt noch `1.0.0`, Container läuft aber mit `1.3.6`!

### 3. Ollama ENTFERNT (KRITISCH!)
- **Status:** Container existiert nicht mehr
- **Auswirkung:** Lokale LLM-Runtime (mistral:7b, llama2:13b) nicht mehr verfügbar
- **Vermutung:** Umstellung auf Claude API via anthropic-proxy (LiteLLM)

### 4. Neue Container hinzugefügt

| Container | Zweck | Dokumentiert? |
|-----------|-------|---------------|
| **anthropic-proxy** | LiteLLM Proxy für Claude API | ❌ Teilweise |
| **osp-doccompare** | Dokumenten-Vergleich | ❌ NEIN |
| **portainer** | Docker-Management UI | ❌ NEIN |

### 5. Container-Namenänderungen
- **Alt:** osp-chromadb → **Neu:** chromadb
- **Alt:** osp-webui → **Neu:** open-webui

---

## Erforderliche Dokument-Updates

### Datei: IT_OSP_KI_Chatbot.md

#### Patch 1: Tech-Stack Tabelle (Zeile 66-76)

**SUCHEN:**
```markdown
| Komponente | Version | Zweck | RAM | Storage |
|------------|---------|-------|-----|---------|
| Ubuntu | 24.04 LTS | OS | - | 50GB |
| Docker | 27.3.1 | Runtime | - | 10GB |
| OSPUI | 0.6.43 | UI/Orchestr. | 2GB | 5GB |
| ChromaDB | 0.5.15 | Vektordatenbank | 2GB | 20GB |
| Ollama | latest | LLM-Runtime | 10GB | 60GB |
| n8n | latest | Workflow | 1GB | 5GB |
| Nginx | 1.26 | Reverse Proxy | 512MB | 1GB |
```

**ERSETZEN:**
```markdown
| Komponente | Version | Zweck | RAM | Storage |
|------------|---------|-------|-----|---------|
| Ubuntu | 24.04 LTS | OS | - | 50GB |
| Docker | 28.2.2 | Runtime | - | 10GB |
| OSPUI | 0.6.43 | UI/Orchestr. | 2GB | 5GB |
| ChromaDB | 1.3.6 | Vektordatenbank | 2GB | 20GB |
| LiteLLM | main-latest | Claude API Proxy | 1GB | 2GB |
| n8n | latest | Workflow | 1GB | 5GB |
| Portainer | latest | Docker-Management | 200MB | 1GB |
| DocCompare | latest | Dokumentenvergleich | 500MB | 2GB |
| Nginx | 1.26 | Reverse Proxy | 512MB | 1GB |
```

#### Patch 2: Architektur-Diagramm (Zeile 48-60)

**SUCHEN:**
```
┌────────┬──────────┬────────┬─────┐
│ OSPUI  │ ChromaDB │ Ollama │ n8n │
│ :3000  │ :8000    │ :11434 │:5678│
└────────┴──────────┴────────┴─────┘
```

**ERSETZEN:**
```
┌────────┬──────────┬─────────┬─────┬───────────┬───────────┐
│ OSPUI  │ ChromaDB │ LiteLLM │ n8n │ Portainer │ DocCompare│
│ :3000  │ :8000    │ :4000   │:5678│ :9443     │ :8050     │
└────────┴──────────┴─────────┴─────┴───────────┴───────────┘
```

#### Patch 3: Docker-Compose Beispiel aktualisieren (Zeile 227-320)

Die Docker-Compose im Dokument ist veraltet und zeigt noch Ollama. Sollte mit aktueller Version aus `/mnt/HC_Volume_104189729/osp/docker-compose.yml` ersetzt werden.

#### Patch 4: Ollama-Abschnitt entfernen oder anpassen (Zeile 581-622)

Der Abschnitt "OLLAMA LLM-RUNTIME" ist obsolet und sollte durch einen "CLAUDE API (via LiteLLM)" Abschnitt ersetzt werden.

---

## Ausgeführte Befehle

```bash
# RAM-Status
free -h | grep Mem
# Output: Mem: 15Gi 2.6Gi 502Mi 6.5Mi 12Gi 12Gi

# CPU-Info
nproc && lscpu | grep "Model name"
# Output: 8, Intel Xeon Processor (Skylake, IBRS, no TSX)

# Docker-Version
docker --version
# Output: Docker version 28.2.2, build 28.2.2-0ubuntu1~24.04.1

# Container-Status
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
# 6 Container aktiv

# Container-Erstellungsdatum
docker ps --format "{{.Names}}: {{.CreatedAt}}" | sort
# Alle Container nach 15.12.2025 neu erstellt

# Docker-Images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
# ChromaDB 1.3.6, Open WebUI v0.6.43, etc.

# Disk-Usage
df -h / /var/lib/docker
# Root: 38G (37%), Volume: 59G (57%)

# Ollama-Check
docker ps -a | grep -i ollama
# Output: Ollama-Container nicht gefunden
```

---

## Zusammenfassung

### Kritische Änderungen
1. **Ollama entfernt** - Architektur-Änderung auf Claude API
2. **ChromaDB 1.3.6** - Major Update, docker-compose.yml inkonsistent
3. **3 neue Container** - Nicht dokumentiert

### Empfohlene Maßnahmen
1. IT_OSP_KI_Chatbot.md aktualisieren (Patches oben)
2. docker-compose.yml auf Server mit Dokumentation synchronisieren
3. Neuen Abschnitt für LiteLLM/Claude API erstellen
4. Portainer und DocCompare dokumentieren

---

**Erstellt:** 2025-12-23 22:55 UTC
**Status:** Erhebung abgeschlossen
**Nächste Aktion:** Patches anwenden

