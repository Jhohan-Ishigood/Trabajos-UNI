# SISTEMA DE PEDIDOS - GRAN BUFFALO

# Variables principales
total = 0
continuar = "SI"

print("===================================")
print("   SISTEMA DE PEDIDOS GRAN BUFFALO")
print("===================================")

# Repetición principal
while continuar == "SI":

    print("\n----------- MENU -----------")
    print("1. Hamburguesa - S/18")
    print("2. Parrilla     - S/35")
    print("3. Bebida       - S/6")

    # Validar opción
    while True:
        try:
            opcion = int(input("\nSeleccione una opción: "))

            if opcion >= 1 and opcion <= 3:
                break
            else:
                print("Error: Producto no disponible.")

        except ValueError:
            print("Error: Debe ingresar solo números.")

    # Validar cantidad
    while True:
        try:
            cantidad = int(input("Ingrese cantidad: "))

            if cantidad > 0:
                break
            else:
                print("Error: La cantidad debe ser mayor a 0.")

        except ValueError:
            print("Error: Debe ingresar solo números.")

    # Calcular subtotal
    if opcion == 1:
        subtotal = cantidad * 18
        producto = "Hamburguesa"

    elif opcion == 2:
        subtotal = cantidad * 35
        producto = "Parrilla"

    else:
        subtotal = cantidad * 6
        producto = "Bebida"

    # Acumular total
    total += subtotal

    # Mostrar resultados
    print("\nProducto:", producto)
    print("Cantidad:", cantidad)
    print("Subtotal: S/", subtotal)
    print("Total acumulado: S/", total)

    # Preguntar si desea continuar
    continuar = input(
        "\n¿Desea agregar otro producto? (SI/NO): "
    ).upper()

# Validar compra
if total > 0:

    print("\n===================================")
    print("TOTAL FINAL: S/", total)
    print("===================================")

    # Validar pago
    while True:
        try:
            pago = float(input("Ingrese monto de pago: S/ "))

            if pago >= total:
                break
            else:
                print("Error: Pago insuficiente.")

        except ValueError:
            print("Error: Debe ingresar un número válido.")

    vuelto = pago - total

    print("\nPago realizado correctamente")
    print("Vuelto: S/", round(vuelto, 2))
    print("Pedido registrado exitosamente")

else:
    print("\nNo se realizó ningún pedido")

print("\nGracias por utilizar el sistema")