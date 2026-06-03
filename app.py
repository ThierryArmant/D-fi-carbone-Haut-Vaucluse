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

# 2. STYLE CSS COMPACT ET AÉRÉ
def set_style(img_b64):
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{img_b64}");
        background-size: cover;
    }}
    
    /* Dégagement en haut pour les onglets */
    .main .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        background: transparent !important;
    }}
    
    /* Dalles compactes (espacement réduit) */
    div[data-testid="stBorderedContainer"], div[data-testid="stColumn"], .stExpander {{
        background-color: rgba(228, 235, 245, 0.6) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.4) !important;
        border-radius: 12px !important;
        padding: 12px !important; /* Réduit pour compacter */
        margin-bottom: 8px !important; /* Réduit pour compacter */
    }}
    
    /* Titres et textes sombres pour contraste */
    h1, h2, .inner-title, p, label {{ color: #0f172a !important; font-weight: bold !important; }}
    
    /* Onglets */
    button[data-baseweb="tab"] {{
        background: rgba(255,255,255,0.3) !important;
        border-radius: 6px !important;
        padding: 5px 15px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

set_style(img_base64)

# 3. LOGIQUE (Reste inchangée pour préserver tes fonctionnalités)
# ... [insérer ici le reste du code fonctionnel précédent] ...
