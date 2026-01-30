#!/usr/bin/env python3
"""
RMS Funktionstest
=================
Automatisierter Test aller RMS-API-Endpunkte.

Verwendung:
    python3 rms_funktionstest.py              # Alle Tests
    python3 rms_funktionstest.py --test TC-03 # Einzelner Test
    python3 rms_funktionstest.py --verbose    # Mit Details

Autor: AL (via Claude)
Erstellt: 2026-01-30
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime

# =============================================================================
# KONFIGURATION
# =============================================================================

BASE_URL = "http://localhost:5678/webhook"

# Gespeicherte IDs aus vorherigen Tests
TEST_STATE = {
    "rekla_kunde_id": None,
    "rekla_kunde_qa_id": None,
    "rekla_lieferant_id": None,
    "rekla_lieferant_qa_id": None,
    "rekla_intern_id": None,
    "rekla_intern_qa_id": None,
    "massnahme_id": None,
}

# =============================================================================
# HELPER
# =============================================================================

@dataclass
class TestResult:
    """Ergebnis eines Tests"""
    name: str
    passed: bool
    message: str
    data: Any = None
    duration_ms: int = 0

def api_request(method: str, endpoint: str, data: Optional[dict] = None, timeout: int = 30) -> dict:
    """HTTP Request an RMS API"""
    url = f"{BASE_URL}/{endpoint}"

    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")

    if data:
        req.data = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            if body:
                return json.loads(body)
            return {"status": "ok", "http_code": response.status}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"error": True, "code": e.code, "message": error_body}
    except urllib.error.URLError as e:
        return {"error": True, "message": str(e.reason)}
    except json.JSONDecodeError:
        return {"error": True, "message": "Invalid JSON response"}

# =============================================================================
# TESTFÄLLE
# =============================================================================

def tc01_reklamationen_abrufen(verbose: bool = False) -> TestResult:
    """TC-01: Reklamationen abrufen"""
    start = time.time()
    result = api_request("GET", "rms-reklamationen?limit=5")
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-01", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    if "value" not in result:
        return TestResult("TC-01", False, "Keine 'value' in Antwort", result, duration)

    count = len(result.get("value", []))
    return TestResult("TC-01", True, f"{count} Reklamationen abgerufen", result if verbose else None, duration)

def tc02_detail_abrufen(verbose: bool = False) -> TestResult:
    """TC-02: Einzelne Reklamation abrufen"""
    start = time.time()
    result = api_request("GET", "rms-detail?id=1")
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-02", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    if "fields" in result or "QA_ID" in str(result):
        return TestResult("TC-02", True, "Detail abgerufen", result if verbose else None, duration)

    return TestResult("TC-02", False, "Unerwartete Antwort", result, duration)

def tc03_kunde_erstellen(verbose: bool = False) -> TestResult:
    """TC-03: Kundenreklamation erstellen"""
    start = time.time()
    data = {
        "Title": f"Test Kundenreklamation {datetime.now().strftime('%H%M%S')}",
        "Rekla_Typ": "Kunde",
        "Prioritaet": "hoch",
        "Beschreibung": "Testfall TC-03: Kabelsatz defekt geliefert. Crimpverbindungen fehlerhaft."
    }

    result = api_request("POST", "rms-create", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-03", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    # Extrahiere ID und QA_ID (API gibt qaId und sharePointId zurück)
    qa_id = result.get("qaId") or result.get("QA_ID") or result.get("fields", {}).get("QA_ID")
    item_id = result.get("sharePointId") or result.get("id") or result.get("fields", {}).get("id")

    if qa_id:
        TEST_STATE["rekla_kunde_qa_id"] = qa_id
        TEST_STATE["rekla_kunde_id"] = item_id
        return TestResult("TC-03", True, f"Erstellt: {qa_id}", result if verbose else None, duration)

    return TestResult("TC-03", False, "Keine QA_ID erhalten", result, duration)

def tc04_lieferant_erstellen(verbose: bool = False) -> TestResult:
    """TC-04: Lieferantenreklamation erstellen"""
    start = time.time()
    data = {
        "Title": f"Test Lieferantenreklamation {datetime.now().strftime('%H%M%S')}",
        "Rekla_Typ": "Lieferant",
        "Prioritaet": "mittel",
        "Beschreibung": "Testfall TC-04: Material nicht spezifikationskonform"
    }

    result = api_request("POST", "rms-create", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-04", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    qa_id = result.get("qaId") or result.get("QA_ID") or result.get("fields", {}).get("QA_ID")
    item_id = result.get("sharePointId") or result.get("id") or result.get("fields", {}).get("id")

    if qa_id:
        TEST_STATE["rekla_lieferant_qa_id"] = qa_id
        TEST_STATE["rekla_lieferant_id"] = item_id
        return TestResult("TC-04", True, f"Erstellt: {qa_id}", result if verbose else None, duration)

    return TestResult("TC-04", False, "Keine QA_ID erhalten", result, duration)

def tc05_intern_erstellen(verbose: bool = False) -> TestResult:
    """TC-05: Interne Reklamation erstellen"""
    start = time.time()
    data = {
        "Title": f"Test Interne Reklamation {datetime.now().strftime('%H%M%S')}",
        "Rekla_Typ": "Intern",
        "Prioritaet": "niedrig",
        "Beschreibung": "Testfall TC-05: Prozessabweichung dokumentiert"
    }

    result = api_request("POST", "rms-create", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-05", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    qa_id = result.get("qaId") or result.get("QA_ID") or result.get("fields", {}).get("QA_ID")
    item_id = result.get("sharePointId") or result.get("id") or result.get("fields", {}).get("id")

    if qa_id:
        TEST_STATE["rekla_intern_qa_id"] = qa_id
        TEST_STATE["rekla_intern_id"] = item_id
        return TestResult("TC-05", True, f"Erstellt: {qa_id}", result if verbose else None, duration)

    return TestResult("TC-05", False, "Keine QA_ID erhalten", result, duration)

def tc06_reklamation_aktualisieren(verbose: bool = False) -> TestResult:
    """TC-06: Reklamation aktualisieren"""
    if not TEST_STATE.get("rekla_kunde_id"):
        return TestResult("TC-06", False, "Keine Reklamation aus TC-03 vorhanden", None, 0)

    start = time.time()
    data = {
        "id": TEST_STATE["rekla_kunde_id"],
        "Rekla_Status": "In Bearbeitung",
        "Tracking_Status": "Offen"
    }

    result = api_request("PATCH", "rms-update", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-06", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-06", True, "Reklamation aktualisiert", result if verbose else None, duration)

def tc07_massnahme_hinzufuegen(verbose: bool = False) -> TestResult:
    """TC-07: Maßnahme hinzufügen"""
    if not TEST_STATE.get("rekla_kunde_qa_id"):
        return TestResult("TC-07", False, "Keine Reklamation aus TC-03 vorhanden", None, 0)

    start = time.time()
    data = {
        "qaId": TEST_STATE["rekla_kunde_qa_id"],
        "reklaId": TEST_STATE["rekla_kunde_id"],
        "Massnahme_Typ": "Sofortmassnahme",
        "Beschreibung": "Sperrung der betroffenen Charge",
        "Verantwortlich": "AL",
        "Faellig_Am": "2026-02-05"
    }

    result = api_request("POST", "rms-massnahmen", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-07", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    massnahme_id = result.get("id") or result.get("fields", {}).get("id")
    if massnahme_id:
        TEST_STATE["massnahme_id"] = massnahme_id
        return TestResult("TC-07", True, f"Maßnahme erstellt (ID: {massnahme_id})", result if verbose else None, duration)

    return TestResult("TC-07", True, "Maßnahme erstellt", result if verbose else None, duration)

def tc08_massnahme_aktualisieren(verbose: bool = False) -> TestResult:
    """TC-08: Maßnahme aktualisieren"""
    if not TEST_STATE.get("massnahme_id"):
        return TestResult("TC-08", False, "Keine Maßnahme aus TC-07 vorhanden", None, 0)

    start = time.time()
    data = {
        "id": TEST_STATE["massnahme_id"],
        "Status": "Erledigt",
        "Erledigt_Am": "2026-01-30",
        "Bemerkung": "Charge gesperrt und gekennzeichnet"
    }

    result = api_request("PATCH", "rms-update-massnahme", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-08", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-08", True, "Maßnahme aktualisiert", result if verbose else None, duration)

def tc09_tracking_setzen(verbose: bool = False) -> TestResult:
    """TC-09: Tracking-Felder setzen"""
    if not TEST_STATE.get("rekla_lieferant_id"):
        return TestResult("TC-09", False, "Keine Reklamation aus TC-04 vorhanden", None, 0)

    start = time.time()
    data = {
        "id": TEST_STATE["rekla_lieferant_id"],
        "Tracking_Status": "Ersatzlieferung angefordert",
        "Tracking_Ersatzlieferung": True,
        "Tracking_Bemerkung": "Ersatzlieferung bei Lieferant angefordert"
    }

    result = api_request("PATCH", "rms-update", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-09", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-09", True, "Tracking-Felder gesetzt", result if verbose else None, duration)

def tc10_kpis_abrufen(verbose: bool = False) -> TestResult:
    """TC-10: KPIs abrufen"""
    start = time.time()
    result = api_request("GET", "rms-kpis")
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-10", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-10", True, "KPIs abgerufen", result if verbose else None, duration)

def tc11_charts_abrufen(verbose: bool = False) -> TestResult:
    """TC-11: Charts abrufen"""
    start = time.time()
    result = api_request("GET", "rms-charts")
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-11", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-11", True, "Chart-Daten abgerufen", result if verbose else None, duration)

def tc12_dateien_abrufen(verbose: bool = False) -> TestResult:
    """TC-12: Dateien einer Reklamation abrufen"""
    qa_id = TEST_STATE.get("rekla_kunde_qa_id") or "QA-26001"

    start = time.time()
    result = api_request("GET", f"rms-files?qaId={qa_id}")
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-12", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-12", True, "Dateien abgerufen", result if verbose else None, duration)

def tc13_formblatt_generieren(verbose: bool = False) -> TestResult:
    """TC-13: Formblatt generieren"""
    qa_id = TEST_STATE.get("rekla_kunde_qa_id") or "QA-26001"

    start = time.time()
    data = {
        "qaId": qa_id,
        "formblatt": "F-QM-14"
    }

    result = api_request("POST", "rms-generate-formblatt", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-13", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-13", True, "Formblatt-Anfrage gesendet", result if verbose else None, duration)

def tc14_benutzer_abrufen(verbose: bool = False) -> TestResult:
    """TC-14: Benutzer abrufen"""
    start = time.time()
    result = api_request("GET", "e8f9a1b2-rms-users")
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-14", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    count = len(result) if isinstance(result, list) else len(result.get("value", []))
    return TestResult("TC-14", True, f"{count} Benutzer abgerufen", result if verbose else None, duration)

def tc15_stammdaten_abrufen(verbose: bool = False) -> TestResult:
    """TC-15: Stammdaten abrufen"""
    start = time.time()
    result = api_request("GET", "rms-stammdaten")
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-15", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-15", True, "Stammdaten abgerufen", result if verbose else None, duration)

def tc16_reklamation_abschliessen(verbose: bool = False) -> TestResult:
    """TC-16: Reklamation abschließen"""
    if not TEST_STATE.get("rekla_intern_id"):
        return TestResult("TC-16", False, "Keine Reklamation aus TC-05 vorhanden", None, 0)

    start = time.time()
    data = {
        "id": TEST_STATE["rekla_intern_id"],
        "Rekla_Status": "Abgeschlossen",
        "Tracking_Status": "Abgeschlossen",
        "Abschlussdatum": "2026-01-30"
    }

    result = api_request("PATCH", "rms-update", data)
    duration = int((time.time() - start) * 1000)

    if "error" in result:
        return TestResult("TC-16", False, f"API-Fehler: {result.get('message')}", duration_ms=duration)

    return TestResult("TC-16", True, "Reklamation abgeschlossen", result if verbose else None, duration)

# =============================================================================
# MAIN
# =============================================================================

TESTS = {
    "TC-01": tc01_reklamationen_abrufen,
    "TC-02": tc02_detail_abrufen,
    "TC-03": tc03_kunde_erstellen,
    "TC-04": tc04_lieferant_erstellen,
    "TC-05": tc05_intern_erstellen,
    "TC-06": tc06_reklamation_aktualisieren,
    "TC-07": tc07_massnahme_hinzufuegen,
    "TC-08": tc08_massnahme_aktualisieren,
    "TC-09": tc09_tracking_setzen,
    "TC-10": tc10_kpis_abrufen,
    "TC-11": tc11_charts_abrufen,
    "TC-12": tc12_dateien_abrufen,
    "TC-13": tc13_formblatt_generieren,
    "TC-14": tc14_benutzer_abrufen,
    "TC-15": tc15_stammdaten_abrufen,
    "TC-16": tc16_reklamation_abschliessen,
}

def main():
    parser = argparse.ArgumentParser(description="RMS Funktionstest")
    parser.add_argument("--test", help="Einzelnen Test ausführen (z.B. TC-03)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Detaillierte Ausgabe")
    parser.add_argument("--json", action="store_true", help="JSON-Ausgabe")
    args = parser.parse_args()

    results = []

    if args.test:
        # Einzelner Test
        if args.test not in TESTS:
            print(f"Unbekannter Test: {args.test}")
            print(f"Verfügbar: {', '.join(TESTS.keys())}")
            sys.exit(1)

        result = TESTS[args.test](args.verbose)
        results.append(result)
    else:
        # Alle Tests
        print("=" * 60)
        print("RMS FUNKTIONSTEST")
        print("=" * 60)
        print()

        for test_id, test_func in TESTS.items():
            result = test_func(args.verbose)
            results.append(result)

            status = "PASS" if result.passed else "FAIL"
            icon = "+" if result.passed else "x"
            print(f"[{icon}] {test_id}: {result.message} ({result.duration_ms}ms)")

            if args.verbose and result.data:
                print(f"    Data: {json.dumps(result.data, indent=2)[:200]}...")

            # Kurze Pause zwischen Tests
            time.sleep(0.2)

    # Zusammenfassung
    print()
    print("=" * 60)
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    print(f"ERGEBNIS: {passed} bestanden, {failed} fehlgeschlagen")
    print("=" * 60)

    if args.json:
        output = {
            "results": [
                {"test": r.name, "passed": r.passed, "message": r.message, "duration_ms": r.duration_ms}
                for r in results
            ],
            "summary": {"passed": passed, "failed": failed}
        }
        print(json.dumps(output, indent=2))

    # Exit code
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
