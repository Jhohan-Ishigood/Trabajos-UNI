using System;

class Program
{
    static void Main1()
    {
        double total = 0;
        string continuar = "SI";
        Console.WriteLine("=== SISTEMA DE PEDIDOS GRAN BUFFALO ===");

        while (continuar == "SI")
        {
            Console.WriteLine("\nMENU");
            Console.WriteLine("1. Hamburguesa - S/18");
            Console.WriteLine("2. Parrilla - S/35");
            Console.WriteLine("3. Bebida - S/6");

            // Leer opción de forma segura frente a nulos o letras
            Console.Write("Seleccione una opcion: ");
            string? entradaOpcion = Console.ReadLine();
            if (!int.TryParse(entradaOpcion, out int opcion))
            {
                Console.WriteLine("Por favor, ingrese un numero valido.");
                continue;
            }

            // Validar producto
            if (opcion >= 1 && opcion <= 3)
            {
                Console.Write("Ingrese cantidad: ");
                string? entradaCantidad = Console.ReadLine();
                if (!int.TryParse(entradaCantidad, out int cantidad) || cantidad <= 0)
                {
                    Console.WriteLine("Cantidad invalida. Debe ser un numero mayor a 0.");
                    continue;
                }

                double subtotal = 0;
                string producto = "";

                // Calcular subtotal
                if (opcion == 1)
                {
                    subtotal = cantidad * 18;
                    producto = "Hamburguesa";
                }
                else if (opcion == 2)
                {
                    subtotal = cantidad * 35;
                    producto = "Parrilla";
                }
                else
                {
                    subtotal = cantidad * 6;
                    producto = "Bebida";
                }

                // Calcular total
                total += subtotal;

                // Mostrar resultados parciales
                Console.WriteLine("\n--------------------------");
                Console.WriteLine($"Producto: {producto}");
                Console.WriteLine($"Subtotal: S/{subtotal}");
                Console.WriteLine($"Total acumulado: S/{total}");
                Console.WriteLine("--------------------------\n");
            }
            else
            {
                Console.WriteLine("Producto no disponible.");
            }

            // Preguntar si decide continuar de forma segura
            Console.Write("Desea agregar otro producto? (SI/NO): ");
            string? entradaContinuar = Console.ReadLine();
            continuar = (entradaContinuar ?? "").ToUpper().Trim();
        }

        // Validar compra final
        if (total > 0)
        {
            Console.WriteLine("\n--------------------------");
            Console.WriteLine($"Total final: S/{total}");

            Console.Write("Ingrese monto de pago: ");
            string? entradaPago = Console.ReadLine();
            
            if (double.TryParse(entradaPago, out double pago))
            {
                // Validar pago
                if (pago >= total)
                {
                    double vuelto = pago - total;

                    Console.WriteLine("Pago realizado correctamente");
                    Console.WriteLine($"Vuelto: S/{vuelto}");
                    Console.WriteLine("Pedido registrado");
                    Console.WriteLine("--------------------------\n");
                }
                else
                {
                    Console.WriteLine("Pago insuficiente. No se pudo registrar el pedido.");
                    Console.WriteLine("--------------------------\n");
                }
            }
            else
            {
                Console.WriteLine("Monto de pago invalido.");
                Console.WriteLine("--------------------------\n");
            }
        }
        else
        {
            Console.WriteLine("\nNo se realizo ningun pedido.");
        }

        Console.WriteLine("GRACIAS POR SU COMPRA VUELVA PRONTO");
        Console.WriteLine("_________________________________");
    }
}
