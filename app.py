import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Défi Carbone", layout="wide")

st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="bilan carbone")
    st.success("Données synchronisées !")

    # --- AJOUT DU GRAPHIQUE ---
    st.subheader("📊 Émissions par établissement")
    
    # On utilise la colonne 'Etablissement' pour les noms 
    # et 'Total émissions (kg CO2e)' pour les barres
    st.bar_chart(data=df, x="Etablissement", y="Total émissions (kg CO2e)")

    # --- LE TABLEAU EN DESSOUS ---
    st.subheader("📋 Tableau de bord détaillé")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erreur : {e}")
