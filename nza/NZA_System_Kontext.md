# NZA-System - Kontext & Konfiguration

**Erstellt:** 2026-01-29  
**Aktualisiert:** 2026-01-29  
**Für:** Implementierung am 2026-01-30  
**Basis:** RMS-System als Vorlage  
**Status:** PLANUNG

---

## 📋 SYSTEM-ÜBERSICHT

### Abgrenzung RMS vs. NZA

| Aspekt | RMS | NZA |
|--------|-----|-----|
| **Zweck** | Externe Reklamationen | Interne Reklamationen + Nacharbeiten |
| **Typen** | Kunde, Lieferant | Intern (Fertigung, Prüffeld, etc.) |
| **E-Mail** | reklamation@schneider-kabelsatzbau.de | nza@schneider-kabelsatzbau.de |
| **SharePoint-Site** | /sites/rms | /sites/nza |
| **ID-Format** | QA-26001 | NZA-26001 |
| **Kostenerfassung** | Nein | Ja (Nacharbeitskosten) |
| **Verursacher** | Extern (Kunde/Lieferant) | Intern (MA aus nza-mitarbeiter) |
| **Dashboard** | osp.schneider-kabelsatzbau.de/rms/ | osp.schneider-kabelsatzbau.de/nza/ |
| **Schriftverkehr** | Wichtig (E-Mail-Kommunikation) | Weniger relevant |
| **Bilder** | Optional | **Wichtig** (Fehlerfotos) |
| **Maßnahmen** | Ja + Benachrichtigung | **Ja + Teams-Benachrichtigung** |

### Verknüpfung RMS ↔ NZA

```
Kundenreklamation (RMS)
    └── kann NZA auslösen → Nacharbeit/Neufertigung intern

Lieferantenreklamation (RMS)
    └── kann NZA auslösen → Kosten-Tracking für Lieferant
```

---

## 🏗️ SHAREPOINT-STRUKTUR

### Site erstellen

**URL:** `https://rainerschneiderkabelsatz.sharepoint.com/sites/nza`

**Zu erstellen:**
- [ ] SharePoint-Site "NZA" (Team-Site)
- [ ] 8 Listen (siehe unten)
- [ ] Dokumentenbibliothek für Bilder/Anhänge

---

### Liste 1: nza-prozesse (Hauptliste)

**Zweck:** Alle NZA-Vorgänge

| Spalte | Typ | Beschreibung | Pflicht |
|--------|-----|--------------|---------|
| Title | Text | Kurzbeschreibung des Problems | Ja |
| NZA_ID | Text | Eindeutige ID (NZA-26xxx) | Ja (auto) |
| NZA_Typ | Choice | Nacharbeit, Neufertigung, Ausschuss, Sonstiges | Ja |
| Status | Choice | Neu, In Bearbeitung, Abgeschlossen | Ja |
| Prioritaet | Choice | niedrig, mittel, hoch, kritisch | Ja |
| Beschreibung | Multiline | Detaillierte Fehlerbeschreibung | Ja |
| Erfassungsdatum | Date | Datum der Erfassung | Ja (auto) |
| Verursacher_ID | Lookup | → nza-mitarbeiter | Nein |
| Verantwortlich | Text | Bearbeiter (M365-User) | Nein |
| KST_Betroffene | Choice | F1, F2, F3, Prüffeld | Ja |
| Fehlerursache | Choice | Maschine, Material, Mensch, Methode, Umwelt | Nein |
| Artikel_Nr | Text | Betroffene Artikelnummer | Nein |
| Auftrag_Nr | Text | Betroffene Auftragsnummer | Nein |
| Menge_Betroffen | Number | Anzahl betroffener Teile | Nein |
| Menge_Nacharbeit | Number | Anzahl nachgearbeiteter Teile | Nein |
| Menge_Ausschuss | Number | Anzahl Ausschuss | Nein |
| Zeit_Nacharbeit_Min | Number | Nacharbeitszeit in Minuten | Nein |
| Bezug_RMS | Text | Verknüpfte RMS QA-ID | Nein |
| Bezug_RMS_Typ | Choice | Kunde, Lieferant | Nein |
| Abschlussdatum | Date | Datum des Abschlusses | Nein |
| Abschluss_Bemerkung | Multiline | Abschlussbericht | Nein |
| Bilder_Ordner | Text | SharePoint Folder-URL für Bilder | Nein |

