import streamlit as st
from datetime import datetime
from PIL import Image
import os

# =========================================================
# CONFIGURACIÓN E INICIALIZACIÓN DE VARIABLES DE SESIÓN
# =========================================================
st.set_page_config(page_title="El Gran Buffalo", page_icon="🍔", layout="centered")

# Inicializamos el carrito de compras en la sesión si no existe
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "total_acumulado" not in st.session_state:
    st.session_state.total_acumulado = 0.0
if "pedido_guardado" not in st.session_state:
    st.session_state.pedido_guardado = False

# Precios del menú
MENU = {
    "Hamburguesa": 18,
    "Carne a la parrilla": 35,
    "Bebida": 6,
    "Combo Buffalo": 25
}

# =========================================================
# ENCABEZADO VISUAL DEL SISTEMA (Consola simulada)
# =========================================================
st.text("____________________________________________")
st.text("SISTEMA DE PEDIDOS GRAN BUFFALO")
st.text("____________________________________________")
fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
st.text(f"Fecha y hora: {fecha_actual}")

# =========================================================
# BLOQUE 1: AGREGAR PRODUCTOS AL PEDIDO
# =========================================================
if not st.session_state.pedido_guardado:
    st.subheader("🛒 AGREGAR PRODUCTOS AL PEDIDO")
    
    col1, col2 = st.columns(2)
    with col1:
        producto_sel = st.selectbox(
            "Seleccione un producto:",
            ["Hamburguesa", "Carne a la parrilla", "Bebida", "Combo Buffalo"]
        )
    with col2:
        cantidad_sel = st.number_input("Ingrese cantidad:", min_value=1, step=1, value=1)
    
    if st.button("Agregar Producto"):
        precio_unitario = MENU[producto_sel]
        subtotal_item = cantidad_sel * precio_unitario
        
        # Guardamos en la estructura del carrito
        st.session_state.carrito.append({
            "producto": producto_sel,
            "cantidad": cantidad_sel,
            "subtotal": subtotal_item
        })
        st.session_state.total_acumulado += subtotal_item
        st.toast(f"✔ {producto_sel} agregado correctamente.", icon="🍕")

    # Mostrar la tabla actual de elementos agregados
    if st.session_state.carrito:
        st.markdown("### Resumen Actual de la Orden:")
        for idx, item in enumerate(st.session_state.carrito):
            st.text(f"• {item['producto']} x{item['cantidad']} - Subtotal: S/{item['subtotal']}.00")
        st.info(f"**Total acumulado actual: S/{st.session_state.total_acumulado:.2f}**")
        
        if st.button("Terminar de agregar productos y continuar"):
            st.session_state.pedido_guardado = True
            st.rerun()

