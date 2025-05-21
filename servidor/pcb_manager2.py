from rich.live import Live
from rich.table import Table
from rich.json import JSON
from rich.panel import Panel
import json
import os
import time
from typing import List, Dict


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ruta hacia la carpeta general/datos
DATOS_PATH = os.path.join(BASE_DIR, 'general', 'datos')

PCB_PATH = os.path.join(DATOS_PATH, 'pcb.json')

class mostrar_pcb:
    def __init__(self, archivo_json: str):
        self.archivo_json = archivo_json
        self.pcbs = self.cargar_pcbs()
    
    def cargar_pcbs(self) -> List[Dict]:
        """Carga los PCBs desde el archivo JSON"""
        try:
            with open(self.archivo_json, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.archivo_json}")
            return []
        except json.JSONDecodeError:
            print(f"Error: El archivo {self.archivo_json} no tiene formato JSON válido")
            return []
    
    def generar_tabla(self) -> Table:
        """Genera una tabla Rich con la información de los PCBs"""
        table = Table(title="📋 Tabla de Bloques de Control de Procesos (PCBs)", border_style="blue")
        
        # Añadir columnas
        table.add_column("PID", style="cyan", justify="center")
        table.add_column("PPID", style="magenta", justify="center")
        table.add_column("Estado", style="red", justify="center")
        table.add_column("ID Usuario", style="green", justify="center")
        table.add_column("ID Cuenta", style="yellow", justify="center")
        table.add_column("Tipo Usuario", style="blue", justify="center")
        table.add_column("Tipo Cuenta", style="magenta", justify="center")
        table.add_column("Operación", style="green", justify="center")
        table.add_column("Timestamp", style="cyan", justify="center")
        
        # Añadir filas con los datos de los PCBs
        for pcb in self.pcbs:
            table.add_row(
                pcb.get("PID", "N/A"),
                str(pcb.get("PPID", "N/A")),
                pcb.get("Estado", "N/A"),
                str(pcb.get("IDUsuario", "N/A")),
                pcb.get("IDCuenta", "N/A"),
                pcb.get("TipoUsuario", "N/A"),
                pcb.get("TipoCuenta", "N/A"),
                pcb.get("Operacion", "N/A"),
                pcb.get("Timestamp", "N/A")
            )
        
        return table
    
    def mostrar(self, actualizar_en_vivo: bool = True, intervalo: float = 2.0):
        """
        Muestra los PCBs en una tabla Rich.
        
        Args:
            actualizar_en_vivo: Si True, actualiza la vista en vivo periódicamente
            intervalo: Intervalo de actualización en segundos (solo si actualizar_en_vivo es True)
        """
        if not self.pcbs:
            print("No hay datos de PCBs para mostrar.")
            return
        
        if actualizar_en_vivo:
            with Live(auto_refresh=False) as live:
                try:
                    while True:
                        # Recargar los datos por si el archivo cambió
                        self.pcbs = self.cargar_pcbs()
                        live.update(self.generar_tabla())
                        time.sleep(intervalo)
                except KeyboardInterrupt:
                    pass
        else:
            from rich.console import Console
            console = Console()
            console.print(self.generar_tabla())
    
    def mostrar_json_crudo(self):
        """Muestra el contenido crudo del JSON en un panel Rich"""
        if not self.pcbs:
            print("No hay datos de PCBs para mostrar.")
            return
        
        from rich.console import Console
        console = Console()
        console.print(Panel.fit(
            JSON(json.dumps(self.pcbs, indent=2)),
            title="Datos crudos de PCBs",
            border_style="green"
        ))

# Ejemplo de uso:
if __name__ == "__main__":
    # Crear instancia y mostrar
    visualizador = mostrar_pcb(PCB_PATH)
    print(PCB_PATH)
    
    # Mostrar como tabla (modo estático)
    visualizador.mostrar()
    