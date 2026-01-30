"""
MA-Kürzel Query-Preprocessing Modul für OSP RAG Pipeline.

Erweitert kurze MA-Kürzel-Queries zu kontextreichen Strings für bessere
Embedding-Suche in ChromaDB.

Version: 1.0
Datum: 2025-12-15
"""

import json
import re
import logging
from pathlib import Path
from typing import Optional, Tuple

# Logger konfigurieren
logger = logging.getLogger("ma_preprocessing")


class MAPreprocessor:
    """Präprozessor für MA-Kürzel in Queries."""

    # Keywords die KEINE MA-Expansion auslösen sollen
    NEGATIVE_KEYWORDS = [
        "defekt", "kaputt", "reparatur", "fehler", "problem",
        "maschine", "werkzeug", "anlage", "gerät", "tool",
        "komax", "crimp", "schneid", "ablän"
    ]

    # Artikel die vor Kürzeln stehen können (dann kein MA)
    ARTICLES = ["die", "der", "das", "eine", "ein", "einen"]

    def __init__(self, json_path: str = "/app/backend/data/lookups/ma_kuerzel.json"):
        """
        Initialisiert den Präprozessor.

        Args:
            json_path: Pfad zur JSON-Datei mit Kürzel-Definitionen
        """
        self.json_path = json_path
        self.kuerzel_set: set = set()
        self.patterns: dict = {}
        self.fallback_template: str = ""
        self._loaded = False

    def load(self) -> bool:
        """
        Lädt die Kürzel-Konfiguration aus der JSON-Datei.

        Returns:
            True wenn erfolgreich, False bei Fehler
        """
        try:
            path = Path(self.json_path)
            if not path.exists():
                logger.error(f"❌ MA-Kürzel JSON nicht gefunden: {self.json_path}")
                return False

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Kürzel laden
            self.kuerzel_set = set(data.get("kuerzel", []))

            # Patterns laden und kompilieren
            self.patterns = {}
            for name, pattern_def in data.get("patterns", {}).items():
                try:
                    compiled = re.compile(pattern_def["regex"], re.IGNORECASE)
                    self.patterns[name] = {
                        "regex": compiled,
                        "expansion": pattern_def["expansion"]
                    }
                except re.error as e:
                    logger.warning(f"⚠️ Regex-Fehler in Pattern '{name}': {e}")

            # Fallback laden
            self.fallback_template = data.get(
                "expansion_fallback",
                "Mitarbeiter Personal Kürzel {kuerzel} HR_CORE"
            )

            self._loaded = True
            logger.info(f"✅ MA-Kürzel geladen: {len(self.kuerzel_set)} Einträge, "
                       f"{len(self.patterns)} Patterns")
            return True

        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON Parse-Fehler: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Fehler beim Laden: {e}")
            return False

    def _contains_negative_keyword(self, query: str) -> bool:
        """Prüft ob Query ein Negativ-Keyword enthält."""
        query_lower = query.lower()
        for keyword in self.NEGATIVE_KEYWORDS:
            if keyword in query_lower:
                return True
        return False

    def _has_article_before_kuerzel(self, query: str, kuerzel: str) -> bool:
        """Prüft ob vor dem Kürzel ein Artikel steht (z.B. 'Die AL')."""
        query_lower = query.lower()
        kuerzel_lower = kuerzel.lower()

        for article in self.ARTICLES:
            pattern = f"{article}\\s+{kuerzel_lower}"
            if re.search(pattern, query_lower):
                return True
        return False

    def _extract_kuerzel(self, query: str) -> Optional[str]:
        """
        Extrahiert ein gültiges MA-Kürzel aus der Query.

        Returns:
            Das gefundene Kürzel (uppercase) oder None
        """
        # Suche nach 2-3 Großbuchstaben
        matches = re.findall(r'\b([A-Z]{2,3})\b', query.upper())

        for match in matches:
            if match in self.kuerzel_set:
                return match
        return None

    def _find_matching_pattern(self, query: str, kuerzel: str) -> Optional[str]:
        """
        Findet das passende Pattern und gibt die Expansion zurück.

        Returns:
            Expansion-String oder None
        """
        for name, pattern_data in self.patterns.items():
            if pattern_data["regex"].search(query):
                expansion = pattern_data["expansion"].replace("{kuerzel}", kuerzel)
                logger.debug(f"Pattern '{name}' matched: {expansion}")
                return expansion
        return None

    def expand_query(self, query: str) -> Tuple[str, bool]:
        """
        Erweitert eine Query falls sie ein MA-Kürzel enthält.

        Args:
            query: Die Original-Query

        Returns:
            Tuple (expandierte_query, wurde_expandiert)
        """
        if not self._loaded:
            if not self.load():
                logger.warning("⚠️ MA-Preprocessing nicht verfügbar, verwende Original")
                return query, False

        original = query.strip()

        # Negativ-Keywords prüfen
        if self._contains_negative_keyword(original):
            logger.debug(f"Negativ-Keyword gefunden, keine Expansion: {original}")
            return original, False

        # Kürzel extrahieren
        kuerzel = self._extract_kuerzel(original)
        if not kuerzel:
            return original, False

        # Artikel-Check
        if self._has_article_before_kuerzel(original, kuerzel):
            logger.debug(f"Artikel vor Kürzel gefunden, keine Expansion: {original}")
            return original, False

        # Pattern matching
        expansion = self._find_matching_pattern(original, kuerzel)

        if expansion:
            expanded = f"{original} {expansion}"
        else:
            # Fallback verwenden
            fallback = self.fallback_template.replace("{kuerzel}", kuerzel)
            expanded = f"{original} {fallback}"

        logger.info(f"🔄 MA-Query expandiert: '{original}' → '{expanded}'")
        return expanded, True


