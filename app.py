import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page en mode LARGE pour avoir de la place
st.set_page_config(page_title="Mon Défi Carbone", layout="wide")

st.title("🌍 Mon Défi Carbone - Haut Vaucluse")

# Connexion au Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données (on récupère toutes les feuilles)
# Note : Assure-toi que ton Sheets est toujours en "Accès public avec lien"
url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"
df = conn.read(spreadsheet=url)

# --- BARRE LATÉRALE ---
st.sidebar.header("Configuration")
# Liste des collèges (onglets du Sheets)
etablissement = st.sidebar.selectbox(
    "Choisir un établissement",
    ["GIONO", "EXUPERY"] # Ajoute tes autres collèges ici
)

# Chargement des données de l'établissement choisi
df_selection = conn.read(spreadsheet=url, worksheet=etablissement)

# --- MISE EN PAGE PRINCIPALE (2/3 et 1/3) ---
col_table, col_dash = st.columns([2, 1])

with col_table:
    st.subheader(f"📊 Données détaillées : {etablissement}")
    # On affiche le tableau proprement
    st.dataframe(df_selection, use_container_width=True, hide_index=True)

with col_dash:
    st.subheader("🎯 Dashboard")
    
    # 1. LE CAMEMBERT (Répartition des postes)
    # On suppose que tu as une colonne 'Poste' et une colonne 'Total' dans ton Sheets
    if 'Poste' in df_selection.columns and 'Total' in df_selection.columns:
        fig_pie = px.pie(
            df_selection, 
            values='Total', 
            names='Poste',
            color_discrete_sequence=px.colors.sequential.RdBu,
            hole=0.3 # Petit trou au milieu pour le style
        )
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Ajoute des colonnes 'Poste' et 'Total' pour voir le camembert.")

    st.divider()

    # 2. LA FUSÉE (Jauge de consommation totale)
    st.subheader("🚀 Niveau Global")
    if 'Total' in df_selection.columns:
        total_conso = df_selection['Total'].sum()
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = total_conso,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "kg CO2e", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [None, 5000]}, # 5000 est la limite haute, à ajuster
                'bar': {'color': "#ef553b"}, # Couleur rouge comme sur ton image
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 2000], 'color': '#ebf5eb'},
                    {'range': [2000, 4000], 'color': '#fcf3cf'}
                ],
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(t=30, b=0, l=30, r=30))
        st.plotly_chart(fig_gauge, use_container_width=True)

# Petite ligne de pied de page
st.caption("Données issues du projet Défi Carbone - Mise à jour en temps réel via Google Sheets.")
