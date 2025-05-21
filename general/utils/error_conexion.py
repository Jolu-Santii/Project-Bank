from interfaces_manager import limpiar_pantalla, pausa

def mostrar_error_conexion(ip_servidor, puerto_servidor):
    limpiar_pantalla()
    print("\033[1;31m", end='')
    print("========================================")
    print("  ERROR DE CONEXIÓN CON EL SERVIDOR")
    print("========================================")
    print("\033[0m\n", end='')

    print("Por favor verifique que:")
    print("1. El servidor esté en ejecución")
    print(f"2. La dirección IP ({ip_servidor}) sea correcta")
    print(f"3. El puerto ({puerto_servidor}) esté disponible\n")

    pausa()
