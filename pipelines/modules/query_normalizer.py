"""
OSP Query-Normalisierung
=========================
Normalisiert Benutzer-Queries für bessere RAG-Ergebnisse.

Stufen:
1. Basis: Case, Whitespace, Sonderzeichen
2. Umlaut: ä↔ae, ö↔oe, ü↔ue Varianten
3. Tippfehler: Bekannte Korrekturen aus JSON

Version: 1.0
Datum: 2025-12-15
"""

import json
import re
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger("osp.query_normalizer")


class QueryNormalizer:
    """Normalisiert Queries für bessere RAG-Ergebnisse."""

    def __init__(self, corrections_path: str = "/app/backend/data/lookups/typo_corrections.json"):
        self.corrections_path = Path(corrections_path)
        self.corrections = {}
        self.umlaut_map = {}
        self._loaded = False
        self._load_corrections()

    def _load_corrections(self):
        """Lädt Tippfehler-Korrekturen aus JSON."""
        # Versuche mehrere Pfade
        paths_to_try = [
            self.corrections_path,
            Path("/opt/osp/lookups/typo_corrections.json"),
            Path("/app/backend/data/lookups/typo_corrections.json")
        ]

        for path in paths_to_try:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.corrections = data.get("corrections", {})
                    self.umlaut_map = data.get("umlaut_variants", {})
                    self._loaded = True
                    logger.info(f"✅ Typo-Korrekturen geladen: {len(self.corrections)} Einträge von {path}")
                    return
                except Exception as e:
                    logger.warning(f"⚠️ Fehler beim Laden von {path}: {e}")

        logger.warning("⚠️ Keine Typo-Korrekturen gefunden - nur Basis-Normalisierung aktiv")

    def normalize(self, query: str) -> Tuple[str, bool, list]:
        """
        Normalisiert eine Query.

        Returns:
            Tuple (normalisierte_query, wurde_geändert, liste_der_änderungen)
        """
        if not query or not query.strip():
            return query, False, []

        original = query
        changes = []

        # STUFE 1: Basis-Normalisierung
        normalized = self._normalize_base(query)
        if normalized != query.lower():
            changes.append("basis")

        # STUFE 2: Tippfehler-Korrektur (Wort für Wort)
        words = normalized.split()
        corrected_words = []

        for word in words:
            # Einzelwort-Korrektur
            if word in self.corrections:
                corrected_words.append(self.corrections[word])
                changes.append(f"typo:{word}→{self.corrections[word]}")
            else:
                corrected_words.append(word)

        normalized = ' '.join(corrected_words)

        # STUFE 2b: Mehrwort-Phrasen korrigieren
        for typo, correction in self.corrections.items():
            if ' ' in typo and typo in normalized:
                normalized = normalized.replace(typo, correction)
                changes.append(f"phrase:{typo}→{correction}")

        # STUFE 3: Umlaut-Normalisierung (ae→ä, etc.)
        normalized = self._normalize_umlauts(normalized)

        was_changed = normalized != original.lower()

        if was_changed:
            logger.debug(f"📝 Query normalisiert: '{original}' → '{normalized}'")

        return normalized, was_changed, changes

    def _normalize_base(self, query: str) -> str:
        """Basis-Normalisierung: Case, Whitespace."""
        # Lowercase
        normalized = query.lower()

        # Mehrfache Leerzeichen entfernen
        normalized = ' '.join(normalized.split())

        # Fragezeichen am Ende behalten (für Pattern-Matching)
        # Aber andere Sonderzeichen normalisieren
        normalized = re.sub(r'[^\w\säöüß\-\?\.]', ' ', normalized)
        normalized = ' '.join(normalized.split())

        return normalized

    def _normalize_umlauts(self, text: str) -> str:
        """
        Normalisiert Umlaut-Varianten.
        ae→ä, oe→ö, ue→ü (aber nicht in allen Kontexten!)
        """
        # Nur am Wortanfang oder nach Konsonanten
        # "aendern" → "ändern", aber "traeger" bleibt

        # Einfache Variante: Bekannte Wörter mit ae/oe/ue ersetzen
        umlaut_words = {
            "aendern": "ändern",
            "aenderung": "änderung",
            "uebersicht": "übersicht",
            "ueberpruefung": "überprüfung",
            "pruefung": "prüfung",
            "pruefmittel": "prüfmittel",
            "geraet": "gerät",
            "geraete": "geräte",
            "qualitaet": "qualität",
            "qualitaets": "qualitäts",
            "zustaendig": "zuständig",
            "zustaendigkeit": "zuständigkeit",
            "groesse": "größe",
            "hoehe": "höhe",
            "laenge": "länge",
            "waerme": "wärme",
        }

        words = text.split()
        result = []

        for word in words:
            if word in umlaut_words:
                result.append(umlaut_words[word])
            else:
                result.append(word)

        return ' '.join(result)

    def get_stats(self) -> dict:
        """Gibt Statistiken zurück."""
        return {
            "verfügbar": self._loaded,
            "corrections_count": len(self.corrections),
            "umlaut_variants": len(self.umlaut_map)
        }


