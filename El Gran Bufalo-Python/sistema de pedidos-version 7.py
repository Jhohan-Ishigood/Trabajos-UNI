import streamlit as st
from datetime import datetime
import os
import streamlit.components.v1 as components
import pandas as pd  
import altair as alt  
import json  # Librería nativa para guardar los precios fijos en un archivo de texto

# =========================================================
# RUTAS DE CONTROL PARA ARQUITECTURA DESACOPLADA Y ARCHIVOS
# =========================================================
BASE_DIR = ""
if os.path.exists("El Gran Buffalo-Python"):
    BASE_DIR = "El Gran Buffalo-Python/"
elif os.path.exists("El Gran Búfalo-Python"):
    BASE_DIR = "El Gran Búfalo-Python/"
elif os.path.exists("El Gran Bufalo-Python"):
    BASE_DIR = "El Gran Bufalo-Python/"
elif os.path.exists("El Gran Búfalo-Pitón"):
    BASE_DIR = "El Gran Búfalo-Pitón/"

RUTA_CSS = os.path.join(BASE_DIR, "estilos.css")
RUTA_HTML = os.path.join(BASE_DIR, "boleta_plantilla.html")
RUTA_JSON_MENU = os.path.join(BASE_DIR, "menu_config.json")  # Archivo donde se guardarán los precios para siempre

# Funciones de persistencia de datos (Lectura y Escritura del menú)
def guardar_menu_en_archivo(menu_data):
    with open(RUTA_JSON_MENU, "w", encoding="utf-8") as archivo:
        json.dump(menu_data, archivo, indent=4, ensure_ascii=False)

