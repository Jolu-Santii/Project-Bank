from queue import PriorityQueue
from multiprocessing import Semaphore, Lock, Process
from despachar import despachar_proceso
from servidor.hilos.procesos import crear_proceso
ventanillas = Semaphore(2)  # 2 ventanillas
asesores = Semaphore(2)     # 2 asesores
cola_prioridad = PriorityQueue()

def planificador(solicitudes):
    for tipo, id_usuario, operacion in solicitudes:
        proceso = crear_proceso(tipo, id_usuario, operacion)
        cola_prioridad.put((proceso.prioridad, proceso))  # ordenado por prioridad

    procesos_en_ejecucion = []

    while not cola_prioridad.empty():
        _, proceso = cola_prioridad.get()

        if proceso.destino == "Ventanilla":
            sem = ventanillas
        elif proceso.destino == "Asesor":
            sem = asesores
        else:
            print(f"[{proceso.pid}] Destino desconocido. Saltando...")
            continue

        # Espera a que el recurso esté libre
        sem.acquire()

        # Lanza proceso en paralelo
        p = Process(target=despachar_proceso, args=(proceso, sem))
        p.start()
        procesos_en_ejecucion.append(p)

    for p in procesos_en_ejecucion:
        p.join()
