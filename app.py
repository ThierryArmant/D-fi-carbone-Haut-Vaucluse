import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Défi Carbone Haut-Vaucluse", layout="wide")
st.title("🚗 Mon Défi Carbone - Suivi des émissions")

# 1. CONNEXION AU GOOGLE SHEETS
# Utilise la configuration 'gsheets' définie dans les Secrets de Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. LECTURE DES DONNÉES
# On lit le tableau en temps réel
df = conn.read()

# --- PARTIE AFFICHAGE (TES GRAPHIQUES) ---
st.subheader("📊 Récapitulatif de mes trajets")

if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Derniers enregistrements :")
        st.dataframe(df.tail(5)) # Affiche les 5 dernières lignes
    
    with col2:
        # Petit graphique simple pour voir l'évolution des KM
        fig = px.bar(df, x="Date", y="KM", color="Transport", title="KM par jour et transport")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Le tableau est vide pour le moment. Ajoutez un trajet ci-dessous !")

st.divider()

# --- PARTIE ACTION (TON BOUTON POUR MODIFIER) ---
st.subheader("📝 Ajouter un nouveau trajet")

with st.form("form_ajout"):
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        nouvelle_date = st.date_input("Date du trajet")
    with col_b:
        nouveaux_km = st.number_input("Nombre de KM", min_value=0.0, step=0.1)
    with col_c:
        nouveau_transport = st.selectbox("Moyen de transport", ["Voiture", "Bus", "Train", "Vélo"])
    
    bouton_valider = st.form_submit_button("Enregistrer dans le Google Sheets")

if bouton_valider:
    # On prépare la nouvelle ligne
    nouvelle_donnee = pd.DataFrame([{
        "Date": str(nouvelle_date),
        "KM": nouveaux_km,
        "Transport": nouveau_transport
    }])
    
    # On ajoute la ligne à l'ancien tableau
    df_mis_a_jour = pd.concat([df, nouvelle_donnee], ignore_index=True)
    
    # ON ENVOIE TOUT À GOOGLE SHEETS
    conn.update(data=df_mis_a_jour)
    
    st.success("✅ Données envoyées ! Le graphique va se mettre à jour.")
    st.balloons()
