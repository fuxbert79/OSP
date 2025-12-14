# OSP KERN-Dateien prüfen

Prüfe die 12 OSP_KERN-Dateien auf Konsistenz und Vollständigkeit.

## OSP_KERN Dateien (12 Stück in documents/)
```
documents/HR_CORE_Personalstamm.md       # 54 MA - KRITISCH!
documents/TM_CORE_Maschinen_Anlagen.md   # ~220 Maschinen - KRITISCH!
documents/TM_WKZ_Werkzeuge.md            # ~342 Werkzeuge - KRITISCH!
documents/AV_AGK_Arbeitsgang_Katalog.md
documents/KST_CORE_Layout_Fertigung.md
documents/QM_CORE_Qualitaetspolitik.md
documents/QM_PMV_Prüfmittelverwaltung.md
documents/QM_REK_Reklamationsmanagement.md
documents/KOM_CORE_Corporate_Identity.md
documents/DMS_CORE_Dokumentenstruktur.md
documents/IT_OSP_KI_Chatbot.md
documents/OSP_Navigator.md               # KRITISCH!
```

## Aufgaben

1. Prüfe ob alle 12 Dateien in documents/ existieren
2. Für jede Datei prüfe:
   - Existiert? ✅/❌
   - Dateigröße (< 40KB empfohlen)
   - UTF-8 Encoding
   - YAML Frontmatter vorhanden?
3. Zeige Zusammenfassung

## Kritische Checks

⚠️ **HR_CORE:** Alle MA-Kürzel eindeutig?
⚠️ **TM_CORE:** Inventar-Nummern eindeutig?
⚠️ **TM_WKZ:** WKZ-Nummern eindeutig?

## Output
```
=== OSP KERN CHECK ===
Geprüft: 12 Dateien
Status: X/12 OK
```
