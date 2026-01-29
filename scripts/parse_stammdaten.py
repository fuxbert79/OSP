#!/usr/bin/env python3
"""
Parst die Stammdaten CSV und gibt JSON aus
"""
import csv
import json
import sys
from pathlib import Path

def parse_stammdaten(csv_path: str) -> list:
    """Parst die CSV-Datei und gibt eine Liste von Dictionaries zurück"""

    stammdaten = []

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        # Semikolon als Delimiter
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            # Mehrzeilige Namen bereinigen (Zeilenumbrüche durch Leerzeichen ersetzen)
            name = row.get('Name', '').replace('\n', ' ').replace('\r', '').strip()

            # Leere Namen überspringen
            if not name:
                continue

            stammdaten.append({
                'Title': name,
                'PLZ': row.get('PLZ', '').strip(),
                'Ort': row.get('Ort', '').strip(),
                'Adresse': row.get('Adresse', '').replace('\n', ', ').strip(),
                'DebKredNr': row.get('Deb./Kred.-Nr', '').strip(),
                'StammdatenTyp': row.get('Typ', '').strip(),
                'Land': row.get('Land', '').strip() or 'Deutschland'
            })

    return stammdaten

def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else '/mnt/HC_Volume_104189729/osp/rms/Stammdaten.csv'

    stammdaten = parse_stammdaten(csv_path)

    print(f"Parsed {len(stammdaten)} Einträge", file=sys.stderr)

    # Statistik
    kunden = len([s for s in stammdaten if s['StammdatenTyp'] == 'Kunde'])
    lieferanten = len([s for s in stammdaten if s['StammdatenTyp'] == 'Lieferant'])
    print(f"  - Kunden: {kunden}", file=sys.stderr)
    print(f"  - Lieferanten: {lieferanten}", file=sys.stderr)

    # JSON ausgeben
    print(json.dumps(stammdaten, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
