import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# --- 1. CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/gviz/tq?tqx=out:csv&gid=1700157246"

@st.cache_data(ttl=60)
def load_data():
    try:
        # Lecture du CSV depuis Google Sheets
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return None

# --- 2. NAVIGATION ---
st.sidebar.title("🌿 Menu de Navigation")
page = st.sidebar.radio("Aller vers :", ["📊 Tableau de Bord", "📖 Glossaire Expert"])

# --- 3. PAGE : TABLEAU DE BORD (Page principale) ---
if page == "📊 Tableau de Bord":
    st.title("📊 Bilan Carbone des Établissements")
    
    df = load_data()
    
    if df is not None:
        # --- ICI TU PEUX REMETTRE TES JAUGES ET GRAPHIQUES ---
        # Exemple pour afficher ton tableau principal :
        st.subheader("Situation actuelle des établissements")
        st.dataframe(df, use_container_width=True)
        
        # Exemple : Si tu avais un graphique spécifique, insère son code ici
        # st.bar_chart(df.set_index('ETABLISSEMENT')['TOTAL EMISSIONS'])

        st.divider()
        
        # --- SECTION ACCÈS FORMULAIRE ---
        st.subheader("📝 Saisie de nouvelles données")
        code_saisi = st.text_input("Code accès formulaire :", type="password")
        
        if code_saisi == "VOTRE_CODE": # Remplace par ton code
            st.success("Accès autorisé")
            st.link_button("Accéder au Formulaire Google", "TON_LIEN_VERS_LE_FORMULAIRE")

# --- 4. PAGE : GLOSSAIRE EXPERT ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel Précis des Facteurs d'Émission")
    st.markdown("Sources : **ADEME**, **GIEC**, **PEBC**.")

    tabs = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "🗑️ Déchets", "💻 Numérique"])

    with tabs[0]:
        st.subheader("Pôle Restauration (Données ADEME)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        c2.metric("Viande Blanche", "1.60 kg", "CO2e/repas")
        c3.metric("Poisson", "2.00 kg", "CO2e/repas")
        c4.metric("Végétarien", "0.50 kg", "CO2e/repas")

    with tabs[1]:
        st.subheader("Énergie & Fluides")
        st.write("**Gaz Naturel :** 0.227 kgCO2e / kWh")
        st.write("**Électricité :** 0.060 kgCO2e / kWh")
        st.write("**Climatisation (R410A) :** 2088 kgCO2e / kg")

    with tabs[2]:
        st.subheader("🚌 Transports")
        st.table({
            "Mode": ["Autocar", "Voiture", "Vélo"],
            "kgCO2e/km": [0.030, 0.218, 0.000]
        })

    with tabs[3]:
        st.subheader("🗑️ Déchets")
        st.write("- **Ordures Ménagères :** 0.45 kgCO2e / kg")
        st.write("- **Gaspillage Pain :** 0.63 kgCO2e / kg")

    with tabs[4]:
        st.subheader("💻 Numérique")
        st.write("- **Ordinateur Portable :** 161 kgCO2e")
        st.write("- **Écran Plat :** 350 kgCO2e")

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("Projet EPLE Bas Carbone")
