import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# --- 2. URL ET CHARGEMENT ---
# URL directe vers le CSV de ton onglet "Bilan" (gid=1700157246)
SHEET_URL = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/gviz/tq?tqx=out:csv&gid=1700157246"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage radical des noms de colonnes : MAJUSCULES et pas d'espaces inutiles
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
        # AFFICHE LES COLONNES POUR DEBUG (À supprimer quand ça marche)
        # st.write("Colonnes détectées :", list(df.columns))

        # --- TABLEAU 1 : VUE D'ENSEMBLE ---
        st.subheader("1. Aperçu général de tous les établissements")
        st.dataframe(df, use_container_width=True)
        
        st.divider()

        # --- RECHERCHE ET JAUGE ---
        st.subheader("2. Zoom par établissement et Jauge")
        
        # Identification de la colonne établissement (souvent 'ETABLISSEMENT')
        col_etab = 'ETABLISSEMENT' if 'ETABLISSEMENT' in df.columns else df.columns[0]
        
        liste_etab = df[col_etab].unique()
        choix = st.selectbox("Sélectionner un établissement :", liste_etab)
        
        # On filtre la ligne correspondant à l'établissement choisi
        topo = df[df[col_etab] == choix].iloc[0]
        
        # --- RÉCUPÉRATION DES SCORES ---
        # ATTENTION : On utilise les noms exacts que l'on voit dans ton fichier
        # On ajoute .get() pour éviter le plantage si le nom change légèrement
        score_total = topo.get('BILAN TOTAL (KG CO2E)', 0)
        
        col_j1, col_j2 = st.columns([1, 2])
        with col_j1:
            st.metric(label="Bilan Global", value=f"{score_total:,.0f} kgCO2e")
        with col_j2:
            # Jauge dynamique
            if score_total < 5000:
                st.success("Performance : Excellente")
                st.progress(0.25)
            elif score_total < 50000:
                st.warning("Performance : Modérée")
                st.progress(0.55)
            else:
                st.error("Performance : Élevée")
                st.progress(0.85)

        st.divider()

        # --- TABLEAU 2 : BILAN INDIVIDUEL PAR PÔLE ---
        st.subheader("3. Détails des consommations (kg CO2e)")
        
        c1, c2, c3, c4 = st.columns(4)
        
        # On pointe vers les colonnes calculées de ton onglet Bilan
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
    st.title("📖 Référentiel Expert Carbone")
    st.markdown("Valeurs basées sur la **Base Empreinte ADEME** et les rapports du **GIEC**.")
    
    t1, t2, t3, t4 = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "🗑️ Déchets"])
    
    with t1:
        st.subheader("Impact des Repas")
        st.write("- **Viande Rouge** : 7,26 kgCO2e / repas")
        st.write("- **Viande Blanche** : 1,60 kgCO2e / repas")
        st.write("- **Végétarien** : 0,50 kgCO2e / repas")
        
    with t2:
        st.subheader("Énergie et Fluides")
        st.write("- **Électricité (France)** : 0,06 kgCO2e / kWh")
        st.write("- **Gaz Naturel** : 0,227 kgCO2e / kWh")
        st.write("- **Climatisation (Fuites R410A)** : 2088 kgCO2e / kg")
        
    with t3:
        st.subheader("Transports scolaire")
        st.write("- **Autocar** : 0,030 kgCO2e / km / élève")
        st.write("- **Voiture** : 0,218 kgCO2e / km")

    with t4:
        st.subheader("Déchets et Papier")
        st.write("- **Papier (Ramette 500f)** : Impact basé sur 2,5 kg / ramette")
        st.write("- **Déchets Ménagers** : 0,45 kgCO2e / kg")

st.sidebar.divider()
st.sidebar.caption("Eco-Score EPLE - 2026")
