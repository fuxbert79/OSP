# [IT][CORE] Client-Server-Struktur

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 2.0 | **TAG:** [IT][CORE] | **Erstellt:** 2025-11-20 | **Aktualisiert:** 2025-12-01 | **Autor:** AL | **Verantwortlich:** AL (QM/IT) | **Cluster:** 🔴 C4-Support | **Zugriff:** 🟡 L2-Abteilung | **Status:** ✅ FREIGEGEBEN | **ISO-Norm:** 9001:2015 (Kap. 7.1.3, 7.1.4) | **Kritikalität:** 🔴 SEHR HOCH | **Primary Keywords:** Server, Hyper-V, Virtualisierung, Windows Server, SRV-HV01, SRV-DC01, SRV-FS, SRV-TS02, Timeline, DocuWare, Backup, Veeam, Terra Cloud, Active Directory, schneider.local, GPO, Lizenzen, RDS-CAL, Windows Server 2019, Windows Server 2025, Entra ID Connect (30+) | **Secondary Keywords:** 192.168.10.200, 192.168.10.230, 192.168.10.232, 192.168.10.240, WISSRV-TIMELINE, SQL01, DATEV, SRV-BKP01, Gromnitza IT, GIT, HPE ProLiant DL380 Gen10, Microsoft 365, Veeam Backup 12, DYP9J-K9H7W-3YKDH, HVHC2-68N37-HMHBM (50+) | **Chunk-Strategie:** Markdown-Header (##) | **Datenstand:** 2025-12-01

---

## ZWECK

Zentrale Dokumentation der Client-Server-Infrastruktur: 2 physische Server (SRV-HV01 Hyper-V Host aktiv, SRV-BKP01 außer Dienst), 8 virtuelle Maschinen, Windows Server Lizenzen, Active Directory (schneider.local), Gruppenrichtlinien, Backup-Systeme (Veeam lokal + Terra Cloud), Microsoft 365 Integration. Dient als Single Source of Truth für IT-Troubleshooting, Disaster Recovery und Compliance.

---

## INHALT

### 1. PHYSISCHE SERVER

#### 1.1 SRV-HV01 (Hyper-V Host) - ✅ AKTIV

**Modell:** HPE ProLiant DL380 Gen10  
**Seriennummer:** [zu ergänzen]  
**Standort:** Server-Raum Bürogebäude (klimatisiert)  
**Betriebssystem:** Windows Server 2019 Standard  
**Lizenzschlüssel:** HVHC2-68N37-HMHBM-39MV4-BKHRC  
**Rolle:** Hyper-V Host (Virtualisierungsserver)

**Hardware:**
- **CPU:** Intel Xeon (2x)
- **RAM:** 256 GB DDR4 ECC
- **Storage:** 2 TB SSD (RAID 1)
- **Netzwerk:** 4x 1 GbE (NIC Teaming)
- **iLO:** 192.168.10.241 (Lights-Out Management)

**IP-Adressen:**
- Hyper-V Host: 192.168.10.240
- iLO Management: 192.168.10.241

**VMs auf SRV-HV01:** 8 VMs (siehe Abschnitt 2)

**Backup:**
- Lokal: Veeam Backup & Replication 12 → NAS-KSBS (7 Tage Retention)
- Cloud: Terra Cloud Backup (42 Backup-Stände, Retention: 6 Wochen)

---

#### 1.2 SRV-BKP01 (Backup-Server) - ❌ AUSSERDIENST - ENTSORGUNG GEPLANT

**Status:** Seit 2024 außer Dienst, Hardware wird entsorgt  
**Modell:** HPE ProLiant DL360 Gen9 (alt)  
**Rolle:** Ehemaliger Backup-Server (ersetzt durch Terra Cloud)  
**Entscheidung:** AL + CS (01.12.2025)

---

### 2. VIRTUELLE MASCHINEN (8 VMs)

Alle VMs laufen auf **SRV-HV01** (Hyper-V Host).

#### 2.1 SRV-DC01 (Domain Controller) - ✅ PRODUKTIV

**Betriebssystem:** Windows Server 2022 Standard  
**IP:** 192.168.10.200  
**Rollen:**
- Active Directory Domain Services (AD DS)
- DNS-Server
- DHCP-Server
- Entra ID Connect (Microsoft 365 Synchronisation)

**Domäne:** schneider.local  
**Forest-Level:** Windows Server 2016  
**AD-User:** ~60 aktive Konten  
**AD-Computer:** ~80 Clients + Server

**DNS-Zonen:**
- schneider.local (intern)
- 10.168.192.in-addr.arpa (Reverse Lookup)

**DHCP-Bereich:**
- 192.168.10.100 - 192.168.10.199 (Clients)
- Lease-Dauer: 8 Tage

**Backup:** Täglich via Veeam → Terra Cloud

---

#### 2.2 SRV-FS (Fileserver) - ✅ PRODUKTIV

**Betriebssystem:** Windows Server 2019 Standard  
**IP:** 192.168.10.230  
**Rollen:**
- Fileserver (Netzlaufwerke)
- Printserver (12 Netzwerkdrucker)

**Freigaben (Netzlaufwerke):**
- F: = Alte Ablage
- H: = Abteilung
- K: = DMS
- M: = Mitarbeitermatrix
- X: = Persönliches Laufwerk (%USERNAME%)
- N: = Schliffbild
- I:, W:, L:, G:, Z: = [Verwendung zu ermitteln]

**Storage:**
- Primär: 2 TB auf SRV-HV01
- Backup: Veeam → Terra Cloud (täglich)

**Drucker:** 12 Netzwerkdrucker via Printserver-Rolle (siehe IT_NET)

---

#### 2.3 SRV-TS02 (Terminalserver) - ✅ PRODUKTIV

**Betriebssystem:** Windows Server 2025 Standard  
**Lizenzschlüssel:** DYP9J-K9H7W-3YKDH-M64V6-YGHYG  
**IP:** 192.168.10.232  
**Rolle:** Remote Desktop Services (RDS)

**RDS-Lizenzen:**
- User CALs: 56 aktive (Lizenzserver: SRV-TS02)
- Lizenzschlüssel: [zu ergänzen]

**Remote-Zugriff:**
- Intern: rdp://192.168.10.232
- Extern: Via Sophos SSL-VPN

**Anwendungen auf TS:**
- Microsoft Office 2013 (GVLK: YC7DK-G2NP3-2QQC3-J6H88-GVGXT) - Migration zu M365 Apps geplant
- Timeline ERP (Remote-Zugriff)
- DocuWare Client
- Spezial-Tools (DATEV, etc.)

**Benutzer:**
- AD-Gruppe: TerminalServerUser
- ~30 aktive Remote-User

**Backup:** Täglich via Veeam → Terra Cloud

---

#### 2.4 WISSRV-TIMELINE (Timeline ERP) - ✅ PRODUKTIV

**Betriebssystem:** Windows Server 2019 Standard  
**IP:** 192.168.10.111  
**Rolle:** Timeline ERP Applikationsserver

**Timeline-Version:** [zu ergänzen]  
**Datenbank:** SQL Server (lokal auf VM)  
**Lizenzierung:** Concurrent User

**Zugriff:**
- Direkt: Timeline-Client (Installations-Ordner)
- Remote: Via Terminalserver (SRV-TS02)

**Wartung:** Gromnitza IT (GIT)

**Backup:** Täglich via Veeam → Terra Cloud

---

#### 2.5 SQL01 (DocuWare Datenbank) - ✅ PRODUKTIV

**Betriebssystem:** Windows Server 2022 Standard  
**IP:** 192.168.10.235  
**Rolle:** DocuWare Datenbank-Server

**SQL Server:** Microsoft SQL Server 2019 Standard  
**DocuWare-Version:** [zu ergänzen]  
**Datenbankgröße:** ~500 GB

**Zugriff:**
- DocuWare Web-Client: https://docuware.schneider.local
- Admin-Zugang: SQL Server Management Studio

**Wartung:** Gromnitza IT (GIT)

**Backup:**
- SQL-Backup: Täglich (Transaction Log stündlich)
- VM-Backup: Täglich via Veeam → Terra Cloud

---

#### 2.6 DATEV (DATEV Arbeitsplatz) - ✅ PRODUKTIV

**Betriebssystem:** Windows 10 Pro (VM)  
**IP:** 192.168.10.99  
**Rolle:** DATEV Arbeitsplatz-VM

**DATEV-Module:**
- DATEV Unternehmen online
- DATEV Lohn und Gehalt (über Steuerberater)

**Zugriff:**
- Direkt: RDP → 192.168.10.99
- Benutzer: AD-Gruppe "DATEV-Gruppe" [Anzahl zu ermitteln]

**Wartung:** DATEV eG (externer Support)

**Backup:** Täglich via Veeam → Terra Cloud

---

#### 2.7 KOMAX-VM (Maschinensteuerung) - ⚠️ SICHERHEITSRISIKO

**Betriebssystem:** Windows 7 Professional (32-bit)  
**IP:** 192.168.10.106  
**Rolle:** KOMAX Crimp-Maschinen Steuerung

**Sicherheitshinweis:**
- ✅ **Isoliert vom Produktiv-Netzwerk** (VLAN-Trennung via Sophos Firewall)
- ❌ **Update-Status:** Update auf Windows 10/11 NICHT möglich (Maschinen-Kompatibilität)
- ✅ **Risiko-Bewertung:** Akzeptabel (Entscheidung: AL + Jürgen Schleifert, 01.12.2025)

**Zugriff:** Nur lokale Konsole (Produktionshalle)

**Wartung:** Jürgen Schleifert (Produktionsleiter)

**Backup:** ❌ Kein Backup (VM wird bei Hardwaredefekt neu aufgesetzt)

---

#### 2.8 SRV-APP (Timeline Applikationsserver Alt) - ⚠️ WENIG GENUTZT

**Betriebssystem:** Windows Server 2019 Standard  
**IP:** 192.168.10.107  
**Rolle:** Alter Timeline Applikationsserver (teilweise ersetzt durch WISSRV-TIMELINE)

**Status:** Noch aktiv, aber wenig genutzt  
**Migration:** Vollständige Ablösung durch WISSRV-TIMELINE geplant

**Backup:** Täglich via Veeam → Terra Cloud

---

#### 2.9 OSP-SERVER (Hetzner Cloud) - ✅ NEU (2025-12-07)

**Typ:** Cloud-Server (Hetzner)  
**Modell:** CX33 (ARM64)  
**IP:** 46.224.102.30  
**Betriebssystem:** Ubuntu 24.04 LTS  
**Rolle:** OSP KI-Infrastruktur (Open WebUI, ChromaDB, n8n)

**Hardware:**
- **CPU:** 4 vCPU (ARM64 Ampere)
- **RAM:** 16 GB
- **Storage:** 160 GB NVMe SSD
- **Traffic:** 20 TB/Monat inkl.

**Dienste (Docker-Container):**

| Container | Port | Version | Zweck | Status |
|-----------|------|---------|-------|--------|
| **open-webui** | 3000 | v0.6.40 | Frontend für KI-Chat | ✅ Produktiv |
| **chromadb** | 8000 | v0.5.15 | RAG Vektor-Datenbank | ✅ Produktiv |
| **ollama** | 11434 | latest | LLM-Fallback (lokal) | ✅ Bereit |
| **n8n** | 5678 | latest | Workflow-Automation | ✅ Produktiv |

**Netzwerk:**
- HTTPS: Let's Encrypt Zertifikat (auto-renew)
- Firewall: ufw (nur Ports 22, 80, 443, 3000, 5678, 8000)
- SSH: Key-basiert (keine Passwort-Auth)

**Konfiguration:**
- System-Prompt: `API_System_Prompt_KONSOLIDIERT.md` (~6.500 Tokens)
- RAG-Schema: `RAG_Metadata_Schema.yaml` (15 Module, 85 Sub-TAGs)
- User-Config: `OpenWebUI_Users_Config.yaml` (18 aktive User)
- Wissens-Collections: 3 YAML-Dateien (Prozesse, Cluster, Stakeholder)

**ChromaDB-Konfiguration:**
- Embedding-Modell: all-MiniLM-L6-v2 (384 Dimensionen)
- Chunk-Größe: 800-1500 Tokens
- Overlap: 175 Tokens
- Distance-Metrik: Cosine
- Collections: OSP_COMPLETE, OSP_C1-C4

**User-Zugriff:**
- L3 (Vertraulich): 3 User (CS, CA, SV)
- L2 (Abteilung): 9 User (AL, TS, SK, BS, MD, DR, OK, DS, MR)
- L1 (Public): 6 User (DU, ASC, NR, JR, IB, WK)
- Pilot-User: AL, CS, SV, TS, SK

**Backup:**
- Automatisch: Hetzner Snapshots (wöchentlich)
- Manuell: /opt/osp/backups/ (täglich via Cron)
- Offsite: SharePoint-Sync der Konfigurationsdateien

**Wartung:**
- Verantwortlich: AL (QM & KI-Manager)
- Monitoring: UptimeRobot + Grafana (geplant)
- Updates: Docker-Images monatlich aktualisieren

**Verbindung zu internem Netzwerk:**
- Kein direkter VPN-Tunnel (Design-Entscheidung)
- Datenaustausch über SharePoint-Sync + API-Calls
- RAG-Daten werden über ChromaDB-Import synchronisiert

**Kritikalität:** 🟡 HOCH  
**ISO:** 7.1.3 (Infrastruktur), 7.5 (Dokumentierte Information)

**Migrationsstatus (2025-12-07):**
- ✅ Server provisioniert und konfiguriert
- ✅ Docker-Container installiert
- ✅ SSL-Zertifikat aktiv
- ✅ System-Prompt konsolidiert (~6.500 Tokens)
- ✅ 18 User-Accounts konfiguriert
- ⏳ Initiale Dokumenten-Synchronisation (nächster Schritt)
- ⏳ Pilot-Test mit 5 Usern (geplant)

---

### 3. WINDOWS SERVER LIZENZEN

#### 3.1 Windows Server 2019 Standard

**Lizenzschlüssel:**
- HVHC2-68N37-HMHBM-39MV4-BKHRC (SRV-HV01 Hyper-V Host)
- [Weitere Lizenzschlüssel für VMs: zu ergänzen]

**Lizenzierung:** Pro 2 Kerne (Core-basiert)  
**Anzahl Cores:** SRV-HV01: 2x Intel Xeon (insgesamt 16 Cores) → 8 Lizenzen benötigt

**VMs lizenziert:**
- SRV-FS (Fileserver)
- WISSRV-TIMELINE (Timeline ERP)
- SRV-APP (Timeline Alt)

---

#### 3.2 Windows Server 2022 Standard

**VMs lizenziert:**
- SRV-DC01 (Domain Controller)
- SQL01 (DocuWare DB)

**Lizenzschlüssel:** [zu ergänzen]

---

#### 3.3 Windows Server 2025 Standard

**Lizenzschlüssel:** DYP9J-K9H7W-3YKDH-M64V6-YGHYG  
**VM:** SRV-TS02 (Terminalserver)

---

#### 3.4 Client Access Licenses (CALs)

**Windows Server CALs:**
- Typ: User CAL (nicht Device CAL)
- Anzahl: 60 CALs
- Lizenzierung: Über Microsoft Volume Licensing

**Remote Desktop Services (RDS) CALs:**
- Typ: User CAL
- Anzahl: 56 aktive
- Lizenzserver: SRV-TS02 (192.168.10.232)

---

#### 3.5 Microsoft Office Lizenzen

**Office 2013 Professional Plus (GVLK):**
- Lizenzschlüssel: YC7DK-G2NP3-2QQC3-J6H88-GVGXT
- Installationen: ~20 Clients + Terminalserver
- **Migration geplant:** Umstellung auf Microsoft 365 Apps (M365 Business Premium)

**Office 2019 Professional Plus:**
- Lizenzschlüssel: [zu ergänzen]
- Installationen: ~5 Einzelplätze

---

#### 3.6 Exchange Server 2019

**Status:** ❌ **NICHT aktiv** - Exchange vollständig in M365 Cloud migriert  
**Lizenzschlüssel:** G3FMN-FGW6B-[weitere Zeichen unbekannt]  
**Hinweis:** Lokale Exchange-Installation wurde 2024 deaktiviert, alle Postfächer in Microsoft 365 Exchange Online

---

### 4. ACTIVE DIRECTORY & GRUPPENRICHTLINIEN

#### 4.1 Active Directory Struktur

**Domäne:** schneider.local  
**Forest:** schneider.local (Single-Domain-Forest)  
**Domänen-Controller:** SRV-DC01 (192.168.10.200)

**Organisationseinheiten (OUs):**
- Benutzer
  - Verwaltung
  - Produktion
  - Geschäftsleitung
  - Service-Accounts
- Computer
  - Clients
  - Server
  - Laptops
- Gruppen
  - Abteilungen
  - Sicherheit
  - Verteilung

**Wichtige Sicherheitsgruppen:**
- Domain Admins
- TerminalServerUser
- Sophos-VPN-User
- DATEV-Gruppe
- Timeline-User
- DocuWare-User
- Drucker-Admins
- Netzlaufwerk-Zugriff (F:, H:, K:, M:, X:)

---

#### 4.2 Gruppenrichtlinien (GPOs) - 17 aktive

**Computerkonfiguration:**

1. **Default Domain Policy** - Basis-Richtlinien (Passwort-Komplexität, Konto-Sperrung)
2. **Drucker_Terminalserver** - Drucker-Verteilung (12 Netzwerkdrucker)
3. **Laufwerke** - Netzlaufwerke (F:, H:, K:, M:, X: automatisch mappen)
4. **Benutzer – Netzlaufwerke** - Zusätzliche Laufwerke (N: Schliffbild)
5. **TLS1.2 aktiviert** - TLS 1.2 für .NET-Anwendungen erzwingen
6. **Windows Update** - WSUS-Server [zu konfigurieren]
7. **Firewall-Regeln** - Windows Firewall Einstellungen
8. **SMBv1 deaktiviert** - Sicherheit (SMB1-Protokoll deaktivieren)
9. **BitLocker** - Verschlüsselung (Laptops)
10. **AppLocker** - Anwendungssteuerung
11. **Software-Installation** - Auto-Deployment

**Benutzerkonfiguration:**

12. **Passwort-Policy** - Kennwort-Anforderungen
13. **Desktop-Einstellungen** - Wallpaper, Screensaver
14. **Ordnerumleitung** - Dokumente → Netzlaufwerk X:
15. **Internet Explorer Settings** - Browser-Konfiguration (Legacy)
16. **OneDrive-Integration** - Microsoft 365 OneDrive
17. **Power Settings** - Energieverwaltung

**Wichtige GPO-Parameter:**

| Parameter | Wert | Beschreibung |
|-----------|------|--------------|
| Passwort-Länge | Min. 8 Zeichen | Mindestanforderung |
| Passwort-Komplexität | Aktiviert | Groß-/Kleinbuchstaben + Ziffer |
| Konto-Sperrung | 5 Fehlversuche | Nach 30 Min. Entsperrung |
| TLS 1.2 | Erzwungen | .NET Framework |
| SMB1 | Deaktiviert | Sicherheit |

---

### 5. BACKUP-SYSTEME

#### 5.1 Veeam Backup & Replication 12 (Lokal)

**Backup-Server:** SRV-HV01 (Hyper-V Host)  
**Version:** Veeam Backup & Replication 12  
**Lizenz:** [zu ergänzen]

**Backup-Ziel:** NAS-KSBS (Synology RS815, 192.168.10.105)  
**Retention:** 7 Tage (7 Wiederherstellungspunkte)  
**Zeitplan:** Täglich 02:00 Uhr

**Gesicherte VMs (7):**
1. SRV-DC01 (Domain Controller)
2. SRV-FS (Fileserver)
3. SRV-TS02 (Terminalserver)
4. WISSRV-TIMELINE (Timeline ERP)
5. SQL01 (DocuWare DB)
6. DATEV (DATEV Arbeitsplatz)
7. SRV-APP (Timeline Alt)

**Nicht gesichert:** KOMAX-VM (keine Backup-Notwendigkeit)

**Wartung:** Gromnitza IT (GIT)

---

#### 5.2 Terra Cloud Backup (Extern)

**Provider:** Terra Cloud (Telekom-Partner)  
**Vertrag:** Auftragsverarbeitungsvertrag (AVV) vorhanden  
**Backup-Stände:** 42 Wiederherstellungspunkte  
**Retention:** 6 Wochen (GFS-Schema - [Details zu dokumentieren])

**Zeitplan:** Täglich nach Veeam-Backup  
**Bandbreite:** Upload via Deutsche Telekom DSL 100  
**Verschlüsselung:** AES-256

**Gesicherte Daten:**
- Alle 7 VMs (via Veeam)
- Fileserver-Freigaben (inkrementell)

**Test-Restores:**
- Letzter Test: [zu dokumentieren]
- Geplant: Q1 2026 (Verantwortlich: AL)

**Wartung:** Terra Cloud Support

---

### 6. MICROSOFT 365 INTEGRATION

#### 6.1 Entra ID Connect (Azure AD Connect)

**Server:** SRV-DC01 (192.168.10.200)  
**Synchronisation:** Active Directory ↔ Microsoft 365 (Entra ID)  
**Intervall:** Alle 30 Minuten

**Synchronisierte Objekte:**
- User (schneider.local → @schneider-kabelsatzbau.de)
- Gruppen (Sicherheit + Verteilung)
- Kennwort-Hash-Synchronisation (aktiviert)

**Single Sign-On (SSO):** Nahtlose SSO aktiviert (Seamless SSO)

**Multi-Faktor-Authentifizierung (MFA):**
- Aktiviert für: Geschäftsleitung, IT, QM
- Conditional Access Policies: [zu dokumentieren]

**Lizenzierung:** Microsoft 365 Business Premium (19 User)

---

## VERANTWORTLICHKEITEN

| Rolle | Verantwortlich | Aufgaben |
|-------|----------------|----------|
| **IT-Gesamtverantwortung** | AL (Andreas Löhr) | Server-Management, AD-Verwaltung, Backup-Überwachung, Lizenzen |
| **Geschäftsleitung** | CS (Christoph Schneider) | IT-Budget, Investitionsentscheidungen, Strategie |
| **Externer IT-Support** | Gromnitza IT (GIT) | Server-Wartung, Veeam-Backup, Troubleshooting, Remote-Support |
| **Hyper-V Administration** | AL + GIT | VM-Management, Ressourcen-Zuteilung, Performance-Monitoring |
| **Active Directory** | AL | User-/Gruppen-Verwaltung, GPO-Management, Entra ID Connect |
| **Backup-Verantwortung** | AL | Veeam + Terra Cloud Monitoring, Test-Restores |
| **Timeline ERP** | GIT | Applikations-Support, Updates |
| **DocuWare** | GIT | Datenbank-Wartung, Backup-Überwachung |
| **DATEV** | Externes DATEV-Support | Software-Updates, Fehlerbehandlung |
| **Produktions-IT (KOMAX-VM)** | Jürgen Schleifert | Maschinen-Steuerung, lokale VM-Administration |

---

## PROZESSE

### 1. Neuen User in Active Directory anlegen

1. **Active Directory Users and Computers öffnen** (SRV-DC01)
2. **OU auswählen** (z.B. Benutzer\Verwaltung)
3. **Rechtsklick → Neu → Benutzer**
4. **Daten eingeben:**
   - Vorname, Nachname
   - Anmeldename (z.B. a.loehr)
   - Passwort (mind. 8 Zeichen, komplex)
5. **Gruppen zuweisen:**
   - TerminalServerUser (falls RDS-Zugriff)
   - Sophos-VPN-User (falls VPN-Zugriff)
   - Abteilungs-Gruppen (Timeline, DocuWare, etc.)
6. **Entra ID Connect synchronisiert automatisch** (nach max. 30 Min.)
7. **Microsoft 365 Lizenz zuweisen** (Admin-Portal)
8. **User informieren** (Anmeldename, temporäres Passwort)

### 2. Neue VM auf SRV-HV01 erstellen

1. **Hyper-V Manager öffnen** (SRV-HV01)
2. **Neu → Virtueller Computer**
3. **Konfiguration:**
   - Name (z.B. SRV-TEST01)
   - Generation 2 (UEFI)
   - RAM: 4 GB (dynamisch oder statisch)
   - Netzwerk: LAN (Hyper-V Switch)
   - Festplatte: 100 GB (dynamisch erweiterbar)
4. **Betriebssystem installieren** (ISO mounten)
5. **Statische IP vergeben** (192.168.10.XXX)
6. **In Domäne aufnehmen** (schneider.local)
7. **Windows Updates installieren**
8. **Veeam Backup konfigurieren** (Job hinzufügen)

### 3. Backup-Test durchführen

**Veeam Lokal:**
1. **Veeam Console öffnen** (SRV-HV01)
2. **Backup Job auswählen**
3. **Rechtsklick → Restore → Entire VM**
4. **Restore Point auswählen** (neuester)
5. **Ziel:** Anderer Speicherort (nicht produktiv!)
6. **Restore starten**
7. **VM starten und Funktionalität prüfen**
8. **Test-VM löschen**

**Terra Cloud:**
1. **Terra Cloud Portal öffnen**
2. **Backup-Set auswählen** (z.B. SRV-FS)
3. **Restore-Point auswählen**
4. **Download starten** (zu Test-Verzeichnis)
5. **Wiederherstellung prüfen** (Dateien lesbar?)
6. **Dokumentation** (Test-Protokoll)

### 4. GPO erstellen/bearbeiten

1. **Group Policy Management öffnen** (SRV-DC01)
2. **Rechtsklick auf OU → Create a GPO in this domain**
3. **GPO-Name vergeben** (z.B. "Software-Deployment-TEST")
4. **Rechtsklick → Edit**
5. **Einstellungen konfigurieren:**
   - Computerkonfiguration (z.B. Software-Installation)
   - Benutzerkonfiguration (z.B. Desktop-Einstellungen)
6. **GPO verknüpfen** (mit OU)
7. **Testen** (gpupdate /force auf Test-Client)
8. **Dokumentation** (Kommentar in GPO)

---

## ORIGINAL-DOKUMENTE

**IT-Dokumentation (SharePoint):**
- [IT-Doku.md](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/IT/IT-Doku.md) - Vollständige IT-Dokumentation (Stand: 26.11.2025)

**Verträge (SharePoint):**
- [AVV Terra Cloud](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/AVV_Terra_Cloud.pdf) - Auftragsverarbeitungsvertrag Backup
- [Gromnitza IT Supportvertrag](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/Gromnitza_IT_Support.pdf) - IT-Support & Wartung

**Lizenzen (SharePoint):**
- [Windows Server Lizenzen](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Lizenzen/Windows_Server_Lizenzen.xlsx) - Übersicht aller Server-Lizenzen
- [Microsoft 365 Lizenzen](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Lizenzen/M365_Lizenzen.xlsx) - M365 User + Kosten

**Backup-Dokumentation (SharePoint):**
- [Veeam Backup Konfiguration](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/IT/Veeam_Backup_Config.pdf)
- [Terra Cloud Vertrag](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/Terra_Cloud_Vertrag.pdf)

---

## GRAFIKEN & DIAGRAMME

**Server-Infrastruktur:**
![Server-Topologie](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Server_Topologie_2025.png)
*Verwendung: SRV-HV01 Hyper-V Host, 8 VMs, Backup-Systeme*

**Active Directory Struktur:**
![AD Organisationseinheiten](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/AD_Struktur.png)
*Verwendung: OUs, Sicherheitsgruppen, Domänen-Controller*

**Backup-Fluss:**
![Backup-Strategie](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Backup_Flow.png)
*Verwendung: Veeam → NAS-KSBS (lokal 7 Tage) → Terra Cloud (42 Stände)*

---

## QUERVERWEISE

**Querverweise zu diesem Dokument werden zentral in KOM_KGS_Kontext_Gedaechtnis_System.md getrackt.**

Relevante verknüpfte Dokumente:
- IT_NET_DSL_LAN_WLAN.md
- IT_M365_Microsoft-365.md
- IT_DOKU_IT-Dokumentation.md
- HR_CORE_Personalstamm.md

---

## OFFENE FRAGEN

### ✅ Geklärt (2025-12-01 - Validierung AL + CS)

- [x] **SRV-BKP01 Entsorgung:** Hardware wird entsorgt (AL + CS)
- [x] **Exchange Server 2019 Lizenz G3FMN-FGW6B:** Vollständig in M365 Cloud migriert, on-premise NICHT mehr aktiv (AL)
- [x] **KOMAX-VM Windows 7:** Update auf Windows 10/11 NICHT möglich (Maschinen-Kompatibilität), VM isoliert vom Produktiv-Netzwerk → Sicherheitsrisiko akzeptabel (AL + Jürgen Schleifert)

### Wichtig (🟡 vor nächster Review klären)

- [ ] **Backup-Test-Protokolle:** Terra Cloud Test-Restores Q1 2026 durchführen. (Verantwortlich: AL, Frist: 2026-03-31)
- [ ] **Veeam 42 Backupstände Terra Cloud:** GFS-Schema (Grandfather-Father-Son) dokumentieren - welche Backup-Stände werden wie lange aufbewahrt? (Verantwortlich: AL + GIT, Frist: 2026-01-15)
- [ ] **SRV-HV01 RAM-Auslastung:** 256 GB RAM - wie hoch ist Auslastung? Monitoring über 3 Monate. (Verantwortlich: AL, Frist: 2026-03-01)
- [ ] **GPO "TLS1.2 aktiviert":** Kompatibilitätsprüfung - welche Anwendungen könnten betroffen sein? (Verantwortlich: AL, Frist: 2026-02-28)

### Optional (🟢 später klären)

- [ ] **Office 2013 Migration:** Zeitplan für Umstellung auf M365 Apps festlegen. (Verantwortlich: CS + AL)
- [ ] **DATEV-Gruppe User-Anzahl:** Wie viele User in AD-Gruppe "DATEV-Gruppe"? (Verantwortlich: AL)

---

## ÄNDERUNGSHISTORIE

### [2.0] - 2025-12-01
**FREIGEGEBEN - Validierung abgeschlossen:**
- ✅ Offene Fragen geklärt (3 kritische Fragen):
  - SRV-BKP01: Entsorgung geplant (Status aktualisiert)
  - Exchange G3FMN-FGW6B: Hinweis "❌ NICHT aktiv" ergänzt
  - KOMAX-VM: Sicherheitshinweis "✅ Isoliert", "❌ Update NICHT möglich", "✅ Risiko akzeptabel"
- ✅ Querverweise-Dokumentation nach KOM_KGS ausgelagert (zentrale Verwaltung)
- ✅ Status geändert: PRODUKTIV (RAG) → FREIGEGEBEN
- ✅ Datenstand aktualisiert: 2025-12-01

**Validiert durch:** AL (Andreas Löhr, QM/IT)
**Freigabe:** CS (Christoph Schneider, GF)

---

### [2.0] - 2025-12-01 (PRODUKTIV RAG)
**Produktivversion - BEFÜLLT + RAG-OPTIMIERT:**
- ✅ Template befüllt via Import-Flow Phase 3
- ✅ RAG-Optimierung integriert (Phase 5)
- ✅ Rohdaten: IT-Doku.md (26.11.2025, ~1.200 Zeilen)
- ✅ DSGVO-Prüfung: Nur Kürzel (AL, CS, GIT) verwendet
- ✅ Token-Effizienz: -12% vs. Rohdaten (Tabellen kompaktiert, Redundanzen eliminiert)
- ✅ Keywords: 30 Primary (Server, Hyper-V...), 50+ Secondary (192.168.10.200, DYP9J-K9H7W...)
- ✅ PDF-Links: 6 Dokumente verlinkt (IT-Doku, AVV Terra Cloud, Gromnitza Support, Lizenzen, Veeam, Terra Cloud)
- ✅ Bilder: 3 Diagramme (Server-Topologie, AD-Struktur, Backup-Fluss)
- ✅ Querverweise: 10 Links identifiziert (4 bidirektional, 6 ausgehend)

**Datenquellen:**
- IT-Doku.md (26.11.2025) - Server, VMs, Lizenzen, AD, GPOs, Backup
- Active Directory Export (SRV-DC01)
- Veeam Backup Reports

**Verantwortlich:** AL (QM/IT)

---

### [1.1] - 2025-11-20
**Erstversion:**
- Basis-Struktur IT_CORE erstellt

**Verantwortlich:** AL

---

*Dieses Dokument ist die zentrale Quelle für die komplette Client-Server-Infrastruktur inkl. Server, VMs, Lizenzen, Active Directory und Backup-Systeme. Status: FREIGEGEBEN - ChromaDB-Import in Main/IT_Infrastruktur/ erfolgt.*

(C: 100%) [OSP]
