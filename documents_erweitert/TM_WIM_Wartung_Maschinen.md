# [TM][WIM] Wartung und Instandhaltung Maschinen

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 1.1 | **TAG:** [TM][WIM] | **Erstellt:** 2025-12-16 | **Aktualisiert:** 2025-12-16 | **Autor:** AL  
**Verantwortlich:** MD (Technik) | **Cluster:** 🟢 C4-Support | **Zugriff:** 🟡 L2-Abteilung | **Status:** ✅ PRODUKTIV

---

## ÄNDERUNGSHISTORIE

| Version | Datum | Änderung | Autor |
|---------|-------|----------|-------|
| 1.1 | 2025-12-16 | CSV-Integration: Statuszeilen für alle Maschinen hinzugefügt | AL |
| 1.0 | 2025-12-16 | Initiale Erstellung mit Wartungshistorie-Struktur | AL |

---

## ZWECK

Wartungshistorie aller Produktionsmaschinen (Inv-Nr) mit Verknüpfung zu SharePoint-Dokumenten.
Ergänzt `TM_CORE_Maschinen_Anlagen.md` um historische Wartungsberichte und Protokolle.

**Statuszeilen-Format:**
- **Status:** Bemerkung/Zustand der Maschine
- **WRT:** Wartungsrhythmus (J=jährlich, H=halbjährlich, Q=vierteljährlich)
- **Ltz.WRT:** Datum der letzten Wartung

**Berichtstypen:**
- **WRT** = Interne Wartung (F-QM-37)
- **SVC** = Externer Service (Hersteller/Fremdfirma)
- **REP** = Reparaturbericht
- **MB** = Montagebericht (z.B. Komax IBN)

---

## URL-RESOLVER

**SP-BASIS:** `https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene%20Dokumente/Wartung_Instandhaltung/`

| Präfix | Auflösung |
|--------|-----------|
| `WRT:` | `{SP-BASIS}Wartungsberichte/F-QM-37_` |
| `REP:` | `{SP-BASIS}Reparaturberichte/` |
| `SVC:` | `{SP-BASIS}Serviceberichte/Fa.%20` |

**Hinweis:** Zur Nutzung der Links muss das Präfix durch die SP-BASIS-URL ersetzt werden.

---

## WARTUNGSINTERVALL-CODES (WRT)

| Code | Intervall | Beschreibung |
|------|-----------|--------------|
| **Q** | vierteljährlich | Code 1 - Hochfrequente Wartung |
| **H** | halbjährlich | Code 2 - z.B. Kompaktierungsmaschinen, WDT-Pressen |
| **J** | jährlich | Code 3 - Standard für die meisten Maschinen |
| **2J** | alle 2 Jahre | Code 4 - Selten |
| **5J** | alle 5 Jahre | Code 5 - Druckbehälter (innere Prüfung) |
| **10J** | alle 10 Jahre | Code 10 - Druckbehälter (Festigkeitsprüfung) |
| **W** | bei Wiederaufnahme | Eingelagerte Geräte |
| **-** | keine | Einfachgeräte ohne Wartungspflicht |

---

## STATISTIK

| Kategorie | Anzahl |
|-----------|--------|
| Maschinen gesamt | 124 |
| Fremdgeräte (WKZ/KAM) | 8 |
| Mit Wartung (WRT ≠ -) | 127 |
| Ohne Wartung | 5 |

---

# MASCHINEN WARTUNGSHISTORIE

## EIGENE MASCHINEN

## 0005

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 24.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 24.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0005) |

---
## 0013

**Status:** Innere Prüfung 5J; Festigkeit 10J | **WRT:** 5J (alle 5 Jahre) | **Ltz.WRT:** 10.01.2023

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 10.01.2023 | 5-Jahres-Prüfung | Innere Prüfung 5J; Festigkeit 10J | [📄 PDF](WRT:0013) |

---
## 0018

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 02.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0018) |

---
## 0019

**Status:** Innere Prüfung 5J; Festigkeit 10J | **WRT:** 5J (alle 5 Jahre) | **Ltz.WRT:** 10.01.2023

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 10.01.2023 | 5-Jahres-Prüfung | Innere Prüfung 5J; Festigkeit 10J | [📄 PDF](WRT:0019) |

---
## 0026

**Status:** Aktiv | **WRT:** - | **Ltz.WRT:** -

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| - | - | Keine Wartungshistorie verfügbar | - |

