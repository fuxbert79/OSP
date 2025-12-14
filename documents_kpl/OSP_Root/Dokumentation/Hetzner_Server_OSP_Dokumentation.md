# Hetzner Server - OSP Chatbot Dokumentation

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

---

**Version:** 1.0  
**Erstellt:** 28.11.2025  
**Ersteller:** AL  
**Status:** ✅ Produktiv

---

## 🖥️ SERVER-ÜBERSICHT

| Eigenschaft | Wert |
|-------------|------|
| **Anbieter** | Hetzner Cloud |
| **Server-Typ** | CX33 |
| **Server-Name** | osp-webui |
| **IPv4** | 46.224.102.30 |
| **IPv6** | 2a01:4f8:c013:b41c:: |
| **Betriebssystem** | Ubuntu (LTS) |
| **Standort** | Deutschland |
| **Monatliche Kosten** | €6 |

---

## 🌐 DOMAINS & URLs

| Dienst | URL | Zweck |
|--------|-----|-------|
| **Open WebUI** | https://osp.schneider-kabelsatzbau.de | KI-Chatbot Oberfläche |
| **n8n** | https://n8n.schneider-kabelsatzbau.de | Workflow-Automatisierung |

---

## 🔐 ZUGANGSDATEN

### SSH-Zugang (Server-Konsole)

| Eigenschaft | Wert |
|-------------|------|
| **Host** | 46.224.102.30 |
| **Port** | 22 |
| **Benutzer** | root |
| **Passwort** | `buepFudtnUde` |
| **SSH-Befehl** | `ssh root@46.224.102.30` |

---

### Hetzner Cloud Console (Server-Verwaltung)

| Eigenschaft | Wert |
|-------------|------|
| **URL** | https://console.hetzner.com |
| **Projekt** | OSP-Chatbot |
| **E-Mail** | `a.loehr@schneider-kabelsatzbau.de` |
| **Passwort** | `fux_KI_bert#8642` |
| **2FA aktiv** | Nein |

---

### Open WebUI (KI-Chatbot)

| Eigenschaft | Wert |
|-------------|------|
| **URL** | https://osp.schneider-kabelsatzbau.de |
| **Admin-E-Mail** | `osp@schneider-kabelsatzbau.de` |
| **Admin-Passwort** | `Start2025!` |

---

### n8n (Workflow-Automatisierung)

| Eigenschaft | Wert |
|-------------|------|
| **URL** | https://n8n.schneider-kabelsatzbau.de |
| **Admin-E-Mail** | `a.loehr@schneider-kabelsatzbau.de` |
| **Admin-Passwort** | `fux_KI_bert#8642` |

---

### API-Keys (für KI-Modelle)

| Anbieter | API-Key | Status |
|----------|---------|--------|
| **OpenAI** | `sk-_______________________________` | ☐ Aktiv |
| **Anthropic (Claude)** | `sk-ant-___________________________` | ☐ Aktiv |

---

### Let's Encrypt (SSL-Zertifikate)

| Eigenschaft | Wert |
|-------------|------|
| **Registrierte E-Mail** | a.loehr@schneider-kabelsatzbau.de |
| **Zertifikat-Domains** | osp.schneider-kabelsatzbau.de, n8n.schneider-kabelsatzbau.de |
| **Gültig bis** | 26.02.2026 |

---

### DNS-Verwaltung (Attentio GmbH)

| Eigenschaft | Wert |
|-------------|------|
| **Ansprechpartner** | Kevin Lieser |
| **E-Mail** | k.lieser@attentio.de |
| **Telefon** | 02662 948007-0 |
| **Zuständig für** | DNS-Einträge der Domain schneider-kabelsatzbau.de |

**Hinweis:** Für neue Subdomains muss Attentio kontaktiert werden!

---

## 🐳 DOCKER-CONTAINER

| Container | Port (intern) | Funktion |
|-----------|---------------|----------|
| **open-webui** | 8080 → 443 | KI-Chat-Interface |
| **chromadb** | 8000 | Vektordatenbank (RAG) |
| **n8n** | 5678 → 443 | Automatisierung |

### Wichtige Docker-Befehle

```bash
# Status aller Container
docker ps

# Container-Logs anzeigen
docker logs open-webui
docker logs chromadb
docker logs n8n

# Container neustarten
docker restart open-webui

# Alle Container neustarten
docker-compose restart

# Container stoppen/starten
docker-compose down
docker-compose up -d
```

### Docker-Compose Pfad

```
/opt/open-webui/docker-compose.yml
```

### Docker-Compose Konfiguration bearbeiten

```bash
# Konfiguration öffnen
nano /opt/open-webui/docker-compose.yml

# Nach Änderungen: Container neu starten
cd /opt/open-webui
docker-compose down
docker-compose up -d
```

---

## 🔑 UMGEBUNGSVARIABLEN (docker-compose.yml)

