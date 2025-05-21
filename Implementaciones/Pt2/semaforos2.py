import os, sys, time
from threading import Semaphore
from multiprocessing import Lock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from actualizar import actualizar_estado_pcb, pid

asesor_semaphore = Lock()  # Instanciación del Lock

with asesor_semaphore:
    actualizar_estado_pcb(pid, estado="Atendido por asesor", operacion="Simulación de cuenta")
    time.sleep(2)
    actualizar_estado_pcb(pid, estado="Finalizado", operacion="Simulación finalizada")
