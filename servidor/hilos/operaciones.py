import time
import random
import sys, os, json

from multiprocessing import Process, Lock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from servidor.hilos.procesos import crear_proceso
#from servidor.hilos.pcb import terminar_proceso
from general.utils.utils import inicializar_archivo, CUENTAS_PATH

cuentas_lock = Lock()

def ejecutar_operacion(tipo_usuario, id_usuario=None, operacion=None):
    try:
        proceso = crear_proceso(tipo_usuario, id_usuario, operacion)
        print(f"[Proceso {proceso.pid}] En espera {operacion}...")

        time.sleep(2 if "Consulta" in operacion else 3)

        #terminar_proceso(proceso)
        #print(f"[Proceso {proceso.pid}] {operacion} completada exitosamente")
    except Exception as e:
        print(f"[Error] En operación {operacion}: {str(e)}")

def generar_solicitudes_automaticas():
    operaciones_clientes = ["NULL"]
    operaciones_visitantes = ["NULL"]
    solicitudes = []

    with cuentas_lock:
        inicializar_archivo(CUENTAS_PATH)
        with open(CUENTAS_PATH, 'r') as f:
            cuentas = json.load(f)

    for cuenta in cuentas:
        id_usuario = cuenta.get('id_usuario')
        if id_usuario:
            for _ in range(random.randint(1, 1)):
                operacion = random.choice(operaciones_clientes)
                solicitudes.append(("Cliente", id_usuario, operacion))

    for _ in range(random.randint(1, 1)):
        operacion = random.choice(operaciones_visitantes)
        solicitudes.append(("Visitante", None, operacion))
        solicitudes.append(("Visitante", None, operacion))

    return solicitudes
