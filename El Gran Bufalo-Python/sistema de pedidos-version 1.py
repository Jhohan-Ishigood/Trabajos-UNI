# Sistema de pedidos - Gran Buffalo
# Variables principales
total = 0
continuar = "SI"
print(" SISTEMA DE PEDIDOS GRAN BUFFALO ")
# Repetición principal
while continuar == "SI":

    # Mostrar menú
    print("\nMENU")
    print("1. Hamburguesa - S/18")
    print("2. Parrilla - S/35")
    print("3. Bebida - S/6")

    # Leer opción
    opcion = int(input("Seleccione una opcion: "))
    
    # Validar producto
    if opcion >= 1 and opcion <= 3:

        cantidad = int(input("Ingrese cantidad: "))

        # Validar cantidad
        if cantidad > 0:

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
            total = total + subtotal

            # Mostrar resultados
            print("\nProducto:", producto)
            print("Subtotal:", subtotal)
            print("Total acumulado:", total)

        else:
            print("Cantidad invalida")

    else:
        print("Producto no disponible")

    # Preguntar si desea continuar
    continuar = input(
        "\nDesea agregar otro producto? (SI/NO): "
    ).upper()

# Validar compra
if total > 0:

    print("\nTotal final:", total)

    pago = float(input("Ingrese monto de pago: "))

    # Validar pago
    if pago >= total:

        vuelto = pago - total

        print("Pago realizado correctamente")
        print("Vuelto:", vuelto)
        print("Pedido registrado")

    else:
        print("Pago insuficiente")

else:
    print("No se realizo ningun pedido")

print("\nGracias por utilizar el sistema")