# Singleton-Instanz für einfache Verwendung
_preprocessor: Optional[MAPreprocessor] = None


def get_preprocessor(json_path: str = "/app/backend/data/lookups/ma_kuerzel.json") -> MAPreprocessor:
    """
    Gibt die Singleton-Instanz des Präprozessors zurück.

    Args:
        json_path: Pfad zur JSON-Datei (nur beim ersten Aufruf relevant)

    Returns:
        MAPreprocessor-Instanz
    """
    global _preprocessor
    if _preprocessor is None:
        _preprocessor = MAPreprocessor(json_path)
        _preprocessor.load()
    return _preprocessor


def expand_ma_query(query: str, json_path: str = "/app/backend/data/lookups/ma_kuerzel.json") -> str:
    """
    Hauptfunktion: Erweitert eine Query falls sie ein MA-Kürzel enthält.

    Diese Funktion ist der Haupteinstiegspunkt für die Pipeline.

    Args:
        query: Die Original-Query
        json_path: Optionaler Pfad zur JSON-Datei

    Returns:
        Expandierte Query oder Original wenn keine Expansion nötig

    Example:
        >>> expand_ma_query("Wer ist AL?")
        "Wer ist AL? Mitarbeiter Kürzel AL Personalstamm HR_CORE Name Funktion Abteilung"

        >>> expand_ma_query("Die AL ist defekt")
        "Die AL ist defekt"  # Keine Expansion wegen "defekt" und Artikel
    """
    preprocessor = get_preprocessor(json_path)
    expanded, _ = preprocessor.expand_query(query)
    return expanded


# Für Tests
if __name__ == "__main__":
    # Test-Logging aktivieren
    logging.basicConfig(level=logging.DEBUG)

    # Test mit lokalen Pfaden
    test_path = "/opt/osp/lookups/ma_kuerzel.json"

    test_queries = [
        "Wer ist AL?",
        "Was macht MD?",
        "CS Kontakt",
        "Telefon SV",
        "Email CA",
        "AL",
        "Die AL ist defekt",
        "Komax AL",
        "Wer ist XY?",  # Ungültiges Kürzel
    ]

    print("\n=== MA-Preprocessing Tests ===\n")

    for q in test_queries:
        result = expand_ma_query(q, test_path)
        changed = "✅" if result != q else "➖"
        print(f"{changed} '{q}' → '{result}'")
