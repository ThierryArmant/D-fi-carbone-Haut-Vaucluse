import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os

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

# CSS : Le filtre Glassmorphism appliqué à tous les conteneurs Streamlit
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{img_base64}");
    background-size: cover;
    background-attachment: fixed;
}}

/* Le filtre Glassmorphism */
[data-testid="stBorderedContainer"], 
[data-testid="stExpander"], 
[data-testid="stDataFrame"],
.stTabs,
.main {{
    background-color: rgba(30, 41, 59, 0.70) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}}

/* Textes toujours lisibles */
h1, h2, h3, p, div, span, .stMarkdown {{
    color: #f8fafc !important;
}}

/* Forcer la couleur des graphiques pour fond sombre */
.js-plotly-plot .plotly .main-svg {{
    background: transparent !important;
}}
</style>
""", unsafe_allow_html=True)

# --- FONCTIONNALITÉS (Gardées intactes) ---
# ... (Insère ici tout ton code de chargement de données et tes colonnes)
# Le design sera automatiquement appliqué aux `st.expander` et `st.dataframe`

# Exemple de structure pour les onglets
tab1, tab2, tab3 = st.tabs(["📊 Tableau de Bord", "🌱 Empreinte carbone", "📖 Référentiel Éléves"])
with tab1:
    st.title("Tableau de Bord")
    with st.expander("Détails"):
        st.write("Contenu ici")
