import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Défi Carbone Haut-Vaucluse", layout="wide")
st.title("🚗 Mon Défi Carbone - Suivi des émissions")

# 1. CONNEXION
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. CHOIX DE L'ÉTABLISSEMENT
# Ajoute ici tous les noms de tes onglets exactement comme dans Google Sheets
liste_etablissements = ["COLLEGE SAINT EXUPERY", "JEAN GIONO", "Lycée Pro A.BRIAND", "VICTOR SCHOELCHER", "Lycée Pro F.REVOUL", "Saint Jean le Batiste", "L.AUBRAC", "ES SAINT LOUIS", "COLLEGE H.BOUDON", "college P.Eluard", "Arausio", "COLLEGE VALLIS AERIA", "ARGENSOL", "college barbara", "lycée de l'arc", Lycée Viticole", "Ecole Jules Ferry", "école du grillon", "école curie"] 
choix = st.selectbox("Sélectionnez votre établissement :", liste_etablissements)

# 3. LECTURE DE L'ONGLET SÉLECTIONNÉ
try:
    df = conn.read(worksheet=choix)
    
    st.subheader(f"📊 Résultats pour l'établissement : {choix}")

    if not df.empty:
        # Nettoyage des colonnes (pour éviter les erreurs de calcul)
        df.columns = df.columns.str.strip()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("Derniers trajets :")
            st.dataframe(df.tail(10))
        
        with col2:
            if "KM" in df.columns and "Date" in df.columns:
                fig = px.bar(df, x="Date", y="KM", color="Transport" if "Transport" in df.columns else None, title=f"Évolution des KM - {choix}")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée enregistrée pour cet établissement.")

    st.divider()

    # 4. FORMULAIRE D'AJOUT
    st.subheader(f"📝 Ajouter un trajet pour {choix}")
    with st.form("form_ajout"):
        c1, c2, c3 = st.columns(3)
        with c1:
            date_saisie = st.date_input("Date")
        with c2:
            km_saisie = st.number_input("Nombre de KM", min_value=0.0, step=0.1)
        with c3:
            transport_saisie = st.selectbox("Transport", ["Voiture", "Bus", "Train", "Vélo"])
        
        valider = st.form_submit_button(f"Enregistrer pour {choix}")

    if valider:
        nouvelle_ligne = pd.DataFrame([{
            "Date": str(date_saisie),
            "KM": km_saisie,
            "Transport": transport_saisie
        }])
        df_final = pd.concat([df, nouvelle_ligne], ignore_index=True)
        
        # MISE À JOUR DE L'ONGLET SPÉCIFIQUE
        conn.update(worksheet=choix, data=df_final)
        st.success(f"✅ Données enregistrées dans l'onglet {choix} !")
        st.balloons()

except Exception as e:
    st.error(f"Erreur lors de la lecture de l'onglet '{choix}'. Vérifiez que le nom de l'onglet est exact.")
    st.write("Détail technique :", e)
