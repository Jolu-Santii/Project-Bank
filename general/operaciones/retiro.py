from .base_operacion import BaseOperacion

class Retiro(BaseOperacion):
    def __init__(self, id_cuenta, monto):
        super().__init__(id_cuenta)
        self.monto = float(monto)
    
    def ejecutar(self):
        cuenta = self.obtener_cuenta()
        if cuenta['estado_cuenta'] != 'activa':
            raise ValueError("Cuenta inactiva, no se puede retirar")

        saldo_actual = float(cuenta['saldo'])
        if saldo_actual < self.monto:
            raise ValueError(f"Fondos insuficientes. Saldo actual: {saldo_actual}")
        
        nuevo_saldo = saldo_actual - self.monto
        self.actualizar_cuenta({'saldo': round(nuevo_saldo, 2)})
        return {
            'mensaje': 'Retiro exitoso',
            'nuevo_saldo': round(nuevo_saldo, 2)
        }
