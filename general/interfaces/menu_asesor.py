def menu_asesor():
    print("Atención del asesor")
    print("Operaciones disponibles:")
    print("1. Consulta de cuentas activas")
    print("2. Modificación de cuenta")
    print("3. Alta de nuevas cuentas (captura de datos personales)")
    print("4. Baja temporal o definitiva")
    print("0. Salir")

    while True:
        opcion = input("Seleccione una opción: ")
        if opcion == "0":
            print("Saliendo del menú del asesor.")
            break
        else:
            print("")