Die wichtigsten Einstellungen in der Docker-Compose-Datei:

| Variable | Beschreibung | Aktueller Wert |
|----------|--------------|----------------|
| `WEBUI_URL` | Öffentliche URL | https://osp.schneider-kabelsatzbau.de |
| `WEBUI_NAME` | Anzeigename | `OSP Schneider Kabelsatzbau` |
| `ENABLE_SIGNUP` | Registrierung erlaubt | false |
| `DEFAULT_USER_ROLE` | Rolle neuer Benutzer |  user  |
| `DEFAULT_LOCALE` | Standardsprache | de |
| `OPENAI_API_KEY` | OpenAI API-Key | (in WebUI hinterlegt) |

### Umgebungsvariablen ändern

1. Datei bearbeiten: `nano /opt/open-webui/docker-compose.yml`
2. Variable ändern unter `environment:`
3. Speichern: `Strg+O`, dann `Enter`, dann `Strg+X`
4. Neu starten: `docker-compose down && docker-compose up -d`

---

## 🔒 SSL-ZERTIFIKATE

| Eigenschaft | Wert |
|-------------|------|
| **Anbieter** | Let's Encrypt |
| **Gültig bis** | 26.02.2026 |
| **Auto-Renewal** | ✅ Aktiv (Certbot) |
| **Zertifikat-Pfad** | /etc/letsencrypt/live/osp.schneider-kabelsatzbau.de/ |

### Zertifikat manuell erneuern

```bash
certbot renew
```

### Renewal testen

```bash
certbot renew --dry-run
```

---

## 🛡️ FIREWALL (UFW)

**Status:** ✅ Aktiv

| Port | Protokoll | Dienst |
|------|-----------|--------|
| 22 | TCP | SSH |
| 80 | TCP | HTTP (Redirect) |
| 443 | TCP | HTTPS |

### Firewall-Befehle

```bash
# Status anzeigen
ufw status

# Regel hinzufügen
ufw allow [PORT]/tcp

# Regel entfernen
ufw delete allow [PORT]/tcp
```

---

## 💾 BACKUPS

| Eigenschaft | Wert |
|-------------|------|
| **Anbieter** | Hetzner (integriert) |
| **Slots** | 7 |
| **Automatisch** | ✅ Ja |
| **Kosten** | 20% des Server-Tarifs (~€1/Monat) |

### Backup-Verwaltung

- **Hetzner Console** → Server → Backups
- Manuelles Backup: "Manuelles Backup starten"
- Wiederherstellung: Backup auswählen → "Wiederherstellen"

---

## 📁 WICHTIGE PFADE

| Pfad | Inhalt |
|------|--------|
| `/opt/open-webui/` | Docker-Compose & Konfiguration |
| `/etc/nginx/sites-enabled/` | Nginx-Konfigurationen |
| `/etc/letsencrypt/` | SSL-Zertifikate |
| `/var/log/nginx/` | Nginx-Logs |

---

## 🔧 NGINX-KONFIGURATION

### Konfigurationsdateien

```
/etc/nginx/sites-enabled/osp    → Open WebUI
/etc/nginx/sites-enabled/n8n    → n8n
```

### Nginx-Befehle

```bash
# Konfiguration testen
nginx -t

# Nginx neuladen
systemctl reload nginx

# Nginx neustarten
systemctl restart nginx

# Status prüfen
systemctl status nginx
```

---

## 📊 SYSTEM-MONITORING

### Ressourcen prüfen

```bash
# CPU & RAM
htop

# Speicherplatz
df -h

# Docker-Ressourcen
docker stats
```

---

## 🔄 SYSTEM-WARTUNG

### Ubuntu System-Updates

```bash
# Paketlisten aktualisieren
apt update

# Pakete upgraden
apt upgrade -y

# Nicht mehr benötigte Pakete entfernen
apt autoremove -y
```

### Docker-Container aktualisieren

```bash
cd /opt/open-webui

# Neueste Images herunterladen
docker-compose pull

# Container mit neuen Images starten
docker-compose up -d

# Alte Images entfernen
docker image prune -a
```

### Speicherplatz freigeben

```bash
# Docker-Cleanup (ungenutzte Container, Images, Volumes)
docker system prune -a

# Log-Dateien prüfen
du -sh /var/log/*

# Alte Logs löschen
journalctl --vacuum-time=7d
```

---

## 📝 KONFIGURATIONSDATEIEN

### Nginx - Open WebUI

**Pfad:** `/etc/nginx/sites-enabled/osp`

```bash
# Bearbeiten
nano /etc/nginx/sites-enabled/osp

# Nach Änderung testen und neu laden
nginx -t && systemctl reload nginx
```

### Nginx - n8n

**Pfad:** `/etc/nginx/sites-enabled/n8n`

```bash
# Bearbeiten
nano /etc/nginx/sites-enabled/n8n

# Nach Änderung testen und neu laden
nginx -t && systemctl reload nginx
```

