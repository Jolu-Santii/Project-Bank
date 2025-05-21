import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from multiprocessing import Lock
from general.utils.utils import CUENTAS_PATH, PCB_PATH, inicializar_archivo

pcb_lock = Lock()
cuentas_lock = Lock()

def guardar_en_pcb(proceso):
    with pcb_lock:
        try:
            inicializar_archivo(PCB_PATH)
            with open(PCB_PATH, 'r+') as f:
                pcb = json.load(f)
                pcb.append(proceso.to_dict())
                f.seek(0)
                json.dump(pcb, f, indent=4)
        except Exception as e:
            print(f"Error crítico al actualizar PCB: {str(e)}")
            raise

# def terminar_proceso(proceso):
#     proceso.estado = "Finalizado"
#     guardar_en_pcb(proceso)

def obtener_datos_cliente(id_usuario):
    with cuentas_lock:
        try:
            inicializar_archivo(CUENTAS_PATH)
            with open(CUENTAS_PATH, 'r') as f:
                cuentas = json.load(f)
            for cuenta in cuentas:
                if cuenta.get('id_usuario') == id_usuario:
                    return cuenta
            return None
        except Exception as e:
            print(f"Error obteniendo datos del cliente: {str(e)}")
            return None
    datos_cliente = {
        'id_cuenta': 'CTA-XXXXXX',
        'tipo_cuenta': 'premium'  # o 'estandar' según corresponda
    }
    return datos_cliente
        


