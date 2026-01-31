# OSP-n8n-Integration | API-Berechtigungen

**Quelle:** Azure Portal - App-Registrierungen
**Datum:** 30.01.2026
**Aktualisiert:** 30.01.2026 (Analyse für NZA Phase 3 ff)

---

## Zusammenfassung

| Kategorie | Anzahl |
|-----------|--------|
| **Aktuell gesamt** | 24 |
| Behalten | 17 |
| Neu hinzufügen | 1 |
| Entfernen | 7 |
| **Ziel gesamt** | 18 |

**Hinweis:** n8n arbeitet mit delegierten Berechtigungen (OAuth2 User-Login). Anwendungsberechtigungen sind nur für User.Read.All und ChannelReadBasic.All erforderlich.

---

## Benötigte Berechtigungen (behalten)

| Berechtigung | Typ | Zweck | Status |
|--------------|-----|-------|--------|
| Sites.ReadWrite.All | Delegiert | SharePoint-Listen CRUD | ✅ Vorhanden |
| Files.ReadWrite.All | Delegiert | Bilder-Upload zu SharePoint | ✅ Vorhanden |
| Mail.Read | Delegiert | E-Mail-Import (nza@, reklamation@) | ✅ Vorhanden |
| Mail.Read.Shared | Delegiert | Shared Mailbox lesen | ✅ Vorhanden |
| Mail.ReadWrite | Delegiert | E-Mails als gelesen markieren | ✅ Vorhanden |
| Mail.ReadWrite.Shared | Delegiert | Shared Mailbox verwalten | ✅ Vorhanden |
| Mail.Send | Delegiert | E-Mail-Benachrichtigungen versenden | ✅ Vorhanden |
| ChannelMessage.Send | Delegiert | Teams-Kanal-Nachrichten senden | ✅ Vorhanden |
| ChannelMessage.Read.All | Delegiert | Kanal-Nachrichten lesen | ✅ Vorhanden |
| Chat.Read | Delegiert | Chat-Nachrichten lesen | ✅ Vorhanden |
| User.Read | Delegiert | Eigenes Profil lesen | ✅ Vorhanden |
| User.Read.All | Delegiert | Alle User lesen (Dropdown) | ✅ Vorhanden |
| User.Read.All | Anwendung | User-Lookup (unbeaufsichtigt) | ✅ Vorhanden |
| ChannelReadBasic.All | Anwendung | Teams-Kanäle auflisten | ✅ Vorhanden |
| offline_access | Delegiert | Token-Refresh (Dauerbetrieb) | ✅ Vorhanden |
| openid | Delegiert | OAuth2 Login | ✅ Vorhanden |
| profile | Delegiert | Benutzerprofil anzeigen | ✅ Vorhanden |

---

## Neu benötigt (hinzufügen)

| Berechtigung | Typ | Zweck | Admin-Einwilligung |
|--------------|-----|-------|-------------------|
| **TeamsActivity.Send** | Delegiert | Teams Activity-Benachrichtigung an einzelne MA | Ja |

**Verwendung:** NZA-Notify-API und RMS-Notify-API für Maßnahmen-Zuweisung mit direkter Benachrichtigung im Teams Activity Feed.

---

## Kann entfernt werden

| Berechtigung | Typ | Grund |
|--------------|-----|-------|
| Calendars.Read | Delegiert | Kalender wird nicht verwendet |
| Calendars.ReadWrite | Delegiert | Kalender wird nicht verwendet |
| Calendars.ReadWrite.Shared | Delegiert | Kalender wird nicht verwendet |
| ChannelMessage.Edit | Delegiert | Nachrichten bearbeiten nicht erforderlich |
| ChannelMessage.ReadWrite | Delegiert | Read + Send reicht aus |
| Mail.ReadBasic | Delegiert | Mail.Read ist umfassender |
| ServiceActivity.Teams.Read.All | Delegiert | Nicht benötigt |

---

## Berechtigungen nach Funktion

### SharePoint (NZA/RMS Listen)
- `Sites.ReadWrite.All` (Delegiert) - Listen erstellen, lesen, aktualisieren

### Dateien (Bilder-Upload)
- `Files.ReadWrite.All` (Delegiert) - Bilder in SharePoint-Bibliotheken speichern

### E-Mail (Import & Benachrichtigung)
- `Mail.Read` (Delegiert) - E-Mails aus nza@/reklamation@ lesen
- `Mail.Read.Shared` (Delegiert) - Shared Mailbox Zugriff
- `Mail.ReadWrite` (Delegiert) - E-Mails als gelesen markieren
- `Mail.ReadWrite.Shared` (Delegiert) - Shared Mailbox verwalten
- `Mail.Send` (Delegiert) - Benachrichtigungs-E-Mails versenden

### Teams (Benachrichtigungen)
- `ChannelMessage.Send` (Delegiert) - Nachrichten in NZA/RMS-Kanal posten
- `ChannelMessage.Read.All` (Delegiert) - Kanal-Historie lesen
- `ChannelReadBasic.All` (Anwendung) - Kanäle auflisten
- `TeamsActivity.Send` (Delegiert) - **NEU** - Activity Feed Benachrichtigung

### Chat
- `Chat.Read` (Delegiert) - Chat-Nachrichten lesen

### Benutzer
- `User.Read` (Delegiert) - Eigenes Profil
- `User.Read.All` (Delegiert + Anwendung) - Alle Benutzer für Dropdown/Lookup

### Authentifizierung
- `offline_access` (Delegiert) - Refresh Token für Dauerbetrieb
- `openid` (Delegiert) - OAuth2 Login
- `profile` (Delegiert) - Profilinformationen

---

## Azure Portal Aktionen

### Hinzufügen
1. Azure Portal → App-Registrierungen → OSP-n8n-Integration
2. API-Berechtigungen → Berechtigung hinzufügen
3. Microsoft Graph → Delegierte Berechtigungen
4. `TeamsActivity.Send` auswählen
5. Administratoreinwilligung erteilen

### Entfernen
1. Azure Portal → App-Registrierungen → OSP-n8n-Integration
2. API-Berechtigungen
3. Folgende Berechtigungen einzeln entfernen:
   - Calendars.Read
   - Calendars.ReadWrite
   - Calendars.ReadWrite.Shared
   - ChannelMessage.Edit
   - ChannelMessage.ReadWrite
   - Mail.ReadBasic
   - ServiceActivity.Teams.Read.All

---

*Erstellt: 30.01.2026*
*Analyse für: NZA Phase 3 ff + RMS*