def cargar_menu_desde_archivo():
    # Menú original por defecto por si el archivo aún no existe
    menu_defecto = {
        "Hamburguesa": {"precio": 18.0, "icono": "🍔", "disponible": True},
        "Carne a la parrilla": {"precio": 35.0, "icono": "🥩", "disponible": True},
        "Bebida": {"precio": 6.0, "icono": "🥤", "disponible": True},
        "Combo Buffalo": {"precio": 25.0, "icono": "🎁", "disponible": True}
    }
    if os.path.exists(RUTA_JSON_MENU):
        try:
            with open(RUTA_JSON_MENU, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except:
            return menu_defecto
    return menu_defecto

# =========================================================
# CONFIGURACIÓN E INICIALIZACIÓN DE VARIABLES DE SESIÓN
# =========================================================
st.set_page_config(page_title="El Gran Buffalo", page_icon="🍔", layout="centered")

# Inyección automatizada del archivo CSS externo
if os.path.exists(RUTA_CSS):
    with open(RUTA_CSS, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# NUEVA MEJORA: El menú se carga directo desde el archivo JSON fijo para persistencia eterna
if "menu_dinamico" not in st.session_state:
    st.session_state.menu_dinamico = cargar_menu_desde_archivo()

# Inicializar estados de control del carrito y del flujo
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
if "historial_ordenes" not in st.session_state:
    st.session_state.historial_ordenes = []

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
    st.markdown("<h1 class='titulo-principal'>📊 PANEL DE AUDITORÍA Y CAJA CHICA</h1>", unsafe_allow_html=True)
    st.info(f"📋 **Reporte Gerencial del Grupo 5** — Generado en tiempo real: {fecha_actual}")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERMANENCIA FIJA: Formulario para editar precios y guardarlos para siempre
    st.markdown("### 🛠️ GESTIÓN DE CARTA Y PRECIOS (PARA SIEMPRE)")
    st.caption("Modifique los precios o desactive productos. Se guardarán en un archivo JSON local.")
    
    edit_col1, edit_col2 = st.columns(2)
    with edit_col1:
        st.markdown("**🍔 Platos Principales**")
        hamb_p = st.number_input("Precio Hamburguesa (S/):", min_value=1.0, value=float(st.session_state.menu_dinamico["Hamburguesa"]["precio"]), step=0.5)
        hamb_d = st.checkbox("🍔 Hamburguesa Disponible", value=st.session_state.menu_dinamico["Hamburguesa"]["disponible"])
        st.markdown("---")
        carne_p = st.number_input("Precio Carne (S/):", min_value=1.0, value=float(st.session_state.menu_dinamico["Carne a la parrilla"]["precio"]), step=0.5)
        carne_d = st.checkbox("🥩 Carne Disponible", value=st.session_state.menu_dinamico["Carne a la parrilla"]["disponible"])
    with edit_col2:
        st.markdown("**🥤 Complementos y Combos**")
        beb_p = st.number_input("Precio Bebida (S/):", min_value=1.0, value=float(st.session_state.menu_dinamico["Bebida"]["precio"]), step=0.5)
        beb_d = st.checkbox("🥤 Bebida Disponible", value=st.session_state.menu_dinamico["Bebida"]["disponible"])
        st.markdown("---")
        combo_p = st.number_input("Precio Combo (S/):", min_value=1.0, value=float(st.session_state.menu_dinamico["Combo Buffalo"]["precio"]), step=0.5)
        combo_d = st.checkbox("🎁 Combo Buffalo Disponible", value=st.session_state.menu_dinamico["Combo Buffalo"]["disponible"])
        
    # Botón exclusivo para confirmar y sobreescribir el archivo de configuración
    if st.button("💾 GUARDAR CAMBIOS DE LA CARTA", use_container_width=True):
        st.session_state.menu_dinamico["Hamburguesa"] = {"precio": hamb_p, "icono": "🍔", "disponible": hamb_d}
        st.session_state.menu_dinamico["Carne a la parrilla"] = {"precio": carne_p, "icono": "🥩", "disponible": carne_d}
        st.session_state.menu_dinamico["Bebida"] = {"precio": beb_p, "icono": "🥤", "disponible": beb_d}
        st.session_state.menu_dinamico["Combo Buffalo"] = {"precio": combo_p, "icono": "🎁", "disponible": combo_d}
        guardar_menu_en_archivo(st.session_state.menu_dinamico)
        st.success("✔ ¡Carta guardada en archivo con éxito! Los cambios se mantendrán fijos.")
        st.rerun()
        
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    # KPIs Financieros Principales encajonados
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
    st.markdown("### 📈 ANALÍTICA: UNIDADES VENDIDAS DE HOY")
    
    # Convertimos los datos guardados en una tabla estructurada de Pandas
    df_grafico = pd.DataFrame({
        'Producto': list(st.session_state.productos_vendidos.keys()),
        'Cantidad': list(st.session_state.productos_vendidos.values())
    })
    
    # Diseñamos las barras con bordes redondeados y degradado de color fuego-parrilla
    barras = alt.Chart(df_grafico).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6
    ).encode(
        x=alt.X('Producto:N', title='Productos del Menú', sort=None, axis=alt.Axis(labelAngle=0, labelColor='#ffffff', titleColor='#f39c12')),
        y=alt.Y('Cantidad:Q', title='Unidades Vendidas', axis=alt.Axis(grid=True, gridColor='#2c2c2c', labelColor='#ffffff', titleColor='#f39c12')),
        color=alt.Color('Cantidad:Q', scale=alt.Scale(scheme='orangered'), legend=None)
    )
    
    # Añadimos las etiquetas numéricas flotantes encima de cada barra
    texto_etiquetas = barras.mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        color='#ffffff',
        fontSize=13,
        fontWeight='bold'
    ).encode(
        text='Cantidad:Q'
    )
    
    # Fusionamos barras y textos con un fondo transparente corporativo
    grafico_final = (barras + texto_etiquetas).properties(
        width=600, height=320
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        domainWidth=1, domainColor='#444444'
    )
    
    st.altair_chart(grafico_final, use_container_width=True)
    
    # Registro de Auditoría en Tabla Formateada con Pandas
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🕒 BITÁCORA: HISTORIAL CRONOLÓGICO DE COMPRAS")
    if st.session_state.historial_ordenes:
        df_historial = pd.DataFrame(st.session_state.historial_ordenes)
        df_historial.columns = ["🕒 FECHA Y HORA", "🧾 NRO. BOLETA", "📦 DETALLE ARTÍCULOS", "🛵 ENTREGA", "💳 MÉTODO PAGO", "💰 TOTAL"]
        st.dataframe(df_historial, use_container_width=True, hide_index=True)
    else:
        st.caption("Aún no se han registrado transacciones en esta sesión.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💳 AUDITORÍA: FLUJO POR MÉTODO DE PAGO")
    
    col_ef, col_yp, col_tj = st.columns(3)
    with col_ef:
        st.markdown(f"<div style='background-color:#1a1a1a; padding:15px; border-radius:6px; border:1px solid #333; text-align:center;'><span style='font-size:24px;'>💵</span><p style='margin:5px 0 0 0; font-size:13px; color:#888;'>EFECTIVO</p><h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{st.session_state.ventas_por_metodo['Efectivo']:.2f}</h4></div>", unsafe_allow_html=True)
    with col_yp:
        st.markdown(f"<div style='background-color:#1a1a1a; padding:15px; border-radius:6px; border:1px solid #333; text-align:center;'><span style='font-size:24px;'>📱</span><p style='margin:5px 0 0 0; font-size:13px; color:#888;'>YAPE</p><h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{st.session_state.ventas_por_metodo['Yape']:.2f}</h4></div>", unsafe_allow_html=True)
    with col_tj:
        st.markdown(f"<div style='background-color:#1a1a1a; padding:15px; border-radius:6px; border:1px solid #333; text-align:center;'><span style='font-size:24px;'>💳</span><p style='margin:5px 0 0 0; font-size:13px; color:#888;'>TARJETA</p><h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{st.session_state.ventas_por_metodo['Tarjeta']:.2f}</h4></div>", unsafe_allow_html=True)
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
else:
    # PANTALLA 1: BIENVENIDA LIMPIA CON TÍTULO GIGANTE PREMIUM
    if st.session_state.pantalla_actual == "bienvenida":
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px;'>¿Desea registrar un nuevo pedido de nuestra deliciosa parrilla?</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🛒 EMPEZAR MI PEDIDO", use_container_width=True):
            st.session_state.pantalla_actual = "catalogo"
            st.rerun()
            
    # PANTALLA 2: CATÁLOGO DE PRODUCTOS EN COLUMNAS DINÁMICAS
    elif st.session_state.pantalla_actual == "catalogo" and not st.session_state.pedido_guardado:
        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        st.text(f"Fecha y hora: {fecha_actual}\n")
        
        st.subheader("🍽️ SELECCIÓN DE PRODUCTOS (EL MENÚ DE HOY)")
        st.info("Ingrese las cantidades de los productos que desea llevar:")

        col1, col2 = st.columns(2)
        cantidades_ingresadas = {}
        
        with col1:
            st.markdown("### 🍔 PLATOS PRINCIPALES")
            if st.session_state.menu_dinamico["Hamburguesa"]["disponible"]:
                precio_h = st.session_state.menu_dinamico["Hamburguesa"]["precio"]
                cantidades_ingresadas["Hamburguesa"] = st.number_input(f"🍔 Hamburguesa — S/{precio_h:.2f}", min_value=0, step=1, key="input_hamb")
            else:
                st.markdown("<p style='color: #ff4b4b; font-weight: bold;'>❌ Hamburguesa (AGOTADO POR HOY)</p>", unsafe_allow_html=True)
                
            if st.session_state.menu_dinamico["Carne a la parrilla"]["disponible"]:
                precio_c = st.session_state.menu_dinamico["Carne a la parrilla"]["precio"]
                cantidades_ingresadas["Carne a la parrilla"] = st.number_input(f"🥩 Carne a la parrilla — S/{precio_c:.2f}", min_value=0, step=1, key="input_carne")
            else:
                st.markdown("<p style='color: #ff4b4b; font-weight: bold;'>❌ Carne a la parrilla (AGOTADO POR HOY)</p>", unsafe_allow_html=True)
                
        with col2:
            st.markdown("### 🥤 COMPLEMENTOS Y COMBOS")
            if st.session_state.menu_dinamico["Bebida"]["disponible"]:
                precio_b = st.session_state.menu_dinamico["Bebida"]["precio"]
                cantidades_ingresadas["Bebida"] = st.number_input(f"🥤 Bebida — S/{precio_b:.2f}", min_value=0, step=1, key="input_beb")
            else:
                st.markdown("<p style='color: #ff4b4b; font-weight: bold;'>❌ Bebida (AGOTADO POR HOY)</p>", unsafe_allow_html=True)
                
            if st.session_state.menu_dinamico["Combo Buffalo"]["disponible"]:
                precio_co = st.session_state.menu_dinamico["Combo Buffalo"]["precio"]
                cantidades_ingresadas["Combo Buffalo"] = st.number_input(f"🎁 Combo Buffalo — S/{precio_co:.2f}", min_value=0, step=1, key="input_combo")
            else:
                st.markdown("<p style='color: #ff4b4b; font-weight: bold;'>❌ Combo Buffalo (AGOTADO POR HOY)</p>", unsafe_allow_html=True)

        st.markdown("---")
        
        if st.button("🛒 ENVIAR PEDIDO Y CONFIGURAR PAGO", use_container_width=True):
            st.session_state.carrito = []
            st.session_state.total_acumulado = 0.0
            
            for prod, cant in cantidades_ingresadas.items():
                if cant > 0:
                    sub = cant * st.session_state.menu_dinamico[prod]["precio"]
                    st.session_state.carrito.append({"producto": prod, "cantidad": cant, "subtotal": sub})
                    st.session_state.total_acumulado += sub
            
            if st.session_state.total_acumulado > 0:
                st.session_state.pedido_guardado = True
                st.rerun()
            else:
                st.error("⚠️ Error: Debe seleccionar al menos 1 producto.")
    # PANTALLA 3: PROCESAMIENTO DE DELIVERY, PASARELA Y COMPROBANTE SUNAT
    else:
        st.subheader("📦 GESTIÓN DE ENTREGA Y PAGO")
        
        st.markdown("**Resumen de artículos solicitados:**")
        for item in st.session_state.carrito:
            icono_p = st.session_state.menu_dinamico[item['producto']]['icono']
            st.text(f"• {icono_p} {item['producto']} x{item['cantidad']} - Subtotal: S/{item['subtotal']}.00")
        
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
                
                correlativo_sunat = f"B001-{st.session_state.numero_boleta:06d}"
                
                detalle_productos_txt = ""
                items_resumen_lista = []
                for item in st.session_state.carrito:
                    detalle_productos_txt += f"{item['cantidad']}x {item['producto']:<18} S/{item['subtotal']}.00\n"
                    items_resumen_lista.append(f"{item['cantidad']}x {item['producto']}")
                
                if tiene_delivery:
                    detalle_productos_txt += f"1x Costo de Envío        S/6.00\n"
                    items_resumen_lista.append("1x Delivery")
                
                resumen_articulos_linea = ", ".join(items_resumen_lista)
                tipo_entrega_txt = f"DELIVERY ({direccion_delivery})" if tiene_delivery else "LOCAL"
                
                # 1. ACTUALIZACIÓN AUTOMÁTICA DEL HISTORIAL CRONOLÓGICO DE AUDITORÍA
                st.session_state.historial_ordenes.append({
                    "Fecha y Hora": fecha_actual,
                    "Nro. Boleta": correlativo_sunat,
                    "Detalle Artículos": resumen_articulos_linea,
                    "Entrega": tipo_entrega_txt,
                    "Método Pago": metodo_pago,
                    "Total": f"S/{total_con_delivery:.2f}"
                })
                
                # 2. ACTUALIZACIÓN DE LAS ESTADÍSTICAS GENERALES DE CAJA CHICA
                st.session_state.caja_chica += total_con_delivery
                st.session_state.total_ordenes += 1
                st.session_state.ventas_por_metodo[metodo_pago] += total_con_delivery
                for item in st.session_state.carrito:
                    st.session_state.productos_vendidos[item['producto']] += item['cantidad']
                
                # 3. PREPARACIÓN DEL TEXTO PARA LA RECOMPOSICIÓN DE LA BOLETA
                if metodo_pago == "Tarjeta":
                    metodo_pago_txt = f"TARJETA (APROBADA)\nTitular:      {titular_tarjeta}\nNro. Tarjeta: ************{ultimos_digitos}"
                elif metodo_pago == "Yape":
                    metodo_pago_txt = "YAPE (PAGO ELECTRÓNICO)\nVuelto:       S/ 0.00 (Monto exacto)"
                else:
                    metodo_pago_txt = f"EFECTIVO\nEfectivo Recibido: S/{pago_usuario:.2f}\nVuelto:            S/{vuelto:.2f}"
                
                # 4. LEER LA PLANTILLA MODULAR HTML EXTERNA
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