---

### Liste 2: nza-massnahmen

**Zweck:** Maßnahmen zu NZA-Vorgängen (inkl. Teams-Benachrichtigung)

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | Maßnahmen-Titel |
| NZA_ID | Lookup | → nza-prozesse |
| Massnahme_Typ | Choice | Sofortmaßnahme, Korrekturmaßnahme, Vorbeugemaßnahme |
| Beschreibung | Multiline | Maßnahmenbeschreibung |
| Verantwortlich_ID | Text | M365-User-ID (für Teams-Benachrichtigung) |
| Verantwortlich_Name | Text | Anzeigename |
| Verantwortlich_Email | Text | E-Mail-Adresse |
| Termin | Date | Fälligkeitsdatum |
| Status | Choice | Offen, In Bearbeitung, Abgeschlossen, Überfällig |
| Erledigt_Am | Date | Abschlussdatum |
| Wirksamkeit | Choice | Nicht geprüft, Wirksam, Nicht wirksam |
| Benachrichtigung_Teams | Boolean | Teams-Nachricht gesendet? |
| Benachrichtigung_Email | Boolean | E-Mail gesendet? |

---

### Liste 3: nza-bilder

**Zweck:** Fehlerfotos und Dokumentation (WICHTIG für NZA!)

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | Bildbeschreibung |
| NZA_ID | Lookup | → nza-prozesse |
| Bild_URL | URL | SharePoint-Link zum Bild |
| Bild_Thumbnail | URL | Thumbnail-URL |
| Hochgeladen_Von | Text | Uploader |
| Hochgeladen_Am | DateTime | Upload-Zeitstempel |
| Kategorie | Choice | Fehlerbild, Vorher, Nachher, Dokumentation |
| Bemerkung | Text | Zusätzliche Notizen |

---

### Liste 4: nza-mitarbeiter

**Zweck:** Produktions-Mitarbeiter (Verursacher) - ersetzt HR_CORE Lookup

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | Vollständiger Name |
| Kuerzel | Text | 2-Buchstaben-Kürzel (z.B. "AB") |
| Personalnummer | Text | Personal-Nr. |
| Abteilung | Choice | Fertigung F1, Fertigung F2, Fertigung F3, Prüffeld, Lager, Sonstiges |
| KST | Text | Kostenstelle |
| Schicht | Choice | Früh, Spät, Nacht, Normal |
| Aktiv | Boolean | Noch beschäftigt? |
| Eintrittsdatum | Date | Beschäftigungsbeginn |
| Vorgesetzter | Text | Name des Vorgesetzten |

---

### Liste 5: nza-material

**Zweck:** Materialverbrauch bei Nacharbeit/Ausschuss

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | Materialbeschreibung |
| NZA_ID | Lookup | → nza-prozesse |
| Artikel_Nr | Text | Artikel-/Materialnummer |
| Bezeichnung | Text | Materialbezeichnung |
| Menge | Number | Verbrauchte Menge |
| Einheit | Choice | Stück, Meter, kg, Liter |
| Einzelpreis | Currency | Preis pro Einheit |
| Gesamtpreis | Currency | Menge × Einzelpreis |
| Lagerort | Text | Entnahme-Lagerort |

---

### Liste 6: nza-kosten

**Zweck:** Kostenerfassung und -aggregation

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | Kostenposition |
| NZA_ID | Lookup | → nza-prozesse |
| Kostenart | Choice | Arbeitszeit, Material, Fremdleistung, Sonstiges |
| Betrag | Currency | Kostenbetrag in € |
| Beschreibung | Text | Details zur Kostenposition |
| Erfasst_Von | Text | Wer hat erfasst |
| Erfasst_Am | DateTime | Erfassungsdatum |
| Belastung_An | Choice | Intern, Lieferant, Kunde |
| Belastung_Referenz | Text | Lieferanten-/Kunden-Nr. |

