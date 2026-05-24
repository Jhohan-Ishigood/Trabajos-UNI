using System;
using System.Collections.Generic;

class Programa
{
    static void Main()
    {
        // Variables principales
        double total = 0;
        List<string> productos = new List<string>();
        List<int> cantidades = new List<int>();
        List<double> subtotales = new List<double>();

        string continuar = "SI";

        // Fecha y hora
        DateTime fecha = DateTime.Now;

        // Encabezado
        Console.WriteLine(new string('_', 45));
        Console.WriteLine("\nSISTEMA DE PEDIDOS GRAN BUFFALO");
        Console.WriteLine(new string('_', 45));
        Console.WriteLine($"\nFecha y hora: {fecha:dd/MM/yyyy HH:mm:ss}");

        // Bucle principal
        while (continuar == "SI")
        {
            // Menu
            Console.WriteLine("\nEL MENU DE HOY:");
            Console.WriteLine("\n1. Hamburguesa   - S/18");
            Console.WriteLine("2. Carne a la parrilla - S/35");
            Console.WriteLine("3. Bebida        - S/6");
            Console.WriteLine("4. Combo Buffalo - S/25");
            Console.WriteLine(new string('_', 28));

            int opcion = 0;
            // Validar opcion
            while (true)
            {
                Console.Write("\nSeleccione una opcion: ");
                string? entradaOpcion = Console.ReadLine();

                if (int.TryParse(entradaOpcion, out opcion) && opcion >= 1 && opcion <= 4)
                {
                    break;
                }
                else
                {
                    Console.WriteLine("Error: Opcion no valida");
                }
            }

            int cantidad = 0;
            // Validar cantidad
            while (true)
            {
                Console.Write("Ingrese cantidad: ");
                string? entradaCantidad = Console.ReadLine();

                if (int.TryParse(entradaCantidad, out cantidad) && cantidad > 0)
                {
                    break;
                }
                else
                {
                    Console.WriteLine("Error: La cantidad debe ser mayor a 0");
                }
            }

            // Procesar pedido
            string producto = "";
            double precio = 0;

            if (opcion == 1)
            {
                producto = "Hamburguesa";
                precio = 18;
            }
            else if (opcion == 2)
            {
                producto = "Carne a la parrilla";
                precio = 35;
            }
            else if (opcion == 3)
            {
                producto = "Bebida";
                precio = 6;
            }
            else
            {
                producto = "Combo Buffalo";
                precio = 25;
            }

            // Calcular subtotal
            double subtotal = cantidad * precio;

            // Guardar datos
            productos.Add(producto);
            cantidades.Add(cantidad);
            subtotales.Add(subtotal);

            // Acumular total
            total += subtotal;

            // Mostrar resumen
            Console.WriteLine("\nProducto agregado correctamente");
            Console.WriteLine($"Producto: {producto}");
            Console.WriteLine($"Cantidad: {cantidad}");
            Console.WriteLine($"Subtotal: S/ {subtotal}");
            Console.WriteLine($"Total acumulado: S/ {total}");

            // Preguntar si desea continuar
            while (true)
            {
                Console.Write("\nDesea agregar otro producto? (SI/NO): ");
                string? entradaContinuar = Console.ReadLine();
                continuar = (entradaContinuar ?? "").ToUpper().Trim();

                if (continuar == "SI" || continuar == "NO")
                {
                    break;
                }
                else
                {
                    Console.WriteLine("Error: Ingrese solo SI o NO");
                }
            }
        }

        // Verificar compra
        if (total > 0)
        {
            Console.WriteLine("\n");
            string delivery = "";

            while (true)
            {
                Console.Write("Desea delivery? (SI/NO): ");
                string? entradaDelivery = Console.ReadLine();
                delivery = (entradaDelivery ?? "").ToUpper().Trim();

                if (delivery == "SI" || delivery == "NO")
                {
                    break;
                }
                else
                {
                    Console.WriteLine("Error: Ingrese solo SI o NO");
                }
            }

            if (delivery == "SI")
            {
                total += 6;
                Console.WriteLine("Costo por Delivery agregado: S/6");
            }

            // Aumento corregido
            double aumento = 0;
            if (total > 100)
            {
                aumento = 6; // Asignamos el valor del aumento
                total = total + aumento;
}

            // Boleta
            Console.WriteLine("\n" + new string('_', 40));
            Console.WriteLine("BOLETA DE FACTURACION");
            Console.WriteLine(new string('_', 40));

            for (int i = 0; i < productos.Count; i++)
            {
                Console.WriteLine($"{productos[i]} x {cantidades[i]} = S/ {subtotales[i]}");
            }

            Console.WriteLine(new string('_', 40));
            Console.WriteLine($"Aumento por Delivery: S/ {Math.Round(aumento, 2)}");
            Console.WriteLine($"TOTAL FINAL: S/ {Math.Round(total, 2)}");
            Console.WriteLine(new string('_', 40));

            // Metodo de pago
            Console.WriteLine("\nMETODO DE PAGO");
            Console.WriteLine("1. Efectivo");
            Console.WriteLine("2. Yape");
            Console.WriteLine("3. Tarjeta");

            int metodo = 0;
            while (true)
            {
                Console.Write("Seleccione metodo de pago: ");
                string? entradaMetodo = Console.ReadLine();

                if (int.TryParse(entradaMetodo, out metodo) && metodo >= 1 && metodo <= 3)
                {
                    break;
                }
                else
                {
                    Console.WriteLine("Opcion invalida");
                }
            }

            // Validar pago
            double pago = 0;
            while (true)
            {
                Console.Write("Ingrese monto de pago: S/ ");
                string? entradaPago = Console.ReadLine();

                if (double.TryParse(entradaPago, out pago))
                {
                    if (pago <= 0)
                    {
                        Console.WriteLine("El pago debe ser mayor a 0");
                    }
                    else if (pago >= total)
                    {
                        break;
                    }
                    else
                    {
                        Console.WriteLine("Pago insuficiente");
                    }
                }
                else
                {
                    Console.WriteLine("Debe ingresar un numero valido");
                }
            }

            // Calcular vuelto
            double vuelto = pago - total;

            // Confirmacion final
            Console.WriteLine("\nPAGO REALIZADO CORRECTAMENTE");

            if (metodo == 1)
            {
                Console.WriteLine("Metodo de pago: Efectivo");
            }
            else if (metodo == 2)
            {
                Console.WriteLine("Metodo de pago: Yape");
            }
            else
            {
                Console.WriteLine("Metodo de pago: Tarjeta");
            }

            Console.WriteLine($"Vuelto: S/ {Math.Round(vuelto, 2)}");
            Console.WriteLine("Pedido registrado exitosamente");
        }
        else
        {
            Console.WriteLine("\nNo se realizo ningun pedido");
        }

        // Despedida
        Console.WriteLine("\nGRACIAS POR SU COMPRA, VUELVA PRONTO!");
    }
}
