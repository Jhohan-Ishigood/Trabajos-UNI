import streamlit as st
from datetime import datetime
import os
import streamlit.components.v1 as components

# =========================================================
# CONFIGURACIÓN E INICIALIZACIÓN DE VARIABLES DE SESIÓN
# =========================================================
st.set_page_config(page_title="El Gran Buffalo", page_icon="🍔", layout="centered")

# SEPARACIÓN DE ARQUITECTURA: Cargar el archivo CSS externo para los bordes verdes
try:
    with open("El Gran Buffalo-Python/estilos.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    # Por si ejecutas en una ruta distinta
    if os.path.exists("estilos.css"):
        with open("estilos.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "total_acumulado" not in st.session_state:
    st.session_state.total_acumulado = 0.0
if "pedido_guardado" not in st.session_state:
    st.session_state.pedido_guardado = False

MENU = {
    "Hamburguesa": {"precio": 18, "icono": "🍔"},
    "Carne a la parrilla": {"precio": 35, "icono": "🥩"},
    "Bebida": {"precio": 6, "icono": "🥤"},
    "Combo Buffalo": {"precio": 25, "icono": "🎁"}
}

st.text("____________________________________________")
st.text("SISTEMA DE PEDIDOS GRAN BUFFALO")
st.text("____________________________________________")
fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
st.text(f"Fecha y hora: {fecha_actual}")

# =========================================================
# BLOQUE 1: SELECCIÓN DE PRODUCTOS EN PARALELO
# =========================================================
if not st.session_state.pedido_guardado:
    st.subheader("🍽️ SELECCIÓN DE PRODUCTOS (EL MENÚ DE HOY)")
    st.info("Ingrese las cantidades de los productos que desea llevar:")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🍔 PLATOS PRINCIPALES")
        cant_hamburguesa = st.number_input(f"{MENU['Hamburguesa']['icono']} Hamburguesa — S/18.00", min_value=0, step=1, value=0)
        cant_carne = st.number_input(f"{MENU['Carne a la parrilla']['icono']} Carne a la parrilla — S/35.00", min_value=0, step=1, value=0)
        
    with col2:
        st.markdown("### 🥤 COMPLEMENTOS Y COMBOS")
        cant_bebida = st.number_input(f"{MENU['Bebida']['icono']} Bebida — S/6.00", min_value=0, step=1, value=0)
        cant_combo = st.number_input(f"{MENU['Combo Buffalo']['icono']} Combo Buffalo — S/25.00", min_value=0, step=1, value=0)

    st.markdown("---")
    
    if st.button("🛒 ENVIAR PEDIDO Y CONFIGURAR PAGO", use_container_width=True):
        cantidades = {
            "Hamburguesa": cant_hamburguesa,
            "Carne a la parrilla": cant_carne,
            "Bebida": cant_bebida,
            "Combo Buffalo": cant_combo
        }
        
        st.session_state.carrito = []
        st.session_state.total_acumulado = 0.0
        
        for producto, cantidad in cantidades.items():
            if cantidad > 0:
                subtotal_item = cantidad * MENU[producto]["precio"]
                st.session_state.carrito.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "subtotal": subtotal_item
                })
                st.session_state.total_acumulado += subtotal_item
        
        if st.session_state.total_acumulado > 0:
            st.session_state.pedido_guardado = True
            st.rerun()
        else:
            st.error("⚠️ Error: Debe seleccionar al menos 1 producto para continuar.")

