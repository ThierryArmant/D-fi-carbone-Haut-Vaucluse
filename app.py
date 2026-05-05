import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Défi Carbone", layout="wide")

# --- FONCTION POUR LE FOND D'ÉCRAN ---
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
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# --- CONNEXION ET NETTOYAGE ---
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    df_raw = pd.read_csv(sheet_url)
    for i in range(len(df_raw)):
        if "Etablissements" in df_raw.iloc[i].values:
            new_cols = df_raw.iloc[i].values
            cleaned_cols = [str(c) if pd.notnull(c) else f"vide_{idx}" for idx, c in enumerate(new_cols)]
            df = df_raw.iloc[i+1:].copy()
            df.columns = cleaned_cols
            break

    df = df.loc[:, ~df.columns.str.contains('vide_')]
    col_nom = "Etablissements"
    col_pers = "conso carbone  par personne" # Nom exact de ta colonne
    df.columns = [str(c).strip() for c in df.columns]

    # Nettoyage de la donnée numérique
    if col_pers in df.columns:
        df[col_pers] = df[col_pers].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_pers] = pd.to_numeric(df[col_pers], errors='coerce').fillna(0)
    
    df = df.dropna(subset=[col_nom])
    # On trie pour le graphique
    df_sorted = df.sort_values(by=col_pers, ascending=True)

    st.markdown("<h3 style='text-align: center;'>🌱 Défi Carbone : Réseau Haut Vaucluse</h3>", unsafe_allow_html=True)
    
    # --- LIGNE 1 : COMPARAISON INDIVIDUELLE VS RÉPARTITION GLOBALE ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<p style='text-align: center; font-weight: bold;'>🏆 Intensité Carbone par Personne (kg CO2e/pers)</p>", unsafe_allow_html=True)
        # Utilisation d'un bar chart horizontal pour comparer les valeurs réelles
        fig_indiv = px.bar(
            df_sorted, 
            x=col_pers, 
            y=col_nom, 
            orientation='h',
            text=col_pers,
            color=col_pers,
            color_continuous_scale='RdYlGn_r' # Vert pour les petites conso, Rouge pour les grosses
        )
        fig_indiv.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_indiv.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_indiv, use_container_width=True)

    with col2:
        st.markdown("<p style='text-align: center; font-weight: bold;'>🎯 Répartition par Poste (Global)</p>", unsafe_allow_html=True)
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        cols_valides = [c for c in postes if c in df.columns]
        
        if cols_valides:
            for c in cols_valides:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            totaux = df[cols_valides].sum().reset_index()
            totaux.columns = ['Poste', 'Valeur']
            couleurs_perso = ['#2ecc71', '#ff8a80', '#fbc02d', '#3498db', '#f39c12']
            fig_postes = px.pie(totaux, values='Valeur', names='Poste', hole=0.4, color_discrete_sequence=couleurs_perso)
            fig_postes.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_postes, use_container_width=True)

    # --- LIGNE 2 : LE TABLEAU ---
    st.markdown("<p style='font-weight: bold; margin-top: 10px;'>📋 Détail des résultats</p>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=400, hide_index=True)

except Exception as e:
    st.error(f"Erreur technique : {e}")
