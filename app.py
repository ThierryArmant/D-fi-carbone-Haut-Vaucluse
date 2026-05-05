import streamlit as st
import pandas as pd
import plotly.express as px

# Config
st.set_page_config(layout="wide")
st.title("🌍 Mon Défi Carbone")

# L'URL magique pour lecture directe sans robot
sheet_id = "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"

etablissement = st.sidebar.selectbox("Choisir un établissement", ["GIONO", "EXUPERY"])

# Construction de l'URL de téléchargement direct
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={etablissement}"

try:
    # Lecture directe du CSV
    df = pd.read_csv(url)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Données : {etablissement}")
        st.dataframe(df, use_container_width=True)
        
    with col2:
        st.subheader("Dashboard")
        # On vérifie si les colonnes existent pour le graphique
        if 'Poste' in df.columns and 'Total' in df.columns:
            fig = px.pie(df, values='Total', names='Poste')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Les colonnes 'Poste' et 'Total' sont nécessaires pour le graphique.")

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
