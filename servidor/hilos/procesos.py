import os, sys, random
from datetime import datetime
from uuid import uuid4

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from servidor.hilos.pcb import obtener_datos_cliente, guardar_en_pcb

class Proceso:
    def __init__(self, tipo_usuario, pid=None, ppid=None, estado="En espera", id_usuario=None, id_cuenta=None, tipo_cuenta=None, operacion=None, prioridad=None, destino=None):
        self.pid = pid or str(random.randint(1000, 9999))
        self.ppid = ppid or str(os.getppid())
        self.estado = estado
        self.id_cuenta = id_cuenta
        self.id_usuario = id_usuario
        self.tipo_usuario = tipo_usuario
        self.tipo_cuenta = tipo_cuenta
        
        
        if tipo_cuenta == "premium":
            self.prioridad = 1
        else:  # estandar o visitante
            self.prioridad = 2
            
        self.destino = destino or random.choice(["Ventanilla", "Asesor"])
        
        self.operacion = operacion or "NULL"
        self.timestamp = datetime.now().strftime("%H:%M:%S")

    def to_dict(self):
        return {
            "PID": self.pid,
            "PPID": self.ppid,
            "Estado": self.estado,
            "IDUsuario": self.id_usuario,
            "IDCuenta": self.id_cuenta,
            "TipoUsuario": self.tipo_usuario,
            "TipoCuenta": self.tipo_cuenta,
            "Prioridad": self.prioridad,
            "Destino": self.destino,
            "Operacion": self.operacion,
            "Timestamp": self.timestamp
        }

def crear_proceso(tipo_usuario, id_usuario=None, operacion=None, prioridad = None, destino = None):
    from .pcb import obtener_datos_cliente

    if tipo_usuario == "Cliente":
        if not id_usuario:
            raise ValueError("Se requiere ID de usuario para clientes")
        datos_cliente = obtener_datos_cliente(id_usuario)
        if not datos_cliente:
            raise ValueError("Cliente no registrado o ID inválido")
        tipo_cuenta = datos_cliente.get('tipo_cuenta', 'Estándar')
        id_cuenta = datos_cliente.get('id_cuenta')
    else:
        if id_usuario is not None:
            raise ValueError("Visitante no debe tener ID de usuario")
        tipo_cuenta = None
        id_cuenta = None

    proceso = Proceso(
        id_usuario=id_usuario,
        id_cuenta=id_cuenta,
        tipo_usuario=tipo_usuario,
        tipo_cuenta=tipo_cuenta,
        prioridad=prioridad,
        destino= destino,
        operacion=operacion
    )
    guardar_en_pcb(proceso)
    return proceso
#
