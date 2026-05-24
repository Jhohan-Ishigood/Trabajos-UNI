def ganancia_producto():
    # Solicitar datos al usuario
    c = float(input("Ingrese el costo de la caja: "))
    n = int(input("Ingrese la cantidad de unidades por caja: "))

    # Calcular costo por unidad
    costo_unidad = c / n

    # Precio de venta con 30% de ganancia
    p = costo_unidad * 1.30

    # Mostrar resultado redondeado a 2 decimales
    print("El precio de venta por unidad es", round(p, 2))

# Ejecutar la función
ganancia_producto()