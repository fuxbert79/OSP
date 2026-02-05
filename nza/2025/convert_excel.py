#!/usr/bin/env python3
"""
NZA 2025 Excel → JavaScript Converter
Konvertiert NZA_DB_2025.xlsx in einbettbare JavaScript-Daten
"""
import pandas as pd
import json
from datetime import datetime
import os

EXCEL_FILE = 'NZA_DB_2025.xlsx'
MITARBEITER_FILE = '../daten/nza_mitarbeiter.csv'

def load_mitarbeiter_mapping():
    """Lädt Mapping Name/Kürzel → Personalnummer"""
    mapping = {}
    try:
        df = pd.read_csv(MITARBEITER_FILE, sep=';', encoding='utf-8-sig')
        for _, row in df.iterrows():
            pers_nr = str(row['Pers.-Nr.']).strip()
            kuerzel_val = row['Kürzel']
            name_val = row['Name']
            kuerzel = str(kuerzel_val).strip() if bool(pd.notna(kuerzel_val)) else None
            name = str(name_val).strip() if bool(pd.notna(name_val)) else None

            if kuerzel and pers_nr and pers_nr != '--':
                mapping[kuerzel.lower()] = pers_nr
            if name and pers_nr and pers_nr != '--':
                mapping[name.lower()] = pers_nr
    except Exception as e:
        print(f"// Warnung: Mitarbeiter-Mapping konnte nicht geladen werden: {e}")
    return mapping

def get_pers_nr(name, mapping):
    """Gibt Personalnummer für einen Namen/Kürzel zurück"""
    if not name:
        return None
    name_lower = str(name).lower().strip()
    return mapping.get(name_lower, name)  # Falls nicht gefunden, Original zurückgeben

def clean_value(val):
    """Bereinigt NaN/None Werte"""
    if pd.isna(val):
        return None
    if isinstance(val, float) and val == int(val):
        return int(val)
    return val

def format_date(val):
    """Formatiert Datum als ISO-String"""
    if pd.isna(val):
        return None
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d')
    return str(val)

def format_nza_id(nza_id):
    """Formatiert NZA-ID: NZA_25_017 → NZA_25017"""
    if not nza_id:
        return None
    s = str(nza_id)
    # Entferne den mittleren Unterstrich: NZA_25_017 → NZA_25017
    parts = s.split('_')
    if len(parts) == 3:
        return f"{parts[0]}_{parts[1]}{parts[2]}"
    return s

