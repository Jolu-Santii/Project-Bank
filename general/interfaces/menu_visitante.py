def menu_visitantes():
    print("Menú para visitantes")
    print("Operaciones bancarias disponibles:")
    print("1. Depósitos")
    print("2. Retiros")
    print("3. Transferencias")
    print("4. Pagos de servicios")
    print("5. Solicitud de creación de cuenta")
    print("6. Consulta con asesor (Se agrega a la cola FIFO)")
    print("0. Salir")

    while True:
        opcion = input("Seleccione una opción: ")
        if opcion == "0":
            print("Saliendo del menú de visitantes.")
            break
        else:
            print("")