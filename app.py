import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# --- FONCTION DE CHARGEMENT DES DONNÉES ---
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
        # Ici ton code d'affichage des graphiques et données existant
        st.dataframe(data.head(10)) 
        
        st.divider()
        
        # --- SECTION ACCÈS FORMULAIRE ---
        st.subheader("📝 Saisie de données")
        code_saisi = st.text_input("Entrez le code secret pour accéder au formulaire :", type="password")
        
        if code_saisi == "MONCODE123": # À personnaliser
            st.success("Accès autorisé")
            st.link_button("Ouvrir le Formulaire de Saisie", "Lien_De_Ton_Formulaire_Google")
        elif code_saisi != "":
            st.error("Code incorrect")

# --- PAGE 2 : GLOSSAIRE EXPERT ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel Expert Carbone")
    st.markdown("""
    Ce référentiel permet de comprendre comment chaque donnée saisie est transformée en impact carbone. 
    Les calculs sont basés sur la **Base Empreinte de l'ADEME** et les rapports du **GIEC**.
    """)

    # Ajout des deux nouveaux onglets : Transports et Déchets
    tabs = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "🗑️ Déchets", "💻 Numérique", "📦 Consommables"])

    with tabs[0]:
        st.subheader("Pôle Restauration")
        with st.expander("🥩 Viande Rouge (Bœuf, Veau)"):
            st.write("**Facteur :** 7,26 kgCO2e par repas")
            st.info("Le bœuf émet du méthane (CH4) lors de la digestion, un gaz à effet de serre très puissant.")
        with st.expander("🍗 Viande Blanche (Poulet, Porc)"):
            st.write("**Facteur :** 1,60 kgCO2e par repas")
            st.info("L'impact vient surtout de la production de l'alimentation des animaux.")
        with st.expander("🥗 Repas Végétarien"):
            st.write("**Facteur :** 0,50 kgCO2e par repas")
            st.success("Impact 14 fois inférieur à la viande rouge.")

    with tabs[1]:
        st.subheader("Énergie et Fluides")
        with st.expander("❄️ Climatisation (Fluides frigorigènes)"):
            st.write("**Donnée :** kg de gaz rechargé lors de l'entretien.")
            st.warning("Certains gaz de clim ont un impact des milliers de fois supérieur au CO2 s'ils s'échappent.")
        with st.expander("⚡ Électricité"):
            st.write("**Facteur :** 0,06 kgCO2e / kWh")

    with tabs[2]:
        st.subheader("🚌 Pôle Transports")
        with st.expander("🚍 Autocar (Sorties scolaires)"):
            st.write("**Donnée :** Kilomètres totaux parcourus par le groupe.")
            st.write("**Mode de calcul :** On divise l'émission du car par le nombre d'élèves présents.")
            st.info("Plus l'autocar est rempli, plus l'empreinte carbone par élève diminue.")
        with st.expander("🚗 Voiture (Trajets domicile-travail)"):
            st.write("**Facteur moyen :** 0,21 kgCO2e / km")
            st.info("C'est l'un des postes les plus importants pour le personnel de l'établissement.")

    with tabs[3]:
        st.subheader("🗑️ Pôle Déchets")
        with st.expander("🚮 Ordures Ménagères (Bac Gris)"):
            st.write("**Donnée :** Poids total en kg.")
            st.info("L'impact vient du transport et de l'incinération (ou enfouissement) qui rejette du CO2.")
        with st.expander("🥖 Gaspillage alimentaire (Pain)"):
            st.write("**Expertise :** 1 kg de pain jeté = environ 0,6 kgCO2e.")
            st.warning("Jeter du pain, c'est jeter toute l'énergie utilisée pour cultiver le blé, le moudre et cuire le pain.")

    with tabs[4]:
        st.subheader("Matériel Informatique")
        with st.expander("💻 Ordinateurs et Tablettes"):
            st.write("**Facteur :** 161 kgCO2e par unité (Fabrication)")

    with tabs[5]:
        st.subheader("Fournitures")
        with st.expander("📄 Papier A4"):
            st.write("**Règle :** 1 ramette de 500 feuilles = 2,5 kg de papier.")
            st.write("**Facteur :** 1,05 kgCO2e / kg")

# Barre de pied de page
st.sidebar.divider()
st.sidebar.caption("Projet EPLE Bas Carbone - Expertise ADEME / GIEC")
