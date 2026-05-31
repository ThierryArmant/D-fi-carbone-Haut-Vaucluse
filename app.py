import streamlit as st

# Titre principal centré ou aligné
st.markdown("<h2 style='text-align: center;'>🔍 Analyse Comparative des Émissions</h2>", unsafe_allow_html=True)
st.write("---")

# 1. Création des deux colonnes (50/50)
col_gauche, col_droite = st.columns(2)

# =====================================================================
# CÔTÉ GAUCHE : ANALYSE PAR ÉTABLISSEMENT
# =====================================================================
with col_gauche:
    st.markdown("### 🏫 Analyse détaillée par Établissement")
    
    # Le sélecteur d'établissement est placé en haut de la colonne gauche
    nom_ecole = st.selectbox(
        "Sélectionnez un établissement pour explorer ses statistiques :",
        options=["école curie", "école pasteur", "collège giono"], # À adapter avec votre liste dynamique
        key="select_etablissement"
    )
    
    st.write("") # Espacement alternatif
    
    # --- Exemple d'affichage des barres pour l'école sélectionnée ---
    # (Remplacez les valeurs dures par vos variables filtrées : ex: df_filtre['total'].sum())
    
    # Poste 1 : Énergie
    st.markdown("**❄️ Énergie & Bâtiments** <span style='float:right;'>**4.76 tonne - 3.9%**</span>", unsafe_allow_html=True)
    st.progress(0.039)
    with st.expander("📊 Détails du poste Énergie"):
        st.write("Détails spécifiques à l'établissement...")

    # Poste 2 : Alimentation
    st.markdown("**🍎 Alimentation & Cantine** <span style='float:right;'>**116.36 tonne - 96.0%**</span>", unsafe_allow_html=True)
    st.progress(0.96)
    with st.expander("📊 Détails du poste Alimentation"):
        st.write("Détails spécifiques à l'établissement...")

    # Poste 3 : Transports
    st.markdown("**🚌 Déplacements & Transports** <span style='float:right;'>**0.0 kg - 0.0%**</span>", unsafe_allow_html=True)
    st.progress(0.0)
    with st.expander("📊 Détails du poste Transports"):
        st.write("Détails spécifiques à l'établissement...")

    # Poste 4 : Consommables
    st.markdown("**📦 Biens, Consommables & Équipements** <span style='float:right;'>**24.98 tonne - 20.6%**</span>", unsafe_allow_html=True)
    st.progress(0.206)
    with st.expander("📊 Détails du poste Équipements & Consommables"):
        st.write("Détails spécifiques à l'établissement...")

    # Poste 5 : Déchets
    st.markdown("**🗑️ Gestion des Déchets** <span style='float:right;'>**0.0 kg - 0.0%**</span>", unsafe_allow_html=True)
    st.progress(0.0)


# =====================================================================
# CÔTÉ DROIT : TOTALITÉ DES ÉTABLISSEMENTS (GLOBAL)
# =====================================================================
with col_droite:
    st.markdown("### 🌍 Totalité des Établissements (Global)")
    
    # Petit message ou indicateur pour équilibrer la hauteur visuelle avec le selectbox de gauche
    st.info("Visualisation des postes les plus énergivores à l'échelle du territoire.")
    
    # --- Affichage des barres globales ---
    # (Ici, utilisez les sommes globales de votre dataframe : ex: df['energie'].sum())
    
    # Poste 1 : Énergie Global
    st.markdown("**❄️ Énergie & Bâtiments (Total)** <span style='float:right;'>**145.20 tonne - 18.5%**</span>", unsafe_allow_html=True)
    st.progress(0.185)
    with st.expander("🔍 Détails globaux Énergie"):
        st.write("Répartition globale de l'énergie...")

    # Poste 2 : Alimentation Global
    st.markdown("**🍎 Alimentation & Cantine (Total)** <span style='float:right;'>**412.10 tonne - 52.4%**</span>", unsafe_allow_html=True)
    st.progress(0.524)
    with st.expander("🔍 Détails globaux Alimentation"):
        st.write("Répartition globale de l'alimentation...")

    # Poste 3 : Transports Global
    st.markdown("**🚌 Déplacements & Transports (Total)** <span style='float:right;'>**120.40 tonne - 15.3%**</span>", unsafe_allow_html=True)
    st.progress(0.153)
    with st.expander("🔍 Détails globaux Transports"):
        st.write("Répartition globale des transports...")

    # Poste 4 : Consommables Global
    st.markdown("**📦 Biens, Consommables & Équipements (Total)** <span style='float:right;'>**85.30 tonne - 10.8%**</span>", unsafe_allow_html=True)
    st.progress(0.108)
    with st.expander("🔍 Détails globaux Équipements"):
        st.write("Répartition globale des consommables...")

    # Poste 5 : Déchets Global
    st.markdown("**🗑️ Gestion des Déchets (Total)** <span style='float:right;'>**24.10 tonne - 3.0%**</span>", unsafe_allow_html=True)
    st.progress(0.03)
