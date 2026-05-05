import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Défi Carbone", layout="wide")

# --- FONCTION POUR LE FOND D'ÉCRAN (DÉZOOMÉ) ---
def set_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://lh3.googleusercontent.com/d/1KA5uUEwfkuW99zl93_ngwq1dJ115zXrK");
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 80%; /* <--- MODIFIE CE % POUR DÉZOOMER (ex: 50% pour dézoomer beaucoup) */
            background-color: #f0f2f6; /* Couleur de secours pour les bords */
        }}
        
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 30px;
            border-radius: 15px;
            margin-top: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

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

    # --- NETTOYAGE ---
    col_nom = "Etablissements"
    col_data = "Total émissions"
    df.columns = [str(c).strip() for c in df.columns]

    if col_data in df.columns:
        df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    
    df = df.dropna(subset=[col_nom])
    df = df.loc[:, df.columns.notnull()]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', na=False)]

    st.success("Données synchronisées !")

    # --- 📊 GRAPHIQUE DU HAUT (MODE DÉROULABLE) ---
    st.subheader("📊 Analyse des émissions par établissement")
    chart_data = df[[col_nom, col_data]].set_index(col_nom)
    st.bar_chart(chart_data, height=300, use_container_width=True, color="#e74c3c")
    
    st.info("💡 **Seuils :** 🟢 < 2000 kg | 🟡 2000-4000 kg | 🔴 > 4000 kg")

    # --- 📋 TABLEAU ET CAMEMBERT ---
    col_gauche, col_droite = st.columns([1.8, 1.2])

    with col_gauche:
        st.subheader("📋 Détail des résultats")
        st.dataframe(df, use_container_width=True, height=350, hide_index=True)
    
    with col_droite:
        st.subheader("🎯 Répartition Globale")
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        cols_valides = [c for c in postes if c in df.columns]
        
        if cols_valides:
            for c in cols_valides:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            
            totaux = df[cols_valides].sum().reset_index()
            totaux.columns = ['Poste', 'Valeur']
            couleurs_perso = ['#2ecc71', '#ff8a80', '#fbc02d', '#3498db', '#f39c12']

            fig_pie = px.pie(
                totaux, values='Valeur', names='Poste', hole=0.4,
                color_discrete_sequence=couleurs_perso
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent')
            fig_pie.update_layout(
                height=350, 
                margin=dict(t=0, b=0, l=0, r=0), 
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.0)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
    st.error(f"Erreur technique : {e}")
