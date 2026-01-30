# [IT][OSP] OSP KI-Chatbot Projekt

Version: 1.4 RAG | TAG: [IT][OSP] | Erstellt: 2025-11-29 | Aktualisiert: 2025-12-23 | Autor: AL | Verantwortlich: AL (IT/KI), CS (GF) | Cluster: C4-Support | Zugriff: L3-FÃ¼hrung | Status: PRODUKTIV | Stage: 2 | Basis: IT_OSP_KI-Chatbot_v1.0.md + Hetzner_Server_OSP_Dokumentation.md

**Projektstart:** 14.11.2025 | **Go-Live:** 26.11.2025 | **Pilot-Ende:** 19.12.2025

---

## ðŸŽ¯ PROJEKTZWECK

**OSP KI-Chatbot** = Technische Infrastruktur fÃ¼r OSP-Wissensmanagement:

1. **OSPUI (Open WebUI)** - UI fÃ¼r KI-Interaktion
2. **ChromaDB** - Vektordatenbank fÃ¼r RAG
3. **Ollama** - Lokale LLM-Runtime (mistral:7b, llama2:13b)
4. **n8n** - Workflow-Automation (geplant)

**Ziele:**
- âœ… 40% Zeitersparnis bei Standardanfragen
- âœ… 85% Fehlerreduktion
- âœ… DSGVO-konform (DE-Standort)
- âœ… Selbst-gehostet

---

## ðŸ“‹ INHALTSVERZEICHNIS

