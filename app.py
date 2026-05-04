import streamlit as st
import pandas as pd

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    # Lecture brute
    df = pd.read_csv(sheet_url)
    
    # Recherche de la ligne de titre "Etablissements"
    for i in range(len(df)):
        if "Etablissements" in df.iloc[i].values:
            # On définit les titres manuellement pour éviter le bug de dedup_names
            df.columns = df.iloc[i]
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # On prépare les données pour le graphique
    col_nom = "Etablissements"
    col_data = "Total émissions"

    # On s'assure que les noms de colonnes sont propres
    df.columns = [str(c).strip() for c in df.columns]

    if col_data in df.columns:
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    
    # Nettoyage final
    df = df.dropna(subset=[col_nom])
    # On enlève les colonnes qui s'appellent "nan" ou qui n'ont pas de nom
    df = df.loc[:, df.columns.notnull()]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', na=False)]

    st.success("Synchronisation réussie !")

    # --- LE GRAPHIQUE ---
    st.subheader("📊 Comparaison des émissions par établissement")
    st.bar_chart(data=df, x=col_nom, y=col_data, color="#2ecc71")

    # --- LE TABLEAU ---
    st.subheader("📋 Détail des résultats")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"Erreur : {e}")
