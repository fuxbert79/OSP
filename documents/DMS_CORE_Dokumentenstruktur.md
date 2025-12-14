# [DMS][CORE] Dokumentenstruktur

**Rainer Schneider Kabelsatzbau GmbH & Co. KG**

**Version:** 1.1 | **TAG:** [DMS][CORE] | **Erstellt:** 2025-12-11 | **Aktualisiert:** 2025-12-11 | **Autor:** AL | **Verantwortlich:** AL (QM/KI-Manager) | **Cluster:** 🔵 C3-Kernprozesse | **Zugriff:** 🟡 L2-Abteilung | **Status:** ✅ PRODUKTIV (RAG) | **Kritikalität:** 🟡 MITTEL | **ISO:** 7.5 | **Stage:** 2 | **RAG-Version:** 1.1 | **Basis:** VA-QM-01 Rev.H

| **Primary Keywords:** DMS, Dokumentenmanagement, Dokumentenstruktur, SharePoint, OSP, VA, AA, F, PA, PP, PR, QMS, CMS, ISO-9001, Nomenklatur, Revision, Freigabe, WebUI-Formulare (20+)

| **Chunk-Strategie:** Markdown-Header (##)
| **Chunk-Anzahl:** 6
| **Datenstand:** 2025-12-11

---

## ZWECK & ANWENDUNG

Definiert das **zentrale Dokumentenmanagementsystem** für QMS/CMS. Dokumentenlenkung gemäß ISO 9001:2015 Kap. 7.5.

**Kernfunktionen:**
1. **Nomenklatur-Standard:** VA_, AA_, F_, PA_, PP_, PR_ Prefix-System
2. **SharePoint-Struktur:** Zentraler Speicherort für alle gelenkten Dokumente
3. **WebUI-Integration:** 4 digitale Markdown-Formblätter
4. **Lebenszyklus:** Erstellung → Prüfung → Freigabe → Archivierung

**Dokumentenregister:**
- **Anweisungen (VA/AA):** → `DMS_ARI_Anweisungen_Richtlinien.md`
- **Formblätter (F):** → `DMS_FORM_Formblaetter.md`

---

## 📝 DOKUMENTEN-NOMENKLATUR

### Dokumententypen

| Prefix | Typ | Beschreibung | Anzahl | Detailliste |
|--------|-----|--------------|--------|-------------|
| **VA** | Verfahrensanweisung | Prozessbeschreibung (WIE) | 33 | → DMS_ARI |
| **AA** | Arbeitsanweisung | Tätigkeitsbeschreibung (WAS) | - | → DMS_ARI |
| **F** | Formblatt | Auszufüllendes Formular | 71 | → DMS_FORM |
| **PA** | Prüfanweisung | Kundenspezifische Prüfung | - | Kundenordner |
| **PP** | Prüfplan | Control Plan | - | Kundenordner |
| **PR** | Prozess Workflow | Visualisierter Ablauf | - | OSP-Module |

### Funktionsbereiche

| Kürzel | Bereich | Kürzel | Bereich |
|--------|---------|--------|---------|
| G | Geschäftsführung | HR/PW | Personal |
| QM | Qualitätsmanagement | IT | Technik/IT |
| CM | Compliance | AS | Arbeitssicherheit |
| EK | Einkauf | UW | Umwelt |
| VT | Vertrieb | AV | Arbeitsvorbereitung |
| VS | Versand | F1/F2/F3 | Fertigung (KST) |
| L | Lager | PS | Schweißen |

### Namensformat

```
[Typ]_[Bereich]_[Nr]_[Titel].[ext]
Beispiel: VA_QM_01_Erstellung_und_Lenkung_von_Dokumenten.pdf
```

**Revision:** Im Dokument-Header, NICHT im Dateinamen!

---

## 📂 SHAREPOINT-STRUKTUR

**Basis-URL:** `https://rainerschneiderkabelsatz.sharepoint.com/sites/OSP/Freigegebene Dokumente/`

### Dokumenten-Ordner

| Ordner | Inhalt | Zugriff |
|--------|--------|---------|
| `/Verfahrensanweisungen/` | VA_*.pdf (33) | 🟡 L2 |
| `/Formblätter/` | F_*.pdf + 4 MD (71) | 🟡 L2 |
| `/Pruefanweisungen/` | PA_*.pdf | 🟡 L2 |
| `/Handbücher/` | Management_Handbuch.pdf | 🟡 L2 |
| `/Richtlinien/` | Richtlinien | 🟡 L2 |
| `/Normen/` | DIN/EN/VDE/VG (~40) | 🟡 L2 |

### Weitere Ordner

| Ordner | Inhalt | Zugriff |
|--------|--------|---------|
| `/PMV_Kalibrierung/` | Kalibrierprotokolle (~90) | 🟡 L2 |
| `/Inventar/` | MA_*.pdf (~130) | 🟡 L2 |
| `/Gesetze/` | BDSG, DGUV, ProdHaftG | 🟢 L1 |
| `/Policies/` | RoHS, REACH, PFAS | 🟢 L1 |
| `/Vetraege_Datenschutz/` | AVV, DPA | 🔴 L3 |
| `/OSP_Root/main/` | 15 OSP-Module (MD) | 🟡 L2 |

---

## 🖥️ WEBUI-FORMULARE

4 Formblätter sind als Markdown für **Open WebUI** verfügbar:

| ID | Formular | Zweck |
|----|----------|-------|
| F_QM_02 | Qualitätsabweichung | Abweichungen dokumentieren |
| F_QM_37 | Wartungsbericht | Wartungsarbeiten erfassen |
| F_QM_39 | Firmenkalibrierschein | Interne PMV-Kalibrierung |
| F_QM_50 | Sitzungsprotokoll | Sitzungen protokollieren |

**Workflow:** WebUI → Ausfüllen → PDF-Export → SharePoint-Ablage

---

## 🔄 DOKUMENTEN-LEBENSZYKLUS

```
ERSTELLUNG → PRÜFUNG → FREIGABE → PUBLIKATION → ARCHIVIERUNG
 (Autor)      (QM)     (QM/GF)     (IT/QM)        (QM)
```

### Freigabe-Matrix

| Typ | Ersteller | Prüfer | Freigabe |
|-----|-----------|--------|----------|
| VA | Fachabteilung | QM | QM + GF |
| AA | Fachabteilung | QM | QM |
| F | Fachabteilung | QM | QM |
| PA/PP | QM/Prüffeld | QM | QM + Kunde |

---

## 🔗 QUERVERWEISE

**DMS-Modul:**
- → `DMS_ARI_Anweisungen_Richtlinien.md` - VA/AA Dokumentenliste
- → `DMS_FORM_Formblaetter.md` - Formblatt-Register

**Governance:**
- ↔ `OSP_System_Prompt_API.md` - Dateibenennungs-Standard
- ↔ `QM_CORE_Qualitaetspolitik.md` - QM-Grundsätze

**Externe:**
- ← VA-QM-01 Rev.H - Quelldokument Dokumentenlenkung

---

## 📝 CHANGELOG

### [1.1] - 2025-12-11
- ✅ Optimiert für OSP_KERN-Nutzung
- ✅ Verweise auf DMS_ARI und DMS_FORM eingefügt
- ✅ Dokumentendetails in Subdokumente ausgelagert
- ✅ Token-Reduktion von ~3.800 auf ~2.200

### [1.0] - 2025-12-11
- Initiale Version

---

**Status:** ✅ PRODUKTIV | **Verantwortlich:** AL | **ISO:** 7.5

*Bei Fragen zur Dokumentenlenkung: QM (AL) kontaktieren.*

(C: 100%) [OSP]
