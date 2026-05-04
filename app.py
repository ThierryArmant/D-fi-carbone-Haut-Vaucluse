import streamlit as st
import pandas as pd

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    # On lit le fichier mais on gère les colonnes en double
    df = pd.read_csv(sheet_url)
    
    # On cherche la ligne de titre "Etablissements"
    for i in range(len(df)):
        if "Etablissements" in df.iloc[i].values:
            # On récupère les noms des colonnes et on les rend uniques
            new_cols = df.iloc[i].values
            df.columns = pd.io.common.dedup_names(new_cols, is_resettable=True)
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # On prépare les données pour le graphique
    col_nom = "Etablissements"
    col_data = "Total émissions"

    if col_data in df.columns:
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    
    # On garde seulement les lignes avec un nom d'établissement
    df = df.dropna(subset=[col_nom])
    # On enlève les colonnes inutiles (celles qui n'ont pas de nom)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed|nan', na=False)]

    st.success("Données synchronisées et nettoyées !")

    # --- LE GRAPHIQUE ---
    st.subheader("📊 Comparaison des émissions par établissement")
    st.bar_chart(data=df, x=col_nom, y=col_data, color="#2ecc71")

    # --- LE TABLEAU ---
    st.subheader("📋 Détail des résultats")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"Note : {e}")
