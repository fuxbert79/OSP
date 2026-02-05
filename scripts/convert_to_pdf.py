#!/usr/bin/env python3
"""
Konvertiert XLSX/DOCX zu PDF mit LibreOffice Headless

Verwendung:
    python3 convert_to_pdf.py input.xlsx output.pdf
    python3 convert_to_pdf.py input.xlsx  # Output: input.pdf

Autor: Claude Code
Datum: 2026-01-28
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path
from typing import Optional


def convert_to_pdf(input_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """Konvertiert Dokument zu PDF"""

    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {input_path}")

    # Output-Pfad bestimmen
    if output_path:
        output_file = Path(output_path)
        output_dir = output_file.parent
    else:
        output_dir = input_file.parent
        output_file = output_dir / f"{input_file.stem}.pdf"

    # Output-Verzeichnis erstellen falls nicht vorhanden
    output_dir.mkdir(parents=True, exist_ok=True)

    # HOME setzen fuer LibreOffice (vermeidet "no display" Fehler)
    env = os.environ.copy()
    env['HOME'] = '/tmp'

    # LibreOffice Headless ausfuehren
    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(input_file)
    ]

    print(f"[PDF] Konvertiere: {input_file.name} -> PDF")
    print(f"      Befehl: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )

        if result.returncode != 0:
            print(f"[ERR] LibreOffice Fehler: {result.stderr}")
            if result.stdout:
                print(f"      stdout: {result.stdout}")
            return None

        # LibreOffice erstellt PDF im outdir mit gleichem Basename
        generated_pdf = output_dir / f"{input_file.stem}.pdf"

        # Falls anderer Output-Name gewuenscht, umbenennen
        if output_path and generated_pdf != output_file:
            shutil.move(str(generated_pdf), str(output_file))

        if output_file.exists():
            size_kb = output_file.stat().st_size / 1024
            print(f"[OK] PDF erstellt: {output_file}")
            print(f"     Groesse: {size_kb:.1f} KB")
            return str(output_file)
        else:
            print(f"[ERR] PDF nicht erstellt")
            return None

    except subprocess.TimeoutExpired:
        print("[ERR] Timeout bei PDF-Konvertierung (120s)")
        return None
    except Exception as e:
        print(f"[ERR] Fehler: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Verwendung: python3 convert_to_pdf.py input.xlsx [output.pdf]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    result = convert_to_pdf(input_path, output_path)

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
