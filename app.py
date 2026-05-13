# --- PAGE 2 : GLOSSAIRE EXPERT (VERSION PRÉCISE ADEME/GIEC) ---
elif page == "📖 Glossaire Expert":
    st.title("📖 Référentiel Précis des Facteurs d'Émission")
    st.markdown("""
    Voici les valeurs de référence utilisées pour convertir vos consommations en **kg CO2 équivalent (kgCO2e)**.
    """)

    tabs = st.tabs(["🍎 Alimentation", "❄️ Énergie & Clim", "🚌 Transports", "🗑️ Déchets", "💻 Numérique"])

    with tabs[0]:
        st.subheader("Pôle Restauration (Données ADEME)")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Viande Rouge", "7.26 kgCO2e", "par repas")
            st.metric("Viande Blanche", "1.60 kgCO2e", "par repas")
        with col2:
            st.metric("Poisson", "2.00 kgCO2e", "par repas")
            st.metric("Végétarien", "0.50 kgCO2e", "par repas")
        st.info("**Le saviez-vous ?** Un repas 'Viande Rouge' émet autant que 32 km en voiture citadine.")

    with tabs[1]:
        st.subheader("Énergie & Fluides (Données PEBC/GIEC)")
        with st.expander("Détails des coefficients Énergie"):
            st.write("- **Électricité (France)** : 0.060 kgCO2e / kWh")
            st.write("- **Gaz Naturel** : 0.227 kgCO2e / kWh")
            st.write("- **Fioul Domestique** : 3.24 kgCO2e / Litre")
            st.write("- **Climatisation (R410A)** : 2088 kgCO2e / kg de fluide")
            st.warning("**Alerte Expert :** 1 kg de gaz de clim qui fuit = 2 tonnes de CO2 dans l'atmosphère !")

    with tabs[2]:
        st.subheader("🚌 Pôle Transports (Données ADEME)")
        st.write("Calculé selon la distance et le mode de transport :")
        data_transp = {
            "Mode de transport": ["Autocar (Scolaire)", "Voiture thermique", "Voiture électrique", "Vélo / Marche"],
            "kgCO2e / km / passager": [0.030, 0.218, 0.050, 0.000]
        }
        st.table(data_transp)
        st.caption("Note : Pour le car, le facteur est bas car on divise l'impact par ~50 passagers.")

    with tabs[3]:
        st.subheader("🗑️ Pôle Déchets (Données ADEME)")
        with st.expander("Coefficients par type de déchet"):
            st.write("- **Ordures Ménagères (Incinération)** : 0.45 kgCO2e / kg")
            st.write("- **Papier/Carton (Recyclage)** : 0.02 kgCO2e / kg")
            st.write("- **Gaspillage Pain** : 0.63 kgCO2e / kg")
            st.success("**Conseil :** Le recyclage du papier divise son impact par 20 par rapport à l'enfouissement.")

    with tabs[4]:
        st.subheader("💻 Pôle Numérique (Données PEBC)")
        st.write("Impact lié à la fabrication (Emissions grises) :")
        with st.expander("Voir le poids carbone des équipements"):
            st.write("- **Ordinateur Portable** : 161 kgCO2e")
            st.write("- **Écran Plat (21-24\")** : 350 kgCO2e")
            st.write("- **Tablette tactile** : 65 kgCO2e")
            st.write("- **Vidéoprojecteur** : 94 kgCO2e")
