import sys
import os, sys

# Añade el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cliente.clientes.clientes import Client
from cliente.clientes.gestor import gestionar_clientes
from cliente.cuentas.gestion_cuenta import crear_cuentas_automaticamente_por_clientes

if __name__ == "__main__":
    cliente_aleatorio = Client()
    gestionar_clientes('agregar', cliente=cliente_aleatorio)
    gestionar_clientes('eliminar', id_usuario=9819)
    gestionar_clientes('generar', nuevo_data={'cantidad': 5})

    crear_cuentas_automaticamente_por_clientes()
