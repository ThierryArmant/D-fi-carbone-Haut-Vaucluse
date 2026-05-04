import streamlit as st
import pandas as pd

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# Ton GID (onglet 5)
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    df = pd.read_csv(sheet_url)
    
    # On cherche la ligne qui contient "Etablissements"
    for i in range(len(df)):
        if "Etablissements" in df.iloc[i].values:
            df.columns = df.iloc[i]
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # --- NOM DES COLONNES (copiés de ton image) ---
    col_nom = "Etablissements"
    col_data = "Total émissions"

    # Conversion en nombres pour le graphique
    if col_data in df.columns:
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    
    # Nettoyage des lignes vides
    df = df.dropna(subset=[col_nom])

    st.success("Données synchronisées ! Tout est prêt.")

    # --- LE GRAPHIQUE ---
    st.subheader("📊 Comparaison des émissions par établissement")
    st.bar_chart(data=df, x=col_nom, y=col_data, color="#2ecc71")

    # --- LE TABLEAU ---
    st.subheader("📋 Détail des résultats")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"Erreur de lecture : {e}")
