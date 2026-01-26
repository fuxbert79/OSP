# RMS System-Prompts

**Status:** In Entwicklung
**Zweck:** KI-gestützte Formblatt-Ausfüllung

## Prompt-Dateien (geplant)

| Datei | Formblatt | Zweck |
|-------|-----------|-------|
| `prompt_f_qm_02.md` | F-QM-02 | Qualitätsabweichung Lieferant |
| `prompt_f_qm_03.md` | F-QM-03 | 8D-Report vollständig |
| `prompt_f_qm_04.md` | F-QM-04 | NZA (Nach-/Zusatzarbeiten) |
| `prompt_f_qm_14.md` | F-QM-14 | Korrekturmaßnahme (8D-Light) |

## Prompt-Struktur

Jeder Prompt enthält:

1. **Kontext** - RMS-spezifische Informationen
2. **Formular-Schema** - JSON-Struktur des Formblatts
3. **Validierungsregeln** - Pflichtfelder, Formate
4. **Beispiele** - Ausgefüllte Muster

## Integration

Die Prompts werden von n8n-Workflows verwendet:
1. Benutzer lädt Reklamationsdaten hoch
2. n8n ruft Claude API mit entsprechendem Prompt auf
3. Claude füllt Formblatt strukturiert aus
4. Ergebnis wird in SharePoint gespeichert

---

*Teil des RMS-Systems | NULL-FEHLER-POLITIK gilt!*
