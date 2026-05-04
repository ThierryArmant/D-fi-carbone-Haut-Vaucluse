import streamlit as st
import pandas as pd

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# Ton lien avec le bon GID
sheet_url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid=477228602"

try:
    # On lit le fichier en disant à Pandas que les titres sont à la ligne 1
    # Si ça ne marche pas, on essaiera header=1 ou header=2
    df = pd.read_csv(sheet_url)
    
    # NETTOYAGE : Supprime les lignes où il n'y a pas d'établissement
    df = df.dropna(subset=[df.columns[1]])

    st.success("Données chargées avec succès !")

    # --- GRAPHIQUE ---
    st.subheader("📊 Émissions par établissement")
    
    # On utilise le numéro des colonnes pour éviter l'erreur de nom
    # Colonne 1 = Établissements, Colonne 6 = Émissions
    st.bar_chart(data=df, x=df.columns[1], y=df.columns[6], color="#2ecc71")

    # --- TABLEAU ---
    st.subheader("📋 Tableau de bord")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"Erreur : {e}")
    st.write("Voici ce que le site voit dans ton fichier :")
    st.dataframe(pd.read_csv(sheet_url).head(5)) # Affiche les 5 premières lignes pour comprendre
