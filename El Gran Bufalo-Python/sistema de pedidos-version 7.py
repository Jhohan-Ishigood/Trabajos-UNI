import streamlit as st
from datetime import datetime, timedelta, timezone  # Reloj oficial para Perú (GMT-5)
import os
import streamlit.components.v1 as components
import pandas as pd  # Motor de analítica para el control de la bitácora
import altair as alt  # Motor gráfico premium para el Dashboard corporativo
import base64  # Motor multimedia para incrustar fotos locales en HTML y CSS

# Configuración premium inicial para que la app se adapte a celulares y la barra lateral inicie oculta por defecto
st.set_page_config(page_title="El Gran Búfalo - Sistema de Pedidos", page_icon="🥩", layout="wide", initial_sidebar_state="collapsed")

# =========================================================
# RUTAS DE CONTROL PARA ARCHIVOS FÍSICOS PERMANENTES
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
RUTA_JSON_MENU = os.path.join(BASE_DIR, "menu_config.json")
RUTA_JSON_HISTORIAL = os.path.join(BASE_DIR, "historial_config.json")  

# --- FUNCIONES DE PERSISTENCIA Y SINCRONIZACIÓN DE LA CARTA ---
def guardar_menu_en_archivo(menu_data):
    import json
    with open(RUTA_JSON_MENU, "w", encoding="utf-8") as archivo:
        json.dump(menu_data, archivo, indent=4, ensure_ascii=False)