---

### Liste 7: nza-config

**Zweck:** System-Konfiguration und Einstellungen

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | Config-Key |
| Wert | Text | Config-Value |
| Typ | Choice | String, Number, Boolean, JSON |
| Beschreibung | Text | Erklärung |
| Gruppe | Choice | System, Kosten, Benachrichtigung, UI |

**Vorgeschlagene Config-Einträge:**

| Key | Wert | Beschreibung |
|-----|------|--------------|
| NZA_ID_COUNTER | 26001 | Aktueller NZA-ID Zähler |
| STUNDENSATZ_F1 | 45.00 | Stundensatz Fertigung F1 |
| STUNDENSATZ_F2 | 50.00 | Stundensatz Fertigung F2 |
| STUNDENSATZ_F3 | 55.00 | Stundensatz Fertigung F3 |
| STUNDENSATZ_PRUEFFELD | 60.00 | Stundensatz Prüffeld |
| TEAMS_NOTIFY_ENABLED | true | Teams-Benachrichtigung aktiv |
| EMAIL_NOTIFY_ENABLED | true | E-Mail-Benachrichtigung aktiv |
| AUTO_KOSTEN_BERECHNUNG | true | Automatische Kostenberechnung |

---

### Liste 8: nza-kpis

**Zweck:** Aggregierte KPIs für Dashboard (täglich berechnet)

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | KPI-Name |
| Datum | Date | Berechnungsdatum |
| Periode | Choice | Tag, Woche, Monat, Jahr |
| Wert | Number | KPI-Wert |
| Einheit | Text | €, Stück, %, Stunden |
| KST | Text | Kostenstelle (optional) |
| Typ | Text | NZA-Typ (optional) |

**Vorgeschlagene KPIs:**

| KPI | Beschreibung |
|-----|--------------|
| OFFENE_NZA | Anzahl offene Vorgänge |
| KOSTEN_MTD | Kosten Month-to-Date |
| KOSTEN_YTD | Kosten Year-to-Date |
| AVG_BEARBEITUNGSZEIT | Ø Tage bis Abschluss |
| AUSSCHUSS_QUOTE | Ausschuss-% |
| TOP_FEHLERURSACHE | Häufigste Ursache |
| TOP_KST | KST mit meisten NZA |

---

### Liste 9: nza-stammdaten (Optional)

**Zweck:** Artikel-/Produktstammdaten für Autocomplete

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Title | Text | Artikelbezeichnung |
| Artikel_Nr | Text | Artikelnummer |
| Kategorie | Choice | Kabel, Stecker, Gehäuse, Sonstiges |
| Lieferant | Text | Haupt-Lieferant |
| Einzelpreis | Currency | Standardpreis |
| Einheit | Choice | Stück, Meter, kg |
| Aktiv | Boolean | Artikel aktiv? |

---

## 📧 E-MAIL-INTEGRATION

### Postfach

**E-Mail:** `nza@schneider-kabelsatzbau.de`

**Eingehende Mails:**
- Interne Fehlermeldungen
- Qualitätsabweichungen aus Fertigung
- Prüffeld-Meldungen

### E-Mail-Parser Regeln

```javascript
// NZA-spezifische Keywords
const nzaKeywords = [
    'nacharbeit', 'nza', 'ausschuss', 'fehler', 'defekt',
    'qualitätsabweichung', 'reklamation intern', 'neufertigung',
    'prüffeld', 'abweichung', 'mangel'
];

// Kostenstellen aus Betreff/Body extrahieren
const kstPattern = /(?:KST|Kostenstelle|F[1-3]|Prüffeld)[:\s]*([A-Z0-9\-]+)/i;

// MA-Kürzel extrahieren (2 Großbuchstaben)
const maPattern = /(?:Verursacher|Mitarbeiter|MA)[:\s]*([A-Z]{2})/i;
```

---

## 🖥️ DASHBOARD-STRUKTUR

### URL

**Produktiv:** `https://osp.schneider-kabelsatzbau.de/nza/`

### Verzeichnis auf Server

