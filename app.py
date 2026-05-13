import streamlit as st
import pandas as pd

# Configuration
st.set_page_config(page_title="Eco-Score EPLE", layout="wide")

# --- NAVIGATION ---
st.sidebar.title("🌿 Menu de Navigation")
page = st.sidebar.radio("Aller vers :", ["📊 Tableau de Bord", "📖 Glossaire Expert"])

# --- PAGE 1 : TABLEAU DE BORD ---
if page == "📊 Tableau de Bord":
    st.title("📊 Bilan Carbone des Établissements")
    st.write("Bienvenue sur le dashboard. Sélectionnez un autre onglet dans le menu de gauche pour voir le glossaire.")
    
    # --- TA SECTION CODE SECRET (exemple) ---
    st.divider()
    code_saisi = st.text_input("Code accès formulaire :", type="password")
    if code_saisi == "MONCODE123":
        st.success("Accès autorisé")

# --- PAGE 2 : GLOSSAIRE EXPERT (L'endroit où l'erreur se produisait) ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel Précis des Facteurs d'Émission")
    st.markdown("Sources : **ADEME (Base Empreinte)**, **GIEC**, **PEBC**.")

    tabs = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "🗑️ Déchets", "💻 Numérique"])

    with tabs[0]:
        st.subheader("Pôle Restauration (Données ADEME)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        c2.metric("Viande Blanche", "1.60 kg", "CO2e/repas")
        c3.metric("Poisson", "2.00 kg", "CO2e/repas")
        c4.metric("Végétarien", "0.50 kg", "CO2e/repas")
        st.info("**Expertise GIEC :** La viande rouge est impactante car les bovins émettent du méthane (CH4), un gaz 28 fois plus puissant que le CO2.")

    with tabs[1]:
        st.subheader("Énergie & Fluides (Données PEBC/ADEME)")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.write("**Électricité (France) :** 0.060 kgCO2e / kWh")
            st.write("**Gaz Naturel :** 0.227 kgCO2e / kWh")
        with col_e2:
            st.write("**Fioul Domestique :** 3.24 kgCO2e / Litre")
            st.write("**Climatisation (R410A) :** 2088 kgCO2e / kg")
        st.warning("**Alerte Expert :** 1 kg de gaz de clim qui fuit = 2 tonnes de CO2 (soit 1 an de chauffage gaz d'une maison).")

    with tabs[2]:
        st.subheader("🚌 Pôle Transports (Données ADEME)")
        st.write("Valeurs moyennes par passager au kilomètre :")
        st.table({
            "Mode": ["Autocar Scolaire", "Voiture thermique", "Voiture électrique", "Vélo / Marche"],
            "kgCO2e / km": [0.030, 0.218, 0.050, 0.000]
        })

    with tabs[3]:
        st.subheader("🗑️ Pôle Déchets (Données ADEME)")
        st.write("- **Ordures Ménagères (Bac Gris) :** 0.45 kgCO2e / kg")
        st.write("- **Gaspillage Pain :** 0.63 kgCO2e / kg")
        st.write("- **Papier/Carton (Recyclé) :** 0.02 kgCO2e / kg")
        st.info("**Poids d'une ramette A4 (500 f.) :** 2,5 kg.")

    with tabs[4]:
        st.subheader("💻 Pôle Numérique (Données PEBC)")
        st.write("Impact lié à la fabrication (Émissions grises) :")
        st.write("- **Ordinateur Portable :** 161 kgCO2e")
        st.write("- **Écran Plat (24\") :** 350 kgCO2e")
        st.write("- **Tablette :** 65 kgCO2e")
