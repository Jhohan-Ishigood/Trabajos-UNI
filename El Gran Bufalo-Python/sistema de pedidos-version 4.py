# SISTEMA DE PEDIDOS - EL GRAN BUFFALO

from datetime import datetime

# Variables principales
total = 0
productos = []
cantidades = []
subtotales = []

continuar = "SI"

# Fecha y hora
fecha = datetime.now()

# Encabezado
print("_" * 45)
print("\nSISTEMA DE PEDIDOS GRAN BUFFALO")
print("_" * 45)
print("\nFecha y hora:", fecha.strftime("%d/%m/%Y %H:%M:%S"))

# Bucle principal
while continuar == "SI":

    # Menu
    print("\nEL MENU DE HOY:")
    print("\n1. Hamburguesa   - S/18")
    print("2. Carne a la parrilla - S/35")
    print("3. Bebida - S/6")
    print("4. Combo Buffalo - S/25")
    print("_" * 28)

    # Validar opcion
    while True:
        try:
            opcion = int(input("\nSeleccione una opcion: "))

            if opcion >= 1 and opcion <= 4:
                break
            else:
                print("Error: Opcion no valida")

        except ValueError:
            print("Error: Debe ingresar solo numeros")

    # Validar cantidad
    while True:
        try:
            cantidad = int(input("Ingrese cantidad: "))

            if cantidad > 0:
                break
            else:
                print("Error: La cantidad debe ser mayor a 0")

        except ValueError:
            print("Error: Debe ingresar solo numeros")

    # Procesar pedido
    if opcion == 1:
        producto = "Hamburguesa"
        precio = 18

    elif opcion == 2:
        producto = "Carne a la parrilla"
        precio = 35

    elif opcion == 3:
        producto = "Bebida"
        precio = 6

    else:
        producto = "Combo Buffalo"
        precio = 25

    # Calcular subtotal
    subtotal = cantidad * precio

    # Guardar datos
    productos.append(producto)
    cantidades.append(cantidad)
    subtotales.append(subtotal)

    # Acumular total
    total += subtotal

    # Mostrar resumen
    print("\nProducto agregado correctamente:")
    print("\nProducto:", producto)
    print("Cantidad:", cantidad)
    print("Subtotal: S/", subtotal)
    print("Total acumulado: S/", total)

    # Preguntar si desea continuar
    while True:

        continuar = input(
            "Desea agregar otro producto? (SI/NO): "
        ).upper()

        if continuar == "SI" or continuar == "NO":
            break
        else:
            print("Error: Ingrese solo SI o NO")

# Verificar compra
if total > 0:

    # Delivery
    print("\n")

    while True:

        delivery = input(
            "Desea delivery? (SI/NO): "
        ).upper()

        if delivery == "SI" or delivery == "NO":
            break
        else:
            print("Error: Ingrese solo SI o NO")

    if delivery == "SI":
        total += 6
        print("\nMonto por Delivery agregado: S/6")

    # Aumento
    Delivery = 6

    if total > 100:
        total = total + Delivery

    # Boleta
    print("\n" + "_" * 8)
    print("\n BOLETA")
    print("_" * 8)

    print("\nFecha y hora:", fecha.strftime("%d/%m/%Y %H:%M:%S"))
    for i in range(len(productos)):
        print("\n",
            productos[i],
            "x",
            cantidades[i],
            "= S/",
            subtotales[i]
        )
        
    print("\nDelivery: S/", round(Delivery, 2))
    print("____________________")
    print("\nTOTAL FINAL: S/", round(total, 2))
    print("_" * 22)

    # Metodo de pago
    print("\nMETODO DE PAGO")
    print("\n1. Efectivo")
    print("2. Yape")
    print("3. Tarjeta")

    while True:
        try:
            metodo = int(input("\nSeleccione metodo de pago: "))

            if metodo >= 1 and metodo <= 3:
                break
            else:
                print("Opcion invalida")

        except ValueError:
            print("Debe ingresar solo numeros")

    # Validar pago
    while True:
        try:
            pago = float(input("Ingrese monto de pago: S/ "))

            if pago <= 0:
                print("El pago debe ser mayor a 0")

            elif pago >= total:
                break

            else:
                print("Pago insuficiente")

        except ValueError:
            print("Debe ingresar un numero valido")

    # Calcular vuelto
    vuelto = pago - total

    # Confirmacion final
    print("\nPAGO REALIZADO CORRECTAMENTE")

    if metodo == 1:
        print("\nMetodo de pago: Efectivo")

    elif metodo == 2:
        print("\nMetodo de pago: Yape")

    else:
        print("\nMetodo de pago: Tarjeta")

    print("Vuelto: S/", round(vuelto, 2))
    print("Pedido registrado exitosamente")

else:
    print("\nNo se realizo ningun pedido")

# Despedida
print("\nGRACIAS POR SU COMPRA, VUELVA PRONTO!")
print("______________________________________")