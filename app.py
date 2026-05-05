import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# --- CONNEXION ---
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    df = pd.read_csv(sheet_url)
    
    # Recherche de la ligne de titre
    for i in range(len(df)):
        if "Etablissements" in df.iloc[i].values:
            df.columns = df.iloc[i]
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # --- NETTOYAGE ---
    col_nom = "Etablissements"
    col_data = "conso carbone  par personne"

    df.columns = [str(c).strip() for c in df.columns]
    if col_data in df.columns:
        df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    
    df = df.dropna(subset=[col_nom])
    df = df.loc[:, df.columns.notnull()]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', na=False)]

    # --- CALCUL DE LA COULEUR DANS LE TABLEAU (Simple et fiable) ---
    def determiner_couleur(valeur):
        if valeur < 2000:
            return "#2ecc71" # Vert
        elif valeur <= 4000:
            return "#f39c12" # Orange
        else:
            return "#e74c3c" # Rouge

    df['color_hex'] = df[col_data].apply(determiner_couleur)

    st.success("Données synchronisées !")

    # --- GRAPHIQUE SIMPLIFIÉ ---
    st.subheader("📊 Analyse des émissions par établissement")

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{col_nom}:N", sort='-y', title="Établissements"),
        y=alt.Y(f"{col_data}:Q", title="Émissions (kg CO2e)"),
        color=alt.Color('color_hex:N', scale=None), # On utilise directement le code couleur du tableau
        tooltip=[col_nom, col_data]
    ).properties(height=450).interactive()

    st.altair_chart(chart, use_container_width=True)

    st.info("💡 **Seuils :** 🟢 < 2000 kg | 🟡 2000-4000 kg | 🔴 > 4000 kg")

    # --- TABLEAU ---
    st.subheader("📋 Détail des résultats")
    st.dataframe(df.drop(columns=['color_hex']), use_container_width=True)
    
except Exception as e:
    st.error(f"Erreur technique : {e}")
