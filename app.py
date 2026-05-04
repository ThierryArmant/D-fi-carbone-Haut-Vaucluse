import streamlit as st
import pandas as pd

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# Lien direct (plus fiable pour l'instant)
sheet_url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid=477228602"

try:
    # Lecture des données
    df = pd.read_csv(sheet_url)
    
    st.success("Données synchronisées en temps réel !")

    # --- PARTIE GRAPHIQUE ---
    st.subheader("📊 Comparaison des émissions par établissement")
    
    # On crée le graphique
    # x="Etablissement" doit correspondre exactement au nom de ta colonne
    # y="Total émissions (kg CO2e)" doit correspondre aussi
    st.bar_chart(data=df, x="Etablissement", y="Total émissions (kg CO2e)", color="#2ecc71")

    # --- PARTIE TABLEAU ---
    st.subheader("📋 Détail des données")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"Erreur lors de l'affichage : {e}")
    st.info("Vérifiez que les noms des colonnes dans le code correspondent bien à ceux du Google Sheet.")
