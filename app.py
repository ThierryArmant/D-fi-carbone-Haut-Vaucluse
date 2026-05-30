import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS
def set_style():
    st.markdown(
        """
        <style>
        .stApp { background-color: #f8f9fa; }
        .main .block-container {
            background-color: #ffffff;
            padding: 2rem 3rem !important;
            border-radius: 0px;
        }
        .inner-title {
            text-align: center; font-weight: bold; font-size: 20px; color: #1e3d59; margin-bottom: 15px;
        }
        [data-testid="stHeader"] { height: 0px; }
        .stTabs [data-baseweb="tab"] { font-weight: bold; }
        
        .anecdote {
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 5px solid #2196f3;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .methode {
            background-color: #f1f8e9;
            padding: 10px;
            border-left: 5px solid #8bc34a;
            border-radius: 5px;
            font-size: 0.9em;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_style()

# 3. CONNEXION
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCa-ml7NJO07Wb09U6ULv4HmHzzKABue1XVeZ7rkW-13vQKm_EjwblGiumu9N1A8X5G2HfpJUX-VPU/pub?gid=717694895&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

df = load_data()

# 4. NAVIGATION
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel consommations carbone (5 Pôles)"])

# --- DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        # Nettoyage des colonnes (utilise les noms exacts de ton Sheets)
        col_etab = "Etablissements"
        col_total = "Total émissions"
        col_conso = "conso carbone par personne"
        
        # Conversion numérique sécurisée
        for col in [col_total, col_conso]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

        st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements</p>', unsafe_allow_html=True)
            if col_etab in df.columns:
                st.dataframe(df[[col_etab, col_conso]].sort_values(col_conso, ascending=True), hide_index=True, use_container_width=True, height=380)
        with c2:
            st.markdown('<p class="inner-title">🚀 Moyenne du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            moyenne = df[col_conso].mean()
            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg"}, gauge = {'axis': {'range': [None, 3000]}, 'bar': {'color': "#1e3d59"}}))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("Données en cours de chargement...")

# --- GLOSSAIRE (Inchangé pour garder tes 173 lignes) ---
with tab_glossaire:
    st.markdown("<h2 style='color: #1e3d59;'>📖 Référentiel des 5 Pôles Carbone</h2>", unsafe_allow_html=True)
    g_tabs = st.tabs(["🍎 1. Alimentation", "❄️ 2. Énergie & Clim", "🚌 3. Transports", "🗑️ 4. Déchets", "📦 5. Biens & Conso"])
    
    with g_tabs[0]:
        st.subheader("Pôle Restauration")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        c2.metric("Viande Blanche", "1.60 kg", "CO2e/repas")
        c3.metric("Poisson", "2.00 kg", "CO2e/repas")
        c4.metric("Végétarien", "0.50 kg", "CO2e/repas")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Calcul sur production ingrédients.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 Le saviez-vous ?</b> 1 steak = 32 km en voiture.</div>', unsafe_allow_html=True)
    
    with g_tabs[1]:
        st.subheader("Pôle Énergie & Fluides")
        st.write("- **Électricité :** 0.06 kgCO2e / kWh")
        st.write("- **Gaz Naturel :** 0.227 kgCO2e / kWh")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Relevé compteurs.</div>', unsafe_allow_html=True)
    
    with g_tabs[2]:
        st.subheader("Pôle Transports")
        st.write("- **Autocar :** 0.030 kgCO2e / km")
        st.write("- **Voiture :** 0.218 kgCO2e / km")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Distance x facteur d\'émission.</div>', unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("Pôle Déchets")
        st.metric("Assiette", "1.20 kg", "CO2e / kg")
        st.markdown('<div class="anecdote"><b>🍽️ Gaspillage :</b> Jeter 1kg d\'assiette = 6 bouteilles plastique.</div>', unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("Pôle Biens & Consommables")
        st.write("**Papier :** Ramette A4 = 2.62 kgCO2e")
        st.write("**Équipements :** PC Portable = 161 kgCO2e")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Énergie grise à la fabrication.</div>', unsafe_allow_html=True)
