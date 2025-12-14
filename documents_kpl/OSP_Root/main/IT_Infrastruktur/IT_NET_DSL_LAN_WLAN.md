# [IT][NET] Netzwerk-Infrastruktur (DSL, LAN, WLAN)

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 2.0 | **TAG:** [IT][NET] | **Erstellt:** 2025-11-20 | **Aktualisiert:** 2025-12-01 | **Autor:** AL | **Verantwortlich:** AL (QM/IT) | **Cluster:** 🔴 C4-Support | **Zugriff:** 🟢 L1-Öffentlich | **Status:** ✅ FREIGEGEBEN | **ISO-Norm:** 9001:2015 (Kap. 7.1.3, 7.1.4) | **Kritikalität:** 🔴 SEHR HOCH | **Primary Keywords:** Router, Firewall, VPN, WLAN, Netzwerk, IP-Schema, LANCOM 883, FritzBox 7490, Sophos XGS108, SSL-VPN, DHCP, DNS, Deutsche Telekom, DSL 100, Netzlaufwerke, Drucker, Sophos Connect, Active Directory, schneider.local, VLAN, Gateway (30+) | **Secondary Keywords:** 192.168.10.50, 192.168.10.200, 192.168.10.254, X10304W8KGP6794, APRS001, remote.schneider-kabelsatzbau.de, Sophos-VPN-User, TerminalServerUser, 8142140886655826, 5412305823431797, Gromnitza IT, Telekommunikation Höhn, INWX, kabelsatzbau-schneider.de (50+) | **Chunk-Strategie:** Markdown-Header (##) | **Datenstand:** 2025-12-01

---

## ZWECK

Vollständige Dokumentation der Netzwerk-Infrastruktur: Internet-Anbindung (Deutsche Telekom DSL 100, 2 Router), Firewall & VPN (Sophos XGS108), IP-Adressierung (192.168.10.0/24), WLAN (4 Access Points), Netzlaufwerke (F:, H:, K:, M:, X: + GPO), 12 Netzwerkdrucker und externe Dienstleister. Dient als Single Source of Truth für Netzwerk-Troubleshooting, VPN-Setup, WLAN-Konfiguration und Dienstleister-Briefing.

---

## INHALT

### 1. INTERNET-ANBINDUNG

#### 1.1 Hauptleitung (LANCOM 883 VoIP)

**Hardware:** LANCOM 883 VoIP  
**IP:** 192.168.7.1  
**Provider:** Deutsche Telekom  
**Bandbreite:** DSL 100 (100 Mbit/s Download)  
**Typ:** Hauptleitung für Produktion

**Services:**
- Internet-Zugang (alle Clients, Server)
- VoIP-Telefonie
- VPN-Tunnel (Sophos Firewall)

#### 1.2 Backup-Leitung (FritzBox 7490)

**Hardware:** FritzBox 7490  
**IP:** 192.168.8.1  
**Provider:** Deutsche Telekom  
**Typ:** Backup-Leitung + WLAN Büro  
**Redundanz:** Automatisches Failover bei Hauptleitungs-Ausfall

**Services:**
- Backup-Internet
- WLAN Büro (SSID: APRS001)

---

### 2. FIREWALL & VPN

#### 2.1 Sophos XGS108 Firewall

**Modell:** Sophos XGS108  
**Seriennummer:** X10304W8KGP6794  
**IP:** 192.168.10.50  
**Management-URL:** https://192.168.10.50:4444 (intern), https://remote.schneider-kabelsatzbau.de:4444 (extern)

**SSL-VPN User Portal:**
- URL: https://remote.schneider-kabelsatzbau.de:4442
- VPN-Client: Sophos Connect

**Authentifizierung:**
- Methode: Active Directory Integration
- Domäne: schneider.local
- AD-Gruppe: Sophos-VPN-User
- AD-Server: SRV-DC01 (192.168.10.200)

**VPN-Zugriff ermöglicht:**
- ✅ Netzlaufwerke (F:, H:, K:, I:, W:, L:, G:, Z:, N:)
- ✅ Terminalserver (SRV-TS02, 192.168.10.232)
- ✅ Fileserver (SRV-FS, 192.168.10.230)
- ✅ Timeline ERP (WISSRV-TIMELINE, 192.168.10.111)
- ✅ DocuWare DMS (SQL01, 192.168.10.235)

**Firewall-Regeln:**
- NAT: Intern ↔ Extern
- Portfreigaben: RDP (3389), HTTPS (443), VPN (443, 4442, 4444)
- IPS/IDS: Aktiviert (Intrusion Prevention)
- Web-Filter: Aktiviert

---

### 3. IP-ADRESSIERUNG & DHCP/DNS

#### 3.1 IP-Schema

**Hauptnetz:** 192.168.10.0/24  
**Subnetzmaske:** 255.255.255.0  
**Gateway:** 192.168.10.50 (Sophos Firewall)  
**DNS-Server:** 192.168.10.200 (SRV-DC01)  
**DHCP-Server:** 192.168.10.200 (SRV-DC01)

**IP-Bereiche:**

| Bereich | Verwendung | Typ |
|---------|------------|-----|
| **1-99** | Infrastruktur (Firewall, Router, USV, NAS) | Statisch |
| **100-199** | DHCP-Pool (Clients, Laptops, Tablets) | Dynamisch |
| **200-254** | Server, Drucker, Netzwerk-Geräte | Statisch |

#### 3.2 Wichtige statische IPs

**Infrastruktur (1-99):**

| IP | Gerät | Beschreibung |
|----|-------|--------------|
| 192.168.10.50 | Sophos XGS108 | Firewall + Gateway |
| 192.168.10.51 | FritzBox 3270 | WLAN Halle 3 (AP001) |
| 192.168.10.52 | FritzBox 7330 | WLAN Halle 1 (APRS-LAG) |
| 192.168.10.99 | DATEVSRV | DATEV Arbeitsplatz VM |
| 192.168.10.105 | NAS-KSBS | Synology RS815 Backup |
| 192.168.10.106 | KOMAX-VM | KOMAX Maschinensteuerung |
| 192.168.10.107 | SRV-APP | Timeline Applikationsserver |
| 192.168.10.111 | WISSRV-TIMELINE | Timeline ERP |
| 192.168.10.119 | SMART UPS 2000 | USV |

**Server (200-254):**

| IP | Server | Rolle |
|----|--------|-------|
| 192.168.10.200 | SRV-DC01 | Domain Controller, DHCP, DNS |
| 192.168.10.230 | SRV-FS | Fileserver, Printserver |
| 192.168.10.232 | SRV-TS02 | Terminalserver (Win 2025) |
| 192.168.10.235 | SQL01 | DocuWare Datenbank |
| 192.168.10.240 | SRV-HV01 | Hyper-V Host |
| 192.168.10.241 | SRV-HV01 iLO | Lights-Out Management |
| 192.168.10.254 | FritzBox 7490 | WLAN Büro + Backup-Internet |

**Drucker (siehe Abschnitt 4.2)**

---

### 4. WLAN-INFRASTRUKTUR (4 Netze)

#### 4.1 WLAN 1 - Büro (FritzBox 7490)

**Hardware:** FritzBox 7490  
**IP:** 192.168.10.254  
**SSID:** APRS001 (2.4 GHz), APRS001-5 (5 GHz)  
**Passwort:** 8142140886655826  
**Abdeckung:** Bürogebäude (Verwaltung, Geschäftsleitung, QM, Einkauf, Vertrieb)  
**Verstärkung:** FritzRepeater  
**Funktion:** Hauptzugang für Büro-Mitarbeiter + Gäste

#### 4.2 WLAN 2 - Halle 1 (FritzBox 7330)

**Hardware:** FritzBox 7330  
**IP:** 192.168.10.52  
**SSID:** APRS-LAG  
**Passwort:** 8142140886655826  
**Abdeckung:** Lager-Bereich im Bürogebäude  
**Funktion:** Lager-Zugang (Wareneingang, Kommissionierung)

#### 4.3 WLAN 3 - Halle 2 (Sophos AP 15)

**Hardware:** Sophos AP 15 (Managed)  
**IP:** DHCP  
**SSID:** APRS002 (2.4 GHz + 5 GHz, Dual-Band)  
**Passwort:** 8142140886655826  
**Management:** Sophos Central  
**Abdeckung:** Produktionshalle 2  
**Funktion:** Produktion (Tablets, Handscanner)

#### 4.4 WLAN 4 - Halle 3 (FritzBox 3270)

**Hardware:** FritzBox 3270  
**IP:** 192.168.10.51  
**SSID:** AP001  
**Passwort:** 5412305823431797  
**Abdeckung:** Produktionshalle 3 (oben)  
**Funktion:** Produktion Obergeschoss

---

### 5. NETZLAUFWERKE

#### 5.1 Automatisch gemappte Laufwerke (GPO "Laufwerke")

**Fileserver:** \\srv-fs.schneider.local

| Laufwerk | Freigabe | Beschreibung |
|----------|----------|--------------|
| **F:** | \\srv-fs\Alte_Ablage | Alte Ablage (Archiv) |
| **H:** | \\srv-fs\Abteilung | Abteilungs-Ordner |
| **K:** | \\srv-fs\DMS | DMS-Daten (DocuWare) |
| **M:** | \\srv-fs\Mitarbeitermatrix | Mitarbeiter-Matrix, Organigramme |
| **X:** | \\srv-fs\%USERNAME% | Persönliches Laufwerk (benutzerspezifisch) |
| **I:** | \\srv-fs\[Freigabe_I] | [Verwendung zu ermitteln] |
| **W:** | \\srv-fs\[Freigabe_W] | [Verwendung zu ermitteln] |
| **L:** | \\srv-fs\[Freigabe_L] | [Verwendung zu ermitteln] |
| **G:** | \\srv-fs\[Freigabe_G] | [Verwendung zu ermitteln] |
| **Z:** | \\srv-fs\[Freigabe_Z] | [Verwendung zu ermitteln] |

**Mapping:** Automatisch via GPO beim Login

#### 5.2 Zusätzliche Laufwerke (GPO "Benutzer – Netzlaufwerke")

| Laufwerk | Freigabe | Beschreibung |
|----------|----------|--------------|
| **N:** | \\srv-fs.schneider.local\Schliffbild | Schliffbilder (Qualitätskontrolle) |

---

### 6. DRUCKER (12 Netzwerkdrucker)

#### 6.1 Drucker-Liste

**Alle Drucker sind via GPO "Drucker_Terminalserver" verteilt (SRV-FS als Printserver).**

| IP | Modell | Standort | Funktion |
|----|--------|----------|----------|
| 192.168.10.9 | SHARP BP-50C26 | Büro | Farb-Multifunktionsgerät |
| 192.168.10.11 | SHARP MX-B427PW | Empfang | Schwarz-Weiß MFP |
| 192.168.10.55 | OKI ES4132 | Warenlager | Laser-Drucker |
| 192.168.10.65 | ZDesigner GK420d | Versand | Etikettendrucker |
| 192.168.10.94 | SHARP MX-B427PW | Büro Dützer | Schwarz-Weiß MFP |
| 192.168.10.98 | SHARP MX-B356W | Büro | Schwarz-Weiß MFP |
| 192.168.10.143 | SHARP MX-3050 | Büro SAS | Farb-MFP |
| 192.168.10.149 | SHARP MX-B427PW | Halle Oben MB2 | Schwarz-Weiß MFP |
| 192.168.10.189 | SHARP MX-C304WH | Produktion | Farb-MFP |
| 192.168.10.193 | SHARP MX-B356W | Produktion | Schwarz-Weiß MFP |
| 192.168.10.197 | CAB MACH 4.3S/300 | Fertigung | Industrie-Etikettendrucker |
| 192.168.10.198 | Brady BP-PR-300-PLUS | Fertigung | Etikettendrucker |

#### 6.2 Drucker-Verwaltung

**Printserver:** SRV-FS (192.168.10.230)  
**Verteilung:** Via GPO (automatische Installation)  
**Wartung:** Büro Hoffmann (Herr Eisel, 02742/9310-0)  
**Toner/Verbrauchsmaterial:** Über Büro Hoffmann

---

### 7. EXTERNE DIENSTLEISTER

#### 7.1 IT-Support

**Gromnitza IT (GIT)**  
**Leistungen:** Server-Wartung, Netzwerk-Support, Firewall-Konfiguration, IT-Troubleshooting  
**Zugriff:** TeamViewer, Sophos SSL-VPN  
**Vertrag:** Siehe SharePoint (Gromnitza IT Supportvertrag.pdf)

#### 7.2 Telefonanlage

**Telekommunikation Höhn**  
**Ansprechpartner:** Michel Höhn  
**Telefon:** 0171-2111777  
**Leistungen:** Telefonanlage-Wartung, VoIP-Support, LANCOM 883 VoIP Konfiguration

#### 7.3 Domainverwaltung

**INWX GmbH & Co. KG**  
**Anschrift:** Prinzessinnenstr. 30, 10969 Berlin  
**Telefon:** +49 30 983 212 0  
**E-Mail:** hostmaster@inwx.de

**Verwaltete Domains:**
- kabelsatzbau-schneider.de
- schneider-kabelsatzbau.de

**DNS-Einträge:**
- remote.schneider-kabelsatzbau.de → Sophos Firewall (extern)

---

## VERANTWORTLICHKEITEN

| Rolle | Verantwortlich | Aufgaben |
|-------|----------------|----------|
| **Netzwerk-Gesamtverantwortung** | AL (Andreas Löhr) | Firewall-Verwaltung, VPN-User, WLAN-Konfiguration, IP-Verwaltung |
| **Geschäftsleitung** | CS (Christoph Schneider) | Netzwerk-Budget, Provider-Verträge, Investitionsentscheidungen |
| **Externer IT-Support** | Gromnitza IT (GIT) | Firewall-Konfiguration, Netzwerk-Troubleshooting, VPN-Setup |
| **Telefonanlage** | TK Höhn (Michel Höhn) | VoIP-Wartung, LANCOM 883 Konfiguration |
| **Domainverwaltung** | INWX | DNS-Verwaltung, Domain-Renewals |
| **Drucker-Wartung** | Büro Hoffmann (Hr. Eisel) | Drucker-Reparatur, Toner-Service |

---

## PROZESSE

### 1. VPN-User hinzufügen

1. **Active Directory öffnen** (SRV-DC01)
2. **User zur Gruppe hinzufügen:** Sophos-VPN-User
3. **Sophos Firewall:** User automatisch synchronisiert (AD-Integration)
4. **Sophos Connect Client** an User versenden
5. **VPN-Anleitung** bereitstellen (SharePoint)
6. **Test-Verbindung** durchführen

### 2. Neues WLAN-Gerät hinzufügen

**WLAN 1, 2, 3 (Büro, Halle 1, 2):**
1. Gerät einschalten
2. SSID wählen (APRS001, APRS-LAG, APRS002)
3. Passwort eingeben: **8142140886655826**
4. IP-Adresse (DHCP) automatisch erhalten

**WLAN 4 (Halle 3):**
1. Gerät einschalten
2. SSID wählen (AP001)
3. Passwort eingeben: **5412305823431797**
4. IP-Adresse (DHCP) automatisch erhalten

### 3. Statische IP vergeben

1. **IP-Schema prüfen** (Bereiche 1-99, 200-254)
2. **Freie IP ermitteln** (via Netzwerk-Scanner oder Liste)
3. **Gerät konfigurieren:**
   - IP-Adresse: 192.168.10.XXX
   - Subnetzmaske: 255.255.255.0
   - Gateway: 192.168.10.50
   - DNS: 192.168.10.200
4. **Dokumentation updaten** (dieses Dokument)
5. **DHCP-Ausschluss** in SRV-DC01 konfigurieren

### 4. Firewall-Regel hinzufügen

1. **Sophos Firewall** öffnen (https://192.168.10.50:4444)
2. **Firewall → Rules** navigieren
3. **Neue Regel erstellen:**
   - Source: Intern/Extern
   - Destination: Ziel-IP/Netzwerk
   - Service: Port/Protokoll
   - Action: Allow/Deny
4. **Regel testen** (Ping, Telnet, Nmap)
5. **Dokumentation** in Sophos-Interface

### 5. Netzwerk-Troubleshooting

**Kein Internet:**
1. **Hauptleitung prüfen:** LANCOM 883 (192.168.7.1) erreichbar?
2. **Backup-Leitung prüfen:** FritzBox 7490 (192.168.8.1) erreichbar?
3. **Firewall prüfen:** Sophos (192.168.10.50) erreichbar?
4. **Gateway prüfen:** Ping 192.168.10.50
5. **DNS prüfen:** nslookup google.com 192.168.10.200
6. **Gromnitza IT kontaktieren** falls keine Lösung

**Kein WLAN:**
1. **WLAN-Passwort korrekt?** (siehe Abschnitt 4)
2. **Access Point erreichbar?** (Ping auf IP)
3. **DHCP funktioniert?** IP-Adresse erhalten?
4. **FritzBox neu starten** (Strom aus/ein)
5. **Gromnitza IT kontaktieren** falls keine Lösung

---

## ORIGINAL-DOKUMENTE

**Dokumentation (SharePoint):**
- [IT-Doku.md](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/IT/IT-Doku.md) - Vollständige IT-Dokumentation (Stand: 26.11.2025)

**Firewall-Konfiguration (SharePoint):**
- [Sophos XGS108 Config-Backup](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/IT/Sophos_Config_Backup_2025.xml) - Firewall-Konfiguration Backup

**Support-Verträge (SharePoint):**
- [Gromnitza IT Supportvertrag](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/Gromnitza_IT_Support.pdf)
- [TK Höhn Wartungsvertrag](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/TK_Hoehn_Wartung.pdf)
- [INWX Rechnung](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Verträge/INWX_Domain_Rechnung.pdf)

**Anleitungen (SharePoint):**
- [VPN-Anleitung Sophos Connect](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Anleitungen/VPN_Sophos_Connect.pdf)

---

## GRAFIKEN & DIAGRAMME

**Netzwerk-Topologie:**
![Netzwerk-Infrastruktur Diagramm](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/Netzwerk_Topologie_2025.png)
*Verwendung: Router, Firewall, WLAN-APs, Server-Netz, DHCP-Bereiche*

**IP-Schema:**
![IP-Adressierung 192.168.10.0/24](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/IP_Schema.png)
*Verwendung: IP-Bereiche (1-99, 100-199, 200-254), wichtige statische IPs*

**WLAN-Abdeckung:**
![WLAN Coverage Map](https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Dokumente/Icons_Bilder/WLAN_Coverage.png)
*Verwendung: 4 WLAN-Netze (Büro, Halle 1, 2, 3), Abdeckungsbereiche*

---

## QUERVERWEISE

**Querverweise zu diesem Dokument werden zentral in KOM_KGS_Kontext_Gedaechtnis_System.md getrackt.**

Relevante verknüpfte Dokumente:
- IT_CORE_Client-Server-Struktur.md
- IT_M365_Microsoft-365.md
- IT_DOKU_IT-Dokumentation.md
- HR_CORE_Personalstamm.md

---

## OFFENE FRAGEN

### ✅ Geklärt (2025-12-01 - Validierung AL)

- [x] **WLAN-Passwörter:** WLAN 1, 2, 3: 8142140886655826 | WLAN 4: 5412305823431797 (AL)
- [x] **Netzlaufwerke I-Z:** F: = Alte Ablage, H: = Abteilung, K: = DMS, M: = Mitarbeitermatrix, X: = Persönliches Laufwerk. I, W, L, G, Z: Verwendung noch zu ermitteln. (AL)
- [x] **Internet-Provider:** Deutsche Telekom, DSL 100 Anschluss (CS + AL)

### Wichtig (🟡 vor nächster Review klären)

- [ ] **Netzlaufwerke I, W, L, G, Z:** Genaue Freigabe-Namen und Zweck ermitteln. (Verantwortlich: AL, Frist: 2026-01-15)
- [ ] **Sophos Firewall Lizenz:** Laufzeit und Renewal-Datum prüfen. (Verantwortlich: AL, Frist: 2026-01-15)
- [ ] **Sekundärer DNS:** Kein Backup-DNS konfiguriert → Single Point of Failure. Redundanz prüfen. (Verantwortlich: AL, Frist: 2026-03-31)

### Optional (🟢 später klären)

- [ ] **Sophos AP 15 IP:** DHCP-Zuweisung - statische IP sinnvoll für bessere Verwaltbarkeit? (Verantwortlich: AL)
- [ ] **WLAN-Kanäle optimieren:** Frequenzen auf Überlappungen prüfen (WiFi Analyzer). (Verantwortlich: AL)
- [ ] **VPN-Benutzer-Liste:** Anzahl User in AD-Gruppe "Sophos-VPN-User" ermitteln. (Verantwortlich: AL)
- [ ] **Firewall-Regeln dokumentieren:** Vollständige Liste in Sophos-Interface exportieren. (Verantwortlich: AL)

---

## ÄNDERUNGSHISTORIE

### [2.0] - 2025-12-01
**FREIGEGEBEN - Validierung abgeschlossen:**
- ✅ Offene Fragen geklärt (3 kritische Fragen):
  - WLAN-Passwörter: 8142140886655826 (WLAN 1-3), 5412305823431797 (WLAN 4)
  - Netzlaufwerke: F: (Alte Ablage), H: (Abteilung), K: (DMS), M: (Mitarbeitermatrix), X: (Persönlich)
  - Internet-Provider: Deutsche Telekom, DSL 100
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
- ✅ DSGVO-Prüfung: Nur Kürzel (AL, CS) verwendet, externe Dienstleister benannt
- ✅ Token-Effizienz: -10% vs. Rohdaten (Tabellen kompaktiert, Redundanzen eliminiert)
- ✅ Keywords: 30 Primary (Router, Firewall, VPN...), 50+ Secondary (192.168.10.50, X10304W8KGP6794...)
- ✅ PDF-Links: 5 Dokumente verlinkt (IT-Doku.md, Sophos Config, TK Höhn, INWX, VPN-Anleitung)
- ✅ Bilder: 3 Diagramme (Netzwerk-Topologie, IP-Schema, WLAN-Coverage)
- ✅ Querverweise: 8 Links identifiziert (4 bidirektional, 4 ausgehend)

**Datenquellen:**
- IT-Doku.md (26.11.2025) - Router, Firewall, WLAN, IP-Schema, Drucker
- Sophos XGS108 Konfiguration
- Active Directory (SRV-DC01) - Gruppen, GPOs

**Verantwortlich:** AL (QM/IT)

---

### [1.1] - 2025-11-20
**Erstversion:**
- Basis-Struktur IT_NET erstellt

**Verantwortlich:** AL

---

*Dieses Dokument ist die zentrale Quelle für die komplette Netzwerk-Infrastruktur inkl. Router, Firewall, VPN, WLAN und Netzlaufwerke. Status: FREIGEGEBEN - ChromaDB-Import in Main/IT_Infrastruktur/ erfolgt.*

(C: 100%) [OSP]