# ═══════════════════════════════════════════════════════════════════════
# SINGLETON & CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

_normalizer: Optional[QueryNormalizer] = None


def get_normalizer(corrections_path: Optional[str] = None) -> QueryNormalizer:
    """Gibt Singleton-Instanz zurück."""
    global _normalizer
    if _normalizer is None:
        _normalizer = QueryNormalizer(corrections_path or "/app/backend/data/lookups/typo_corrections.json")
    return _normalizer


def normalize_query(query: str, corrections_path: Optional[str] = None) -> str:
    """
    Convenience-Funktion für Query-Normalisierung.

    Verwendung in Pipeline:
        from query_normalizer import normalize_query
        normalized = normalize_query(user_message)
    """
    normalizer = get_normalizer(corrections_path)
    normalized, _, _ = normalizer.normalize(query)
    return normalized


def normalize_query_with_info(query: str) -> Tuple[str, bool, list]:
    """Wie normalize_query, aber mit Details zu Änderungen."""
    normalizer = get_normalizer()
    return normalizer.normalize(query)


# ═══════════════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════════════

def run_tests():
    """Führt Test-Suite aus."""
    print("\n" + "="*60)
    print("OSP Query-Normalizer - TEST")
    print("="*60 + "\n")

    # Test mit lokaler JSON
    import tempfile
    test_corrections = {
        "corrections": {
            "mitarbieter": "mitarbeiter",
            "maschinne": "maschine",
            "werkezug": "werkzeug",
            "alfa": "alpha",
            "komax alfa": "komax alpha"
        },
        "umlaut_variants": {"ae": "ä", "oe": "ö", "ue": "ü"}
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_corrections, f)
        test_path = f.name

    try:
        normalizer = QueryNormalizer(test_path)

        test_cases = [
            # (Input, Expected Contains, Beschreibung)
            ("Mitarbieter AL", "mitarbeiter", "Tippfehler korrigiert"),
            ("KOMAX ALFA 530", "komax alpha", "Case + Tippfehler"),
            ("  Mehrere   Leerzeichen  ", "mehrere leerzeichen", "Whitespace"),
            ("Maschinne Wartung", "maschine", "Tippfehler Maschine"),
            ("Werkezug 602", "werkzeug", "Tippfehler Werkzeug"),
            ("Qualität prüfen", "qualität", "Umlaute erhalten"),
            ("Normale Anfrage", "normale anfrage", "Keine Änderung nötig"),
        ]

        passed = 0
        failed = 0

        for query, expected, description in test_cases:
            normalized, changed, changes = normalizer.normalize(query)

            if expected in normalized:
                status = "✅ PASS"
                passed += 1
            else:
                status = "❌ FAIL"
                failed += 1

            print(f"{status} | {description}")
            print(f"        Input:  '{query}'")
            print(f"        Output: '{normalized}'")
            if changes:
                print(f"        Changes: {changes}")
            print()

        print("="*60)
        print(f"ERGEBNIS: {passed}/{passed+failed} Tests bestanden")
        print("="*60)

    finally:
        import os
        os.unlink(test_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run_tests()