def cargar_menu_desde_archivo():
    import json
    # Silueta vectorial en Base64 por defecto para evitar pantallas colapsadas
    FOTO_DEFECTO = "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' width='100' height='100' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='3' width='18' height='18' rx='2' ry='2'/><circle cx='8.5' cy='8.5' r='1.5'/><polyline points='21 15 16 10 5 21'/></svg>"
    
    menu_defecto = {
        "Hamburguesa": {
            "precio": 18.0, 
            "icono": "🍔", 
            "disponible": True,
            "foto": FOTO_DEFECTO
        },
        "Carne a la parrilla": {
            "precio": 35.0, 
            "icono": "🥩", 
            "disponible": True,
            "foto": FOTO_DEFECTO
        },
        "Jugo": {
            "precio": 6.0, 
            "icono": "🥤", 
            "disponible": True,
            "foto": FOTO_DEFECTO
        },
        "Combo Buffalo": {
            "precio": 25.0, 
            "icono": "🎁", 
            "disponible": True,
            "foto": FOTO_DEFECTO
        }
    }
    if os.path.exists(RUTA_JSON_MENU):
        try:
            with open(RUTA_JSON_MENU, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except:
            return menu_defecto
    return menu_defecto
# --- FUNCIONES DE PERSISTENCIA Y REGISTRO EN TIEMPO REAL DEL HISTORIAL ---
def guardar_historial_en_archivo(historial_data):
    import json
    with open(RUTA_JSON_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(historial_data, archivo, indent=4, ensure_ascii=False)

def cargar_historial_desde_archivo():
    import json
    if os.path.exists(RUTA_JSON_HISTORIAL):
        try:
            with open(RUTA_JSON_HISTORIAL, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except:
            return []
    return []

# =========================================================
# LECTURA Y CARGA DE HOJAS DE ESTILOS Y ARCHIVOS CONFIG
# =========================================================
if os.path.exists(RUTA_CSS):
    with open(RUTA_CSS, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sincronización reactiva inmediata de los datos permanentes
st.session_state.menu_dinamico = cargar_menu_desde_archivo()
st.session_state.historial_ordenes = cargar_historial_desde_archivo()

if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "total_acumulado" not in st.session_state:
    st.session_state.total_acumulado = 0.0
if "pedido_guardado" not in st.session_state:
    st.session_state.pedido_guardado = False
if "pantalla_actual" not in st.session_state:
    st.session_state.pantalla_actual = "bienvenida"

# ANCLAJE DE RELOJ OFICIAL PARA PERÚ (GMT-5) SINCRO WEB
zona_peru = timezone(timedelta(hours=-5))
fecha_actual = datetime.now(zona_peru).strftime("%d/%m/%Y %H:%M:%S")

# PROCESAMIENTO REACTIVO DE KPI'S DEL NEGOCIO
total_caja = 0.0
total_pedidos = len(st.session_state.historial_ordenes)
conteos_productos = {prod: 0 for prod in st.session_state.menu_dinamico.keys()}
metodos_pagos = {"Efectivo": 0.0, "Yape": 0.0, "Tarjeta": 0.0}

for orden in st.session_state.historial_ordenes:
    monto_num = float(orden["Total"].replace("S/", ""))
    total_caja += monto_num
    if orden["Método Pago"] in metodos_pagos:
        metodos_pagos[orden["Método Pago"]] += monto_num
        
    detalle = orden["Detalle Artículos"]
    for prod in list(conteos_productos.keys()):
        if prod in detalle:
            try:
                partes = detalle.split(", ")
                for parte in partes:
                    if prod in parte:
                        cant_txt = parte.split(f"x {prod}")[0].strip()
                        conteos_productos[prod] += int(cant_txt)
            except:
                pass

st.session_state.numero_boleta = total_pedidos + 1

# Enlace dinámico local de la foto de la fachada de tu restaurante
URL_BANNER_LOCAL = os.path.join(BASE_DIR, "Captura de pantalla 2026-05-24 090610.png")

# =========================================================
# BARRA LATERAL (SIDEBAR): MENÚ MULTIUSO INTERACTIVO
# =========================================================
st.sidebar.markdown("<h2 style='text-align: center; color: #f39c12;'>🥩 El Gran Búfalo</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 13px; color: #aaa;'>Especialistas en carnes y parrillas premium al carbón de manera artesanal.</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Sección 1: Datos de Atención e Información del Local
st.sidebar.markdown("#### 🕒 HORARIO DE ATENCIÓN")
st.sidebar.caption("Lunes a Domingo: 12:00 PM - 11:00 PM")

st.sidebar.markdown("#### 📍 NUESTRA UBICACIÓN")
st.sidebar.caption("Av. Principal El Gran Búfalo 742, Trujillo, Perú")
st.sidebar.markdown("---")

# Sección 2: Botón de Soporte Técnico Directo por WhatsApp
st.sidebar.markdown("#### 📞 ¿NECESITAS AYUDA?")
st.sidebar.markdown("""
    <a href="https://wa.me" target="_blank" style="text-decoration: none;">
        <button style="width: 100%; background-color: #25d366; color: white; border: none; padding: 10px; border-radius: 5px; font-weight: bold; cursor: pointer; margin-bottom: 15px;">
            💬 Chatear con Soporte
        </button>
    </a>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Sección 3: Acceso Administrativo (Oculto discretamente al final)
st.sidebar.markdown("### 🔒 ACCESO ADMINISTRATIVO")
usuario_input = st.sidebar.text_input("Nombre de Usuario:", key="user_login").strip()
clave_input = st.sidebar.text_input("Contraseña:", type="password", key="pass_login").strip()

es_admin = (usuario_input == "Grupo 5" and clave_input == "jhohan-2026")

if es_admin:
    st.sidebar.success("✔ Modo Administrador Activo")
elif usuario_input or clave_input:
    st.sidebar.error("❌ Credenciales incorrectas")
# =========================================================
# FLUJO DE PANTALLAS (MODO ADMINISTRADOR INTEGRAL)
# =========================================================
if es_admin:
    st.markdown("<h1 class='titulo-principal'>📊 PANEL DE AUDITORÍA Y CAJA CHICA</h1>", unsafe_allow_html=True)
    st.info(f"📋 **Reporte Gerencial del Grupo 5** — Sincronizado en tiempo real: {fecha_actual}")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # MÓDULO MULTIMEDIA: Formulario para añadir nuevos productos con foto local
    with st.expander("➕ 🛠️ AÑADIR NUEVO PRODUCTO CON FOTO", expanded=False):
        st.caption("Complete los datos para agregar un plato nuevo subiendo una imagen desde su dispositivo.")
        nuevo_nombre = st.text_input("Nombre del nuevo producto:", placeholder="Ej. Alitas BBQ, Papas Nativas...").strip()
        
        col_new1, col_new2 = st.columns(2)
        with col_new1:
            nuevo_precio = st.number_input("Precio de venta (S/):", min_value=0.5, value=10.0, step=0.5)
        with col_new2:
            nuevo_icono = st.text_input("Icono representativo (Emoji):", value="🍟", max_chars=2).strip()
            
        archivo_foto = st.file_uploader("Selecciona la foto del plato desde tu equipo:", type=["jpg", "jpeg", "png"], key="upload_nuevo_prod")
            
        if st.button("🚀 GUARDAR E INTEGRAR NUEVO PRODUCTO", use_container_width=True):
            if nuevo_nombre:
                if nuevo_nombre not in st.session_state.menu_dinamico:
                    if archivo_foto is not None:
                        bytes_foto = archivo_foto.getvalue()
                        encoded_foto = base64.b64encode(bytes_foto).decode()
                        src_final_foto = f"data:image/png;base64,{encoded_foto}"
                    else:
                        src_final_foto = "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' width='100' height='100' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='3' width='18' height='18' rx='2' ry='2'/><circle cx='8.5' cy='8.5' r='1.5'/><polyline points='21 15 16 10 5 21'/></svg>"

                    st.session_state.menu_dinamico[nuevo_nombre] = {
                        "precio": nuevo_precio,
                        "icono": nuevo_icono,
                        "disponible": True,
                        "foto": src_final_foto
                    }
                    guardar_menu_en_archivo(st.session_state.menu_dinamico)
                    st.success(f"✔ ¡{nuevo_icono} {nuevo_nombre} con foto propia integrado con éxito!")
                    st.rerun()
                else:
                    st.error("⚠️ Error: Ese producto ya existe en la carta actual.")
            else:
                st.error("⚠️ Error: El nombre del producto no puede estar vacío.")

    # GESTIÓN Y EDICIÓN DE CARTA EXISTENTE (ACTUALIZADO: VER FOTO ESTILIZADA Y ELIMINAR)
    st.markdown("### 📝 GESTIÓN DE PRECIOS, STOCK Y FOTOS")
    st.caption("Modifique los valores, actualice fotos o elimine alimentos permanentemente.")
    
    eliminar_producto = None
    productos_lista = list(st.session_state.menu_dinamico.keys())
    
    for i in range(0, len(productos_lista), 2):
        col_ed1, col_ed2 = st.columns(2)
        
        # Producto Izquierda
        p_izq = productos_lista[i]
        with col_ed1:
            st.markdown(f"### {st.session_state.menu_dinamico[p_izq]['icono']} {p_izq}")
            
            # Previsualización de la foto actual estilizada en la administración
            foto_actual_izq = st.session_state.menu_dinamico[p_izq].get("foto", "")
            if foto_actual_izq:
                st.markdown(f"""<img src="{foto_actual_izq}" style="width:100%; height:120px; object-fit:cover; border-radius:6px; margin-bottom:10px; border: 1px solid #444;">""", unsafe_allow_html=True)
            
            p_izq_val = st.number_input(f"Precio (S/) - {p_izq}:", min_value=1.0, value=float(st.session_state.menu_dinamico[p_izq]["precio"]), step=0.5, key=f"p_{p_izq}")
            p_izq_disp = st.checkbox("Disponible para venta", value=st.session_state.menu_dinamico[p_izq]["disponible"], key=f"d_{p_izq}")
            
            foto_cambio_izq = st.file_uploader(f"Actualizar foto de {p_izq}:", type=["jpg", "jpeg", "png"], key=f"f_up_{p_izq}")
            
            if foto_cambio_izq is not None:
                bytes_f = foto_cambio_izq.getvalue()
                encoded_f = base64.b64encode(bytes_f).decode()
                foto_existente_izq = f"data:image/png;base64,{encoded_f}"
            else:
                foto_existente_izq = st.session_state.menu_dinamico[p_izq].get("foto", "")
            
            st.session_state.menu_dinamico[p_izq] = {
                "precio": p_izq_val, 
                "icono": st.session_state.menu_dinamico[p_izq]["icono"], 
                "disponible": p_izq_disp,
                "foto": foto_existente_izq
            }
            
            if st.button(f"❌ Eliminar {p_izq}", key=f"del_{p_izq}", use_container_width=True):
                eliminar_producto = p_izq
                
        # Producto Derecha (Si existe en el índice)
        if i + 1 < len(productos_lista):
            p_der = productos_lista[i+1]
            with col_ed2:
                st.markdown(f"### {st.session_state.menu_dinamico[p_der]['icono']} {p_der}")
                
                # Previsualización de la foto actual estilizada en la administración
                foto_actual_der = st.session_state.menu_dinamico[p_der].get("foto", "")
                if foto_actual_der:
                    st.markdown(f"""<img src="{foto_actual_der}" style="width:100%; height:120px; object-fit:cover; border-radius:6px; margin-bottom:10px; border: 1px solid #444;">""", unsafe_allow_html=True)
                
                p_der_val = st.number_input(f"Precio (S/) - {p_der}:", min_value=1.0, value=float(st.session_state.menu_dinamico[p_der]["precio"]), step=0.5, key=f"p_{p_der}")
                p_der_disp = st.checkbox("Disponible para venta", value=st.session_state.menu_dinamico[p_der]["disponible"], key=f"d_{p_der}")
                
                foto_cambio_der = st.file_uploader(f"Actualizar foto de {p_der}:", type=["jpg", "jpeg", "png"], key=f"f_up_{p_der}")
                
                if foto_cambio_der is not None:
                    bytes_f = foto_cambio_der.getvalue()
                    encoded_f = base64.b64encode(bytes_f).decode()
                    foto_existente_der = f"data:image/png;base64,{encoded_f}"
                else:
                    foto_existente_der = st.session_state.menu_dinamico[p_der].get("foto", "")
                
                st.session_state.menu_dinamico[p_der] = {
                    "precio": p_der_val, 
                    "icono": st.session_state.menu_dinamico[p_der]["icono"], 
                    "disponible": p_der_disp,
                    "foto": foto_existente_der
                }
                
                if st.button(f"❌ Eliminar {p_der}", key=f"del_{p_der}", use_container_width=True):
                    eliminar_producto = p_der
        st.markdown("---")
    # Lógica de eliminación inmediata física
    if eliminar_producto is not None:
        del st.session_state.menu_dinamico[eliminar_producto]
        guardar_menu_en_archivo(st.session_state.menu_dinamico)
        st.warning(f"🗑️ Producto '{eliminar_producto}' removido permanentemente de la base de datos.")
        st.rerun()
        
    if st.button("💾 CONFIRMAR Y SINCRONIZAR CAMBIOS DE LA CARTA", use_container_width=True):
        guardar_menu_en_archivo(st.session_state.menu_dinamico)
        st.success("✔ ¡Cambios de la carta guardados físicamente con éxito!")
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 AUDITORÍA GENERAL DE CAJA CHICA")

    # KPIs Financieros Principales Reactivos
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.markdown(f"<div style='background-color: #1c1c1c; padding: 20px; border-radius: 8px; border-left: 5px solid #27ae60; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);'><p style='margin:0; font-size:14px; color:#aaa; font-weight:bold;'>💰 RECAUDACIÓN TOTAL ACUMULADA</p><h2 style='margin:5px 0 0 0; color:#fff; font-size:32px;'>S/{total_caja:.2f}</h2></div>", unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f"<div style='background-color: #1c1c1c; padding: 20px; border-radius: 8px; border-left: 5px solid #f39c12; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);'><p style='margin:0; font-size:14px; color:#aaa; font-weight:bold;'>📦 ÓRDENES HISTÓRICAS PROCESADAS</p><h2 style='margin:5px 0 0 0; color:#fff; font-size:32px;'>{total_pedidos} Pedidos</h2></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 ANALÍTICA: UNIDADES VENDIDAS DE LA JORNADA")
    
    df_grafico = pd.DataFrame({
        'Producto': list(conteos_productos.keys()),
        'Cantidad': list(conteos_productos.values())
    })
    barras = alt.Chart(df_grafico).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X('Producto:N', title='Productos del Menú', sort=None, axis=alt.Axis(labelAngle=0, labelColor='#ffffff', titleColor='#f39c12')),
        y=alt.Y('Cantidad:Q', title='Unidades Vendidas', axis=alt.Axis(grid=True, gridColor='#2c2c2c', labelColor='#ffffff', titleColor='#f39c12')),
        color=alt.Color('Cantidad:Q', scale=alt.Scale(scheme='orangered'), legend=None)
    )
    texto_etiquetas = barras.mark_text(align='center', baseline='bottom', dy=-5, color='#ffffff', fontSize=13, fontWeight='bold').encode(text='Cantidad:Q')
    grafico_final = (barras + texto_etiquetas).properties(width=600, height=320).configure_view(strokeWidth=0).configure_axis(domainWidth=1, domainColor='#444444')
    st.altair_chart(grafico_final, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🕒 BITÁCORA: CONTROL HISTÓRICO DE PEDIDOS")
    if st.session_state.historial_ordenes:
        df_historial = pd.DataFrame(st.session_state.historial_ordenes)
        df_historial.columns = ["🕒 FECHA Y HORA", "🧾 NRO. BOLETA", "📦 DETALLE ARTÍCULOS", "🛵 ENTREGA", "💳 MÉTODO PAGO", "💰 TOTAL"]
        st.dataframe(df_historial, use_container_width=True, hide_index=True)
    else:
        st.caption("Aún no se han registrado transacciones en la base de datos.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💳 FLUJO DE CAJA POR MÉTODO DE PAGO")
    
    col_ef, col_yp, col_tj = st.columns(3)
    with col_ef:
        st.markdown(f"<div style='background-color:#1a1a1a; padding:15px; border-radius:6px; border:1px solid #333; text-align:center;'><span style='font-size:24px;'>💵</span><p style='margin:5px 0 0 0; font-size:13px; color:#888;'>EFECTIVO</p><h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{metodos_pagos['Efectivo']:.2f}</h4></div>", unsafe_allow_html=True)
    with col_yp:
        st.markdown(f"<div style='background-color:#1a1a1a; padding:15px; border-radius:6px; border:1px solid #333; text-align:center;'><span style='font-size:24px;'>📱</span><p style='margin:5px 0 0 0; font-size:13px; color:#888;'>YAPE</p><h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{metodos_pagos['Yape']:.2f}</h4></div>", unsafe_allow_html=True)
    with col_tj:
        st.markdown(f"<div style='background-color:#1a1a1a; padding:15px; border-radius:6px; border:1px solid #333; text-align:center;'><span style='font-size:24px;'>💳</span><p style='margin:5px 0 0 0; font-size:13px; color:#888;'>TARJETA</p><h4 style='margin:5px 0 0 0; color:#27ae60;'>S/{metodos_pagos['Tarjeta']:.2f}</h4></div>", unsafe_allow_html=True)
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
else:
    # PANTALLA 1: BIENVENIDA LIMPIA CON BANNER Y BOTÓN DE MENÚ COLAPSABLE
    if st.session_state.pantalla_actual == "bienvenida":
        if os.path.exists(URL_BANNER_LOCAL):
            with open(URL_BANNER_LOCAL, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            
            st.markdown(f"""
                <style>
                .stApp {{
                    background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url("data:image/png;base64,{encoded_string}");
                    background-size: cover !important;
                    background-position: center !important;
                    background-repeat: no-repeat !important;
                    background-attachment: fixed !important;
                }}
                </style>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón premium superior para desplegar el menú de la izquierda con las 3 rayitas
                        # RUTA CORRECTA: Forzamos a que el botón se acomode al lado izquierdo usando columnas estáticas
        if st.button("☰ Menú de Opciones", key="btn_abrir_sidebar"):
            st.toast("⬅️ Despliega el menú utilizando la zona táctil en la esquina superior izquierda de tu pantalla.", icon="📱")

        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        
        st.markdown("<br><p style='text-align: center; font-size: 24px; font-weight: bold; color: #f39c12;'>🔥 Bienvenidos al templo de la buena carne 🔥</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px; color: #ffffff;'>¿Desea registrar un nuevo pedido de nuestra deliciosa parrilla?</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🛒 EMPEZAR MI PEDIDO", use_container_width=True):
            st.session_state.pantalla_actual = "catalogo"
            st.rerun()
            
        # Pie de página de Redes Sociales (Footer)
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div class='social-footer'>
                <p style='margin-bottom: 10px; font-size: 14px; letter-spacing: 2px; color: #888; font-weight: bold;'>SÍGUENOS EN REDES SOCIALES</p>
                <a href='https://facebook.com' target='_blank' class='social-icon'>📘 Facebook</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <a href='https://instagram.com' target='_blank' class='social-icon'>📸 Instagram</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <a href='https://wa.me' target='_blank' class='social-icon'>🟢 WhatsApp</a>
            </div>
        """, unsafe_allow_html=True)
    # PANTALLA 2: CATÁLOGO EN COLUMNAS CON IMÁGENES DINÁMICAS (FOOD CARDS PREMIUM)
    elif st.session_state.pantalla_actual == "catalogo" and not st.session_state.pedido_guardado:
        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        st.image(URL_BANNER_LOCAL, use_container_width=True)
        st.text(f"Fecha y hora oficial de Perú (GMT-5): {fecha_actual}\n")
        
        st.subheader("🍽️ SELECCIÓN DE PRODUCTOS (EL MENÚ DE HOY)")
        st.info("Ingrese las cantidades de los productos que desea llevar:")

        col1, col2 = st.columns(2)
        cantidades_ingresadas = {}
        
        productos_lista = list(st.session_state.menu_dinamico.keys())
        
        for i in range(len(productos_lista)):
            prod = productos_lista[i]
            info = st.session_state.menu_dinamico[prod]
            target_col = col1 if i % 2 == 0 else col2
            
            with target_col:
                if info["disponible"]:
                    url_imagen_plato = info.get("foto", "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' width='100' height='100' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='3' width='18' height='18' rx='2' ry='2'/><circle cx='8.5' cy='8.5' r='1.5'/><polyline points='21 15 16 10 5 21'/></svg>")
                    
                    # Imagen con sombreado y bordes perfectos
                    st.markdown(f"""<img src="{url_imagen_plato}" style="width:100%; height:200px; object-fit:cover; border-radius:12px 12px 0px 0px; box-shadow: 0px 4px 12px rgba(0,0,0,0.6); display:block; margin:0; padding:0;">""", unsafe_allow_html=True)
                    
                    # Estilizado completo con textos gigantes y precio dorado resaltado
                    st.markdown(f"""
                        <div class='product-card-bottom'>
                            <span class='product-title'>{info['icono']} {prod}</span>
                            <span class='product-price'>S/{info['precio']:.2f}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Casilla de entrada numérica compacta acoplada debajo
                    cantidades_ingresadas[prod] = st.number_input(
                        f"Cantidad a llevar de {prod}:", 
                        min_value=0, step=1, key=f"cat_{prod}", label_visibility="collapsed"
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="width:100%; height:200px; background-color:#222; border-radius:12px 12px 0px 0px; display:flex; align-items:center; justify-content:center;"><span style="font-size:50px; filter:grayscale(100%);">{info['icono']}</span></div>""", unsafe_allow_html=True)
                    st.markdown(f"<div style='background-color:#1c1c1c; padding:20px; border-radius:0px 0px 12px 12px; border:2px solid #ff4b4b; text-align:center; margin-bottom:25px;'><p style='color: #ff4b4b; font-size:18px; font-weight: bold; margin:0;'>❌ {prod}<br>(AGOTADO POR HOY)</p></div>", unsafe_allow_html=True)
