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

# 2. DESIGN GIVRÉ SÉCURISÉ (Pas de position: fixed pour éviter le scroll)
st.markdown(f"""
<style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
    }}
    .main .block-container {{
        background: rgba(228, 235, 245, 0.58) !important;
        backdrop-filter: blur(15px);
        border-radius: 20px;
        margin: 50px;
        padding: 40px;
    }}
    div[data-testid="stExpander"] {{
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 10px !important;
    }}
    h1, h2, h3, p, label {{ color: #0f172a !important; font-weight: bold !important; }}
</style>
""", unsafe_allow_html=True)

# 3. FONCTIONS
def draw_custom_bar(label, value, total, color, sub=False):
    pct = (value / total * 100) if total > 0 else 0
    st.markdown(f"**{label}** : {pct:.1f}%")
    st.progress(pct/100)

# 4. DATA (Reprends ton load_data habituel ici)
# ...

# 5. NAVIGATION
tab1, tab2, tab3 = st.tabs(["📊 Tableau de Bord", "🌱 Empreinte carbone", "📖 Référentiel Éléves"])

with tab1:
    st.title("Défi Carbone")
    # ... ton code Dashboard ...

with tab2:
    st.header("Analyse graphique")
    # ... ton code Graph ...

with tab3:
    st.header("Référentiel Carbone")
    g_tabs = st.tabs(["🍎 Cantine", "❄️ Énergie", "🚌 Transports", "📦 Biens & Équipements", "🗑️ Déchets"])
    
    with g_tabs[0]:
        st.write("Détails Cantine...")
    with g_tabs[1]:
        st.write("Détails Énergie...")
    with g_tabs[2]:
        st.write("Détails Transports...")
    with g_tabs[3]:
        st.write("📦 Biens et Équipements : Détails ici...")
    with g_tabs[4]:
        st.write("🗑️ Gestion des déchets : Détails ici...")
