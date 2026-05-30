import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS (Lisibilité et design des encadrés)
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
        
        /* Style des anecdotes (Bleu) */
        .anecdote {
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 5px solid #2196f3;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        /* Style de la méthode (Vert) */
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

# 3. VARIABLES DE CONNEXION
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCa-ml7NJO07Wb09U6ULv4HmHzzKABue1XVeZ7rkW-13vQKm_EjwblGiumu9N1A8X5G2HfpJUX-VPU/pub?gid=717694895&single=true&output=csv"

# 4. CHARGEMENT DES DONNÉES
@st.cache_data(ttl=60)
def load_data():
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
        return pd.DataFrame()

df = load_data()

# 5. NAVIGATION PAR ONGLETS
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel consommations carbone (5 Pôles)"])

# --- ONGLET DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        # Recherche flexible des colonnes (évite le KeyError)
        try:
            col_etab = [c for c in df.columns if "Etablissement" in c][0]
            col_total = [c for c in df.columns if "Total émissions" in c][0]
            col_conso = [c for c in df.columns if "conso" in c and "par personne" in c][0]
            col_eff = [c for c in df.columns if "Effectif total" in c][0]

            # Nettoyage et conversion numérique
            for col in [col_total, col_conso, col_eff]:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            
            st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown('<p class="inner-title">📊 Classement des Établissements</p>', unsafe_allow_html=True)
                st.dataframe(df[[col_etab, col_conso]].sort_values(col_conso, ascending=False), hide_index=True, use_container_width=True, height=380)
            with col2:
                st.markdown('<p class="inner-title">🚀 Moyenne du Réseau (kg/pers)</p>', unsafe_allow_html=True)
                moyenne = df[col_total].sum() / df[col_eff].sum() if df[col_eff].sum() > 0 else 0
                fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg"}, gauge = {'axis': {'range': [None, 5000]}, 'bar': {'color': "#1e3d59"}}))
                fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
                st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("🔐 Mise à jour des données"):
                pwd = st.text_input("Code secret :", type="password", key="main_pwd")
                if pwd == "CARBONE2026":
                    st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform")
            st.dataframe(df, hide_index=True, use_container_width=True)
        except Exception as e:
            st.error(f"Erreur d'affichage : assurez-vous que les colonnes 'Etablissement', 'Total émissions', 'conso carbone par personne' et 'Effectif total' existent.")
    else:
        st.warning("Données introuvables.")

# --- ONGLET GLOSSAIRE ---
with tab_glossaire:
    st.markdown("<h2 style='color: #1e3d59;'>📖 Référentiel des 5 Pôles Carbone</h2>", unsafe_allow_html=True)
    g_tabs = st.tabs(["🍎 1. Alimentation", "❄️ 2. Énergie & Clim", "🚌 3. Transports", "🗑️ 4. Déchets", "📦 5. Biens & Conso"])
    with g_tabs[0]:
        st.subheader("Pôle Restauration")
        st.columns(4)[0].metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Calcul sur production ingrédients.</div>', unsafe_allow_html=True)
    with g_tabs[1]:
        st.subheader("Pôle Énergie & Fluides")
        st.write("- **Électricité :** 0.06 kgCO2e / kWh")
    with g_tabs[2]:
        st.subheader("Pôle Transports")
        st.write("- **Autocar :** 0.030 kgCO2e / km")
    with g_tabs[3]:
        st.subheader("Pôle Déchets")
        st.metric("Assiette", "1.20 kg", "CO2e / kg")
    with g_tabs[4]:
        st.subheader("Pôle Biens & Consommables")
        st.write("**Papier :** Ramette A4 = 2.62 kgCO2e")
    st.divider()
    st.caption("Sources : Méthodologie ADEME - Mise à jour Mai 2026")
