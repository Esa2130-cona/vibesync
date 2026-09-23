import streamlit as st
from supabase import create_client, Client

# Configuración de la página (Estilo Minimalista)
st.set_page_config(
    page_title="VibeSync",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para mantener un look limpio y moderno
st.markdown("""
    <style>
    .main {
        background-color: #FAFAFA;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #0f172a;
        color: white;
        font-weight: 600;
        padding: 0.6rem;
    }
    .stButton>button:hover {
        background-color: #334155;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar conexión a Supabase (Usa tus credenciales de Settings > API)
SUPABASE_URL = "https://jemlrjrbbfeezojuuqye.supabase.co"
SUPABASE_KEY = "sb_publishable_R7f_854Ol9n5JeGiISvnSA_ImMTeW0h"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_connection()
except Exception as e:
    st.error(f"Error al conectar con Supabase: {e}")

# --- ENCABEZADO DE LA APP ---
st.markdown("<h1 style='text-align: center; color: #0f172a;'>⚡ VibeSync</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Organiza fiestas y regalos según el ADN de tus amigos</p>", unsafe_allow_html=True)
st.divider()

# --- NAVEGACIÓN SIMPLE (Pestañas) ---
tab_perfil, tab_evento = st.tabs(["👤 Mi Perfil & ADN", "🎉 Bote Automático"])

with tab_perfil:
    st.subheader("Tu ADN de Celebración")
    
    # Formulario rápido para simular el perfil
    with st.form("profile_form"):
        username = st.text_input("Usuario", "esau_clemente")
        full_name = st.text_input("Nombre Completo", "Esaú Clemente")
        
        st.markdown("### Tus Gustos Principales")
        col1, col2 = st.columns(2)
        with col1:
            fitness_taste = st.selectbox("Fitness / Deporte", ["Gym / Pesas", "Running", "Artes Marciales", "Ninguno"])
            music_taste = st.selectbox("Música", ["Techno / Deep House", "Rock", "Pop", "Electrónica"])
        with col2:
            tech_taste = st.selectbox("Tecnología / Stack", ["Python / Streamlit", "TrueNAS / Docker", "Desarrollo Web", "Sistemas"])
            coffee_taste = st.selectbox("Bebida Favorita", ["Café de Especialidad", "Cerveza Artesanal", "Matcha", "Agua"])
            
        submitted = st.form_submit_button("Guardar Preferencias")
        
        if submitted:
            taste_data = {
                "fitness": fitness_taste,
                "music": music_taste,
                "tech": tech_taste,
                "drink": coffee_taste
            }
            try:
                # Insertar o actualizar en Supabase
                data = {
                    "username": username,
                    "full_name": full_name,
                    "taste_dna": taste_data
                }
                supabase.table("profiles").upsert(data, on_conflict="username").execute()
                st.success("¡Preferencias guardadas con éxito en tu base de datos!")
            except Exception as e:
                st.error(f"Hubo un error al guardar: {e}")

with tab_evento:
    st.subheader("Gestión de Bote Grupal")
    st.markdown("Visualiza y coopera para el regalo o evento del grupo.")
    
    # Tarjeta de simulación del bote
    st.info("📌 **Evento Activo:** Cumpleaños de Carlos\n\n🎯 **Meta del Regalo:** $5,000.00 MXN\n💰 **Recaudado hasta ahora:** $3,500.00 MXN")
    
    # Barra de progreso visual
    st.progress(0.7, text="Progreso del Regalo: 70%")
    
    # Botón de cooperación
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Participantes Confirmados", value="12 personas")
    with col_b:
        st.metric(label="Tu Cooperación Sugerida", value="$291.66 MXN")
        
    if st.button("💳 Cooperar Ahora ($291.66 MXN)"):
        st.balloons()
        st.success("¡Gracias por tu aportación! El bote se ha actualizado.")
