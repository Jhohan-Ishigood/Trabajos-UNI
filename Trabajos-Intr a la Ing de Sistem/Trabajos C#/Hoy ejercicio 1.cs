using System;

class Problema1
{
    static void Main()
    {
        Console.Write("¿Cuál es el total de su compra?: ");

        double totalCompra = double.Parse(Console.ReadLine());

        double descuento = totalCompra * 0.15;

        double total = totalCompra - descuento;

        Console.WriteLine("Con un descuento del 15% en su total de compra, debe pagar: S/" + total);
    }
}
