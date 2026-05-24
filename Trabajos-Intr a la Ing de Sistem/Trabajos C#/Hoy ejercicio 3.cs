using System;

namespace EjercicioUtilidad
{
    class Program
    {
        static void Main(string[] args)
        {
            // Declaración de variables
            double c, n, costo_unidad, p;

            // Entrada de datos
            Console.Write("Ingrese el costo de la caja: ");
            c = double.Parse(Console.ReadLine());

            Console.Write("Ingrese la cantidad de unidades por caja: ");
            n = double.Parse(Console.ReadLine());

            // Proceso: Cálculo del costo por unidad y precio con 30% de utilidad
            costo_unidad = c / n;
            p = costo_unidad * 1.30;

            // Salida de resultados redondeado a 2 decimales
            Console.WriteLine("\n--- Resultados ---");
            Console.WriteLine("Costo por unidad: " + Math.Round(costo_unidad, 2));
            Console.WriteLine("El precio de venta por unidad es: " + Math.Round(p, 2));
            
            // Pausa para ver el resultado
            Console.WriteLine("\nPresione cualquier tecla para salir...");
            Console.ReadKey();
        }
    }
}