# [IT][CORE] Client-Server-Struktur

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 2.2 | **TAG:** [IT][CORE] | **Erstellt:** 2025-11-20 | **Aktualisiert:** 2025-12-23 | **Autor:** AL | **Verantwortlich:** AL (QM/IT) | **Cluster:** ðŸ”´ C4-Support | **Zugriff:** ðŸŸ¡ L2-Abteilung | **Status:** âœ… FREIGEGEBEN | **ISO-Norm:** 9001:2015 (Kap. 7.1.3, 7.1.4) | **KritikalitÃ¤t:** ðŸ”´ SEHR HOCH | **Primary Keywords:** Server, Hyper-V, Virtualisierung, Windows Server, SRV-HV01, SRV-DC01, SRV-FS, SRV-TS02, Timeline, DocuWare, Backup, Veeam, Terra Cloud, Active Directory, schneider.local, GPO, Lizenzen, RDS-CAL, Windows Server 2019, Windows Server 2025, Entra ID Connect (30+) | **Secondary Keywords:** 192.168.10.200, 192.168.10.230, 192.168.10.232, 192.168.10.240, WISSRV-TIMELINE, SQL01, DATEV, SRV-BKP01, Gromnitza IT, GIT, HPE ProLiant DL380 Gen10, Microsoft 365, Veeam Backup 12, DYP9J-K9H7W-3YKDH, HVHC2-68N37-HMHBM (50+) | **Chunk-Strategie:** Markdown-Header (##) | **Datenstand:** 2025-12-23

---

## ZWECK

Zentrale Dokumentation der Client-Server-Infrastruktur: 2 physische Server (SRV-HV01 Hyper-V Host aktiv, SRV-BKP01 auÃŸer Dienst), 8 virtuelle Maschinen, Windows Server Lizenzen, Active Directory (schneider.local), Gruppenrichtlinien, Backup-Systeme (Veeam lokal + Terra Cloud), Microsoft 365 Integration. Dient als Single Source of Truth fÃ¼r IT-Troubleshooting, Disaster Recovery und Compliance.

---

## INHALT

### 1. PHYSISCHE SERVER

#### 1.1 SRV-HV01 (Hyper-V Host) - âœ… AKTIV

**Modell:** HPE ProLiant DL380 Gen10  
**Seriennummer:** [zu ergÃ¤nzen]  
**Standort:** Server-Raum BÃ¼rogebÃ¤ude (klimatisiert)  
**Betriebssystem:** Windows Server 2019 Standard  
**LizenzschlÃ¼ssel:** HVHC2-68N37-HMHBM-39MV4-BKHRC  
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
- Lokal: Veeam Backup & Replication 12 â†’ NAS-KSBS (7 Tage Retention)
- Cloud: Terra Cloud Backup (42 Backup-StÃ¤nde, Retention: 6 Wochen)

---

#### 1.2 SRV-BKP01 (Backup-Server) - âŒ AUSSERDIENST - ENTSORGUNG GEPLANT

**Status:** Seit 2024 auÃŸer Dienst, Hardware wird entsorgt  
**Modell:** HPE ProLiant DL360 Gen9 (alt)  
**Rolle:** Ehemaliger Backup-Server (ersetzt durch Terra Cloud)  
**Entscheidung:** AL + CS (01.12.2025)

---

### 2. VIRTUELLE MASCHINEN (8 VMs)

Alle VMs laufen auf **SRV-HV01** (Hyper-V Host).

#### 2.1 SRV-DC01 (Domain Controller) - âœ… PRODUKTIV

**Betriebssystem:** Windows Server 2022 Standard  
**IP:** 192.168.10.200  
**Rollen:**
- Active Directory Domain Services (AD DS)
- DNS-Server
- DHCP-Server
- Entra ID Connect (Microsoft 365 Synchronisation)

**DomÃ¤ne:** schneider.local  
**Forest-Level:** Windows Server 2016  
**AD-User:** ~60 aktive Konten  
**AD-Computer:** ~80 Clients + Server

**DNS-Zonen:**
- schneider.local (intern)
- 10.168.192.in-addr.arpa (Reverse Lookup)

**DHCP-Bereich:**
- 192.168.10.100 - 192.168.10.199 (Clients)
- Lease-Dauer: 8 Tage

**Backup:** TÃ¤glich via Veeam â†’ Terra Cloud

---

#### 2.2 SRV-FS (Fileserver) - âœ… PRODUKTIV

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
- X: = PersÃ¶nliches Laufwerk (%USERNAME%)
- N: = Schliffbild
- I:, W:, L:, G:, Z: = [Verwendung zu ermitteln]

**Storage:**
- PrimÃ¤r: 2 TB auf SRV-HV01
- Backup: Veeam â†’ Terra Cloud (tÃ¤glich)

**Drucker:** 12 Netzwerkdrucker via Printserver-Rolle (siehe IT_NET)

---

#### 2.3 SRV-TS02 (Terminalserver) - âœ… PRODUKTIV

**Betriebssystem:** Windows Server 2025 Standard  
**LizenzschlÃ¼ssel:** DYP9J-K9H7W-3YKDH-M64V6-YGHYG  
**IP:** 192.168.10.232  
**Rolle:** Remote Desktop Services (RDS)

**RDS-Lizenzen:**
- User CALs: 56 aktive (Lizenzserver: SRV-TS02)
- LizenzschlÃ¼ssel: [zu ergÃ¤nzen]

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

**Backup:** TÃ¤glich via Veeam â†’ Terra Cloud

---

#### 2.4 WISSRV-TIMELINE (Timeline ERP) - âœ… PRODUKTIV

**Betriebssystem:** Windows Server 2019 Standard  
**IP:** 192.168.10.111  
**Rolle:** Timeline ERP Applikationsserver

**Timeline-Version:** [zu ergÃ¤nzen]  
**Datenbank:** SQL Server (lokal auf VM)  
**Lizenzierung:** Concurrent User

**Zugriff:**
- Direkt: Timeline-Client (Installations-Ordner)
- Remote: Via Terminalserver (SRV-TS02)

**Wartung:** Gromnitza IT (GIT)

**Backup:** TÃ¤glich via Veeam â†’ Terra Cloud

---

#### 2.5 SQL01 (DocuWare Datenbank) - âœ… PRODUKTIV

**Betriebssystem:** Windows Server 2022 Standard  
**IP:** 192.168.10.235  
**Rolle:** DocuWare Datenbank-Server

**SQL Server:** Microsoft SQL Server 2019 Standard  
**DocuWare-Version:** [zu ergÃ¤nzen]  
**DatenbankgrÃ¶ÃŸe:** ~500 GB

**Zugriff:**
- DocuWare Web-Client: https://docuware.schneider.local
- Admin-Zugang: SQL Server Management Studio

**Wartung:** Gromnitza IT (GIT)

**Backup:**
- SQL-Backup: TÃ¤glich (Transaction Log stÃ¼ndlich)
- VM-Backup: TÃ¤glich via Veeam â†’ Terra Cloud

---

#### 2.6 DATEV (DATEV Arbeitsplatz) - âœ… PRODUKTIV

**Betriebssystem:** Windows 10 Pro (VM)  
**IP:** 192.168.10.99  
**Rolle:** DATEV Arbeitsplatz-VM

**DATEV-Module:**
- DATEV Unternehmen online
- DATEV Lohn und Gehalt (Ã¼ber Steuerberater)

**Zugriff:**
- Direkt: RDP â†’ 192.168.10.99
- Benutzer: AD-Gruppe "DATEV-Gruppe" [Anzahl zu ermitteln]

**Wartung:** DATEV eG (externer Support)

**Backup:** TÃ¤glich via Veeam â†’ Terra Cloud

---

#### 2.7 KOMAX-VM (Maschinensteuerung) - âš ï¸ SICHERHEITSRISIKO

**Betriebssystem:** Windows 7 Professional (32-bit)  
**IP:** 192.168.10.106  
**Rolle:** KOMAX Crimp-Maschinen Steuerung

**Sicherheitshinweis:**
- âœ… **Isoliert vom Produktiv-Netzwerk** (VLAN-Trennung via Sophos Firewall)
- âŒ **Update-Status:** Update auf Windows 10/11 NICHT mÃ¶glich (Maschinen-KompatibilitÃ¤t)
- âœ… **Risiko-Bewertung:** Akzeptabel (Entscheidung: AL + JÃ¼rgen Schleifert, 01.12.2025)

**Zugriff:** Nur lokale Konsole (Produktionshalle)

**Wartung:** JÃ¼rgen Schleifert (Produktionsleiter)

**Backup:** âŒ Kein Backup (VM wird bei Hardwaredefekt neu aufgesetzt)

---

#### 2.8 SRV-APP (Timeline Applikationsserver Alt) - âš ï¸ WENIG GENUTZT

**Betriebssystem:** Windows Server 2019 Standard  
**IP:** 192.168.10.107  
**Rolle:** Alter Timeline Applikationsserver (teilweise ersetzt durch WISSRV-TIMELINE)

**Status:** Noch aktiv, aber wenig genutzt  
**Migration:** VollstÃ¤ndige AblÃ¶sung durch WISSRV-TIMELINE geplant

**Backup:** TÃ¤glich via Veeam â†’ Terra Cloud

---

#### 2.9 OSP-SERVER (Hetzner Cloud) - âœ… PRODUKTIV (aktualisiert 2025-12-15)

**Typ:** Cloud-Server (Hetzner)
**Modell:** CX43 (AMD EPYC) â¬†ï¸ Upgrade von CX33
**IP:** 46.224.102.30
**Betriebssystem:** Ubuntu 24.04 LTS
**Rolle:** OSP KI-Infrastruktur (Open WebUI, ChromaDB, n8n)

**Hardware:**
- **CPU:** 8 vCPU (AMD EPYC) â¬†ï¸ Upgrade
- **RAM:** 16 GB â¬†ï¸ Upgrade
- **Storage:** 160 GB NVMe SSD
- **Traffic:** 20 TB/Monat inkl.

**Dienste (Docker-Container):**

| Container | Port | Version | Zweck | Status |
|-----------|------|---------|-------|--------|
| **open-webui** | 3000 | v0.6.41 | Frontend fÃ¼r KI-Chat | âœ… Produktiv |
| **chromadb** | 8000 | v0.5.15 | RAG Vektor-Datenbank | âœ… Produktiv |
| **ollama** | 11434 | latest | LLM-Fallback (lokal) | âœ… Bereit |
| **n8n** | 5678 | latest | Workflow-Automation | âœ… Produktiv |

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
- Chunk-GrÃ¶ÃŸe: 800-1500 Tokens
- Overlap: 175 Tokens
- Distance-Metrik: Cosine
- Collections: OSP_COMPLETE, OSP_C1-C4

**User-Zugriff:**
- L3 (Vertraulich): 3 User (CS, CA, SV)
- L2 (Abteilung): 9 User (AL, TS, SK, BS, MD, DR, OK, DS, MR)
- L1 (Public): 6 User (DU, ASC, NR, JR, IB, WK)
- Pilot-User: AL, CS, SV, TS, SK

**Backup:**
- Automatisch: Hetzner Snapshots (wÃ¶chentlich)
- Manuell: /mnt/HC_Volume_104189729/osp/backups/ (tÃ¤glich via Cron)
- Offsite: SharePoint-Sync der Konfigurationsdateien

**Wartung:**
- Verantwortlich: AL (QM & KI-Manager)
- Monitoring: UptimeRobot + Grafana (geplant)
- Updates: Docker-Images monatlich aktualisieren

**Verbindung zu internem Netzwerk:**
- Kein direkter VPN-Tunnel (Design-Entscheidung)
- Datenaustausch Ã¼ber SharePoint-Sync + API-Calls
- RAG-Daten werden Ã¼ber ChromaDB-Import synchronisiert

**KritikalitÃ¤t:** ðŸŸ¡ HOCH  
**ISO:** 7.1.3 (Infrastruktur), 7.5 (Dokumentierte Information)

**Migrationsstatus (aktualisiert 2025-12-15):**
- âœ… Server provisioniert und konfiguriert
- âœ… Hardware-Upgrade CX33 â†’ CX43 (8 vCPU, 16GB RAM)
- âœ… Docker-Container installiert (Open WebUI v0.6.41)
- âœ… SSL-Zertifikat aktiv
- âœ… System-Prompt konsolidiert (~6.500 Tokens)
- âœ… 18 User-Accounts konfiguriert
- âœ… 4 Pre-Processing-Module implementiert (15.12.2025)
- âœ… 58 Dokumente in ChromaDB geladen
- âœ… Pilot-Test mit 5 Usern lÃ¤uft
- â³ VollstÃ¤ndige Dokumenten-Synchronisation (Q1/2026)

---

### 3. WINDOWS SERVER LIZENZEN

#### 3.1 Windows Server 2019 Standard

**LizenzschlÃ¼ssel:**
- HVHC2-68N37-HMHBM-39MV4-BKHRC (SRV-HV01 Hyper-V Host)
- [Weitere LizenzschlÃ¼ssel fÃ¼r VMs: zu ergÃ¤nzen]

**Lizenzierung:** Pro 2 Kerne (Core-basiert)  
**Anzahl Cores:** SRV-HV01: 2x Intel Xeon (insgesamt 16 Cores) â†’ 8 Lizenzen benÃ¶tigt

**VMs lizenziert:**
- SRV-FS (Fileserver)
- WISSRV-TIMELINE (Timeline ERP)
- SRV-APP (Timeline Alt)

---

#### 3.2 Windows Server 2022 Standard

**VMs lizenziert:**
- SRV-DC01 (Domain Controller)
- SQL01 (DocuWare DB)

**LizenzschlÃ¼ssel:** [zu ergÃ¤nzen]

---

#### 3.3 Windows Server 2025 Standard

**LizenzschlÃ¼ssel:** DYP9J-K9H7W-3YKDH-M64V6-YGHYG  
**VM:** SRV-TS02 (Terminalserver)

---

#### 3.4 Client Access Licenses (CALs)

**Windows Server CALs:**
- Typ: User CAL (nicht Device CAL)
- Anzahl: 60 CALs
- Lizenzierung: Ãœber Microsoft Volume Licensing

**Remote Desktop Services (RDS) CALs:**
- Typ: User CAL
- Anzahl: 56 aktive
- Lizenzserver: SRV-TS02 (192.168.10.232)

---

#### 3.5 Microsoft Office Lizenzen

**Office 2013 Professional Plus (GVLK):**
- LizenzschlÃ¼ssel: YC7DK-G2NP3-2QQC3-J6H88-GVGXT
- Installationen: ~20 Clients + Terminalserver
- **Migration geplant:** Umstellung auf Microsoft 365 Apps (M365 Business Premium)

**Office 2019 Professional Plus:**
- LizenzschlÃ¼ssel: [zu ergÃ¤nzen]
- Installationen: ~5 EinzelplÃ¤tze

---

#### 3.6 Exchange Server 2019

**Status:** âŒ **NICHT aktiv** - Exchange vollstÃ¤ndig in M365 Cloud migriert  
**LizenzschlÃ¼ssel:** G3FMN-FGW6B-[weitere Zeichen unbekannt]  
**Hinweis:** Lokale Exchange-Installation wurde 2024 deaktiviert, alle PostfÃ¤cher in Microsoft 365 Exchange Online

---

### 4. ACTIVE DIRECTORY & GRUPPENRICHTLINIEN

#### 4.1 Active Directory Struktur

**DomÃ¤ne:** schneider.local  
**Forest:** schneider.local (Single-Domain-Forest)  
**DomÃ¤nen-Controller:** SRV-DC01 (192.168.10.200)

**Organisationseinheiten (OUs):**
- Benutzer
  - Verwaltung
  - Produktion
  - GeschÃ¤ftsleitung
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

1. **Default Domain Policy** - Basis-Richtlinien (Passwort-KomplexitÃ¤t, Konto-Sperrung)
2. **Drucker_Terminalserver** - Drucker-Verteilung (12 Netzwerkdrucker)
3. **Laufwerke** - Netzlaufwerke (F:, H:, K:, M:, X: automatisch mappen)
4. **Benutzer â€“ Netzlaufwerke** - ZusÃ¤tzliche Laufwerke (N: Schliffbild)
5. **TLS1.2 aktiviert** - TLS 1.2 fÃ¼r .NET-Anwendungen erzwingen
6. **Windows Update** - WSUS-Server [zu konfigurieren]
7. **Firewall-Regeln** - Windows Firewall Einstellungen
8. **SMBv1 deaktiviert** - Sicherheit (SMB1-Protokoll deaktivieren)
9. **BitLocker** - VerschlÃ¼sselung (Laptops)
10. **AppLocker** - Anwendungssteuerung
11. **Software-Installation** - Auto-Deployment

**Benutzerkonfiguration:**

12. **Passwort-Policy** - Kennwort-Anforderungen
13. **Desktop-Einstellungen** - Wallpaper, Screensaver
14. **Ordnerumleitung** - Dokumente â†’ Netzlaufwerk X:
15. **Internet Explorer Settings** - Browser-Konfiguration (Legacy)
16. **OneDrive-Integration** - Microsoft 365 OneDrive
17. **Power Settings** - Energieverwaltung

**Wichtige GPO-Parameter:**

| Parameter | Wert | Beschreibung |
|-----------|------|--------------|
| Passwort-LÃ¤nge | Min. 8 Zeichen | Mindestanforderung |
| Passwort-KomplexitÃ¤t | Aktiviert | GroÃŸ-/Kleinbuchstaben + Ziffer |
| Konto-Sperrung | 5 Fehlversuche | Nach 30 Min. Entsperrung |
| TLS 1.2 | Erzwungen | .NET Framework |
| SMB1 | Deaktiviert | Sicherheit |

---

### 5. BACKUP-SYSTEME

#### 5.1 Veeam Backup & Replication 12 (Lokal)

**Backup-Server:** SRV-HV01 (Hyper-V Host)  
**Version:** Veeam Backup & Replication 12  
**Lizenz:** [zu ergÃ¤nzen]

**Backup-Ziel:** NAS-KSBS (Synology RS815, 192.168.10.105)  
**Retention:** 7 Tage (7 Wiederherstellungspunkte)  
**Zeitplan:** TÃ¤glich 02:00 Uhr

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
**Backup-StÃ¤nde:** 42 Wiederherstellungspunkte  
**Retention:** 6 Wochen (GFS-Schema - [Details zu dokumentieren])

**Zeitplan:** TÃ¤glich nach Veeam-Backup  
**Bandbreite:** Upload via Deutsche Telekom DSL 100  
**VerschlÃ¼sselung:** AES-256

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
**Synchronisation:** Active Directory â†” Microsoft 365 (Entra ID)  
**Intervall:** Alle 30 Minuten

**Synchronisierte Objekte:**
- User (schneider.local â†’ @schneider-kabelsatzbau.de)
- Gruppen (Sicherheit + Verteilung)
- Kennwort-Hash-Synchronisation (aktiviert)

**Single Sign-On (SSO):** Nahtlose SSO aktiviert (Seamless SSO)

**Multi-Faktor-Authentifizierung (MFA):**
- Aktiviert fÃ¼r: GeschÃ¤ftsleitung, IT, QM
- Conditional Access Policies: [zu dokumentieren]

**Lizenzierung:** Microsoft 365 Business Premium (19 User)

---

## VERANTWORTLICHKEITEN

| Rolle | Verantwortlich | Aufgaben |
|-------|----------------|----------|
| **IT-Gesamtverantwortung** | AL (Andreas LÃ¶hr) | Server-Management, AD-Verwaltung, Backup-Ãœberwachung, Lizenzen |
| **GeschÃ¤ftsleitung** | CS (Christoph Schneider) | IT-Budget, Investitionsentscheidungen, Strategie |
| **Externer IT-Support** | Gromnitza IT (GIT) | Server-Wartung, Veeam-Backup, Troubleshooting, Remote-Support |
| **Hyper-V Administration** | AL + GIT | VM-Management, Ressourcen-Zuteilung, Performance-Monitoring |
| **Active Directory** | AL | User-/Gruppen-Verwaltung, GPO-Management, Entra ID Connect |
| **Backup-Verantwortung** | AL | Veeam + Terra Cloud Monitoring, Test-Restores |
| **Timeline ERP** | GIT | Applikations-Support, Updates |
| **DocuWare** | GIT | Datenbank-Wartung, Backup-Ãœberwachung |
| **DATEV** | Externes DATEV-Support | Software-Updates, Fehlerbehandlung |
| **Produktions-IT (KOMAX-VM)** | JÃ¼rgen Schleifert | Maschinen-Steuerung, lokale VM-Administration |

---

## PROZESSE

### 1. Neuen User in Active Directory anlegen

1. **Active Directory Users and Computers Ã¶ffnen** (SRV-DC01)
2. **OU auswÃ¤hlen** (z.B. Benutzer\Verwaltung)
3. **Rechtsklick â†’ Neu â†’ Benutzer**
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
8. **User informieren** (Anmeldename, temporÃ¤res Passwort)

### 2. Neue VM auf SRV-HV01 erstellen

1. **Hyper-V Manager Ã¶ffnen** (SRV-HV01)
2. **Neu â†’ Virtueller Computer**
3. **Konfiguration:**
   - Name (z.B. SRV-TEST01)
   - Generation 2 (UEFI)
   - RAM: 4 GB (dynamisch oder statisch)
   - Netzwerk: LAN (Hyper-V Switch)
   - Festplatte: 100 GB (dynamisch erweiterbar)
4. **Betriebssystem installieren** (ISO mounten)
5. **Statische IP vergeben** (192.168.10.XXX)
6. **In DomÃ¤ne aufnehmen** (schneider.local)
7. **Windows Updates installieren**
8. **Veeam Backup konfigurieren** (Job hinzufÃ¼gen)

### 3. Backup-Test durchfÃ¼hren

**Veeam Lokal:**
1. **Veeam Console Ã¶ffnen** (SRV-HV01)
2. **Backup Job auswÃ¤hlen**
3. **Rechtsklick â†’ Restore â†’ Entire VM**
4. **Restore Point auswÃ¤hlen** (neuester)
5. **Ziel:** Anderer Speicherort (nicht produktiv!)
6. **Restore starten**
7. **VM starten und FunktionalitÃ¤t prÃ¼fen**
8. **Test-VM lÃ¶schen**

**Terra Cloud:**
1. **Terra Cloud Portal Ã¶ffnen**
2. **Backup-Set auswÃ¤hlen** (z.B. SRV-FS)
3. **Restore-Point auswÃ¤hlen**
4. **Download starten** (zu Test-Verzeichnis)
5. **Wiederherstellung prÃ¼fen** (Dateien lesbar?)
6. **Dokumentation** (Test-Protokoll)

### 4. GPO erstellen/bearbeiten

1. **Group Policy Management Ã¶ffnen** (SRV-DC01)
2. **Rechtsklick auf OU â†’ Create a GPO in this domain**
3. **GPO-Name vergeben** (z.B. "Software-Deployment-TEST")
4. **Rechtsklick â†’ Edit**
5. **Einstellungen konfigurieren:**
   - Computerkonfiguration (z.B. Software-Installation)
   - Benutzerkonfiguration (z.B. Desktop-Einstellungen)
6. **GPO verknÃ¼pfen** (mit OU)
7. **Testen** (gpupdate /force auf Test-Client)
8. **Dokumentation** (Kommentar in GPO)

---

## ORIGINAL-DOKUMENTE

**IT-Dokumentation (SharePoint):**
- [IT-Doku.md](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/IT/IT-Doku.md) - VollstÃ¤ndige IT-Dokumentation (Stand: 26.11.2025)

**VertrÃ¤ge (SharePoint):**
- [AVV Terra Cloud](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/VertrÃ¤ge/AVV_Terra_Cloud.pdf) - Auftragsverarbeitungsvertrag Backup
- [Gromnitza IT Supportvertrag](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/VertrÃ¤ge/Gromnitza_IT_Support.pdf) - IT-Support & Wartung

**Lizenzen (SharePoint):**
- [Windows Server Lizenzen](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Lizenzen/Windows_Server_Lizenzen.xlsx) - Ãœbersicht aller Server-Lizenzen
- [Microsoft 365 Lizenzen](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Lizenzen/M365_Lizenzen.xlsx) - M365 User + Kosten

**Backup-Dokumentation (SharePoint):**
- [Veeam Backup Konfiguration](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/IT/Veeam_Backup_Config.pdf)
- [Terra Cloud Vertrag](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/VertrÃ¤ge/Terra_Cloud_Vertrag.pdf)

---

## GRAFIKEN & DIAGRAMME

**Server-Infrastruktur:**
![Server-Topologie](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Server_Topologie_2025.png)
*Verwendung: SRV-HV01 Hyper-V Host, 8 VMs, Backup-Systeme*

**Active Directory Struktur:**
![AD Organisationseinheiten](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/AD_Struktur.png)
*Verwendung: OUs, Sicherheitsgruppen, DomÃ¤nen-Controller*

**Backup-Fluss:**
![Backup-Strategie](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Backup_Flow.png)
*Verwendung: Veeam â†’ NAS-KSBS (lokal 7 Tage) â†’ Terra Cloud (42 StÃ¤nde)*

---

## QUERVERWEISE

**Querverweise zu diesem Dokument werden zentral in KOM_KGS_Kontext_Gedaechtnis_System.md getrackt.**

Relevante verknÃ¼pfte Dokumente:
- IT_NET_DSL_LAN_WLAN.md
- IT_M365_Microsoft-365.md
- IT_DOKU_IT-Dokumentation.md
- HR_CORE_Personalstamm.md

---

## OFFENE FRAGEN

### âœ… GeklÃ¤rt (2025-12-23 - Validierung AL + CS)

- [x] **SRV-BKP01 Entsorgung:** Hardware wird entsorgt (AL + CS)
- [x] **Exchange Server 2019 Lizenz G3FMN-FGW6B:** VollstÃ¤ndig in M365 Cloud migriert, on-premise NICHT mehr aktiv (AL)
- [x] **KOMAX-VM Windows 7:** Update auf Windows 10/11 NICHT mÃ¶glich (Maschinen-KompatibilitÃ¤t), VM isoliert vom Produktiv-Netzwerk â†’ Sicherheitsrisiko akzeptabel (AL + JÃ¼rgen Schleifert)

### Wichtig (ðŸŸ¡ vor nÃ¤chster Review klÃ¤ren)

- [ ] **Backup-Test-Protokolle:** Terra Cloud Test-Restores Q1 2026 durchfÃ¼hren. (Verantwortlich: AL, Frist: 2026-03-31)
- [ ] **Veeam 42 BackupstÃ¤nde Terra Cloud:** GFS-Schema (Grandfather-Father-Son) dokumentieren - welche Backup-StÃ¤nde werden wie lange aufbewahrt? (Verantwortlich: AL + GIT, Frist: 2026-01-15)
- [ ] **SRV-HV01 RAM-Auslastung:** 256 GB RAM - wie hoch ist Auslastung? Monitoring Ã¼ber 3 Monate. (Verantwortlich: AL, Frist: 2026-03-01)
- [ ] **GPO "TLS1.2 aktiviert":** KompatibilitÃ¤tsprÃ¼fung - welche Anwendungen kÃ¶nnten betroffen sein? (Verantwortlich: AL, Frist: 2026-02-28)

### Optional (ðŸŸ¢ spÃ¤ter klÃ¤ren)

- [ ] **Office 2013 Migration:** Zeitplan fÃ¼r Umstellung auf M365 Apps festlegen. (Verantwortlich: CS + AL)
- [ ] **DATEV-Gruppe User-Anzahl:** Wie viele User in AD-Gruppe "DATEV-Gruppe"? (Verantwortlich: AL)

---

## Ã„NDERUNGSHISTORIE

### [2.2] - 2025-12-23 - RAM-KORREKTUR
**Quelle:** Server-Erhebung 2025-12-23

**Korrekturen:**
- ❌ RAM-Dokumentation: 32GB war falsch dokumentiert
- ✅ Korrigiert auf: 16GB (verifiziert via `free -h`)

**Verantwortlich:** AL (QM & KI-Manager)

---

### [2.1] - 2025-12-15
**OSP-Server Hardware-Upgrade:**
- âœ… Server-Modell aktualisiert: CX33 â†’ CX43
- âœ… CPU aktualisiert: 4 vCPU â†’ 8 vCPU (AMD EPYC)
- âœ… RAM-Dokumentation korrigiert: CX43 hat 16GB
- âœ… Open WebUI Version: v0.6.40 â†’ v0.6.41
- âœ… Migrationsstatus aktualisiert (Pre-Processing-Module, Pilot-Test)

**Verantwortlich:** AL (QM/IT)

---

### [2.0] - 2025-12-23
**FREIGEGEBEN - Validierung abgeschlossen:**
- âœ… Offene Fragen geklÃ¤rt (3 kritische Fragen):
  - SRV-BKP01: Entsorgung geplant (Status aktualisiert)
  - Exchange G3FMN-FGW6B: Hinweis "âŒ NICHT aktiv" ergÃ¤nzt
  - KOMAX-VM: Sicherheitshinweis "âœ… Isoliert", "âŒ Update NICHT mÃ¶glich", "âœ… Risiko akzeptabel"
- âœ… Querverweise-Dokumentation nach KOM_KGS ausgelagert (zentrale Verwaltung)
- âœ… Status geÃ¤ndert: PRODUKTIV (RAG) â†’ FREIGEGEBEN
- âœ… Datenstand aktualisiert: 2025-12-23

**Validiert durch:** AL (Andreas LÃ¶hr, QM/IT)
**Freigabe:** CS (Christoph Schneider, GF)

---

### [2.0] - 2025-12-23 (PRODUKTIV RAG)
**Produktivversion - BEFÃœLLT + RAG-OPTIMIERT:**
- âœ… Template befÃ¼llt via Import-Flow Phase 3
- âœ… RAG-Optimierung integriert (Phase 5)
- âœ… Rohdaten: IT-Doku.md (26.11.2025, ~1.200 Zeilen)
- âœ… DSGVO-PrÃ¼fung: Nur KÃ¼rzel (AL, CS, GIT) verwendet
- âœ… Token-Effizienz: -12% vs. Rohdaten (Tabellen kompaktiert, Redundanzen eliminiert)
- âœ… Keywords: 30 Primary (Server, Hyper-V...), 50+ Secondary (192.168.10.200, DYP9J-K9H7W...)
- âœ… PDF-Links: 6 Dokumente verlinkt (IT-Doku, AVV Terra Cloud, Gromnitza Support, Lizenzen, Veeam, Terra Cloud)
- âœ… Bilder: 3 Diagramme (Server-Topologie, AD-Struktur, Backup-Fluss)
- âœ… Querverweise: 10 Links identifiziert (4 bidirektional, 6 ausgehend)

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

*Dieses Dokument ist die zentrale Quelle fÃ¼r die komplette Client-Server-Infrastruktur inkl. Server, VMs, Lizenzen, Active Directory und Backup-Systeme. Status: FREIGEGEBEN - ChromaDB-Import in Main/IT_Infrastruktur/ erfolgt.*

(C: 100%) [OSP]
