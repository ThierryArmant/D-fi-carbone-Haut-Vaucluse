import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration large
st.set_page_config(page_title="Défi Carbone : Réseau Haut Vaucluse", layout="wide")

st.title("🌍 Défi Carbone : Réseau Haut Vaucluse")

# 2. Identifiant du Sheets
sheet_id = "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"
onglet_principal = "GIONO" # L'onglet qui contient la liste de tous les collèges

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={onglet_principal}"

try:
    # Lecture des données
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]

    # --- GRAPHIQUE DU HAUT (Statistiques par établissement) ---
    st.subheader("📊 Analyse des émissions par établissement")
    if 'Etablissement' in df.columns and 'Total émissions' in df.columns:
        fig_top = px.bar(df, x='Etablissement', y='Total émissions', color_discrete_sequence=['#e74c3c'])
        fig_top.update_layout(height=350)
        st.plotly_chart(fig_top, use_container_width=True)
    
    st.divider()

    # --- MISE EN PAGE INFÉRIEURE ---
    col_gauche, col_droite = st.columns([2, 1])

    with col_gauche:
        st.subheader("📑 Détail des résultats")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col_droite:
        st.subheader("🎯 Dashboard Global")
        
        # On calcule les totaux par poste pour l'ensemble des établissements
        # On additionne les colonnes de consommation
        colonnes_conso = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        
        # Vérification si ces colonnes existent
        existantes = [c for c in colonnes_conso if c in df.columns]
        
        if existantes:
            # Somme de chaque poste pour le camembert
            somme_postes = df[existantes].sum().reset_index()
            somme_postes.columns = ['Poste', 'Valeur']

            # 1. LE CAMEMBERT GLOBAL
            fig_pie = px.pie(somme_postes, values='Valeur', names='Poste', hole=0.4)
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.divider()
            
            # 2. LA FUSÉE (Consommation totale cumulée)
            total_reseau = somme_postes['Valeur'].sum()
            st.metric("Total Réseau (kg CO2e)", f"{total_reseau:,.0f}")
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_reseau,
                gauge = {
                    'axis': {'range': [None, 2000000]}, # Ajusté pour le réseau global
                    'bar': {'color': "#e74c3c"},
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

except Exception as e:
    st.error(f"Erreur : {e}")

st.caption("Données synchronisées - Réseau Haut Vaucluse")
