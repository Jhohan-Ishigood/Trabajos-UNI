using System;

class Programat1
{
    static void Main()
    {
        // PROMEDIO DE NOTAS:
        Console.WriteLine("PROMEDIO DE NOTAS:");

        Console.Write("¿Cuántas notas desea ingresar?: ");
        int cantidad = int.Parse(Console.ReadLine() ?? "0");

        double suma = 0;

        // Bucle para ingresar las notas
        for (int i = 0; i < cantidad; i++)
        {
            Console.Write($"Ingrese la nota {i + 1}: ");
            double nota = double.Parse(Console.ReadLine() ?? "0");
            suma += nota;
        }

        // Calcular el promedio
        double promedio = suma / cantidad;

        // Mostrar el promedio final con 2 decimales
        Console.WriteLine($"\nEl promedio final es: {promedio:F2}");

        // Verificar el estado del alumno
        if (promedio >= 11)
        {
            Console.WriteLine("Estado: APROBADO");
        }
        else
        {
            Console.WriteLine("Estado: DESAPROBADO");
        }
    }
}
