
#PROMEDIO DE NOTAS:
print("PROMEDIO DE NOTAS:")

cantidad = int(input("¿Cuántas notas desea ingresar?: "))

suma = 0

for i in range(cantidad):
    nota = float(input(f"Ingrese la nota {i + 1}: "))
    suma += nota

promedio = suma / cantidad

print(f"\nEl promedio final es: {promedio:.2f}")

if promedio >= 11:
    print("Estado: APROBADO")
else:
    print("Estado: DESAPROBADO")
