"""
Kontakt-WKZ Lookup fuer Open WebUI Pipeline
============================================

Schneller JSON-basierter Lookup fuer Kontaktnummern.
Wird VOR der RAG-Verarbeitung aufgerufen fuer sofortige Antworten
bei exakten Kontaktnummer-Anfragen.

WICHTIG: Verwendet direkten Key-Lookup statt Regex-Pattern,
da Kontaktnummern sehr unterschiedliche Formate haben:
- TE-Format: 0-0141075-2
- Stocko: 25004
- RSB: RSB 7603 MS
- Mit Slash: 0-0163081-7/8
- 10-stellig: 0010129205

Autor: AL
Stand: 2025-12-14
Version: 2.0 (Multi-Format Support)
Deployment: /opt/osp/pipelines/modules/kontakt_lookup.py
"""

import json
import logging
import re
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

# Lookup-Datei Pfade (Fallback-Kette)
LOOKUP_PATHS = [
    Path('/opt/osp/lookups/kontakt_wkz_mapping.json'),
    Path('/mnt/HC_Volume_104189729/osp/lookups/kontakt_wkz_mapping.json'),
    Path('/app/backend/data/lookups/kontakt_wkz_mapping.json'),
]

# Cache fuer wiederholte Anfragen
_lookup_cache: Optional[Dict] = None
_kontakt_keys: Optional[List[str]] = None


def _find_lookup_file() -> Optional[Path]:
    """Findet die Lookup-Datei in der Fallback-Kette."""
    for path in LOOKUP_PATHS:
        if path.exists():
            return path
    return None