---
## 0028

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 30.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 30.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0028) |

---
## 0029

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 30.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 30.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0029) |

---
## 0030

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 30.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 30.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0030) |

---
## 0031

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 01.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 01.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0031) |

---
## 0032

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 03.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0032) |

---
## 0091

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 04.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 04.09.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0091) |

---
## 0092

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 03.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.07.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0092) |

---
## 0110

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 25.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0110) |

---
## 0118

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 02.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0118) |

---
## 0122

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 30.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 30.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0122) |

---
## 0141

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 30.05.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 30.05.2025 | Jahreswartung | - | [📄 PDF](WRT:0141) |

---
## 0142

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 26.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 26.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0142) |

---
## 0172

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 10.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 10.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0172) |

---
## 0173

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0173) |

---
## 0198

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0198) |

---
## 0201

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 10.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 10.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0201) |

---
## 0250

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 30.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 30.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0250) |

---
## 0251

**Status:** 🔧 Wartung: Fa. Nowak | **WRT:** J (jährlich) | **Ltz.WRT:** 26.02.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 26.02.2025 | Jahreswartung | Wartung: Fa. Nowak | [📄 PDF](WRT:0251) |

---
## 0252

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 25.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0252) |

---
## 0256

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 26.08.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 26.08.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0256) |

---
## 0266

**Status:** 🔧 Wartung: Fa. Hänel | **WRT:** J (jährlich) | **Ltz.WRT:** 23.01.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 23.01.2025 | Jahreswartung | Wartung: Fa. Hänel | [📄 PDF](WRT:0266) |

---
## 0267

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 27.11.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 27.11.2025 | Jahreswartung | - | [📄 PDF](WRT:0267) |

---
## 0270

**Status:** 📦 Eingelagert | **WRT:** W (bei Wiederaufnahme) | **Ltz.WRT:** -

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| - | - | Keine Wartungshistorie verfügbar | - |

---
## 0271

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 25.08.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.08.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0271) |

---
## 0281

**Status:** Rep. 12.12.2024 | **WRT:** J (jährlich) | **Ltz.WRT:** 08.01.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.01.2025 | Jahreswartung | Rep. 12.12.2024 | [📄 PDF](WRT:0281) |

---
## 0282

**Status:** Aktiv | **WRT:** - | **Ltz.WRT:** -

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| - | - | Keine Wartungshistorie verfügbar | - |

---
## 0287

**Status:** 🔧 Wartung: Fa. Hänel | **WRT:** J (jährlich) | **Ltz.WRT:** 23.01.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 23.01.2025 | Jahreswartung | Wartung: Fa. Hänel | [📄 PDF](WRT:0287) |

---
## 0292

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 17.12.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 17.12.2024 | Jahreswartung | - | [📄 PDF](WRT:0292) |

---
## 0295

**Status:** 🔧 Wartung: Komax/Schirk | **WRT:** J (jährlich) | **Ltz.WRT:** 17.11.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 17.11.2025 | Jahreswartung | Wartung: Komax/Schirk | [📄 PDF](WRT:0295) |

---
## 0297

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 02.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0297) |

---
## 0298

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 10.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 10.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0298) |

---
## 0299

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 02.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.06.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0299) |

---
## 0300

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0300) |

---
## 0302

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 03.06.2026

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.06.2026 | Jahreswartung | - | [📄 PDF](WRT:0302) |

---
## 0303

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0303) |

---
## 0304

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 30.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 30.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0304) |

---
## 0309

**Status:** Aktiv | **WRT:** - | **Ltz.WRT:** -

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| - | - | Keine Wartungshistorie verfügbar | - |

---
## 0315

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 27.11.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 27.11.2025 | Jahreswartung | - | [📄 PDF](WRT:0315) |

---
## 0317

**Status:** 🔧 Wartung: Fa. Domino | **WRT:** J (jährlich) | **Ltz.WRT:** 19.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 19.09.2025 | Jahreswartung | Wartung: Fa. Domino | [📄 PDF](WRT:0317) |

---
## 0318

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0318) |

---
## 0319

**Status:** 🔧 Wartung: Fa. Nowak; Behälterprüfung alle 5/10 Jahre | **WRT:** J (jährlich) | **Ltz.WRT:** 02.10.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.10.2025 | Jahreswartung | Wartung: Fa. Nowak; Behälterprüfung alle 5/10 Jahre | [📄 PDF](WRT:0319) |

