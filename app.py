import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page (on force le mode large)
st.set_page_config(page_title="Défi Carbone", layout="wide")

# --- FOND D'ÉCRAN DÉZOOMÉ ---
def set_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://lh3.googleusercontent.com/d/1KA5uUEwfkuW99zl93_ngwq1dJ115zXrK");
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 70%; /* Dézoomé pour laisser respirer */
            background-color: #f0f2f6;
        }}
        /* Réduction des marges pour tout faire tenir */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 1.5rem 3rem;
            border-radius: 15px;
            margin-top: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# Titre compact
st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>🌱 Défi Carbone : Réseau Haut Vaucluse</h2>", unsafe_allow_html=True)

# --- CONNEXION ---
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    df = pd.read_csv(sheet_url)
    for i in range(len(df)):
        if "Etablissements" in df.iloc[i].values:
            df.columns = df.iloc[i]
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # Nettoyage
    col_nom = "Etablissements"
    col_data = "Total émissions"
    df.columns = [str(c).strip() for c in df.columns]
    if col_data in df.columns:
        df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    df = df.dropna(subset=[col_nom])

    # --- LIGNE 1 : LES GRAPHIQUES (Côte à côte) ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4 style='text-align: center;'>🏫 Par Établissement</h4>", unsafe_allow_html=True)
        fig_etab = px.pie(df, values=col_data, names=col_nom, hole=0.4)
        fig_etab.update_traces(textposition='inside', textinfo='percent')
        fig_etab.update_layout(height=320, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_etab, use_container_width=True)

    with col2:
        st.markdown("<h4 style='text-align: center;'>🎯 Par Poste (Global)</h4>", unsafe_allow_html=True)
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        cols_valides = [c for c in postes if c in df.columns]
        if cols_valides:
            for c in cols_valides:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            totaux = df[cols_valides].sum().reset_index()
            totaux.columns = ['Poste', 'Valeur']
            couleurs_perso = ['#2ecc71', '#ff8a80', '#fbc02d', '#3498db', '#f39c12']
            fig_postes = px.pie(totaux, values='Valeur', names='Poste', hole=0.4, color_discrete_sequence=couleurs_perso)
            fig_postes.update_traces(textposition='inside', textinfo='percent')
            fig_postes.update_layout(height=320, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_postes, use_container_width=True)

    # --- LIGNE 2 : LE TABLEAU (Fini le scroll de page) ---
    st.markdown("<h4 style='margin-top: 0;'>📋 Détail des résultats</h4>", unsafe_allow_html=True)
    # On force une hauteur de 250px : le tableau aura son propre scroll interne
    st.dataframe(df, use_container_width=True, height=250, hide_index=True)

except Exception as e:
    st.error(f"Erreur : {e}")
