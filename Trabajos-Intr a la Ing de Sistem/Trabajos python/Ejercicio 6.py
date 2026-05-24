# CÁLCULO DE PRECIO A COBRAR POR GALONES DE COMBUSTIBLE
print("CÁLCULO DE PRECIO A COBRAR POR GALONES DE COMBUSTIBLE:")

# Constantes
PRECIO_LITRO = 10.50
GALON_A_LITROS = 3.785

# Entrada
galones = float(input("Ingrese la cantidad de galones surtidos: "))

# Proceso
litros = galones * GALON_A_LITROS
total_cobrar = litros * PRECIO_LITRO

# Salida
print(f"Cantidad de litros equivalentes: {litros:.3f} lts.")
print(f"El total a cobrar al cliente es: S/ {total_cobrar:.2f}")
