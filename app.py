import streamlit as st
from supabase import create_client, Client

# Configuración de la página
st.set_page_config(
    page_title="VibeSync",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS minimalistas
st.markdown("""
    <style>
    .main { background-color: #FAFAFA; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #0f172a;
        color: white;
        font-weight: 600;
        padding: 0.6rem;
    }
    .stButton>button:hover { background-color: #334155; color: white; }
    </style>
""", unsafe_allow_html=True)

# Conexión a Supabase usando Secrets de Streamlit Cloud
SUPABASE_URL = st.secrets["https://jemlrjrbbfeezojuuqye.supabase.co"]
SUPABASE_KEY = st.secrets["sb_publishable_R7f_854Ol9n5JeGiISvnSA_ImMTeW0h"]

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# --- GESTIÓN DE SESIÓN EN STREAMLIT ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #0f172a;'>⚡ VibeSync</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Tu red social de eventos y regalos basada en Taste DNA</p>", unsafe_allow_html=True)
st.divider()

# Si el usuario NO ha iniciado sesión, mostramos pantalla de Acceso / Registro
if st.session_state.user is None:
    tab_login, tab_signup = st.tabs(["🔑 Iniciar Sesión", "✨ Registrarse"])
    
    with tab_login:
        st.subheader("Bienvenido de nuevo")
        with st.form("login_form"):
            email = st.text_input("Correo Electrónico")
            password = st.text_input("Contraseña", type="password")
            submit_login = st.form_submit_button("Entrar")
            
            if submit_login:
                try:
                    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = response.user
                    st.success("¡Inicio de sesión exitoso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al iniciar sesión: {e}")
                    
    with tab_signup:
        st.subheader("Crea tu cuenta en VibeSync")
        with st.form("signup_form"):
            new_email = st.text_input("Correo Electrónico")
            new_password = st.text_input("Crea una Contraseña", type="password")
            new_username = st.text_input("Nombre de Usuario (ej. esau_clemente)")
            new_fullname = st.text_input("Nombre Completo")
            submit_signup = st.form_submit_button("Registrarse")
            
            if submit_signup:
                try:
                    # 1. Registrar usuario en Auth de Supabase
                    response = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    
                    if response.user:
                        # 2. Crear su registro inicial en la tabla 'profiles'
                        supabase.table("profiles").insert({
                            "id": response.user.id,
                            "username": new_username,
                            "full_name": new_fullname,
                            "taste_dna": {"fitness": "General", "music": "Indefinido", "tech": "General"}
                        }).execute()
                        
                        st.success("¡Cuenta creada con éxito! Ya puedes iniciar sesión.")
                except Exception as e:
                    st.error(f"Error en el registro: {e}")

# Si el usuario YA inició sesión, mostramos la plataforma social
else:
    user_id = st.session_state.user.id
    
    # Obtener perfil actual de la base de datos
    profile_data = supabase.table("profiles").select("*").eq("id", user_id).execute()
    current_profile = profile_data.data[0] if profile_data.data else {}
    
    # Barra lateral o superior para control de sesión
    col_info, col_logout = st.columns([4, 1])
    with col_info:
        st.write(f"👋 Hola, **{current_profile.get('full_name', 'Usuario')}** (@{current_profile.get('username', 'user')})")
    with col_logout:
        if st.button("Cerrar Sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
            
    st.divider()

    # Pestañas principales de la red social
    tab_perfil, tab_amigos, tab_eventos = st.tabs(["🧬 Mi Taste DNA", "👥 Amigos", "🎉 Eventos & Botes"])
    
    with tab_perfil:
        st.subheader("Configura tu ADN de Gustos")
        st.markdown("Esto ayuda a que tus amigos sepan exactamente qué regalarte o qué planes armar contigo.")
        
        taste_dna = current_profile.get("taste_dna", {})
        
        with st.form("dna_form"):
            fit = st.selectbox("Fitness / Deporte", ["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"], 
                               index=["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"].index(taste_dna.get("fitness", "Gym / Pesas")) if taste_dna.get("fitness") in ["Gym / Pesas", "Running", "Artes Marciales", "Yoga", "Ninguno"] else 0)
            
            mus = st.selectbox("Música Favorita", ["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"],
                               index=["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"].index(taste_dna.get("music", "Techno / House")) if taste_dna.get("music") in ["Techno / House", "Rock", "Pop", "Electrónica", "Hip Hop"] else 0)
            
            tch = st.selectbox("Tecnología / Pasatiempo", ["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"],
                               index=["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"].index(taste_dna.get("tech", "Python / Streamlit")) if taste_dna.get("tech") in ["Python / Streamlit", "Servidores / Docker", "Videojuegos", "Lectura"] else 0)
            
            save_dna = st.form_submit_button("Actualizar Taste DNA")
            
            if save_dna:
                updated_dna = {"fitness": fit, "music": mus, "tech": tch}
                supabase.table("profiles").update({"taste_dna": updated_dna}).eq("id", user_id).execute()
                st.success("¡Taste DNA actualizado correctamente!")
                st.rerun()

    with tab_amigos:
        st.subheader("Directorio de Amigos")
        st.markdown("Busca perfiles de la comunidad para ver sus gustos y conectarte.")
        
        # Mostrar lista de otros usuarios registrados
        all_profiles = supabase.table("profiles").select("username, full_name, taste_dna").neq("id", user_id).execute()
        
        if all_profiles.data:
            for p in all_profiles.data:
                with st.container():
                    st.markdown(f"### 👤 {p.get('full_name')} `@{p.get('username')}`")
                    dna = p.get("taste_dna", {})
                    st.caption(f"🏋️ Deporte: {dna.get('fitness', 'N/A')} | 🎵 Música: {dna.get('music', 'N/A')} | 💻 Tech: {dna.get('tech', 'N/A')}")
                    st.divider()
        else:
            st.info("Aún no hay más usuarios registrados. ¡Invita a tus amigos a unirse a VibeSync!")

    with tab_eventos:
        st.subheader("Próximos Eventos y Botes Grupales")
        st.info("📌 **Próximo módulo en desarrollo:** Creación de eventos personalizados y automatización de botes para regalos en grupo.")
