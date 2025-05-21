import os, sys, time
from multiprocessing import Lock, Semaphore
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.prioridad2 import PRIORIDAD, cola_procesos
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from Implementaciones.Pt2.ejecucion2 import operacion_deposito, operacion_consulta

# Semáforo global que permite solo un proceso en ejecución a la vez
semaforo_global = Semaphore(1)

def despachar_proceso(proceso):
    try:
        # Adquirir el semáforo global (solo un proceso puede ejecutarse)
        semaforo_global.acquire()
        
        # FIFO ya lo controla el planificador
        actualizar_estado_pcb(proceso.pid, estado="En ejecución", operacion=f"Asignado a {proceso.destino}")
        cuentas_lock = Lock()
        
        # Ejecuta la operación
        if proceso.operacion == "Depósito":
            operacion_deposito(proceso, monto=100.0, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Consulta":
            operacion_consulta(proceso, cuentas_lock=cuentas_lock)
        else:
            actualizar_estado_pcb(proceso.pid, estado="Error", operacion="Operación no implementada")

    finally:
        # Liberar el semáforo global cuando el proceso termine
        semaforo_global.release()