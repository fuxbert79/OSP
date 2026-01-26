# F-QM-02 Qualitätsabweichung

**Formblatt-ID:** F-QM-02
**Anwendung:** Lieferanten-Reklamationen
**Status:** Template geplant

## Beschreibung

Dieses Formblatt wird verwendet, um Qualitätsabweichungen bei Lieferantenware zu dokumentieren.

## Dateien (geplant)

| Datei | Beschreibung |
|-------|--------------|
| `F_QM_02_template.md` | Markdown-Template |
| `F_QM_02_schema.json` | JSON-Schema für Validierung |
| `F_QM_02_prompt.md` | KI-Prompt für automatische Ausfüllung |

## Workflow

1. Qualitätsabweichung wird festgestellt (Wareneingang/Fertigung)
2. AL/TS erstellt Reklamation mit ID QA-JJNNN
3. KI füllt Formblatt vor (n8n Workflow)
4. Prüfung und Ergänzung durch QM
5. Versand an Lieferant

---

*Teil des RMS-Systems | Stand: 2026-01-26*
