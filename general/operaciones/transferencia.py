from .base_operacion import BaseOperacion
#transferencia
class Transferencia:
    def __init__(self, id_origen, id_destino, monto):
        self.origen = BaseOperacion(id_origen)
        self.destino = BaseOperacion(id_destino)
        self.monto = float(monto)
    
    def ejecutar(self):
        try:
            cuenta_origen = self.origen.obtener_cuenta()
        except ValueError:
            raise ValueError("Cuenta de origen no encontrada")

        try:
            cuenta_destino = self.destino.obtener_cuenta()
        except ValueError:
            raise ValueError("Cuenta de destino no encontrada")
        
        if cuenta_origen['estado_cuenta'] != 'activa':
            raise ValueError("Cuenta de origen inactiva")
        if cuenta_destino['estado_cuenta'] != 'activa':
            raise ValueError("Cuenta de destino inactiva")

        saldo_origen = float(cuenta_origen['saldo'])
        if saldo_origen < self.monto:
            raise ValueError(f"Fondos insuficientes en cuenta origen. Saldo actual: {saldo_origen}")

        nuevo_saldo_origen = saldo_origen - self.monto
        nuevo_saldo_destino = float(cuenta_destino['saldo']) + self.monto

        self.origen.actualizar_cuenta({'saldo': round(nuevo_saldo_origen, 2)})
        self.destino.actualizar_cuenta({'saldo': round(nuevo_saldo_destino, 2)})

        return {
            'mensaje': 'Transferencia exitosa',
            'origen': {
                'id_cuenta': cuenta_origen['id_cuenta'],
                'saldo': round(nuevo_saldo_origen, 2)
            },
            'destino': {
                'id_cuenta': cuenta_destino['id_cuenta'],
                'saldo': round(nuevo_saldo_destino, 2)
            }
        }
