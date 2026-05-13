import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", layout="wide")

# 2. STYLE CSS (BANDEAU DISCRET + FOND BLANC OPAQUE)
def set_bg_and_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://lh3.googleusercontent.com/d/1KA5uUEwfkuW99zl93_ngwq1dJ115zXrK");
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 60%;
            background-color: #f0f2f6;
        }}
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.9); 
            padding: 1rem 2rem !important; 
            border-radius: 12px;
            margin-top: 10px;
        }}
        [data-testid="stExpanderSummary"] {{
            background-color: white !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            min-height: 40px !important;
            padding: 0px 10px !important;
        }}
        [data-testid="stHeader"] {{ height: 0px; }}
        .inner-title {{
            text-align: center; font-weight: bold; font-size: 18px; color: #1e3d59; margin-bottom: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_and_style()

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
                new_cols = []
                for j, val in enumerate(row.values):
                    c_name = str(val).strip() if pd.notnull(val) else f"Col_{j}"
                    new_cols.append(c_name)
                data.columns = new_cols
                # Nettoyage automatique des noms de colonnes pour le glossaire
                data.columns = data.columns.str.strip()
                return data.loc[:, ~data.columns.duplicated()].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
    return pd.DataFrame()

# 5. EXECUTION ET NAVIGATION PAR ONGLETS
df = load_data()

# Création des onglets principaux
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel & Glossaire"])

# --- CONTENU DE L'ONGLET DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        # Nettoyage des colonnes numériques
        cols_to_fix = ["Total émissions", "conso carbone  par personne", "Effectif total"]
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

        st.markdown("<h2 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h2>", unsafe_allow_html=True)

        # LIGNE 1 : CLASSEMENT ET JAUGE
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<p class="inner-title">📊 Classement (kg/pers)</p>', unsafe_allow_html=True)
            if "Etablissements" in df.columns:
                st.dataframe(df[["Etablissements", "conso carbone  par personne"]].sort_values("conso carbone  par personne", ascending=False), hide_index=True, use_container_width=True, height=350)
        
        with col2:
            st.markdown('<p class="inner-title">🚀 Moyenne Réelle du Réseau</p>', unsafe_allow_html=True)
            total_co2 = df["Total émissions"].sum()
            total_pop = df["Effectif total"].sum()
            moyenne = total_co2 / total_pop if total_pop > 0 else 0
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = moyenne,
                number = {'suffix': " kg", 'font': {'size': 35}},
                gauge = {
                    'axis': {'range': [None, 5000]},
                    'bar': {'color': "#1e3d59"},
                    'steps': [
                        {'range': [0, 1500], 'color': "#2ecc71"},
                        {'range': [1500, 2500], 'color': "#fbc02d"},
                        {'range': [2500, 5000], 'color': "#ff8a80"}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 5}, 'value': 2500}
                }
            ))
            fig.update_layout(height=350, margin=dict(t=20, b=0, l=30, r=30))
            st.plotly_chart(fig, use_container_width=True)

        # LIGNE 2 : BANDEAU MISE À JOUR
        with st.expander("📝 Mettre à jour les données"):
            c_p1, c_p2 = st.columns([1, 1])
            with c_p1:
                pwd = st.text_input("Code établissement :", type="password", key="pwd_input")
            with c_p2:
                st.write("Accès au formulaire de saisie pour l'année en cours.")
            if pwd == "CARBONE2026":
                st.success("Code valide")
                st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)

        # LIGNE 3 : TABLEAU DÉTAILLÉ
        st.markdown("<p style='font-weight: bold; color: #1e3d59;'>📋 Détails complets</p>", unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("⚠️ Aucune donnée trouvée. Vérifiez l'onglet Bilan et le partage du fichier.")

# --- CONTENU DE L'ONGLET GLOSSAIRE ---
with tab_glossaire:
    st.markdown("<h2 style='color: #1e3d59;'>📖 Référentiel Expert Carbone</h2>", unsafe_allow_html=True)
    st.write("Retrouvez ici les modes de calcul et les facteurs d'émission officiels (ADEME / GIEC).")
    
    g_tab1, g_tab2, g_tab3, g_tab4 = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "📦 Biens & Conso"])
    
    with g_tab1:
        st.subheader("Pôle Restauration")
        c1, c2, c3 = st.columns(3)
        c1.metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        c2.metric("Viande Blanche", "1.60 kg", "CO2e/repas")
        c3.metric("Végétarien", "0.50 kg", "CO2e/repas")
        st.info("**Expertise :** L'impact du bœuf est élevé en raison du méthane (CH4) produit par les ruminants.")

    with g_tab2:
        st.subheader("Énergie et Fluides")
        st.write("- **Électricité (Mix FR) :** 0.06 kgCO2e / kWh")
        st.write("- **Gaz Naturel :** 0.227 kgCO2e / kWh")
        st.write("- **Climatisation (R410A) :** 2088 kgCO2e / kg")
        st.warning("**Alerte Fuite :** 1 kg de gaz de clim = 2 tonnes de CO2 dans l'atmosphère.")

    with g_tab3:
        st.subheader("Déplacements Scolaires")
        st.write("- **Autocar Scolaire :** 0.030 kgCO2e / km / passager")
        st.write("- **Voiture Thermique :** 0.218 kgCO2e / km")
        st.info("Le car est très performant car l'impact est divisé par 50 passagers.")

    with g_tab4:
        st.subheader("Biens et Consommables")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.write("**Papier A4 (80g) :**")
            st.write("- 1 ramette (500 f.) = 2.5 kg")
            st.write("- Impact = 1.05 kgCO2e / kg de papier")
        with col_g2:
            st.write("**Équipement numérique :**")
            st.write("- Ordinateur : 161 kgCO2e (Fabrication)")
            st.write("- Tablette : 65 kgCO2e (Fabrication)")

    st.divider()
    st.caption("Sources : Base Empreinte ADEME - Mise à jour 2026")
