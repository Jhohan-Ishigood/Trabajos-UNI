import streamlit as st
from datetime import datetime
import os
import streamlit.components.v1 as components

# =========================================================
# CONFIGURACIÓN E INICIALIZACIÓN DE VARIABLES DE SESIÓN
# =========================================================
st.set_page_config(page_title="El Gran Buffalo", page_icon="🍔", layout="centered")

# Escaneo inteligente para inyectar el archivo CSS externo
css_rutas = [
    "El Gran Buffalo-Python/estilos.css",
    "El Gran Búfalo-Python/estilos.css",
    "El Gran Bufalo-Python/estilos.css",
    "El Gran Búfalo-Pitón/estilos.css",
    "estilos.css"
]
for ruta in css_rutas:
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        break

# Inicializar estados de control
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "total_acumulado" not in st.session_state:
    st.session_state.total_acumulado = 0.0
if "pedido_guardado" not in st.session_state:
    st.session_state.pedido_guardado = False
if "numero_boleta" not in st.session_state:
    st.session_state.numero_boleta = 1
if "pantalla_actual" not in st.session_state:
    st.session_state.pantalla_actual = "bienvenida"

# VARIABLES DEL PANEL DE CONTROL DE CAJA
if "caja_chica" not in st.session_state:
    st.session_state.caja_chica = 0.0
if "total_ordenes" not in st.session_state:
    st.session_state.total_ordenes = 0
if "productos_vendidos" not in st.session_state:
    st.session_state.productos_vendidos = {
        "Hamburguesa": 0, "Carne a la parrilla": 0, "Bebida": 0, "Combo Buffalo": 0
    }
if "ventas_por_metodo" not in st.session_state:
    st.session_state.ventas_por_metodo = {"Efectivo": 0.0, "Yape": 0.0, "Tarjeta": 0.0}

MENU = {
    "Hamburguesa": {"precio": 18, "icono": "🍔"},
    "Carne a la parrilla": {"precio": 35, "icono": "🥩"},
    "Bebida": {"precio": 6, "icono": "🥤"},
    "Combo Buffalo": {"precio": 25, "icono": "🎁"}
}

# =========================================================
# BARRA LATERAL (SIDEBAR): LOGIN GRUPO 5
# =========================================================
st.sidebar.markdown("### 🔒 ACCESO ADMINISTRATIVO")
usuario_input = st.sidebar.text_input("Nombre de Usuario:", key="user_login").strip()
clave_input = st.sidebar.text_input("Contraseña:", type="password", key="pass_login").strip()

es_admin = (usuario_input == "Grupo 5" and clave_input == "jhohan-2026")

if es_admin:
    st.sidebar.success("✔ Modo Administrador Activo")
elif usuario_input or clave_input:
    st.sidebar.error("❌ Credenciales incorrectas")

# =========================================================
# FLUJO DE PANTALLAS
# =========================================================
fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

