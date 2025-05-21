import unicodedata
import json
import os
from cliente.cuentas.cuenta2 import Cuenta
from multiprocessing import Lock
import shutil
from pathlib import Path

pcb_lock = Lock()
cuentas_lock = Lock()

# Subimos dos niveles desde este archivo (por ejemplo, desde cliente/cuentas/gestion_cuenta.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Ruta hacia la carpeta general/datos
DATOS_PATH = os.path.join(BASE_DIR, 'general', 'datos')

# Rutas de archivos
CUENTAS_PATH = os.path.join(DATOS_PATH, 'cuentas.json')
CLIENTES_PATH = os.path.join(DATOS_PATH, 'clientes.json')
PCB_PATH = os.path.join(DATOS_PATH, 'pcb.json')

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

def eliminar_carpeta_datos():
    datos_dir = DATOS_PATH
    if datos_dir is None:
        datos_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'general', 'datos')
    
    datos_path = Path(datos_dir).resolve()

def formatear_telefono(numero):
    digitos = ''.join(filter(str.isdigit, numero))
    if len(digitos) >= 10:
        return f"{digitos[-10:-7]}-{digitos[-7:-4]}-{digitos[-4:]}"
    else:
        return numero

def cargar_cuentas():
    if os.path.exists(CUENTAS_PATH):
        with open(CUENTAS_PATH, 'r') as f:
            try:
                return [Cuenta.from_dict(c) for c in json.load(f)]
            except json.JSONDecodeError:
                return []
    return []

def guardar_cuentas(cuentas):
    os.makedirs(os.path.dirname(CUENTAS_PATH), exist_ok=True) 
    with open(CUENTAS_PATH, 'w') as f:
        json.dump([c.to_dict() for c in cuentas], f, indent=4)


def inicializar_archivo(filename, default=[]):
    """Asegura que el archivo JSON exista"""
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default, f)

def guardar_en_pcb(proceso_dict, lock):
    with lock:
        try:
            os.makedirs(os.path.dirname(PCB_PATH), exist_ok=True)
            try:
                with open(PCB_PATH, 'r') as f:
                    pcb = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pcb = []

            pcb.append(proceso_dict)

            with open(PCB_PATH, 'w') as f:
                json.dump(pcb, f, indent=4)

            print(f"Proceso {proceso_dict.get('PID')} guardado correctamente en PCB")
        except Exception as e:
            print(f"Error al guardar en PCB: {str(e)}")
            raise

            
def obtener_datos_cliente(id_usuario):
    with cuentas_lock:
        with open(CUENTAS_PATH, 'r') as f:
            try:
                cuentas = json.load(f)
            except json.JSONDecodeError:
                return None
        for cuenta in cuentas:
            if cuenta.get('id_usuario') == id_usuario:
                return cuenta
    return None