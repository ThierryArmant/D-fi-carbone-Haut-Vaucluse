import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration de la page
st.set_page_config(page_title="Défi Carbone", layout="wide")

# --- STYLE CSS (FOND BLANC OPAQUE) ---
def set_bg_and_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://lh3.googleusercontent.com/d/1KA5uUEwfkuW99zl93_ngwq1dJ115zXrK");
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 60%;
            background-color: #f0f2f6;
        }}
        .main .block-container {{
            background-color: #ffffff; 
            padding: 1.5rem 2rem !important;
            border-radius: 12px;
            margin-top: 10px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
        }}
        [data-testid="stHeader"] {{ height: 0px; }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_and_style()

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
    col_pers = "conso carbone  par personne"
    df.columns = [str(c).strip() for c in df.columns]

    if col_pers in df.columns:
        df[col_pers] = pd.to_numeric(df[col_pers].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
    
    df = df.dropna(subset=[col_nom])

    # --- TITRE ---
    st.markdown("<h2 style='text-align: center; color: #1e3d59; margin-bottom: 10px;'>🌱 Consommation Carbone : Réseau Haut Vaucluse</h2>", unsafe_allow_html=True)

    # --- LIGNE 1 : TABLEAU DE PERFORMANCE ET JAUGE ---
    col_gauche, col_droite = st.columns([1.1, 0.9])

    with col_gauche:
        st.markdown("**📊 Classement par Établissement**")
        st.dataframe(
            df[[col_nom, col_pers]].sort_values(by=col_pers, ascending=False),
            column_config={
                col_nom: "Établissement",
                col_pers: st.column_config.ProgressColumn(
                    "Consommations Carbones",
                    help="kg CO2e par personne",
                    format="%.1f kg",
                    min_value=0,
                    max_value=float(df[col_pers].max() if not df.empty else 5000),
                ),
            },
            hide_index=True,
            use_container_width=True,
            height=350 
        )

    with col_droite:
        st.markdown("**🚀 Objectif : Rester sous les 2500 kg**")
        
        # Calcul de la moyenne du réseau pour la jauge
        valeur_moyenne = df[col_pers].mean() if not df.empty else 0
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = valeur_moyenne,
            number = {'suffix': " kg", 'font': {'size': 40}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 5000], 'tickwidth': 1},
                'bar': {'color': "#1e3d59"},
                'steps': [
                    {'range': [0, 1500], 'color': "#2ecc71"},   # Zone Verte (Top)
                    {'range': [1500, 2500], 'color': "#fbc02d"}, # Zone Jaune (Attention)
                    {'range': [2500, 5000], 'color': "#ff8a80"}  # Zone Rouge (Alerte)
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 5},
                    'thickness': 0.8,
                    'value': 2500 # Le trait rouge limite
                }
            }
        ))
        
        fig_gauge.update_layout(height=350, margin=dict(t=30, b=0, l=30, r=30))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # --- LIGNE 2 : TABLEAU DÉTAILLÉ ---
    st.markdown("---")
    st.markdown("**📋 Détails Complets (kg CO2e)**")
    st.dataframe(df, use_container_width=True, height=400, hide_index=True)

except Exception as e:
    st.error(f"Erreur lors de l'analyse : {e}")