if es_admin:
    # NUEVO DISEÑO: Encabezado estilizado tipo Dashboard Corporativo
    st.markdown("<h1 class='titulo-principal'>📊 PANEL DE AUDITORÍA Y CAJA CHICA</h1>", unsafe_allow_html=True)
    st.info(f"📋 **Reporte Gerencial del Grupo 5** — Generado en tiempo real: {fecha_actual}")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPIs Financieros Principales encajonados de forma limpia
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.markdown(
            f"""
            <div style='background-color: #1c1c1c; padding: 20px; border-radius: 8px; border-left: 5px solid #27ae60; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);'>
                <p style='margin:0; font-size:14px; color:#aaa; font-weight:bold;'>💰 RECAUDACIÓN TOTAL</p>
                <h2 style='margin:5px 0 0 0; color:#fff; font-size:32px;'>S/{st.session_state.caja_chica:.2f}</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col_kpi2:
        st.markdown(
            f"""
            <div style='background-color: #1c1c1c; padding: 20px; border-radius: 8px; border-left: 5px solid #f39c12; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);'>
                <p style='margin:0; font-size:14px; color:#aaa; font-weight:bold;'>📦 ÓRDENES PROCESADAS</p>
                <h2 style='margin:5px 0 0 0; color:#fff; font-size:32px;'>{st.session_state.total_ordenes} Pedidos</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 ANALÍTICA: UNIDADES VENDIDAS")
    # Gráfico de barras interactivo de productos
    st.bar_chart(st.session_state.productos_vendidos)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💳 AUDITORÍA: FLUJO POR MÉTODO DE PAGO")
    
    # Subpaneles detallados con iconos para control de arqueo de caja
    col_ef, col_yp, col_tj = st.columns(3)
    with col_ef:
        st.markdown(
            f"""
            <div style='background-color: #1a1a1a; padding: 15px; border-radius: 6px; border: 1px solid #333; text-align:center;'>
                <span style='font-size:24px;'>💵</span>
                <p style='margin:5px 0 0 0; font-size:13px; color:#888;'>EFECTIVO</p>
                <h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{st.session_state.ventas_por_metodo['Efectivo']:.2f}</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col_yp:
        st.markdown(
            f"""
            <div style='background-color: #1a1a1a; padding: 15px; border-radius: 6px; border: 1px solid #333; text-align:center;'>
                <span style='font-size:24px;'>📱</span>
                <p style='margin:5px 0 0 0; font-size:13px; color:#888;'>YAPE</p>
                <h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{st.session_state.ventas_por_metodo['Yape']:.2f}</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col_tj:
        st.markdown(
            f"""
            <div style='background-color: #1a1a1a; padding: 15px; border-radius: 6px; border: 1px solid #333; text-align:center;'>
                <span style='font-size:24px;'>💳</span>
                <p style='margin:5px 0 0 0; font-size:13px; color:#888;'>TARJETA</p>
                <h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{st.session_state.ventas_por_metodo['Tarjeta']:.2f}</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
    st.markdown("<br><hr><br>", unsafe_allow_html=True)

else:
    if st.session_state.pantalla_actual == "bienvenida":
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px;'>¿Desea registrar un nuevo pedido de nuestra deliciosa parrilla?</p>", unsafe_allow_html=True)
        
        if st.button("🛒 EMPEZAR MI PEDIDO", use_container_width=True):
            st.session_state.pantalla_actual = "catalogo"
            st.rerun()
            
    elif st.session_state.pantalla_actual == "catalogo" and not st.session_state.pedido_guardado:
        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        st.text(f"Fecha y hora: {fecha_actual}\n")
        
        st.subheader("🍽️ SELECCIÓN DE PRODUCTOS (EL MENÚ DE HOY)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🍔 PLATOS PRINCIPALES")
            cant_hamburguesa = st.number_input(f"{MENU['Hamburguesa']['icono']} Hamburguesa — S/18.00", min_value=0, step=1)
            cant_carne = st.number_input(f"{MENU['Carne a la parrilla']['icono']} Carne a la parrilla — S/35.00", min_value=0, step=1)
        with col2:
            st.markdown("### 🥤 COMPLEMENTOS Y COMBOS")
            cant_bebida = st.number_input(f"{MENU['Bebida']['icono']} Bebida — S/6.00", min_value=0, step=1)
            cant_combo = st.number_input(f"{MENU['Combo Buffalo']['icono']} Combo Buffalo — S/25.00", min_value=0, step=1)

        if st.button("🛒 ENVIAR PEDIDO Y CONFIGURAR PAGO", use_container_width=True):
            cantidades = {"Hamburguesa": cant_hamburguesa, "Carne a la parrilla": cant_carne, "Bebida": cant_bebida, "Combo Buffalo": cant_combo}
            st.session_state.carrito = []
            st.session_state.total_acumulado = 0.0
            
            for prod, cant in cantidades.items():
                if cant > 0:
                    sub = cant * MENU[prod]["precio"]
                    st.session_state.carrito.append({"producto": prod, "cantidad": cant, "subtotal": sub})
                    st.session_state.total_acumulado += sub
            
            if st.session_state.total_acumulado > 0:
                st.session_state.pedido_guardado = True
                st.rerun()
            else:
                st.error("⚠️ Error: Debe seleccionar al menos 1 producto.")
    # PANTALLA 3: GESTIÓN DE PAGO Y GENERACIÓN DE COMPROBANTE
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
                st.balloons()
                st.markdown("### 🧾 COMPROBANTE EMITIDO")
                
                # ACTUALIZACIÓN DE AUDITORÍA: Alimenta el nuevo dashboard gerencial del Grupo 5 en tiempo real
                st.session_state.caja_chica += total_con_delivery
                st.session_state.total_ordenes += 1
                st.session_state.ventas_por_metodo[metodo_pago] += total_con_delivery
                for item in st.session_state.carrito:
                    st.session_state.productos_vendidos[item['producto']] += item['cantidad']
                
                correlativo_sunat = f"B001-{st.session_state.numero_boleta:06d}"
                
                tipo_entrega_txt = f"DELIVERY\nDir. Entrega: {direccion_delivery}" if tiene_delivery else "CONSUMO EN LOCAL"
                
                if metodo_pago == "Tarjeta":
                    metodo_pago_txt = f"TARJETA (APROBADA)\nTitular:      {titular_tarjeta}\nNro. Tarjeta: ************{ultimos_digitos}"
                elif metodo_pago == "Yape":
                    metodo_pago_txt = "YAPE (PAGO ELECTRÓNICO)\nVuelto:       S/ 0.00 (Monto exacto)"
                else:
                    metodo_pago_txt = f"EFECTIVO\nEfectivo Recibido: S/{pago_usuario:.2f}\nVuelto:            S/{vuelto:.2f}"
                
                detalle_productos_txt = ""
                for item in st.session_state.carrito:
                    detalle_productos_txt += f"{item['cantidad']}x {item['producto']:<18} S/{item['subtotal']}.00\n"
                if tiene_delivery:
                    detalle_productos_txt += f"1x Costo de Envío        S/6.00\n"
                
                # LEER LA PLANTILLA HTML EXTERNA: Inyección limpia en la vista modular
                html_rutas = [
                    "El Gran Buffalo-Python/boleta_plantilla.html",
                    "El Gran Búfalo-Python/boleta_plantilla.html",
                    "El Gran Bufalo-Python/boleta_plantilla.html",
                    "El Gran Búfalo-Pitón/boleta_plantilla.html",
                    "boleta_plantilla.html"
                ]
                
                plantilla_contenido = ""
                for ruta in html_rutas:
                    if os.path.exists(ruta):
                        with open(ruta, "r", encoding="utf-8") as archivo_html:
                            plantilla_contenido = archivo_html.read()
                        break
                
                if plantilla_contenido:
                    html_final = plantilla_contenido
                    html_final = html_final.replace("{{ SERIE_BOLETA }}", correlativo_sunat)
                    html_final = html_final.replace("{{ FECHA_HORA }}", fecha_actual)
                    html_final = html_final.replace("{{ TIPO_ENTREGA }}", tipo_entrega_txt)
                    html_final = html_final.replace("{{ METODO_PAGO }}", metodo_pago_txt)
                    html_final = html_final.replace("{{ DETALLE_PRODUCTOS }}", detalle_productos_txt.strip())
                    html_final = html_final.replace("{{ TOTAL_FINAL }}", f"{total_con_delivery:.2f}")
                    
                    components.html(html_final, height=650)
                else:
                    st.error("⚠️ Error: No se pudo encontrar 'boleta_plantilla.html'.")
                
        if st.session_state.pedido_guardado:
            if st.button("🔄 Crear una nueva orden", use_container_width=True):
                st.session_state.numero_boleta += 1
                st.session_state.carrito = []
                st.session_state.total_acumulado = 0.0
                st.session_state.pedido_guardado = False
                st.session_state.pantalla_actual = "bienvenida"
                st.rerun()