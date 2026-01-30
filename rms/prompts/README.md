# RMS Prompts

**Status:** Geplant
**Verwendung:** Claude API für Formblatt-Ausfüllung

## Prompt-Dateien (geplant)

| Datei | Formblatt | Beschreibung |
|-------|-----------|--------------|
| RMS_Prompt_F_QM_02.md | Qualitätsabweichung | Lieferanten-Reklamation |
| RMS_Prompt_F_QM_03.md | 8D-Report | Vollständiger 8D für Kunden |
| RMS_Prompt_F_QM_04.md | NZA | Nach-/Zusatzarbeiten |
| RMS_Prompt_F_QM_14.md | Korrekturmaßnahme | 8D-Light intern |
| RMS_System_Prompt.md | - | Basis-System-Prompt |

## Prompt-Struktur

Jeder Formblatt-Prompt enthält:
1. **Kontext:** OSP-Regeln, NULL-FEHLER-POLITIK
2. **Schema:** JSON-Feldstruktur
3. **Beispiele:** Few-Shot für konsistente Ausgabe
4. **Validierung:** Pflichtfelder, Formatprüfung

---

*Teil des OSP-Systems | NULL-FEHLER-POLITIK gilt!*
