import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# --- 2. URL ET CHARGEMENT ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/gviz/tq?tqx=out:csv&gid=1700157246"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage des noms de colonnes
        df.columns = df.columns.str.strip()
        df = df.fillna(0)
        return df
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return None

# --- 3. NAVIGATION ---
st.sidebar.title("🌿 Menu Principal")
page = st.sidebar.radio("Aller vers :", ["📊 Tableau de Bord", "📖 Glossaire Expert"])

# --- 4. PAGE PRINCIPALE (TABLEAU DE BORD) ---
if page == "📊 Tableau de Bord":
    st.title("📊 Bilan Carbone des Établissements")
    
    df = load_data()
    
    if df is not None:
        # --- TABLEAU 1 : VUE D'ENSEMBLE ---
        st.subheader("1. Aperçu général de tous les établissements")
        st.dataframe(df, use_container_width=True)
        
        st.divider()

        # --- RECHERCHE ET JAUGE ---
        st.subheader("2. Zoom par établissement et Jauge")
        
        # Sélection de l'établissement
        choix = st.selectbox("Sélectionner un établissement :", df['ETABLISSEMENT'].unique())
        
        # Données filtrées pour l'établissement choisi
        topo = df[df['ETABLISSEMENT'] == choix].iloc[0]
        
        # Correction ici : Utilisation du nom exact de ta colonne pour le score
        # On cherche 'BILAN TOTAL (KG CO2E)' qui semble être ta colonne finale
        score = topo.get('BILAN TOTAL (KG CO2E)', 0)
        
        col_j1, col_j2 = st.columns([1, 2])
        with col_j1:
            st.metric(label="Bilan Total (kgCO2e)", value=f"{score:,.0f} kg")
        with col_j2:
            # Dynamique de la jauge (seuils à adapter selon tes besoins pédagogiques)
            if score < 5000:
                st.success("Niveau : Très Bas Carbone")
                st.progress(0.2)
            elif score < 20000:
                st.warning("Niveau : Moyenne constatée")
                st.progress(0.5)
            else:
                st.error("Niveau : Consommation importante")
                st.progress(0.8)

        st.divider()

        # --- TABLEAU 2 : BILAN INDIVIDUEL PAR PÔLE ---
        st.subheader("3. Détails des consommations (kg CO2e)")
        
        # Utilisation des noms exacts de ton fichier Google Sheets
        c1, c2, c3, c4 = st.columns(4)
        
        # On récupère les valeurs des colonnes spécifiques de ton tableau
        val_repas = topo.get('REPAS (KG CO2E)', 0)
        val_energie = topo.get('ENERGIE (KG CO2E)', 0)
        val_transport = topo.get('TRANSPORT (KG CO2E)', 0)
        val_fournitures = topo.get('FOURNITURES (KG CO2E)', 0)

        c1.info(f"🍎 **Repas**\n\n {val_repas:,.0f} kg")
        c2.info(f"⚡ **Énergie**\n\n {val_energie:,.0f} kg")
        c3.info(f"🚌 **Transport**\n\n {val_transport:,.0f} kg")
        c4.info(f"📄 **Fournitures**\n\n {val_fournitures:,.0f} kg")

        st.divider()
        
        # --- ACCÈS FORMULAIRE ---
        st.subheader("📝 Accès au Formulaire")
        code = st.text_input("Code secret :", type="password")
        if code == "MONCODE123":
            st.success("Accès autorisé")
            st.link_button("Ouvrir le formulaire de saisie", "TON_LIEN_ICI")

# --- 5. PAGE GLOSSAIRE ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel des Facteurs d'Émission")
    st.markdown("Valeurs certifiées **ADEME** et **GIEC**.")
    
    tabs = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "🗑️ Déchets"])
    
    with tabs[1]:
        st.write("**Climatisation (R410A) :** 2088 kgCO2e/kg")
        st.info("C'est le poste le plus critique en cas de fuite !")

st.sidebar.divider()
st.sidebar.caption("Projet EPLE Bas Carbone - 2026")
