"""
Kontakt-WKZ Lookup für Open WebUI Pipeline
==========================================

Schneller JSON-basierter Lookup für Kontaktnummern.
Wird VOR der RAG-Verarbeitung aufgerufen für sofortige Antworten
bei exakten Kontaktnummer-Anfragen.

Autor: AL
Stand: 2025-12-13
Deployment: /mnt/HC_Volume_104189729/osp/modules/kontakt_lookup.py
"""

import re
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Kontaktnummer-Pattern (10-stellig, VT-Satz Format)
# Beispiele: 0010129205, 0010916001, 0011111201
KONTAKT_PATTERN = r'\b\d{10}\b'

# Lookup-Datei Pfad
LOOKUP_PATH = Path('/mnt/HC_Volume_104189729/osp/lookups/kontakt_wkz_mapping.json')

# Cache für wiederholte Anfragen
_lookup_cache: Optional[Dict] = None


def _load_lookup_data() -> Dict:
    """
    Lädt die Lookup-Daten mit Caching.
    
    Returns:
        Dict mit Mapping-Daten
    
    Raises:
        FileNotFoundError: Wenn Lookup-Datei nicht existiert
    """
    global _lookup_cache
    
    if _lookup_cache is not None:
        return _lookup_cache
    
    try:
        with open(LOOKUP_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _lookup_cache = data
            logger.info(f"✅ Lookup-Daten geladen: {data['meta']['eintraege_gesamt']} Einträge")
            return data
    except FileNotFoundError:
        logger.warning(f"⚠️ Lookup-Datei nicht gefunden: {LOOKUP_PATH}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON Parse Error: {e}")
        raise


def check_kontakt_lookup(user_message: str) -> Optional[str]:
    """
    Prüft ob eine Kontaktnummer in der Nachricht enthalten ist
    und führt ggf. einen JSON-Lookup durch.
    
    Diese Funktion sollte VOR der RAG-Verarbeitung aufgerufen werden.
    Bei einem Treffer wird die Antwort direkt zurückgegeben (kein RAG nötig).
    
    Parameters:
        user_message: Die User-Eingabe
    
    Returns:
        Formatierte Antwort bei Kontaktnummer-Fund
        None wenn keine Kontaktnummer erkannt oder Lookup nicht verfügbar
    
    Examples:
        >>> check_kontakt_lookup("Welches WKZ für 0-0350415-1?")
        '**Werkzeug für Kontakt 0-0350415-1:**\\n...'
        
        >>> check_kontakt_lookup("Zeige mir alle Maschinen")
        None  # Kein Kontaktnummer-Pattern → RAG übernimmt
    """
    # Pattern-Suche
    match = re.search(KONTAKT_PATTERN, user_message)
    if not match:
        return None  # Keine Kontaktnummer → weiter zu RAG
    
    kontakt_nr = match.group()
    logger.info(f"🔍 Kontaktnummer erkannt: {kontakt_nr}")
    
    try:
        data = _load_lookup_data()
        
        if kontakt_nr in data['mappings']:
            entry = data['mappings'][kontakt_nr]
            logger.info(f"✅ Lookup-Treffer für {kontakt_nr}")
            return format_wkz_response(kontakt_nr, entry)
        else:
            # Kontaktnummer erkannt, aber nicht in DB
            logger.warning(f"⚠️ Kontaktnummer {kontakt_nr} nicht in Lookup-Datenbank")
            return f"""⚠️ **Kontaktnummer {kontakt_nr} nicht in der Datenbank gefunden.**

Mögliche Ursachen:
- Neue Kontaktnummer (noch nicht dokumentiert)
- Tippfehler in der Nummer
- Kontakt wird nicht bei Schneider verarbeitet

**Nächste Schritte:**
1. Prüfen Sie die Nummer in TM_WKZ_Werkzeuge.md
2. Bei neuen Kontakten: MD oder AL kontaktieren

(C: 0%) [OSP-Lookup]"""

    except FileNotFoundError:
        # Fallback: Lookup nicht verfügbar → RAG übernimmt
        logger.warning("Lookup nicht verfügbar, Fallback zu RAG")
        return None
    except Exception as e:
        logger.error(f"Lookup-Fehler: {e}")
        return None  # Bei Fehler: RAG übernimmt


def format_wkz_response(kontakt_nr: str, entries) -> str:
    """
    Formatiert die Lookup-Antwort im OSP-Standard-Format.

    Parameters:
        kontakt_nr: Die gefundene Kontaktnummer
        entries: Liste von Dicts mit Werkzeug-Daten (eine Kontaktnummer kann mehrere WKZ haben)

    Returns:
        Formatierte Markdown-Antwort
    """
    # Stand aus Cache holen
    stand = _lookup_cache['meta']['stand'] if _lookup_cache else 'unbekannt'

    # Sicherstellen dass entries eine Liste ist
    if not isinstance(entries, list):
        entries = [entries]

    if len(entries) == 1:
        # Einzelnes WKZ
        entry = entries[0]
        bemerkung = entry.get('bemerkung') or 'keine'
        response = f"""**Werkzeug für Kontakt {kontakt_nr}:**

| Eigenschaft | Wert |
|-------------|------|
| **WKZ** | {entry.get('wkz', 'N/A')} |
| **Typ** | {entry.get('wkz_typ', 'N/A')} |
| **VT-Satz** | {entry.get('vt_satz', 'N/A')} |
| **Hersteller** | {entry.get('hersteller', 'N/A') or 'N/A'} |
| **Kontaktbezeichnung** | {entry.get('kontakt_bezeichnung', 'N/A') or 'N/A'} |
| **Querschnitt** | {entry.get('querschnitt', 'N/A') or 'N/A'} |
| **Standort** | {entry.get('standort', 'N/A')} |
| **Bemerkung** | {bemerkung} |

**Quelle:** TM_WKZ_Werkzeuge.md (Stand: {stand})

(C: 100%) [OSP-Lookup]"""
    else:
        # Mehrere WKZ für dieselbe Kontaktnummer
        response = f"""**Werkzeuge für Kontakt {kontakt_nr}:**

⚠️ *{len(entries)} verschiedene WKZ-Zuordnungen gefunden:*

"""
        for i, entry in enumerate(entries, 1):
            bemerkung = entry.get('bemerkung') or 'keine'
            response += f"""**Option {i}: {entry.get('wkz', 'N/A')}**
| Eigenschaft | Wert |
|-------------|------|
| **Typ** | {entry.get('wkz_typ', 'N/A')} |
| **VT-Satz** | {entry.get('vt_satz', 'N/A')} |
| **Standort** | {entry.get('standort', 'N/A')} |
| **Bemerkung** | {bemerkung} |

"""
        response += f"""**Quelle:** TM_WKZ_Werkzeuge.md (Stand: {stand})

(C: 100%) [OSP-Lookup]"""

    return response


def get_lookup_stats() -> Dict[str, Any]:
    """
    Gibt Statistiken über die Lookup-Datenbank zurück.
    
    Returns:
        Dict mit Meta-Informationen
    """
    try:
        data = _load_lookup_data()
        return {
            "verfügbar": True,
            "version": data['meta']['version'],
            "stand": data['meta']['stand'],
            "eintraege": data['meta']['eintraege_gesamt'],
            "kontakte_unique": data['meta']['kontakte_unique'],
            "quelle": data['meta']['quelle']
        }
    except Exception:
        return {
            "verfügbar": False,
            "grund": "Lookup-Datei nicht gefunden oder fehlerhaft"
        }


def reload_lookup_cache() -> bool:
    """
    Erzwingt ein Neuladen der Lookup-Daten.
    Nützlich nach Updates der JSON-Datei.
    
    Returns:
        True bei Erfolg, False bei Fehler
    """
    global _lookup_cache
    _lookup_cache = None
    
    try:
        _load_lookup_data()
        return True
    except Exception:
        return False


# Für direkten Test
if __name__ == "__main__":
    # Test-Modus
    logging.basicConfig(level=logging.INFO)
    
    print("=== Kontakt-Lookup Test ===\n")
    
    # Stats
    stats = get_lookup_stats()
    print(f"Status: {stats}\n")
    
    # Test-Anfragen
    test_queries = [
        "Welches WKZ für 0-0350415-1?",
        "Zeige mir alle Maschinen",  # Kein Kontakt
        "Kontakt 0-0282110-1 Details",
        "0-9999999-9 nicht vorhanden",  # Unbekannt
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        result = check_kontakt_lookup(query)
        if result:
            print(f"Result:\n{result}\n")
        else:
            print("Result: None (→ RAG)\n")
