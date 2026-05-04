import streamlit as st
import pandas as pd

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# Ton GID (onglet 5)
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    df = pd.read_csv(sheet_url)
    
    # On cherche la ligne qui contient ton nouveau mot "Etablissements"
    for i in range(len(df)):
        if "Etablissements" in df.iloc[i].values:
            df.columns = df.iloc[i]
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # On prépare les données pour le graphique
    # On s'assure que la colonne "Total" est bien lue comme des nombres
    if "Total" in df.columns:
        df["Total"] = pd.to_numeric(df["Total"], errors='coerce').fillna(0)
    
    # On nettoie les lignes vides
    df = df.dropna(subset=["Etablissements"])

    st.success("Données synchronisées avec succès !")

    # --- LE GRAPHIQUE ---
    st.subheader("📊 Comparaison des émissions par établissement")
    # Utilisation des noms exacts que tu as saisis
    st.bar_chart(data=df, x="Etablissements", y="Total", color="#2ecc71")

    # --- LE TABLEAU ---
    st.subheader("📋 Détail des résultats")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.write("Aperçu de ce que le site reçoit (vérifie les noms des colonnes) :")
    st.dataframe(pd.read_csv(sheet_url).head(5))
