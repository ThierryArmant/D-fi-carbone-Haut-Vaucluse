import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# 1. CONFIGURATION INITIALE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

def get_base64_image(file_name_without_ext):
    current_dir = os.path.dirname(__file__)
    for ext in ["", ".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
        path = os.path.join(current_dir, file_name_without_ext + ext)
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return ""

img_base64 = get_base64_image("image_1")

# 2. STYLE CSS FONCTIONNEL ET STABLE
def set_style(img_b64):
    bg_style = f"""
    [data-testid="stAppViewContainer"], .stAppViewContainer {{
        background-image: url("data:image/jpeg;base64,{img_b64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
    }}
    """
    
    st.markdown(f"""
    <style>
    {bg_style}
    .stApp {{ background: transparent !important; }}
    
    /* Style Ardoise Profond pour les conteneurs */
    div[data-testid="stBorderedContainer"], div[data-testid="stExpander"], .stExpander {{
        background-color: rgba(30, 41, 59, 0.85) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
    }}
    
    /* Assurer que les textes restent lisibles */
    h1, h2, h3, p, label, .pole-header, .sub-pole-header {{ color: #f1f5f9 !important; }}
    </style>
    """, unsafe_allow_html=True)

set_style(img_base64)

# 3. FONCTIONS UTILITAIRES
def draw_custom_bar(label, value_kg, total_kg, color, is_sub=False):
    pct = (value_kg / total_kg * 100) if total_kg > 0 else 0
    display_weight = f"{value_kg/1000:.2f} t" if value_kg >= 1000 else f"{value_kg:.1f} kg"
    
    if not is_sub:
        st.markdown(f"**{label}** : {display_weight} ({pct:.1f}%)")
        st.progress(pct/100)
    else:
        st.markdown(f"&nbsp;&nbsp;&nbsp;• {label} : {display_weight}")

# 4. CHARGEMENT DONNÉES ET STRUCTURE (Reprends ton code ici)
# Assure-toi de bien conserver ton `load_data()` et la structure de tes tabs
tab1, tab2, tab3 = st.tabs(["📊 Tableau de Bord", "🌱 Empreinte carbone", "📖 Référentiel Éléves"])

# ... (Réinsère ici tout ton code fonctionnel qui suit normalement)
