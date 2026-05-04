import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Défi Carbone Haut-Vaucluse", layout="wide")
st.title("🚗 Mon Défi Carbone - Suivi des émissions")

# 1. CONNEXION
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. DICTIONNAIRE DES ETABLISSEMENTS
# A gauche : le nom qui s'affiche sur le site
# A droite : le nom EXACT de l'onglet dans ton Google Sheets
etablissements = {
    "Collège Saint-Exupéry": "EXUPERY",
    "Lycée Jean Giono": "GIONO",
    "Lycée Pro A. Briand": "BRIAND",
    "Collège Victor Schoelcher": "SCHOELCHER",
    "Lycée Pro F. Revoul": "REVOUL",
    "Saint Jean le Baptiste": "BAPTISTE",
    "Lycée Lucie Aubrac": "AUBRAC",
    "Saint Louis": "ST_LOUIS",
    "Collège Henri Boudon": "BOUDON",
    "Collège Paul Éluard": "ELUARD",
    "Arausio": "ARAUSIO",
    "Collège Vallis Aeria": "VALLIS_AERIA",
    "Argensol": "ARGENSOL",
    "Collège Barbara": "HENDRICKS",
    "Lycée de l'Arc": "ARC",
    "Lycée Viticole": "VITICOLE",
    "École Jules Ferry": "FERRY",
    "École du Grillon": "GRILLON",
    "École Curie": "CURIE"
}

# 3. INTERFACE DE SÉLECTION
choix_joli = st.selectbox("Sélectionnez votre établissement :", list(etablissements.keys()))
nom_onglet_reel = etablissements[choix_joli]

# 4. LECTURE DES DONNÉES
try:
    # On lit l'onglet simplifié (ex: GIONO)
    # ttl=0 permet de voir les changements immédiatement
    df = conn.read(worksheet=nom_onglet_reel, ttl=0)
    
    if df is not None and not df.empty:
        st.subheader(f"📊 Résultats pour : {choix_joli}")
        
        # Affichage du tableau
        st.write("Derniers trajets enregistrés :")
        st.dataframe(df.tail(10))
        
        # Graphique si les colonnes existent
        if "KM" in df.columns and "Date" in df.columns:
            fig = px.bar(df, x="Date", y="KM", title=f"Consommation KM - {choix_joli}")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"L'onglet '{nom_onglet_reel}' est vide ou n'a pas encore de données.")

except Exception as e:
    st.error(f"Impossible d'ouvrir l'onglet '{nom_onglet_reel}'")
    st.info("Vérifiez que vous avez bien renommé vos onglets dans Google Sheets comme convenu.")

st.divider()

# 5. FORMULAIRE D'AJOUT
st.subheader(f"📝 Ajouter un trajet pour {choix_joli}")
with st.form("form_ajout"):
    c1, c2, c3 = st.columns(3)
    with c1:
        date_saisie = st.date_input("Date")
    with c2:
        km_saisie = st.number_input("Nombre de KM", min_value=0.0, step=0.1)
    with c3:
        transport_saisie = st.selectbox("Transport", ["Voiture", "Bus", "Train", "Vélo"])
    
    valider = st.form_submit_button("Enregistrer le trajet")

if valider:
    try:
        # On prépare la nouvelle ligne
        nouvelle_ligne = pd.DataFrame([{
            "Date": str(date_saisie),
            "KM": km_saisie,
            "Transport": transport_saisie
        }])
        
        # On fusionne avec l'existant
        df_final = pd.concat([df, nouvelle_ligne], ignore_index=True)
        
        # On renvoie tout vers le bon onglet
        conn.update(worksheet=nom_onglet_reel, data=df_final)
        st.success(f"✅ Trajet enregistré avec succès pour {choix_joli} !")
        st.balloons()
    except Exception as e:
        st.error("Erreur lors de l'enregistrement.")
        st.write(e)
