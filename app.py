import streamlit as st
from supabase import create_client, Client

# Configuración de la página
st.set_page_config(
    page_title="VibeSync",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados tipo Red Social (Estilo Facebook/Moderno)
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #0f172a;
        color: white;
        font-weight: 600;
        padding: 0.5rem;
    }
    .stButton>button:hover { background-color: #334155; color: white; }
    
    /* Tarjetas de perfil estilo muro */
    .profile-card {
        background-color: white;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }
    .badge {
        display: inline-block;
        background-color: #e2e8f0;
        color: #1e293b;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
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
st.markdown("<h1 style='text-align: center; color: #0f172a;'>⚡ VibeSync</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Conecta con amigos, comparte tu vibra y organiza los mejores botes</p>", unsafe_allow_html=True)
st.divider()

# Si el usuario NO ha iniciado sesión
if st.session_state.user is None:
    tab_login, tab_signup = st.tabs(["🔑 Iniciar Sesión", "✨ Registrarse"])
    
    with tab_login:
        st.subheader("Bienvenido de nuevo")
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
        st.subheader("Crea tu cuenta social")
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
                        supabase.table("profiles").insert({
                            "id": response.user.id,
                            "username": new_username,
                            "full_name": new_fullname,
                            "taste_dna": {"fitness": "Gym / Pesas", "music": "Techno / House", "tech": "Python / Streamlit"}
                        }).execute()
                        st.success("¡Cuenta creada con éxito! Ya puedes iniciar sesión en la otra pestaña.")
                except Exception as e:
                    st.error(f"Error en el registro: {e}")

# Si el usuario YA inició sesión (Interfaz Social Tipo Perfil)
else:
    user_id = st.session_state.user.id
    
    # Obtener perfil actual
    profile_data = supabase.table("profiles").select("*").eq("id", user_id).execute()
    current_profile = profile_data.data[0] if profile_data.data else {}
    
    # Barra superior de navegación / usuario
    col_info, col_logout = st.columns([4, 1])
    with col_info:
        st.write(f"Conectado como: **{current_profile.get('full_name', 'Usuario')}** `@{current_profile.get('username', 'user')}`")
    with col_logout:
        if st.button("Cerrar Sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
            
    st.divider()

    # Pestañas principales de la Red Social
    tab_perfil, tab_amigos, tab_eventos = st.tabs(["👤 Mi Muro y Perfil", "👥 Comunidad de Amigos", "🎉 Eventos & Botes"])
    
    with tab_perfil:
        # Estilo de Tarjeta de Perfil Tipo Red Social
        st.markdown(f"""
            <div class='profile-card'>
                <h2>{current_profile.get('full_name', 'Mi Nombre')}</h2>
                <p style='color: #64748b; margin-top: -10px;'>@{current_profile.get('username', 'usuario')}</p>
                <hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;'>
                <h4>🧬 Mi Taste DNA (ADN de Gustos)</h4>
        """, unsafe_allow_html=True)
        
        taste_dna = current_profile.get("taste_dna", {})
        st.markdown(f"""
                <div>
                    <span class='badge'>🏋️ Deporte: {taste_dna.get('fitness', 'N/A')}</span>
                    <span class='badge'>🎵 Música: {taste_dna.get('music', 'N/A')}</span>
                    <span class='badge'>💻 Tech: {taste_dna.get('tech', 'N/A')}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulario para actualizar el Taste DNA
        with st.expander("✏️ Editar mi Taste DNA e Intereses"):
            with st.form("dna_form"):
                fit = st.selectbox("Fitness / Deporte", ["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"], 
                                   index=["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"].index(taste_dna.get("fitness", "Gym / Pesas")) if taste_dna.get("fitness") in ["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"] else 0)
                
                mus = st.selectbox("Música Favorita", ["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"],
                                   index=["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"].index(taste_dna.get("music", "Techno / House")) if taste_dna.get("music") in ["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"] else 0)
                
                tch = st.selectbox("Tecnología / Pasatiempo", ["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"],
                                   index=["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"].index(taste_dna.get("tech", "Python / Streamlit")) if taste_dna.get("tech") in ["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"] else 0)
                
                save_dna = st.form_submit_button("Guardar Cambios en mi Perfil")
                
                if save_dna:
                    updated_dna = {"fitness": fit, "music": mus, "tech": tch}
                    supabase.table("profiles").update({"taste_dna": updated_dna}).eq("id", user_id).execute()
                    st.success("¡Perfil actualizado con éxito!")
                    st.rerun()

    with tab_amigos:
        st.subheader("👥 Comunidad y Amigos en VibeSync")
        st.markdown("Descubre los perfiles y gustos de otros miembros de la red.")
        
        all_profiles = supabase.table("profiles").select("username, full_name, taste_dna").neq("id", user_id).execute()
        
        if all_profiles.data:
            for p in all_profiles.data:
                dna = p.get("taste_dna", {})
                st.markdown(f"""
                    <div class='profile-card'>
                        <h3>👤 {p.get('full_name')} <span style='font-size: 0.9rem; color: #64748b;'>@{p.get('username')}</span></h3>
                        <div style='margin-top: 10px;'>
                            <span class='badge'>🏋️ {dna.get('fitness', 'N/A')}</span>
                            <span class='badge'>🎵 {dna.get('music', 'N/A')}</span>
                            <span class='badge'>💻 {dna.get('tech', 'N/A')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aún no hay más usuarios en la red. ¡Invita a tus conocidos a unirse!")

    with tab_eventos:
        st.subheader("🎉 Eventos y Botes Grupales")
        st.info("📌 Próximo módulo: Creación de fiestas, reuniones y administración de botes automatizados.")
