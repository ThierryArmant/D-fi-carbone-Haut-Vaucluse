import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Eco-Score EPLE - Référentiel Carbone",
    page_icon="🌿",
    layout="wide"
)

# --- 2. PARAMÈTRES ET URL ---
# URL de ton Google Sheets (format export CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/gviz/tq?tqx=out:csv&gid=1700157246"
CODE_SECRET = "MONCODE123" # À modifier selon ton choix

# --- 3. FONCTION DE CHARGEMENT SÉCURISÉE ---
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage critique des noms de colonnes (supprime espaces et met en majuscules)
        df.columns = df.columns.str.strip().str.upper()
        # Remplace les cases vides par 0 pour éviter les erreurs de calcul
        df = df.fillna(0)
        return df
    except Exception as e:
        st.error(f"Erreur de connexion au Google Sheets : {e}")
        return None

# --- 4. BARRE LATÉRALE (NAVIGATION) ---
st.sidebar.image("https://www.ademe.fr/wp-content/uploads/2022/05/logo-ademe.png", width=100)
st.sidebar.title("🌿 Menu Principal")
page = st.sidebar.radio("Navigation :", ["📊 Tableau de Bord", "📖 Glossaire Expert"])

# --- 5. LOGIQUE DES PAGES ---

# PAGE : TABLEAU DE BORD
if page == "📊 Tableau de Bord":
    st.title("📊 Bilan Carbone des Établissements")
    st.markdown("Visualisation des émissions et accès aux formulaires de saisie.")
    
    df = load_data()
    
    if df is not None:
        # Détection dynamique de la colonne établissement
        col_nom = 'ETABLISSEMENT' if 'ETABLISSEMENT' in df.columns else df.columns[0]
        
        # Sélecteur
        liste_etab = df[col_nom].unique()
        choix = st.selectbox("Choisir un établissement :", liste_etab)
        
        # Données de l'établissement
        topo = df[df[col_nom] == choix].iloc[0]
        
        # Affichage du Score Global (Jauge)
        # On cherche 'SCORE GLOBAL' ou on prend 0 par défaut
        score = topo.get('SCORE GLOBAL', 0)
        
        col_score1, col_score2 = st.columns([1, 2])
        with col_score1:
            st.metric(label="Impact par élève", value=f"{score:.2f} kgCO2e")
        with col_score2:
            if score < 150:
                st.success("Performance : Excellente (Classe A)")
            elif score < 350:
                st.warning("Performance : Moyenne (Classe C)")
            else:
                st.error("Performance : Alerte (Classe E)")
            st.progress(min(score/1000, 1.0)) # Barre de progression limitée à 100%

        st.divider()
        
        # Détails par Pôle
        st.subheader("Répartition par pôle de consommation")
        p1, p2, p3, p4 = st.columns(4)
        p1.write(f"🍎 **Alimentation**\n\n {topo.get('REPAS', 0)} kgCO2e")
        p2.write(f"⚡ **Énergie**\n\n {topo.get('ENERGIE', 0)} kgCO2e")
        p3.write(f"🚌 **Transports**\n\n {topo.get('TRANSPORT', 0)} kgCO2e")
        p4.write(f"📄 **Fournitures**\n\n {topo.get('PAPIER', 0)} kgCO2e")

        st.divider()
        
        # Accès Formulaire
        st.subheader("📝 Zone de Saisie")
        code_input = st.text_input("Entrez le code pour accéder au formulaire :", type="password")
        if code_input == CODE_SECRET:
            st.success("Code valide")
            st.link_button("Ouvrir le Formulaire de Saisie", "https://votre-lien-google-form")
        elif code_input != "":
            st.error("Code incorrect")

# PAGE : GLOSSAIRE EXPERT
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel Expert Carbone")
    st.markdown("Détails des facteurs d'émission basés sur l'**ADEME** et le **GIEC**.")
    
    t1, t2, t3, t4, t5 = st.tabs(["🍎 Repas", "❄️ Clim & Énergie", "🚌 Transports", "🗑️ Déchets", "💻 Numérique"])
    
    with t1:
        st.subheader("Pôle Alimentation")
        c1, c2, c3 = st.columns(3)
        c1.metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        c2.metric("Viande Blanche", "1.60 kg", "CO2e/repas")
        c3.metric("Végétarien", "0.50 kg", "CO2e/repas")
        st.info("Source ADEME : L'impact du bœuf inclut les émissions de méthane des ruminants.")

    with t2:
        st.subheader("Pôle Énergie")
        st.write("- **Électricité (France) :** 0.060 kgCO2e / kWh")
        st.write("- **Gaz Naturel :** 0.227 kgCO2e / kWh")
        st.write("- **Climatisation (R410A) :** 2088 kgCO2e / kg")
        st.warning("Expertise : 1 kg de fuite de gaz clim = 2 tonnes de CO2.")

    with t3:
        st.subheader("Pôle Transports")
        st.table({
            "Mode de transport": ["Autocar Scolaire", "Voiture thermique", "Voiture électrique", "Vélo / Marche"],
            "kgCO2e / km / passager": [0.030, 0.218, 0.050, 0.000]
        })

    with t4:
        st.subheader("Pôle Déchets")
        st.write("- **Ordures Ménagères :** 0.45 kgCO2e / kg")
        st.write("- **Gaspillage Pain :** 0.63 kgCO2e / kg")
        st.write("- **Papier/Carton Recyclé :** 0.02 kgCO2e / kg")

    with t5:
        st.subheader("Pôle Numérique")
        st.write("- **Ordinateur Portable :** 161 kgCO2e (Fabrication)")
        st.write("- **Écran Plat 24\" :** 350 kgCO2e (Fabrication)")
        st.write("- **Tablette :** 65 kgCO2e (Fabrication)")

# --- 6. FOOTER ---
st.sidebar.divider()
st.sidebar.caption("Développé pour le Projet EPLE Bas Carbone - 2026")
