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

# --- ONGLET DASHBOARD (Identique) ---
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
            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg"}, gauge = {'axis': {'range': [None, 5000]}, 'bar': {'color': "#1e3d59"}, 'steps': [{'range': [0, 1500], 'color': "#d4edda"}, {'range': [1500, 2500], 'color': "#fff3cd"}, {'range': [2500, 5000], 'color': "#f8d7da"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 2500}}))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)
        with st.expander("🔐 Mise à jour des données"):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform")
        st.dataframe(df, hide_index=True, use_container_width=True)

# --- ONGLET GLOSSAIRE AVEC PRÉCISIONS MÉTHODOLOGIQUES ---
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
        st.markdown('<div class="methode"><b>📝 Méthode :</b> On multiplie le nombre de repas servis par l\'empreinte de production des ingrédients.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 Le saviez-vous ?</b> Manger 1 steak de bœuf émet autant que 32 km en voiture !</div>', unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("Pôle Énergie & Fluides")
        st.write("- **Électricité :** 0.06 kgCO2e / kWh")
        st.write("- **Gaz Naturel :** 0.227 kgCO2e / kWh")
        st.write("- **Climatisation (R410A) :** 2088 kgCO2e / kg")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> On relève la consommation réelle sur les compteurs ou les factures. Pour la clim, on note la quantité de gaz rajoutée lors de l\'entretien (car 1 kg rajouté = 1 kg qui a fui).</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>❄️ L\'anecdote :</b> 1 kg de fuite de clim = 10 000 km en voiture !</div>', unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("Pôle Transports")
        st.write("- **Autocar :** 0.030 kgCO2e / km / élève")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> On calcule la distance totale parcourue multipliée par le facteur d\'émission du véhicule, divisée par le nombre de passagers.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>🚌 Union :</b> Venir en bus scolaire retire 43 voitures de la route.</div>', unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("Pôle Déchets")
        st.write("- **Gaspillage Pain :** 0.63 kgCO2e / kg")
        st.write("- **Papier jeté (non trié) :** 0.45 kgCO2e / kg")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> On pèse les bacs de déchets. Le calcul inclut la collecte et le traitement (incinération ou enfouissement).</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>🥖 Gaspillage :</b> Jeter 1 kg de pain = 60 heures d\'ampoule allumée !</div>', unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("Pôle Biens & Consommables")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.write("**Papier et Impression :**")
            st.write("- **Ramette A4 (500 f.) :** 2.62 kgCO2e")
            st.write("- **Photocopieur pro :** 850 kgCO2e")
        with col_b2:
            st.write("**Équipements :**")
            st.write("- **Vidéoprojecteur :** 94 kgCO2e")
            st.write("- **Ordinateur Portable :** 161 kgCO2e")
        
        st.markdown("""
        <div class="methode">
        <b>📝 Méthode de calcul (La règle ADEME) :</b><br>
        • <b>Pour les consommables (Papier, craies) :</b> On note la quantité consommée sur l'année. La fabrication est incluse dans l'unité.<br>
        • <b>Pour le matériel durable (PC, Projecteurs) :</b> On calcule l'impact de <b>FABRICATION</b> (énergie grise). L'ADEME précise que fabriquer un PC portable représente 80% de son impact total. Le levier d'action est donc de faire durer le matériel le plus longtemps possible.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="anecdote">
        <b>📹 Focus Vidéoprojecteur :</b> Sa fabrication émet 94 kg de CO2 (autant que 750 brosses à dents). Éteindre l'ampoule permet d'économiser l'énergie de 20 smartphones par heure !
        <br><b>📄 Forêt de papier :</b> 1000 ramettes par an = une forêt de 10 arbres "consommée".
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("Sources : Méthodologie ADEME / GIEC - Mise à jour Mai 2026")
