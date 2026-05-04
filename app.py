import streamlit as st
import pandas as pd

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# Utilisation du GID que tu as trouvé
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    # Lecture des données
    df = pd.read_csv(sheet_url)
    
    # Nettoyage pour trouver le tableau dans la page
    # On cherche la ligne qui contient "Etablissement"
    for i in range(len(df)):
        if "Etablissement" in df.iloc[i].values:
            df.columns = df.iloc[i]
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # Conversion des chiffres (kg CO2e) en nombres réels pour le graphique
    col_co2 = "Total émissions (kg CO2e)"
    if col_co2 in df.columns:
        df[col_co2] = pd.to_numeric(df[col_co2], errors='coerce')
    
    # On enlève les lignes vides
    df = df.dropna(subset=["Etablissement"])

    st.success("Félicitations ! Connexion établie avec l'onglet Bilan Carbone.")

    # --- LE GRAPHIQUE ---
    st.subheader("📊 Comparaison des émissions par établissement")
    st.bar_chart(data=df, x="Etablissement", y=col_co2, color="#2ecc71")

    # --- LE TABLEAU ---
    st.subheader("📋 Détail des résultats")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"Oups, une petite erreur : {e}")
    st.write("Aperçu technique des données reçues :")
    st.dataframe(pd.read_csv(sheet_url).head(5))
