#!/usr/bin/env python3
"""Test OSP RAG Filter"""
import asyncio
import sqlite3
import sys

def main():
    # Lade den Filter-Code aus der DB
    conn = sqlite3.connect('/app/backend/data/webui.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM function WHERE id = 'osp_rag_filter'")
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("Filter nicht gefunden")
        return

    code = row[0]
    print(f"Filter-Code geladen: {len(code)} chars")
    print(f"Enthält 'class Filter': {'class Filter' in code}")

    # Führe den Code aus
    local_ns = {}
    exec(code, local_ns)

    # Prüfe ob Filter-Klasse existiert
    if 'Filter' not in local_ns:
        print("ERROR: Filter-Klasse nicht gefunden in ausgeführtem Code")
        print(f"Verfügbare Klassen: {[k for k in local_ns.keys() if not k.startswith('_')]}")
        return

    # Instanziiere den Filter
    FilterClass = local_ns['Filter']
    filter_instance = FilterClass()
    print(f"Filter instanziiert: {filter_instance.name}")

    async def test_filter():
        # Starte den Filter
        print("\nStarte Filter (lädt E5-Modell und verbindet ChromaDB)...")
        await filter_instance.on_startup()

        # Prüfe ob ChromaDB und Embedding verfügbar
        if not filter_instance.chroma_client:
            print("ERROR: ChromaDB nicht verbunden")
            return
        if not filter_instance.embedding_model:
            print("ERROR: Embedding-Modell nicht geladen")
            return

        print("✅ ChromaDB verbunden")
        print("✅ Embedding-Modell geladen")

        # Test-Request
        test_body = {
            "messages": [
                {"role": "user", "content": "Wer ist AL?"}
            ]
        }

        print("\n=== TEST: Wer ist AL? ===")
        result = await filter_instance.inlet(test_body)

        messages = result.get("messages", [])
        if messages and messages[0].get("role") == "system":
            system_content = messages[0].get("content", "")
            print(f"✅ System-Prompt hinzugefügt ({len(system_content)} chars)")
            # Zeige einen Ausschnitt
            if "KONTEXT AUS DER WISSENSDATENBANK" in system_content:
                print("✅ RAG-Kontext enthalten")
                # Zeige die ersten 500 chars des Kontexts
                start = system_content.find("KONTEXT AUS DER WISSENSDATENBANK")
                print(f"\n--- Kontext-Ausschnitt ---")
                print(system_content[start:start+1000])
            else:
                print("❌ Kein RAG-Kontext gefunden")
        else:
            print("❌ Kein System-Prompt hinzugefügt")

    asyncio.run(test_filter())

if __name__ == "__main__":
    main()
