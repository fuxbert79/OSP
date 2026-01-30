# RMS Formular-Übersicht - OSP Schneider Kabelsatzbau

**Stand:** 2025-12-21  
**Erstellt durch:** OSP-System (AL)  
**Modul:** Reklamationsmanagement System (RMS)

---

## 📊 Konvertierte QM-Formulare

| ID | Titel | Typ | 8D-Mapping | Dateien |
|----|-------|-----|------------|---------|
| **F-QM-02** | Qualitätsabweichung | Extern (Lieferant) | Auslöser für 8D | 3 |
| **F-QM-03** | 8D-Report | Extern (Kunde/Lieferant) | Vollständig D1-D8 | 3 |
| **F-QM-04** | Nach- und Zusatzarbeiten (NZA) | Intern | Dokumentation | 3 |
| **F-QM-14** | Korrekturmaßnahme | Intern (Audit/CAPA) | 8D-Light (D2-D4-D6-D7) | 3 |

**Gesamt: 12 Dateien (4 Formulare × 3 Dateitypen)**

---

## 🔗 Formular-Verknüpfungen

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNE REKLAMATION                          │
│                                                                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │  F-QM-02    │──────│  F-QM-03    │──────│  F-QM-04    │     │
│  │  Qualitäts- │      │  8D-Report  │      │  NZA        │     │
│  │  abweichung │      │  (Vollst.)  │      │             │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│       QA-Nr.              QA-Nr.              QA-Nr.           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    INTERNE ABWEICHUNG                           │
│                                                                 │
│  ┌─────────────┐      ┌─────────────┐                          │
│  │  F-QM-14    │──────│  F-QM-04    │                          │
│  │  Korrektur- │      │  NZA        │                          │
│  │  maßnahme   │      │  (optional) │                          │
│  │  (8D-Light) │      │             │                          │
│  └─────────────┘      └─────────────┘                          │
│       KM-Nr.              NZA-Nr.                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Dateitypen pro Formular

| Dateityp | Zweck | Namensschema |
|----------|-------|--------------|
| **Markdown (.md)** | Template mit YAML-Frontmatter | `F_QM_XX_Name.md` |
| **RMS-Prompt (.md)** | System-Prompt für KI-Befüllung | `RMS_Prompt_F_QM_XX_Name.md` |
| **JSON-Schema (.json)** | API-Validierung | `F_QM_XX_Schema.json` |

---

## 🎯 Verwendungszweck

### F-QM-02 Qualitätsabweichung
- **Trigger:** Lieferant liefert fehlerhafte Ware
- **Ausgabe:** Reklamationsschreiben an Lieferant
- **Folge:** 8D-Report (F-QM-03) anfordern

### F-QM-03 8D-Report
- **Trigger:** Kundenreklamation ODER F-QM-02 (Lieferant)
- **Inhalt:** Vollständiger 8D-Prozess (D1-D8)
- **Team:** Ja, interdisziplinär

### F-QM-04 NZA (Nach- und Zusatzarbeiten)
- **Trigger:** Nacharbeit erforderlich (intern oder extern)
- **Inhalt:** Dokumentation von Zusatzaufwand
- **Verknüpfung:** QA-Nummer möglich

### F-QM-14 Korrekturmaßnahme (8D-Light)
- **Trigger:** Internes Audit, Prozessbeobachtung, CAPA
- **Inhalt:** Vereinfachter 8D (D2-D4-D6-D7)
- **Team:** Nein, 1 Verantwortlicher

---

## 📊 8D-Abdeckung

| 8D-Schritt | F-QM-03 | F-QM-14 |
|------------|---------|---------|
| D1 Team | ✅ | ❌ |
| D2 Problem | ✅ | ✅ Phase 1 |
| D3 Sofort | ✅ | ❌ |
| D4 Ursache | ✅ | ✅ Phase 2 |
| D5 Geplant | ✅ | ✅ Phase 2 |
| D6 Durchgeführt | ✅ | ✅ Phase 3 |
| D7 Prävention | ✅ | ✅ Phase 4 |
| D8 Abschluss | ✅ | ❌ |

---

## 🔧 Integration

### n8n Webhooks
```
POST /webhook/rms/qualitaetsabweichung   → F-QM-02
POST /webhook/rms/8d-report              → F-QM-03
POST /webhook/rms/nza                    → F-QM-04
POST /webhook/rms/korrekturmassnahme     → F-QM-14
```

### SharePoint-Ablage
```
/sites/OSP/Freigegebene Dokumente/Formblätter/Ausgefüllt/QM/
├── Qualitätsabweichungen/    → F-QM-02
├── 8D-Reports/               → F-QM-03
├── NZA/                      → F-QM-04
└── Korrekturmaßnahmen/       → F-QM-14
```

### Nummernkreise
| Formular | Präfix | Format |
|----------|--------|--------|
| F-QM-02 | QA | QA-YYYY-NNN |
| F-QM-03 | (nutzt QA) | QA-YYYY-NNN |
| F-QM-04 | NZA | NZA-YYYY-NNN |
| F-QM-14 | KM | KM-YYYY-NNN |

---

## ✅ Nächste Schritte

1. [ ] RMS-Prompts in Open WebUI hinterlegen
2. [ ] JSON-Schemas in n8n-Workflows integrieren
3. [ ] SharePoint-Ordnerstruktur anlegen
4. [ ] Nummernkreis-Generator implementieren
5. [ ] Test-Durchläufe mit echten Daten

---

*Dokumentversion: 1.0 | Stand: 2025-12-21*  
*OSP - Organisations-System-Prompt | Schneider Kabelsatzbau*
