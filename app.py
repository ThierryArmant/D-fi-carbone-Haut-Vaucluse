import streamlit as st
import pandas as pd

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# Lien direct SANS passer par les secrets
# On utilise le format /export?format=csv pour forcer la lecture
sheet_url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid=477228602"

try:
    df = pd.read_csv(sheet_url)
    st.success("Connexion réussie via lien direct !")
    
    st.subheader("📊 Aperçu des données")
    st.dataframe(df)
    
except Exception as e:
    st.error(f"Nouvelle erreur : {e}")
