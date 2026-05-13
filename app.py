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
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_style()

# 3. VARIABLES DE CONNEXION
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

# 4. CHARGEMENT DES DONNÉES
@st.cache_data(ttl=60)
def load_data():
    try:
        raw = pd.read_csv(url, header=None)
        for i, row in raw.iterrows():
            row_str = [str(x).strip() for x in row.values]
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
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel Expert (5 Pôles)"])

# --- ONGLET DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        cols_to_fix = ["Total émissions", "conso carbone  par personne", "Effectif total"]
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

        st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements</p>', unsafe_allow_html=True)
            if "Etablissements" in df.columns:
                st.dataframe(df[["Etablissements", "conso carbone  par personne"]].sort_values("conso carbone  par personne", ascending=False), hide_index=True, use_container_width=True, height=380)
        
        with col2:
            st.markdown('<p class="inner-title">🚀 Moyenne du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            moyenne = df["Total émissions"].sum() / df["Effectif total"].sum() if df["Effectif total"].sum() > 0 else 0
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = moyenne, number = {'suffix': " kg"},
                gauge = {
                    'axis': {'range': [None, 5000]}, 'bar': {'color': "#1e3d59"},
                    'steps': [{'range': [0, 1500], 'color': "#d4edda"}, {'range': [1500, 2500], 'color': "#fff3cd"}, {'range': [2500, 5000], 'color': "#f8d7da"}],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'value': 2500}
                }
            ))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔐 Mise à jour des données"):
            pwd = st.text_input("Code secret :", type="password")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform")

        st.dataframe(df, hide_index=True, use_container_width=True)

# --- ONGLET GLOSSAIRE AVEC ANECDOTES ---
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
        
        st.markdown("""
        <div class="anecdote">
        <b>💡 Le saviez-vous ?</b><br>
        Manger <b>un seul steak de bœuf</b> émet autant de CO2 que de parcourir <b>32 km en voiture</b>. 
        À l'inverse, un repas végétarien équivaut à seulement 2 km. Pour compenser un repas "Viande Rouge", il faudrait planter un arbre et le laisser pousser pendant 4 mois !
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("Pôle Énergie & Fluides")
        st.write("- **Climatisation (R410A) :** 2088 kgCO2e / kg")
        
        st.markdown("""
        <div class="anecdote">
        <b>❄️ L'anecdote "Glaçante" :</b><br>
        Si votre climatisation fuit de seulement <b>1 kg de gaz</b>, cela pollue autant que de rouler <b>10 000 km</b> avec une voiture thermique (soit un trajet aller-retour Paris-Pékin) ! 
        C'est pour cela que l'entretien des machines est crucial.
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("Pôle Transports")
        st.write("- **Autocar :** 0.030 kgCO2e / km / élève")
        
        st.markdown("""
        <div class="anecdote">
        <b>🚌 L'union fait la force :</b><br>
        Un bus scolaire transporte environ 50 élèves. Si chaque élève venait seul en voiture, on émettrait <b>7 fois plus de CO2</b>. 
        Venir en bus, c'est comme si 43 voitures disparaissaient instantanément de la route !
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("Pôle Déchets")
        st.write("- **Gaspillage Pain :** 0.63 kgCO2e / kg")
        
        st.markdown("""
        <div class="anecdote">
        <b>🥖 Ne perdez pas une miette :</b><br>
        Jeter <b>1 kg de pain</b> à la poubelle, c'est l'équivalent en CO2 de laisser une <b>ampoule allumée pendant 60 heures</b>. 
        Pourquoi ? Parce qu'il a fallu de l'énergie pour cultiver le blé, le moudre, transporter la farine et cuire le pain au four !
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("Pôle Biens & Consommables")
        st.write("- **Ordinateur Portable :** 161 kgCO2e")
        
        st.markdown("""
        <div class="anecdote">
        <b>💻 L'énergie "grise" :</b><br>
        Fabriquer <b>un seul ordinateur portable</b> demande d'extraire près de <b>800 kg de matières premières</b>. 
        Son impact carbone est tel qu'il faudrait l'utiliser pendant <b>25 ans</b> pour que sa consommation électrique dépasse enfin la pollution causée par sa fabrication !
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("Sources : Base Empreinte ADEME - Comparaisons pédagogiques 2026")
