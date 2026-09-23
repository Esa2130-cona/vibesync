import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="VibeSync",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Profesionales
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main { background-color: #f8fafc; }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        font-weight: 600;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.25);
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
    }
    
    .modern-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        background-color: #f1f5f9;
        color: #334155;
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid #e2e8f0;
    }
    
    .avatar-img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border: 3px solid #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Conexión directa a Supabase
SUPABASE_URL = "https://jemlrjrbbfeezojuuqye.supabase.co"
SUPABASE_KEY = "sb_publishable_R7f_854Ol9n5JeGiISvnSA_ImMTeW0h"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# --- GESTIÓN DE SESIÓN ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- ENCABEZADO PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 700; letter-spacing: -1px;'>⚡ VibeSync</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.05rem; margin-top: -10px;'>Red social privada, eventos y chat con amigos</p>", unsafe_allow_html=True)
st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

# Si el usuario NO ha iniciado sesión
if st.session_state.user is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Iniciar Sesión", "✨ Registrarse"])
        
        with tab_login:
            st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Correo Electrónico")
                password = st.text_input("Contraseña", type="password")
                submit_login = st.form_submit_button("Entrar a VibeSync")
                
                if submit_login:
                    try:
                        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = response.user
                        st.success("¡Bienvenido de vuelta!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al iniciar sesión: {e}")
                        
        with tab_signup:
            st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
            with st.form("signup_form"):
                new_email = st.text_input("Correo Electrónico")
                new_password = st.text_input("Crea una Contraseña", type="password")
                new_username = st.text_input("Nombre de Usuario (ej. esau_clemente)")
                new_fullname = st.text_input("Nombre Completo")
                submit_signup = st.form_submit_button("Crear Cuenta")
                
                if submit_signup:
                    try:
                        response = supabase.auth.sign_up({"email": new_email, "password": new_password})
                        if response.user:
                            default_avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={new_username}"
                            supabase.table("profiles").insert({
                                "id": response.user.id,
                                "username": new_username,
                                "full_name": new_fullname,
                                "avatar_url": default_avatar,
                                "taste_dna": {"fitness": "Gym / Pesas", "music": "Techno / House", "tech": "Python / Streamlit"}
                            }).execute()
                            st.success("¡Cuenta creada con éxito! Ya puedes iniciar sesión.")
                    except Exception as e:
                        st.error(f"Error en el registro: {e}")

