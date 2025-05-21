from multiprocessing import Process, Lock
import threading
import json, time, os, shutil, sys, datetime
from pathlib import Path

pcb_lock = threading.Lock()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from general.utils.utils import PCB_PATH

def actualizar_estado_pcb(pid, estado=None, prioridad=None, destino=None, operacion = None):
    with pcb_lock:
        try:
            # Leer el archivo PCB
            with open(PCB_PATH, 'r+') as f:
                pcb = json.load(f)
                
                # Buscar y actualizar el proceso correspondiente
                for proceso in pcb:
                    if str(proceso["PID"]) == str(pid):
                        if estado is not None:
                            proceso["Estado"] = estado
                        if prioridad is not None:
                            proceso["Prioridad"] = prioridad
                        if prioridad is not None:
                            proceso["Prioridad"] = prioridad
                        if destino is not None:
                            proceso["Destino"] = destino
                        if operacion is not None:
                            proceso["Operacion"] = operacion
                        break
                
                # Guardar los cambios
                f.seek(0)
                f.truncate()
                json.dump(pcb, f, indent=4)
                
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo PCB en {PCB_PATH}")
        except json.JSONDecodeError:
            print("Error: El archivo PCB no tiene un formato JSON válido")
        except Exception as e:
            print(f"Error inesperado al actualizar PCB: {str(e)}")