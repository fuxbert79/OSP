#!/usr/bin/env python3
"""
OSP Tag-Routing Validierungsprotokoll
=====================================
Testet das Tag-Routing-System und erstellt einen Report.

Verwendung:
    python3 validate_tag_routing.py
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Module-Pfad hinzufügen
sys.path.insert(0, '/opt/osp/pipelines/modules')

import chromadb
from sentence_transformers import SentenceTransformer
from tag_router import TagRouter, get_where_filter  # type: ignore[import-not-found]

# ═══════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

CHROMADB_HOST = "172.19.0.3"
CHROMADB_PORT = 8000
COLLECTION_NAME = "osp_kern"

# Validierungs-Queries mit erwarteten Ergebnissen
VALIDATION_QUERIES = [
    # (Query, Erwarteter TAG, Erwartetes Dokument-Prefix)
    ("Wer ist AL?", "HR", "HR_"),
    ("Was macht MD?", "HR", "HR_"),
    ("Mitarbeiter Schulungsplan", "HR", "HR_"),
    ("Komax Alpha 530", "TM", "TM_"),
    ("Wartungsplan Maschinen", "TM", "TM_"),
    ("Werkzeug WKZ 602", "TM", "TM_"),
    ("NULL-FEHLER-POLITIK", "QM", "QM_"),
    ("ISO 9001 Audit", "QM", "QM_"),
    ("Reklamation 8D-Report", "QM", "QM_"),
    ("Prüfmittel Kalibrierung", "QM", "QM_"),
    ("Fertigung F2/2000", "KST", "KST_"),
    ("Arbeitsgang AGK", "AV", "AV_"),
    ("Corporate Identity", "KOM", "KOM_"),
    ("Dokumentenstruktur", "DMS", "DMS_"),
    ("OSP Chatbot", "IT", "IT_"),
]


def run_validation():
    """Führt vollständige Validierung durch."""

    print("\n" + "="*80)
    print("OSP TAG-ROUTING VALIDIERUNGSPROTOKOLL")
    print(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    # 1. Komponenten initialisieren
    print("\n[1] INITIALISIERUNG")
    print("-"*40)

    router = TagRouter()
    print(f"Tag-Router: {len(router.compiled_patterns)} TAGs")

    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_collection(COLLECTION_NAME)
    print(f"ChromaDB: {collection.count()} Dokumente in {COLLECTION_NAME}")

    print("Lade E5-large Embedding-Modell...")
    model = SentenceTransformer("intfloat/multilingual-e5-large")
    print(f"Embedding-Modell geladen (Dim: {model.get_sentence_embedding_dimension()})")

    # 2. Metadaten prüfen
    print("\n[2] METADATEN-PRÜFUNG")
    print("-"*40)

    sample = collection.get(limit=5, include=["metadatas"])
    has_tags = all("tag" in m for m in sample["metadatas"])  # type: ignore[union-attr]

    if has_tags:
        print("TAG-Feld in Metadaten vorhanden")
        tags_found = set(m["tag"] for m in sample["metadatas"])  # type: ignore[union-attr]
        print(f"   Gefundene TAGs: {tags_found}")
    else:
        print("TAG-Feld FEHLT in Metadaten!")
        print("   -> Führe reindex_with_tags.py aus!")
        return False

    # 3. Query-Validierung
    print("\n[3] QUERY-VALIDIERUNG")
    print("-"*40)

    results = []
    passed = 0
    failed = 0

    for query, expected_tag, expected_prefix in VALIDATION_QUERIES:
        # Tag extrahieren
        detected_tags = router.extract_tags(query)
        primary_tag = detected_tags[0] if detected_tags else None

        # WHERE-Filter erstellen
        where_filter = get_where_filter(query)

        # ChromaDB Query MIT Filter
        query_embedding = model.encode(f"query: {query}", normalize_embeddings=True)

        search_results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=3,
            where=where_filter,
            include=["metadatas", "distances"]
        )

        # Ergebnis prüfen
        if search_results["metadatas"] and search_results["metadatas"][0]:
            top_result = search_results["metadatas"][0][0]
            top_file = top_result.get("filename", "")
            top_tag = top_result.get("tag", "")
            distance = search_results["distances"][0][0] if search_results["distances"] else 0
            score = 1 - distance

            tag_correct = (primary_tag == expected_tag)
            doc_correct = str(top_file).startswith(expected_prefix)

            if tag_correct and doc_correct:
                status = "PASS"
                passed += 1
            else:
                status = "FAIL"
                failed += 1

            result = {
                "query": query,
                "expected_tag": expected_tag,
                "detected_tag": primary_tag,
                "expected_prefix": expected_prefix,
                "top_result": top_file,
                "score": round(score, 4),
                "success": tag_correct and doc_correct
            }
        else:
            status = "FAIL (keine Ergebnisse)"
            failed += 1
            result = {
                "query": query,
                "expected_tag": expected_tag,
                "detected_tag": primary_tag,
                "top_result": None,
                "success": False
            }

        results.append(result)

        print(f"\n[{status}]")
        print(f"   Query: '{query}'")
        print(f"   Tag:   {primary_tag} (erwartet: {expected_tag})")
        if result.get("top_result"):
            print(f"   Top-1: {result['top_result']} (Score: {result.get('score', 'N/A')})")

    # 4. Zusammenfassung
    print("\n" + "="*80)
    print("ZUSAMMENFASSUNG")
    print("="*80)

    success_rate = (passed / len(VALIDATION_QUERIES)) * 100

    print(f"\nBestanden: {passed}/{len(VALIDATION_QUERIES)}")
    print(f"Fehlgeschlagen: {failed}/{len(VALIDATION_QUERIES)}")
    print(f"Erfolgsrate: {success_rate:.1f}%")

    if success_rate >= 90:
        print("\nTAG-ROUTING FUNKTIONIERT KORREKT!")
        status_text = "BESTANDEN"
    elif success_rate >= 70:
        print("\nTAG-ROUTING TEILWEISE FUNKTIONAL")
        status_text = "TEILWEISE"
    else:
        print("\nTAG-ROUTING HAT PROBLEME")
        status_text = "FEHLGESCHLAGEN"

    # 5. Report speichern
    report = {
        "timestamp": datetime.now().isoformat(),
        "collection": COLLECTION_NAME,
        "document_count": collection.count(),
        "tests_total": len(VALIDATION_QUERIES),
        "tests_passed": passed,
        "tests_failed": failed,
        "success_rate": success_rate,
        "status": status_text,
        "results": results
    }

    report_path = Path("/opt/osp/logs/tag_routing_validation.json")
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nJSON-Report: {report_path}")

    # Markdown-Report
    md_report = f"""# OSP Tag-Routing Validierungsprotokoll

