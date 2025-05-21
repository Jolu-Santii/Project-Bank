from rich.live import Live
from rich.table import Table
from rich.json import JSON
from rich.panel import Panel
from rich.console import Console
from rich.layout import Layout
from rich.text import Text
import json
import os
import time
from typing import List, Dict, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATOS_PATH = os.path.join(BASE_DIR, 'general', 'datos')
PCB_PATH = os.path.join(DATOS_PATH, 'pcb.json')

class PCBWatcher(FileSystemEventHandler):
    """Monitor de cambios en el archivo PCB"""
    def __init__(self, callback):
        self.callback = callback
    
    def on_modified(self, event):
        if event.src_path.endswith('pcb.json'):
            self.callback()

class mostrar_pcb:
    def __init__(self, archivo_json: str):
        self.archivo_json = archivo_json
        self.pcbs = self.cargar_pcbs()
        self.console = Console()
        self.last_update = time.time()
        self.error = None
    
    def cargar_pcbs(self) -> List[Dict]:
        """Carga los PCBs desde el archivo JSON"""
        try:
            with open(self.archivo_json, 'r') as f:
                data = json.load(f)
                self.error = None
                return data
        except FileNotFoundError:
            self.error = f"Error: No se encontró el archivo {self.archivo_json}"
            return []
        except json.JSONDecodeError as e:
            self.error = f"Error JSON: {str(e)}"
            return []
        except Exception as e:
            self.error = f"Error inesperado: {str(e)}"
            return []
    
    def _get_state_style(self, estado: str) -> str:
        """Devuelve el estilo Rich según el estado del proceso"""
        estados = {
            "En espera": "yellow",
            "Ejecutando": "green",
            "Terminado": "blue",
            "Bloqueado": "red",
            "Error": "bold red",
            "N/A": "dim"
        }
        return estados.get(estado, "white")
    
    def generar_tabla(self) -> Table:
        """Genera una tabla Rich con la información de los PCBs"""
        table = Table(
            title=f"📋 PCB - Procesos [dim](Actualizado: {time.strftime('%H:%M:%S')})[/]",
            border_style="blue",
            header_style="bold magenta",
            expand=True
        )
        
        # Columnas principales
        columnas = [
            ("PID", "cyan", "center"),
            ("PPID", "magenta", "center"),
            ("Estado", self._get_state_style, "left"),
            ("Usuario", "green", "center"),
            ("Tipo", "blue", "center"),
            ("Prioridad", "green", "center"),  # Asegúrate que está como "green" y "center"
            ("Destino", "blue", "center"),
            ("Operación", "yellow", "left"),
            ("Timestamp", "cyan", "center")
        ]
        
        for col, style, justify in columnas:
            if callable(style):
                table.add_column(col, justify=justify)
            else:
                table.add_column(col, style=style, justify=justify)
        
        # Añadir filas con los datos
        for pcb in self.pcbs:
            estado = pcb.get("Estado", "N/A")
            
            # Convertir Prioridad a string si es numérico
            prioridad = pcb.get("Prioridad", "N/A")
            if isinstance(prioridad, int):
                prioridad = str(prioridad)
            
            row = [
                pcb.get("PID", "N/A"),
                str(pcb.get("PPID", "N/A")),
                Text(estado, style=self._get_state_style(estado)),
                str(pcb.get("IDUsuario", "N/A")),
                pcb.get("TipoUsuario", "N/A"),
                prioridad,  # Ahora es string
                pcb.get("Destino", "N/A"),
                pcb.get("Operacion", "N/A"),
                pcb.get("Timestamp", "N/A")
            ]
            
            # Resaltar procesos activos
            if estado == "Ejecutando":
                for i, item in enumerate(row):
                    if isinstance(item, str):
                        row[i] = Text(item, style="bold green")
            
            table.add_row(*row)
        
        return table

    def generar_layout(self) -> Layout:
        """Genera un layout completo con tabla y posibles mensajes de error"""
        layout = Layout()
        
        if self.error:
            layout.split_column(
                Layout(Panel.fit(f"[red]{self.error}[/]", title="Error", border_style="red")),
                Layout(self.generar_tabla())
            )
        else:
            layout.update(self.generar_tabla())
        
        return layout
    
    def mostrar(self, modo_vivo: bool = True, intervalo: float = 1.0):
        """
        Muestra los PCBs con diferentes opciones de visualización.
        
        Args:
            modo_vivo: Si True, muestra una vista que se actualiza automáticamente
            intervalo: Intervalo de actualización en segundos (solo para modo polling)
        """
        if not modo_vivo:
            self.console.print(self.generar_layout())
            return
        
        # Modo live con watchdog (más eficiente)
        try:
            layout = Layout()
            
            def actualizar():
                self.pcbs = self.cargar_pcbs()
                layout.update(self.generar_layout())
            
            event_handler = PCBWatcher(actualizar)
            observer = Observer()
            observer.schedule(event_handler, os.path.dirname(self.archivo_json))
            observer.start()
            
            try:
                with Live(layout, refresh_per_second=4, screen=True) as live:
                    actualizar()  # Carga inicial
                    while True:
                        time.sleep(0.1)
            except KeyboardInterrupt:
                observer.stop()
            
            observer.join()
            
        except ImportError:
            # Fallback a polling si watchdog no está disponible
            self.console.print("[yellow]Advertencia: watchdog no disponible, usando polling[/]")
            with Live(self.generar_layout(), refresh_per_second=4) as live:
                try:
                    while True:
                        self.pcbs = self.cargar_pcbs()
                        live.update(self.generar_layout())
                        time.sleep(intervalo)
                except KeyboardInterrupt:
                    pass
    
    def mostrar_json_crudo(self):
        """Muestra el contenido crudo del JSON en un panel Rich"""
        try:
            with open(self.archivo_json, 'r') as f:
                data = json.load(f)
                self.console.print(
                    Panel.fit(
                        JSON.from_data(data),
                        title="[bold green]Datos crudos de PCBs[/]",
                        border_style="green",
                        subtitle=f"{len(data)} procesos"
                    )
                )
        except Exception as e:
            self.console.print(
                Panel.fit(
                    f"[red]Error cargando JSON: {str(e)}[/]",
                    title="Error",
                    border_style="red"
                )
            )

if __name__ == "__main__":
    # Ejemplo de uso
    visualizador = mostrar_pcb(PCB_PATH)
    
    # Mostrar ayuda
    print("\nOpciones disponibles:")
    print("1. Vista en tiempo real")
    print("2. Ver JSON crudo")
    print("3. Salir")
    
    while True:
        opcion = input("\nSeleccione una opción (1-4): ")
        
        if opcion == "1":
            print("\nIniciando vista en tiempo real... (Presione Ctrl+C para salir)")
            try:
                visualizador.mostrar(modo_vivo=True)
            except KeyboardInterrupt:
                print("\nRegresando al menú principal...")
        elif opcion == "2":
            visualizador.mostrar_json_crudo()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")