def main():
    # Mitarbeiter-Mapping laden
    ma_mapping = load_mitarbeiter_mapping()

    xlsx = pd.ExcelFile(EXCEL_FILE)

    # 1. NZA Hauptdaten
    df_nza = pd.read_excel(xlsx, sheet_name='NZA DB')
    nza_data = []

    # Alle Fehlerkategorien sammeln
    alle_kategorien = set()

    for _, row in df_nza.iterrows():
        verursacher_name = clean_value(row['verursacher'])
        verursacher_pers_nr = get_pers_nr(verursacher_name, ma_mapping)

        kategorie = clean_value(row['Fehlerkategorie'])
        if kategorie is not None:
            alle_kategorien.add(kategorie)

        nza_data.append({
            'nzaId': format_nza_id(row['NZA-ID']),
            'reklamationstyp': clean_value(row['reklamationstyp']),
            'datum': format_date(row['datum']),
            'artikelNr': str(clean_value(row['artikel_nr'])) if clean_value(row['artikel_nr']) is not None else None,
            'betriebsauftrag': str(clean_value(row['betriebsauftrag'])) if clean_value(row['betriebsauftrag']) is not None else None,
            'pruefmenge': clean_value(row['pruefmenge']),
            'davonNio': clean_value(row['davon_nio']),
            'verursacher': verursacher_pers_nr,
            'verursacherPersNr': clean_value(row['verursacher_persnr.']),
            'kostenstelle': str(clean_value(row['kostenstelle'])) if clean_value(row['kostenstelle']) is not None else None,
            'fehlerbeschreibung': clean_value(row['fehlerbeschreibung']),
            'fehlerkategorie': kategorie,
            'qaNummerRms': clean_value(row['QA-Nummer']),
            'qNummerKunde': clean_value(row['Q-Nummer Kunde']),
            'bemerkungen': clean_value(row['bemerkungen']),
            'kostenProzesse': round(float(clean_value(row['kosten_prozesse']) or 0), 2),
            'kostenMaterial': round(float(clean_value(row['kosten_material']) or 0), 2),
            'kostenGesamt': round(float(clean_value(row['kosten_sonstige']) or 0), 2)
        })

    # 2. Prozess-Daten
    df_proc = pd.read_excel(xlsx, sheet_name='Prozess DB')
    prozess_data = {}

    for _, row in df_proc.iterrows():
        nza_id = format_nza_id(row['NZA-ID'])
        prozesse = []

        for i in range(1, 6):
            prozess_name = clean_value(row.get(f'prozess_{i}'))
            if prozess_name:
                werker_name = clean_value(row.get(f'werker_{i}'))
                werker_pers_nr = get_pers_nr(werker_name, ma_mapping)

                prozesse.append({
                    'prozess': prozess_name,
                    'werker': werker_pers_nr,
                    'kostenstelle': str(clean_value(row.get(f'kostenstelle_{i}'))) if clean_value(row.get(f'kostenstelle_{i}')) is not None else None,
                    'zeitMin': clean_value(row.get(f'zeit_min_{i}')),
                    'kosten': round(float(clean_value(row.get(f'kosten_{i}')) or 0), 2)
                })

        if prozesse:
            prozess_data[nza_id] = {
                'prozesse': prozesse,
                'kostenKpl': round(float(clean_value(row.get('kosten_kpl')) or 0), 2)
            }

    # 3. Material-Daten
    df_mat = pd.read_excel(xlsx, sheet_name='Material DB')
    material_data = {}

    for _, row in df_mat.iterrows():
        nza_id = format_nza_id(row['NZA-ID'])
        materialien = []

        for i in range(1, 6):
            artikel_nr = clean_value(row.get(f'artikelnummer_{i}'))
            if artikel_nr:
                materialien.append({
                    'artikelNr': str(artikel_nr),
                    'bezeichnung': clean_value(row.get(f'artikelbezeichnung_{i}')),
                    'menge': clean_value(row.get(f'menge_{i}')),
                    'einheit': clean_value(row.get(f'einheit_{i}'))
                })

        if materialien:
            material_data[nza_id] = {
                'materialien': materialien,
                'materialkosten': round(float(clean_value(row.get('Materialkosten')) or 0), 2)
            }

    # 4. Statistiken berechnen
    total_kosten = sum(n['kostenGesamt'] for n in nza_data)
    total_nio = sum(n['davonNio'] or 0 for n in nza_data)
    total_pruef = sum(n['pruefmenge'] or 0 for n in nza_data)

    # Umsatzerlös 2025 (fester Wert)
    umsatz_2025 = 6253386.26

    # Typ-Verteilung
    typ_counts = {}
    for n in nza_data:
        typ = n['reklamationstyp'] or 'Unbekannt'
        typ_counts[typ] = typ_counts.get(typ, 0) + 1

    # KST-Verteilung
    kst_counts = {}
    for n in nza_data:
        kst = n['kostenstelle'] or 'Unbekannt'
        kst_counts[kst] = kst_counts.get(kst, 0) + 1

    # Fehlerursachen
    fehler_counts = {}
    for n in nza_data:
        fehler = n['fehlerkategorie'] or 'Unbekannt'
        fehler_counts[fehler] = fehler_counts.get(fehler, 0) + 1

    # Monats-Trend
    monats_trend = {}
    for n in nza_data:
        if n['datum']:
            monat = n['datum'][:7]  # YYYY-MM
            if monat not in monats_trend:
                monats_trend[monat] = {'anzahl': 0, 'kosten': 0}
            monats_trend[monat]['anzahl'] += 1
            monats_trend[monat]['kosten'] += n['kostenGesamt']

    # NZA-Kennzahl berechnen: (Gesamtkosten * 100 / Umsatzerlös) * 100
    nza_kennzahl = round((total_kosten * 100 / umsatz_2025) * 100, 2) if umsatz_2025 > 0 else 0

    # Top Fehlerursache
    top_fehler = max(fehler_counts.items(), key=lambda x: x[1])[0] if fehler_counts else '-'

    stats = {
        'anzahl': len(nza_data),
        'kostenGesamt': round(total_kosten, 2),
        'umsatz2025': umsatz_2025,
        'nzaKennzahl': nza_kennzahl,
        'totalNio': total_nio,
        'totalPruef': total_pruef,
        'topFehlerursache': top_fehler,
        'typVerteilung': typ_counts,
        'kstVerteilung': kst_counts,
        'fehlerVerteilung': dict(sorted(fehler_counts.items(), key=lambda x: -x[1])[:10]),
        'alleKategorien': sorted(list(alle_kategorien)),
        'monatsTrend': dict(sorted(monats_trend.items()))
    }

    # JavaScript ausgeben
    print("// NZA 2025 Daten - Generiert am", datetime.now().strftime('%Y-%m-%d %H:%M'))
    print()
    print("const nzaData =", json.dumps(nza_data, ensure_ascii=False, indent=2), ";")
    print()
    print("const prozessData =", json.dumps(prozess_data, ensure_ascii=False, indent=2), ";")
    print()
    print("const materialData =", json.dumps(material_data, ensure_ascii=False, indent=2), ";")
    print()
    print("const statsData =", json.dumps(stats, ensure_ascii=False, indent=2), ";")

if __name__ == '__main__':
    main()
