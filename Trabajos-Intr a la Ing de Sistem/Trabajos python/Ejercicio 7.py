# PROMEDIO DE CALIFICACIONES OBTENIDAS EN UN CURSO:
print("PROMEDIO DE CALIFICACIONES OBTENIDAS EN UN CURSO:")

# Entrada de calificaciones
nota1 = float(input("Ingrese la nota del primer examen (20%): "))
nota2 = float(input("Ingrese la nota del segundo examen (30%): "))
nota3 = float(input("Ingrese la nota del tercer examen (50%): "))

# Cálculo del promedio ponderado
promedio = (nota1 * 0.20) + (nota2 * 0.30) + (nota3 * 0.50)

# Salida del resultado
print(f"El promedio de las calificaciones obtenidas es: {promedio}")
