import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration de la page (Mode Large pour la place)
st.set_page_config(page_title="Mon Défi Carbone", layout="wide")

st.title("🌍 Mon Défi Carbone - Haut Vaucluse")

# 2. Identifiant du Sheets
sheet_id = "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"

# 3. Menu de sélection
etablissement = st.sidebar.selectbox("Choisir un établissement", ["GIONO", "EXUPERY"])

# 4. URL de lecture directe
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={etablissement}"

try:
    # Lecture des données
    df = pd.read_csv(url)
    
    # Nettoyage des noms de colonnes (enlève les espaces et met une majuscule)
    df.columns = [c.strip().capitalize() for c in df.columns]

    # --- MISE EN PAGE (2/3 tableau, 1/3 dashboard) ---
    col_table, col_dash = st.columns([2, 1])

    with col_table:
        st.subheader(f"📊 Tableau de synthèse : {etablissement}")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col_dash:
        st.subheader("🎯 Dashboard")
        
        # Vérification si les colonnes nécessaires existent
        if 'Poste' in df.columns and 'Total' in df.columns:
            # --- LE CAMEMBERT ---
            fig_pie = px.pie(
                df, 
                values='Total', 
                names='Poste',
                color_discrete_sequence=px.colors.sequential.RdBu,
                hole=0.3
            )
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.divider()
            
            # --- LA JAUGE (FUSÉE) ---
            st.subheader("🚀 Consommation Totale")
            total_conso = df['Total'].sum()
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_conso,
                title = {'text': "kg CO2e", 'font': {'size': 16}},
                gauge = {
                    'axis': {'range': [None, 5000]}, # À ajuster selon tes objectifs
                    'bar': {'color': "#ef553b"},
                    'steps': [
                        {'range': [0, 2000], 'color': "#e8f5e9"},
                        {'range': [2000, 4000], 'color': "#fff9c4"}
                    ],
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.warning("⚠️ Pour voir les graphiques, assure-toi d'avoir les colonnes 'Poste' et 'Total' dans ton Sheets.")

except Exception as e:
    st.error(f"Erreur lors de l'affichage des données : {e}")

st.caption("Projet EPLE Bas Carbone - Actualisation automatique via Google Sheets")
