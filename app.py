import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page (Mode Dashboard compact)
st.set_page_config(page_title="Défi Carbone", layout="wide")

# --- FONCTION POUR LE FOND D'ÉCRAN DÉZOOMÉ ---
def set_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://lh3.googleusercontent.com/d/1KA5uUEwfkuW99zl93_ngwq1dJ115zXrK");
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 75%;
            background-color: #f0f2f6;
        }}
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.92);
            padding: 1rem 2rem;
            border-radius: 15px;
            margin-top: 10px;
        }}
        /* Réduction des espaces entre les éléments pour optimiser la place */
        div.stMarkdown {{ margin-bottom: -10px; }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# --- CONNEXION ET NETTOYAGE ANTI-BUG ---
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    df_raw = pd.read_csv(sheet_url)
    
    # Correction du bug "nan" : on cherche la ligne de titre
    for i in range(len(df_raw)):
        if "Etablissements" in df_raw.iloc[i].values:
            new_cols = df_raw.iloc[i].values
            cleaned_cols = [str(c) if pd.notnull(c) else f"vide_{idx}" for idx, c in enumerate(new_cols)]
            df = df_raw.iloc[i+1:].copy()
            df.columns = cleaned_cols
            break

    # Nettoyage final des colonnes inutiles
    df = df.loc[:, ~df.columns.str.contains('vide_')]
    col_nom = "Etablissements"
    col_data = "Total émissions"
    df.columns = [str(c).strip() for c in df.columns]

    if col_data in df.columns:
        df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    
    df = df.dropna(subset=[col_nom])

    # --- AFFICHAGE (Titre) ---
    st.markdown("<h3 style='text-align: center;'>🌱 Défi Carbone : Réseau Haut Vaucluse</h3>", unsafe_allow_html=True)
    
    # --- LIGNE 1 : LES CAMEMBERTS (Côte à côte) ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<p style='text-align: center; font-weight: bold;'>🏫 Par Établissement et par personne</p>", unsafe_allow_html=True)
        fig_etab = px.pie(df, values=col_data, names=col_nom, hole=0.4)
        fig_etab.update_traces(textposition='inside', textinfo='percent')
        fig_etab.update_layout(height=280, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_etab, use_container_width=True)

    with col2:
        st.markdown("<p style='text-align: center; font-weight: bold;'>🎯 Par Poste (Global)</p>", unsafe_allow_html=True)
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
            fig_postes.update_layout(height=280, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_postes, use_container_width=True)

    # --- LIGNE 2 : LE TABLEAU (HAUTEUR AUGMENTÉE) ---
    st.markdown("<p style='font-weight: bold; margin-top: 10px;'>📋 Détail des résultats</p>", unsafe_allow_html=True)
    # Hauteur passée à 400px pour qu'il occupe plus d'espace
    st.dataframe(df, use_container_width=True, height=400, hide_index=True)

except Exception as e:
    st.error(f"Erreur technique : {e}")
