# OSP/RMS/NZA Deployment Report

## Infrastruktur und SharePoint-Intranet Integration

**Dokumenten-Nr.:** OSP-DEP-2026-001
**Version:** 1.0
**Datum:** 02.02.2026
**Ersteller:** Andreas Löhr, QM-Manager / KI-Manager
**Zielgruppe:** IT-Administration, Geschäftsleitung

---

## 1. Executive Summary

Dieses Dokument beschreibt die aktuelle Infrastruktur der Systeme OSP (Organisations-System-Prompt), RMS (Reklamationsmanagementsystem) und NZA (Nach- und Zusatzarbeiten) sowie die geplante Integration in das neue SharePoint-Intranet.

**Aktueller Stand:**
- Alle Systeme produktiv auf dediziertem Hetzner-Server
- Dashboards über https://osp.schneider-kabelsatzbau.de erreichbar
- Daten in Microsoft 365 SharePoint gespeichert

**Ziel:**
- Integration der Dashboards als Subdomain im SharePoint-Intranet
- Einheitliche Benutzererfahrung für alle Mitarbeiter
- Zentrale Verwaltung über Microsoft 365

---

## 2. Systemübersicht

### 2.1 Die drei Systeme

| System | Zweck | Status | URL |
|--------|-------|--------|-----|
| **OSP** | KI-Wissensdatenbank, RAG-System | Produktiv | osp.schneider-kabelsatzbau.de |
| **RMS** | Reklamationsmanagement (extern) | Produktiv | .../rms/ |
| **NZA** | Nacharbeiten-Erfassung (intern) | Produktiv | .../nza/ |

### 2.2 Komponenten-Architektur

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         BENUTZER (Browser)                               │
│                    Microsoft 365 Authentifizierung                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌───────────┐   ┌───────────┐   ┌───────────┐
            │  /rms/    │   │  /nza/    │   │  /rms/2025│
            │ Dashboard │   │ Dashboard │   │  Archiv   │
            └───────────┘   └───────────┘   └───────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      NGINX REVERSE PROXY                                 │
