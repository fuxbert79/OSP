"""
Komax CSV-Generator Tool Pipeline für Open WebUI
================================================
Ermöglicht die Konvertierung von Excel-Schneidlisten zu TCD-kompatiblen CSV-Dateien
und den Upload zu Komax Alpha 355/356 Maschinen.

Version: 1.0
Autor: QM/KI-Manager (AL)
Datum: 2025-12-12
"""

import os
import sys
import logging
from typing import List, Union, Generator, Optional
from pydantic import BaseModel, Field

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pipeline Metadata
class Pipeline:
    """
    Komax CSV-Generator Tool Pipeline
    
    Stellt Funktionen bereit für:
    - Excel-Validierung
    - CSV-Konvertierung (TCD-Format)
    - Maschinen-Status-Prüfung
    - Upload zu Komax Alpha 355/356
    """
    
    class Valves(BaseModel):
        """Konfigurierbare Parameter"""
        KOMAX_BASE_PATH: str = Field(
            default="C:\\Users\\andreas.loehr.SCHNEIDER\\OneDrive - Rainer Schneider Kabelsatzbau und Konfektion\\claude\\komax_csv_generator",
            description="Pfad zum Komax CSV-Generator"
        )
        ALPHA_355_IP: str = Field(
            default="192.168.1.100",
            description="IP-Adresse Komax Alpha 355"
        )
        ALPHA_356_IP: str = Field(
            default="192.168.1.101", 
            description="IP-Adresse Komax Alpha 356"
        )
        DEFAULT_MACHINE: str = Field(
            default="ALPHA_355",
            description="Standard-Maschine für Upload"
        )
        STRICT_MODE: bool = Field(
            default=False,
            description="Strenge Validierung (unbekannte Kontakte = Fehler)"
        )
    
    class Tools:
        """Tool-Funktionen die vom LLM aufgerufen werden können"""
        
        def __init__(self, pipeline):
            self.pipeline = pipeline
            self._modules_loaded = False
            self._excel_parser = None
            self._csv_generator = None
            self._validator = None
            self._network_upload = None
        
        def _load_modules(self):
            """Lazy-Load der Komax-Module"""
            if self._modules_loaded:
                return True
            
            try:
                base_path = self.pipeline.valves.KOMAX_BASE_PATH
                if base_path not in sys.path:
                    sys.path.insert(0, base_path)
                
                from modules import excel_parser, csv_generator, validator, network_upload  # type: ignore[import-not-found]
                
                self._excel_parser = excel_parser
                self._csv_generator = csv_generator
                self._validator = validator
                self._network_upload = network_upload
                self._modules_loaded = True
                
                logger.info("✅ Komax-Module geladen")
                return True
                
            except ImportError as e:
                logger.error(f"❌ Fehler beim Laden der Module: {e}")
                return False
        
        def check_machine_status(self) -> str:
            """
            Prüft den Verbindungsstatus der Komax-Maschinen.
            
            Returns:
                str: Status-Bericht für alle konfigurierten Maschinen
            """
            if not self._load_modules():
                return "❌ Komax-Module nicht verfügbar"
            
            machines = {
                "ALPHA_355": self.pipeline.valves.ALPHA_355_IP,
                "ALPHA_356": self.pipeline.valves.ALPHA_356_IP
            }

            results = []
            for name, ip in machines.items():
                try:
                    if self._network_upload is None:
                        results.append(f"{name} ({ip}): ❌ Modul nicht geladen")
                        continue
                    is_online = self._network_upload.check_machine_connection(ip)
                    status = "🟢 ONLINE" if is_online else "🔴 OFFLINE"
                    results.append(f"{name} ({ip}): {status}")
                except Exception as e:
                    results.append(f"{name} ({ip}): ❌ Fehler - {str(e)}")
            
            return "**Komax Maschinen-Status:**\n" + "\n".join(results)
        
        def validate_excel(
            self,
            file_path: str,
            sheet_name: Optional[str] = None
        ) -> str:
            """
            Validiert eine Excel-Schneidliste gemäß NULL-FEHLER-POLITIK.
            
            Args:
                file_path: Pfad zur Excel-Datei
                sheet_name: Optional: Name des Tabellenblatts
            
            Returns:
                str: Validierungsergebnis mit Fehlern/Warnungen
            """
            if not self._load_modules():
                return "❌ Komax-Module nicht verfügbar"
            
            try:
                if self._excel_parser is None or self._validator is None:
                    return "❌ Komax-Module nicht vollständig geladen"

                # Excel parsen
                df = self._excel_parser.parse_excel_file(file_path, sheet_name)

                # Validieren
                result = self._validator.validate_data(
                    df,
                    strict_mode=self.pipeline.valves.STRICT_MODE
                )
                
                # Ergebnis formatieren
                output = []
                output.append(f"**Validierung: {file_path}**\n")
                
                if result.is_valid:
                    output.append("✅ **Validierung erfolgreich!**")
                else:
                    output.append("❌ **Validierung fehlgeschlagen!**")
                
                output.append(f"\n📊 **Statistik:**")
                output.append(f"- Zeilen geprüft: {len(df)}")
                output.append(f"- Fehler: {len(result.errors)}")
                output.append(f"- Warnungen: {len(result.warnings)}")
                
                if result.errors:
                    output.append("\n🚫 **Kritische Fehler:**")
                    for err in result.errors[:10]:  # Max 10 Fehler anzeigen
                        output.append(f"- {err}")
                    if len(result.errors) > 10:
                        output.append(f"  ... und {len(result.errors) - 10} weitere")
                
                if result.warnings:
                    output.append("\n⚠️ **Warnungen:**")
                    for warn in result.warnings[:10]:
                        output.append(f"- {warn}")
                    if len(result.warnings) > 10:
                        output.append(f"  ... und {len(result.warnings) - 10} weitere")
                
                return "\n".join(output)
                
            except FileNotFoundError:
                return f"❌ Datei nicht gefunden: {file_path}"
            except Exception as e:
                return f"❌ Fehler bei Validierung: {str(e)}"
        
        def convert_to_csv(
            self,
            file_path: str,
            output_path: Optional[str] = None,
            sheet_name: Optional[str] = None
        ) -> str:
            """
            Konvertiert eine Excel-Schneidliste zu TCD-kompatiblem CSV.
            
            Args:
                file_path: Pfad zur Excel-Datei
                output_path: Optional: Pfad für CSV-Ausgabe
                sheet_name: Optional: Name des Tabellenblatts
            
            Returns:
                str: Pfad zur erstellten CSV-Datei oder Fehlermeldung
            """
            if not self._load_modules():
                return "❌ Komax-Module nicht verfügbar"
            
            try:
                if self._excel_parser is None or self._validator is None or self._csv_generator is None:
                    return "❌ Komax-Module nicht vollständig geladen"

                # Excel parsen
                df = self._excel_parser.parse_excel_file(file_path, sheet_name)

                # Erst validieren
                validation = self._validator.validate_data(df)
                if not validation.is_valid:
                    return f"❌ Konvertierung abgebrochen - Validierungsfehler:\n" + \
                           "\n".join(validation.errors[:5])
                
                # Daten verwenden (ggf. mit Auto-Korrekturen)
                data_to_use = validation.modified_data if validation.modified_data is not None else df
                
                # CSV generieren
                if output_path is None:
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_path = os.path.join(
                        os.path.dirname(file_path),
                        f"{base_name}_TCD.csv"
                    )
                
                self._csv_generator.generate_csv(data_to_use, output_path)
                
                # Verifizieren
                is_valid = self._csv_generator.verify_csv_format(output_path)
                
                if is_valid:
                    return f"✅ **CSV erfolgreich erstellt!**\n\n" \
                           f"📄 Datei: `{output_path}`\n" \
                           f"📊 Zeilen: {len(data_to_use)}\n" \
                           f"✓ Format: TCD-kompatibel (79 Spalten, cp850)"
                else:
                    return f"⚠️ CSV erstellt, aber Format-Verifizierung fehlgeschlagen:\n{output_path}"
                    
            except Exception as e:
                return f"❌ Fehler bei Konvertierung: {str(e)}"
        
        def upload_to_machine(
            self,
            csv_path: str,
            machine: str = "ALPHA_355",
            mode: str = "OVERWRITE"
        ) -> str:
            """
            Lädt eine CSV-Datei auf eine Komax-Maschine hoch.
            
            Args:
                csv_path: Pfad zur CSV-Datei
                machine: Zielmaschine (ALPHA_355 oder ALPHA_356)
                mode: OVERWRITE oder APPEND
            
            Returns:
                str: Upload-Ergebnis
            """
            if not self._load_modules():
                return "❌ Komax-Module nicht verfügbar"
            
            # IP ermitteln
            if machine == "ALPHA_355":
                ip = self.pipeline.valves.ALPHA_355_IP
            elif machine == "ALPHA_356":
                ip = self.pipeline.valves.ALPHA_356_IP
            else:
                return f"❌ Unbekannte Maschine: {machine}"
            
            try:
                if self._network_upload is None:
                    return "❌ Network-Upload Modul nicht geladen"

                # Verbindung prüfen
                if not self._network_upload.check_machine_connection(ip):
                    return f"❌ Maschine {machine} ({ip}) nicht erreichbar"

                # Upload durchführen
                success = self._network_upload.upload_to_komax(
                    csv_path,
                    ip,
                    mode=mode
                )
                
                if success:
                    return f"✅ **Upload erfolgreich!**\n\n" \
                           f"📄 Datei: `{os.path.basename(csv_path)}`\n" \
                           f"🎯 Maschine: {machine} ({ip})\n" \
                           f"📥 Modus: {mode}"
                else:
                    return f"❌ Upload fehlgeschlagen"
                    
            except Exception as e:
                return f"❌ Fehler beim Upload: {str(e)}"
        
        def process_complete(
            self,
            file_path: str,
            machine: str = "ALPHA_355",
            sheet_name: Optional[str] = None
        ) -> str:
            """
            Führt den kompletten Workflow aus: Validieren → Konvertieren → Hochladen.
            
            Args:
                file_path: Pfad zur Excel-Datei
                machine: Zielmaschine für Upload
                sheet_name: Optional: Name des Tabellenblatts
            
            Returns:
                str: Zusammenfassung des gesamten Workflows
            """
            results = []
            results.append("# 🔄 Komax Komplett-Workflow\n")
            
            # Schritt 1: Validierung
            results.append("## 1️⃣ Validierung")
            validation_result = self.validate_excel(file_path, sheet_name)
            results.append(validation_result)
            
            if "❌" in validation_result and "fehlgeschlagen" in validation_result:
                results.append("\n⛔ **Workflow abgebrochen** - Validierungsfehler beheben!")
                return "\n\n".join(results)
            
            # Schritt 2: Konvertierung
            results.append("\n## 2️⃣ Konvertierung")
            csv_result = self.convert_to_csv(file_path, sheet_name=sheet_name)
            results.append(csv_result)
            
            if "❌" in csv_result:
                results.append("\n⛔ **Workflow abgebrochen** - Konvertierungsfehler!")
                return "\n\n".join(results)
            
            # CSV-Pfad extrahieren
            csv_path = None
            for line in csv_result.split("\n"):
                if "Datei:" in line:
                    csv_path = line.split("`")[1] if "`" in line else None
                    break
            
            if not csv_path:
                # Fallback: Standard-Pfad konstruieren
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                csv_path = os.path.join(
                    os.path.dirname(file_path),
                    f"{base_name}_TCD.csv"
                )
            
            # Schritt 3: Upload
            results.append("\n## 3️⃣ Upload")
            upload_result = self.upload_to_machine(csv_path, machine)
            results.append(upload_result)
            
            # Zusammenfassung
            if "✅" in upload_result:
                results.append("\n---\n## ✅ Workflow erfolgreich abgeschlossen!")
            else:
                results.append("\n---\n## ⚠️ Workflow mit Problemen beendet")
            
            return "\n\n".join(results)
    
    def __init__(self):
        self.name = "Komax CSV-Generator"
        self.id = "komax_csv_generator"
        self.valves = self.Valves()
        self.tools = self.Tools(self)
    
    async def on_startup(self):
        """Initialisierung beim Start"""
        logger.info("🚀 Komax CSV-Generator Tool Pipeline gestartet")
        
        # Prüfe ob Basis-Pfad existiert
        if not os.path.exists(self.valves.KOMAX_BASE_PATH):
            logger.warning(f"⚠️ Komax-Pfad nicht gefunden: {self.valves.KOMAX_BASE_PATH}")
    
    async def on_shutdown(self):
        """Cleanup beim Beenden"""
        logger.info("🛑 Komax CSV-Generator Tool Pipeline beendet")
    
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict
    ) -> Union[str, Generator]:
        """
        Haupt-Pipeline-Methode.
        
        Diese Pipeline ist primär als Tool-Provider gedacht.
        Direkte Nachrichten werden mit Hilfe-Text beantwortet.
        """
        
        # Hilfe-Text für direkte Anfragen
        help_text = """
# 🔧 Komax CSV-Generator

Dieses Tool konvertiert Excel-Schneidlisten zu TCD-kompatiblem CSV-Format 
und lädt sie auf Komax Alpha 355/356 Maschinen.

## Verfügbare Funktionen:

1. **check_machine_status()** - Prüft Verbindung zu den Maschinen
2. **validate_excel(file_path)** - Validiert eine Excel-Datei
3. **convert_to_csv(file_path)** - Konvertiert zu TCD-CSV
4. **upload_to_machine(csv_path, machine)** - Lädt CSV hoch
5. **process_complete(file_path, machine)** - Kompletter Workflow

## Beispiel-Nutzung:

"Prüfe den Status der Komax-Maschinen"
"Validiere die Schneidliste unter C:\\Daten\\schneidliste.xlsx"
"Konvertiere und sende schneidliste.xlsx an ALPHA_355"
"""
        return help_text


# Pipeline-Instanz für Open WebUI
pipeline = Pipeline()
