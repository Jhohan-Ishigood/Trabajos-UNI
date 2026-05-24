# DISTRIBUCIÓN DE PRESUPUESTO PARA OBRAS EN AVENIDAS
print("DISTRIBUCIÓN DE PRESUPUESTO PARA OBRAS EN AVENIDAS:")

# Entrada
inversion = float(input("Ingrese el monto de inversión en soles: S/ "))

# Procesos
Av_1 = inversion * 0.35
Av_2 = inversion * 0.25
Av_3 = inversion * 0.10
Av_4 = inversion * 0.15
Av_5 = inversion * 0.15

presu = {
    "Av": ["Av. La Mar", "Av. Abancay", "Av. 28 Julio", "Av. Aviacion", "Av. Tacna"],
    "pre": [Av_1, Av_2, Av_3, Av_4, Av_5]
}

# Salida
for i in range(len(presu["Av"])):
    print(presu["Av"][i], "tiene un presupuesto de: S/", presu["pre"][i])
    