```
/var/www/html/nza/
├── index.html
├── css/
│   └── style.css
├── js/
│   ├── app.js
│   ├── bilder.js          # Bilder-Upload/Galerie
│   ├── massnahmen.js      # Maßnahmen mit Teams-Notify
│   ├── kosten.js          # Kosten-Erfassung
│   └── charts.js          # KPI-Charts
└── img/
    └── logo.png
```

### KPIs (Dashboard-Header)

| KPI | Beschreibung | Berechnung |
|-----|--------------|------------|
| Offene NZA | Anzahl Status ≠ Abgeschlossen | COUNT |
| Kosten MTD | Gesamtkosten aktueller Monat | SUM aus nza-kosten |
| Kosten YTD | Gesamtkosten aktuelles Jahr | SUM aus nza-kosten |
| Ø Bearbeitungszeit | Durchschnittliche Tage bis Abschluss | AVG(Abschlussdatum - Erfassungsdatum) |
| Top Verursacher KST | Kostenstelle mit meisten NZA | GROUP BY KST |

### Charts

1. **Trend-Chart:** NZA pro Monat (Linie)
2. **Typ-Verteilung:** Nacharbeit/Neufertigung/Ausschuss (Donut)
3. **KST-Verteilung:** Nach Kostenstelle (Bar)
4. **Kosten-Trend:** Kosten pro Monat (Bar)
5. **Fehlerursachen:** Ishikawa-Kategorien (Donut)

### Filter

- Suchfeld (NZA-ID, Titel, Beschreibung)
- Typ (Nacharbeit, Neufertigung, Ausschuss, Sonstiges)
- Status (Alle, Neu, In Bearbeitung, Abgeschlossen)
- KST (F1, F2, F3, Prüffeld, Alle)
- Zeitraum (Heute, Diese Woche, Dieser Monat, Dieses Jahr, Alle)

### Detail-View Features

**Tabs im Detail-Modal:**

| Tab | Inhalt | Priorität |
|-----|--------|-----------|
| **Übersicht** | Stammdaten, Status, Verursacher | 🔴 |
| **Bilder** | **Galerie mit Upload-Funktion** | 🔴 |
| **Maßnahmen** | **Liste + Teams-Benachrichtigung** | 🔴 |
| **Kosten** | Material + Arbeitszeit | 🔴 |
| **Historie** | Änderungsprotokoll | 🟡 |

### Bilder-Galerie (WICHTIG!)

```html
<!-- Bilder-Tab im Detail-Modal -->
<div id="tab-bilder" class="tab-content">
    <div class="bilder-header">
        <h4>📷 Fehlerbilder</h4>
        <button class="btn btn-primary" onclick="openBildUpload()">
            + Bild hochladen
        </button>
    </div>
    
    <div id="bilder-galerie" class="galerie-grid">
        <!-- Dynamisch befüllt -->
    </div>
    
    <!-- Lightbox für Vollbild -->
    <div id="bild-lightbox" class="lightbox" style="display: none;">
        <img id="lightbox-img" src="">
        <button class="lightbox-close" onclick="closeLightbox()">×</button>
        <div class="lightbox-info">
            <span id="lightbox-kategorie"></span>
            <span id="lightbox-datum"></span>
        </div>
    </div>
</div>
```

### Maßnahmen mit Teams-Benachrichtigung

```html
<!-- Maßnahmen-Tab -->
<div id="tab-massnahmen" class="tab-content">
    <div class="massnahmen-header">
        <h4>📋 Maßnahmen</h4>
        <button class="btn btn-primary" onclick="openMassnahmeModal()">
            + Maßnahme anlegen
        </button>
    </div>
    
    <div id="massnahmen-liste">
        <!-- Dynamisch befüllt -->
    </div>
</div>

<!-- Maßnahme-Modal -->
<div id="modal-massnahme" class="modal">
    <div class="modal-content">
        <h3>Neue Maßnahme</h3>
        
        <!-- ... Felder ... -->
        
        <div class="form-group">
            <label>Benachrichtigung</label>
            <div class="notify-options">
                <label>
                    <input type="checkbox" id="notify-teams" checked>
                    📱 Teams-Nachricht
                </label>
                <label>
                    <input type="checkbox" id="notify-email">
                    ✉️ E-Mail
                </label>
            </div>
        </div>
        
        <button class="btn btn-primary" onclick="saveMassnahme()">
            Speichern & Benachrichtigen
        </button>
    </div>
</div>
```

