import os
import json
import random
from faker import Faker
import sys

from general.utils.utils import CLIENTES_PATH  
from general.utils.utils import quitar_acentos, formatear_telefono

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

"""
Clase que representa a un cliente con sus datos personales.
Genera información aleatoria para campos no proporcionados.
"""
class Client:
    def __init__(self, id_usuario=None, nombre=None, contrasena=None, num_telefono=None, direccion=None):
        fake = Faker('es_MX')
        self.id_usuario = id_usuario or self._generar_id_unico()
        self.nombre = nombre or quitar_acentos(fake.name())
        self.contrasena = contrasena or self._generar_contrasena()
        self.num_telefono = num_telefono or formatear_telefono(fake.phone_number())
        self.direccion = direccion or quitar_acentos(fake.address().replace('\n', ', '))

        """
        Genera un ID numérico único para el cliente, verificando que no exista
        en el archivo clientes.json.
        """
    def _generar_id_unico(self):
        existentes = set()
        if os.path.exists('clientes.json'):
            with open('clientes.json', 'r') as f:
                clientes = json.load(f)
                existentes = {c['id_usuario'] for c in clientes}
        while True:
            nuevo_id = random.randint(1000, 9999)
            if nuevo_id not in existentes:
                return nuevo_id

    """
        Genera una contraseña aleatoria segura de 12 caracteres que incluye:
        - Letras minúsculas
        - Letras mayúsculas
        - Números
        - Caracteres especiales (!^*)
    """
    def _generar_contrasena(self):
        caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!^*'
        return ''.join(random.choice(caracteres) for _ in range(12))


    """
        Convierte el objeto Client a un diccionario para facilitar
        su serialización a JSON.
    """
    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'contrasena': self.contrasena,
            'num_telefono': self.num_telefono,
            'direccion': self.direccion
        }