### Docker-Compose

**Pfad:** `/opt/open-webui/docker-compose.yml`

```bash
# Bearbeiten
nano /opt/open-webui/docker-compose.yml

# Nach Änderung Container neu starten
cd /opt/open-webui
docker-compose down && docker-compose up -d
```

---

## 🚨 TROUBLESHOOTING

### Dienst nicht erreichbar

```bash
# 1. Container-Status prüfen
docker ps

# 2. Container-Logs anzeigen
docker logs open-webui --tail 100
docker logs chromadb --tail 100
docker logs n8n --tail 100

# 3. Nginx-Status prüfen
systemctl status nginx

# 4. Firewall prüfen
ufw status

# 5. Port-Belegung prüfen
netstat -tlnp | grep -E '(80|443|8080|5678)'
```

### Container startet nicht

```bash
# Detaillierte Logs
docker logs open-webui

# Container manuell starten (für Debug)
cd /opt/open-webui
docker-compose up  # Ohne -d für Live-Output

# Container komplett neu erstellen
docker-compose down
docker-compose up -d --force-recreate
```

### SSL-Fehler

```bash
# Zertifikat-Status prüfen
certbot certificates

# Renewal testen
certbot renew --dry-run

# Zertifikat manuell erneuern
certbot renew

# Nginx neu laden
systemctl reload nginx
```

### Speicherplatz voll

```bash
# Speicher prüfen
df -h

# Größte Verzeichnisse finden
du -sh /* | sort -h

# Docker-Cleanup
docker system prune -a

# Logs bereinigen
journalctl --vacuum-time=3d
```

### Server reagiert nicht (Notfall)

1. **Hetzner Console öffnen:** https://console.hetzner.com
2. **Server auswählen:** osp-webui
3. **Konsole öffnen:** Reiter "Konsole" → VNC-Konsole
4. **Oder Neustart:** Reiter "Power" → "Neu starten"

### Passwort vergessen (Open WebUI)

```bash
# In Container einloggen
docker exec -it open-webui bash

# SQLite-Datenbank öffnen
sqlite3 /app/backend/data/webui.db

# Admin-E-Mail anzeigen
SELECT email FROM auth WHERE role = 'admin';

# Passwort kann nur über "Passwort vergessen" in WebUI zurückgesetzt werden
# Oder: Benutzer löschen und neu anlegen
```

---

## 📞 SUPPORT-KONTAKTE

| Bereich | Kontakt | Telefon/E-Mail |
|---------|---------|----------------|
| **DNS (Subdomains)** | Kevin Lieser, Attentio GmbH | 02662 948007-0, k.lieser@attentio.de |
| **Hetzner Support** | Hetzner Online GmbH | https://console.hetzner.com → Support |
| **OSP-Projekt intern** | Andreas Löhr (AL) | a.loehr@schneider-kabelsatzbau.de |

---

## 👥 BENUTZER-VERWALTUNG (Open WebUI)

### Über Web-Interface

1. Einloggen als Admin: https://osp.schneider-kabelsatzbau.de
2. Unten links: Avatar-Icon → "Admin Panel"
3. "Users" → Benutzer verwalten

### Benutzer-Rollen

| Rolle | Rechte |
|-------|--------|
| **pending** | Kann sich einloggen, aber nicht chatten (wartet auf Freigabe) |
| **user** | Normaler Benutzer, kann chatten |
| **admin** | Vollzugriff, kann Benutzer und Einstellungen verwalten |

### Neuen Benutzer anlegen

1. Admin Panel → Users → "+" Symbol
2. Name, E-Mail, Passwort eingeben
3. Rolle wählen (empfohlen: "pending" für manuelle Freigabe)

---

## ➕ NEUE SUBDOMAIN HINZUFÜGEN

Falls ein weiterer Dienst benötigt wird:

### 1. DNS-Eintrag bei Attentio anfragen

E-Mail an Kevin Lieser mit:
```
Subdomain: [name].schneider-kabelsatzbau.de
A-Record:    46.224.102.30
AAAA-Record: 2a01:4f8:c013:b41c::
```

### 2. Nginx-Konfiguration erstellen

```bash
# Neue Konfiguration erstellen
nano /etc/nginx/sites-available/[name]

# Aktivieren
ln -s /etc/nginx/sites-available/[name] /etc/nginx/sites-enabled/

# Testen und laden
nginx -t && systemctl reload nginx
```

### 3. SSL-Zertifikat hinzufügen

```bash
certbot --nginx -d [name].schneider-kabelsatzbau.de
```

---

## 📋 ÄNDERUNGSHISTORIE

| Datum | Version | Änderung | Verantwortlich |
|-------|---------|----------|----------------|
| 28.11.2025 | 1.0 | Initiale Dokumentation | AL |

---

*Dokumentation erstellt im Rahmen des OSP-Projekts (Organisation-System-Prompt)*

(C: 100%) [OSP]
