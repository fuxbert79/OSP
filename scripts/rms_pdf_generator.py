#!/usr/bin/env python3
"""
RMS PDF Generator fuer F-QM-02 Qualitaetsabweichung
Verwendet vorhandenes JSON-Schema zur Validierung

Endpoints:
  GET  /health       - Status pruefen
  GET  /schema       - JSON-Schema abrufen
  POST /generate-pdf - PDF generieren
  POST /validate     - Daten validieren

Autor: AL (QM & KI-Manager)
Version: 1.0.0
Erstellt: 2026-01-27
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import re
from datetime import datetime
import logging

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# WeasyPrint und Jinja2 imports
try:
    from weasyprint import HTML
    from jinja2 import Environment, FileSystemLoader
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    logger.warning("WeasyPrint nicht installiert. Installiere mit: pip install weasyprint jinja2")

# Pfade
TEMPLATE_DIR = "/opt/osp/templates"
OUTPUT_DIR = "/opt/osp/output"
SCHEMA_PATH = "/mnt/HC_Volume_104189729/osp/rms/formulare/f_qm_02_qualitaetsabweichung/F_QM_02_Schema.json"

# Schema laden fuer Validierung
def load_schema():
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Schema nicht gefunden: {SCHEMA_PATH}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Schema JSON-Fehler: {e}")
        return None

SCHEMA = load_schema()


def validate_data(data):
    """Validiert Daten gegen das JSON-Schema (einfache Pruefung)"""
    errors = []

    # Pflichtfelder pruefen
    required_fields = ['datum', 'lieferant_firma', 'artikel_nr_schneider',
                       'artikel_bezeichnung', 'lieferschein_nr', 'beschreibung']

    for field in required_fields:
        if not data.get(field):
            errors.append(f"Pflichtfeld fehlt: {field}")

    # Beschreibung mindestens 50 Zeichen
    if data.get('beschreibung') and len(data['beschreibung']) < 50:
        errors.append("Beschreibung muss mindestens 50 Zeichen haben")

    # Mindestens eine Massnahme
    if not data.get('massnahmen') or len(data.get('massnahmen', [])) == 0:
        errors.append("Mindestens eine Massnahme muss ausgewaehlt werden")

    # Abweichungs-Nr Format pruefen (wenn angegeben)
    if data.get('abweichungs_nr'):
        if not re.match(r'^QA-\d{4}-\d{3}$', data['abweichungs_nr']):
            errors.append("Abweichungs-Nr muss Format QA-YYYY-NNN haben")

    # Datum-Format pruefen
    if data.get('datum'):
        try:
            datetime.strptime(data['datum'], '%Y-%m-%d')
        except ValueError:
            errors.append("Datum muss Format YYYY-MM-DD haben")

    return errors


def generate_pdf(data, return_base64=False):
    """Generiert PDF aus den Formulardaten

    Args:
        data: Formulardaten
        return_base64: Wenn True, wird der PDF-Inhalt als Base64 zurueckgegeben
    """
    import base64

    if not WEASYPRINT_AVAILABLE:
        return None, None, "WeasyPrint nicht verfuegbar"

    # Template laden
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    try:
        template = env.get_template('F_QM_02_template.html')
    except Exception as e:
        return None, f"Template-Fehler: {str(e)}"

    # Defaults setzen
    if not data.get('abweichungs_nr'):
        year = datetime.now().year
        data['abweichungs_nr'] = f"QA-{year}-XXX"  # Wird spaeter ersetzt

    if not data.get('datum'):
        data['datum'] = datetime.now().strftime('%Y-%m-%d')

    if not data.get('ersteller'):
        data['ersteller'] = 'System'

    # Leere Felder mit Defaults fuellen
    defaults = {
        'lieferant_ansprechpartner': '',
        'lieferant_telefon': '',
        'lieferant_email': '',
        'artikel_nr_lieferant': '',
        'lieferdatum': '',
        'liefermenge': '',
        'beanstandungsmenge': '',
        'massnahmen': []
    }
    for key, default in defaults.items():
        if key not in data or data[key] is None:
            data[key] = default

    # Mengen formatieren
    if isinstance(data.get('liefermenge'), dict):
        data['liefermenge'] = f"{data['liefermenge'].get('wert', '')} {data['liefermenge'].get('einheit', '')}"
    if isinstance(data.get('beanstandungsmenge'), dict):
        data['beanstandungsmenge'] = f"{data['beanstandungsmenge'].get('wert', '')} {data['beanstandungsmenge'].get('einheit', '')}"

    # HTML rendern
    try:
        html_content = template.render(**data)
    except Exception as e:
        return None, f"Template-Rendering-Fehler: {str(e)}"

    # PDF generieren
    filename = f"F-QM-02_{data['abweichungs_nr']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Sicherstellen dass Output-Verzeichnis existiert
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # PDF schreiben
    try:
        pdf_document = HTML(string=html_content, base_url=TEMPLATE_DIR)
        pdf_bytes = pdf_document.write_pdf()

        # In Datei schreiben
        with open(filepath, 'wb') as f:
            f.write(pdf_bytes)

        # Optional: Base64-Encoding fuer API-Response
        pdf_base64 = None
        if return_base64:
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    except Exception as e:
        return None, None, f"PDF-Generierung fehlgeschlagen: {str(e)}"

    logger.info(f"PDF erstellt: {filepath}")
    return filepath, pdf_base64, None


class PDFHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        logger.info(f"{self.client_address[0]} - {format % args}")

    def _send_json(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/health':
            self._send_json(200, {
                'status': 'ok',
                'service': 'RMS PDF Generator',
                'version': '1.0.0',
                'weasyprint': WEASYPRINT_AVAILABLE,
                'schema_loaded': SCHEMA is not None,
                'template_dir': TEMPLATE_DIR,
                'output_dir': OUTPUT_DIR
            })
        elif self.path == '/schema':
            if SCHEMA:
                self._send_json(200, SCHEMA)
            else:
                self._send_json(404, {'error': 'Schema nicht geladen'})
        else:
            self._send_json(404, {'error': 'Endpoint nicht gefunden'})

    def do_POST(self):
        if self.path == '/generate-pdf':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    self._send_json(400, {'success': False, 'error': 'Kein Request-Body'})
                    return

                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                # Validieren
                errors = validate_data(data)
                if errors:
                    self._send_json(400, {
                        'success': False,
                        'errors': errors
                    })
                    return

                # PDF generieren (mit Base64 wenn angefragt)
                return_base64 = data.get('return_base64', False)
                filepath, pdf_base64, error = generate_pdf(data, return_base64=return_base64)

                if error:
                    self._send_json(500, {
                        'success': False,
                        'error': error
                    })
                    return

                response = {
                    'success': True,
                    'filepath': filepath,
                    'filename': os.path.basename(filepath)
                }

                # Base64-Inhalt hinzufuegen wenn angefragt
                if return_base64 and pdf_base64:
                    response['content_base64'] = pdf_base64

                self._send_json(200, response)

            except json.JSONDecodeError as e:
                self._send_json(400, {'success': False, 'error': f'Ungueltiges JSON: {str(e)}'})
            except Exception as e:
                logger.exception("Unerwarteter Fehler bei PDF-Generierung")
                self._send_json(500, {'success': False, 'error': str(e)})

        elif self.path == '/validate':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    self._send_json(400, {'error': 'Kein Request-Body'})
                    return

                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                errors = validate_data(data)

                self._send_json(200, {
                    'valid': len(errors) == 0,
                    'errors': errors
                })
            except Exception as e:
                self._send_json(500, {'error': str(e)})

        else:
            self._send_json(404, {'error': 'Endpoint nicht gefunden'})


def main():
    port = int(os.environ.get('PDF_GENERATOR_PORT', 5001))
    server = HTTPServer(('0.0.0.0', port), PDFHandler)

    print(f"""
{'='*65}
  RMS PDF Generator - F-QM-02 Qualitaetsabweichung
{'='*65}
  Port:        {port}
  WeasyPrint:  {'Verfuegbar' if WEASYPRINT_AVAILABLE else 'NICHT INSTALLIERT'}
  Schema:      {'Geladen' if SCHEMA else 'Nicht gefunden'}
  Templates:   {TEMPLATE_DIR}
  Output:      {OUTPUT_DIR}
{'='*65}
  Endpoints:
    GET  /health       - Status pruefen
    GET  /schema       - JSON-Schema abrufen
    POST /generate-pdf - PDF generieren
    POST /validate     - Daten validieren
{'='*65}
  Starte Server auf Port {port}...
""")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gestoppt.")
        server.shutdown()


if __name__ == "__main__":
    main()