**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status:** {status_text}
**Erfolgsrate:** {success_rate:.1f}%

## Ergebnisse

| Query | Erw. TAG | Erk. TAG | Top-1 Dokument | Score | Status |
|-------|----------|----------|----------------|-------|--------|
"""

    for r in results:
        status_icon = "PASS" if r["success"] else "FAIL"
        query_short = r['query'][:30] + "..." if len(r['query']) > 30 else r['query']
        top_result = r.get('top_result', '-')
        top_result_short = top_result[:25] if top_result else "-"
        md_report += f"| {query_short} | {r['expected_tag']} | {r.get('detected_tag', '-')} | {top_result_short} | {r.get('score', '-')} | {status_icon} |\n"

    md_report += f"""
## Zusammenfassung

- **Bestanden:** {passed}/{len(VALIDATION_QUERIES)}
- **Fehlgeschlagen:** {failed}/{len(VALIDATION_QUERIES)}
- **Dokumente in Collection:** {collection.count()}

## Empfehlung

"""

    if success_rate >= 90:
        md_report += "Das Tag-Routing-System funktioniert wie erwartet. Keine weiteren Massnahmen erforderlich."
    elif success_rate >= 70:
        md_report += "Das Tag-Routing funktioniert groesstenteils. Einzelne TAGs oder Patterns sollten ueberprueft werden."
    else:
        md_report += "Das Tag-Routing hat signifikante Probleme. Bitte TAG_PATTERNS ueberpruefen und ggf. Re-Index durchfuehren."

    md_path = Path("/opt/osp/logs/tag_routing_validation.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_report)

    print(f"Markdown-Report: {md_path}")

    return success_rate >= 70


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