---

## ⚙️ N8N WORKFLOWS

### Zu erstellen

| Workflow | Trigger | Funktion | Priorität |
|----------|---------|----------|-----------|
| NZA-Email-Import | Schedule (5 Min) | E-Mails aus nza@ importieren | 🟡 |
| NZA-Prozesse-API | Webhook GET | Liste für Dashboard laden | 🔴 |
| NZA-Update-Prozess | Webhook PATCH | Vorgang aktualisieren | 🔴 |
| NZA-Create-Prozess | Webhook POST | Neuen Vorgang anlegen | 🔴 |
| NZA-Massnahmen-API | Webhook GET/POST | Maßnahmen verwalten | 🔴 |
| NZA-Notify-Massnahme | Webhook POST | **Teams + E-Mail Benachrichtigung** | 🔴 |
| NZA-Bilder-API | Webhook GET/POST | **Bilder hochladen/abrufen** | 🔴 |
| NZA-Bilder-Upload | Webhook POST | **Bild in SharePoint speichern** | 🔴 |
| NZA-Mitarbeiter-API | Webhook GET | **Verursacher aus nza-mitarbeiter** | 🔴 |
| NZA-Material-API | Webhook GET/POST | Material-Verbrauch erfassen | 🟡 |
| NZA-Kosten-API | Webhook GET/POST | Kosten erfassen/abrufen | 🔴 |
| NZA-Kosten-Berechnung | Webhook POST | Auto-Berechnung Arbeitszeit | 🟡 |
| NZA-Generate-Formblatt | Webhook POST | F-QM-04 PDF generieren | 🟡 |
| NZA-KPI-Update | Schedule (Täglich) | KPIs berechnen und speichern | 🟢 |
| NZA-Config-API | Webhook GET | Config-Werte laden | 🟢 |

### Entfernt (nicht benötigt für NZA):
- ~~NZA-Schriftverkehr-API~~ → Schriftverkehr weniger relevant
- ~~NZA-Users-API (HR_CORE)~~ → Ersetzt durch nza-mitarbeiter Liste

---

### Workflow-Details: NZA-Notify-Massnahme

**Wichtig:** Teams-Benachrichtigung ist Kernfunktion!

**Nodes:**
1. Webhook Trigger (POST)
2. Code: Prepare Notification Data
3. IF: Check Notification Type
4. Branch A: Send Teams Message (Graph API)
5. Branch B: Send Email (Graph API)
6. Code: Update Massnahme (Benachrichtigung gesendet)
7. HTTP Request: Update SharePoint Item
8. Respond

**Teams Activity Notification:**
```javascript
// Graph API: Send Activity Notification
const teamsPayload = {
    topic: {
        source: "text",
        value: `Neue Maßnahme: ${massnahmeTitle}`,
        webUrl: dashboardUrl
    },
    activityType: "taskCreated",
    previewText: {
        content: `NZA ${nzaId}: ${beschreibung.substring(0, 100)}`
    },
    recipient: {
        "@odata.type": "microsoft.graph.aadUserNotificationRecipient",
        userId: verantwortlichId
    }
};
```

---

### Workflow-Details: NZA-Bilder-API

**Wichtig:** Bilder/Fotos sind zentral für NZA-Dokumentation!

**GET: Bilder zu einem NZA-Vorgang laden**
```
URL: /webhook/nza-bilder?nzaId=NZA-26001
Response: Array von Bild-URLs mit Thumbnails
```

**POST: Neues Bild hochladen**
```
URL: /webhook/nza-bilder-upload
Body: { nzaId, bildData (Base64), kategorie, beschreibung }
Response: { success, bildUrl, thumbnailUrl }
```

