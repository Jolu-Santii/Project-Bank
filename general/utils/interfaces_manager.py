import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado(titulo):
    print(f"\n\033[1;34m=== {titulo} ===\033[0m\n")

def mostrar_mensaje(mensaje):
    if mensaje is None:
        return

    if "ERROR" in mensaje:
        print(f"\n\033[1;31m{mensaje}\033[0m")
    elif "éxito" in mensaje or "correctamente" in mensaje:
        print(f"\n\033[1;32m{mensaje}\033[0m")
    else:
        print(f"\n\033[1;36m{mensaje}\033[0m")

def pausa():
    input("\nPresione Enter para continuar...")

def obtener_opcion_sn():
    while True:
        opcion = input().strip().lower()
        if opcion in ['s', 'n']:
            return opcion
        print("Opción inválida. Ingrese 's' o 'n': ", end='')
