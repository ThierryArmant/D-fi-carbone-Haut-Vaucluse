import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS (Interface épurée et lisible)
def set_style():
    st.markdown(
        """
        <style>
        /* Fond de l'application gris très clair */
        .stApp {
            background-color: #f8f9fa;
        }
        /* Conteneur principal blanc opaque pour une lecture parfaite */
        .main .block-container {
            background-color: #ffffff;
            padding: 2rem 3rem !important;
            border-radius: 0px;
            box-shadow: none;
        }
        /* Style des titres */
        .inner-title {
            text-align: center; 
            font-weight: bold; 
            font-size: 20px; 
            color: #1e3d59; 
            margin-bottom: 15px;
        }
        /* Suppression du header Streamlit par défaut */
        [data-testid="stHeader"] { height: 0px; }
        
        /* Harmonisation des onglets */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #f1f3f5;
            border-radius: 5px 5px 0px 0px;
            gap: 1px;
            padding-top: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            border-bottom: 2px solid #1e3d59 !important;
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
                new_cols = []
                for j, val in enumerate(row.values):
                    c_name = str(val).strip() if pd.notnull(val) else f"Col_{j}"
                    new_cols.append(c_name)
                data.columns = new_cols
                data.columns = data.columns.str.strip()
                return data.loc[:, ~data.columns.duplicated()].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
    return pd.DataFrame()

# 5. EXECUTION ET NAVIGATION
df = load_data()

# Navigation par onglets (Tabs)
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel & Glossaire"])

# --- ONGLET DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        # Nettoyage des colonnes numériques
        cols_to_fix = ["Total émissions", "conso carbone  par personne", "Effectif total"]
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

        st.markdown("<h1 style='text-align: center; color: #1e3d59; margin-bottom: 30px;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements</p>', unsafe_allow_html=True)
            if "Etablissements" in df.columns:
                st.dataframe(
                    df[["Etablissements", "conso carbone  par personne"]].sort_values("conso carbone  par personne", ascending=False), 
                    hide_index=True, 
                    use_container_width=True, 
                    height=380
                )
        
        with col2:
            st.markdown('<p class="inner-title">🚀 Moyenne du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            total_co2 = df["Total émissions"].sum()
            total_pop = df["Effectif total"].sum()
            moyenne = total_co2 / total_pop if total_pop > 0 else 0
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = moyenne,
                number = {'suffix': " kg", 'font': {'size': 40}},
                gauge = {
                    'axis': {'range': [None, 5000], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#1e3d59"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 1500], 'color': "#d4edda"},
                        {'range': [1500, 2500], 'color': "#fff3cd"},
                        {'range': [2500, 5000], 'color': "#f8d7da"}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 2500}
                }
            ))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)

        # Zone de mise à jour
        st.divider()
        with st.expander("🔐 Accès Administration / Mise à jour"):
            c_p1, c_p2 = st.columns([1, 1])
            with c_p1:
                pwd = st.text_input("Code secret :", type="password")
            with c_p2:
                if pwd == "CARBONE2026":
                    st.success("Accès autorisé")
                    st.link_button("🚀 Ouvrir le formulaire de saisie", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform")

        st.markdown("<p style='font-weight: bold; color: #1e3d59; margin-top: 20px;'>📋 Détails complets des données</p>", unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("⚠️ En attente de connexion avec le fichier de données...")

# --- ONGLET GLOSSAIRE (CORRIGÉ SANS TRANSPARENCE) ---
with tab_glossaire:
    st.markdown("<h2 style='color: #1e3d59;'>📖 Référentiel Expert Carbone</h2>", unsafe_allow_html=True)
    st.write("Calculs basés sur les facteurs d'émission officiels de l'**ADEME** et du **GIEC** (Mise à jour 2026).")
    
    g_tab1, g_tab2, g_tab3, g_tab4 = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "📦 Biens & Conso"])
    
    with g_tab1:
        st.subheader("Pôle Restauration")
        c1, c2, c3 = st.columns(3)
        c1.metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        c2.metric("Viande Blanche", "1.60 kg", "CO2e/repas")
        c3.metric("Végétarien", "0.50 kg", "CO2e/repas")
        st.info("**Note pédagogique :** La viande rouge est le poste le plus lourd à cause du méthane issu de l'élevage bovin.")

    with g_tab2:
        st.subheader("Énergie et Fluides")
        st.markdown("""
        *   **Électricité :** 0.06 kgCO2e / kWh (Mix décarboné français).
        *   **Gaz Naturel :** 0.227 kgCO2e / kWh.
        *   **Fuites Climatisation :** 2088 kgCO2e par kg de fluide R410A rechargé.
        """)
        st.warning("Saviez-vous qu'une fuite de 1kg de clim équivaut à rouler 10 000 km en voiture ?")

    with g_tab3:
        st.subheader("Déplacements")
        st.write("- **Autocar :** 0.030 kgCO2e / km / élève.")
        st.write("- **Voiture :** 0.218 kgCO2e / km.")
        st.write("- **Train / TER :** 0.002 kgCO2e / km.")

    with g_tab4:
        st.subheader("Biens et Consommables")
        st.write("**Papier :** 1 ramette (2.5 kg) = 2.62 kgCO2e.")
        st.write("**Numérique :** Ordinateur (161 kgCO2e) | Tablette (65 kgCO2e).")
        st.info("On compte ici l'impact de fabrication (énergie grise).")

    st.divider()
    st.caption("Application Défi Carbone - Réseau Haut Vaucluse - Documentation Pédagogique")
