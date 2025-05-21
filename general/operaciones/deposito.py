from .base_operacion import BaseOperacion

class Deposito(BaseOperacion):
    def __init__(self, id_cuenta, monto):
        super().__init__(id_cuenta)
        self.monto = float(monto)
    
    def ejecutar(self):
        cuenta = self.obtener_cuenta()
        if cuenta['estado_cuenta'] != 'activa':
            raise ValueError("Cuenta inactiva, no se puede depositar")

        nuevo_saldo = float(cuenta['saldo']) + self.monto
        self.actualizar_cuenta({'saldo': round(nuevo_saldo, 2)})
        return {
            'mensaje': 'Depósito exitoso',
            'nuevo_saldo': round(nuevo_saldo, 2)
        }
