import streamlit as st

# Configuration de base
st.set_page_config(page_title="Défi Carbone 2026", layout="wide")

# Titre et texte d'accueil
st.title("🌱 Défi Carbone : Les 14 Établissements")
st.subheader("Suivi en temps réel de notre impact environnemental")

st.write("---")

# Simulation de l'affichage (On connectera ton Sheet après)
col1, col2 = st.columns(2)

with col1:
    st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?w=500", caption="Exemple d'établissement")
    st.metric(label="Consommation", value="450 kWh", delta="-5%")

with col2:
    st.info("Bientôt ici : Le classement de vos 14 établissements avec leurs photos et leurs données réelles.")