def _load_lookup_data() -> Dict:
    """
    Laedt die Lookup-Daten mit Caching.

    Returns:
        Dict mit Mapping-Daten

    Raises:
        FileNotFoundError: Wenn Lookup-Datei nicht existiert
    """
    global _lookup_cache, _kontakt_keys

    if _lookup_cache is not None:
        return _lookup_cache

    lookup_path = _find_lookup_file()
    if lookup_path is None:
        logger.warning(f"Lookup-Datei nicht gefunden in: {LOOKUP_PATHS}")
        raise FileNotFoundError("Lookup-Datei nicht gefunden")

    try:
        with open(lookup_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _lookup_cache = data
            # Kontakt-Keys fuer schnellen Lookup cachen
            # Sortiert nach Laenge (laengste zuerst) fuer praezisere Matches
            _kontakt_keys = sorted(
                data['mappings'].keys(),
                key=len,
                reverse=True
            )
            logger.info(
                f"Lookup-Daten geladen: {data['meta']['eintraege_gesamt']} Eintraege "
                f"aus {lookup_path}"
            )
            return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON Parse Error: {e}")
        raise


def _find_kontakt_in_message(message: str) -> Optional[str]:
    """
    Sucht eine bekannte Kontaktnummer in der Nachricht.

    Verwendet direkten String-Match gegen alle bekannten Kontaktnummern
    aus dem JSON. Dies ist robuster als Regex, da die Formate sehr
    unterschiedlich sind.

    Parameters:
        message: Die User-Nachricht

    Returns:
        Gefundene Kontaktnummer oder None
    """
    global _kontakt_keys

    if _kontakt_keys is None:
        _load_lookup_data()

    # Nachricht normalisieren (fuer besseren Match)
    msg_upper = message.upper()

    # Durchsuche alle bekannten Kontaktnummern
    if _kontakt_keys is None:
        return None
    for kontakt in _kontakt_keys:
        # Case-insensitive Match
        if kontakt.upper() in msg_upper:
            # Stelle sicher, dass es ein "ganzes Wort" ist
            # (nicht Teil einer laengeren Zeichenkette)
            pattern = re.escape(kontakt)
            if re.search(rf'(?<![0-9a-zA-Z]){pattern}(?![0-9a-zA-Z])', message, re.IGNORECASE):
                return kontakt

    return None


def check_kontakt_lookup(user_message: str) -> Optional[str]:
    """
    Prueft ob eine Kontaktnummer in der Nachricht enthalten ist
    und fuehrt ggf. einen JSON-Lookup durch.

    Diese Funktion sollte VOR der RAG-Verarbeitung aufgerufen werden.
    Bei einem Treffer wird die Antwort direkt zurueckgegeben (kein RAG noetig).

    Parameters:
        user_message: Die User-Eingabe

    Returns:
        Formatierte Antwort bei Kontaktnummer-Fund
        None wenn keine Kontaktnummer erkannt oder Lookup nicht verfuegbar

    Examples:
        >>> check_kontakt_lookup("Welches WKZ fuer 0-0350415-1?")
        '**Werkzeug fuer Kontakt 0-0350415-1:**\\n...'

        >>> check_kontakt_lookup("Zeige mir alle Maschinen")
        None  # Keine Kontaktnummer -> RAG uebernimmt
    """
    try:
        # Kontaktnummer in Nachricht suchen
        kontakt_nr = _find_kontakt_in_message(user_message)

        if kontakt_nr is None:
            return None  # Keine Kontaktnummer -> weiter zu RAG

        logger.info(f"Kontaktnummer erkannt: {kontakt_nr}")

        data = _load_lookup_data()

        if kontakt_nr in data['mappings']:
            entries = data['mappings'][kontakt_nr]
            logger.info(f"Lookup-Treffer fuer {kontakt_nr}: {len(entries) if isinstance(entries, list) else 1} WKZ")
            return format_wkz_response(kontakt_nr, entries)
        else:
            # Sollte nicht passieren, da wir nur bekannte Keys suchen
            logger.warning(f"Kontaktnummer {kontakt_nr} nicht in Mappings (unerwartet)")
            return None

    except FileNotFoundError:
        logger.warning("Lookup nicht verfuegbar, Fallback zu RAG")
        return None
    except Exception as e:
        logger.error(f"Lookup-Fehler: {e}")
        return None


def format_wkz_response(kontakt_nr: str, entries) -> str:
    """
    Formatiert die Lookup-Antwort im OSP-Standard-Format.

    Parameters:
        kontakt_nr: Die gefundene Kontaktnummer
        entries: Liste von Dicts mit Werkzeug-Daten

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
        hersteller = entry.get('hersteller') or 'N/A'
        kontakt_bez = entry.get('kontakt_bezeichnung') or 'N/A'
        querschnitt = entry.get('querschnitt') or 'N/A'

        response = f"""**Werkzeug fuer Kontakt {kontakt_nr}:**

| Eigenschaft | Wert |
|-------------|------|
| **WKZ** | {entry.get('wkz', 'N/A')} |
| **Typ** | {entry.get('wkz_typ', 'N/A')} |
| **VT-Satz** | {entry.get('vt_satz') or 'N/A'} |
| **Hersteller** | {hersteller} |
| **Kontaktbezeichnung** | {kontakt_bez} |
| **Querschnitt** | {querschnitt} |
| **Standort** | {entry.get('standort') or 'N/A'} |
| **Bemerkung** | {bemerkung} |

**Quelle:** TM_WKZ_Werkzeuge.md (Stand: {stand})

(C: 100%) [OSP-Lookup]"""
    else:
        # Mehrere WKZ fuer dieselbe Kontaktnummer
        response = f"""**Werkzeuge fuer Kontakt {kontakt_nr}:**

*{len(entries)} verschiedene WKZ-Zuordnungen gefunden:*

| WKZ | Typ | VT-Satz | Standort | Bemerkung |
|-----|-----|---------|----------|-----------|
"""
        for entry in entries:
            wkz = entry.get('wkz', 'N/A')
            typ = entry.get('wkz_typ', 'N/A')
            vt = entry.get('vt_satz') or 'N/A'
            standort = entry.get('standort') or 'N/A'
            bemerkung = entry.get('bemerkung') or '-'
            response += f"| {wkz} | {typ} | {vt} | {standort} | {bemerkung} |\n"

        response += f"""
**Quelle:** TM_WKZ_Werkzeuge.md (Stand: {stand})

(C: 100%) [OSP-Lookup]"""

    return response


def get_lookup_stats() -> Dict[str, Any]:
    """
    Gibt Statistiken ueber die Lookup-Datenbank zurueck.

    Returns:
        Dict mit Meta-Informationen
    """
    try:
        data = _load_lookup_data()
        return {
            "verfuegbar": True,
            "version": data['meta']['version'],
            "stand": data['meta']['stand'],
            "eintraege": data['meta']['eintraege_gesamt'],
            "kontakte_unique": data['meta']['kontakte_unique'],
            "quelle": data['meta']['quelle']
        }
    except Exception as e:
        return {
            "verfuegbar": False,
            "grund": str(e)
        }


def reload_lookup_cache() -> bool:
    """
    Erzwingt ein Neuladen der Lookup-Daten.
    Nuetzlich nach Updates der JSON-Datei.

    Returns:
        True bei Erfolg, False bei Fehler
    """
    global _lookup_cache, _kontakt_keys
    _lookup_cache = None
    _kontakt_keys = None

    try:
        _load_lookup_data()
        return True
    except Exception:
        return False


# Fuer direkten Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=== Kontakt-Lookup Test (v2.0) ===\n")

    # Stats
    stats = get_lookup_stats()
    print(f"Status: {stats}\n")

    # Test-Anfragen mit verschiedenen Formaten
    test_queries = [
        # TE-Format
        ("TE-Format", "Welches WKZ fuer 0-0141075-2?"),
        # Stocko (5-stellig)
        ("Stocko", "Kontakt 25004 welches Werkzeug?"),
        # RSB-Prefix
        ("RSB", "WKZ fuer RSB 7603 MS"),
        # Mit Slash
        ("Mit Slash", "0-0163081-7/8 welches WKZ?"),
        # 10-stellig
        ("10-stellig", "Werkzeug fuer 0010129205"),
        # Kein Kontakt
        ("Kein Kontakt", "Zeige mir alle Maschinen"),
    ]

    for format_name, query in test_queries:
        print(f"[{format_name}] Query: {query}")
        result = check_kontakt_lookup(query)
        if result:
            # Nur erste Zeilen zeigen
            lines = result.split('\n')[:5]
            print(f"Result: {chr(10).join(lines)}...")
        else:
            print("Result: None (-> RAG)")
        print()
