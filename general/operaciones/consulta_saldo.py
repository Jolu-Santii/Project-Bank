from .base_operacion import BaseOperacion

class ConsultaSaldo(BaseOperacion):
    def __init__(self, id_cuenta):
        super().__init__(id_cuenta)
    
    def ejecutar(self):
        cuenta = self.obtener_cuenta()
        return {
            'id_cuenta': cuenta['id_cuenta'],
            'saldo': cuenta['saldo'],
            'estado': cuenta['estado_cuenta']
        }