# =========================================================
# BLOQUE 2: PROCESAMIENTO DE DELIVERY Y PAGO
# =========================================================
else:
    st.subheader("📦 GESTIÓN DE ENTREGA Y PAGO")
    
    st.markdown("**Resumen de artículos solicitados:**")
    for item in st.session_state.carrito:
        st.text(f"• {MENU[item['producto']]['icono']} {item['producto']} x{item['cantidad']} - Subtotal: S/{item['subtotal']}.00")
    
    st.markdown("---")
    
    opcion_delivery = st.radio("¿Desea delivery? (+ S/6.00)", ["NO", "SI"])
    direccion_delivery = ""
    costo_delivery = 0.0
    tiene_delivery = False
    
    if opcion_delivery == "SI":
        tiene_delivery = True
        costo_delivery = 6.0
        direccion_delivery = st.text_input("Ingrese su dirección de entrega (Ubicación):", placeholder="Ej. Av. Larco 123...").strip()
            
    total_con_delivery = st.session_state.total_acumulado + costo_delivery
    st.metric(label="Monto Total a Procesar", value=f"S/{total_con_delivery:.2f}")

    metodo_pago = st.selectbox("Seleccione método de pago:", ["Efectivo", "Yape", "Tarjeta"])
    
    pago_usuario = total_con_delivery
    vuelto = 0.0
    titular_tarjeta = ""
    ultimos_digitos = ""
    formulario_valido = True

    if metodo_pago == "Yape":
        st.info(f"--- PROCESANDO PAGO CON YAPE ---\nMonto total a yapear: S/{total_con_delivery:.2f}")
        st.caption("[!] Abriendo tu ventana de Yape con titular: Jhohan Antoni...")
        if os.path.exists("mi_qr_yape.png"):
            st.image("mi_qr_yape.png", caption="Código QR de Yape oficial", width=250)
        else:
            st.warning("[Aviso] No se encontró el archivo 'mi_qr_yape.png' en la carpeta.")

    elif metodo_pago == "Tarjeta":
        st.info("--- PROCESANDO TRANSMISIÓN POS ---")
        titular_tarjeta = st.text_input("Ingrese nombre del titular de la tarjeta:").strip().upper()
        ultimos_digitos = st.text_input("Ingrese los últimos 4 dígitos de la tarjeta:", max_chars=4)
        if not titular_tarjeta or len(ultimos_digitos) != 4 or not ultimos_digitos.isdigit():
            st.error("Error: Complete los datos obligatorios de la tarjeta de manera válida (4 dígitos).")
            formulario_valido = False

    else:
        st.warning("⚠️ ¡ALERTA DE CAJA: SOLO SE ACEPTA MONEDA NACIONAL!\nEste establecimiento NO recibe dólares ni euros.")
        pago_usuario = st.number_input("Ingrese monto de pago: S/", min_value=0.0, value=total_con_delivery, step=1.0)
        if pago_usuario < total_con_delivery:
            st.error("Pago insuficiente")
            formulario_valido = False
        else:
            vuelto = pago_usuario - total_con_delivery

    if st.button("💾 EMITIR BOLETA DE VENTA", use_container_width=True):
        if tiene_delivery and not direccion_delivery:
            st.error("⚠️ Error: Llenar este campo obligatorio (Ingrese su dirección de entrega).")
        elif not formulario_valido:
            st.error("⚠️ Error: Complete correctamente los datos del formulario de pago antes de continuar.")
        else:
            st.success("PAGO REALIZADO CORRECTAMENTE - Pedido registrado exitosamente")
            st.markdown("### 🧾 COMPROBANTE EMITIDO")
            
            boleta_texto = f"==============================================<br>"
            boleta_texto += f"            EL GRAN BUFFALO E.I.R.L.<br>"
            boleta_texto += f"            RUC: 20608247140<br>"
            boleta_texto += f"            ║█│█║▌│█║▌│║▌║▌█║│▌║█│<br>"
            boleta_texto += f"   Av. La Revolucion Nro. 1821 P.J. Almirante Grau<br>"
            boleta_texto += f"             El Porvenir - Trujillo<br>"
            boleta_texto += f"==============================================<br>"
            boleta_texto += f"                BOLETA DE VENTA<br>"
            boleta_texto += f"----------------------------------------------<br>"
            boleta_texto += f"Fecha y hora: {fecha_actual}<br>"
            
            if tiene_delivery:
                boleta_texto += f"Tipo Entrega: DELIVERY<br>Dir. Entrega: {direccion_delivery}<br>"
            else:
                boleta_texto += f"Tipo Entrega: CONSUMO EN LOCAL<br>"
                
            if metodo_pago == "Tarjeta":
                boleta_texto += f"Forma de Pago: TARJETA (APROBADA)<br>Titular:      {titular_tarjeta}<br>Nro. Tarjeta: ************{ultimos_digitos}<br>"
            elif metodo_pago == "Yape":
                boleta_texto += f"Forma de Pago: YAPE (PAGO ELECTRÓNICO)<br>Vuelto:       S/ 0.00 (Monto exacto)<br>"
            else:
                boleta_texto += f"Forma de Pago: EFECTIVO<br>Efectivo Recibido: S/{pago_usuario:.2f}<br>Vuelto:            S/{vuelto:.2f}<br>"

            boleta_texto += f"----------------------------------------------<br>"
            for item in st.session_state.carrito:
                boleta_texto += f"{item['cantidad']}x {item['producto']:<18} S/{item['subtotal']}.00<br>"
            if tiene_delivery:
                boleta_texto += f"1x Costo de Envío        S/6.00<br>"
            boleta_texto += f"----------------------------------------------<br>"
            boleta_texto += f"TOTAL A PAGAR:            S/{total_con_delivery:.2f}<br>"
            boleta_texto += f"=============================================="

            # SEPARACIÓN DE ARQUITECTURA: Cargar la plantilla HTML externa y reemplazar datos
            plantilla_ruta = "El Gran Buffalo-Python/boleta_plantilla.html"
            if not os.path.exists(plantilla_ruta) and os.path.exists("boleta_plantilla.html"):
                plantilla_ruta = "boleta_plantilla.html"
                
            with open(plantilla_ruta, "r", encoding="utf-8") as archivo_html:
                plantilla_contenido = archivo_html.read()
            
            html_final = plantilla_contenido.replace("TEXTO_DE_LA_BOLETA", boleta_texto)
            components.html(html_final, height=650)
            
    if st.session_state.pedido_guardado:
        if st.button("🔄 Crear una nueva orden", use_container_width=True):
            st.session_state.clear()
            st.rerun()