**Nodes für Upload:**
1. Webhook Trigger
2. Code: Decode Base64
3. HTTP Request: Create SharePoint Folder (falls nicht existiert)
4. HTTP Request: Upload File to SharePoint
5. HTTP Request: Create Thumbnail
6. HTTP Request: Create nza-bilder List Item
7. Respond

---

### Workflow-Details: NZA-Mitarbeiter-API

**Ersetzt HR_CORE Lookup - Daten aus SharePoint-Liste nza-mitarbeiter**

**GET: Alle aktiven Mitarbeiter**
```
URL: /webhook/nza-mitarbeiter
Response: Array von Mitarbeitern mit Kürzel, Name, KST
```

**GET: Mitarbeiter nach KST filtern**
```
URL: /webhook/nza-mitarbeiter?kst=F1
Response: Nur Mitarbeiter aus F1
```

**Code Node: Transform**
```javascript
const items = $input.first().json.value || [];

const mitarbeiter = items
    .filter(item => item.fields.Aktiv === true)
    .map(item => ({
        id: item.id,
        kuerzel: item.fields.Kuerzel,
        name: item.fields.Title,
        abteilung: item.fields.Abteilung,
        kst: item.fields.KST,
        schicht: item.fields.Schicht
    }))
    .sort((a, b) => a.name.localeCompare(b.name));

return { mitarbeiter, count: mitarbeiter.length };
```

---

## 📄 FORMBLÄTTER

### F-QM-04: Nacharbeits-/Ausschussmeldung

**Template:** `/mnt/HC_Volume_104189729/osp/rms/formulare/F_QM_04_Template.xlsx`

**Felder zum Befüllen:**

| Feld | SharePoint-Spalte |
|------|-------------------|
| NZA-Nr. | NZA_ID |
| Datum | Erfassungsdatum |
| Typ | NZA_Typ |
| Beschreibung | Beschreibung |
| Verursacher | Verursacher_Name |
| KST | KST_Betroffene |
| Artikel-Nr. | Artikel_Nr |
| Auftrags-Nr. | Auftrag_Nr |
| Menge betroffen | Menge_Betroffen |
| Menge Nacharbeit | Menge_Nacharbeit |
| Menge Ausschuss | Menge_Ausschuss |
| Kosten Material | Kosten_Material |
| Kosten Arbeitszeit | Kosten_Arbeitszeit |
| Kosten Gesamt | Kosten_Gesamt |
| Fehlerursache | Fehlerursache |

---

## 🔗 NGINX-KONFIGURATION

### Zu ergänzen in `/etc/nginx/sites-available/osp`

```nginx
# ============================================
# NZA DASHBOARD & API
# ============================================

# NZA Dashboard (Frontend)
location /nza/ {
    alias /var/www/html/nza/;
    try_files $uri $uri/ /nza/index.html;
}

# === NZA Prozesse (Hauptliste) ===
location = /api/nza/prozesse {
    proxy_pass http://127.0.0.1:5678/webhook/nza-prozesse;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

location = /api/nza/update {
    proxy_pass http://127.0.0.1:5678/webhook/nza-update;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

location = /api/nza/create {
    proxy_pass http://127.0.0.1:5678/webhook/nza-create;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

# === NZA Maßnahmen (mit Teams-Benachrichtigung) ===
location = /api/nza/massnahmen {
    proxy_pass http://127.0.0.1:5678/webhook/nza-massnahmen;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

location = /api/nza/notify {
    proxy_pass http://127.0.0.1:5678/webhook/nza-notify;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

# === NZA Bilder (WICHTIG!) ===
location = /api/nza/bilder {
    proxy_pass http://127.0.0.1:5678/webhook/nza-bilder;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

location = /api/nza/bilder-upload {
    proxy_pass http://127.0.0.1:5678/webhook/nza-bilder-upload;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    client_max_body_size 20M;  # Für Bild-Uploads
    add_header Access-Control-Allow-Origin * always;
}

# === NZA Mitarbeiter (Verursacher) ===
location = /api/nza/mitarbeiter {
    proxy_pass http://127.0.0.1:5678/webhook/nza-mitarbeiter;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

# === NZA Material ===
location = /api/nza/material {
    proxy_pass http://127.0.0.1:5678/webhook/nza-material;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

# === NZA Kosten ===
location = /api/nza/kosten {
    proxy_pass http://127.0.0.1:5678/webhook/nza-kosten;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

# === NZA Config ===
location = /api/nza/config {
    proxy_pass http://127.0.0.1:5678/webhook/nza-config;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

# === NZA KPIs ===
location = /api/nza/kpis {
    proxy_pass http://127.0.0.1:5678/webhook/nza-kpis;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin * always;
}

# === NZA Formblatt PDF ===
location = /api/nza/generate-formblatt {
    proxy_pass http://127.0.0.1:5678/webhook/nza-generate-formblatt;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 120s;
    add_header Access-Control-Allow-Origin * always;
}
```

