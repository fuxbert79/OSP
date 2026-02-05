#!/usr/bin/env python3
"""Test-Skript für OSP RAG Filter im Container - v2 mit E5-large"""

import sys
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

print("=== Test: Embedding Model (E5-large) ===")
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("intfloat/multilingual-e5-large")
    print(f"OK: E5-large geladen, Dimension: {model.get_sentence_embedding_dimension()}")
except Exception as e:
    print(f"FAIL: Embedding Model: {e}")
    sys.exit(1)

print("\n=== Test: ChromaDB Verbindung ===")
try:
    import chromadb
    from chromadb.config import Settings
    client = chromadb.HttpClient(
        host="chromadb",
        port=8000,
        settings=Settings(anonymized_telemetry=False)
    )
    print("OK: ChromaDB verbunden")

    # Collections laden
    collections = {}
    for name in ["osp_kern", "osp_kpl", "osp_erweitert"]:
        try:
            collections[name] = client.get_collection(name)
            count = collections[name].count()
            print(f"  {name}: {count} Dokumente")
        except Exception as e:
            print(f"  WARN {name}: {e}")

except Exception as e:
    print(f"FAIL: ChromaDB: {e}")
    sys.exit(1)

print("\n=== Test: Query 'wer ist AL' mit E5-large Embeddings ===")
try:
    # Query mit E5-large berechnen
    query = "wer ist AL Mitarbeiter Kuerzel Personalstamm HR_CORE"
    query_with_prefix = f"query: {query}"
    query_embedding = model.encode([query_with_prefix], normalize_embeddings=True).tolist()
    print(f"OK: Query-Embedding berechnet ({len(query_embedding[0])} dim)")

    # Query gegen osp_kern
    results = collections["osp_kern"].query(
        query_embeddings=query_embedding,
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    if results and results.get("documents"):
        print(f"OK: {len(results['documents'][0])} Ergebnisse gefunden")
        for i, doc in enumerate(results["documents"][0][:3]):
            meta = results.get("metadatas", [[]])[0]
            filename = meta[i].get("filename", "?") if meta else "?"
            dist = results.get("distances", [[]])[0][i] if results.get("distances") else 0
            preview = doc[:200].replace('\n', ' ') if doc else "LEER"
            print(f"\n  [{i+1}] {filename} (dist: {dist:.4f})")
            print(f"      {preview}...")
    else:
        print("WARN: Keine Ergebnisse")

except Exception as e:
    print(f"FAIL: Query: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n=== ALLE TESTS BESTANDEN ===")