# =========================================================
# BLOQUE 2: PROCESAMIENTO DE DELIVERY Y PAGO
# =========================================================
else:
    st.subheader("📦 GESTIÓN DE ENTREGA Y PAGO")
    
    # 2.1 Lógica de Delivery
    opcion_delivery = st.radio("¿Desea delivery? (+ S/6.00)", ["NO", "SI"])
    direccion_delivery = ""
    costo_delivery = 0.0
    tiene_delivery = False
    
    if opcion_delivery == "SI":
        tiene_delivery = True
        costo_delivery = 6.0
        direccion_delivery = st.text_input("Ingrese su dirección de entrega (Ubicación):").strip()
        if not direccion_delivery:
            st.warning("⚠️ Error: La dirección no puede estar vacía si solicitó delivery.")
            
    total_con_delivery = st.session_state.total_acumulado + costo_delivery
    st.metric(label="Monto Total a Procesar", value=f"S/{total_con_delivery:.2f}")

    # 2.2 Método de Pago
    metodo_pago = st.selectbox("Seleccione método de pago:", ["Efectivo", "Yape", "Tarjeta"])
    
    pago_usuario = total_con_delivery
    vuelto = 0.0
    titular_tarjeta = ""
    ultimos_digitos = ""
    formulario_valido = True

    if metodo_pago == "Yape":
        st.info(f"--- PROCESANDO PAGO CON YAPE ---\nMonto total a yapear: S/{total_con_delivery:.2f}")
        st.caption("[!] Abriendo tu ventana de Yape con titular: Jhohan Antoni...")
        
        # Lógica para mostrar el QR en Streamlit de forma nativa en lugar de .show() externo
        if os.path.exists("mi_qr_yape.png"):
            st.image("mi_qr_yape.png", caption="Código QR de Yape oficial", width=250)
        else:
            st.warning("[Aviso] No se encontró el archivo 'mi_qr_yape.png' en la carpeta. Se simulará la operación.")

    elif metodo_pago == "Tarjeta":
        st.info("--- PROCESANDO TRANSMISIÓN POS ---")
        titular_tarjeta = st.text_input("Ingrese nombre del titular de la tarjeta:").strip().upper()
        ultimos_digitos = st.text_input("Ingrese los últimos 4 dígitos de la tarjeta:", max_chars=4)
        
        if not titular_tarjeta or len(ultimos_digitos) != 4 or not ultimos_digitos.isdigit():
            st.error("Error: Complete los datos obligatorios de la tarjeta de manera válida (4 dígitos).")
            formulario_valido = False

    else: # Efectivo
        st.warning("⚠️ ¡ALERTA DE CAJA: SOLO SE ACEPTA MONEDA NACIONAL!\nEste establecimiento NO recibe dólares ni euros. Asegúrese de recibir el monto en Soles (S/).")
        pago_usuario = st.number_input("Ingrese monto de pago: S/", min_value=0.0, value=total_con_delivery, step=1.0)
        
        if pago_usuario < total_con_delivery:
            st.error("Pago insuficiente")
            formulario_valido = False
        else:
            vuelto = pago_usuario - total_con_delivery

    # Botón Finalizador que ejecuta la boleta SUNAT exacta
    if formulario_valido and (opcion_delivery == "NO" or direccion_delivery != ""):
        if st.button("💾 EMITIR BOLETA DE VENTA"):
            st.success("PAGO REALIZADO CORRECTAMENTE - Pedido registrado exitosamente")
            
            # Imprimiendo Boleta estructurada exactamente como el diseño SUNAT de tu script
            st.markdown("### 🧾 IMPRESIÓN DE LA BOLETA FINAL")
            
            boleta_texto = f"""
==================================================
            EL GRAN BUFFALO E.I.R.L.
            RUC: 20608247140
            ║█│█║▌│█║▌│║▌║▌█║│▌║█│
   Av. La Revolucion Nro. 1821 P.J. Almirante Grau
             El Porvenir - Trujillo
==================================================
                BOLETA DE VENTA
--------------------------------------------------
Fecha y hora: {fecha_actual}
"""
            if tiene_delivery:
                boleta_texto += f"Tipo Entrega: DELIVERY\nDir. Entrega: {direccion_delivery}\n"
            else:
                boleta_texto += "Tipo Entrega: CONSUMO EN LOCAL\n"
                
            if metodo_pago == "Tarjeta":
                boleta_texto += f"Forma de Pago: TARJETA (APROBADA)\nTitular:      {titular_tarjeta}\nNro. Tarjeta: ************{ultimos_digitos}\n"
            elif metodo_pago == "Yape":
                boleta_texto += f"Forma de Pago: YAPE (PAGO ELECTRÓNICO)\nVuelto:       S/ 0.00 (Monto exacto)\n"
            else:
                boleta_texto += f"Forma de Pago: EFECTIVO\nEfectivo Recibido: S/{pago_usuario:.2f}\nVuelto:            S/{vuelto:.2f}\n"

            boleta_texto += "--------------------------------------------------\n"
            
            # Detalle de artículos dentro de la boleta
            for item in st.session_state.carrito:
                boleta_texto += f"{item['cantidad']}x {item['producto']:<20} S/{item['subtotal']}.00\n"
            
            if tiene_delivery:
                boleta_texto += f"1x Costo de Envío        S/6.00\n"
                
            boleta_texto += f"--------------------------------------------------\nTOTAL A PAGAR:            S/{total_con_delivery:.2f}\n=================================================="
            
            # Se renderiza con formato monoespaciado tipo ticketera de boleta real
            st.code(boleta_texto, language="text")
            
            # Botón opcional por si quieren reiniciar el punto de venta
            if st.button("Crear una nueva orden"):
                st.session_state.clear()
                st.rerun()