1. [ProjektÃ¼bersicht](#projektÃ¼bersicht)
2. [Hetzner Server-Infrastruktur](#hetzner-server-infrastruktur)
3. [Docker-Container-Architektur](#docker-container-architektur)
4. [OSPUI Konfiguration](#ospui-open-webui-konfiguration)
5. [ChromaDB Vektordatenbank](#chromadb-vektordatenbank)
6. [Claude API (LiteLLM)](#claude-api-litellm)
7. [n8n Workflow-Automation](#n8n-workflow-automation)
8. [Netzwerk & Sicherheit](#netzwerk--sicherheit)
9. [Backup & Wartung](#backup--wartung)
10. [Monitoring & Performance](#monitoring--performance)
11. [Troubleshooting](#troubleshooting)
12. [Querverweise](#querverweise)

---

## PROJEKTÃœBERSICHT

### Architektur-Diagramm

```
User (AL,CS,SV,SK,TS) â†’ https://osp.schneider-kabelsatzbau.de
    â†“
Nginx Reverse Proxy (SSL/TLS)
    â†“
Hetzner CX43 (Ubuntu 24.04, 8vCPU, 16GB RAM, 160GB SSD, Falkenstein DE)
    â†“
Docker-Compose Stack
    â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”
â”‚ OSPUI  â”‚ ChromaDB â”‚ Ollama â”‚ n8n â”‚
â”‚ :3000  â”‚ :8000    â”‚ :11434 â”‚:5678â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”˜
```

---

### Tech-Stack

| Komponente | Version | Zweck | RAM | Storage |
|------------|---------|-------|-----|---------|
| Ubuntu | 24.04 LTS | OS | - | 50GB |
| Docker | 28.2.2 | Runtime | - | 10GB |
| OSPUI | 0.6.43 | UI/Orchestr. | 2GB | 5GB |
| ChromaDB | 1.3.6 | Vektordatenbank | 2GB | 20GB |
| LiteLLM | main-latest | Claude API Proxy | 1GB | 2GB |
| n8n | latest | Workflow | 1GB | 5GB |
| Nginx | 1.26 | Reverse Proxy | 512MB | 1GB |

**Gesamt:** RAM 15GB/16GB (94%), Storage 151GB/160GB (94%)

---

### Projekt-Timeline

| Datum | Meilenstein | Status |
|-------|-------------|--------|
| 14.11.25 | Kick-off, Konzept | âœ… |
| 20.11.25 | Hetzner Server bestellt | âœ… |
| 22.11.25 | Server Setup (Ubuntu, Docker) | âœ… |
| 24.11.25 | OSPUI + ChromaDB deployed | âœ… |
| 25.11.25 | Ollama + Modelle (mistral:7b) | âœ… |
| **26.11.25** | **GO-LIVE** - 5 Pilot-User | âœ… |
| 29.11.25 | RAG-Import Infrastruktur | âœ… |
| 06.12.25 | Erste RAG-Dokumente | â³ |
| 19.12.25 | **Pilot-Ende** - Evaluation | â³ |
| 15.01.26 | Rollout Phase 2 (20+ User) | â³ |

---

## HETZNER SERVER-INFRASTRUKTUR

### Server-Details

**Hetzner Cloud CX43** â¬†ï¸ Upgrade von CX33

| Eigenschaft | Wert |
|-------------|------|
| Server-Name | osp-webui |
| CPU | 8 vCPU (AMD EPYC) â¬†ï¸ Upgrade |
| RAM | 16GB DDR4 â¬†ï¸ Upgrade |
| Storage | 160GB NVMe SSD |
| Netzwerk | 20TB Traffic/Monat |
| Standort | Falkenstein, DE ðŸ‡©ðŸ‡ª |
| IPv4 | 46.224.102.30 |
| IPv6 | 2a01:4f8:c013:b41c:: |
| OS | Ubuntu 24.04.1 LTS |
| Kernel | 6.8.0-49-generic |

**Kosten:** â‚¬6/Monat (inkl. Backup)

---

### Netzwerk-Konfiguration

**Firewall (Hetzner Cloud):**

| Port | Protokoll | Quelle | Zweck |
|------|-----------|--------|-------|
| 22 | TCP | 0.0.0.0/0 | SSH (Key-Auth) |
| 80 | TCP | 0.0.0.0/0 | HTTPâ†’HTTPS Redirect |
| 443 | TCP | 0.0.0.0/0 | HTTPS (OSPUI) |

**Blockiert:** 3000 (OSPUI), 8000 (ChromaDB), 11434 (Ollama), 5678 (n8n)

**Zugriff:** Nur via Nginx Reverse Proxy!

---

### Domains & URLs

| Dienst | URL | Status |
|--------|-----|--------|
| OSPUI | https://osp.schneider-kabelsatzbau.de | âœ… Aktiv |
| n8n | https://n8n.schneider-kabelsatzbau.de | âœ… Aktiv |

---

### DNS-Verwaltung

**Provider:** Attentio GmbH  
**Kontakt:** Kevin Lieser  
**E-Mail:** k.lieser@attentio.de  
**Telefon:** 02662 948007-0

**Domain:** schneider-kabelsatzbau.de

**DNS-EintrÃ¤ge:**
```
osp.schneider-kabelsatzbau.de   â†’ A: 46.224.102.XXX, AAAA: 2a01:4f8:c013:b41c::
n8n.schneider-kabelsatzbau.de   â†’ A: 46.224.102.XXX, AAAA: 2a01:4f8:c013:b41c::
```

**Neue Subdomain:** Anfrage an Attentio nÃ¶tig!

---

### SSH-Zugang

**User:** root  
**Auth:** SSH-Key + Passwort (siehe Passwort-Manager)  
**Keys:** AL

**SSH-Config:**
```
Host osp-server
    HostName 46.224.102.30
    User root
    IdentityFile ~/.ssh/id_ed25519_osp
```

**Verbindung:** `ssh osp-server`

**Hetzner Console:** https://console.hetzner.com (Projekt: OSP-Chatbot)

---

### Storage-Layout

```
/ (Root)                160GB NVMe
â”œâ”€â”€ /var/lib/docker/    120GB
â”‚   â”œâ”€â”€ volumes/
â”‚   â”‚   â”œâ”€â”€ open-webui_data/      5GB
â”‚   â”‚   â”œâ”€â”€ chromadb_data/       20GB
â”‚   â”‚   â”œâ”€â”€ ollama_data/         60GB
â”‚   â”‚   â””â”€â”€ n8n_data/             5GB
â”‚   â””â”€â”€ images/                  10GB
â”œâ”€â”€ /mnt/HC_Volume_104189729/osp/                    10GB
â”‚   â”œâ”€â”€ docker-compose.yml
â”‚   â”œâ”€â”€ nginx/
â”‚   â”œâ”€â”€ backups/
â”‚   â””â”€â”€ scripts/
â”œâ”€â”€ /home/                        5GB
â””â”€â”€ /var/log/                     5GB
```

---

### Installierte Software

**System-Pakete:**
```bash
apt install -y curl wget git vim htop nano docker.io docker-compose certbot python3-certbot-nginx netdata
```

**Docker-Version:**
```
Docker 27.3.1, build ce12230
Docker Compose v2.29.7
```

---

## DOCKER-CONTAINER-ARCHITEKTUR

### Docker-Compose-Datei

**Pfad:** `/mnt/HC_Volume_104189729/osp/docker-compose.yml`

```yaml
version: '3.8'

services:
  chromadb:
    image: chromadb/chroma:0.5.15
    container_name: osp-chromadb
    hostname: chromadb
    ports: ["127.0.0.1:8000:8000"]
    volumes: [chromadb_data:/chroma/chroma]
    environment:
      CHROMA_DB_IMPL: duckdb+parquet
      CHROMA_TELEMETRY_DISABLED: "true"
      CHROMA_SERVER_AUTH_PROVIDER: "chromadb.auth.token.TokenAuthServerProvider"
      CHROMA_SERVER_AUTH_CREDENTIALS_FILE: "/chroma/server.htpasswd"
    restart: always
    networks: [osp-network]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v2/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3

  ollama:
    image: ollama/ollama:latest
    container_name: osp-ollama
    hostname: ollama
    ports: ["127.0.0.1:11434:11434"]
    volumes: [ollama_data:/root/.ollama]
    environment:
      OLLAMA_KEEP_ALIVE: "24h"
      OLLAMA_HOST: "0.0.0.0:11434"
    restart: always
    networks: [osp-network]
    deploy:
      resources:
        limits: {memory: 12G}
        reservations: {memory: 8G}

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: osp-webui
    hostname: open-webui
    ports: ["127.0.0.1:3000:8080"]
    depends_on: [chromadb, ollama]
    volumes: [open-webui_data:/app/backend/data]
    environment:
      WEBUI_URL: "https://osp.schneider-kabelsatzbau.de"
      WEBUI_NAME: "OSP KI-Assistent"
      OLLAMA_BASE_URL: "http://ollama:11434"
      VECTOR_DB: "chroma"
      CHROMA_HTTP_HOST: "chromadb"
      CHROMA_HTTP_PORT: "8000"
      CHROMA_TENANT: "osp_tenant"
      RAG_EMBEDDING_MODEL: "multilingual-e5-large"
      ENABLE_SIGNUP: "false"
      DEFAULT_USER_ROLE: "user"
      DEFAULT_LOCALE: "de"
      ENABLE_ADMIN_EXPORT: "true"
      ENABLE_ADMIN_CHAT_ACCESS: "false"
      JWT_EXPIRES_IN: "7d"
      GLOBAL_LOG_LEVEL: "INFO"
      THREAD_POOL_SIZE: "40"
    restart: always
    networks: [osp-network]
    deploy:
      resources:
        limits: {memory: 4G}
        reservations: {memory: 2G}

  n8n:
    image: n8nio/n8n:latest
    container_name: osp-n8n
    hostname: n8n
    ports: ["127.0.0.1:5678:5678"]
    volumes: [n8n_data:/home/node/.n8n]
    environment:
      N8N_HOST: "n8n.osp.local"
      N8N_PORT: "5678"
      N8N_PROTOCOL: "http"
      WEBHOOK_URL: "https://osp.schneider-kabelsatzbau.de/n8n"
    restart: always
    networks: [osp-network]

volumes:
  open-webui_data:
  chromadb_data:
  ollama_data:
  n8n_data:

networks:
  osp-network:
    driver: bridge
```

---

### Container-Management

**Start:** `docker-compose up -d`  
**Stop:** `docker-compose down`  
**Logs:** `docker-compose logs -f [container]`  
**Status:** `docker-compose ps`  
**Restart:** `docker-compose restart [container]`

---

## OSPUI (OPEN WEBUI) KONFIGURATION

### Benutzer-Accounts

**6 Accounts erstellt (26.11.2025):**

| # | Name | E-Mail | Rolle | OSP-Level |
|---|------|--------|-------|-----------|-
| 1 | AL | andreas.loehr@... | Admin | L3 |
| 2 | CS | christoph.schneider@... | Admin | L4 |
| 3 | SV | sebastian.vierschilling@... | User | L4 |
| 4 | SK | stefan.kandorfer@... | User | L2 |
| 5 | TS | tobias.schmidt@... | User | L3 |
| 6 | MD | marcel.duetzer@... | User | L2 |

**Rollen:**
- **Admin:** AL, CS (volle Konfiguration)
- **User:** SV, SK, TS, MD (Chat + eigene Modelle)

---

### OSP-Level-Mapping

**OSPUI unterstÃ¼tzt keine nativen OSP-Level â†’ Workaround via ChromaDB-Metadata-Filter**

| OSP-Level | Beschreibung | OSPUI-Rolle | User |
|-----------|--------------|-------------|------|
| **L1** | Ã–ffentlich | User | Alle |
| **L2** | Abteilung | User | SK, MD |
| **L3** | FÃ¼hrung | User/Admin | AL, TS |
| **L4** | Geheim | Admin | CS, SV |

**Filterung:** Im Backend via ChromaDB-Metadata (`user_level: L1/L2/L3/L4`)

---

### OSPUI-Funktionen

**Aktiviert:**
- âœ… Chat mit RAG-UnterstÃ¼tzung
- âœ… Modell-Auswahl (mistral, llama2, gpt-4)
- âœ… Dokumente hochladen
- âœ… Custom-Modelle erstellen
- âœ… Chat-Export
- âœ… Message-Rating

**Deaktiviert:**
- âŒ Signup (nur Admin-Invite)
- âŒ Community-Sharing
- âŒ Web-Search (noch)
- âŒ Image-Generation (noch)
- âŒ Admin-Chat-Access (DSGVO)

---

### Einstellungen

**Lokalisierung:** Deutsch (de)  
**Theme:** Dark Mode  
**JWT-Expiry:** 7 Tage  
**Max Upload:** 100MB  
**Log-Level:** INFO  
**Auto-Save:** Aktiviert

---

## CHROMADB VEKTORDATENBANK

### Collection: OSP_COMPLETE

**Eine zentrale Collection, Filterung via Metadata**

**Konfiguration:**
```python
collection_name = "OSP_COMPLETE"
embedding_function = "multilingual-e5-large"
distance_metric = "cosine"
```

---

### Embedding-Modell

**multilingual-e5-large (lokal)**
- **Sprache:** Multilingual (de, en)
- **Dimensionen:** 384
- **Speed:** ~120 Embeddings/s
- **QualitÃ¤t:** Gut fÃ¼r deutsche Fachtexte
- **GrÃ¶ÃŸe:** ~80MB

**Alternative (geplant):** OpenAI `text-embedding-3-small` (hÃ¶here QualitÃ¤t, Kosten: â‚¬0.02/1M Tokens)

---

### Metadata-Schema

```python
metadata = {
    "source": "IT_DOKU_IT-Dokumentation.md",
    "tag": "IT", "sub_tag": "DOKU",
    "cluster": "C4", "version": "2.1",
    "chunk_id": "IT_DOKU_CH01",
    "user_level": "L2",
    "keywords": ["Server", "Hyper-V", "Backup"]
}
```

---

### Import-Workflow

**Schritt 1: Dokument RAG-optimieren**  
â†’ Siehe `IT_RAG_Richtlinie.md`

**Schritt 2: Dokument nach `/main/[TAG]/` verschieben**

**Schritt 3: ChromaDB-Scan**
```python
from chromadb import Client
client = Client()
collection = client.get_collection("OSP_COMPLETE")

# Dokumente scannen
docs = scan_directory("/main/")

# Chunks erstellen + embedden
for doc in docs:
    chunks = split_document(doc, chunk_size=1000, overlap=175)
    embeddings = embed_chunks(chunks)
    collection.add(documents=chunks, embeddings=embeddings, metadatas=metadata)
```

**Schritt 4: Test-Queries durchfÃ¼hren**

---

### Queries (Beispiel)

**User SK (L2) sucht "Wo ist SRV-FS?":**
```python
results = collection.query(
    query_texts=["Wo ist SRV-FS?"],
    n_results=5,
    where={"$or": [{"user_level": "L1"}, {"user_level": "L2"}]}
)
```

**Ergebnis:** Nur L1 + L2 Chunks (L3/L4 gefiltert)

---

### Statistiken (Stand 15.12.2025)

| Metrik | Aktuell | Ziel |
|--------|---------|------|
| Collections | 2 | 3 |
| Dokumente | 58 | 80+ |
| Chunks | ~580 | 800+ |
| Embeddings | ~580 | 800+ |
| Query-Latenz | 250ms | <500ms |
| Speicher | 8GB | 20GB |

---

## PIPELINE-ARCHITEKTUR (NEU v1.3)

### Pre-Processing-Module (15.12.2025)

Am 15.12.2025 wurden **4 Pre-Processing-Module** implementiert, die die RAG-QualitÃ¤t signifikant verbessern:

```
USER MESSAGE
     â”‚
     â–¼
STEP -1: Query-Normalisierung
     â”‚    "Mitarbieter AL" â†’ "mitarbeiter al"
     â”‚    Modul: query_normalizer.py
     â–¼
STEP 0: MA-KÃ¼rzel Expansion
     â”‚    "mitarbeiter al" â†’ "mitarbeiter al Personalstamm HR_CORE..."
     â”‚    Modul: ma_preprocessing.py
     â–¼
STEP 1: Kontakt-Lookup (WKZ-Nummern)
     â”‚    "WKZ fÃ¼r 0460-202-2091" â†’ Direktantwort
     â”‚    Modul: kontakt_lookup.py
     â–¼
STEP 1.5: Keyword-Filter
     â”‚    "NULL-FEHLER" â†’ QM_CORE direkt laden
     â”‚    Modul: keyword_filter.py
     â–¼
STEP 2: RAG mit TAG-FILTER
     â”‚    ChromaDB WHERE: {"tag": "HR"}
     â”‚    Modul: tag_router.py
     â–¼
LLM Response
```

---

### Modul-Ãœbersicht

| Modul | Problem gelÃ¶st | Verbesserung |
|-------|----------------|--------------|
| **Query-Normalizer** | Tippfehler nicht gefunden | 70% â†’ 90%+ |
| **MA-Preprocessing** | KÃ¼rzel (AL, MD) nicht gefunden | 0% â†’ 100% |
| **Keyword-Filter** | Kritische Begriffe falsch geroutet | 70% â†’ 95%+ |
| **Tag-Router** | KERN-Layer PrÃ¤zision unzureichend | 70% â†’ 100% |

---

### Neue Valves (Konfiguration)

| Valve | Default | Beschreibung |
|-------|---------|--------------|
| `ENABLE_QUERY_NORMALIZATION` | True | Tippfehler-Korrektur aktivieren |
| `ENABLE_MA_PREPROCESSING` | True | MA-KÃ¼rzel Expansion aktivieren |
| `ENABLE_KEYWORD_FILTER` | True | Keyword-Trigger Pre-RAG aktivieren |
| `ENABLE_TAG_ROUTING` | True | ChromaDB WHERE-Filter aktivieren |
| `MA_KUERZEL_PATH` | /app/.../ma_kuerzel.json | Pfad zur KÃ¼rzel-JSON |
| `DOCUMENTS_PATH` | /app/.../docs | Pfad zum Documents-Verzeichnis |

---

### Container-Pfade fÃ¼r Module

| Host-Pfad | Container-Pfad |
|-----------|----------------|
| /opt/osp/pipelines/ | /app/backend/data/pipelines/ |
| /opt/osp/pipelines/modules/ | /app/backend/data/pipelines/modules/ |
| /opt/osp/lookups/ | /app/backend/data/lookups/ |
| /opt/osp/documents/ | /app/backend/data/docs/ |

---

### Metriken (Stand 15.12.2025)

| Metrik | Vorher | Nachher | Ziel |
|--------|--------|---------|------|
| Overall Retrieval | 80% | ~95% | 95%+ |
| KERN-Layer PrÃ¤zision | 70% | 100% | 100% |
| Tippfehler-Toleranz | 70% | ~90% | 90%+ |
| MA-KÃ¼rzel Queries | 0% | 100% | 100% |
| Keyword PrÃ¤zision | 70% | ~95% | 100% |
| Avg. Query Latenz | 206ms | ~250ms | <500ms |

---

## OLLAMA LLM-RUNTIME

### Installierte Modelle

| Modell | GrÃ¶ÃŸe | RAM | Zweck | Status |
|--------|-------|-----|-------|--------|
| mistral:7b | 4GB | 6GB | Standard-Chat | âœ… Aktiv |
| llama2:13b | 7.3GB | 10GB | Komplexe Anfragen | âœ… Aktiv |
| codellama:7b | 3.8GB | 6GB | Code-Generierung | â³ Geplant |

**Gesamt:** ~15GB Modelle, ~10GB RAM-Nutzung

---

### Modell-Download

```bash
docker exec osp-ollama ollama pull mistral:7b
docker exec osp-ollama ollama pull llama2:13b
```

---

### Modell-Auswahl-Strategie

**Kriterien:**
- **Geschwindigkeit:** mistral:7b (Standard)
- **QualitÃ¤t:** llama2:13b (komplexe Anfragen)
- **Deutsch:** Beide gut (multilingual)
- **Kosten:** Lokal = â‚¬0

**Fallback:** gpt-4 (OpenAI API) fÃ¼r kritische Anfragen

---

### Performance

| Modell | Tokens/s | Response-Zeit | QualitÃ¤t |
|--------|----------|---------------|----------|
| mistral:7b | 40 | 3.2s | â­â­â­â­ |
| llama2:13b | 25 | 5.1s | â­â­â­â­â­ |
| gpt-4 (API) | 60 | 2.8s | â­â­â­â­â­ |

---

## N8N WORKFLOW-AUTOMATION

### Status

**â³ GEPLANT - Q1 2026**

**Workflows (geplant):**
1. **Dokument-Import:** SharePoint â†’ ChromaDB Auto-Sync
2. **Benachrichtigungen:** Neue RAG-Docs â†’ Slack/E-Mail
3. **Backup:** ChromaDB â†’ Terra Cloud (wÃ¶chentlich)
4. **Monitoring:** Container-Health â†’ Webhook
5. **User-Onboarding:** Neuer MA â†’ OSPUI-Account + E-Mail

---

### Konfiguration (vorbereitet)

**URL:** http://localhost:5678 (intern)  
**Webhook:** https://osp.schneider-kabelsatzbau.de/n8n  
**Storage:** 5GB Docker-Volume

---

## NETZWERK & SICHERHEIT

### SSL/TLS-Zertifikat

**Let's Encrypt (Certbot):**
```bash
certbot --nginx -d osp.schneider-kabelsatzbau.de
```

**Details:**
- **Anbieter:** Let's Encrypt
- **GÃ¼ltig bis:** 26.02.2026
- **Auto-Renewal:** âœ… Alle 90 Tage via Certbot Cron
- **Registrierte E-Mail:** a.loehr@schneider-kabelsatzbau.de
- **Zertifikat-Pfad:** `/etc/letsencrypt/live/osp.schneider-kabelsatzbau.de/`
- **Cipher Suites:** TLS 1.2+ (A+ Rating)

**Befehle:**
```bash
certbot renew                 # Manuell erneuern
certbot renew --dry-run       # Test-Renewal
certbot certificates          # Status prÃ¼fen
systemctl reload nginx        # Nach Erneuerung
```

---

### Nginx-Konfiguration

**Pfad:** `/etc/nginx/sites-available/osp`

```nginx
server {
    listen 443 ssl http2;
    server_name osp.schneider-kabelsatzbau.de;
    
    ssl_certificate /etc/letsencrypt/live/osp.schneider-kabelsatzbau.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/osp.schneider-kabelsatzbau.de/privkey.pem;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_read_timeout 3600s;
    }
}
```

---

### Firewall

**UFW Status:** âœ… Aktiv

| Port | Protokoll | Dienst | Zweck |
|------|-----------|--------|-------|
| 22 | TCP | SSH | Server-Verwaltung |
| 80 | TCP | HTTP | â†’ 443 Redirect |
| 443 | TCP | HTTPS | Nginx Reverse Proxy |

**Befehle:**
```bash
ufw status                     # Status anzeigen
ufw allow 443/tcp              # Regel hinzufÃ¼gen
ufw delete allow 80/tcp        # Regel entfernen
ufw enable                     # Firewall aktivieren
ufw reload                     # Neu laden
```

**Interne Ports (nicht extern):**
- 3000 (OSPUI), 8000 (ChromaDB), 11434 (Ollama), 5678 (n8n)

---

### DSGVO-KonformitÃ¤t

**Datenstandort:** Deutschland (Falkenstein)  
**Datenverarbeitung:** Lokal (kein Cloud-Export)  
**Backups:** Terra Cloud (DE)  
**Datenschutz:**
- Keine externen APIs (auÃŸer optional gpt-4)
- Keine Telemetrie
- User-Daten isoliert
- 90 Tage Retention

---

## BACKUP & WARTUNG

### Backup-Strategie

**Hetzner Server-Backup (Cloud):**
- **Anbieter:** Hetzner Cloud (integriert)
- **Slots:** 7 Backups (automatisch rotierend)
- **Automatisch:** âœ… TÃ¤glich, 7 Tage Retention
- **Kosten:** ~â‚¬1/Monat (20% Server-Tarif)
- **Verwaltung:** https://console.hetzner.com â†’ Server â†’ Backups
- **Wiederherstellung:** Backup auswÃ¤hlen â†’ "Wiederherstellen" â†’ ~10 Min

**Docker-Volumes (Lokal):**

**TÃ¤glich (02:00 Uhr):**
```bash
#!/bin/bash
# /mnt/HC_Volume_104189729/osp/scripts/backup-daily.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/mnt/HC_Volume_104189729/osp/backups
mkdir -p $BACKUP_DIR

docker run --rm \
  -v open-webui_data:/data \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/open-webui_$DATE.tar.gz /data

docker run --rm \
  -v chromadb_data:/data \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/chromadb_$DATE.tar.gz /data

docker run --rm \
  -v ollama_data:/data \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/ollama_$DATE.tar.gz /data

find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
echo "Backup completed: $DATE"
```

**Cron:** `0 2 * * * /mnt/HC_Volume_104189729/osp/scripts/backup-daily.sh >> /var/log/osp-backup.log 2>&1`

---

### Offsite-Backup

**Terra Cloud (extern):**
- WÃ¶chentlich (So 03:00)
- 4 Wochen Retention
- VerschlÃ¼sselt (AES-256)

---

### Update-Prozedur

**System-Updates (Ubuntu):**
```bash
apt update                    # Paketlisten aktualisieren
apt upgrade -y                # Pakete upgraden
apt autoremove -y             # Nicht benÃ¶tigte Pakete entfernen
reboot                        # Bei Kernel-Updates
```

**Docker-Container (monatlich - 1. So, 04:00):**
```bash
#!/bin/bash
# /mnt/HC_Volume_104189729/osp/scripts/update-monthly.sh

cd /opt/open-webui

docker-compose pull           # Neueste Images herunterladen
docker-compose down           # Container stoppen
docker-compose up -d          # Mit neuen Images starten
docker image prune -a -f      # Alte Images lÃ¶schen
docker-compose logs --tail=50 # Logs prÃ¼fen
```

**Speicherplatz freigeben:**
```bash
docker system prune -a        # Docker-Cleanup (Container, Images, Volumes)
journalctl --vacuum-time=7d   # Alte Logs lÃ¶schen
du -sh /var/log/*             # Log-GrÃ¶ÃŸen prÃ¼fen
```

---

### Wartungs-Kalender

| Task | Frequenz | Zeit | Verantw. |
|------|----------|------|----------|
| Backup lokal | TÃ¤glich | 02:00 | Auto |
| Backup offsite | WÃ¶chentlich | So 03:00 | Auto |
| Updates | Monatlich | 1.So 04:00 | AL |
| SSL-Erneuerung | 90 Tage | Auto | Certbot |
| Disk-Space | WÃ¶chentlich | Mo 08:00 | AL |
| Log-Rotation | TÃ¤glich | 00:00 | Auto |

---

## MONITORING & PERFORMANCE

### Resource-Monitoring

**Netdata:** http://116.203.XXX.XXX:19999 (intern)

**Metriken:**
- CPU-Auslastung (Ziel: <80%)
- RAM-Nutzung (Ziel: <90%)
- Disk-Usage (Ziel: <85%)
- Container-Status

---

### Performance-Benchmarks

**Ziel-Werte (Pilot):**

| Metrik | Ziel | Aktuell | Status |
|--------|------|---------|--------|
| RAG-Query-Latenz | <2s | 1.2s | âœ… |
| LLM-Response | <5s | 3.8s | âœ… |
| Embedding-Speed | >100/s | 120/s | âœ… |
| Concurrent Users | 5 | 5 | âœ… |
| Uptime | >99% | 99.8% | âœ… |

---

### Logs

**Log-Rotation:**
```bash
/var/log/osp-*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
}
```

**Wichtige Logs:**
- `/var/log/osp-backup.log`
- `/var/log/nginx/access.log`
- `/var/log/nginx/error.log`
- Docker: `docker-compose logs`

---

## TROUBLESHOOTING

### Problem: Container startet nicht

**Symptome:** `docker-compose ps` â†’ Exited (1)

**LÃ¶sung:**
```bash
docker-compose logs [container]
docker-compose restart [container]
# Bei Bedarf: Rebuild
docker-compose up -d --build
```

---

### Problem: ChromaDB nicht erreichbar

**Symptome:** "Failed to connect to ChromaDB" / Keine RAG-Ergebnisse

**LÃ¶sung:**
```bash
docker ps | grep chromadb
curl http://localhost:8000/api/v2/heartbeat
docker-compose restart chromadb
docker logs osp-chromadb --tail=100
```

---

### Problem: Out of Memory (OOM)

**Symptome:** Container unerwartet beendet / "OOM Killed"

**LÃ¶sung:**
```bash
docker stats
# In docker-compose.yml: memory: 12G â†’ 10G
docker-compose down
docker-compose up -d
```

---

### Problem: Disk-Space voll

**Symptome:** "No space left on device"

**LÃ¶sung:**
```bash
df -h
docker system df
docker image prune -a
docker system prune -a --volumes
find /mnt/HC_Volume_104189729/osp/backups -mtime +7 -delete
```

---

### Problem: SSL-Zertifikat abgelaufen

**Symptome:** Browser-Warnung: "Connection not private"

**LÃ¶sung:**
```bash
certbot certificates          # Status prÃ¼fen
certbot renew --nginx         # Manuell erneuern
certbot renew --dry-run       # Test ohne Erneuerung
systemctl reload nginx        # Nginx neu laden
curl -I https://osp.schneider-kabelsatzbau.de
```

---

### Problem: Dienst nicht erreichbar

**Symptome:** Timeout, Connection refused, 502/503 Error

**Diagnose-Schritte:**
```bash
# 1. Container-Status
docker ps

# 2. Container-Logs
docker logs open-webui --tail 100
docker logs chromadb --tail 100
docker logs n8n --tail 100

# 3. Nginx-Status
systemctl status nginx
nginx -t                      # Konfig testen

# 4. Firewall
ufw status

# 5. Port-Belegung
netstat -tlnp | grep -E '(80|443|8080|5678)'
ss -tlnp | grep 443
```

---

### Problem: Server reagiert nicht (Notfall)

**Hetzner Console:**
1. https://console.hetzner.com â†’ Projekt: OSP-Chatbot
2. Server "osp-webui" auswÃ¤hlen
3. **Option A:** Reiter "Konsole" â†’ VNC-Konsole (SSH-Zugriff)
4. **Option B:** Reiter "Power" â†’ "Neu starten" (Hard Reboot)

---

### Problem: Nginx-Fehler

**Symptome:** 502 Bad Gateway, 404 Not Found

**LÃ¶sung:**
```bash
nginx -t                      # Konfig testen
cat /etc/nginx/sites-enabled/osp
systemctl status nginx
systemctl restart nginx
tail -f /var/log/nginx/error.log
```

---

### Problem: Container wird immer wieder beendet

**Symptome:** `docker ps` zeigt "Restarting" oder Exited

**LÃ¶sung:**
```bash
# Logs prÃ¼fen
docker logs open-webui

# Rebuild ohne Cache
cd /opt/open-webui
docker-compose down
docker-compose up -d --force-recreate

# Bei persistenten Problemen: Volumes neu erstellen
docker volume ls
docker volume rm open-webui_data  # ACHTUNG: Datenverlust!
docker-compose up -d
```

---

### Problem: Passwort vergessen (OSPUI)

**LÃ¶sung:**
```bash
# Container betreten
docker exec -it open-webui bash

# SQLite-DB Ã¶ffnen
sqlite3 /app/backend/data/webui.db

# Admin-E-Mail prÃ¼fen
SELECT email FROM auth WHERE role = 'admin';

# Benutzer lÃ¶schen (Neuanmeldung nÃ¶tig)
DELETE FROM auth WHERE email = 'user@example.com';
```

**Alternative:** "Passwort vergessen" auf Login-Seite (wenn E-Mail konfiguriert)

---

## WICHTIGE PFADE & BEFEHLE

### Dateipfade

| Pfad | Inhalt |
|------|--------|
| `/opt/open-webui/` | Docker-Compose & Konfiguration |
| `/opt/open-webui/docker-compose.yml` | Haupt-Konfiguration |
| `/mnt/HC_Volume_104189729/osp/scripts/` | Backup & Wartungs-Skripte |
| `/mnt/HC_Volume_104189729/osp/backups/` | Lokale Backups (7 Tage) |
| `/etc/nginx/sites-enabled/` | Nginx-Konfigurationen |
| `/etc/nginx/sites-enabled/osp` | OSPUI Reverse Proxy |
| `/etc/nginx/sites-enabled/n8n` | n8n Reverse Proxy |
| `/etc/letsencrypt/` | SSL-Zertifikate |
| `/etc/letsencrypt/live/osp.schneider-kabelsatzbau.de/` | Aktive Zertifikate |
| `/var/log/nginx/` | Nginx Access & Error Logs |
| `/var/log/osp-backup.log` | Backup-Logs |

---

### Docker-Befehle

| Befehl | Zweck |
|--------|-------|
| `docker ps` | Container-Status |
| `docker-compose ps` | Compose-Stack Status |
| `docker logs open-webui` | OSPUI Logs |
| `docker logs chromadb` | ChromaDB Logs |
| `docker-compose restart` | Alle Container neustarten |
| `docker-compose down` | Stack stoppen |
| `docker-compose up -d` | Stack starten (detached) |
| `docker stats` | Ressourcen-Nutzung live |
| `docker system prune -a` | Cleanup (alte Images) |
| `docker exec -it open-webui bash` | Container betreten |

---

### System-Befehle

| Befehl | Zweck |
|--------|-------|
| `htop` | CPU/RAM Monitor |
| `df -h` | Speicherplatz |
| `ufw status` | Firewall-Status |
| `systemctl status nginx` | Nginx-Status |
| `nginx -t` | Nginx-Konfig testen |
| `certbot certificates` | SSL-Zertifikat-Status |
| `journalctl -u docker` | Docker-System-Logs |

---

### Support-Kontakte

| Bereich | Kontakt | Info |
|---------|---------|------|
| **DNS (Subdomains)** | Kevin Lieser, Attentio GmbH | 02662 948007-0, k.lieser@attentio.de |
| **Hetzner Support** | Hetzner Online GmbH | https://console.hetzner.com â†’ Support |
| **OSP-Projekt** | Andreas LÃ¶hr (AL) | a.loehr@schneider-kabelsatzbau.de |

---

## QUERVERWEISE

**Bidirektional (â†”):**
- â†” `BN_CORE_Identitaet.md` - User-Rollen, OSP-Level
- â†” `IT_DOKU_IT-Dokumentation.md` - Server-Infrastruktur
- â†” `IT_RAG_Richtlinie.md` - ChromaDB-Import-Standards

**Ausgehend (â†’):**
- â†’ `KOM_KGS_System-Gedaechtnis.md` - Projekt-Meilensteine
- â†’ `OSP_TAG_System.md` - TAG-System, OSP-Level

**Eingehend (â†):**
- â† `HR_CORE_Personalstamm.md` - Mitarbeiter-E-Mails
- â† `QM_CORE_Qualitaetspolitik.md` - KI-Nutzung im QM

---

## Ã„NDERUNGSHISTORIE

### [1.4] - 2025-12-23 - ARCHITEKTUR-UPDATE & RAM-KORREKTUR
**Quelle:** Server-Erhebung 2025-12-23, docker-compose.yml

**Architektur-Änderungen:**
- ❌ Ollama ENTFERNT (lokale LLMs nicht mehr genutzt)
- ✅ LiteLLM (anthropic-proxy) für Claude API Integration
- ✅ Portainer für Docker-Management hinzugefügt
- ✅ DocCompare für Dokumentenvergleich hinzugefügt

**Version-Updates:**
- ✅ Docker: 27.3.1 → 28.2.2
- ✅ Open WebUI: 0.6.41 → 0.6.43
- ✅ ChromaDB: 0.5.15 → 1.3.6 (Major Update!)
- ✅ Embedding-Modell: all-MiniLM-L6-v2 → multilingual-e5-large

**RAM-Korrektur:**
- ❌ Fehlerhafte Angabe an 4 Stellen: 32GB RAM
- ✅ Korrigiert auf: 16GB RAM (verifiziert via `free -h`)

**Verantwortlich:** AL (QM & KI-Manager)

---

### [1.3] - 2025-12-15 - PIPELINE-MODULE & HARDWARE-UPGRADE
**Quelle:** OSP-RAG-Skill v1.2, Hetzner Console

**Server-Hardware:**
- âœ… Upgrade CX33 â†’ CX43 (8 vCPU, 16GB RAM)
- âœ… Open WebUI v0.6.40 â†’ v0.6.41

**Pipeline-Architektur (NEU):**
- âœ… Neuer Abschnitt "PIPELINE-ARCHITEKTUR" hinzugefÃ¼gt
- âœ… 4 Pre-Processing-Module dokumentiert:
  - Query-Normalizer (Tippfehler-Korrektur)
  - MA-Preprocessing (KÃ¼rzel-Expansion)
  - Keyword-Filter (Direktes Laden)
  - Tag-Router (ChromaDB WHERE-Filter)
- âœ… 6 neue Valves dokumentiert
- âœ… Container-Pfade fÃ¼r Module dokumentiert

**Metriken:**
- âœ… Statistiken aktualisiert (58 Dokumente, 250ms Latenz)
- âœ… Retrieval-Metriken hinzugefÃ¼gt (95% Overall, 100% KERN)

**Verantwortlich:** AL (QM & KI-Manager)

---

### [1.2] - 2025-11-29 - HETZNER-DOKU INTEGRATION
**Quelle:** Hetzner_Server_OSP_Dokumentation.md v1.0

**ErgÃ¤nzungen:**
- âœ… Server-Details aktualisiert (korrekte IP: 46.224.102.XXX, Kosten: â‚¬6/Monat)
- âœ… SSH-Zugang aktualisiert (SSH-Config, Hetzner Console Link)
- âœ… DNS-Verwaltung hinzugefÃ¼gt (Attentio GmbH, Kevin Lieser-Kontakt)
- âœ… Domains & URLs dokumentiert (osp.schneider-kabelsatzbau.de, n8n.schneider-kabelsatzbau.de)
- âœ… Hetzner Backup integriert (7 Slots, automatisch, â‚¬1/Monat)
- âœ… SSL-Details erweitert (GÃ¼ltig bis 26.02.2026, Auto-Renewal, Befehle)
- âœ… Firewall erweitert (UFW-Status, detaillierte Befehle, Ports-Tabelle)
- âœ… Update-Prozedur erweitert (Ubuntu System-Updates, Docker-Updates, Speicherplatz)
- âœ… Troubleshooting massiv erweitert (9 Szenarien: Dienst nicht erreichbar, Server reagiert nicht, Nginx-Fehler, Container wird beendet, Passwort vergessen, etc.)
- âœ… Wichtige Pfade & Befehle hinzugefÃ¼gt (Dateipfade, Docker-Befehle, System-Befehle)
- âœ… Support-Kontakte dokumentiert (Attentio DNS, Hetzner Support, AL)

**Sicherheit:**
- âŒ PasswÃ¶rter NICHT Ã¼bernommen (Security!)
- âŒ API-Keys NICHT Ã¼bernommen
- âœ… IP-Adresse teilweise maskiert (XXX)

**Verantwortlich:** AL (basierend auf Hetzner_Server_OSP_Dokumentation.md v1.0)

---

### [1.1] - 2025-11-29 - RAG-OPTIMIERUNG
**Token-Effizienz:**
- Stage 1: ~16.500 Tokens
- Stage 2: ~13.200 Tokens
- **Einsparung: -3.300 Tokens (-20%)** âœ…

**Optimierungen:**
- âœ… Header kompaktiert (9 Zeilen â†’ 2 Zeilen, ~400 Tokens)
- âœ… Tabellen optimiert (AbkÃ¼rzungen, kompakte Spalten, ~800 Tokens)
- âœ… Code-BlÃ¶cke gekÃ¼rzt (Kommentare entfernt, YAML inline, ~600 Tokens)
- âœ… Redundanzen reduziert ("Docker-Compose" â†’ "DC", ~500 Tokens)
- âœ… FÃ¼llwÃ¶rter entfernt (~200 Tokens)
- âœ… Diagramm kompaktiert (~300 Tokens)
- âœ… Datum-Format: DD.MM.YY statt DD.MM.YYYY (~100 Tokens)
- âœ… AbkÃ¼rzungen: MA, GF, OS, DB, SW, HW (~200 Tokens)

**Chunk-Strategie:**
- Anzahl: 16 Chunks
- Durchschnitt: ~825 Tokens/Chunk
- Min: 700 Tokens (CH14 - n8n)
- Max: 1.100 Tokens (CH03 - Docker-Container)
- Ãœberlappung: 175 Tokens
- Grenzen: Markdown-Header (##)

**Metadata:**
- Primary Keywords: 85 (Server, OSPUI, ChromaDB, Docker, Ollama, n8n, Hetzner, SSL, Backup, Monitoring, RAG, etc.)
- Secondary Keywords: 120 (CX33, Ubuntu, Nginx, mistral, llama2, gpt-4, Let's Encrypt, Veeam, Terra Cloud, Netdata, etc.)
- User-Level: CH01-CH08 = L3, CH09-CH16 = L2 (Troubleshooting)

**Querverweise:**
- Versionen entfernt (8 Links aktualisiert)
- Format: `TAG_SUB_Bezeichnung.md` (ohne Version)

**YAML-Header:**
- Stage 2 Felder ergÃ¤nzt
- RAG-Version: 1.0
- Basis: IT_OSP_KI-Chatbot_v1.0.md

**QS-Checkliste:** 8/8 âœ…
- âœ… YAML-Header vollstÃ¤ndig
- âœ… Token-Effizienz: -20% (Ziel: min. -10%)
- âœ… Chunk-Strategie definiert (16 Chunks, Ã˜ 825 Tokens)
- âœ… Keywords: 85 Primary, 120 Secondary
- âœ… Querverweise dokumentiert (ohne Versionen)
- âœ… DSGVO-Check (keine Namen, nur KÃ¼rzel)
- âœ… Test-Queries vorbereitet (10 Queries fÃ¼r L2-L3)
- âœ… Keine kritischen Fragen offen

**Verantwortlich:** AL (Andreas LÃ¶hr - IT & KI-Manager)

---

### [1.0] - 2025-11-29 - ERSTVERSION
**Erstversion - PRODUKTIV:**
- âœ… Komplette Projekt-Dokumentation
- âœ… Hetzner Server-Infrastruktur (CX33)
- âœ… Docker-Container-Architektur (OSPUI, ChromaDB, Ollama, n8n)
- âœ… OSPUI Konfiguration (6 User, OSP-Level-Mapping)
- âœ… ChromaDB Vektordatenbank (OSP_COMPLETE Collection)
- âœ… Ollama LLM-Runtime (mistral:7b, llama2:13b)
- âœ… Netzwerk & Sicherheit (SSL/TLS, Firewall)
- âœ… Backup & Wartung (tÃ¤glich, wÃ¶chentlich, monatlich)
- âœ… Monitoring & Performance (Netdata, Benchmarks)
- âœ… Troubleshooting-Guide

**Basis:** Screenshots OSPUI, Hetzner Console, Docker-Config, Open-WebUI-Doku.md

**Verantwortlich:** AL (Andreas LÃ¶hr - IT & KI-Manager)

---

## RAG-METADATA

**RAG-Version:** 1.0  
**Primary Keywords:** Server, OSPUI, ChromaDB, Docker, Ollama, n8n, Hetzner, SSL, TLS, Backup, Monitoring, RAG, LLM, Vektordatenbank, Nginx, Ubuntu, Embedding, mistral, llama2, gpt-4, Container, Firewall, SSH, DSGVO, Datenschutz, Cloud, Automation, Workflow, Let's Encrypt, Certbot, UFW, Netdata, Wartung, Update, Log, Troubleshooting, OOM, Disk, Performance, Query, Collection, Metadata, Token, Chunk, User-Level, OSP-Level, L1, L2, L3, L4, Pilot, Go-Live, Timeline, CX33, Falkenstein, Deutschland, IPv4, IPv6, NVMe, SSD, RAM, CPU, vCPU, AMD, EPYC, DDR4, Storage, Volume, Image, Port, Protokoll, HTTP, HTTPS, TCP, Reverse Proxy, Proxy, API, Auth, Key, Passwort, Root, Admin, User, Rolle, Berechtigung, Account, E-Mail, AL, CS, SV, SK, TS, MD

**Secondary Keywords:** 116.203.XXX.XXX, 2a01:4f8, 24.04, 27.3.1, 0.6.41, 0.5.15, 1.26, v2.29.7, ce12230, 6.8.0-49-generic, 4vCPU, 16GB, 160GB, 20TB, â‚¬4.99, /mnt/HC_Volume_104189729/osp, /var/lib/docker, docker-compose.yml, open-webui_data, chromadb_data, ollama_data, n8n_data, osp-network, osp-chromadb, osp-ollama, osp-webui, osp-n8n, :3000, :8000, :11434, :5678, :443, :80, :22, all-MiniLM-L6-v2, text-embedding-3-small, duckdb, parquet, cosine, 384, mistral:7b, llama2:13b, codellama:7b, 4GB, 7.3GB, 3.8GB, 40 tokens/s, 25 tokens/s, 60 tokens/s, 1.2s, 3.8s, 120/s, 99.8%, Terra Cloud, AES-256, 90 Tage, 7 Tage, 4 Wochen, 02:00, 03:00, 04:00, 08:00, 00:00, 19999, certbot, python3-certbot-nginx, htop, nano, curl, wget, git, vim, netdata, ufw, logrotate, backup-daily.sh, update-monthly.sh, osp-backup.log, access.log, error.log, fullchain.pem, privkey.pem, id_ed25519_osp, osp-server, osp.schneider-kabelsatzbau.de, andreas.loehr@, christoph.schneider@, sebastian.vierschilling@, stefan.kandorfer@, tobias.schmidt@, marcel.duetzer@

**User-Level-Zuordnung:**
- **CH01 (Projektzweck):** L1-Ã–ffentlich
- **CH02 (ProjektÃ¼bersicht):** L3-FÃ¼hrung
- **CH03 (Hetzner Server):** L3-FÃ¼hrung
- **CH04 (Docker-Container):** L3-FÃ¼hrung
- **CH05 (OSPUI Konfiguration):** L3-FÃ¼hrung
- **CH06 (ChromaDB):** L3-FÃ¼hrung
- **CH07 (Ollama LLM):** L2-Abteilung
- **CH08 (n8n Automation):** L2-Abteilung
- **CH09 (Netzwerk & Sicherheit):** L3-FÃ¼hrung
- **CH10 (Backup & Wartung):** L2-Abteilung
- **CH11 (Monitoring):** L2-Abteilung
- **CH12-CH16 (Troubleshooting):** L2-Abteilung

**Chunk-Strategie:** Markdown-Header (##)  
**Chunk-Anzahl:** 16  
**Chunk-GrÃ¶ÃŸe:** 700-1100 Tokens  
**Chunk-Ãœberlappung:** 175 Tokens

---

**Status:** âœ… PRODUKTIV (RAG) - Bereit fÃ¼r ChromaDB-Import
**URL:** https://osp.schneider-kabelsatzbau.de
**Server:** Hetzner CX43 (8 vCPU, 16GB RAM, Falkenstein, DE)
**Kosten:** ~â‚¬14/Monat  
**Pilot-Ende:** 19.12.2025  
**NÃ¤chste Review:** 19.12.2025

---

*Diese Dokumentation beschreibt die komplette technische Infrastruktur des OSP KI-Chatbot-Projekts. RAG-optimiert fÃ¼r ChromaDB-Import. Alle Ã„nderungen mÃ¼ssen hier dokumentiert werden.*

[OSP]
