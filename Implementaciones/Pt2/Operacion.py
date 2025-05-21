import time
import json, sys, os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb  # asegúrate de tener esta función
from general.utils.utils import CUENTAS_PATH

def operacion_deposito(proceso, monto, cuentas_lock):
    pid = str(proceso.pid)
    id_cuenta = proceso.id_cuenta

    try:
        if monto <= 0:
            actualizar_estado_pcb(pid, estado="Fallido", operacion="Monto inválido")
            return False

        # 1. Estado: Esperando lock
        actualizar_estado_pcb(pid,
            estado="Esperando",
            operacion="Esperando acceso a cuentas",
        )

        with cuentas_lock:
            # 2. Estado: Lock adquirido
            actualizar_estado_pcb(pid,
                estado="Trabajando",
                operacion="Procesando deposito",
                recurso_esperando=None,
                recurso_adquirido="accounts_lock"
            )

            # 3. Cargar cuentas
            with open(CUENTAS_PATH, 'r+') as f:
                cuentas = json.load(f)
                cuenta = next((c for c in cuentas if c["id_cuenta"] == id_cuenta), None)

                if not cuenta:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta no encontrada")
                    return False

                # 4. Simular procesamiento
                time.sleep(2)
                cuenta["saldo"] = cuenta.get("saldo", 0) + monto

                # 5. Guardar cambios
                f.seek(0)
                f.truncate()
                json.dump(cuentas, f, indent=4)

        # 6. Estado: Finalizado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Deposito completado (+${monto:.2f})",
            recurso_esperando=None,
            recurso_adquirido=None
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en deposito: {str(e)}")
        return False
