# OSP Server Architektur-Analyse

**Datum:** 2025-12-18 21:53 UTC
**Server:** Hetzner CX43 (46.224.102.30)
**Hostname:** osp-webui
**Analysiert von:** Claude Code (AL)

---

## 1. SYSTEM-STATUS

| Metrik | Wert | Bemerkung |
|--------|------|-----------|
| **OS** | Ubuntu 24.04.3 LTS (Noble Numbat) | Aktuell |
| **Kernel** | 6.8.0-90-generic | Aktuell |
| **RAM Total** | 15.25 GB | ⚠️ ACHTUNG: CLAUDE.md sagt 32GB! |
| **RAM Used** | 2.8 GB | |
| **RAM Available** | 12 GB | Sehr gut |
| **RAM Buff/Cache** | 11 GB | Normal |
| **Swap** | 0 B | Kein Swap konfiguriert |
| **Disk Total** | 38 GB | |
| **Disk Used** | 13 GB (37%) | OK |
| **Disk Available** | 23 GB | |
| **Uptime** | 3 days, 13:21 | |
| **Load Average** | 0.70, 0.26, 0.09 | Niedrig |

### Korrektur erforderlich:
Die CLAUDE.md gibt **32GB RAM** an, aber der Server hat nur **16GB RAM** (CX43 Spezifikation).

---

## 2. CONTAINER-ÜBERSICHT

| Container | Status | RAM | CPU | Ports | Netzwerk | Problem? |
|-----------|--------|-----|-----|-------|----------|----------|
| **open-webui** | ✅ Up 10h (healthy) | 1.15 GB | 0.33% | 3000→8080 | osp-network | - |
| **chromadb** | ✅ Up 3d | 102 MB | 0.00% | 127.0.0.1:8000 | osp-network | - |
| **anthropic-proxy** | ⚠️ Up 3d (unhealthy) | 357 MB | 0.30% | 127.0.0.1:4000 | osp-network | Health-Check failed |
| **n8n** | ❌ NICHT VORHANDEN | - | - | - | - | **502 Bad Gateway** |
| **ollama** | ❌ NICHT VORHANDEN | - | - | - | - | - |

### Container-Details:

```
NAMES             STATUS                  PORTS
anthropic-proxy   Up 3 days (unhealthy)   127.0.0.1:4000->4000/tcp
open-webui        Up 10 hours (healthy)   0.0.0.0:3000->8080/tcp
chromadb          Up 3 days               127.0.0.1:8000->8000/tcp
```

---

## 3. RAM-RANKING (Größte Verbraucher)

| Rang | Container | RAM | Anteil |
|------|-----------|-----|--------|
| 1 | **open-webui** | 1.15 GB | 7.57% |
| 2 | **anthropic-proxy** | 357 MB | 34.85% (von 1GB Limit) |
| 3 | **chromadb** | 102 MB | 0.65% |
| **Total Docker** | | **~1.6 GB** | **~10%** |

**Fazit:** RAM-Verbrauch ist sehr niedrig. Genug Kapazität für weitere Dienste.

---

## 4. N8N-PROBLEM-DIAGNOSE

### Root Cause Analysis:

| Prüfpunkt | Status | Details |
|-----------|--------|---------|
| Nginx-Konfiguration | ✅ Vorhanden | `/etc/nginx/sites-enabled/n8n` |
| Nginx → localhost:5678 | ✅ Korrekt | Proxy-Pass konfiguriert |
| SSL/Certbot | ✅ OK | Nutzt osp.schneider-kabelsatzbau.de Zertifikat |
| n8n Docker-Image | ✅ Vorhanden | `docker.n8n.io/n8nio/n8n:latest` (1.04GB) |
| n8n Docker-Volume | ✅ Vorhanden | `osp-n8n-data` |
| n8n in docker-compose.yml | ❌ **FEHLT** | Nicht definiert! |
| n8n Container | ❌ **NICHT VORHANDEN** | Nie erstellt |
| Port 5678 | ❌ **GESCHLOSSEN** | Connection refused |

### Nginx-Error-Log (Auszug):
```
2025/12/18 21:48:47 [error] connect() failed (111: Connection refused)
while connecting to upstream, server: n8n.schneider-kabelsatzbau.de,
upstream: "http://127.0.0.1:5678/"
```

### ROOT CAUSE:
**n8n wurde NIEMALS in der docker-compose.yml definiert!**

Die Nginx-Konfiguration und das Docker-Image/Volume wurden eingerichtet, aber der Container wurde nie zur docker-compose.yml hinzugefügt und daher nie gestartet.

---

## 5. EMPFOHLENE AKTIONEN

### Priorität 1 (Sofort - n8n 502 beheben):

