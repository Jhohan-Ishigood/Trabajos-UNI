import streamlit as st
from datetime import datetime, timedelta, timezone  # Reloj oficial para Perú (GMT-5)
import os
import streamlit.components.v1 as components
import pandas as pd  # Motor de analítica para el control de la bitácora
import altair as alt  # Motor gráfico premium para el Dashboard corporativo
import base64  # Motor multimedia para incrustar fotos locales en HTML y CSS

# Configuración premium inicial de pantalla responsiva con barra lateral colapsada por defecto
st.set_page_config(
    page_title="El Gran Búfalo - Sistema de Pedidos", 
    page_icon="🥩", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DETERMINACIÓN DINÁMICA DE LA RUTA RAÍZ PARA EVITAR ERRORES EN LA NUBE
# ============================================================================
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

# Enlace de la ruta de la foto de tu restaurante para el fondo premium
URL_BANNER_LOCAL = os.path.join(BASE_DIR, "Captura de pantalla 2026-05-24 090610.png")

# ============================================================================
# LECTURA Y CARGA EN TIEMPO REAL DE LA HOJA DE ESTILOS CSS
# ============================================================================
if os.path.exists(RUTA_CSS):
    with open(RUTA_CSS, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# --- FUNCIONES DE PERSISTENCIA Y SINCRONIZACIÓN DE LA CARTA ---
def guardar_menu_en_archivo(menu_data):
    import json
    with open(RUTA_JSON_MENU, "w", encoding="utf-8") as archivo:
        json.dump(menu_data, archivo, indent=4, ensure_ascii=False)

def cargar_menu_desde_archivo():
    import json
    # Silueta vectorial en Base64 por defecto por seguridad informática
    FOTO_DEFECTO = "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' width='100' height='100' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='3' width='18' height='18' rx='2' ry='2'/><circle cx='8.5' cy='8.5' r='1.5'/><polyline points='21 15 16 10 5 21'/></svg>"
    
    menu_defecto = {
        "Hamburguesa": {
            "precio": 18.0, 
            "icono": "🍔", 
            "disponible": True,
            "foto": FOTO_DEFECTO,
            "stock": 15
        },
        "Carne a la parrilla": {
            "precio": 35.0, 
            "icono": "🥩", 
            "disponible": True,
            "foto": FOTO_DEFECTO,
            "stock": 10
        },
        "Jugo": {
            "precio": 6.0, 
            "icono": "🥤", 
            "disponible": True,
            "foto": FOTO_DEFECTO,
            "stock": 20
        },
        "Combo Buffalo": {
            "precio": 25.0, 
            "icono": "🎁", 
            "disponible": True,
            "foto": FOTO_DEFECTO,
            "stock": 8
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


# ============================================================================
# INICIALIZACIÓN DE VARIABLES REACTIVAS DE SESIÓN (ESTADOS CRÍTICOS)
# ============================================================================
if "menu_dinamico" not in st.session_state:
    st.session_state.menu_dinamico = cargar_menu_desde_archivo()
if "historial_ordenes" not in st.session_state:
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
# ============================================================================
# PROCESAMIENTO REACTIVO DE KPI'S Y AUDITORÍA DE LA JORNADA
# ============================================================================
total_caja = 0.0
total_pedidos = len(st.session_state.historial_ordenes)
conteos_productos = {prod: 0 for prod in st.session_state.menu_dinamico.keys()}
metodos_pagos = {"Efectivo": 0.0, "Yape": 0.0, "Tarjeta": 0.0}

for orden in st.session_state.historial_ordenes:
    monto_num = float(orden["Total"].replace("S/", "").strip())
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
                        # Extraemos de forma segura la cantidad numérica
                        cant_txt = parte.split(f"x {prod}")[0].strip()
                        conteos_productos[prod] += int(cant_txt)
            except:
                pass

st.session_state.numero_boleta = total_pedidos + 1

# ============================================================================
# BARRA LATERAL (SIDEBAR): MENÚ MULTIUSO INTERACTIVO
# ============================================================================
st.sidebar.markdown("<h2 style='text-align: center; color: #f39c12;'>🥩 El Gran Búfalo</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 13px; color: #aaa;'>Especialistas en carnes y parrillas premium al carbón de manera artesanal.</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

if "mostrar_login_admin" not in st.session_state:
    st.session_state.mostrar_login_admin = False

st.sidebar.markdown("#### ⚙️ GESTIÓN INTERNA")
if st.sidebar.button("🔑 Ingresar como Administrador", use_container_width=True, key="btn_toggle_admin_login"):
    st.session_state.mostrar_login_admin = not st.session_state.mostrar_login_admin

usuario_input = ""
clave_input = ""
es_admin = False

if st.session_state.mostrar_login_admin:
    st.sidebar.markdown("<div style='background-color: #121212; padding: 12px; border-radius: 6px; border: 1px solid #333;'>", unsafe_allow_html=True)
    usuario_input = st.sidebar.text_input("Nombre de Usuario:", key="user_login").strip()
    clave_input = st.sidebar.text_input("Contraseña:", type="password", key="pass_login").strip()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

es_admin = (usuario_input == "Grupo 5" and clave_input == "jhohan-2026")

if es_admin:
    st.sidebar.success("✔ Modo Administrador Activo")
elif usuario_input or clave_input:
    st.sidebar.error("❌ Credenciales incorrectas")

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🕒 HORARIO DE ATENCIÓN")
st.sidebar.caption("Lunes a Domingo: 12:00 PM - 11:00 PM")

st.sidebar.markdown("#### 📍 NUESTRA UBICACIÓN")
st.sidebar.caption("Av. Principal El Gran Búfalo 742, Trujillo, Perú")
st.sidebar.markdown("---")

st.sidebar.markdown("#### 📞 ¿NECESITAS AYUDA?")
st.sidebar.markdown("""
    <a href="https://wa.me" target="_blank" style="text-decoration: none;">
        <button style="width: 100%; background-color: #25d366; color: white; border: none; padding: 10px; border-radius: 5px; font-weight: bold; cursor: pointer; margin-bottom: 15px;">
            💬 Chatear con Soporte
        </button>
    </a>
""", unsafe_allow_html=True)
# ============================================================================
# BARRA DE EXPLORACIÓN GLOBAL (ESTILO NETFLIX TEXTO PLANO AL COSTADO)
# ============================================================================

# Inicializamos estados globales de pestañas si no existen
if "categoria_activa" not in st.session_state:
    st.session_state.categoria_activa = "Todos"
if "lista_categorias" not in st.session_state:
    st.session_state.lista_categorias = ["Todos", "Parrillas", "Hamburguesas", "Bebidas", "Combos"]

# Inicializamos la variable de búsqueda limpia por defecto
busqueda = ""

# CASO 1: BARRA HORIZONTAL COMPACTA EXCLUSIVA PARA EL CLIENTE (EN EL CATÁLOGO)
if not es_admin and (st.session_state.pantalla_actual == "catalogo" and not st.session_state.pedido_guardado):
    # Creamos las columnas necesarias dinámicamente según las secciones existentes
    num_cats = len(st.session_state.lista_categorias)
    nav_cols = st.columns([1.2] + [1] * num_cats + [2.5], gap="small")
    
    with nav_cols[0]:
        st.markdown("<div class='nav-explorer-title' style='margin-top:8px;'>✨ EXPLORAR</div>", unsafe_allow_html=True)
        
    for idx, cat in enumerate(st.session_state.lista_categorias):
        with nav_cols[idx + 1]:
            if st.button(cat, key=f"nav_cli_{cat}", use_container_width=True):
                st.session_state.categoria_activa = cat
                st.rerun()
                
    with nav_cols[-1]:
        busqueda = st.text_input("🔍 Buscar...", placeholder="¿Qué se te antoja hoy?", label_visibility="collapsed", key="search_bar_cliente").strip().lower()
    st.markdown("<br>", unsafe_allow_html=True)


# 📊 CASO 2: BARRA HORIZONTAL COMPACTA EXCLUSIVA PARA EL ADMINISTRADOR (PANEL DE CONTROL)
if es_admin:
    num_cats_admin = len(st.session_state.lista_categorias)
    nav_cols_admin = st.columns([1.2] + [1] * num_cats_admin + [2.5], gap="small")
    
    with nav_cols_admin[0]:
        st.markdown("<div class='nav-explorer-title' style='margin-top:8px;'>⚙️ FILTRAR</div>", unsafe_allow_html=True)
        
    for idx, cat in enumerate(st.session_state.lista_categorias):
        with nav_cols_admin[idx + 1]:
            if st.button(cat, key=f"nav_adm_{cat}", use_container_width=True):
                st.session_state.categoria_activa = cat
                st.rerun()
                
    with nav_cols_admin[-1]:
        busqueda = st.text_input("🔍 Buscar en inventario...", placeholder="Buscar plato...", label_visibility="collapsed", key="search_bar_admin").strip().lower()
    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================================
# PANEL DE CONTROL DEL ADMINISTRADOR - INTEGRACIÓN DE MÓDULOS GESTORES
# ============================================================================
if es_admin:
    st.markdown("<h1 class='titulo-principal'>📊 PANEL DE AUDITORÍA Y CAJA CHICA</h1>", unsafe_allow_html=True)
    st.info(f"📋 **Reporte Gerencial del Grupo 5** — Sincronizado en tiempo real: {fecha_actual}")
    st.markdown("<br>", unsafe_allow_html=True)

    # CONFIGURACIÓN COMPACTA Y MODERNA DE GESTIÓN DE SECCIONES (SIN CAJAS FANTASMA)
    with st.expander("📁 ⚙️ CONFIGURACIÓN DE SECCIONES EN LA CARTA", expanded=False):
        st.caption("Añada nuevas pestañas al menú horizontal o elimine las secciones que ya no utilice en la jornada.")
        st.markdown("<br>", unsafe_allow_html=True)

        col_cat1, col_cat2 = st.columns(2, gap="medium")
        
        with col_cat1:
            with st.container(border=True):
                st.markdown("##### ➕ Crear Nueva Sección")
                nueva_cat = st.text_input(
                    "Crear Sección", 
                    placeholder="Escribe aquí la nueva sección (Ej. Postres)...", 
                    key="input_create_cat_name",
                    label_visibility="collapsed"
                ).strip().capitalize()
                
                if st.button("➕ CREAR NUEVA SECCIÓN", use_container_width=True, key="btn_create_cat"):
                    if nueva_cat and nueva_cat not in st.session_state.lista_categorias:
                        st.session_state.lista_categorias.append(nueva_cat)
                        st.success(f"✔ ¡Sección '{nueva_cat}' integrada con éxito!")
                        st.rerun()
                    elif nueva_cat in st.session_state.lista_categorias:
                        st.error("⚠️ Error: Esta categoría ya existe en el menú.")
                    else:
                        st.error("⚠️ Error: El nombre no puede estar vacío.")
                    
        with col_cat2:
            with st.container(border=True):
                st.markdown("##### 🗑️ Eliminar Sección Seleccionada")
                cats_borrables = [c for c in st.session_state.lista_categorias if c != "Todos"]
                
                cat_a_borrar = st.selectbox(
                    "Eliminar Sección", 
                    options=cats_borrables, 
                    key="select_delete_cat_name",
                    label_visibility="collapsed"
                )
                
                if st.button("🗑️ ELIMINAR SECCIÓN SELECCIONADA", use_container_width=True, key="btn_delete_cat"):
                    if cat_a_borrar:
                        st.session_state.lista_categorias.remove(cat_a_borrar)
                        if st.session_state.categoria_activa == cat_a_borrar:
                            st.session_state.categoria_activa = "Todos"
                        st.warning(f"🗑️ Sección '{cat_a_borrar}' removida físicamente de la carta.")
                        st.rerun()
    # MÓDULO MULTIMEDIA: Formulario para añadir nuevos productos con foto local
    with st.expander("➕ 🛠️ AÑADIR NUEVO PRODUCTO CON FOTO", expanded=False):
        st.caption("Complete los datos para agregar un plato nuevo subiendo una imagen desde su dispositivo.")
        nuevo_nombre = st.text_input("Nombre del nuevo producto:", placeholder="Ej. Alitas BBQ, Papas Nativas...").strip()
        
        col_new1, col_new2, col_new3 = st.columns(3)
        with col_new1:
            nuevo_precio = st.number_input("Precio de venta (S/):", min_value=0.5, value=10.0, step=0.5)
        with col_new2:
            nuevo_icono = st.text_input("Icono representativo (Emoji):", value="🍟", max_chars=2).strip()
        with col_new3:
            nuevo_stock = st.number_input("Stock inicial (Unidades):", min_value=0, value=15, step=1)
            
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
                        "foto": src_final_foto,
                        "stock": int(nuevo_stock)
                    }
                    guardar_menu_en_archivo(st.session_state.menu_dinamico)
                    st.success(f"✔ ¡{nuevo_icono} {nuevo_nombre} con foto propia e inventario integrado con éxito!")
                    st.rerun()
                else:
                    st.error("⚠️ Error: Ese producto ya existe en la carta actual.")
            else:
                st.error("⚠️ Error: El nombre del producto no puede estar vacío.")

    # GESTIÓN Y EDICIÓN DE CARTA EXISTENTE (ACTUALIZADO: CON FILTRADO OPERATIVO)
    st.markdown("### 📝 GESTIÓN DE PRECIOS, STOCK Y FOTOS")
    st.caption(f"Modifique los valores. Filtrado actual: **{st.session_state.categoria_activa}**")
    
    eliminar_producto = None
    productos_lista = list(st.session_state.menu_dinamico.keys())
    
    # Clasificación y mapeo en tiempo real de los platos para el panel admin
    productos_filtrados_admin = []
    for prod in productos_lista:
        if busqueda and busqueda not in prod.lower():
            continue
            
        cat_prod = "Todos"
        if "parrilla" in prod.lower() or "carne" in prod.lower():
            cat_prod = "Parrillas"
        elif "hamburguesa" in prod.lower():
            cat_prod = "Hamburguesas"
        elif "jugo" in prod.lower() or "gaseosa" in prod.lower() or "bebida" in prod.lower() or "café" in prod.lower():
            cat_prod = "Bebidas"
        elif "combo" in prod.lower():
            cat_prod = "Combos"

        if st.session_state.categoria_activa == "Todos" or st.session_state.categoria_activa == cat_prod:
            productos_filtrados_admin.append(prod)
    
    for i in range(0, len(productos_filtrados_admin), 2):
        col_ed1, col_ed2 = st.columns(2)
        
        # Producto Izquierda
        p_izq = productos_filtrados_admin[i]
        with col_ed1:
            st.markdown(f"### {st.session_state.menu_dinamico[p_izq]['icono']} {p_izq}")
            foto_actual_izq = st.session_state.menu_dinamico[p_izq].get("foto", "")
            if foto_actual_izq:
                st.markdown(f"""<img src="{foto_actual_izq}" style="width:100%; height:120px; object-fit:cover; border-radius:6px; margin-bottom:10px; border: 1px solid #444;">""", unsafe_allow_html=True)
            
            p_izq_val = st.number_input(f"Precio (S/) - {p_izq}:", min_value=1.0, value=float(st.session_state.menu_dinamico[p_izq]["precio"]), step=0.5, key=f"p_{p_izq}")
            p_izq_disp = st.checkbox("Disponible para venta", value=st.session_state.menu_dinamico[p_izq]["disponible"], key=f"d_{p_izq}")
            p_izq_stock = st.number_input(f"Stock Disponible - {p_izq}:", min_value=0, value=int(st.session_state.menu_dinamico[p_izq].get("stock", 10)), step=1, key=f"s_{p_izq}")
            
            foto_cambio_izq = st.file_uploader(f"Actualizar foto de {p_izq}:", type=["jpg", "jpeg", "png"], key=f"f_up_{p_izq}")
            foto_existing_izq = st.session_state.menu_dinamico[p_izq].get("foto", "")
            if foto_cambio_izq is not None:
                bytes_f = foto_cambio_izq.getvalue()
                encoded_f = base64.b64encode(bytes_f).decode()
                foto_existing_izq = f"data:image/png;base64,{encoded_f}"
            
            st.session_state.menu_dinamico[p_izq] = {"precio": p_izq_val, "icono": st.session_state.menu_dinamico[p_izq]["icono"], "disponible": p_izq_disp, "foto": foto_existing_izq, "stock": p_izq_stock}
            if st.button(f"❌ Eliminar {p_izq}", key=f"del_{p_izq}", use_container_width=True):
                eliminar_producto = p_izq
                
        # Producto Derecha
        if i + 1 < len(productos_filtrados_admin):
            p_der = productos_filtrados_admin[i+1]
            with col_ed2:
                st.markdown(f"### {st.session_state.menu_dinamico[p_der]['icono']} {p_der}")
                foto_actual_der = st.session_state.menu_dinamico[p_der].get("foto", "")
                if foto_actual_der:
                    st.markdown(f"""<img src="{foto_actual_der}" style="width:100%; height:120px; object-fit:cover; border-radius:6px; margin-bottom:10px; border: 1px solid #444;">""", unsafe_allow_html=True)
                
                p_der_val = st.number_input(f"Precio (S/) - {p_der}:", min_value=1.0, value=float(st.session_state.menu_dinamico[p_der]["precio"]), step=0.5, key=f"p_{p_der}")
                p_der_disp = st.checkbox("Disponible para venta", value=st.session_state.menu_dinamico[p_der]["disponible"], key=f"d_{p_der}")
                p_der_stock = st.number_input(f"Stock Disponible - {p_der}:", min_value=0, value=int(st.session_state.menu_dinamico[p_der].get("stock", 10)), step=1, key=f"s_{p_der}")
                
                foto_cambio_der = st.file_uploader(f"Actualizar foto de {p_der}:", type=["jpg", "jpeg", "png"], key=f"f_up_{p_der}")
                foto_existing_der = st.session_state.menu_dinamico[p_der].get("foto", "")
                if foto_cambio_der is not None:
                    bytes_f = foto_cambio_der.getvalue()
                    encoded_f = base64.b64encode(bytes_f).decode()
                    foto_existing_der = f"data:image/png;base64,{encoded_f}"
                
                st.session_state.menu_dinamico[p_der] = {"precio": p_der_val, "icono": st.session_state.menu_dinamico[p_der]["icono"], "disponible": p_der_disp, "foto": foto_existing_der, "stock": p_der_stock}
                if st.button(f"❌ Eliminar {p_der}", key=f"del_{p_der}", use_container_width=True):
                    eliminar_producto = p_der
        st.markdown("---")

    if eliminar_producto is not None:
        del st.session_state.menu_dinamico[eliminar_producto]
        guardar_menu_en_archivo(st.session_state.menu_dinamico)
        st.success(f"✔ ¡Producto '{eliminar_producto}' eliminado con éxito!")
        st.rerun()

    if st.button("💾 CONFIRMAR Y SINCRONIZAR CAMBIOS DE LA CARTA", use_container_width=True):
        guardar_menu_en_archivo(st.session_state.menu_dinamico)
        st.success("✔ ¡Cambios guardados físicamente con éxito!")
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 AUDITORÍA GENERAL DE CAJA CHICA")

    # KPIs Financieros Reactivos
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
    # PANTALLA 1: BIENVENIDA LIMPIA CON BANNER Y BANNER DE FONDO
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
    # PANTALLA 2: CATÁLOGO DE PRODUCTOS (VISTA DE CLIENTE CON FILTRADO OPERATIVO)
    elif st.session_state.pantalla_actual == "catalogo" and not st.session_state.pedido_guardado:
        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        st.text(f"Fecha y hora oficial de Perú (GMT-5): {fecha_actual}\n")
        
        st.subheader(f"🍽️ SELECCIÓN DE {st.session_state.categoria_activa.upper()}")
        st.info("Ingrese las cantidades de los productos que desea llevar:")

        # =========================================================
        # FILTRADO DINÁMICO DE PRODUCTOS EN TIEMPO REAL
        # =========================================================
        productos_lista = list(st.session_state.menu_dinamico.keys())
        productos_filtrados = []

        for prod in productos_lista:
            # 1. Filtro por la barra de búsqueda superior global
            if busqueda and busqueda not in prod.lower():
                continue
                
            # 2. Clasificación automática por palabras clave en los nombres
            cat_prod = "Todos"
            if "parrilla" in prod.lower() or "carne" in prod.lower():
                cat_prod = "Parrillas"
            elif "hamburguesa" in prod.lower():
                cat_prod = "Hamburguesas"
            elif "jugo" in prod.lower() or "gaseosa" in prod.lower() or "bebida" in prod.lower() or "café" in prod.lower():
                cat_prod = "Bebidas"
            elif "combo" in prod.lower():
                cat_prod = "Combos"

            # Validamos si coincide con la categoría seleccionada en la barra superior
            if st.session_state.categoria_activa == "Todos" or st.session_state.categoria_activa == cat_prod:
                productos_filtrados.append(prod)

        # Rejilla responsiva forzada a 2 columnas en celulares y PC mediante st.columns y gap
        col1, col2 = st.columns(2, gap="medium")
        cantidades_ingresadas = {}
        
        for i in range(len(productos_filtrados)):
            prod = productos_filtrados[i]
            info = st.session_state.menu_dinamico[prod]
            target_col = col1 if i % 2 == 0 else col2
            
            stock_actual = info.get("stock", 0)
            esta_disponible = info["disponible"] and stock_actual > 0
            
            with target_col:
                if esta_disponible:
                    url_imagen_plato = info.get("foto", "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' width='100' height='100' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='3' width='18' height='18' rx='2' ry='2'/><circle cx='8.5' cy='8.5' r='1.5'/><polyline points='21 15 16 10 5 21'/></svg>")
                    st.markdown(f"""<img src="{url_imagen_plato}" style="width:100%; height:200px; object-fit:cover; border-radius:12px 12px 0px 0px; box-shadow: 0px 4px 12px rgba(0,0,0,0.6); display:block; margin:0; padding:0;">""", unsafe_allow_html=True)
                    
                    texto_precio = f"S/{info['precio']:.2f}"
                    if stock_actual <= 3:
                        texto_precio = f"🔥 ¡SOLO QUEDAN {stock_actual}! 🔥"
                    
                    st.markdown(f"""
                        <div class='product-card-bottom'>
                            <span class='product-title'>{info['icono']} {prod}</span>
                            <span class='product-price'>{texto_precio}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    cantidades_ingresadas[prod] = st.number_input(
                        f"Cantidad de {prod}:", min_value=0, max_value=int(stock_actual), step=1, key=f"cat_{prod}", label_visibility="collapsed"
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="width:100%; height:200px; background-color:#222; border-radius:12px 12px 0px 0px; display:flex; align-items:center; justify-content:center;"><span style="font-size:50px; filter:grayscale(100%);">{info['icono']}</span></div>""", unsafe_allow_html=True)
                    st.markdown(f"<div style='background-color:#1c1c1c; padding:20px; border-radius:0px 0px 12px 12px; border:2px solid #ff4b4b; text-align:center; margin-bottom:25px;'><p style='color: #ff4b4b; font-size:18px; font-weight: bold; margin:0;'>❌ {prod}<br>(AGOTADO)</p></div>", unsafe_allow_html=True)

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
        # Inyección JavaScript reforzada para resetear el scroll superior en la nube
        components.html(
            """
            <script>
                window.scrollTo({top: 0, behavior: 'instant'});
                if (window.parent) {
                    window.parent.scrollTo({top: 0, behavior: 'instant'});
                    var appContainer = window.parent.document.querySelector('.main') || window.parent.document.querySelector('.stApp');
                    if (appContainer) {
                        appContainer.scrollTo({top: 0, behavior: 'instant'});
                    }
                }
            </script>
            """,
            height=0,
        )
        
        st.subheader("📦 GESTIÓN DE ENTREGA Y PAGO")
        st.markdown("**Resumen de artículos solicitados:**")
        for item in st.session_state.carrito:
            icono_p = st.session_state.menu_dinamico[item['producto']]['icono']
            st.text(f"• {icono_p} {item['producto']} x{item['cantidad']} - Subtotal: S/{item['subtotal']:.2f}")
        
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
            # Generación remota blindada del código QR oficial para evitar caídas de servidores locales
            url_qr_remoto = f"https://qrserver.com"
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 25px auto; max-width: 450px; background-color: #1e1e1e; padding: 25px; border-radius: 16px; border: 2px solid #8e44ad; box-shadow: 0px 8px 25px rgba(142, 68, 173, 0.25); text-align: center;">
                    <p style="color: #aaaaaa; font-size: 14px; margin-bottom: 15px; font-weight: bold;">[!] Abriendo ventana de Yape corporativo...</p>
                    <img src="{url_qr_remoto}" style="width: 280px; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px;" />
                    <span style="color: #8e44ad; font-size: 14px; font-weight: bold; letter-spacing: 1px;">🟣 CÓDIGO QR DE YAPE OFICIAL</span>
                </div>
            """, unsafe_allow_html=True)

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
                    detalle_productos_txt += f"{item['cantidad']}x {item['producto']:<18} S/{item['subtotal']:.2f}\n"
                    items_resumen_lista.append(f"{item['cantidad']}x {item['producto']}")
                
                if tiene_delivery:
                    detalle_productos_txt += f"1x Costo de Envío        S/6.00\n"
                    items_resumen_lista.append("1x Delivery")
                
                resumen_articulos_linea = ", ".join(items_resumen_lista)
                tipo_entrega_txt = f"DELIVERY ({direccion_delivery})" if tiene_delivery else "LOCAL"
                
                st.session_state.historial_ordenes.append({
                    "Fecha y Hora": fecha_actual,
                    "Nro. Boleta": correlativo_sunat,
                    "Detalle Artículos": resumen_articulos_linea,
                    "Entrega": tipo_entrega_txt,
                    "Método Pago": metodo_pago,
                    "Total": f"S/{total_con_delivery:.2f}"
                })
                
                # DESCUENTO AUTOMÁTICO DE STOCK EN COCINA EN TIEMPO REAL
                for item in st.session_state.carrito:
                    prod_comprado = item["producto"]
                    cant_comprada = item["cantidad"]
                    st.session_state.menu_dinamico[prod_comprado]["stock"] = max(0, st.session_state.menu_dinamico[prod_comprado].get("stock", 10) - cant_comprada)
                
                # Sincronización física inmediata de las bases de datos transaccionales
                guardar_menu_en_archivo(st.session_state.menu_dinamico)
                guardar_historial_en_archivo(st.session_state.historial_ordenes)
                
                if metodo_pago == "Tarjeta":
                    metodo_pago_txt = f"TARJETA (APROBADA)\nTitular:      {titular_tarjeta}\nNro. Tarjeta: ************{ultimos_digitos}"
                elif metodo_pago == "Yape":
                    metodo_pago_txt = "YAPE (PAGO ELECTRÓNICO)\nVuelto:       S/ 0.00 (Monto exacto)"
                else:
                    metodo_pago_txt = f"EFECTIVO\nEfectivo Recibido: S/{pago_usuario:.2f}\nVuelto:            S/{vuelto:.2f}"
                
                if os.path.exists(RUTA_HTML):
                    with open(RUTA_HTML, "r", encoding="utf-8") as archivo_html:
                        plantilla_contenido = archivo_html.read()
                    
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
            if st.button("🔄 Crear una nueva orden", use_container_width=True, key="btn_nueva_orden_final"):
                st.session_state.carrito = []
                st.session_state.total_acumulado = 0.0
                st.session_state.pedido_guardado = False
                st.session_state.pantalla_actual = "bienvenida"
                st.rerun()
