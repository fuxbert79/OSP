# Open WebUI Pipeline Integration Guide - OSP RAG System

**Version:** Open WebUI 0.6.40+ | **Framework:** Pipelines (Separate Container)  
**Deployment Target:** Hetzner Ubuntu 24 (Docker)  
**Last Updated:** December 2025

---

## Table of Contents

1. [Quick Start (5 Min Setup)](#1-quick-start-5-min-setup)
2. [Architecture & Deployment Model](#2-architecture--deployment-model)
3. [Pipeline Development Basics](#3-pipeline-development-basics)
4. [Deployment Guide (Step-by-Step)](#4-deployment-guide-step-by-step)
5. [Troubleshooting Guide](#5-troubleshooting-guide)
6. [Environment Configuration](#6-environment-configuration)
7. [Integration Patterns](#7-integration-patterns)
8. [Testing & Debugging](#8-testing--debugging)
9. [Performance Optimization](#9-performance-optimization)
10. [Security & DSGVO Compliance](#10-security--dsgvo-compliance)
11. [Code Examples (Ready-to-Use)](#11-code-examples-ready-to-use)
12. [Best Practices Checklist](#12-best-practices-checklist)

---

## 1. Quick Start (5 Min Setup)

### Minimal Working Setup (docker-compose)

```yaml
# docker-compose.yml
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
    depends_on:
      - pipelines

  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    container_name: pipelines
    ports:
      - "9099:9099"
    volumes:
      - pipelines:/app/pipelines
    environment:
      - PIPELINES_API_KEY=0p3n-w3bu!
    restart: unless-stopped
    add_hosts:
      - "host.docker.internal:host-gateway"

volumes:
  open-webui: {}
  pipelines: {}
```

### Deploy

```bash
# 1. Start both containers
docker-compose up -d

# 2. Verify running
docker-compose ps

# 3. Copy OSP Pipeline
docker cp /root/osp_rag.py pipelines:/app/pipelines/

# 4. Restart Pipelines to load new pipeline
docker restart pipelines

# 5. Connect in Open WebUI
# Admin Panel → Settings → Connections → Add Connection
# API URL: http://pipelines:9099
# API Key: 0p3n-w3bu!

# 6. Verify Logs
docker logs pipelines -f | grep "OSP\|Pipeline"
```

**Expected Output After Setup:**
```
pipelines    | 🚀 Loaded pipelines: OSP Multi-Layer RAG
open-webui   | Successfully connected to Pipelines
```

---

## 2. Architecture & Deployment Model

### ⚠️ CRITICAL: Two Deployment Models

Open WebUI hat sich entwickelt. Es gibt **ZWEI unterschiedliche Ansätze**:

| Aspekt | **Alte Methode** | **Neue Methode (Empfohlen)** |
|--------|-----------------|---------------------------|
| **Pfad** | `/app/backend/data/plugins/` | Separate `pipelines` Container |
| **Port** | None (embedded) | 9099 |
| **Architecture** | Monolithic | Microservices |
| **Skalierbarkeit** | Gering | Sehr gut |
| **Maintenance** | Schwierig | Einfach |
| **Docker Restart** | Ganzer Container | Nur Pipelines Container |
| **Status** | ⚠️ Deprecated | ✅ Standard seit v0.6.0 |

### Moderne Architektur (Empfohlen)

```
┌─────────────────────────────────────────┐
│       Open WebUI Container              │
│  - Frontend (Port 3000)                 │
│  - Backend LLM Management               │
│                                         │
│  Admin Panel:                           │
│  → Settings → Connections              │
│  → Add: http://pipelines:9099           │
└────────────────┬────────────────────────┘
                 │ HTTP/REST
                 │ (OpenAI API Compatible)
                 ▼
┌─────────────────────────────────────────┐
│    Pipelines Container (Port 9099)      │
│  - OSP Multi-Layer RAG Pipeline         │
│  - LlamaIndex + ChromaDB                │
│  - Custom Business Logic                │
│  - Independent Scaling & Restarts       │
│                                         │
│  Files: /app/pipelines/osp_rag.py       │
│         /app/pipelines/osp_router.py    │
└─────────────────────────────────────────┘
```

### Warum diese Architektur?

✅ **Isolation:** Pipelines-Fehler crashen nicht den ganzen WebUI  
✅ **Skalierbarkeit:** Mehrere Pipelines Container möglich  
✅ **Unabhängige Updates:** Pipelines ohne WebUI neustarten  
✅ **Performance:** Rechenintensive RAG-Operationen offloaded  
✅ **Debugging:** Separate Logs pro Container  

---

## 3. Pipeline Development Basics

### 3.1 Pipeline Class Structure (Vollständige Referenz)

```python
from typing import List, Union, Generator, Iterator, Optional
import asyncio
import logging

# Optional: Für Logging
logger = logging.getLogger(__name__)

class Pipeline:
    """
    Basis-Klasse für alle Pipelines in Open WebUI Pipelines Framework.
    
    Die Klasse MUSS diese exakte Struktur implementieren.
    """
    
    def __init__(self):
        """
        Initialize method - wird beim Container-Start aufgerufen.
        
        ⚠️ WICHTIG: KEINE schweren Operationen hier!
        Nutze on_startup() für Resource-Loading.
        
        Gültig hier:
        - Variablen-Initialisierung (None)
        - Konfiguration laden
        - Valve-Definition (Konfigurationsparameter)
        """
        self.name = "OSP Multi-Layer RAG"
        self.id = "osp_rag"  # Eindeutige ID
        
        # Valves = Konfigurationsparameter für WebUI
        # Können später in Admin Panel geändert werden
        self.valves = {
            "ANTHROPIC_API_KEY": "",
            "ENABLE_LOGGING": True,
            "MAX_CONTEXT_LENGTH": 2000,
            "USE_STREAMING": True,
        }
        
        # Lazy-loaded Resources (wird in on_startup gesetzt)
        self.router = None
        self.llm_chain = None
        self.embeddings = None
    
    async def on_startup(self):
        """
        Asynchron lifecycle hook - wird EINMAL beim Container-Start aufgerufen.
        
        HIER gehören hin:
        - Model/Service Initialization
        - API Connections
        - Database Connections
        - External Library Loading (LlamaIndex, ChromaDB, etc.)
        
        Exceptions hier werden im Log sichtbar gemacht.
        """
        try:
            logger.info("🚀 OSP RAG Pipeline Starting...")
            
            # Import hier - nicht in __init__!
            # So wird es erst geladen wenn nötig
            from osp_production_system import osp_router
            from anthropic import Anthropic
            
            # Initialize Router
            self.router = osp_router
            await self.router.initialize()
            
            # Initialize LLM Client
            self.llm_chain = Anthropic(api_key=self.valves["ANTHROPIC_API_KEY"])
            
            logger.info("✅ OSP RAG Pipeline Ready")
            
        except Exception as e:
            logger.error(f"❌ Pipeline Startup Error: {str(e)}")
            # Pipeline lädt trotzdem, aber mit None-Resources
            # on_error-Handling in pipe() method
    
    async def on_shutdown(self):
        """
        Lifecycle hook - wird beim Container-Shutdown aufgerufen.
        
        Cleanup:
        - Datenbankverbindungen schließen
        - Resources freigeben
        - Temporäre Dateien löschen
        """
        try:
            if hasattr(self, 'router') and self.router:
                await self.router.cleanup()
            logger.info("🛑 OSP RAG Pipeline Shutdown")
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")
    
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict,
    ) -> Union[str, Generator, Iterator]:
        """
        MAIN PROCESSING METHOD - wird für jeden User-Input aufgerufen.
        
        Parameters:
        -----------
        user_message : str
            Die aktuelle User-Eingabe
            z.B. "Welche Fehler wurden diese Woche gemeldet?"
        
        model_id : str
            Das ausgewählte Modell-ID in WebUI
            z.B. "osp_rag" (muss im Namen passen)
        
        messages : List[dict]
            Komplette Chat-History mit Schema:
            [
                {"role": "user", "content": "Erste Frage"},
                {"role": "assistant", "content": "Antwort"},
                {"role": "user", "content": "Zweite Frage"}
            ]
        
        body : dict
            Zusätzliche Parameter (OpenAI-Compatible):
            {
                "temperature": 0.7,
                "max_tokens": 2000,
                "top_p": 0.9,
                ...
            }
        
        Return:
        -------
        Union[str, Generator, Iterator]
            - str: Einfache Antwort
            - Generator: Streaming Response (chunk by chunk)
            - Iterator: Alternative zu Generator
        
        Examples:
        ---------
        # Einfache Antwort
        return "Gefundene 5 Fehler in dieser Woche"
        
        # Streaming Response
        def streaming():
            for chunk in self.router.stream(user_message):
                yield chunk
        return streaming()
        """
        
        # 1. Error Handling für uninitialisierte Resources
        if not self.router:
            return "❌ OSP Router nicht verfügbar. Kontaktiere Admin."
        
        # 2. Logging für Debugging
        logger.info(f"📨 User Message: {user_message[:100]}...")
        
        try:
            # 3. Hauptlogik: Route & Query
            result = self.router.route_and_query(
                user_message,
                verbose=self.valves["ENABLE_LOGGING"],
                max_context_length=self.valves["MAX_CONTEXT_LENGTH"],
            )
            
            # 4. Streaming oder Direct Response
            if self.valves["USE_STREAMING"]:
                return self._stream_response(result)
            else:
                return result["answer"]
        
        except Exception as e:
            logger.error(f"❌ Pipeline Error: {str(e)}")
            return f"⚠️ Fehler: {str(e)}"
    
    def _stream_response(self, result: dict) -> Generator:
        """
        Hilfsmethode für Streaming-Responses.
        Sendet Antwort in Chunks an WebUI.
        """
        answer = result.get("answer", "")
        for chunk in answer.split(" "):
            yield f"{chunk} "


# Wichtig: Am Ende der Datei muss eine Pipeline-Instanz erstellt werden
# Diese wird vom Framework automatisch geladen
pipeline = Pipeline()
```

### 3.2 Eingabe-Parameter Detailliert

```python
# user_message - Die aktuelle Eingabe
user_message = "Zeige mir alle kritischen Fehler vom letzten Monat"

# model_id - Muss zu den registrierten Modellen passen
model_id = "osp_rag"  # MUSS dem Pipeline-Namen entsprechen

# messages - Komplette Konversationshistorie (für Multi-Turn)
messages = [
    {
        "role": "user",
        "content": "Was sind die Trends in unserer Fehlerrate?"
    },
    {
        "role": "assistant",
        "content": "Die Fehlerrate ist um 5% gestiegen. Hauptprobleme sind..."
    },
    {
        "role": "user",
        "content": "Welche Fehler wurden diese Woche gemeldet?"  # <- Aktueller User-Input
    }
]

# body - OpenAI-Compatible Parameter
body = {
    "model": "osp_rag",
    "messages": messages,
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.9,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stream": False,  # True für Streaming
}
```

### 3.3 Return-Werte & Response-Typen

```python
# ✅ OPTION 1: Simple String Response
def pipe(self, user_message: str, **kwargs) -> str:
    answer = self.router.route_and_query(user_message)
    return answer["answer"]  # Direkter String


# ✅ OPTION 2: Streaming Response (Empfohlen für lange Antworten)
def pipe(self, user_message: str, **kwargs) -> Generator:
    result = self.router.route_and_query(user_message)
    
    def streaming():
        for chunk in result["answer"].split(" "):
            yield f"{chunk} "
    
    return streaming()


# ✅ OPTION 3: Generator mit Yield
def pipe(self, user_message: str, **kwargs) -> Generator:
    yield "📊 Analysiere Daten...\n"
    
    for i, chunk in enumerate(self.router.stream_chunks(user_message)):
        yield chunk
        
    yield "\n✅ Analyse abgeschlossen"


# ⚠️ FALSCH: Dict oder andere Typen
def pipe(self, user_message: str, **kwargs) -> dict:
    return {"answer": "Text"}  # ❌ FALSCH - nur String/Generator erlaubt
```

### 3.4 Async vs Sync

```python
# ✅ on_startup & on_shutdown sind ASYNC
async def on_startup(self):
    # Async Code hier OK
    await self.router.initialize()
    await self.llm_chain.setup()


# ⚠️ pipe() ist SYNCHRON (wird nicht mit await aufgerufen)
def pipe(self, user_message: str, **kwargs) -> str:
    # Hier KEIN await!
    # Wenn async nötig: nutze asyncio.run()
    
    # Option 1: Synchroner Code
    result = self.router.route_and_query(user_message)
    
    # Option 2: Async Code erzwingen (Fallback)
    # async_result = asyncio.run(self.async_router.query(user_message))
    
    return result["answer"]
```

---

## 4. Deployment Guide (Step-by-Step)

### 4.1 Voraussetzungen

```bash
# Check 1: Docker & Docker Compose installiert
docker --version          # Version >= 20.10
docker-compose --version  # Version >= 1.29

# Check 2: Ports verfügbar
netstat -an | grep -E ':3000|:9099'  # Sollte leer sein

# Check 3: Hetzner Server Zugriff
ssh root@46.224.102.30 "docker ps"  # Sollte Container-Liste zeigen
```

### 4.2 Verzeichnisstruktur Setup

```bash
# Auf Hetzner Server
mkdir -p /mnt/HC_Volume_104189729/osp/{docker,pipelines,docs}
cd /mnt/HC_Volume_104189729/osp

# Verzeichnisstruktur
/mnt/HC_Volume_104189729/osp/
├── docker/
│   ├── docker-compose.yml
│   └── .env
├── pipelines/
│   ├── osp_rag.py
│   ├── osp_router.py
│   └── osp_production_system.py
└── docs/
    ├── troubleshooting.md
    └── deployment-log.md
```

### 4.3 Docker-Compose Setup

```bash
# 1. docker-compose.yml erstellen
cat > /mnt/HC_Volume_104189729/osp/docker/docker-compose.yml << 'EOF'
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
      - ./pipelines-config:/app/backend/data/pipelines  # Optional
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
      - ENABLE_RAG_WEB_SEARCH=false
      - ENABLE_USER_AUTH=true
      - OPEN_WEBUI_LOG_DATA=false  # DSGVO!
    restart: unless-stopped
    depends_on:
      - pipelines
    networks:
      - osp-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    mem_limit: 4g
    cpus: 2

  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    container_name: pipelines
    ports:
      - "9099:9099"
    volumes:
      - pipelines:/app/pipelines
    environment:
      - PIPELINES_API_KEY=${PIPELINES_API_KEY:-0p3n-w3bu!}
      - PIPELINES_DIR=/app/pipelines
      - LOG_LEVEL=INFO
    restart: unless-stopped
    add_hosts:
      - "host.docker.internal:host-gateway"
    networks:
      - osp-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9099/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    mem_limit: 2g
    cpus: 1

  # Optional: ChromaDB als separaten Service
  chromadb:
    image: ghcr.io/chroma-core/chroma:latest
    container_name: chromadb
    ports:
      - "8000:8000"
    volumes:
      - chromadb:/chroma/data
    environment:
      - IS_PERSISTENT=TRUE
    restart: unless-stopped
    networks:
      - osp-network

volumes:
  open-webui: {}
  pipelines: {}
  chromadb: {}

networks:
  osp-network:
    driver: bridge
EOF

# 2. .env Datei erstellen
cat > /mnt/HC_Volume_104189729/osp/docker/.env << 'EOF'
# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# OpenAI (optional)
OPENAI_API_KEY=sk-proj-...

# Security
WEBUI_SECRET_KEY=$(openssl rand -hex 32)
PIPELINES_API_KEY=0p3n-w3bu!
EOF

# 3. Umgebungsvariablen sichern
chmod 600 /mnt/HC_Volume_104189729/osp/docker/.env
```

### 4.4 Pipeline-Dateien Deployment

```bash
# 1. OSP Production System kopieren
scp /root/osp_production_system.py root@46.224.102.30:/mnt/HC_Volume_104189729/osp/pipelines/
scp /root/osp_router.py root@46.224.102.30:/mnt/HC_Volume_104189729/osp/pipelines/

# 2. OSP RAG Pipeline kopieren (NÄCHSTER SCHRITT)
scp /root/osp_rag.py root@46.224.102.30:/mnt/HC_Volume_104189729/osp/pipelines/

# 3. Rechtevergabe
ssh root@46.224.102.30 "chmod 755 /mnt/HC_Volume_104189729/osp/pipelines/*.py"

# 4. Verify
ssh root@46.224.102.30 "ls -lah /mnt/HC_Volume_104189729/osp/pipelines/"
# Output:
# -rw-r--r-- 1 root root  5.2K osp_rag.py
# -rw-r--r-- 1 root root  8.4K osp_router.py
# -rw-r--r-- 1 root root 12.1K osp_production_system.py
```

### 4.5 Container Starten

```bash
cd /mnt/HC_Volume_104189729/osp/docker

# 1. Container hochfahren
docker-compose up -d

# 2. Status prüfen (warten Sie 30-60 Sekunden)
docker-compose ps
# Output:
# NAME            STATUS              PORTS
# open-webui      Up (healthy) ...    0.0.0.0:3000->8080/tcp
# pipelines       Up (healthy) ...    0.0.0.0:9099->9099/tcp
# chromadb        Up ...              0.0.0.0:8000->8000/tcp

# 3. Logs anschauen
docker-compose logs -f --tail=50

# 4. Pipelines Container Logs (am wichtigsten!)
docker logs pipelines -f | head -50
```

### 4.6 Pipeline in Open WebUI Registrieren

```
1. Browser: http://46.224.102.30:3000
2. Admin Panel (Zahnrad-Icon) → Settings
3. Gehe zu: Connections (oder "Pipelines")
4. Klick: "+" oder "Add Connection"
5. Fülle aus:
   - API URL: http://pipelines:9099
   - API Key: 0p3n-w3bu!
6. Klick: "Save" oder "Verify"
7. Sollte ✅ "Connected" anzeigen

8. Gehe zu: Admin Panel → Settings → Pipelines
9. Suche: "OSP Multi-Layer RAG"
10. Sollte mit grünem Punkt sichtbar sein
```

### 4.7 Erste Test-Anfrage

```
1. Neue Chat starten (Home)
2. Modell auswählen: "OSP Multi-Layer RAG"
3. Eingebenimestamp: "Test: Zeige mir Status"
4. Enter
5. Sollte Antwort bekommen (oder aussagekräftiger Fehler)
```

### 4.8 Daten in ChromaDB Laden

```bash
# Wenn Sie bereits Daten haben:
python3 /mnt/HC_Volume_104189729/osp/load_chromadb.py

# Logs verfolgen:
docker logs pipelines -f | grep -E "ChromaDB|Collection|Added"
```

---

## 5. Troubleshooting Guide

### FEHLER 1: Pipeline nicht in UI sichtbar

**Symptom:**
```
- Open WebUI zeigt Pipeline nicht
- Settings → Pipelines ist leer oder "OSP RAG" fehlt
```

**Checkliste (In dieser Reihenfolge):**

```bash
# 1. Ist Pipelines Container running?
docker ps | grep pipelines
# Falls nicht:
docker-compose up -d pipelines

# 2. Sind Pipeline-Dateien im Container?
docker exec pipelines ls -la /app/pipelines/
# Output sollte zeigen: osp_rag.py

# 3. Python Syntax prüfen
docker exec pipelines python3 -m py_compile /app/pipelines/osp_rag.py
# Falls Fehler: Syntax-Error in osp_rag.py

# 4. Pipeline geladen?
docker logs pipelines | grep -i "pipeline\|osp\|loaded"
# Sollte zeigen: "🚀 Loaded pipelines: OSP Multi-Layer RAG"

# 5. Ist Connection in WebUI korrekt?
curl -X GET http://pipelines:9099/pipelines
# Response sollte JSON mit Pipeline-Liste sein

# 6. Ports richtig gemappt?
netstat -an | grep 9099
# Sollte zeigen: LISTEN 0.0.0.0:9099
```

**Lösungen (nach Checkliste):**

| Schritt | Problem | Lösung |
|---------|---------|--------|
| 1 | Container nicht laufend | `docker-compose up -d pipelines` |
| 2 | Datei nicht vorhanden | `docker cp osp_rag.py pipelines:/app/pipelines/` |
| 3 | Syntax Error | Datei lokal mit `python3 -m py_compile` prüfen |
| 4 | Pipeline-Load Error | `docker logs pipelines -f` → Fehlerquellen finden |
| 5 | API nicht erreichbar | Firewall/Netzwerk prüfen, `docker network ls` |
| 6 | Port nicht gemappt | docker-compose.yml: `ports: - "9099:9099"` prüfen |

---

### FEHLER 2: Import Errors (ModuleNotFoundError)

**Symptom:**
```
ModuleNotFoundError: No module named 'llama_index'
ModuleNotFoundError: No module named 'chromadb'
ModuleNotFoundError: No module named 'osp_production_system'
```

**Root Causes & Lösungen:**

```bash
# URSACHE 1: Dependency nicht im Container installiert
# LÖSUNG:
docker exec pipelines pip install llama-index chromadb anthropic

# URSACHE 2: osp_production_system.py nicht im Container
# LÖSUNG:
docker cp /root/osp_production_system.py pipelines:/app/pipelines/
docker exec pipelines python3 -c "import sys; sys.path.insert(0, '/app/pipelines'); from osp_production_system import osp_router"

# URSACHE 3: Python Path falsch
# In osp_rag.py Anfang:
import sys
sys.path.insert(0, '/app/pipelines')  # Add this
from osp_production_system import osp_router

# URSACHE 4: Docker Image hat alte Dependencies
# LÖSUNG: Image updaten
docker-compose down
docker pull ghcr.io/open-webui/pipelines:main
docker-compose up -d pipelines
```

**Permanente Lösung (Dependencies in Dockerfile):**

```dockerfile
# Dockerfile.pipelines
FROM ghcr.io/open-webui/pipelines:main

RUN pip install \
    llama-index==0.9.x \
    chromadb==0.4.x \
    anthropic==0.25.x \
    pydantic==2.x

COPY ./pipelines /app/pipelines
```

Dann bauen und deployen:
```bash
docker build -f Dockerfile.pipelines -t osp-pipelines:custom .
docker tag osp-pipelines:custom ghcr.io/myregistry/osp-pipelines:custom
docker push ghcr.io/myregistry/osp-pipelines:custom

# docker-compose.yml anpassen:
# image: ghcr.io/myregistry/osp-pipelines:custom
```

---

### FEHLER 3: Runtime Error - "AttributeError: 'Pipeline' object has no attribute 'router'"

**Symptom:**
```
AttributeError: 'Pipeline' object has no attribute 'router'
Traceback:
  File "/app/pipelines/osp_rag.py", line 45, in pipe()
    result = self.router.route_and_query(user_message)
AttributeError: 'NoneType' object has no attribute 'route_and_query'
```

**Analyse:**

```python
# ❌ PROBLEM: router ist None
class Pipeline:
    def __init__(self):
        self.router = None  # ← Bleibt None wenn on_startup fehlschlägt
    
    def pipe(self, ...):
        result = self.router.route_and_query(...)  # ← CRASH hier


# ✅ LÖSUNG: Error Handling
class Pipeline:
    def pipe(self, user_message: str, **kwargs):
        # Check vor Verwendung!
        if not self.router:
            return "❌ OSP Router nicht initialized. Check logs."
        
        try:
            result = self.router.route_and_query(user_message)
            return result["answer"]
        except AttributeError as e:
            logger.error(f"Router Error: {str(e)}")
            return f"⚠️ Router nicht verfügbar: {str(e)}"
```

**Debugging Steps:**

```bash
# 1. on_startup Logs prüfen
docker logs pipelines | grep -A 20 "on_startup\|Error\|Traceback"

# 2. osp_production_system import testen
docker exec pipelines python3 << 'EOF'
try:
    from osp_production_system import osp_router
    print("✅ Import successful")
    print(f"Router object: {osp_router}")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
EOF

# 3. API Key prüfen
docker exec pipelines python3 -c "import os; print(f'API Key set: {bool(os.getenv(\"ANTHROPIC_API_KEY\"))}')"

# 4. Container Umgebung prüfen
docker exec pipelines env | grep -E "ANTHROPIC|PATH|PYTHONPATH"
```

**Häufige Root Causes:**

| Ursache | Prüfung | Fix |
|---------|---------|-----|
| on_startup nie aufgerufen | `docker logs pipelines \| grep "on_startup"` | Container neu starten: `docker restart pipelines` |
| on_startup hatte Exception | `docker logs pipelines \| grep "Error\|Exception"` | Exception Handling verbessern oder Dependencies prüfen |
| ANTHROPIC_API_KEY fehlt | `docker exec pipelines env \| grep ANTHROPIC` | .env Datei mit API Key füllen |
| osp_production_system fehlt | `docker exec pipelines ls /app/pipelines/osp_*.py` | `docker cp` Datei kopieren |

---

### FEHLER 4: "ChromaDB Connection Refused" / "Collection already exists"

**Symptom:**
```
ConnectionError: Failed to connect to ChromaDB at localhost:8000
RuntimeError: Collection 'osp_kern' already exists
```

**LÖSUNG A: Collection-Error beheben**

```python
# ❌ FALSCH
collection = chroma_client.create_collection("osp_kern")

# ✅ RICHTIG
collection = chroma_client.get_or_create_collection("osp_kern")
# oder
try:
    collection = chroma_client.get_collection("osp_kern")
except:
    collection = chroma_client.create_collection("osp_kern")
```

**LÖSUNG B: ChromaDB Connection**

```bash
# 1. ChromaDB läuft?
docker ps | grep chromadb
# Falls nicht, starten:
docker-compose up -d chromadb

# 2. ChromaDB erreichbar?
curl http://localhost:8000/api/v2/heartbeat

# 3. In Pipeline Code: hostname anpassen
# Wenn ChromaDB in Docker Compose:
chroma_client = chromadb.HttpClient(
    host="chromadb",  # Docker hostname, nicht localhost!
    port=8000
)

# 4. Falls Persistent Client gewünscht:
# (Für lokale Testing ohne separaten Service)
chroma_client = chromadb.PersistentClient(
    path="/app/pipelines/data/chromadb"
)
```

---

### FEHLER 5: "Pipeline sehr langsam (>30s Response Time)"

**Symptom:**
```
- Anfrage dauert >30 Sekunden
- Zeitüberschreitung in Open WebUI
- Sichtbar langsam, aber keine Fehler im Log
```

**Diagnose:**

```bash
# 1. Container Ressourcen prüfen
docker stats pipelines --no-stream
# Prüfen: CPU %, MEM USAGE, ob 100% erreicht

# 2. Pipelines Logs mit Timestamps
docker logs pipelines --timestamps -f | grep -E "pipe|query|time"

# 3. Memory Limit prüfen
docker inspect pipelines | grep -A 5 "Memory"

# 4. Python Profiling (in Pipeline hinzufügen)
import time
def pipe(self, user_message: str, **kwargs):
    start = time.time()
    result = self.router.route_and_query(user_message)
    elapsed = time.time() - start
    print(f"⏱️ Query took {elapsed:.2f}s")
    return result["answer"]
```

**Performance Optimierungen:**

```bash
# 1. Memory Limit erhöhen (docker-compose.yml)
pipelines:
    mem_limit: 4g  # von 2g auf 4g erhöhen
    cpus: 2        # von 1 auf 2 CPUs

# 2. Connection Pooling in Pipeline
class Pipeline:
    def __init__(self):
        self.router_cache = {}  # Cache für häufige Queries
    
    def pipe(self, user_message: str, **kwargs):
        # Cache prüfen
        if user_message in self.router_cache:
            return self.router_cache[user_message]
        
        # Query ausführen
        result = self.router.route_and_query(user_message)
        
        # In Cache speichern (max 100 Einträge)
        if len(self.router_cache) < 100:
            self.router_cache[user_message] = result["answer"]
        
        return result["answer"]

# 3. Batch Processing für Multiple Queries
# Wenn mehrere Sequential Queries - diese kombinieren

# 4. ChromaDB Query Limit
chroma_collection.query(
    query_embeddings=embeddings,
    n_results=5  # Nur Top 5, nicht 100!
)
```

---

### FEHLER 6: "Logs nicht sichtbar" / "Print Statements funktionieren nicht"

**Symptom:**
```
- docker logs pipelines ist leer
- Print statements erscheinen nicht
- Keine Fehlermeldungen sichtbar
```

**Lösungen:**

```bash
# 1. Buffer flushing erzwingen
python3 -u script.py  # -u = unbuffered
# In Docker Compose:
environment:
  - PYTHONUNBUFFERED=1

# 2. Zu stderr schreiben (wird immer gezeigt)
import sys
print("Message", file=sys.stderr)

# 3. Logging verwenden (empfohlen)
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Message")  # Immer sichtbar

# 4. Logs mit Tail ansehen
docker logs pipelines -f --tail=100

# 5. Container Logs explizit aktivieren
# docker-compose.yml:
pipelines:
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=DEBUG

# 6. Logs zu Datei schreiben (Fallback)
with open("/app/pipelines/debug.log", "a") as f:
    f.write(f"Debug: {message}\n")
```

---

## 6. Environment Configuration

### 6.1 Environment Variables

```yaml
# .env file
# ============================================

# ANTHROPIC API
ANTHROPIC_API_KEY=sk-ant-...

# OPENAI (optional - falls Sie auch OpenAI nutzen)
OPENAI_API_KEY=sk-proj-...

# Security
WEBUI_SECRET_KEY=<random-hex-32-chars>
PIPELINES_API_KEY=0p3n-w3bu!

# OpenWebUI Config
ENABLE_RAG_WEB_SEARCH=false
ENABLE_USER_AUTH=true
OPEN_WEBUI_LOG_DATA=false  # DSGVO wichtig!

# ChromaDB
CHROMADB_HOST=chromadb
CHROMADB_PORT=8000

# OSP Specific
OSP_PRODUCTION_MODE=true
OSP_MAX_CONTEXT_LENGTH=2000
OSP_ENABLE_LOGGING=true
```

### 6.2 docker-compose.yml Detailliert

```yaml
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    
    # Ports
    ports:
      - "3000:8080"  # Web UI
    
    # Volumes
    volumes:
      - open-webui:/app/backend/data  # Persistente Daten
      - ./logs:/app/backend/logs       # Optional: Logs
    
    # Environment
    env_file:
      - .env  # Load variables from .env
    environment:
      # Override spezifische Values
      - ENABLE_RAG_WEB_SEARCH=false
      - OPEN_WEBUI_LOG_DATA=false
    
    # Dependencies
    depends_on:
      - pipelines
    
    # Network
    networks:
      - osp-network
    
    # Health Check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # Resources
    mem_limit: 4g
    cpus: 2
    
    # Restart Policy
    restart: unless-stopped
  
  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    container_name: pipelines
    
    # Ports
    ports:
      - "9099:9099"  # Pipelines API
    
    # Volumes
    volumes:
      - pipelines:/app/pipelines
      - ./pipelines-config:/config  # Optional
    
    # Environment
    environment:
      - PIPELINES_API_KEY=0p3n-w3bu!
      - PIPELINES_DIR=/app/pipelines
      - LOG_LEVEL=INFO
      - PYTHONUNBUFFERED=1  # Logs sofort anzeigen
    
    # Docker Host Access
    add_hosts:
      - "host.docker.internal:host-gateway"
    
    # Network
    networks:
      - osp-network
    
    # Health Check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9099/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    
    # Resources
    mem_limit: 2g
    cpus: 1
    
    # Restart Policy
    restart: unless-stopped

volumes:
  open-webui:
  pipelines:

networks:
  osp-network:
    driver: bridge
```

### 6.3 Firewall & Netzwerk (für Hetzner)

```bash
# Check Firewall (UFW - Ubuntu)
sudo ufw status

# Ports öffnen
sudo ufw allow 3000/tcp   # Open WebUI
sudo ufw allow 9099/tcp   # Pipelines API
sudo ufw enable

# Docker Network prüfen
docker network ls
docker network inspect osp-network

# Container im Network erreichbar?
docker exec open-webui curl -I http://pipelines:9099/health
# Sollte 200 OK zurückgeben
```

---

## 7. Integration Patterns

### 7.1 Lazy Loading (Best Practice)

```python
# ❌ FALSCH - schwere Operationen in __init__
class Pipeline:
    def __init__(self):
        from llama_index import VectorStoreIndex
        from chromadb import PersistentClient
        
        # Diese Operationen dauern lange!
        self.index = VectorStoreIndex.load()  # ← Bottleneck
        self.chroma = PersistentClient()      # ← Slow
        # Wenn __init__ fehlschlägt → ganze Pipeline crasht


# ✅ RICHTIG - lazy loading in on_startup
class Pipeline:
    def __init__(self):
        # Nur Variablen initialisieren
        self.index = None
        self.chroma = None
    
    async def on_startup(self):
        # Schwere Operationen HIER
        from llama_index import VectorStoreIndex
        from chromadb import PersistentClient
        
        self.index = VectorStoreIndex.load()
        self.chroma = PersistentClient()
        # Fehler hier werden logged, Pipeline lädt aber trotzdem
```

### 7.2 Streaming Responses

```python
def pipe(self, user_message: str, **kwargs) -> Generator:
    """
    Streaming ermöglicht:
    - Real-time Feedback an User
    - Bessere UX für lange Antworten
    - Partial Results zeigen
    """
    
    # Variante 1: Simple Wort-für-Wort Streaming
    result = self.router.route_and_query(user_message)
    answer = result["answer"]
    
    for word in answer.split(" "):
        yield word + " "
    
    # Variante 2: Chunk-basiertes Streaming
    for chunk in self.router.stream_response(user_message):
        yield chunk  # chunk = "Teil der Antwort"
    
    # Variante 3: Mit Status-Updates
    def streaming():
        yield "🔍 Searching database...\n"
        results = self.router.search(user_message)
        
        yield f"📊 Found {len(results)} results\n"
        
        yield "💭 Generating response...\n"
        answer = self.router.generate(results)
        
        yield answer
    
    return streaming()
```

### 7.3 External API Calls

```python
class Pipeline:
    def __init__(self):
        self.anthropic_client = None
    
    async def on_startup(self):
        from anthropic import Anthropic
        self.anthropic_client = Anthropic(
            api_key=self.valves["ANTHROPIC_API_KEY"]
        )
    
    def pipe(self, user_message: str, **kwargs):
        try:
            # Call externe API
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
            )
            
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            return f"❌ API Error: {str(e)}"
```

### 7.4 Database Connections (ChromaDB)

```python
class Pipeline:
    def __init__(self):
        self.chroma_client = None
        self.collection = None
    
    async def on_startup(self):
        import chromadb
        
        # Connection Option 1: HTTP (Remote)
        self.chroma_client = chromadb.HttpClient(
            host="chromadb",  # Docker service name
            port=8000
        )
        
        # Connection Option 2: Persistent (Local)
        # self.chroma_client = chromadb.PersistentClient(
        #     path="/app/pipelines/data"
        # )
        
        # Get or Create Collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="osp_documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def pipe(self, user_message: str, **kwargs):
        # Query Collection
        results = self.collection.query(
            query_texts=[user_message],
            n_results=5
        )
        
        # Process Results
        documents = results["documents"][0]
        distances = results["distances"][0]
        
        context = "\n".join(documents)
        
        # Use in RAG
        answer = self.router.generate(
            question=user_message,
            context=context
        )
        
        return answer
```

### 7.5 Error Handling Strategy

```python
class Pipeline:
    def pipe(self, user_message: str, **kwargs):
        """Comprehensive Error Handling"""
        
        # Level 1: Uninitialized Resources
        if not self.router:
            return "❌ Pipeline not ready. Try again in a moment."
        
        try:
            # Level 2: Main Logic
            result = self.router.route_and_query(user_message)
            
            # Level 3: Response Validation
            if not result or "answer" not in result:
                return "⚠️ Invalid response from router"
            
            answer = result["answer"]
            if not answer:
                return "⚠️ Empty response from router"
            
            return answer
        
        except ConnectionError as e:
            # External Service Error
            logger.error(f"Connection Error: {str(e)}")
            return "❌ External service unavailable"
        
        except ValueError as e:
            # Input Validation Error
            logger.warning(f"Invalid Input: {str(e)}")
            return f"⚠️ Invalid input: {str(e)}"
        
        except Exception as e:
            # Generic Error Handling
            logger.error(f"Unexpected Error: {str(e)}", exc_info=True)
            return f"❌ System Error: {type(e).__name__}"
```

---

## 8. Testing & Debugging

### 8.1 Local Testing (Vor Deployment)

```bash
# 1. Python Virtual Environment
python3 -m venv /mnt/HC_Volume_104189729/osp/venv
source /mnt/HC_Volume_104189729/osp/venv/bin/activate

# 2. Dependencies installieren
pip install llama-index chromadb anthropic

# 3. Pipeline local testen
cd /mnt/HC_Volume_104189729/osp
python3 << 'EOF'
import sys
sys.path.insert(0, '.')

from osp_rag import pipeline

# Test __init__
print(f"✅ Pipeline name: {pipeline.name}")

# Test pipe
response = pipeline.pipe(
    user_message="Test query",
    model_id="osp_rag",
    messages=[],
    body={}
)
print(f"✅ Response: {response[:100]}...")
EOF

# 4. Syntax-Validierung
python3 -m py_compile /mnt/HC_Volume_104189729/osp/osp_rag.py
echo "✅ Syntax OK"
```

### 8.2 Container Debugging

```bash
# 1. Real-Time Logs (am wichtigsten!)
docker logs pipelines -f --tail=100

# Filtered Logs
docker logs pipelines -f | grep -E "ERROR|Exception|OSP"

# Mit Timestamps
docker logs pipelines --timestamps -f

# 2. Container interaktiv betreten
docker exec -it pipelines /bin/bash

# Dann im Container:
ls -la /app/pipelines/
python3 -m py_compile /app/pipelines/osp_rag.py
python3 -c "from osp_rag import pipeline; print(pipeline.name)"

# 3. Prozess-Details
docker top pipelines
docker inspect pipelines

# 4. Network Test
docker exec pipelines curl http://chromadb:8000/health
docker exec pipelines curl http://open-webui:8080/health

# 5. File System Check
docker exec pipelines find /app/pipelines -name "*.py" -exec wc -l {} \;
```

### 8.3 Debug Logging aktivieren

```python
# In osp_rag.py
import logging
import sys

# Configure Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Console
        logging.FileHandler('/app/pipelines/debug.log')  # File
    ]
)

logger = logging.getLogger(__name__)

class Pipeline:
    def pipe(self, user_message: str, **kwargs):
        logger.debug(f"📨 Incoming message: {user_message}")
        logger.debug(f"📊 Message length: {len(user_message)}")
        logger.debug(f"🔧 Router ready: {bool(self.router)}")
        
        try:
            result = self.router.route_and_query(user_message)
            logger.info(f"✅ Query successful")
            return result["answer"]
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}", exc_info=True)
            raise
```

### 8.4 Unit Tests

```python
# tests/test_pipeline.py
import pytest
from osp_rag import pipeline

class TestPipeline:
    def test_init(self):
        """Test Pipeline Initialization"""
        assert pipeline.name == "OSP Multi-Layer RAG"
        assert pipeline.router is None  # Lazy loaded
    
    def test_pipe_basic(self):
        """Test Basic Pipe Functionality"""
        response = pipeline.pipe(
            user_message="Test",
            model_id="osp_rag",
            messages=[],
            body={}
        )
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_pipe_with_error(self):
        """Test Error Handling"""
        pipeline.router = None  # Simulate uninitialized
        response = pipeline.pipe(
            user_message="Test",
            model_id="osp_rag",
            messages=[],
            body={}
        )
        assert "❌" in response  # Should show error

# Run Tests
# pytest tests/test_pipeline.py -v
```

---

## 9. Performance Optimization

### 9.1 Response Time Optimization

```python
class Pipeline:
    def __init__(self):
        self.cache = {}  # Query cache
        self.max_cache_size = 100
    
    def pipe(self, user_message: str, **kwargs) -> str:
        # 1. Cache Check (schnellest!)
        cache_key = f"{user_message}:{kwargs.get('temperature', 0.7)}"
        if cache_key in self.cache:
            logger.info("🚀 Cache Hit!")
            return self.cache[cache_key]
        
        # 2. Query Processing
        result = self.router.route_and_query(user_message)
        
        # 3. Cache Store
        if len(self.cache) < self.max_cache_size:
            self.cache[cache_key] = result["answer"]
        
        return result["answer"]
```

### 9.2 Memory Management

```python
# docker-compose.yml
pipelines:
    mem_limit: 2g   # Limit
    memswap_limit: 2g  # No swap beyond limit
    
    # Monitor
    # docker stats pipelines
```

### 9.3 Connection Pooling

```python
class Pipeline:
    def __init__(self):
        self.chroma_pool = None
    
    async def on_startup(self):
        # Reuse single connection
        import chromadb
        self.chroma_client = chromadb.HttpClient(
            host="chromadb",
            port=8000,
            # Optional: Connection pooling
        )
```

---

## 10. Security & DSGVO Compliance

### 10.1 DSGVO-Relevante Settings

```yaml
# docker-compose.yml
open-webui:
    environment:
      # KRITISCH: User Data Logging DEAKTIVIEREN
      - OPEN_WEBUI_LOG_DATA=false
      
      # Authentication aktivieren
      - ENABLE_USER_AUTH=true
      
      # RAG Web Search optional
      - ENABLE_RAG_WEB_SEARCH=false
```

### 10.2 API Key Management

```bash
# ❌ FALSCH - Keys in Code
API_KEY = "sk-ant-..."

# ✅ RICHTIG - Environment Variables
import os
api_key = os.getenv("ANTHROPIC_API_KEY")

# ✅ NOCH BESSER - Secrets Manager
# docker-compose.yml:
secrets:
  anthropic_key:
    file: ./secrets/anthropic.key

services:
  pipelines:
    secrets:
      - anthropic_key
    environment:
      - ANTHROPIC_API_KEY_FILE=/run/secrets/anthropic_key
```

### 10.3 Input Validation & Sanitization

```python
class Pipeline:
    def pipe(self, user_message: str, **kwargs):
        # Validate Input
        if not user_message or len(user_message) == 0:
            return "⚠️ Empty message"
        
        if len(user_message) > 5000:  # Max length
            user_message = user_message[:5000]
            logger.warning("Message truncated to 5000 chars")
        
        # Sanitize (no SQL injection, etc.)
        # In LlamaIndex: typically handled automatically
        
        return self.router.route_and_query(user_message)
```

---

## 11. Code Examples (Ready-to-Use)

### 11.1 Minimal Working Pipeline

```python
# /pipelines/minimal_rag.py
"""Minimal RAG Pipeline für Open WebUI"""

from typing import Generator, Union

class Pipeline:
    def __init__(self):
        self.name = "Minimal RAG"
        
    async def on_startup(self):
        print("🚀 Pipeline started")
    
    async def on_shutdown(self):
        print("🛑 Pipeline stopped")
    
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: list,
        body: dict,
    ) -> Union[str, Generator]:
        # Simple echo with formatting
        return f"📝 You asked: {user_message}\n\n✅ Pipeline working!"

pipeline = Pipeline()
```

### 11.2 RAG Pipeline mit LlamaIndex

```python
# /pipelines/llama_rag.py
"""RAG Pipeline mit LlamaIndex Integration"""

import logging
from typing import Generator, Union
import asyncio

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self):
        self.name = "LlamaIndex RAG"
        self.index = None
        self.llm = None
    
    async def on_startup(self):
        try:
            from llama_index.core import VectorStoreIndex, Settings
            from llama_index.embeddings.openai import OpenAIEmbedding
            from anthropic import Anthropic
            
            # Initialize Embeddings
            Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
            
            # Initialize LLM
            self.llm = Anthropic()
            
            # Load Index (if exists)
            try:
                self.index = VectorStoreIndex.load_from_disk("./osp_index")
                logger.info("✅ Index loaded")
            except:
                logger.info("⚠️ No existing index found")
                self.index = None
            
        except Exception as e:
            logger.error(f"❌ Startup error: {e}")
    
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: list,
        body: dict,
    ) -> str:
        if not self.index:
            return "❌ RAG Index not available"
        
        try:
            # Query Index
            query_engine = self.index.as_query_engine()
            response = query_engine.query(user_message)
            
            return str(response)
        
        except Exception as e:
            logger.error(f"❌ Query error: {e}")
            return f"⚠️ Error: {str(e)}"

pipeline = Pipeline()
```

### 11.3 Streaming Response Pipeline

```python
# /pipelines/streaming_rag.py
"""Pipeline mit Streaming Responses"""

import logging
from typing import Generator
import time

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self):
        self.name = "Streaming RAG"
    
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: list,
        body: dict,
    ) -> Generator:
        """
        Returns Generator für Streaming.
        WebUI zeigt jeden yielded Chunk in Echtzeit.
        """
        
        # Phase 1: Analysis
        yield "🔍 Analyzing your question...\n\n"
        time.sleep(0.5)
        
        # Phase 2: Searching
        yield "📚 Searching documents...\n"
        documents = self._search_documents(user_message)
        yield f"Found {len(documents)} relevant documents\n\n"
        time.sleep(0.5)
        
        # Phase 3: Generating
        yield "💭 Generating response...\n\n"
        
        # Stream response word by word
        response = f"Answer to '{user_message}': "
        for word in response.split():
            yield word + " "
            time.sleep(0.1)  # Simulate thinking
        
        yield "\n\n✅ Done!"
    
    def _search_documents(self, query: str) -> list:
        # Dummy implementation
        return ["Doc 1", "Doc 2", "Doc 3"]

pipeline = Pipeline()
```

---

## 12. Best Practices Checklist

### Vor dem Deployment

- [ ] Lokaler Python Test erfolgreich (`python3 osp_rag.py`)
- [ ] Syntax validiert (`python3 -m py_compile osp_rag.py`)
- [ ] Alle Dependencies gelistet (`pip freeze > requirements.txt`)
- [ ] Environment Variables in .env gesetzt
- [ ] docker-compose.yml überprüft
- [ ] API Keys aus Code entfernt (nur Env Vars)
- [ ] Error Handling implementiert
- [ ] Logging hinzugefügt
- [ ] Health Checks definiert

### Beim Deployment

- [ ] `docker-compose up -d` erfolgreich
- [ ] Beide Container laufen (`docker ps`)
- [ ] Logs überprüft (`docker logs pipelines -f`)
- [ ] Pipeline in WebUI sichtbar
- [ ] Test-Anfrage funktioniert
- [ ] Response-Zeit <30 Sekunden

### Im Production-Betrieb

- [ ] Regelmäßige Logs Checks
- [ ] Memory/CPU Monitoring
- [ ] API Key Rotation (monatlich)
- [ ] Dokumentation aktuell halten
- [ ] Backup Strategy für Daten
- [ ] DSGVO Compliance überprüfen

### Code Best Practices

```python
# ✅ DO THIS
class Pipeline:
    def __init__(self):
        self.name = "Clear Name"
        self.router = None  # Lazy load
    
    async def on_startup(self):
        self.router = await self._init_router()  # Heavy operations here
    
    def pipe(self, user_message: str, **kwargs) -> str:
        if not self.router:
            return "Error message"  # Graceful degradation
        
        try:
            result = self.router.query(user_message)
            return result["answer"]
        except Exception as e:
            logger.error(f"Error: {e}")
            return "Error message"

# ❌ DON'T DO THIS
class Pipeline:
    def __init__(self):
        self.router = self._init_router()  # Slow in init
        self.name = "Bad"
    
    def pipe(self, user_message: str, **kwargs):
        result = self.router.query(user_message)  # No error handling
        return result
```

---

## Appendix A: Pipeline Class Reference

### Required Methods

| Method | Required | Async | Called When |
|--------|----------|-------|------------|
| `__init__()` | ✅ Yes | ❌ No | Container start |
| `on_startup()` | ❌ Optional | ✅ Yes | After `__init__`, once |
| `on_shutdown()` | ❌ Optional | ✅ Yes | Container stop |
| `pipe()` | ✅ Yes | ❌ No | Each user message |

### `__init__()` Method

```python
def __init__(self):
    # ALLOWED:
    self.name = "String"
    self.config = {"key": "value"}
    self.cache = {}
    
    # NOT ALLOWED (should be in on_startup):
    # from heavy_library import Model
    # self.model = Model.load()
```

### `pipe()` Method Signature

```python
def pipe(
    self,
    user_message: str,        # User input
    model_id: str,            # Model identifier
    messages: List[dict],     # Chat history
    body: dict,               # Additional parameters (OpenAI-compatible)
) -> Union[str, Generator, Iterator]:  # Response type
```

---

## Appendix B: Common docker-compose Patterns

### Minimal (für Testing)

```yaml
version: '3.8'
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports: ["3000:8080"]
    volumes: [open-webui:/app/backend/data]
    environment:
      ANTHROPIC_API_KEY: sk-ant-...
  
  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    ports: ["9099:9099"]
    volumes: [pipelines:/app/pipelines]
    environment:
      PIPELINES_API_KEY: 0p3n-w3bu!

volumes:
  open-webui:
  pipelines:
```

### Production (empfohlen)

```yaml
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: unless-stopped
    env_file: .env
    environment:
      OPEN_WEBUI_LOG_DATA: "false"
      ENABLE_USER_AUTH: "true"
    ports: ["3000:8080"]
    volumes:
      - open-webui:/app/backend/data
      - ./logs:/app/backend/logs
    networks: [osp-network]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    mem_limit: 4g
    cpus: 2

  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    container_name: pipelines
    restart: unless-stopped
    env_file: .env
    environment:
      PYTHONUNBUFFERED: "1"
      LOG_LEVEL: "INFO"
    ports: ["9099:9099"]
    volumes:
      - pipelines:/app/pipelines
      - ./pipelines-config:/config
    networks: [osp-network]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9099/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    mem_limit: 2g
    cpus: 1

volumes:
  open-webui:
  pipelines:

networks:
  osp-network:
```

---

## Appendix C: Häufige Error Messages & Fixes

### "ModuleNotFoundError: No module named 'X'"

```bash
docker exec pipelines pip install <package>
# dann docker restart pipelines
```

### "Connection refused"

```bash
# Check Ports
netstat -an | grep 909
# Check Network
docker network inspect osp-network
```

### "Timeout after 30s"

```
Erhöhen Sie mem_limit in docker-compose.yml
oder optimieren Sie Query-Performance
```

### "AttributeError: 'Pipeline' object has no attribute 'X'"

```python
# Immer checken ob None ist
if self.router:
    # use
else:
    # error message
```

---

**Kontakt & Support:**

Falls Fragen: Dokumentation updaten oder in  
`/mnt/HC_Volume_104189729/osp/docs/troubleshooting.md` eintragen

