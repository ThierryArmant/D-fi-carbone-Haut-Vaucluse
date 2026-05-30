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
            background-color: #e3f2fd; padding: 15px; border-left: 5px solid #2196f3; border-radius: 5px; margin: 10px 0;
        }
        /* Style de la méthode (Vert) */
        .methode {
            background-color: #f1f8e9; padding: 10px; border-left: 5px solid #8bc34a; border-radius: 5px; font-size: 0.9em; margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_style()

# 3. VARIABLES DE CONNEXION (Ton onglet Bilan Carbone)
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

# 4. CHARGEMENT DES DONNÉES
@st.cache_data(ttl=60)
def load_data():
    try:
        raw = pd.read_csv(url, header=None)
        for i, row in raw.iterrows():
            row_str = [str(x).strip() for x in row.values]
            # Détection stricte de ton en-tête de colonne
            if "Etablissements" in row_str:
                data = raw.iloc[i+1:].copy()
                new_cols = [str(val).strip() if pd.notnull(val) else f"Col_{j}" for j, val in enumerate(row.values)]
                data.columns = new_cols
                return data.loc[:, ~data.columns.duplicated()].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
    return pd.DataFrame()

df = load_data()

# 5. NAVIGATION PAR ONGLETS
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel consommations carbone (5 Pôles)"])

# --- ONGLET DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        # Noms de colonnes STRICTS calqués sur ton fichier Google Sheets
        col_etab = "Etablissements"
        col_total = "Total émissions"
        col_eff = "Effectif total"
        col_conso = "conso carbone par personne"

        # Nettoyage et conversion numérique des colonnes de scores
        for col in [col_total, col_eff, col_conso]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        # On ne garde que les lignes où un établissement est saisi et actif (score > 0)
        df_active = df[(df[col_etab].astype(str).str.strip() != "") & (df[col_conso] > 0)].copy()

        st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements (kg/personne)</p>', unsafe_allow_html=True)
            if col_etab in df_active.columns and col_conso in df_active.columns:
                # Tri décroissant direct basé sur le ratio (colonne I) de ton Sheets
                df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                st.dataframe(df_ranking, hide_index=True, width="stretch", height=380)
            else:
                st.info("En attente de données calculées dans le tableur...")
                
        with col2:
            st.markdown('<p class="inner-title">🚀 Moyenne du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            if not df_active.empty and df_active[col_eff].sum() > 0:
                moyenne = df_active[col_total].sum() / df_active[col_eff].sum()
            else:
                moyenne = 0

            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg"}, gauge = {'axis': {'range': [None, 2000]}, 'bar': {'color': "#1e3d59"}, 'steps': [{'range': [0, 500], 'color': "#d4edda"}, {'range': [500, 1000], 'color': "#fff3cd"}, {'range': [1000, 2000], 'color': "#f8d7da"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 1000}}))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("🔐 Saisie de nouvelles données"):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform")
        
        st.markdown('<p class="inner-title">📋 Synthèse Globale des Établissements (Données Centralisées)</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch")

# --- ONGLET GLOSSAIRE ---
with tab_glossaire:
    st.markdown("<h2 style='color: #1e3d59;'>📖 Référentiel des 5 Pôles Carbone</h2>", unsafe_allow_html=True)
    g_tabs = st.tabs(["🍎 1. Alimentation", "❄️ 2. Énergie & Clim", "🚌 3. Transports", "🗑️ 4. Déchets Alimentaires", "📦 5. Biens & Conso"])
    
    with g_tabs[0]:
        st.subheader("Pôle Restauration (Production)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        c2.metric("Viande Blanche", "1.60 kg", "CO2e/repas")
        c3.metric("Poisson", "2.00 kg", "CO2e/repas")
        c4.metric("Végétarien", "0.50 kg", "CO2e/repas")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Nombre de repas x empreinte de production.</div>', unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("Pôle Énergie & Fluides")
        st.write("- **Électricité :** 0.06 kgCO2e / kWh")
        st.write("- **Gaz Naturel :** 0.227 kgCO2e / kWh")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Consommation réelle des compteurs.</div>', unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("Pôle Transports")
        st.write("- **Autocar Scolaire :** 0.030 kgCO2e / km / élève")
        st.write("- **Voiture thermique :** 0.218 kgCO2e / km")

    with g_tabs[3]:
        st.subheader("Pôle Déchets Alimentaires")
        c_d1, c_d2 = st.columns(2)
        c_d1.metric("Assiette jetée (moyenne)", "1.20 kg", "CO2e / kg jeté")
        c_d2.metric("Gaspillage Pain", "0.63 kg", "CO2e / kg jeté")

    with g_tabs[4]:
        st.subheader("Pôle Biens & Consommables")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.write("**Papier et Fin de vie :**")
            st.write("- **Ramette A4 neuve :** 2.62 kgCO2e")
        with col_b2:
            st.write("**Équipements (Fabrication) :**")
            st.write("- **Photocopieur :** 850 kgCO2e")
            st.write("- **Ordinateur Portable :** 161 kgCO2e")

    st.divider()
    st.caption("Sources : Méthodologie ADEME / GIEC / PEBC - Mise à jour Mai 2026")