---

## 🎨 DESIGN / CI

### Farben (Abgrenzung zu RMS)

| Element | RMS | NZA |
|---------|-----|-----|
| Primärfarbe | #2E7D32 (Grün) | #1565C0 (Blau) |
| Header-BG | #388E3C | #1976D2 |
| Akzent | #4CAF50 | #2196F3 |
| Status Neu | #FFC107 | #FFC107 |
| Status In Bearbeitung | #2196F3 | #FF9800 |
| Status Abgeschlossen | #4CAF50 | #4CAF50 |

### Logo/Header

```html
<header class="dashboard-header nza-header">
    <div class="header-content">
        <img src="img/logo.png" alt="Schneider Logo" class="logo">
        <div class="header-text">
            <h1>NZA Dashboard</h1>
            <p class="header-subtitle">Interne Nacharbeits- und Ausschussverwaltung</p>
        </div>
    </div>
</header>
```

---

## 📊 KOSTEN-KALKULATION

### Stundensätze (aus AV_AGK)

| Kostenstelle | Stundensatz |
|--------------|-------------|
| F1 (Vorfertigung) | 45,00 € |
| F2 (Montage) | 50,00 € |
| F3 (Endmontage) | 55,00 € |
| Prüffeld | 60,00 € |

### Berechnung

```javascript
function berechneKosten(zeitMinuten, kst, materialKosten = 0) {
    const stundensaetze = {
        'F1': 45.00,
        'F2': 50.00,
        'F3': 55.00,
        'Prüffeld': 60.00
    };
    
    const stundensatz = stundensaetze[kst] || 50.00;
    const arbeitszeitKosten = (zeitMinuten / 60) * stundensatz;
    const gesamtKosten = arbeitszeitKosten + materialKosten;
    
    return {
        kosten_arbeitszeit: Math.round(arbeitszeitKosten * 100) / 100,
        kosten_material: materialKosten,
        kosten_gesamt: Math.round(gesamtKosten * 100) / 100
    };
}
```

---

## 🔄 VERKNÜPFUNG RMS ↔ NZA

### Use Case 1: Kundenreklamation → NZA

```
1. Kunde reklamiert (RMS QA-26042)
2. Ursache: Interner Fehler
3. Button im RMS: "NZA anlegen"
4. NZA wird erstellt mit:
   - Bezug_RMS = "QA-26042"
   - Bezug_RMS_Typ = "Kunde"
   - Beschreibung = aus RMS übernommen
```

### Use Case 2: Lieferantenreklamation → NZA

```
1. Lieferant liefert Fehlmaterial (RMS QA-26043)
2. Nacharbeit nötig (Material ersetzen)
3. Button im RMS: "NZA für Kosten"
4. NZA wird erstellt mit:
   - Bezug_RMS = "QA-26043"
   - Bezug_RMS_Typ = "Lieferant"
   - Kosten werden erfasst → Weiterbelastung an Lieferant
```

### API für Verknüpfung

**Endpoint:** POST `/api/nza/create-from-rms`

```json
{
    "rmsQaId": "QA-26042",
    "rmsTyp": "Kunde",
    "nzaTyp": "Nacharbeit",
    "beschreibung": "Nacharbeit wegen Kundenreklamation",
    "kst": "F2"
}
```

---

## 📁 VERZEICHNISSTRUKTUR

### Auf Server

