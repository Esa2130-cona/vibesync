import streamlit as st
from supabase import create_client, Client

# Configuración de la página
st.set_page_config(
    page_title="VibeSync",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Profesionales (Diseño Fluido y Moderno)
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
    
    /* Tarjetas flotantes modernas sin bordes rígidos */
    .modern-card {
        background: #ffffff;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
    }
    .modern-card:hover {
        box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.08);
    }
    
    /* Insignias / Badges modernos */
    .badge {
        display: inline-flex;
        align-items: center;
        background-color: #f1f5f9;
        color: #334155;
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Avatar circular con borde elegante */
    .avatar-img {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border: 4px solid #ffffff;
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
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.05rem; margin-top: -10px;'>Conecta con amigos, comparte tu vibra y organiza los mejores botes</p>", unsafe_allow_html=True)
st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)

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
    
    # Barra superior moderna
    col_info, col_logout = st.columns([4, 1])
    with col_info:
        st.markdown(f"<span style='color: #475569;'>Hola de nuevo,</span> <strong style='color: #0f172a;'>{current_profile.get('full_name', 'Usuario')}</strong> <code style='background: #e2e8f0; padding: 2px 6px; border-radius: 6px;'>@{current_profile.get('username', 'user')}</code>", unsafe_allow_html=True)
    with col_logout:
        if st.button("Cerrar Sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
            
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

    # Pestañas principales con diseño flotante
    tab_perfil, tab_amigos, tab_eventos = st.tabs(["👤 Mi Perfil y Muro", "👥 Comunidad", "🎉 Eventos & Botes"])
    
    with tab_perfil:
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        avatar = current_profile.get('avatar_url') or "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
        
        # Contenedor principal del perfil en tarjeta flotante
        st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
        col_avatar, col_datos = st.columns([1, 4])
        with col_avatar:
            st.markdown(f"<img src='{avatar}' class='avatar-img'>", unsafe_allow_html=True)
        with col_datos:
            st.markdown(f"<h2 style='margin: 0; color: #0f172a; font-weight: 700;'>{current_profile.get('full_name', 'Mi Nombre')}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #64748b; margin: 2px 0 12px 0; font-weight: 500;'>@{current_profile.get('username', 'usuario')}</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 0; border-top: 1px solid #f1f5f9; margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1e293b; font-size: 1.1rem; margin-bottom: 15px;'>🧬 Mi Taste DNA (ADN de Gustos)</h4>", unsafe_allow_html=True)
        
        taste_dna = current_profile.get("taste_dna", {})
        st.markdown(f"""
            <div>
                <span class='badge'>🏋️ Deporte: <b>{taste_dna.get('fitness', 'N/A')}</b></span>
                <span class='badge'>🎵 Música: <b>{taste_dna.get('music', 'N/A')}</b></span>
                <span class='badge'>💻 Tech: <b>{taste_dna.get('tech', 'N/A')}</b></span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Formulario de edición estilizado
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
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0f172a; font-weight: 700; margin-bottom: 5px;'>👥 Comunidad y Amigos</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; margin-bottom: 25px;'>Descubre los perfiles y gustos de otros miembros de la red.</p>", unsafe_allow_html=True)
        
        all_profiles = supabase.table("profiles").select("username, full_name, avatar_url, taste_dna").neq("id", user_id).execute()
        
        if all_profiles.data:
            for p in all_profiles.data:
                dna = p.get("taste_dna", {})
                p_avatar = p.get('avatar_url') or "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
                
                st.markdown(f"""
                    <div class='modern-card'>
                        <table style='width:100%; border:none;'>
                            <tr>
                                <td style='width: 100px; border:none; vertical-align: middle;'>
                                    <img src='{p_avatar}' class='avatar-img'>
                                </td>
                                <td style='border:none; vertical-align: middle; padding-left: 10px;'>
                                    <h3 style='margin:0; color: #0f172a; font-weight: 700;'>{p.get('full_name')}</h3>
                                    <p style='color: #64748b; margin:2px 0 10px 0; font-weight: 500;'>@{p.get('username')}</p>
                                    <div>
                                        <span class='badge'>🏋️ {dna.get('fitness', 'N/A')}</span>
                                        <span class='badge'>🎵 {dna.get('music', 'N/A')}</span>
                                        <span class='badge'>💻 {dna.get('tech', 'N/A')}</span>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aún no hay más usuarios en la red. ¡Invita a tus conocidos a unirse!")

    with tab_eventos:
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='modern-card'><h3>🎉 Eventos y Botes Grupales</h3><p style='color: #64748b;'>Próximo módulo en desarrollo: Creación de fiestas, reuniones y administración de botes automatizados.</p></div>", unsafe_allow_html=True)
