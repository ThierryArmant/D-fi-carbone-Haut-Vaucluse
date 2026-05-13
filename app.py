import streamlit as st
import pandas as pd

# 1. CONFIGURATION (Toujours en premier)
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# 2. DÉFINITION DE LA VARIABLE 'page' (La source de votre erreur)
st.sidebar.title("🌿 Menu de Navigation")
page = st.sidebar.radio("Aller vers :", ["📊 Tableau de Bord", "📖 Glossaire Expert"])

# 3. CHARGEMENT DES DONNÉES
SHEET_URL = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/gviz/tq?tqx=out:csv&gid=1700157246"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage rapide pour éviter les erreurs de calcul
        df = df.fillna(0) 
        return df
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return None

# 4. LOGIQUE DE NAVIGATION
if page == "📊 Tableau de Bord":
    st.title("📊 Bilan Carbone des Établissements")
    
    df = load_data()
    
    if df is not None:
        # --- FILTRAGE ET JAUGE ---
        st.subheader("Bilan par établissement")
        
        # Vérifiez que la colonne s'appelle exactement 'ETABLISSEMENT'
        liste_etablissements = df['ETABLISSEMENT'].unique()
        choix = st.selectbox("Sélectionner un établissement :", liste_etablissements)
        
        # Extraction des données de l'établissement choisi
        topo = df[df['ETABLISSEMENT'] == choix].iloc[0]
        
        # Affichage de la Jauge de Score Global
        # Remplacer 'SCORE GLOBAL' par le nom exact de votre colonne de total
        score_global = topo.get('SCORE GLOBAL', 0) 
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric(label="Impact Total (kgCO2e / élève)", value=f"{score_global:.2f}")
        
        with col2:
            # Jauge visuelle simplifiée
            if score_global < 150:
                st.success("Niveau : Très Performant (A)")
            elif score_global < 350:
                st.warning("Niveau : Moyen (C)")
            else:
                st.error("Niveau : Amélioration Prioritaire (E)")
        
        st.divider()

        # --- BILAN INDIVIDUEL PAR PÔLE ---
        st.subheader("Répartition par pôle de consommation")
        c1, c2, c3, c4 = st.columns(4)
        # Utilisez .get() pour éviter que l'app plante si une colonne manque
        c1.write(f"🍎 **Repas**\n\n {topo.get('REPAS', 0)} kg")
        c2.write(f"⚡ **Énergie**\n\n {topo.get('ENERGIE', 0)} kg")
        c3.write(f"🚌 **Transports**\n\n {topo.get('TRANSPORT', 0)} kg")
        c4.write(f"📄 **Fournitures**\n\n {topo.get('PAPIER', 0)} kg")

        st.divider()
        
        # --- ACCÈS FORMULAIRE ---
        st.subheader("📝 Accès Formulaire")
        code_saisi = st.text_input("Code secret :", type="password")
        if code_saisi == "VOTRE_CODE":
            st.link_button("Ouvrir le Formulaire", "LIEN_VERS_GOOGLE_FORM")

elif page == "📖 Glossaire Expert":
    # Le code du glossaire que nous avons fait précédemment
    st.title("📖 Glossaire Expert")
    st.write("Détails des facteurs d'émission (ADEME / GIEC)...")
