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
votre_gid = "717694895" 
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
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel consommations carbone (5 Pôles)"])

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
            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg"}, gauge = {'axis': {'range': [None, 5000]}, 'bar': {'color': "#1e3d59"}, 'steps': [{'range': [0, 1500], 'color': "#d4edda"}, {'range': [1500, 2500], 'color': "#fff3cd"}, {'range': [2500, 5000], 'color': "#f8d7da"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 2500}}))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("🔐 Mise à jour des données"):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform")
        st.dataframe(df, hide_index=True, use_container_width=True)

# --- ONGLET GLOSSAIRE (Avec Anecdotes & Méthodes) ---
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
        st.markdown('<div class="methode"><b>📝 Méthode :</b> On multiplie le nombre de repas servis par l\'empreinte de production des ingrédients.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 Le saviez-vous ?</b> Manger 1 seul steak de bœuf émet autant de CO2 que de parcourir 32 km en voiture ! À l\'inverse, un repas végétarien équivaut à seulement 2 km.</div>', unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("Pôle Énergie & Fluides")
        st.write("- **Électricité :** 0.06 kgCO2e / kWh")
        st.write("- **Gaz Naturel :** 0.227 kgCO2e / kWh")
        st.write("- **Climatisation (R410A) :** 2088 kgCO2e / kg")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Consommation réelle des compteurs. Pour la clim, on mesure la recharge de gaz (1kg rajouté = 1kg de fuite polluante).</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>❄️ L\'anecdote glaçante :</b> 1 kg de fuite de clim = 10 000 km en voiture (un aller-retour Paris-Pékin) ! L\'entretien est vital.</div>', unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("Pôle Transports")
        st.write("- **Autocar Scolaire :** 0.030 kgCO2e / km / élève")
        st.write("- **Voiture thermique :** 0.218 kgCO2e / km")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Distance parcourue x facteur d\'émission / nombre de passagers.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>🚌 Union :</b> Venir en bus scolaire permet de retirer virtuellement 43 voitures de la route.</div>', unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("Pôle Déchets Alimentaires")
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            st.metric("Assiette jetée (moyenne)", "1.20 kg", "CO2e / kg jeté")
        with c_d2:
            st.metric("Gaspillage Pain", "0.63 kg", "CO2e / kg jeté")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Pesée des restes. L\'assiette est lourde en carbone car elle contient des produits transformés (viande, sauces) qui ont déjà coûté cher à produire.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>🍽️ L\'assiette fantôme :</b> Jeter 1 kg d\'assiettes pleines émet autant que de fabriquer 6 bouteilles en plastique ou de recharger un smartphone 150 fois !</div>', unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("Pôle Biens & Consommables")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.write("**Papier et Fin de vie :**")
            st.write("- **Ramette A4 neuve :** 2.62 kgCO2e")
            st.write("- **Papier jeté (poubelle grise) :** 0.45 kgCO2e / kg")
            st.write("- **Papier trié (recyclage) :** 0.02 kgCO2e / kg")
        with col_b2:
            st.write("**Équipements (Fabrication) :**")
            st.write("- **Photocopieur :** 850 kgCO2e")
            st.write("- **Ordinateur Portable :** 161 kgCO2e")
            st.write("- **Vidéoprojecteur :** 94 kgCO2e")
        
        st.markdown("""
        <div class="methode">
        <b>📝 Méthode ADEME :</b><br>
        On mesure la <b>FABRICATION</b> (énergie grise) pour le matériel durable. 80% de l'impact d'un ordi a lieu avant sa première utilisation ! Pour le papier, on cumule l'achat et le mode de traitement (tri ou non).
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="anecdote">
        <b>📄 Forêt de papier :</b> 1000 ramettes/an = une forêt de 10 arbres consommée. Trier le papier divise son impact par 20 !<br>
        <b>📹 Focus Vidéo :</b> Fabriquer un projecteur émet autant que 750 brosses à dents. L'éteindre économise l'énergie de 20 smartphones par heure.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("Sources : Méthodologie ADEME / GIEC / PEBC - Mise à jour Mai 2026")