---
## 0320

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2026

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2026 | Jahreswartung | - | [📄 PDF](WRT:0320) |

---
## 0321

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 03.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0321) |

---
## 0322

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0322) |

---
## 0323

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 01.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 01.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0323) |

---
## 0324

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 02.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.07.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0324) |

---
## 0325

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 05.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 05.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0325) |

---
## 0326

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 28.10.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 28.10.2024 | Jahreswartung | - | [📄 PDF](WRT:0326) |

---
## 0329

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 27.11.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 27.11.2025 | Jahreswartung | - | [📄 PDF](WRT:0329) |

---
## 0330

**Status:** 🔧 Wartung: Fa. Nowak | **WRT:** J (jährlich) | **Ltz.WRT:** 26.02.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 26.02.2025 | Jahreswartung | Wartung: Fa. Nowak | [📄 PDF](WRT:0330) |

---
## 0331

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 07.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 07.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0331) |

---
## 0333

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 14.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 14.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0333) |

---
## 0338

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 05.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 05.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0338) |

---
## 0341

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 15.12.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 15.12.2025 | Jahreswartung | - | [📄 PDF](WRT:0341) |

---
## 0342

**Status:** 🔧 Wartung: Fa. Hänel | **WRT:** J (jährlich) | **Ltz.WRT:** 23.01.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 23.01.2025 | Jahreswartung | Wartung: Fa. Hänel | [📄 PDF](WRT:0342) |

---
## 0346

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 01.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 01.07.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0346) |

---
## 0347

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 09.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 09.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0347) |

---
## 0349

**Status:** Eigene + Komax-Wartung | **WRT:** J (jährlich) | **Ltz.WRT:** 09.12.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 09.12.2025 | Jahreswartung | Eigene + Komax-Wartung | [📄 PDF](WRT:0349) |

---
## 0350

**Status:** Eigene + Komax-Wartung | **WRT:** J (jährlich) | **Ltz.WRT:** 16.12.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 16.12.2025 | Jahreswartung | Eigene + Komax-Wartung | [📄 PDF](WRT:0350) |

---
## 0351

**Status:** 🔧 Wartung: Komax/Schirk | **WRT:** H (halbjährlich) | **Ltz.WRT:** 17.11.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 17.11.2025 | Halbjahreswartung | Wartung: Komax/Schirk | [📄 PDF](WRT:0351) |

---
## 0352

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 18.12.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 18.12.2024 | Jahreswartung | - | [📄 PDF](WRT:0352) |

---
## 0353

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 09.01.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 09.01.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0353) |

---
## 0354

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 15.12.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 15.12.2025 | Jahreswartung | - | [📄 PDF](WRT:0354) |

---
## 0355

**Status:** 🔧 Wartung: Fa. Domino | **WRT:** J (jährlich) | **Ltz.WRT:** 19.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 19.09.2025 | Jahreswartung | Wartung: Fa. Domino | [📄 PDF](WRT:0355) |

---
## 0356

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 16.12.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 16.12.2024 | Jahreswartung | - | [📄 PDF](WRT:0356) |

---
## 0357

**Status:** Vorfilter: 20.01.2026 | **WRT:** J (jährlich) | **Ltz.WRT:** 20.10.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 20.10.2025 | Jahreswartung | Vorfilter: 20.01.2026 | [📄 PDF](WRT:0357) |

---
## 0358

**Status:** Vorfilter: 03.03.2026 | **WRT:** J (jährlich) | **Ltz.WRT:** 03.12.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.12.2025 | Jahreswartung | Vorfilter: 03.03.2026 | [📄 PDF](WRT:0358) |

---
## 0359

**Status:** Vorfilter: 03.10.2025 | **WRT:** J (jährlich) | **Ltz.WRT:** 02.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.07.2025 | Jahreswartung | Vorfilter: 03.10.2025 | [📄 PDF](WRT:0359) |

---
## 0362

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 04.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 04.07.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0362) |

---
## 0363

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 04.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 04.07.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0363) |

---
## 0364

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 30.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 30.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0364) |

---
## 0365

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 04.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 04.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0365) |

---
## 0366

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 07.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 07.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0366) |

---
## 0367

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 29.08.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 29.08.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0367) |

---
## 0368

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 07.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 07.07.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0368) |

---
## 0369

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 04.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 04.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0369) |

