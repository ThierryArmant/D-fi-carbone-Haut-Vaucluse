# --- 3. PAGE : TABLEAU DE BORD (Page principale) ---
if page == "📊 Tableau de Bord":
    st.title("📊 Bilan Carbone des Établissements")
    
    df = load_data()
    
    if df is not None:
        # 1. SÉLECTEUR D'ÉTABLISSEMENT
        liste_etablissements = df['ETABLISSEMENT'].unique()
        choix = st.selectbox("Choisir un établissement pour voir le bilan individuel :", liste_etablissements)
        
        # 2. FILTRAGE DES DONNÉES
        topo = df[df['ETABLISSEMENT'] == choix].iloc[0]
        score = topo['SCORE GLOBAL'] # Assure-toi que cette colonne existe dans ton Sheets
        
        # 3. AFFICHAGE DE LA JAUGE (INDICATEUR)
        st.subheader(f"Performance Carbone : {choix}")
        st.metric(label="Score Global (kgCO2e / élève)", value=f"{score:.2f}")
        
        # Barre de progression colorée (simulant une jauge)
        if score < 100:
            st.success("Excellent : Établissement Bas Carbone")
            st.progress(score / 500) # Ajuste le 500 selon ton maximum théorique
        elif score < 300:
            st.warning("Moyen : Des efforts sont possibles")
            st.progress(score / 500)
        else:
            st.error("Élevé : Poste de consommation à surveiller")
            st.progress(score / 500)

        # 4. BILAN INDIVIDUEL DÉTAILLÉ (Tableau ou Colonnes)
        st.write("---")
        st.subheader("Détails par pôle de consommation")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**🍎 Alimentation**")
            st.write(f"{topo['REPAS']} kgCO2e") # Nom de colonne à vérifier dans ton Sheets
        with col2:
            st.write("**⚡ Énergie**")
            st.write(f"{topo['ENERGIE']} kgCO2e")
        with col3:
            st.write("**🚌 Transports**")
            st.write(f"{topo['TRANSPORT']} kgCO2e")

        st.divider()
        
        # --- SECTION ACCÈS FORMULAIRE (Code masqué) ---
        st.subheader("📝 Saisie de nouvelles données")
        code_saisi = st.text_input("Code accès formulaire :", type="password")
        
        if code_saisi == "VOTRE_CODE":
            st.success("Accès autorisé")
            st.link_button("Accéder au Formulaire Google", "LIEN_FORMULAIRE")
