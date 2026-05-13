import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# --- FONCTION DE CHARGEMENT DES DONNÉES ---
# Remplace l'URL ci-dessous par l'URL de ton Google Sheets (format export=csv)
SHEET_URL = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/gviz/tq?tqx=out:csv&gid=1700157246"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"Erreur de connexion au Sheets : {e}")
        return None

# --- NAVIGATION ---
st.sidebar.title("🌿 Menu de Navigation")
page = st.sidebar.radio("Aller vers :", ["📊 Tableau de Bord", "📖 Glossaire Expert"])

# --- PAGE 1 : TABLEAU DE BORD ---
if page == "📊 Tableau de Bord":
    st.title("📊 Bilan Carbone des Établissements")
    
    data = load_data()
    
    if data is not None:
        # Affichage du tableau de bord (ton code actuel ici)
        st.dataframe(data.head(10)) # Exemple d'affichage
        
        st.divider()
        
        # --- SECTION ACCÈS FORMULAIRE ---
        st.subheader("📝 Saisie de données")
        # Le type="password" cache le code à la saisie
        code_saisi = st.text_input("Entrez le code secret pour accéder au formulaire :", type="password")
        
        if code_saisi == "MONCODE123": # Remplace par ton vrai code
            st.success("Accès autorisé")
            st.link_button("Ouvrir le Formulaire de Saisie", "Lien_De_Ton_Formulaire_Google")
        elif code_saisi != "":
            st.error("Code incorrect")

# --- PAGE 2 : GLOSSAIRE EXPERT ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel Expert Carbone")
    st.markdown("""
    Ce glossaire répertorie les données utilisées pour le calcul de l'empreinte carbone. 
    Il s'appuie sur les bases de données de l'**ADEME**, du **PEBC** et les rapports du **GIEC**.
    """)

    tabs = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "💻 Numérique", "📦 Consommables"])

    with tabs[0]:
        st.subheader("Pôle Restauration")
        
        with st.expander("🥩 Viande Rouge (Bœuf, Veau)"):
            st.write("**Facteur :** 7,26 kgCO2e par repas")
            st.info("Pourquoi ? Les ruminants produisent du méthane (CH4) lors de la digestion. Ce gaz a un pouvoir réchauffant 28 fois supérieur au CO2.")
            
        with st.expander("🍗 Viande Blanche (Poulet, Porc)"):
            st.write("**Facteur :** 1,60 kgCO2e par repas")
            st.info("Pourquoi ? Pas de méthane ici. L'impact vient surtout des cultures (soja, maïs) pour nourrir les animaux.")

        with st.expander("🐟 Poisson"):
            st.write("**Facteur :** 2,00 kgCO2e par repas")
            st.info("Pourquoi ? Principalement lié au carburant consommé par les bateaux de pêche.")

        with st.expander("🥗 Repas Végétarien"):
            st.write("**Facteur :** 0,50 kgCO2e par repas")
            st.success("C'est le choix le plus performant pour réduire l'empreinte de l'établissement.")

    with tabs[1]:
        st.subheader("Énergie et Fluides")
        
        with st.expander("❄️ Climatisation (Fluides frigorigènes)"):
            st.write("**Donnée à chercher :** Masse de gaz rechargée (kg) lors de la maintenance.")
            st.warning("Attention : On ne parle pas ici de l'électricité, mais des gaz internes. Une fuite de 1kg de fluide peut équivaloir à plusieurs tonnes de CO2 !")
            
        with st.expander("⚡ Électricité"):
            st.write("**Facteur :** 0,06 kgCO2e / kWh")
            st.info("Mix électrique français : très bas carbone grâce au nucléaire et au renouvelable.")

    with tabs[2]:
        st.subheader("Matériel Informatique")
        
        with st.expander("💻 Ordinateurs et Tablettes"):
            st.write("**Facteur :** Environ 161 kgCO2e par unité (Fabrication)")
            st.info("Plus de 80% de l'impact d'un ordinateur a lieu AVANT son premier allumage, lors de l'extraction des métaux.")

    with tabs[3]:
        st.subheader("Fournitures")
        
        with st.expander("📄 Papier A4"):
            st.write("**Unité de saisie :** Nombre de ramettes")
            st.write("**Règle de conversion :** 1 ramette de 500 feuilles = 2,5 kg de papier.")
            st.info("Le papier recyclé permet de réduire cet impact car il demande moins d'énergie de transformation.")

# Barre de pied de page
st.sidebar.divider()
st.sidebar.caption("Projet EPLE Bas Carbone - Expertise ADEME / GIEC")
