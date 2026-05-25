using System;

class Ejercicio3 {
    public static void Ejecutar() {
        // Algoritmo ParOImpar
        int n;

        Console.Write("Ingresa un número entero: ");
        n = Convert.ToInt32(Console.ReadLine());

        if (n % 2 == 0) {
            Console.WriteLine(n + " es un número PAR");
        } else {
            Console.WriteLine(n + " es un número IMPAR");
        }
    }
}



