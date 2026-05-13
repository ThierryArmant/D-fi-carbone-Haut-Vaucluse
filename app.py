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
        # NETTOYAGE RADICAL : On enlève les espaces et on met tout en MAJUSCULES
        df.columns = df.columns.str.strip().str.upper()
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
        
        # On définit les noms de colonnes cibles en MAJUSCULES (grâce au nettoyage plus haut)
        COL_ETAB = 'ETABLISSEMENT'
        COL_TOTAL = 'BILAN TOTAL (KG CO2E)'
        
        # Sécurité : Si 'ETABLISSEMENT' n'est pas trouvé malgré tout, on prend la 1ère colonne
        target_col = COL_ETAB if COL_ETAB in df.columns else df.columns[0]
        
        liste_etab = df[target_col].unique()
        choix = st.selectbox("Sélectionner un établissement :", liste_etab)
        
        # Données filtrées
        topo = df[df[target_col] == choix].iloc[0]
        
        # Récupération du score avec sécurité
        score = topo.get(COL_TOTAL, 0)
        
        col_j1, col_j2 = st.columns([1, 2])
        with col_j1:
            st.metric(label="Bilan Total", value=f"{score:,.0f} kgCO2e")
        with col_j2:
            if score < 5000:
                st.success("Niveau : Bas Carbone")
                st.progress(0.2)
            elif score < 20000:
                st.warning("Niveau : Modéré")
                st.progress(0.5)
            else:
                st.error("Niveau : Élevé")
                st.progress(0.8)

        st.divider()

        # --- TABLEAU 2 : BILAN INDIVIDUEL PAR PÔLE ---
        st.subheader("3. Détails des consommations (kg CO2e)")
        
        c1, c2, c3, c4 = st.columns(4)
        
        # On utilise .get() avec les noms exacts nettoyés
        val_repas = topo.get('REPAS (KG CO2E)', 0)
        val_energie = topo.get('ENERGIE (KG CO2E)', 0)
        val_transport = topo.get('TRANSPORT (KG CO2E)', 0)
        val_fournitures = topo.get('FOURNITURES (KG CO2E)', 0)

        c1.info(f"🍎 **Repas**\n\n {val_repas:,.0f}")
        c2.info(f"⚡ **Énergie**\n\n {val_energie:,.0f}")
        c3.info(f"🚌 **Transport**\n\n {val_transport:,.0f}")
        c4.info(f"📄 **Fournitures**\n\n {val_fournitures:,.0f}")

# --- 5. PAGE GLOSSAIRE ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel Expert")
    st.write("Détails des facteurs d'émission...")
    # (Remettre ici le code des onglets de ton glossaire)

st.sidebar.divider()
st.sidebar.caption("Projet EPLE Bas Carbone - 2026")