```bash
# Option A: n8n zur docker-compose.yml hinzufügen (EMPFOHLEN)
# Füge folgenden Service zur /opt/osp/docker-compose.yml hinzu:

  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n
    restart: always
    ports:
      - "127.0.0.1:5678:5678"
    volumes:
      - osp-n8n-data:/home/node/.n8n
    environment:
      - N8N_HOST=n8n.schneider-kabelsatzbau.de
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.schneider-kabelsatzbau.de/
      - GENERIC_TIMEZONE=Europe/Berlin
    networks:
      - osp-network

# Dann:
docker-compose -f /opt/osp/docker-compose.yml up -d n8n
```

```bash
# Option B: n8n manuell starten (Quick-Fix)
docker run -d \
  --name n8n \
  --restart always \
  -p 127.0.0.1:5678:5678 \
  -v osp-n8n-data:/home/node/.n8n \
  -e N8N_HOST=n8n.schneider-kabelsatzbau.de \
  -e N8N_PORT=5678 \
  -e N8N_PROTOCOL=https \
  -e WEBHOOK_URL=https://n8n.schneider-kabelsatzbau.de/ \
  -e GENERIC_TIMEZONE=Europe/Berlin \
  --network osp-network \
  docker.n8n.io/n8nio/n8n:latest
```

### Priorität 2 (anthropic-proxy Health-Check):

```bash
# Prüfen warum unhealthy:
docker logs anthropic-proxy --tail 50

# Ggf. Neustart:
docker restart anthropic-proxy
```

### Priorität 3 (Dokumentation korrigieren):

- [ ] CLAUDE.md: RAM von 32GB auf **16GB** korrigieren
- [ ] Server-Typ überprüfen (CX43 hat standardmäßig 16GB)

### Priorität 4 (Optional - Ollama):

Falls KI-Modelle lokal benötigt werden:
```bash
# Ollama hinzufügen (benötigt ~4-8GB RAM pro Modell!)
# VORSICHT: Bei nur 16GB RAM genau prüfen!
```

---

## 6. ARCHITEKTUR-DIAGRAMM (Aktuell)

```
                           INTERNET
                               │
                               ▼
                        ┌─────────────┐
                        │   Hetzner   │
                        │   Firewall  │
                        │  (ufw)      │
                        └──────┬──────┘
                               │
              Ports: 22, 80, 443, 8080
                               │
                               ▼
                        ┌─────────────┐
                        │   NGINX     │
                        │  (Reverse   │
                        │   Proxy)    │
                        └──────┬──────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│ osp.schneider- │   │ n8n.schneider- │   │  :8080         │
│ kabelsatzbau.de│   │ kabelsatzbau.de│   │ Werkzeugmappe  │
│     :443       │   │     :443       │   │                │
└───────┬────────┘   └───────┬────────┘   └───────┬────────┘
        │                    │                    │
        ▼                    ▼                    ▼
   localhost:3000      localhost:5678       /opt/osp/webapp/
        │                    │
        │                    │
        ▼                    ▼
┌────────────────┐   ┌────────────────┐
│  open-webui    │   │     n8n        │
│   Container    │   │   Container    │
│   (healthy)    │   │   ❌ FEHLT!    │
│   1.15 GB RAM  │   │                │
└───────┬────────┘   └────────────────┘
        │
        │ CHROMA_HTTP_HOST=chromadb
        ▼
┌────────────────┐
│   chromadb     │
│   Container    │
│   102 MB RAM   │
│  localhost:8000│
└────────────────┘

┌────────────────┐
│anthropic-proxy │
│  (LiteLLM)     │
│  ⚠️ unhealthy  │
│  357 MB RAM    │
│ localhost:4000 │
└────────────────┘

══════════════════════════════════════════════════════════
                    Docker Network: osp-network
                    Subnet: 172.19.0.0/16
══════════════════════════════════════════════════════════
```

---

## 7. DOMAINS & SSL

| Domain | Ziel | SSL | Status |
|--------|------|-----|--------|
| osp.schneider-kabelsatzbau.de | localhost:3000 | ✅ Let's Encrypt | ✅ OK |
| n8n.schneider-kabelsatzbau.de | localhost:5678 | ✅ Let's Encrypt | ❌ 502 |
| 46.224.102.30:8080 | /opt/osp/webapp | - | ✅ OK |

---

## 8. DOCKER-COMPOSE.YML (Aktuell)

Services definiert:
1. **open-webui** - Open WebUI v0.6.x
2. **chromadb** - ChromaDB v1.0.0
3. **anthropic-proxy** - LiteLLM Proxy

**FEHLEND:**
- n8n (obwohl Nginx-Config + Image + Volume existieren)
- ollama (nicht eingerichtet)

---

## 9. NÄCHSTE SCHRITTE

1. [ ] **SOFORT:** n8n-Service zur docker-compose.yml hinzufügen
2. [ ] **SOFORT:** Container starten: `docker-compose up -d n8n`
3. [ ] anthropic-proxy Health-Check untersuchen
4. [ ] CLAUDE.md RAM-Angabe korrigieren (32GB → 16GB)
5. [ ] Entscheidung: Wird Ollama benötigt? (RAM-Planung!)

---

*Analyse erstellt: 2025-12-18 21:53 UTC*
*Erstellt mit: Claude Code (Opus 4.5)*
