import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# 1. CONFIGURATION
st.set_page_config(page_title="Défi Carbone", page_icon="🌱", layout="wide")

def get_base64_image(file_name_without_ext):
    current_dir = os.path.dirname(__file__)
    for ext in ["", ".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
        path = os.path.join(current_dir, file_name_without_ext + ext)
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return ""

img_base64 = get_base64_image("image_1")

# 2. CSS CIBLÉ (On protège les composants natifs, on stylise uniquement les fonds)
def set_style(img_b64):
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{img_b64}");
        background-size: cover;
    }}
    
    /* Le style Bleu Ardoise Glossy pour les conteneurs uniquement */
    .block-container {{ background: transparent; }}
    
    [data-testid="stBorderedContainer"], [data-testid="stExpander"] {{
        background-color: rgba(30, 41, 59, 0.85) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px;
    }}
    
    /* On force la couleur des textes pour qu'ils soient lisibles sur le fond sombre */
    h1, h2, h3, p, div, span {{ color: #f1f5f9 !important; }}
    </style>
    """, unsafe_allow_html=True)

set_style(img_base64)

# 3. CHARGEMENT DONNÉES (inchangé)
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

@st.cache_data(ttl=30)
def load_data():
    try:
        raw = pd.read_csv(url, header=None)
        # ... (ton code de chargement reste le même)
        return raw # simplifié pour l'exemple ici
    except: return pd.DataFrame()

# Structure de l'app inchangée pour garder les fonctionnalités
tab1, tab2, tab3 = st.tabs(["📊 Tableau de Bord", "🌱 Empreinte carbone", "📖 Référentiel Éléves"])

with tab1:
    st.title("Défi Carbone")
    # Tes expanders natifs retrouveront leurs flèches ici
    with st.expander("Détails"):
        st.write("Contenu")

with tab2:
    st.header("Graphique")
    # Graphique

with tab3:
    st.header("Référentiel")
