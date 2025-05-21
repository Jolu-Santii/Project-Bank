import os
import json
import sys

from .clientes import Client


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATOS_DIR = os.path.join(BASE_DIR, 'general', 'datos')

os.makedirs(DATOS_DIR, exist_ok=True)  # Asegura que la carpeta exista
archivo = os.path.join(DATOS_DIR, 'clientes.json')

"""
    Gestiona operaciones para los clientes almacenados en el archivo JSON.
    
Ejemplo de uso:
# 1. Generar 3 clientes aleatorios
gestionar_clientes('generar', nuevo_data={'cantidad': 3})

# 2. Agregar un cliente específico
cliente_especial = Client(
    id_usuario=9999,
    nombre="Cliente Premium"
)
gestionar_clientes('agregar', cliente=cliente_especial)

# 3. Actualizar su dirección
gestionar_clientes('modificar', 
    id_usuario=9999, 
    nuevo_data={'direccion': 'Zona Premium 001'})

# 4. Eliminarlo si es necesario
gestionar_clientes('eliminar', id_usuario=9999)
        
    """

def gestionar_clientes(accion, cliente=None, id_usuario=None, nuevo_data=None):
    try:
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                clientes = json.load(f)
        else:
            clientes = []

        # Convertimos la lista a diccionario con IDs como clave para fácil acceso
        clientes_dict = {c['id_usuario']: c for c in clientes}

        if accion == 'agregar':
            if cliente.id_usuario in clientes_dict:
                print(f"Error: El ID de usuario {cliente.id_usuario} ya existe.")
                return False
            clientes_dict[cliente.id_usuario] = cliente.to_dict()
            print(f"Cliente {cliente.nombre} agregado correctamente.")
        
        elif accion == 'eliminar':
            if id_usuario not in clientes_dict:
                print(f"Error: El ID de usuario {id_usuario} no existe.")
                return False
            del clientes_dict[id_usuario]
            print(f"Cliente con ID {id_usuario} eliminado correctamente.")

        elif accion == 'modificar':
            if id_usuario not in clientes_dict:
                print(f"Error: El ID de usuario {id_usuario} no existe.")
                return False
            for key, value in nuevo_data.items():
                if key in clientes_dict[id_usuario]:
                    clientes_dict[id_usuario][key] = value
            print(f"Cliente con ID {id_usuario} modificado correctamente.")

        # Operación: Generar clientes aleatorios
        elif accion == 'generar':
            cantidad = nuevo_data.get('cantidad', 1)
            for _ in range(cantidad):
                cliente = Client()
                clientes_dict[cliente.id_usuario] = cliente.to_dict()
                print(f"Cliente {cliente.nombre} generado con ID {cliente.id_usuario}")
        # Acción no reconocida
        else:
            print("Error: Acción no válida.")
            return False
        # Guardamos cambios en el archivo JSON
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(list(clientes_dict.values()), f, indent=4, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Error al gestionar clientes: {str(e)}")
        return False
