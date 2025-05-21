import json
from pathlib import Path

class BaseOperacion:
    def __init__(self, id_cuenta):
        self.id_cuenta = id_cuenta
        self.cuentas_path = Path(__file__).resolve().parent.parent.parent / 'cuentas.json'
            
    def cargar_cuentas(self):
        if not self.cuentas_path.exists():
            raise FileNotFoundError("No existe el archivo cuentas.json")
        try:
            with open(self.cuentas_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Error al leer el archivo cuentas.json")

    def guardar_cuentas(self, cuentas):
        with open(self.cuentas_path, 'w') as f:
            json.dump(cuentas, f, indent=4)
    
    def obtener_cuenta(self):
        cuentas = self.cargar_cuentas()
        for cuenta in cuentas:
            if cuenta['id_cuenta'] == self.id_cuenta:
                return cuenta
        raise ValueError(f"No existe la cuenta: {self.id_cuenta}")
    
    def actualizar_cuenta(self, nuevos_datos):
        cuentas = self.cargar_cuentas()
        for cuenta in cuentas:
            if cuenta['id_cuenta'] == self.id_cuenta:
                cuenta.update(nuevos_datos)
                self.guardar_cuentas(cuentas)
                return
        raise ValueError(f"No se encontró la cuenta para actualizar: {self.id_cuenta}")