# Si el usuario YA inició sesión
else:
    user_id = st.session_state.user.id
    
    profile_data = supabase.table("profiles").select("*").eq("id", user_id).execute()
    current_profile = profile_data.data[0] if profile_data.data else {}
    
    col_info, col_logout = st.columns([4, 1])
    with col_info:
        st.markdown(f"<span style='color: #475569;'>Hola,</span> <strong style='color: #0f172a;'>{current_profile.get('full_name', 'Usuario')}</strong> <code style='background: #e2e8f0; padding: 2px 6px; border-radius: 6px;'>@{current_profile.get('username', 'user')}</code>", unsafe_allow_html=True)
    with col_logout:
        if st.button("Cerrar Sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
            
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

    # Pestañas principales de la red social
    tab_perfil, tab_amigos, tab_eventos, tab_chat = st.tabs(["👤 Mi Perfil", "👥 Buscar & Amigos", "🎉 Mis Eventos", "💬 Chat Privado"])
    
    with tab_perfil:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        avatar = current_profile.get('avatar_url') or "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
        
        st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
        col_avatar, col_datos = st.columns([1, 4])
        with col_avatar:
            st.markdown(f"<img src='{avatar}' class='avatar-img'>", unsafe_allow_html=True)
        with col_datos:
            st.markdown(f"<h2 style='margin: 0; color: #0f172a; font-weight: 700;'>{current_profile.get('full_name', 'Mi Nombre')}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #64748b; margin: 2px 0 10px 0; font-weight: 500;'>@{current_profile.get('username', 'usuario')}</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 0; border-top: 1px solid #f1f5f9; margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1e293b; font-size: 1.05rem; margin-bottom: 12px;'>🧬 Mi Taste DNA (ADN de Gustos)</h4>", unsafe_allow_html=True)
        
        taste_dna = current_profile.get("taste_dna", {})
        st.markdown(f"""
            <div>
                <span class='badge'>🏋️ Deporte: <b>{taste_dna.get('fitness', 'N/A')}</b></span>
                <span class='badge'>🎵 Música: <b>{taste_dna.get('music', 'N/A')}</b></span>
                <span class='badge'>💻 Tech: <b>{taste_dna.get('tech', 'N/A')}</b></span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        with st.expander("✏️ Editar mi Perfil y Taste DNA"):
            with st.form("dna_form"):
                new_avatar = st.text_input("URL de tu Foto / Avatar", value=current_profile.get('avatar_url', ''))
                
                fit = st.selectbox("Fitness / Deporte", ["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"], 
                                   index=["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"].index(taste_dna.get("fitness", "Gym / Pesas")) if taste_dna.get("fitness") in ["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"] else 0)
                
                mus = st.selectbox("Música Favorita", ["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"],
                                   index=["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"].index(taste_dna.get("music", "Techno / House")) if taste_dna.get("music") in ["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"] else 0)
                
                tch = st.selectbox("Tecnología / Pasatiempo", ["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"],
                                   index=["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"].index(taste_dna.get("tech", "Python / Streamlit")) if taste_dna.get("tech") in ["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"] else 0)
                
                save_dna = st.form_submit_button("Guardar Cambios")
                
                if save_dna:
                    updated_dna = {"fitness": fit, "music": mus, "tech": tch}
                    supabase.table("profiles").update({
                        "taste_dna": updated_dna,
                        "avatar_url": new_avatar
                    }).eq("id", user_id).execute()
                    st.success("¡Perfil actualizado con éxito!")
                    st.rerun()

    with tab_amigos:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🔍 Buscar Usuarios", "🤝 Mis Amigos", "📥 Solicitudes Pendientes"])
        
        with sub_tab1:
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            busqueda = st.text_input("Buscar por nombre de usuario o `@usuario`")
            
            if busqueda:
                # Buscar usuarios que coincidan
                found = supabase.table("profiles").select("*").ilike("username", f"%{busqueda}%").neq("id", user_id).execute()
                
                if found.data:
                    for u in found.data:
                        u_id = u.get("id")
                        u_avatar = u.get("avatar_url") or "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
                        
                        # Revisar si ya son amigos o hay solicitud pendiente
                        existing = supabase.table("friendships").select("*").or_(
                            f"and(requester_id.eq.{user_id},receiver_id.eq.{u_id}),and(requester_id.eq.{u_id},receiver_id.eq.{user_id})"
                        ).execute()
                        
                        estado_btn = "Agregar Amigo"
                        ya_enviado = False
                        
                        if existing.data:
                            status = existing.data[0].get("status")
                            if status == "accepted":
                                estado_btn = "✅ Amigos"
                                ya_enviado = True
                            elif status == "pending":
                                estado_btn = "⏳ Solicitud Pendiente"
                                ya_enviado = True

                        col_u1, col_u2 = st.columns([3, 1])
                        with col_u1:
                            st.markdown(f"""
                                <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 10px;'>
                                    <img src='{u_avatar}' style='width: 45px; height: 45px; border-radius: 50%; object-fit: cover;'>
                                    <div>
                                        <h4 style='margin: 0; color: #0f172a;'>{u.get('full_name')}</h4>
                                        <p style='margin: 0; color: #64748b; font-size: 0.85rem;'>@{u.get('username')}</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        with col_u2:
                            if not ya_enviado:
                                if st.button("Agregar", key=f"add_{u_id}"):
                                    supabase.table("friendships").insert({
                                        "requester_id": user_id,
                                        "receiver_id": u_id,
                                        "status": "pending"
                                    }).execute()
                                    st.success("¡Solicitud enviada!")
                                    st.rerun()
                            else:
                                st.write(f"*{estado_btn}*")
                else:
                    st.info("No se encontraron usuarios con ese nombre.")

        with sub_tab2:
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            # Buscar amistades aceptadas
            amigos_q = supabase.table("friendships").select("*").or_(
                f"requester_id.eq.{user_id},receiver_id.eq.{user_id}"
            ).eq("status", "accepted").execute()
            
            if amigos_q.data:
                for rel in amigos_q.data:
                    # Identificar el ID del amigo
                    amigo_id = rel.get("receiver_id") if rel.get("requester_id") == user_id else rel.get("requester_id")
                    
                    # Obtener perfil del amigo
                    amigo_perfil = supabase.table("profiles").select("*").eq("id", amigo_id).execute()
                    if amigo_perfil.data:
                        ap = amigo_perfil.data[0]
                        ap_avatar = ap.get("avatar_url") or "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
                        dna = ap.get("taste_dna", {})
                        
                        # Buscar eventos de este amigo (privacidad de amigos)
                        evs = supabase.table("events").select("*").eq("host_id", amigo_id).execute()
                        eventos_str = ""
                        if evs.data:
                            for ev in evs.data:
                                eventos_str += f"<p style='font-size:0.8rem; color:#64748b; margin:2px 0;'>🎉 {ev.get('title')} ({ev.get('event_date', '')})</p>"
                        else:
                            eventos_str = "<p style='font-size:0.8rem; color:#94a3b8;'>Sin eventos activos.</p>"

                        st.markdown(f"""
                            <div class='modern-card'>
                                <table style='width:100%; border:none;'>
                                    <tr>
                                        <td style='width: 80px; border:none; vertical-align: top;'>
                                            <img src='{ap_avatar}' style='width:65px; height:65px; border-radius:50%; object-fit:cover;'>
                                        </td>
                                        <td style='border:none; vertical-align: top;'>
                                            <h4 style='margin:0; color:#0f172a;'>{ap.get('full_name')}</h4>
                                            <p style='margin:2px 0 8px 0; color:#64748b; font-size:0.85rem;'>@{ap.get('username')}</p>
                                            <div>
                                                <span class='badge'>🏋️ {dna.get('fitness', 'N/A')}</span>
                                                <span class='badge'>🎵 {dna.get('music', 'N/A')}</span>
                                            </div>
                                            <div style='margin-top: 10px; border-top: 1px solid #f1f5f9; padding-top: 8px;'>
                                                <p style='font-size:0.82rem; font-weight:600; color:#475569; margin-bottom:4px;'>Sus Eventos:</p>
                                                {eventos_str}
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Aún no tienes amigos agregados. ¡Busca a alguien en la pestaña de búsqueda!")

        with sub_tab3:
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            # Solicitudes donde el usuario es receptor y el estado es pending
            pendientes = supabase.table("friendships").select("*").eq("receiver_id", user_id).eq("status", "pending").execute()
            
            if pendientes.data:
                for req in pendientes.data:
                    req_id = req.get("id")
                    sender_id = req.get("requester_id")
                    
                    sender_info = supabase.table("profiles").select("*").eq("id", sender_id).execute()
                    if sender_info.data:
                        si = sender_info.data[0]
                        si_avatar = si.get("avatar_url") or "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
                        
                        col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
                        with col_p1:
                            st.markdown(f"**{si.get('full_name')}** `@{si.get('username')}` te envió una solicitud.")
                        with col_p2:
                            if st.button("Aceptar", key=f"acc_{req_id}"):
                                supabase.table("friendships").update({"status": "accepted"}).eq("id", req_id).execute()
                                st.success("¡Solicitud aceptada!")
                                st.rerun()
                        with col_p3:
                            if st.button("Rechazar", key=f"rej_{req_id}"):
                                supabase.table("friendships").delete().eq("id", req_id).execute()
                                st.info("Solicitud rechazada.")
                                st.rerun()
            else:
                st.info("No tienes solicitudes de amistad pendientes.")

    with tab_eventos:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0f172a; font-weight: 700; margin-bottom: 5px;'>🎉 Mis Eventos Privados</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; margin-bottom: 20px;'>Aquí solo tú administras las reuniones o botes que organizas.</p>", unsafe_allow_html=True)
        
        with st.expander("➕ Organizar Nuevo Evento"):
            with st.form("event_form"):
                ev_title = st.text_input("Título del Evento (ej. Carne Asada / Rodada / Cumpleaños)")
                
                ubicacion_opcion = st.selectbox("Lugar de Encuentro", [
                    "🏡 Casa / Terraza Principal", 
                    "🏋️ Gimnasio Local", 
                    "🏞️ Parque Nacional El Tepozteco", 
                    "📍 Otro lugar personalizado..."
                ])
                
                if ubicacion_opcion == "📍 Otro lugar personalizado...":
                    ev_location = st.text_input("Escribe la ubicación exacta")
                else:
                    ev_location = ubicacion_opcion

                col_d, col_h = st.columns(2)
                with col_d:
                    fecha_sel = st.date_input("Fecha del Evento")
                with col_h:
                    hora_sel = st.time_input("Hora del Encuentro")
                
                submit_event = st.form_submit_button("Publicar mi Evento")
                
                if submit_event:
                    try:
                        fecha_hora_combinada = f"{fecha_sel} {hora_sel.strftime('%H:%M')}"
                        supabase.table("events").insert({
                            "title": ev_title,
                            "location": ev_location,
                            "event_date": fecha_hora_combinada,
                            "host_id": user_id
                        }).execute()
                        st.success("¡Evento publicado con éxito!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al crear el evento: {e}")
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # Mostrar ÚNICAMENTE los eventos creados por el usuario actual
        my_events = supabase.table("events").select("*").eq("host_id", user_id).execute()
        
        if my_events.data:
            for ev in my_events.data:
                ev_id = ev.get('id')
                st.markdown(f"""
                    <div class='modern-card'>
                        <h3 style='margin:0; color: #0f172a; font-weight: 700;'>🎉 {ev.get('title')}</h3>
                        <p style='color: #64748b; margin: 8px 0 5px 0;'>📍 <b>Lugar:</b> {ev.get('location', 'Por definir')}</p>
                        <p style='color: #64748b; margin: 0 0 10px 0;'>📅 <b>Fecha y Hora:</b> {ev.get('event_date', 'Próximamente')}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🗑️ Borrar este Evento", key=f"del_me_{ev_id}"):
                    supabase.table("events").delete().eq("id", ev_id).execute()
                    st.success("¡Evento eliminado!")
                    st.rerun()
                st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        else:
            st.info("No has organizado ningún evento todavía. ¡Crea el tuyo arriba!")

    with tab_chat:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0f172a; font-weight: 700; margin-bottom: 5px;'>💬 Chat Privado con Amigos</h3>", unsafe_allow_html=True)
        
        # Obtener lista de amigos aceptados para chatear
        amigos_chat = supabase.table("friendships").select("*").or_(
            f"requester_id.eq.{user_id},receiver_id.eq.{user_id}"
        ).eq("status", "accepted").execute()
        
        if amigos_chat.data:
            amigos_ids = []
            for rel in amigos_chat.data:
                a_id = rel.get("receiver_id") if rel.get("requester_id") == user_id else rel.get("requester_id")
                amigos_ids.append(a_id)
            
            # Obtener datos de los amigos
            amigos_profiles = supabase.table("profiles").select("id, full_name, username").in_("id", amigos_ids).execute()
            
            if amigos_profiles.data:
                # Diccionario para selector
                amigos_dict = {f"{p.get('full_name')} (@{p.get('username')})": p.get('id') for p in amigos_profiles.data}
                
                seleccion_amigo = st.selectbox("Selecciona un amigo para chatear", list(amigos_dict.keys()))
                destinatario_id = amigos_dict[seleccion_amigo]
                
                st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
                
                # Cargar historial de mensajes entre ambos usuarios
                mensajes_q = supabase.table("messages").select("*").or_(
                    f"and(sender_id.eq.{user_id},receiver_id.eq.{destinatario_id}),and(sender_id.eq.{destinatario_id},receiver_id.eq.{user_id})"
                ).order("created_at", desc=False).execute()
                
                # Contenedor visual de chat
                chat_container = st.container()
                with chat_container:
                    if mensajes_q.data:
                        for m in mensajes_q.data:
                            is_me = m.get("sender_id") == user_id
                            alineacion = "right" if is_me else "left"
                            color_fondo = "#0f172a" if is_me else "#e2e8f0"
                            color_texto = "white" if is_me else "#1e293b"
                            
                            st.markdown(f"""
                                <div style='text-align: {alineacion}; margin-bottom: 10px;'>
                                    <div style='display: inline-block; background: {color_fondo}; color: {color_texto}; padding: 10px 16px; border-radius: 14px; max-width: 75%; text-align: left;'>
                                        {m.get('content')}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Aún no hay mensajes en este chat. ¡Escribe el primero!")
                
                st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
                
                # Input para enviar nuevo mensaje
                with st.form("chat_form", clear_on_submit=True):
                    nuevo_mensaje = st.text_input("Escribe tu mensaje...")
                    enviar_msg = st.form_submit_button("Enviar Mensaje")
                    
                    if enviar_msg and nuevo_mensaje.strip():
                        supabase.table("messages").insert({
                            "sender_id": user_id,
                            "receiver_id": destinatario_id,
                            "content": nuevo_mensaje.strip()
                        }).execute()
                        st.rerun()
            else:
                st.info("No se pudieron cargar los datos de tus amigos.")
        else:
            st.info("Necesitas tener al menos un amigo con la solicitud aceptada para poder chatear.")
