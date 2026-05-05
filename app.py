import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Config large
st.set_page_config(page_title="Mon Défi Carbone", layout="wide")

st.title("🌍 Mon Défi Carbone - Haut Vaucluse")

# 2. Lien du Google Sheets (Vérifie bien que c'est le bon)
url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"

# 3. Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Sélection de l'établissement dans la barre latérale
etablissement = st.sidebar.selectbox(
    "Choisir un établissement",
    ["JEAN GIONO", "PAUL ELUARD"] 
)

# 5. Lecture UNIQUE (On ne lit que l'onglet sélectionné)
try:
    df_selection = conn.read(spreadsheet=url, worksheet=etablissement)
    
    # --- MISE EN PAGE 2/3 et 1/3 ---
    col_table, col_dash = st.columns([2, 1])

    with col_table:
        st.subheader(f"📊 Données : {etablissement}")
        st.dataframe(df_selection, use_container_width=True, hide_index=True)

    with col_dash:
        st.subheader("🎯 Dashboard")
        
        # On cherche les colonnes automatiquement (même si majuscules différentes)
        df_selection.columns = [c.strip().capitalize() for c in df_selection.columns]
        
        if 'Poste' in df_selection.columns and 'Total' in df_selection.columns:
            # Camembert
            fig_pie = px.pie(df_selection, values='Total', names='Poste', hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Fusée (Jauge)
            total = df_selection['Total'].sum()
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total,
                title = {'text': "kg CO2e"},
                gauge = {'axis': {'range': [None, 5000]}, 'bar': {'color': "#ef553b"}}
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.warning("Vérifiez que vos colonnes s'appellent 'Poste' et 'Total' dans Excel.")

except Exception as e:
    st.error("Impossible de lire le fichier. Vérifiez que le partage est bien sur 'Tous les utilisateurs disposant du lien'.")