│                 osp.schneider-kabelsatzbau.de                           │
│                    SSL/TLS (Let's Encrypt)                              │
│                                                                          │
│  Routing:                                                                │
│  ├── /rms/          → /var/www/html/rms/                                │
│  ├── /nza/          → /var/www/html/nza/                                │
│  ├── /rms/2025/     → /var/www/html/rms/2025/                           │
│  ├── /api/rms/*     → http://127.0.0.1:5678/webhook/rms-*               │
│  ├── /api/nza/*     → http://127.0.0.1:5678/webhook/nza-*               │
│  └── /api/rms2025/* → http://127.0.0.1:5678/webhook/rms2025/*           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         N8N WORKFLOW ENGINE                              │
│                        http://127.0.0.1:5678                            │
│                                                                          │
│  Workflows:                                                              │
│  ├── RMS: 15 Workflows (Dashboard-API, CRUD, Email, Notify)             │
│  ├── NZA: 12 Workflows (Prozesse, Kosten, Bilder, Notify)               │
│  └── RMS-2025: 1 Workflow (Archiv-Dashboard Standalone)                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    MICROSOFT 365 / SHAREPOINT ONLINE                     │
│                  rainerschneiderkabelsatz.sharepoint.com                │
│                                                                          │
│  Sites:                                                                  │
│  ├── /sites/RMS/           → Reklamationen-2026, RMS-Massnahmen         │
│  ├── /sites/NZA_NEU/       → nza-kpl, nza-massnahmen, nza-bilder, ...   │
│  └── /sites/Intranet/      → Neues SharePoint-Intranet (geplant)        │
│                                                                          │
│  Dokumentenbibliotheken:                                                 │
│  ├── /sites/RMS/Freigegebene Dokumente/2025/    → RMS Archiv 2025       │
│  ├── /sites/RMS/Freigegebene Dokumente/2026/    → RMS aktuell           │
│  └── /sites/NZA_NEU/Freigegebene Dokumente/     → NZA Dokumente         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         OSP WISSENSDATENBANK                             │
│                                                                          │
│  ├── ChromaDB v1.0.0      → Vektor-Datenbank für RAG                    │
│  ├── Open WebUI v0.6.41   → Chat-Interface für KI                       │
│  └── Claude API           → Anthropic LLM Backend                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Aktuelle Infrastruktur

### 3.1 Server-Spezifikation

| Parameter | Wert |
|-----------|------|
| **Anbieter** | Hetzner Cloud |
| **Modell** | CX43 |
| **vCPU** | 8 Kerne |
| **RAM** | 32 GB |
| **Storage** | 240 GB SSD + 100 GB Volume |
| **OS** | Ubuntu 24.04 LTS |
| **IP** | 46.224.102.30 |
| **Standort** | Deutschland (Falkenstein) |

### 3.2 Software-Stack

| Komponente | Version | Port | Beschreibung |
|------------|---------|------|--------------|
| **Nginx** | 1.24 | 80, 443 | Reverse Proxy, SSL-Terminierung |
| **n8n** | 1.x | 5678 | Workflow-Automatisierung |
| **ChromaDB** | 1.0.0 | 8000 | Vektor-Datenbank |
| **Open WebUI** | 0.6.41 | 3000 | KI-Chat-Interface |
| **Docker** | 24.x | - | Container-Runtime |

### 3.3 DNS-Konfiguration

| Domain | Typ | Ziel |
|--------|-----|------|
| osp.schneider-kabelsatzbau.de | A | 46.224.102.30 |
| n8n.schneider-kabelsatzbau.de | A | 46.224.102.30 |

### 3.4 SSL-Zertifikate

| Domain | Aussteller | Gültigkeit |
|--------|------------|------------|
| osp.schneider-kabelsatzbau.de | Let's Encrypt | Auto-Renewal |
| n8n.schneider-kabelsatzbau.de | Let's Encrypt | Auto-Renewal |

---

## 4. Microsoft 365 Integration

### 4.1 Azure App Registration

| Parameter | Wert |
|-----------|------|
| **App-Name** | OSP-n8n-Integration |
| **Client ID** | f99f47af-da3a-493c-aa17-e6b30e3b197c |
| **Tenant ID** | 31d02377-b699-4cef-a113-fc66e586df88 |
| **Redirect URI** | https://n8n.schneider-kabelsatzbau.de/rest/oauth2-credential/callback |

### 4.2 API-Berechtigungen (Graph API)

| Bereich | Berechtigungen |
|---------|----------------|
| **SharePoint** | Sites.ReadWrite.All, Sites.Manage.All |
| **Files** | Files.ReadWrite.All |
| **Mail** | Mail.Read, Mail.ReadWrite, Mail.Send |
| **Calendar** | Calendars.ReadWrite |
| **Teams** | TeamsActivity.Send, ChannelMessage.Read.All |
| **User** | User.Read.All |

### 4.3 Shared Mailboxes

| Postfach | Verwendung |
|----------|------------|
| reklamation@schneider-kabelsatzbau.de | RMS E-Mail-Import |
| nza@schneider-kabelsatzbau.de | NZA E-Mail-Import |

### 4.4 SharePoint-Sites

| Site | URL | Zweck |
|------|-----|-------|
| **RMS** | /sites/RMS/ | Reklamations-Daten und Dokumente |
| **NZA_NEU** | /sites/NZA_NEU/ | NZA-Daten und Dokumente |
| **Intranet** | /sites/Intranet/ | Neues Mitarbeiter-Intranet (geplant) |

---

## 5. SharePoint-Intranet Integration

### 5.1 Ziel-Architektur

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SHAREPOINT INTRANET (Ziel)                            │
│              rainerschneiderkabelsatz.sharepoint.com/sites/Intranet     │
│                                                                          │
│  Navigation:                                                             │
│  ├── Startseite                                                          │
│  ├── Qualitätsmanagement                                                │
│  │   ├── RMS Dashboard (iframe/Embed)                                   │
│  │   ├── NZA Dashboard (iframe/Embed)                                   │
│  │   └── QM-Dokumente                                                   │
│  ├── Fertigung                                                          │
│  ├── Personal                                                           │
│  └── ...                                                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ iframe src="https://osp.../rms/"
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      HETZNER SERVER (Backend)                            │
│                 osp.schneider-kabelsatzbau.de                           │
│                                                                          │
│  Dashboards + API bleiben auf dediziertem Server                        │
│  (n8n-Workflows können nicht in SharePoint laufen)                      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Integrations-Optionen

| Option | Beschreibung | Vorteile | Nachteile |
|--------|--------------|----------|-----------|
| **A: iframe Embed** | Dashboard per iframe in SharePoint-Seite einbetten | Einfach, bestehende Lösung bleibt | CSP-Anpassung nötig |
| **B: SharePoint Hosted** | HTML-Dateien in SharePoint Dokumentenbibliothek | Native Integration | API-Calls problematisch |
| **C: Power Apps** | Dashboard als Power App nachbauen | Volle M365-Integration | Hoher Aufwand |
| **D: Subdomain Link** | Link im Intranet zu externer URL | Sehr einfach | Keine echte Integration |

### 5.3 Empfehlung: Option A (iframe Embed)

**Begründung:**
- Dashboards bleiben funktional wie bisher
- n8n-Backend läuft weiterhin auf dediziertem Server
- Benutzer sehen Dashboard innerhalb des Intranets
- Minimaler Migrationsaufwand

**Voraussetzungen:**
1. CSP-Header auf Hetzner-Server anpassen (X-Frame-Options)
2. SharePoint-Seite mit Embed-Webpart erstellen
3. Authentifizierung: Benutzer sind bereits in M365 angemeldet

### 5.4 Technische Umsetzung (Option A)

#### 5.4.1 Nginx-Anpassung (Server-Seite)

```nginx
# Erlaube Embedding von SharePoint-Domain
add_header X-Frame-Options "ALLOW-FROM https://rainerschneiderkabelsatz.sharepoint.com" always;
add_header Content-Security-Policy "frame-ancestors 'self' https://rainerschneiderkabelsatz.sharepoint.com https://*.sharepoint.com" always;
```

#### 5.4.2 SharePoint-Seite (Intranet-Seite)

1. Neue Seite erstellen: "Qualitätsmanagement"
2. Webpart "Einbetten" hinzufügen
3. URL eingeben: `https://osp.schneider-kabelsatzbau.de/rms/`
4. Größe anpassen (Vollbreite, 800px Höhe)

#### 5.4.3 Alternative: SharePoint Framework (SPFx)

Für tiefere Integration kann ein SPFx-Webpart entwickelt werden:

```typescript
// Beispiel: RMS Dashboard Webpart
export default class RmsDashboardWebPart extends BaseClientSideWebPart<IRmsDashboardProps> {
  public render(): void {
    this.domElement.innerHTML = `
      <iframe
        src="https://osp.schneider-kabelsatzbau.de/rms/"
        width="100%"
        height="800px"
        frameborder="0"
      ></iframe>
    `;
  }
}
```

---

## 6. Deployment-Prozess

### 6.1 Aktuelles Deployment (Hetzner)

```bash
# 1. Dashboard-Dateien aktualisieren
scp -r dashboard/* root@46.224.102.30:/var/www/html/rms/

# 2. n8n-Workflow importieren
# Manuell über n8n UI: Import from File

# 3. Nginx-Konfiguration anpassen
sudo nano /etc/nginx/sites-available/osp
sudo nginx -t && sudo systemctl reload nginx

# 4. Workflow aktivieren
# Manuell in n8n: Toggle "Active"
```

### 6.2 Dateistruktur auf Server

```
/var/www/html/
├── rms/
│   ├── index.html          # RMS Dashboard 2026
│   └── 2025/
│       └── index.html      # RMS Archiv 2025
├── nza/
│   └── index.html          # NZA Dashboard

/mnt/HC_Volume_104189729/osp/
├── rms/
│   ├── dashboard/          # Quelldateien
│   ├── workflows/          # n8n Workflow JSONs
│   ├── docs/               # Dokumentation
│   └── 2025/               # Archiv 2025
├── nza/
│   ├── workflows/          # n8n Workflow JSONs
│   └── docs/               # Dokumentation
└── docs/                   # Übergreifende Docs
```

### 6.3 n8n-Workflows

| System | Anzahl | Wichtige Workflows |
|--------|--------|-------------------|
| **RMS** | 15 | Dashboard-API, Detail-API, Create, Update, Delete, Email-Import, Notify |
| **NZA** | 12 | Prozesse-API, Massnahmen-API, Bilder-API, Kosten-API, Notify |
| **RMS-2025** | 1 | Dashboard-API-Standalone (embedded data) |

### 6.4 Backup-Strategie

| Komponente | Backup-Methode | Frequenz |
|------------|----------------|----------|
| SharePoint-Daten | Microsoft 365 Retention | Automatisch |
| n8n-Workflows | Git Repository | Bei Änderung |
| Dashboard-HTML | Git Repository | Bei Änderung |
| Server-Config | /etc Backup | Wöchentlich |
| ChromaDB | Volume Snapshot | Täglich |

---

## 7. Sicherheit

### 7.1 Netzwerk

| Maßnahme | Status |
|----------|--------|
| HTTPS/TLS 1.3 | ✅ Aktiv |
| Let's Encrypt Zertifikat | ✅ Auto-Renewal |
| Firewall (ufw) | ✅ Konfiguriert |
| Nur Ports 80, 443, 22 offen | ✅ |

### 7.2 Authentifizierung

| System | Methode |
|--------|---------|
| SharePoint-Daten | Microsoft 365 OAuth2 |
| n8n Admin | Lokaler Benutzer + Passwort |
| Dashboard | Keine (öffentlich lesbar) |
| Open WebUI | Lokaler Benutzer |

### 7.3 Empfehlungen für Intranet-Integration

| Maßnahme | Priorität | Status |
|----------|-----------|--------|
| Dashboard hinter M365-Auth | Hoch | Geplant |
| IP-Whitelist für API | Mittel | Offen |
| Audit-Logging | Mittel | Offen |
| Rate-Limiting | Niedrig | Offen |

---

## 8. Monitoring

### 8.1 Aktuelle Überwachung

| Komponente | Monitoring |
|------------|------------|
| Server-Uptime | Hetzner Cloud Console |
| Nginx | Access/Error Logs |
| n8n | Execution History |
| SharePoint | Microsoft 365 Admin Center |

### 8.2 Empfohlene Erweiterungen

| Tool | Zweck | Priorität |
|------|-------|-----------|
| Uptime Kuma | Verfügbarkeits-Monitoring | Hoch |
| Grafana | Dashboard für Metriken | Mittel |
| Loki | Log-Aggregation | Niedrig |

---

## 9. Kosten

### 9.1 Laufende Kosten

| Posten | Monatlich | Jährlich |
|--------|-----------|----------|
| Hetzner CX43 | ~35 EUR | ~420 EUR |
| Hetzner Volume 100GB | ~5 EUR | ~60 EUR |
| Domain (optional) | ~1 EUR | ~12 EUR |
| **Summe Infrastruktur** | **~41 EUR** | **~492 EUR** |
| Microsoft 365 | (bestehend) | (bestehend) |
| Claude API | ~50-100 EUR | ~600-1200 EUR |

### 9.2 Einmalige Kosten (bei SharePoint-Integration)

| Posten | Aufwand | Kosten (geschätzt) |
|--------|---------|-------------------|
| CSP-Konfiguration | 2h | Intern |
| SharePoint-Seiten erstellen | 4h | Intern |
| SPFx-Webpart (optional) | 16h | Extern: ~2000 EUR |
| Dokumentation | 4h | Intern |

---

## 10. Roadmap

### 10.1 Phase 1: Stabilisierung (Q1/2026) ✅

- [x] RMS produktiv
- [x] NZA produktiv
- [x] Archiv-Dashboard 2025
- [x] Dokumentation

### 10.2 Phase 2: Intranet-Integration (Q2/2026)

- [ ] CSP-Header anpassen
- [ ] SharePoint-Intranet Seite "Qualitätsmanagement"
- [ ] RMS Dashboard einbetten
- [ ] NZA Dashboard einbetten
- [ ] Benutzer-Schulung

### 10.3 Phase 3: Erweiterungen (Q3-Q4/2026)

- [ ] M365-Authentifizierung für Dashboards
- [ ] Mobile-Optimierung
- [ ] Power BI Integration für erweiterte Auswertungen
- [ ] Automatischer E-Mail-Import (RMS + NZA)

---

## 11. Ansprechpartner

| Rolle | Name | Kontakt |
|-------|------|---------|
| **Projektverantwortung** | Andreas Löhr | AL |
| **IT-Administration** | [IT-Kontakt] | |
| **Microsoft 365 Admin** | [M365-Admin] | |
| **Geschäftsleitung** | CS, CA | |

---

## 12. Anhänge

- **Anhang A:** Nginx-Konfiguration (vollständig)
- **Anhang B:** n8n Workflow-Liste
- **Anhang C:** SharePoint-Listen Spezifikation
- **Anhang D:** API-Endpunkt Dokumentation

---

## Anhang A: Nginx-Konfiguration

```nginx
server {
    server_name osp.schneider-kabelsatzbau.de;
    client_max_body_size 50M;

    # Open WebUI (Hauptanwendung)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 600s;
    }

    # RMS Dashboard
    location /rms/ {
        alias /var/www/html/rms/;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # NZA Dashboard
    location /nza/ {
        alias /var/www/html/nza/;
        index index.html;
        try_files $uri $uri/ /nza/index.html;
    }

    # RMS 2025 Archiv
    location /rms/2025/ {
        alias /var/www/html/rms/2025/;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # RMS API Endpoints
    location /api/rms/ {
        proxy_pass http://127.0.0.1:5678/webhook/rms-;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        add_header Access-Control-Allow-Origin * always;
    }

    # NZA API Endpoints
    location /api/nza/ {
        proxy_pass http://127.0.0.1:5678/webhook/nza-;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        add_header Access-Control-Allow-Origin * always;
    }

    # SSL (Let's Encrypt)
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/osp.schneider-kabelsatzbau.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/osp.schneider-kabelsatzbau.de/privkey.pem;
}
```

---

**Dokumentenhistorie:**

| Version | Datum | Änderung | Autor |
|---------|-------|----------|-------|
| 1.0 | 02.02.2026 | Erstversion | AL |

---

*Rainer Schneider Kabelsatzbau GmbH & Co. KG - Internes Dokument*
