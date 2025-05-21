from queue import PriorityQueue
from multiprocessing import Process, Semaphore, Lock
import sys, os, json, time, random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from servidor.hilos.procesos import crear_proceso
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH, inicializar_archivo
from Implementaciones.Pt2.Operacion import operacion_deposito  # Debes tener esta función implementada

# Configuraciones de concurrencia
cuentas_lock = Lock()
ventanillas = Semaphore(2)
asesores = Semaphore(2)

# Operaciones válidas
OPERACIONES_CLIENTES = ["Depósito", "Consulta"]
OPERACIONES_VISITANTES = ["Consulta"]

# 1. Generar solicitudes automáticas
def generar_solicitudes_automaticas():
    solicitudes = []

    with cuentas_lock:
        inicializar_archivo(CUENTAS_PATH)
        with open(CUENTAS_PATH, 'r') as f:
            cuentas = json.load(f)

    for cuenta in cuentas:
        id_usuario = cuenta.get('id_usuario')
        if id_usuario:
            operacion = random.choice(OPERACIONES_CLIENTES)
            solicitudes.append(("Cliente", id_usuario, operacion))

    for _ in range(2):
        operacion = random.choice(OPERACIONES_VISITANTES)
        solicitudes.append(("Visitante", None, operacion))

    return solicitudes

# 2. Despachar proceso a ventanilla o asesor
def despachar_proceso(proceso, semaforo):
    try:
        actualizar_estado_pcb(proceso.pid, estado="En ejecución", operacion=f"Asignado a {proceso.destino}")

        if proceso.operacion == "Depósito":
            operacion_deposito(proceso, monto=100.0, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Consulta":
            time.sleep(1)  # Simulación
            actualizar_estado_pcb(proceso.pid, estado="Finalizado", operacion="Consulta realizada")
        else:
            actualizar_estado_pcb(proceso.pid, estado="Error", operacion="Operación no implementada")

    finally:
        semaforo.release()

# 3. Planificador de prioridades con FIFO dentro de cada nivel
def planificador():
    solicitudes = generar_solicitudes_automaticas()
    cola_prioridad = PriorityQueue()

    for tipo, id_usuario, operacion in solicitudes:
        proceso = crear_proceso(tipo, id_usuario, operacion)
        # El destino ya viene asignado aleatoriamente en el proceso
        cola_prioridad.put((proceso.prioridad, time.time(), proceso))

    procesos_en_ejecucion = []

    while not cola_prioridad.empty():
        _, _, proceso = cola_prioridad.get()

        if proceso.destino == "Ventanilla":
            sem = ventanillas
        elif proceso.destino == "Asesor":
            sem = asesores
        else:
            actualizar_estado_pcb(proceso.pid, estado="Error", operacion="Destino no válido")
            continue

        sem.acquire()
        p = Process(target=despachar_proceso, args=(proceso, sem))
        p.start()
        procesos_en_ejecucion.append(p)

    for p in procesos_en_ejecucion:
        p.join()


if __name__ == '__main__':
    planificador()
    