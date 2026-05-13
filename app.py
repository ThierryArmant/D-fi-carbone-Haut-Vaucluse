import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# --- 2. URL ET CHARGEMENT ---
# Utilisation de l'URL directe de ton fichier
SHEET_URL = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/gviz/tq?tqx=out:csv&gid=1700157246"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage pour éviter les erreurs de lecture
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
        
        # On vérifie si la colonne existe
        col_etab = 'ETABLISSEMENT' if 'ETABLISSEMENT' in df.columns else df.columns[0]
        choix = st.selectbox("Sélectionner un établissement :", df[col_etab].unique())
        
        # Données filtrées
        topo = df[df[col_etab] == choix].iloc[0]
        
        # Affichage de la Jauge (Score Global)
        # Note : On récupère 'SCORE GLOBAL' ou 'TOTAL' selon ton Sheets
        score = topo.get('SCORE GLOBAL', 0)
        
        col_j1, col_j2 = st.columns([1, 2])
        with col_j1:
            st.metric(label="Impact Total (kgCO2e/élève)", value=f"{score:.2f}")
        with col_j2:
            if score < 150:
                st.success("Niveau A : Très Bas Carbone")
                st.progress(0.2)
            elif score < 350:
                st.warning("Niveau C : Moyenne Nationale")
                st.progress(0.5)
            else:
                st.error("Niveau E : Consommation Élevée")
                st.progress(0.9)

        st.divider()

        # --- TABLEAU 2 : BILAN INDIVIDUEL PAR PÔLE ---
        st.subheader("3. Détails des consommations")
        
        # On crée des colonnes pour un affichage propre
        c1, c2, c3, c4 = st.columns(4)
        c1.info(f"🍎 **Repas**\n\n {topo.get('REPAS', 0)} kgCO2e")
        c2.info(f"⚡ **Énergie**\n\n {topo.get('ENERGIE', 0)} kgCO2e")
        c3.info(f"🚌 **Transport**\n\n {topo.get('TRANSPORT', 0)} kgCO2e")
        c4.info(f"📄 **Papier**\n\n {topo.get('PAPIER', 0)} kgCO2e")

        st.divider()
        
        # --- ACCÈS FORMULAIRE ---
        st.subheader("📝 Accès au Formulaire")
        code = st.text_input("Code secret :", type="password")
        if code == "MONCODE123":
            st.success("Accès autorisé")
            st.link_button("Ouvrir le formulaire de saisie", "https://votre-lien-google-form")

# --- 5. PAGE GLOSSAIRE ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel des Facteurs d'Émission")
    st.markdown("Valeurs issues de l'**ADEME** et du **PEBC**.")
    
    tabs = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "🗑️ Déchets"])
    
    with tabs[0]:
        st.metric("Viande Rouge", "7.26 kgCO2e", "par repas")
        st.metric("Végétarien", "0.50 kgCO2e", "par repas")
    with tabs[1]:
        st.write("**Électricité :** 0.06 kgCO2e/kWh")
        st.write("**Gaz :** 0.227 kgCO2e/kWh")
        st.write("**Clim (R410A) :** 2088 kgCO2e/kg")
    with tabs[2]:
        st.write("**Autocar :** 0.030 kgCO2e/km/passager")
    with tabs[3]:
        st.write("**Papier :** 1.05 kgCO2e/kg (soit ~2.6kg par ramette)")

st.sidebar.divider()
st.sidebar.caption("Projet EPLE Bas Carbone - Expertise GIEC/ADEME")
