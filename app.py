import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Défi Carbone", layout="wide")

# --- STYLE CSS ÉPURÉ (FOND BLANC OPAQUE) ---
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
            padding: 1rem 2rem !important;
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

    # Conversion numérique
    if col_pers in df.columns:
        df[col_pers] = pd.to_numeric(df[col_pers].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
    
    df = df.dropna(subset=[col_nom])

    # --- TITRE ---
    st.markdown("<h2 style='text-align: center; color: #1e3d59; margin-bottom: 10px;'>🌱 Consommation Carbone : Réseau Haut Vaucluse</h2>", unsafe_allow_html=True)

    # --- MISE EN PAGE : 2 COLONNES ---
    col_gauche, col_droite = st.columns([1.2, 0.8])

    with col_gauche:
        st.markdown("**📊 Performance Individuelle (kg CO2e/pers)**")
        # ICI ON UTILISE LA FORMULE DU TABLEAU DU BAS POUR LE HAUT
        # On crée une colonne avec des barres visuelles dans le tableau
        st.dataframe(
            df[[col_nom, col_pers]].sort_values(by=col_pers, ascending=False),
            column_config={
                col_nom: "Établissement",
                col_pers: st.column_config.ProgressColumn(
                    "Intensité Carbone",
                    help="Consommation par personne",
                    format="%.1f kg",
                    min_value=0,
                    max_value=float(df[col_pers].max()),
                ),
            },
            hide_index=True,
            use_container_width=True,
            height=350 # Même hauteur que ton camembert
        )

    with col_droite:
        st.markdown("**🎯 Répartition par Poste (Global)**")
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        cols_valides = [c for c in postes if c in df.columns]
        if cols_valides:
            temp_df = df[cols_valides].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce')).sum().reset_index()
            temp_df.columns = ['Poste', 'Valeur']
            fig_pie = px.pie(temp_df, values='Valeur', names='Poste', hole=0.4, 
                             color_discrete_sequence=['#2ecc71', '#ff8a80', '#fbc02d', '#3498db', '#f39c12'])
            fig_pie.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- LE GRAND TABLEAU DU BAS (L'original) ---
    st.markdown("---")
    st.markdown("**📋 Détails Complets des Emissions**")
    st.dataframe(df, use_container_width=True, height=400, hide_index=True)

except Exception as e:
    st.error(f"Erreur : {e}")