---
## 0370

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 14.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 14.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0370) |

---
## 0371

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 25.08.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.08.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0371) |

---
## 0372

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 24.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 24.06.2025 | Jahreswartung | - | [📄 PDF](WRT:0372) |

---
## 0373

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 25.08.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.08.2025 | Jahreswartung | - | [📄 PDF](WRT:0373) |

---
## 0374

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 02.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0374) |

---
## 0375

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 19.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 19.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0375) |

---
## 0376

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 28.02.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 28.02.2025 | Jahreswartung | - | [📄 PDF](WRT:0376) |

---
## 0377

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 03.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0377) |

---
## 0378

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 03.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0378) |

---
## 0381

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0381) |

---
## 0382

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 18.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 18.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0382) |

---
## 0383

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 03.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0383) |

---
## 0384

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 25.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0384) |

---
## 0385

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 02.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0385) |

---
## 0386

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | - | [📄 PDF](WRT:0386) |

---
## 0389

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 08.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0389) |

---
## 0390

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 25.08.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.08.2025 | Jahreswartung | - | [📄 PDF](WRT:0390) |

---
## 0391

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 25.08.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.08.2025 | Jahreswartung | - | [📄 PDF](WRT:0391) |

---
## 0392

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 07.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 07.07.2025 | Jahreswartung | - | [📄 PDF](WRT:0392) |

---
## 0394

**Status:** Eigene Wartung ab Herbst 2024 | **WRT:** J (jährlich) | **Ltz.WRT:** 08.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.11.2024 | Jahreswartung | Eigene Wartung ab Herbst 2024 | [📄 PDF](WRT:0394) |

---
## 0396

**Status:** Rep. 28.02.2023 | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | Rep. 28.02.2023 | [📄 PDF](WRT:0396) |

---
## 0397

**Status:** IBN: 09.03.2021 | **WRT:** H (halbjährlich) | **Ltz.WRT:** 04.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 04.07.2025 | Halbjahreswartung | IBN: 09.03.2021 | [📄 PDF](WRT:0397) |

---
## 0398

**Status:** IBN: 23.04.2021 | **WRT:** H (halbjährlich) | **Ltz.WRT:** 04.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 04.07.2025 | Halbjahreswartung | IBN: 23.04.2021 | [📄 PDF](WRT:0398) |

---
## 0399

**Status:** IBN: 04.05.2021 | **WRT:** J (jährlich) | **Ltz.WRT:** 02.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 02.09.2025 | Jahreswartung | IBN: 04.05.2021 | [📄 PDF](WRT:0399) |

---
## 0400

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0400) |

---
## 0407

**Status:** IBN: 02.12.2021 | **WRT:** J (jährlich) | **Ltz.WRT:** 23.06.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 23.06.2025 | Jahreswartung | IBN: 02.12.2021 | [📄 PDF](WRT:0407) |

---
## 0408

**Status:** IBN: 02.12.2021 | **WRT:** J (jährlich) | **Ltz.WRT:** 29.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 29.11.2024 | Jahreswartung | IBN: 02.12.2021 | [📄 PDF](WRT:0408) |

---
## 0410

**Status:** IBN: 14.12.2021 | **WRT:** J (jährlich) | **Ltz.WRT:** 29.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 29.11.2024 | Jahreswartung | IBN: 14.12.2021 | [📄 PDF](WRT:0410) |

---
## 0412

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0412) |

---
## 0413

**Status:** IBN: 23.02.2022 | **WRT:** H (halbjährlich) | **Ltz.WRT:** 07.07.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 07.07.2025 | Halbjahreswartung | IBN: 23.02.2022 | [📄 PDF](WRT:0413) |

---
## 0414

**Status:** Aktiv | **WRT:** - | **Ltz.WRT:** -

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| - | - | Keine Wartungshistorie verfügbar | - |

---
## 0415

**Status:** IBN: 22.08.2022 | **WRT:** J (jährlich) | **Ltz.WRT:** 12.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 12.09.2025 | Jahreswartung | IBN: 22.08.2022 | [📄 PDF](WRT:0415) |

---
## 0416

**Status:** Ersatzteilträger | **WRT:** - | **Ltz.WRT:** -

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| - | - | Keine Wartungshistorie verfügbar | - |

---
## 0417

**Status:** Aktiv | **WRT:** H (halbjährlich) | **Ltz.WRT:** 25.08.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 25.08.2025 | Halbjahreswartung | - | [📄 PDF](WRT:0417) |

