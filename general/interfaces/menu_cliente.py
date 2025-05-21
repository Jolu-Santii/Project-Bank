def menu_clientes():
    print("Menú para clientes (ventanilla)")
    print("Operaciones disponibles:")
    print("1. Depósitos")
    print("2. Retiros")
    print("3. Consultas de saldo")
    print("4. Pago de servicios y préstamos")
    print("5. Transferencias")
    print("6. Solicitud de tarjetas (débito, crédito, temporales)")
    print("0. Salir")

    while True:
        opcion = input("Seleccione una opción: ")
        if opcion == "0":
            print("Saliendo del menú de clientes.")
            break
        else:
            print(f"")