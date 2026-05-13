import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# --- 2. URL ET CHARGEMENT ---
# GID 1700157246 correspond à votre onglet de synthèse "Bilan"
SHEET_URL = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/gviz/tq?tqx=out:csv&gid=1700157246"

@st.cache_data(ttl=30) # Rafraîchissement toutes les 30 secondes
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage profond : tout en MAJUSCULES, on retire les espaces et points
        df.columns = df.columns.str.strip().str.upper().str.replace('.', '').str.replace(' ', '_')
        df = df.fillna(0)
        return df
    except Exception as e:
        st.error(f"Erreur de lecture du Sheets : {e}")
        return None

# --- 3. NAVIGATION ---
st.sidebar.title("🌿 Menu Principal")
page = st.sidebar.radio("Aller vers :", ["📊 Tableau de Bord", "📖 Glossaire Expert"])

# --- 4. PAGE PRINCIPALE (TABLEAU DE BORD) ---
if page == "📊 Tableau de Bord":
    st.title("📊 Bilan Carbone des Établissements")
    
    df = load_data()
    
    if df is not None:
        # Affiche le tableau brut pour vérification visuelle
        st.subheader("1. Aperçu de la base de données")
        st.dataframe(df, use_container_width=True)
        
        st.divider()

        # --- ZOOM ET JAUGE ---
        st.subheader("2. Zoom par établissement et Jauge")
        
        # Identification de la colonne établissement
        col_etab = 'ETABLISSEMENT' if 'ETABLISSEMENT' in df.columns else df.columns[0]
        choix = st.selectbox("Sélectionner un établissement :", df[col_etab].unique())
        
        # On extrait la ligne
        topo = df[df[col_etab] == choix].iloc[0]
        
        # Récupération du Score (On teste plusieurs noms possibles)
        score = topo.get('BILAN_TOTAL_(KG_CO2E)', topo.get('BILAN_TOTAL', topo.get('TOTAL', 0)))
        
        col_j1, col_j2 = st.columns([1, 2])
        with col_j1:
            st.metric(label="Bilan Global", value=f"{score:,.0f} kgCO2e")
        with col_j2:
            st.write("**Indicateur de Performance**")
            if score < 5000:
                st.success("Niveau : Bas Carbone")
                st.progress(0.2)
            elif score < 25000:
                st.warning("Niveau : Modéré")
                st.progress(0.5)
            else:
                st.error("Niveau : Élevé")
                st.progress(0.8)

        st.divider()

        # --- DÉTAILS DES CONSOMMATIONS ---
        st.subheader("3. Détails des consommations par pôle")
        c1, c2, c3, c4 = st.columns(4)
        
        # Mapping flexible pour trouver les données même si le nom change
        val_repas = topo.get('REPAS_(KG_CO2E)', topo.get('REPAS', 0))
        val_energie = topo.get('ENERGIE_(KG_CO2E)', topo.get('ENERGIE', 0))
        val_transp = topo.get('TRANSPORT_(KG_CO2E)', topo.get('TRANSPORT', 0))
        val_fourni = topo.get('FOURNITURES_(KG_CO2E)', topo.get('FOURNITURES', topo.get('CONSOMMABLES', 0)))

        c1.info(f"🍎 **Repas**\n\n {val_repas:,.0f} kg")
        c2.info(f"⚡ **Énergie**\n\n {val_energie:,.0f} kg")
        c3.info(f"🚌 **Transport**\n\n {val_transp:,.0f} kg")
        c4.info(f"📦 **Biens & Conso**\n\n {val_fourni:,.0f} kg")

# --- 5. PAGE GLOSSAIRE ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel Expert Carbone")
    st.markdown("Valeurs certifiées pour la conversion des unités scolaires.")
    
    tabs = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "📦 Biens & Conso"])
    
    with tabs[0]:
        st.subheader("Impact des Repas")
        st.write("- **Viande Rouge** : 7,26 kgCO2e / repas")
        st.write("- **Végétarien** : 0.50 kgCO2e / repas")
        
    with tabs[1]:
        st.subheader("Énergie")
        st.write("- **Électricité (FR)** : 0,06 kgCO2e/kWh")
        st.write("- **Climatisation (R410A)** : 2088 kgCO2e/kg")
        
    with tabs[2]:
        st.subheader("Déplacements")
        st.write("- **Autocar Scolaire** : 0,030 kgCO2e / km / passager")
        
    with tabs[3]:
        st.subheader("Biens et Consommables")
        st.markdown("""
        *   **Papier A4 (Ramette 500f)** : 2,62 kgCO2e (Calculé sur 2,5kg de papier).
        *   **Ordinateur Portable** : 161 kgCO2e (Fabrication).
        *   **Tablette numérique** : 65 kgCO2e (Fabrication).
        *   **Produits d'entretien** : ~1,5 kgCO2e par litre de concentré.
        """)
        st.info("Note : Pour les biens mobiliers, on compte l'empreinte de fabrication (émissions grises).")

st.sidebar.divider()
st.sidebar.caption("EPLE Bas Carbone - Source ADEME/GIEC")