---
## 0419

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 11.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 11.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0419) |

---
## 0420

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 11.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 11.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0420) |

---
## 0421

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 11.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 11.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0421) |

---
## 0422

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 11.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 11.11.2024 | Jahreswartung | - | [📄 PDF](WRT:0422) |

---
## 0423

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 16.12.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 16.12.2024 | Jahreswartung | - | [📄 PDF](WRT:0423) |

---
## 0424

**Status:** Aktiv | **WRT:** J (jährlich) | **Ltz.WRT:** 16.12.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 16.12.2024 | Jahreswartung | - | [📄 PDF](WRT:0424) |

---
## 0425

**Status:** IBN: 11/2024 | **WRT:** J (jährlich) | **Ltz.WRT:** 01.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 01.11.2024 | Jahreswartung | IBN: 11/2024 | [📄 PDF](WRT:0425) |

---
## 0427

**Status:** IBN: 09/2025 | **WRT:** J (jährlich) | **Ltz.WRT:** -

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| - | - | Keine Wartungshistorie verfügbar | - |

---
## 0428

**Status:** IBN: 09/2025 | **WRT:** H (halbjährlich) | **Ltz.WRT:** -

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| - | - | Keine Wartungshistorie verfügbar | - |

---

---

## FREMDGERÄTE (KUNDENEIGENTUM)

**Hinweis:** Fremdgeräte haben WKZ-Nr. oder Kunden-Kennung als Hauptkennung.

## KAM 836-2

**Status:** Fa. BBT | **WRT:** J (jährlich) | **Ltz.WRT:** 11.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 11.11.2024 | Jahreswartung | Fa. BBT | [📄 PDF](WRT:KAM 836-2) |

---
## WKZ 601/01

**Status:** Fa. Siemens | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | Fa. Siemens | [📄 PDF](WRT:WKZ 601/01) |

---
## WKZ 601/02

**Status:** Fa. Siemens | **WRT:** J (jährlich) | **Ltz.WRT:** 03.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 03.09.2025 | Jahreswartung | Fa. Siemens | [📄 PDF](WRT:WKZ 601/02) |

---
## WKZ 602/01

**Status:** Fa. Siemens | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2024 | Jahreswartung | Fa. Siemens | [📄 PDF](WRT:WKZ 602/01) |

---
## WKZ 603/01

**Status:** Fa. Siemens | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | Fa. Siemens | [📄 PDF](WRT:WKZ 603/01) |

---
## WKZ 604/01

**Status:** Fa. Siemens | **WRT:** J (jährlich) | **Ltz.WRT:** 08.09.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 08.09.2025 | Jahreswartung | Fa. Siemens | [📄 PDF](WRT:WKZ 604/01) |

---
## WKZ 605/01

**Status:** Fa. Siemens | **WRT:** J (jährlich) | **Ltz.WRT:** 12.11.2024

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 12.11.2024 | Jahreswartung | Fa. Siemens | [📄 PDF](WRT:WKZ 605/01) |

---
## WKZ 606/01

**Status:** Fa. Siemens | **WRT:** J (jährlich) | **Ltz.WRT:** 15.10.2025

### Wartungshistorie

| Datum | Art | Bemerkung | Dokument |
|-------|-----|-----------|----------|
| 15.10.2025 | Jahreswartung | Fa. Siemens | [📄 PDF](WRT:WKZ 606/01) |

---

---

## QUERVERWEISE

| Dokument | Bezug |
|----------|-------|
| `TM_CORE_Maschinen_Anlagen.md` | Stammdaten (Inv-Nr, Typ, Hersteller, Standort) |
| `QM_PMV_Pruefmittelverwaltung.md` | Prüfmittel und Kalibrierung |
| `TM_EIN_Einlagerung.md` | Eingelagerte Geräte |
| `TM_FUHR_Fuhrpark.md` | Fuhrpark und Stapler |

---

## TECHNISCHE HINWEISE

⚠️ **RAG-OPTIMIERUNG:** 
- Jeder Maschinen-Abschnitt enthält vollständige Statusinformationen für Chunking-Unabhängigkeit
- Statuszeilen ermöglichen direkte Antworten ohne Kontext-Verlust
- Wartungshistorie-Tabellen sind je Maschine abgeschlossen

**Generiert:** 2025-12-16 20:01:42

---

[OSP]
