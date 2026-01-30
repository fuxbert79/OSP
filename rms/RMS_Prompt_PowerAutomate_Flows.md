# 🔄 RMS POWER AUTOMATE - NÄCHSTE SCHRITTE

## KONTEXT

Ich arbeite am RMS (Reklamationsmanagementsystem) für Rainer Schneider Kabelsatzbau.

**SharePoint-Site:** https://rainerschneiderkabelsatz.sharepoint.com/sites/RMS

**Bereits erstellt (Phase 1):**
- ✅ Liste "RMS-Reklamationen" mit Spalten: Titel, QA_ID, Rekla_Typ, Prioritaet, Rekla_Status, Beschreibung, KST, Verantwortlich, Erfassungsdatum, Zieldatum
- ✅ Liste "RMS-Massnahmen" mit Lookup zu RMS-Reklamationen
- ✅ Liste "RMS-Schriftverkehr" mit Lookup zu RMS-Reklamationen
- ✅ Liste "RMS-KPIs"
- ✅ Liste "RMS-Config" mit Einträgen: CURRENT_YEAR=2026, Last_ID=1, EMAIL_REKLAMATION, EMAIL_NZA, ALARM_TAGE=3, ADMIN_EMAIL

---

## AUFGABE 1: Power Automate Flow "RMS-Email-Import"

### Anforderung

Erstelle einen Power Automate Flow, der:
1. **Trigger:** Neue E-Mail in einem der Postfächer empfängt:
   - `reklamation@schneider-kabelsatzbau.de` → Typ = KUNDE
   - `nza@schneider-kabelsatzbau.de` → Typ = INTERN
2. **Aktion:** Automatisch einen neuen Eintrag in "RMS-Reklamationen" erstellt

### Flow-Logik

```
TRIGGER: Wenn eine neue E-Mail eingeht (Office 365 Outlook)
│
├─ BEDINGUNG: Prüfe Empfänger-Postfach
│   ├─ reklamation@... → Rekla_Typ = "KUNDE"
│   └─ nza@... → Rekla_Typ = "INTERN"
│
├─ AKTION: HTTP-Request an Flow "QA-ID-Generator" (oder Child Flow)
│   └─ Erhalte: Neue QA_ID (z.B. "QA-26002")
│
├─ AKTION: Element in SharePoint erstellen (RMS-Reklamationen)
│   ├─ Titel = E-Mail-Betreff
│   ├─ QA_ID = [von Generator]
│   ├─ Rekla_Typ = [KUNDE oder INTERN]
│   ├─ Prioritaet = "MITTEL" (Standard)
│   ├─ Rekla_Status = "NEU"
│   ├─ Beschreibung = E-Mail-Body (Text)
│   ├─ KST = "VW" (Standard, später manuell ändern)
│   ├─ Verantwortlich = [ADMIN_EMAIL aus Config]
│   ├─ Erfassungsdatum = utcNow()
│   └─ Zieldatum = addDays(utcNow(), 14)
│
├─ AKTION: Element in SharePoint erstellen (RMS-Schriftverkehr)
│   ├─ Titel = E-Mail-Betreff
│   ├─ Reklamation = [ID des neuen Eintrags]
│   ├─ Email_Datum = E-Mail-Empfangsdatum
│   ├─ Richtung = "EINGANG"
│   ├─ Absender = E-Mail-Von
│   ├─ Empfaenger = E-Mail-An
│   └─ Inhalt = E-Mail-Body (gekürzt auf 5000 Zeichen)
│
└─ AKTION: E-Mail senden (Benachrichtigung)
    ├─ An: ADMIN_EMAIL
    ├─ Betreff: "Neue Reklamation: [QA_ID] - [Titel]"
    └─ Body: Link zur Reklamation
```

### Prioritäts-Erkennung (Optional)

Keywords im Betreff für automatische Priorisierung:
- "dringend", "sofort", "kritisch", "stopp" → KRITISCH
- "wichtig", "eilig" → HOCH
- Standard → MITTEL

---

## AUFGABE 2: Power Automate Flow "RMS-QA-ID-Generator"

### Anforderung

Erstelle einen Power Automate Flow (als HTTP-Trigger oder Child Flow), der:
1. Die aktuelle ID aus RMS-Config liest
2. Inkrementiert
3. Eine neue QA-ID im Format `QA-JJNNN` zurückgibt
4. Die Config aktualisiert

### Flow-Logik

```
TRIGGER: HTTP-Anforderung (oder "Manuell aus einem anderen Flow")
│
├─ AKTION: Element abrufen (RMS-Config)
│   └─ Filter: Titel = "CURRENT_YEAR"
│   └─ Speichere: currentYear
│
├─ AKTION: Element abrufen (RMS-Config)
│   └─ Filter: Titel = "Last_ID"
│   └─ Speichere: lastId
│
├─ VARIABLE: newId = int(lastId) + 1
│
├─ VARIABLE: qaId = concat('QA-', substring(currentYear, 2, 2), '-', formatNumber(newId, '000'))
│   └─ Beispiel: QA-26-002
│
├─ AKTION: Element aktualisieren (RMS-Config)
│   └─ Titel = "Last_ID"
│   └─ Wert = string(newId)
│
└─ ANTWORT (bei HTTP-Trigger):
    └─ { "qa_id": "[qaId]", "nummer": [newId] }
```

### QA-ID Format

- **QA-JJ-NNN** oder **QA-JJNNN**
- JJ = 2-stelliges Jahr (26 für 2026)
- NNN = 3-stellige laufende Nummer (001, 002, ...)
- Beispiele: QA-26-001, QA-26-002, QA-26-150

### Jahreswechsel-Logik

Am 01.01. eines neuen Jahres:
- Prüfe ob currentYear ≠ aktuelles Jahr
- Falls ja: Reset Last_ID auf 0, Update CURRENT_YEAR

---

## TECHNISCHE DETAILS

### SharePoint-Verbindung
- Site: rainerschneiderkabelsatz.sharepoint.com/sites/RMS
- Listen: RMS-Reklamationen, RMS-Schriftverkehr, RMS-Config

### Outlook-Verbindung
- Shared Mailbox oder Delegierung für beide Postfächer
- Alternativ: Zwei separate Flows (einer pro Postfach)

### Berechtigungen
- Flow-Ersteller braucht Zugriff auf SharePoint-Site
- Flow-Ersteller braucht Zugriff auf Outlook-Postfächer

---

## FRAGEN ZUR KLÄRUNG

1. **Postfach-Zugriff:** Sind `reklamation@` und `nza@` Shared Mailboxes oder separate Accounts?
2. **QA-ID Format:** Bevorzugst du `QA-26-001` (mit Bindestrich) oder `QA-26001` (ohne)?
3. **Child Flow vs. HTTP:** Soll der ID-Generator als HTTP-Trigger (extern aufrufbar) oder als Child Flow (nur intern) erstellt werden?
4. **Anhänge:** Sollen E-Mail-Anhänge automatisch in SharePoint gespeichert werden?

---

Bitte führe mich Schritt für Schritt durch die Erstellung dieser beiden Power Automate Flows.
