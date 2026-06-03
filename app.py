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

# 2. DESIGN FINAL (Cadre flottant avec marges)
st.markdown(f"""
<style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
    }}
    
    /* Le cadre global devient flottant avec des marges */
    .main .block-container {{
        background-color: rgba(228, 235, 245, 0.58) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.5) !important;
        border-radius: 20px !important;
        margin: 20px !important; /* Marge autour du cadre */
        padding: 20px !important;
        margin-top: 80px !important; /* Dégagement suffisant pour les onglets en haut */
    }}
    
    /* Style des expanders */
    div[data-testid="stExpander"] {{
        background-color: rgba(255, 255, 255, 0.3) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        border-radius: 10px !important;
    }}
    
    /* Onglets de navigation */
    div[data-baseweb="tab-list"] {{
        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }}
    button[data-baseweb="tab"] {{
        background: rgba(255,255,255,0.4) !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
    }}

    h1, h2, p, label {{ color: #0f172a !important; font-weight: bold !important; }}
</style>
""", unsafe_allow_html=True)

# 3. STRUCTURE DES ONGLETS (Réinsère ici ton code de chargement et tes calculs)
tab1, tab2, tab3 = st.tabs(["📊 Tableau de Bord", "🌱 Empreinte carbone", "📖 Référentiel Éléves"])

with tab1:
    st.title("🌱 Défi Carbone - Réseau Haut Vaucluse")
    # ... le contenu de ton onglet 1 ...

with tab2:
    st.header("Analyse graphique")
    # ... le contenu de ton onglet 2 ...

with tab3:
    st.header("Référentiel")
    # ... le contenu de ton onglet 3 ...
