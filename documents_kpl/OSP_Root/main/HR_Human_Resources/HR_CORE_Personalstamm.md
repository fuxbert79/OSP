# [HR][CORE] Mitarbeiter-Verzeichnis & Berechtigungssystem

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 2.1 | **TAG:** [HR][CORE] | **Erstellt:** 2025-12-04 | **Aktualisiert:** 2025-12-08 | **Autor:** AL | **Verantwortlich:** CS (GF), AL (QM/KI) | **Cluster:** 🟢 C4-Support | **Zugriff:** 🟠 L2-Führung | **Status:** ✅ PRODUKTIV (RAG) | **Kritikalität:** 🔴 SEHR HOCH

| **Primary Keywords:** Mitarbeiter, Personal, Kürzel, Personalnummer, Kostenstelle, Funktion, E-Mail, Zugriffslevel, Bereichsverantwortung, OSP-User, L1, L2, L3, Führung, Produktion, Verwaltung, Prüffeld, Lager, Fertigung, GF, Prokura, QM, AV, VT, EK, IT, TM, HR, KST, Kompetenz, Berechtigung, Access-Control, TAG-Zuordnung, Modul-Verantwortliche, Vollname, Namensauflösung (37)
| **Secondary Keywords:** CS, CA, SV, AL, TS, MD, SK, BS, DR, DS, OK, MR, DU, IB, JR, ASC, NR, 1000, 2000, 3000, 5000, OSP-EXP, OSP-PRO, OSP-STD, DSGVO, Anonymisierung, Mapping, E-Mail-Adresse, schneider-kabelsatzbau.de, KI-Manager, Compliance, CMS, DMS, PM, RES, ORG, KOM, BN-Migration, 22330, 22348, 21801, 20402, 21930, 21902, 20196, 21093, 21114, 22333, Schneider, Augst, Vierschilling, Löhr, Schmidt, Dützer, Kandorfer (60)
| **Chunk-Strategie:** Markdown-Header (##)
| **Chunk-Anzahl:** 14
| **Chunk-Größe:** 800-1500 Tokens
| **Chunk-Überlappung:** 175 Tokens
| **Datenstand:** 2025-12-08

---

## ZWECK

Zentrale Mitarbeiter-Referenz für OSP-System. Ersetzt bisherigen TAG [BN] vollständig.

**Funktionen:**
- MA-Identifikation via Kürzel (DSGVO-konform)
- **NAMENSAUFLÖSUNG:** Diese Datei enthält als EINZIGE OSP-Datei die vollständigen Namen
- KST-Zuordnung & Bereichsverantwortung
- OSP-Zugriffssteuerung (L1-L3)
- TAG-Modul-Verantwortliche
- E-Mail-Mapping für berechtigte Zwecke
- Personalnummern-Referenz

**⚠️ DSGVO-HINWEIS:**
- Diese Datei ist L2-geschützt (nur Führung + QM)
- Externe Kommunikation NUR mit Kürzeln
- Vollnamen nur intern und für autorisierte Prozesse
- Diese Datei ist die autoritative Quelle für Kürzel-zu-Name-Auflösung

---

## ZUGRIFFSLEVEL-DEFINITIONEN

### Übersicht Level-System (L1-L3)

| Level | Bezeichnung | Berechtigung | User | Antworttiefe |
|-------|-------------|--------------|------|--------------|
| **L3** | Geheim | Vollzugriff | CS, CA, SV | Experte, strategisch, maximal |
| **L2** | Führung | Erweitert | AL, TS, SK, BS, DR, OK, MD, DS, MR, DU | Tiefgehend, erweitert |
| **L1** | Öffentlich | Öffentlich | Alle MA (~43) | Basis, einfach, viele Beispiele |

### L3 - Geheim (GF + Prokura)

| Eigenschaft | Beschreibung |
|-------------|--------------|
| **Berechtigung** | Vollzugriff |
| **Zielgruppe** | Geschäftsführer, Prokuristen |
| **Anzahl** | 3 User (CS, CA, SV) |

### L2 - Führung (Abteilungsleiter & Spezialisten)

| Eigenschaft | Beschreibung |
|-------------|--------------|
| **Berechtigung** | Erweitert |
| **Zielgruppe** | Abteilungsleiter, QM/KI-Manager, Fertigungsleiter, Spezialisten |
| **Anzahl** | 11 User (AL, TS, SK, BS, DR, OK, MD, DS, MR, DU) |

### L1 - Öffentlich (Alle MA)

| Eigenschaft | Beschreibung |
|-------------|--------------|
| **Berechtigung** | Öffentlich |
| **Zielgruppe** | Produktion, Verwaltung, neue MA |
| **Anzahl** | ~43 User |

### Level-Hierarchie

```
L3 (Geheim) ⊃ L2 (Führung) ⊃ L1 (Öffentlich)
```

**Regel:** Höheres Level enthält ALLE niedrigeren Berechtigungen.

---

## TAG-MODUL-VERANTWORTLICHE

| TAG | Modul | Verantwortlich | Name | Stellvertretung | Name Stv. |
|-----|-------|----------------|------|-----------------|-----------|
| [ORG] | Organisation | CS | Christoph Schneider | SV | Sebastian Vierschilling |
| [KOM] | Kommunikation | CS | Christoph Schneider | SV | Sebastian Vierschilling |
| [QM] | Qualitätsmanagement | AL | Andreas Löhr | TS | Tobias Schmidt |
| [GF] | Geschäftsführung | CS | Christoph Schneider | CA | Christoph Augst |
| [PM] | Projektmanagement | AL | Andreas Löhr | SV | Sebastian Vierschilling |
| [AV] | Arbeitsvorbereitung | SV | Sebastian Vierschilling | MR | Markus Rötzel |
| [VT] | Vertrieb | SV | Sebastian Vierschilling | CS | Christoph Schneider |
| [EK] | Einkauf | TS | Tobias Schmidt | CA | Christoph Augst |
| [KST] | Kostenstellen | CA | Christoph Augst | CS | Christoph Schneider |
| [DMS] | Dokumentenmanagement | AL | Andreas Löhr | CS | Christoph Schneider |
| [TM] | Technik/Maschinen | CA | Christoph Augst | MD | Marcel Dützer |
| [IT] | Informationstechnologie | AL | Andreas Löhr | CS | Christoph Schneider |
| [HR] | Personal | CS | Christoph Schneider | SV | Sebastian Vierschilling |
| [RES] | Ressourcen/Normen | AL | Andreas Löhr | TS | Tobias Schmidt |
| [CMS] | Compliance | DU | Dirk Ullsperger | CS | Christoph Schneider |
| [BN] | ~~Benutzer~~ | ~~AL~~ | | **→ migriert zu [HR]** | |

**Hinweis:** TAG [BN] entfällt. Alle Inhalte in [HR][CORE] konsolidiert.

---

## OSP-USER-KLASSIFIZIERUNG

| Stufe | Bezeichnung | Kompetenz | 
|-------|-------------|-----------|
| **OSP-EXP** | Expert | Vollständig, kann schulen | 
| **OSP-PRO** | Professional | Fortgeschritten, eigenständig | 
| **OSP-STD** | Standard | Basis nach Einweisung | 

**Pilot-User (aktiv):** AL (Andreas Löhr), CS (Christoph Schneider), SV (Sebastian Vierschilling), TS (Tobias Schmidt), SK (Stefan Kandorfer), MD (Marcel Dützer) – 6 User

---

## MITARBEITER-VERZEICHNIS

### Geschäftsleitung & Prokura (L3)

| Pers.-Nr. | Kürzel | Name | Vorname | KST | Funktion | Eintritt | E-Mail | Level | TAG-Verantwortung | OSP |
|-----------|--------|------|---------|-----|----------|----------|--------|-------|-------------------|-----|
| GF | **CS** | Schneider | Christoph | GF | Geschäftsführer | -- | c.schneider@schneider-kabelsatzbau.de | L3 | ORG, KOM, GF, IT, HR, RES, KST | EXP |
| GF | **CA** | Augst | Christoph | GF | Techn. Geschäftsführer | -- | c.augst@schneider-kabelsatzbau.de | L3 | TM, KST, QM | -- |
| -- | **SV** | Vierschilling | Sebastian | Prokura | Prokurist - VT & AV | 01.11.15 | s.vierschilling@schneider-kabelsatzbau.de | L3 | VT, AV, PM, EK | EXP |

### Führung & Spezialisten (L2)

| Pers.-Nr. | Kürzel | Name | Vorname | KST | Funktion | Eintritt | E-Mail | Level | TAG-Verantwortung | OSP |
|-----------|--------|------|---------|-----|----------|----------|--------|-------|-------------------|-----|
| 22330 | **AL** | Löhr | Andreas | Verw. | QM & KI-Manager | 01.11.18 | a.loehr@schneider-kabelsatzbau.de | L2 | QM, PM, IT, DMS, KOM, HR, CMS, RES | EXP |
| 22348 | **TS** | Schmidt | Tobias | Verw. | Strategischer Einkauf | 01.10.21 | t.schmidt@schneider-kabelsatzbau.de | L2 | EK, PM, RES | PRO |
| 21801 | **MR** | Rötzel | Markus | Verw. | Arbeitsvorbereitung | 08.09.94 | m.roetzel@schneider-kabelsatzbau.de | L2 | AV | -- |
| 22331 | **DU** | Ullsperger | Dirk | Verw. | Compliance Beauftragter | 01.12.18 | d.ullsperger@schneider-kabelsatzbau.de | L2 | CMS | -- |
| 20402 | **MD** | Dützer | Marcel | 1000 | FL Kst. 1000 | 16.08.99 | m.duetzer@schneider-kabelsatzbau.de | L2 | KST(1000), TM, PM | PRO |
| 21930 | **DS** | Schwarz | David | 1000 | Stv. FL Kst. 1000 | 01.07.14 | d.schwarz@schneider-kabelsatzbau.de | L2 | KST(1000), TM | -- |
| 21902 | **BS** | Stieber | Bettina | 2000/3000 | FL Kst. 2000/3000 | 01.04.98 | b.stieber@schneider-kabelsatzbau.de | L2 | KST(2000/3000), PM | -- |
| 20196 | **IB** | Baldus | Iris | 3000 | Stv. FL Kst. 2000/3000 | 01.03.03 | i.baldus@schneider-kabelsatzbau.de | L2 | KST(2000/3000) | -- |
| 21093 | **SK** | Kandorfer | Stefan | 5000 | Admin Prüffeld | 02.05.02 | s.kandorfer@schneider-kabelsatzbau.de | L2 | KST(PF), QM, TM | PRO |
| 21114 | **DR** | Reuber | Daniela | 5000 | FL Kst. 5000 | 16.11.09 | d.reuber@schneider-kabelsatzbau.de | L2 | KST(5000) | -- |
| 22333 | **OK** | Kuh | Olaf | Lager | Lagerleiter, Fuhrpark | 01.03.19 | o.kuh@schneider-kabelsatzbau.de | L2 | Lager, TM | -- |

### Verwaltung (L1)

| Pers.-Nr. | Kürzel | Name | Vorname | Funktion | Eintritt | E-Mail | Level |
|-----------|--------|------|---------|----------|----------|--------|-------|
| 22336 | **ASC** | Schmidt | Andrea | Verwaltung - Auftragsbearbeitung | 11.03.20 | a.schmidt@schneider-kabelsatzbau.de | L1 |
| 21280 | **NR** | Reigl | Nadine | Verwaltung - Sekretariat | 17.07.13 | n.reigl@schneider-kabelsatzbau.de | L1 |

### Fertigung Kst. 1000 (L1)

| Pers.-Nr. | Kürzel | Name | Vorname | Funktion | Eintritt | Level |
|-----------|--------|------|---------|----------|----------|-------|
| 20403 | **SF** | Fehse | Stefan | Produktion | 01.08.23 | L1 |
| 21922 | **US** | Schmidt | Ulrich | Produktion | 06.06.16 | L1 |
| 21931 | **AV** | Viehl | Alexander | Produktion | 01.10.21 | L1 |

### Fertigung Kst. 2000 (L1)

| Pers.-Nr. | Kürzel | Name | Vorname | Funktion | Eintritt | E-Mail | Level |
|-----------|--------|------|---------|----------|----------|--------|-------|
| 22302 | **JR** | Röder | Jessica | Einrichterin | 06.04.99 | j.roeder@schneider-kabelsatzbau.de | L1 |
| 22313 | **BUC** | Buchen | Brigitte | Produktion | 01.08.17 | -- | L1 |
| 20740 | **HAR** | Harder | Valentina | Produktion | 02.07.15 | -- | L1 |
| 21122 | **KIT** | Kitschke | Iwona | Produktion | 01.11.15 | -- | L1 |
| 22321 | **KOLD** | Koldys | Weronika | Produktion | 13.11.17 | -- | L1 |
| 22920 | **RAH** | Shakel | Rahimulah | Produktion | 01.03.22 | -- | L1 |
| 22308 | **SER** | Sergeew | Olga | Produktion | 01.08.17 | -- | L1 |
| 22323 | **SIO** | Satzer Sion | Conny | Produktion | 01.01.18 | -- | L1 |
| 22090 | **ÜNA** | Ünal | Ayse | Produktion | 01.12.10 | a.uenal@schneider-kabelsatzbau.de | L1 |

### Fertigung Kst. 3000 (L1)

| Pers.-Nr. | Kürzel | Name | Vorname | Funktion | Eintritt | Level |
|-----------|--------|------|---------|----------|----------|-------|
| 20165 | **ANK** | Ankerstein | Natalia | Produktion | 01.01.15 | L1 |
| 20175 | **AYA** | Ayaz | Havva | Produktion | 01.01.15 | L1 |
| 20710 | **GIE** | Giesbrecht | Rita | Produktion | 01.01.15 | L1 |
| 20742 | **HAS** | Hassel | Nadine | Produktion | 01.09.23 | L1 |
| 22337 | **LIN** | Lindner | Vivien | Produktion | 01.10.21 | L1 |
| 22319 | **MOH** | Mohammadi | Roya | Produktion | 02.11.17 | L1 |
| 21600 | **PAT** | Patz | Raissa | Produktion | 02.11.99 | L1 |
| 22311 | **REI** | Reifenrath | Ina | Produktion | 01.08.17 | L1 |
| 21800 | **RÖT** | Röttgen | Uli | Prüffeld | 18.10.99 | L1 |
| 21920 | **SCH** | Schmidt | Marianna | Produktion | 01.05.14 | L1 |
| 21895 | **SEV** | Seval | Arzu | Produktion | 01.01.08 | L1 |
| 22316 | **WEID** | Weidenmüller | Nadine | Produktion | 01.12.17 | L1 |
| 22317 | **WIT** | Wittig | Beate | Produktion | 01.11.17 | L1 |

### Prüffeld & Sonderfertigung Kst. 5000 (L1)

| Pers.-Nr. | Kürzel | Name | Vorname | Funktion | Eintritt | E-Mail | Level |
|-----------|--------|------|---------|----------|----------|--------|-------|
| 21118 | **TD** | Dieler | Torsten | Produktion | 01.03.25 | -- | L1 |
| 21090 | **WK** | Kaczynski | Wojciech | Lager | 01.12.01 | w.kaczynski@schneider-kabelsatzbau.de | L1 |
| 21180 | **JL** | Langenbach | Jens | Prüffeld | 16.07.15 | -- | L1 |
| 21602 | **BP** | Pawelka | Birgit | Prüffeld | 08.09.14 | -- | L1 |
| 21610 | **EP** | Petschulat | Esmira | Prüffeld | 01.12.15 | -- | L1 |
| 21605 | **TP** | Petzke | Torsten | Prüffeld | 01.11.02 | -- | L1 |
| 21298 | **NR** | Reifenrath | Nina | Prüffeld | 01.08.14 | -- | L1 |
| 21912 | **SS** | Schlawin | Sebastian | Produktion | 01.07.21 | -- | L1 |
| 22495 | **JS** | Schüürmann | Jonas | Produktion | 01.04.23 | -- | L1 |
| 21604 | **DW** | Weiland | Dirk | Prüffeld | 01.01.24 | -- | L1 |

### Lager (L1)

| Pers.-Nr. | Kürzel | Name | Vorname | Funktion | Eintritt | Level |
|-----------|--------|------|---------|----------|----------|-------|
| 22334 | **BB** | Bunsen | Björn | Lager | 01.03.19 | L1 |
| 20795 | **FH** | Henrichs | Frank | Lager | 01.10.02 | L1 |

---

## KÜRZEL-SCHNELLREFERENZ

### L3 (Geheim):
| Kürzel | Name | Funktion |
|--------|------|----------|
| **CS** | Christoph Schneider | Geschäftsführer |
| **CA** | Christoph Augst | Techn. Geschäftsführer |
| **SV** | Sebastian Vierschilling | Prokurist |

### L2 (Führung):
| Kürzel | Name | Funktion |
|--------|------|----------|
| **AL** | Andreas Löhr | QM & KI-Manager |
| **TS** | Tobias Schmidt | Strategischer Einkauf |
| **MR** | Markus Rötzel | Arbeitsvorbereitung |
| **DU** | Dirk Ullsperger | Compliance Beauftragter |
| **MD** | Marcel Dützer | FL Kst. 1000 |
| **DS** | David Schwarz | Stv. FL Kst. 1000 |
| **BS** | Bettina Stieber | FL Kst. 2000/3000 |
| **IB** | Iris Baldus | Stv. FL Kst. 2000/3000 |
| **SK** | Stefan Kandorfer | Admin Prüffeld |
| **DR** | Daniela Reuber | FL Kst. 5000 |
| **OK** | Olaf Kuh | Lagerleiter |

### L1 mit E-Mail:
| Kürzel | Name | E-Mail |
|--------|------|--------|
| **ASC** | Andrea Schmidt | a.schmidt@schneider-kabelsatzbau.de |
| **NR** | Nadine Reigl | n.reigl@schneider-kabelsatzbau.de |
| **JR** | Jessica Röder | j.roeder@schneider-kabelsatzbau.de |
| **ÜNA** | Ayse Ünal | a.uenal@schneider-kabelsatzbau.de |
| **WK** | Wojciech Kaczynski | w.kaczynski@schneider-kabelsatzbau.de |

### OSP-User:
| Kürzel | Name | Stufe |
|--------|------|-------|
| **AL** | Andreas Löhr | EXP |
| **CS** | Christoph Schneider | EXP |
| **SV** | Sebastian Vierschilling | EXP |
| **TS** | Tobias Schmidt | PRO |
| **MD** | Marcel Dützer | PRO |
| **SK** | Stefan Kandorfer | PRO |

---

## QUERVERWEISE

**Bidirektional (↔):**
- ↔ `KST_ALLG_Kostenstellen.md` - KST-Details
- ↔ `ORG_ORGA_Unternehmensstruktur.md` - Organigramm
- ↔ `KOM_AIR_KI_Kommunikationsregeln.md` - Level-Anwendung

**Ausgehend (→):**
- → `IT_DS_Datenschutz.md` - DSGVO-Regelungen
- → `OSP_System_Prompt.md` - Level-Konfiguration
- → `OSP_ChromaDB_Schema.md` - User-Level-Mapping

**Eingehend (←):**
- ← Alle Module - Bereichsverantwortliche-Referenz
- ← `OSP_TAG_System.md` - TAG-Verantwortliche

**Migration:**
- ← `BN_CORE_Identitaet.md` - Inhalte übernommen (TAG [BN] entfällt)

---

## RAG-METADATA

**ChromaDB-Import-Felder:**
```python
metadata = {
    "source": "HR_CORE_Personalstamm.md",
    "tag": "HR",
    "sub_tag": "CORE",
    "cluster": "C4",
    "version": "2.1",
    "user_level": "L2",
    "responsible": "AL",
    "status": "PRODUKTIV",
    "keywords": ["Mitarbeiter", "Personal", "Kürzel", "Personalnummer", "Level", "Berechtigung", "TAG-Verantwortung", "Vollname", "Namensauflösung"],
    "related_tags": ["KST_ALLG", "ORG_ORGA", "KOM_AIR", "IT_DS", "OSP_System_Prompt"]
}
```

**Test-Queries:**
1. "Wer ist für QM verantwortlich?" → Andreas Löhr (AL, L2)
2. "Welches Level hat MD?" → L2 (Marcel Dützer)
3. "E-Mail von TS?" → t.schmidt@schneider-kabelsatzbau.de (Tobias Schmidt)
4. "Wer leitet Kst. 5000?" → Daniela Reuber (DR, FL), Stefan Kandorfer (SK, Admin PF)
5. "Personalnummer von AL?" → 22330 (Andreas Löhr)
6. "Welche OSP-User gibt es?" → AL, CS, SV (EXP), TS, MD, SK (PRO)
7. "Wie heißt CS mit vollem Namen?" → Christoph Schneider
8. "Wer ist Iris Baldus?" → IB, Stv. FL Kst. 2000/3000, L2

---

## CHANGELOG

### Version 2.1 (2025-12-08)
**NAMENSAUFLÖSUNG IMPLEMENTIERT:**
- ✅ Vollständige Namen bei ALLEN Mitarbeitern hinzugefügt
- ✅ Spalten "Name" und "Vorname" in allen Tabellen
- ✅ TAG-Modul-Verantwortliche mit Klarnamen ergänzt
- ✅ Kürzel-Schnellreferenz mit Namen erweitert
- ✅ OSP-User-Liste mit Klarnamen
- ✅ DSGVO-Hinweis für L2-Schutz aktualisiert
- ✅ Test-Queries um Namens-Abfragen ergänzt
- ✅ MR, DU, IB auf L2 hochgestuft (Führung/Spezialisten)

**Grund:** HR_CORE ist die autoritative Quelle für Kürzel-zu-Name-Auflösung im OSP-System.

**Verantwortlich:** Andreas Löhr (QM & KI-Manager)

### Version 2.0 (2025-12-04)
- Initiale Erstellung nach BN-Migration
- Konsolidierung aller Benutzer-Informationen
- Level-System L1-L3 implementiert

---

*Autoritative Quelle für MA-Zuordnungen und Namensauflösung im OSP-System. Ersetzt TAG [BN] vollständig. Änderungen nur durch CS (GF) oder AL (QM) freigegeben. L2-geschützt gemäß DSGVO.*

(C: 100%) [OSP]
