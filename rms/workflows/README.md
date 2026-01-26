# RMS n8n Workflows

**Status:** In Entwicklung
**Plattform:** n8n (Self-hosted auf Hetzner)

## Geplante Workflows

| Workflow | Beschreibung | Trigger |
|----------|--------------|---------|
| `rms_email_import.json` | E-Mail-Reklamationen erfassen | IMAP Polling |
| `rms_formblatt_generator.json` | KI-gestützte Formblatt-Ausfüllung | Webhook |
| `rms_alarm_eskalation.json` | Alarme bei kritischen Reklamationen | Cron/Event |
| `rms_sharepoint_sync.json` | Synchronisation mit SharePoint | Scheduled |

## Import in n8n

1. n8n Dashboard öffnen (localhost:5678)
2. Workflows → Import from File
3. JSON-Datei auswählen
4. Credentials konfigurieren

## Credentials (benötigt)

- `sharepoint_oauth2` - SharePoint API Zugriff
- `anthropic_api` - Claude API Key
- `smtp_email` - E-Mail Versand

---

*Teil des RMS-Systems | Stand: 2026-01-26*
