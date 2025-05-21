
import os
import json
import random
import sys


from cliente.cuentas.cuenta2 import Cuenta

# Corregido: doble guion bajo en __file__ y cierre del paréntesis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from general.utils.utils import cargar_cuentas, guardar_cuentas



# BASE_DIR ahora apunta a la raíz del proyecto BANCO/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# CLIENTES_PATH apunta a BANCO/general/datos/clientes.json
CLIENTES_PATH = os.path.join(BASE_DIR, 'general', 'datos', 'clientes.json')
                  
def crear_cuenta_para_cliente(id_usuario):
    if not os.path.exists(CLIENTES_PATH):
        print("Error: No existe el archivo de clientes")
        return None

    with open(CLIENTES_PATH, 'r') as f:
        clientes = json.load(f)

    id_usuario = int(id_usuario)
    cliente = next((c for c in clientes if c['id_usuario'] == id_usuario), None)
    if not cliente:
        print(f"Error: No existe cliente con ID {id_usuario}")
        return None

    nueva_cuenta = Cuenta(
        id_usuario=id_usuario,
        saldo=round(random.uniform(500, 100000), 2),
        adeudos=round(random.uniform(0, 2000), 2)
    )
    
    cuentas = cargar_cuentas()
    cuentas.append(nueva_cuenta)
    guardar_cuentas(cuentas)

    print(f"Cuenta {nueva_cuenta.id_cuenta} creada para cliente {id_usuario}")
    return nueva_cuenta

def obtener_cuentas_por_usuario(id_usuario):
    try:
        id_usuario = int(id_usuario)
        cuentas = cargar_cuentas()
        return [c for c in cuentas if c.id_usuario == id_usuario]
    except ValueError:
        print(f"Error: ID de usuario inválido {id_usuario}")
        return []

def gestionar_cuenta(accion, cuenta=None, id_cuenta=None, nuevos_datos=None):
    try:
        cuentas = cargar_cuentas()
        cuentas_dict = {c.id_cuenta: c for c in cuentas}

        if accion == 'agregar':
            if not cuenta or not cuenta.id_usuario:
                print("Error: Falta información para agregar la cuenta")
                return False
            if cuenta.id_cuenta in cuentas_dict:
                print(f"Error: La cuenta {cuenta.id_cuenta} ya existe")
                return False
            cuentas_dict[cuenta.id_cuenta] = cuenta
            print(f"Cuenta {cuenta.id_cuenta} agregada correctamente")

        elif accion == 'eliminar':
            if not id_cuenta or id_cuenta not in cuentas_dict:
                print("Error: Cuenta no encontrada para eliminar")
                return False
            del cuentas_dict[id_cuenta]
            print(f"Cuenta {id_cuenta} eliminada correctamente")

        elif accion == 'modificar':
            if not id_cuenta or not nuevos_datos or id_cuenta not in cuentas_dict:
                print("Error: Datos inválidos para modificar")
                return False
            cuenta = cuentas_dict[id_cuenta]
            for key, value in nuevos_datos.items():
                if hasattr(cuenta, key) and key not in ['id_cuenta', 'id_usuario']:
                    try:
                        if key in ['saldo', 'adeudos']:
                            value = float(value)
                        setattr(cuenta, key, value)
                    except Exception as e:
                        print(f"Error al actualizar {key}: {str(e)}")
                        return False
            print(f"Cuenta {id_cuenta} modificada correctamente")
        else:
            print("Error: Acción no válida")
            return False

        guardar_cuentas(list(cuentas_dict.values()))
        return True

    except Exception as e:
        print(f"Error al gestionar cuenta: {str(e)}")
        return False

def crear_cuentas_automaticamente_por_clientes():
    if not os.path.exists(CLIENTES_PATH):
        print("Error: No existe el archivo de clientes")
        return
    with open(CLIENTES_PATH, 'r') as f:
        clientes = json.load(f)

    for cliente in clientes:
        crear_cuenta_para_cliente(cliente["id_usuario"])