```
/mnt/HC_Volume_104189729/osp/
├── rms/                          # Bestehendes RMS
│   ├── docs/
│   ├── prompts/
│   ├── formulare/
│   └── ...
└── nza/                          # Neues NZA
    ├── docs/
    │   └── NZA_System_Kontext.md  # Diese Datei
    ├── prompts/
    │   └── CLAUDE_CODE_PROMPT_NZA.md
    ├── formulare/
    │   └── F_QM_04_Template.xlsx
    └── workflows/
        └── (n8n Workflow Exports)
```

### Frontend auf Server

```
/var/www/html/
├── rms/                          # RMS Dashboard
└── nza/                          # NZA Dashboard (neu)
    ├── index.html
    ├── css/
    │   └── style.css
    ├── js/
    │   ├── app.js
    │   ├── charts.js
    │   └── massnahmen-templates.js
    └── img/
        └── logo.png
```

---

## ✅ IMPLEMENTIERUNGS-CHECKLISTE

### Vorbereitung (VOR Claude Code)
- [ ] SharePoint-Site `/sites/nza` erstellen
- [ ] E-Mail-Postfach `nza@schneider-kabelsatzbau.de` einrichten
- [ ] F-QM-04 Template als XLSX vorbereiten
- [ ] HR_CORE Mitarbeiter-Daten für Import vorbereiten

### Phase 1: SharePoint-Listen erstellen
- [ ] nza-prozesse (Hauptliste)
- [ ] nza-massnahmen
- [ ] nza-bilder
- [ ] nza-mitarbeiter (aus HR_CORE importieren)
- [ ] nza-material
- [ ] nza-kosten
- [ ] nza-config (mit Initialwerten)
- [ ] nza-kpis
- [ ] nza-stammdaten (optional)

### Phase 2: Infrastruktur
- [ ] Frontend-Verzeichnis `/var/www/html/nza/` anlegen
- [ ] Nginx-Konfiguration ergänzen
- [ ] Basis-HTML/CSS/JS erstellen

### Phase 3: n8n Workflows (Priorität 🔴)
- [ ] NZA-Prozesse-API
- [ ] NZA-Update-Prozess
- [ ] NZA-Create-Prozess
- [ ] NZA-Massnahmen-API
- [ ] NZA-Notify-Massnahme (Teams + E-Mail)
- [ ] NZA-Bilder-API
- [ ] NZA-Bilder-Upload
- [ ] NZA-Mitarbeiter-API
- [ ] NZA-Kosten-API

### Phase 4: n8n Workflows (Priorität 🟡)
- [ ] NZA-Email-Import
- [ ] NZA-Material-API
- [ ] NZA-Kosten-Berechnung
- [ ] NZA-Generate-Formblatt

### Phase 5: n8n Workflows (Priorität 🟢)
- [ ] NZA-KPI-Update
- [ ] NZA-Config-API

### Phase 6: Frontend
- [ ] Dashboard mit KPIs
- [ ] Tabelle mit Filter/Suche/Sort/Pagination
- [ ] Detail-View Modal mit Tabs
- [ ] **Bilder-Galerie mit Upload**
- [ ] **Maßnahmen mit Teams-Benachrichtigung**
- [ ] Kosten-Erfassung
- [ ] Verursacher-Dropdown (aus nza-mitarbeiter)
- [ ] Charts

### Phase 7: Integration
- [ ] RMS → NZA Verknüpfung (Button)
- [ ] Zentrale QM-Seite
- [ ] Tests

---

## 📞 REFERENZEN

| Resource | Wert |
|----------|------|
| Server | 46.224.102.30 |
| n8n | http://127.0.0.1:5678 |
| SharePoint RMS | rainerschneiderkabelsatz.sharepoint.com/sites/rms |
| SharePoint NZA | rainerschneiderkabelsatz.sharepoint.com/sites/nza |
| n8n Credential | Fm3IuAbVYBYDIA4U |
| RMS Dashboard | https://osp.schneider-kabelsatzbau.de/rms/ |
| NZA Dashboard | https://osp.schneider-kabelsatzbau.de/nza/ |

---

*Erstellt: 2026-01-29*  
*Für Implementierung: 2026-01-30*
