import streamlit as st
from datetime import datetime, timedelta, timezone  # Reloj oficial para Perú (GMT-5)
import os
import streamlit.components.v1 as components
import pandas as pd  # Motor de analítica para el control de la bitácora
import altair as alt  # Motor gráfico premium para el Dashboard corporativo

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
    # NUEVO: Menú inicial con enlaces URL de fotos de alta velocidad preconfiguradas
    menu_defecto = {
        "Hamburguesa": {
            "precio": 18.0, 
            "icono": "🍔", 
            "disponible": True,
            "foto": "https://unsplash.com"
        },
        "Carne a la parrilla": {
            "precio": 35.0, 
            "icono": "🥩", 
            "disponible": True,
            "foto": "https://unsplash.com"
        },
        "Bebida": {
            "precio": 6.0, 
            "icono": "🥤", 
            "disponible": True,
            "foto": "https://unsplash.com"
        },
        "Combo Buffalo": {
            "precio": 25.0, 
            "icono": "🎁", 
            "disponible": True,
            "foto": "https://unsplash.com"
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

# Enlace web panorámico de alta definición por defecto para la cabecera del local
URL_BANNER_LOCAL = "https://unsplash.com"
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
# FLUJO DE PANTALLAS (MODO ADMINISTRADOR INTEGRAL)
# =========================================================
if es_admin:
    st.markdown("<h1 class='titulo-principal'>📊 PANEL DE AUDITORÍA Y CAJA CHICA</h1>", unsafe_allow_html=True)
    st.info(f"📋 **Reporte Gerencial del Grupo 5** — Sincronizado en tiempo real: {fecha_actual}")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # MÓDULO MULTIMEDIA: Formulario para añadir nuevos productos con foto URL en caliente
    with st.expander("➕ 🛠️ AÑADIR NUEVO PRODUCTO CON FOTO", expanded=False):
        st.caption("Complete los datos para agregar un plato nuevo con su respectiva imagen web al catálogo dinámico.")
        nuevo_nombre = st.text_input("Nombre del nuevo producto:", placeholder="Ej. Alitas BBQ, Papas Nativas...").strip()
        
        col_new1, col_new2 = st.columns(2)
        with col_new1:
            nuevo_precio = st.number_input("Precio de venta (S/):", min_value=0.5, value=10.0, step=0.5)
        with col_new2:
            nuevo_icono = st.text_input("Icono representativo (Emoji):", value="🍟", max_chars=2).strip()
            
        nuevo_link_foto = st.text_input("Enlace URL de la foto del plato:", value="https://unsplash.com", placeholder="Pegue aquí el link de la imagen de internet...").strip()
            
        if st.button("🚀 GUARDAR E INTEGRAR NUEVO PRODUCTO", use_container_width=True):
            if nuevo_nombre:
                if nuevo_nombre not in st.session_state.menu_dinamico:
                    # Inserción en la base de datos viva incluyendo su foto externa
                    st.session_state.menu_dinamico[nuevo_nombre] = {
                        "precio": nuevo_precio,
                        "icono": nuevo_icono,
                        "disponible": True,
                        "foto": nuevo_link_foto
                    }
                    guardar_menu_en_archivo(st.session_state.menu_dinamico)
                    st.success(f"✔ ¡{nuevo_icono} {nuevo_nombre} con foto integrada guardado para siempre!")
                    st.rerun()
                else:
                    st.error("⚠️ Error: Ese producto ya existe en la carta actual.")
            else:
                st.error("⚠️ Error: El nombre del producto no puede estar vacío.")

    # GESTIÓN Y EDICIÓN DE CARTA EXISTENTE (CON SOPORTE MULTIMEDIA)
    st.markdown("### 📝 GESTIÓN DE PRECIOS Y STOCK DISPONIBLE")
    st.caption("Modifique los valores o desactive productos. Se guardarán en el archivo JSON local de forma permanente.")
    
    productos_lista = list(st.session_state.menu_dinamico.keys())
    for i in range(0, len(productos_lista), 2):
        col_ed1, col_ed2 = st.columns(2)
        
        # Producto Izquierda
        p_izq = productos_lista[i]
        with col_ed1:
            st.markdown(f"**{st.session_state.menu_dinamico[p_izq]['icono']} {p_izq}**")
            p_izq_val = st.number_input(f"Precio (S/) - {p_izq}:", min_value=1.0, value=float(st.session_state.menu_dinamico[p_izq]["precio"]), step=0.5, key=f"p_{p_izq}")
            p_izq_disp = st.checkbox("Disponible para venta", value=st.session_state.menu_dinamico[p_izq]["disponible"], key=f"d_{p_izq}")
            st.session_state.menu_dinamico[p_izq] = {
                "precio": p_izq_val, 
                "icono": st.session_state.menu_dinamico[p_izq]["icono"], 
                "disponible": p_izq_disp,
                "foto": st.session_state.menu_dinamico[p_izq].get("foto", "https://unsplash.com")
            }
            
        # Producto Derecha (Si existe en el índice)
        if i + 1 < len(productos_lista):
            p_der = productos_lista[i+1]
            with col_ed2:
                st.markdown(f"**{st.session_state.menu_dinamico[p_der]['icono']} {p_der}**")
                p_der_val = st.number_input(f"Precio (S/) - {p_der}:", min_value=1.0, value=float(st.session_state.menu_dinamico[p_der]["precio"]), step=0.5, key=f"p_{p_der}")
                p_der_disp = st.checkbox("Disponible para venta", value=st.session_state.menu_dinamico[p_der]["disponible"], key=f"d_{p_der}")
                st.session_state.menu_dinamico[p_der] = {
                    "precio": p_der_val, 
                    "icono": st.session_state.menu_dinamico[p_der]["icono"], 
                    "disponible": p_der_disp,
                    "foto": st.session_state.menu_dinamico[p_der].get("foto", "https://unsplash.com")
                }
        st.markdown("---")
        
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
    
    # Reconstrucción Adaptativa del Gráfico Avanzado de Altair
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
    
    # Registro de Auditoría en Tabla Formateada con Pandas
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
    # PANTALLA 1: BIENVENIDA LIMPIA CON TÍTULO GIGANTE Y BANNER DEL LOCAL
    if st.session_state.pantalla_actual == "bienvenida":
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        
        # Banner estético de la fachada/parrilla del restaurante
        st.image(URL_BANNER_LOCAL, caption="🔥 Bienvenidos al templo de la buena carne 🔥", use_container_width=True)
        st.markdown("<br><p style='text-align: center; font-size: 18px;'>¿Desea registrar un nuevo pedido de nuestra deliciosa parrilla?</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🛒 EMPEZAR MI PEDIDO", use_container_width=True):
            st.session_state.pantalla_actual = "catalogo"
            st.rerun()
            
    # PANTALLA 2: CATÁLOGO EN COLUMNAS CON IMÁGENES DINÁMICAS (FOOD CARDS)
    elif st.session_state.pantalla_actual == "catalogo" and not st.session_state.pedido_guardado:
        st.markdown("<h1 class='titulo-principal'>SISTEMA DE PEDIDOS GRAN BUFFALO</h1>", unsafe_allow_html=True)
        st.image(URL_BANNER_LOCAL, use_container_width=True)
        st.text(f"Fecha y hora oficial de Perú (GMT-5): {fecha_actual}\n")
        
        st.subheader("🍽️ SELECCIÓN DE PRODUCTOS (EL MENÚ DE HOY)")
        st.info("Ingrese las cantidades de los productos que desea llevar:")

        col1, col2 = st.columns(2)
        cantidades_ingresadas = {}
        
        # Bucle inteligente que dibuja las tarjetas con fotos según la base de datos JSON
        productos_lista = list(st.session_state.menu_dinamico.keys())
        
        for i in range(len(productos_lista)):
            prod = productos_lista[i]
            info = st.session_state.menu_dinamico[prod]
            
            # Repartir los platos simétricamente
            target_col = col1 if i % 2 == 0 else col2
            
            with target_col:
                if info["disponible"]:
                    # Renderizar la foto del plato arriba con esquinas redondeadas
                    st.markdown(f"""<img src="{info['foto']}" style="width:100%; height:180px; object-fit:cover; border-radius:8px 8px 0px 0px; box-shadow: 0px 4px 8px rgba(0,0,0,0.5); display:block; margin:0; padding:0;">""", unsafe_allow_html=True)
                    
                    # La casilla numérica de Streamlit se acopla abajo con borde verde
                    cantidades_ingresadas[prod] = st.number_input(
                        f"{info['icono']} {prod} — S/{info['precio']:.2f}", 
                        min_value=0, step=1, key=f"cat_{prod}"
                    )
                else:
                    st.markdown(f"""<div style="width:100%; height:180px; background-color:#222; border-radius:8px 8px 0px 0px; display:flex; align-items:center; justify-content:center;"><span style="font-size:40px; filter:grayscale(100%);">{info['icono']}</span></div>""", unsafe_allow_html=True)
                    st.markdown(f"<div style='background-color:#1c1c1c; padding:15px; border-radius:0px 0px 8px 8px; border:1px solid #ff4b4b; text-align:center; margin-bottom:25px;'><p style='color: #ff4b4b; font-weight: bold; margin:0;'>❌ {prod}<br>(AGOTADO POR HOY)</p></div>", unsafe_allow_html=True)

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
                    detalle_productos_txt += f"{item['cantidad']}x {item['producto']:<18} S/{item['subtotal']:.2f}\n"
                    items_resumen_lista.append(f"{item['cantidad']}x {item['producto']}")
                
                if tiene_delivery:
                    detalle_productos_txt += f"1x Costo de Envío        S/6.00\n"
                    items_resumen_lista.append("1x Delivery")
                
                resumen_articulos_linea = ", ".join(items_resumen_lista)
                tipo_entrega_txt = f"DELIVERY ({direccion_delivery})" if tiene_delivery else "LOCAL"
                
                # PERSISTENCIA FIJA: Añadir el nuevo registro a la memoria local de la sesión
                st.session_state.historial_ordenes.append({
                    "Fecha y Hora": fecha_actual,
                    "Nro. Boleta": correlativo_sunat,
                    "Detalle Artículos": resumen_articulos_linea,
                    "Entrega": tipo_entrega_txt,
                    "Método Pago": metodo_pago,
                    "Total": f"S/{total_con_delivery:.2f}"
                })
                
                # MULTI-PERSISTENCIA AUTOMÁTICA: Guardar toda la tabla actualizada en el archivo físico JSON del servidor
                guardar_historial_en_archivo(st.session_state.historial_ordenes)
                
                # PREPARACIÓN DEL TEXTO PARA LA RECOMPOSICIÓN DE LA BOLETA
                if metodo_pago == "Tarjeta":
                    metodo_pago_txt = f"TARJETA (APROBADA)\nTitular:      {titular_tarjeta}\nNro. Tarjeta: ************{ultimos_digitos}"
                elif metodo_pago == "Yape":
                    metodo_pago_txt = "YAPE (PAGO ELECTRÓNICO)\nVuelto:       S/ 0.00 (Monto exacto)"
                else:
                    metodo_pago_txt = f"EFECTIVO\nEfectivo Recibido: S/{pago_usuario:.2f}\nVuelto:            S/{vuelto:.2f}"
                
                # LEER LA PLANTILLA MODULAR HTML EXTERNA
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
            if st.button("🔄 Crear una nueva orden", use_container_width=True):
                st.session_state.carrito = []
                st.session_state.total_acumulado = 0.0
                st.session_state.pedido_guardado = False
                st.session_state.pantalla_actual = "bienvenida"
                st.rerun()
