# --- ONGLET GLOSSAIRE (Version Spéciale Élèves / Vie Quotidienne) ---
with tab_glossaire:
    st.markdown("<h2 style='color: #38bdf8; text-align: center;'>📖 Traducteur Carbone : Ça représente quoi dans ma vie ?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>Parce que les 'kg de CO2' c'est abstrait, voici ce que nos consommations représentent en objets ou activités de ton quotidien !</p>", unsafe_allow_html=True)
    
    g_tabs = st.tabs(["🍎 1. À la Cantine", "❄️ 2. Chauffage & Lumière", "🚌 3. Transports & Sorties", "🗑️ 4. Le Gaspillage", "📦 5. Matériel & Ordis"])
    
    with g_tabs[0]:
        st.subheader("🍎 Pôle Alimentation (L'impact de mon plateau)")
        
        st.markdown("""
        <div class="anecdote">
        <b>Si tu prends l'option VIANDE ROUGE (Bœuf) :</b><br>
        L'impact est de 7,26 kg CO2e. C'est l'équivalent exact de :<br>
        • Fabriquer <b>1 PAIRE DE BASKETS neuve</b> pour aller en EPS.<br>
        • Regarder des vidéos en streaming 4G sur ton téléphone pendant <b>150 HEURES d'affilée</b>.<br>
        • L'empreinte de fabrication de <b>300 canettes de soda</b> en aluminium.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="methode">
        <b>💡 Le réflexe malin :</b> En choisissant l'option <b>Poisson</b> (2 kg) ou <b>Viande Blanche</b> (1,6 kg), tu divises l'impact par 3. Si tu choisis le repas <b>Végétarien</b> (0,5 kg), c'est comme si tu ne lançais ton jeu vidéo préféré que pendant quelques heures. L'effort est énorme !
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("❄️ Pôle Énergie (L'électricité et le chauffage du collège)")
        
        st.markdown("""
        <div class="anecdote">
        <b>Pour comprendre l'Électricité (1 kWh = 0,06 kg CO2e) :</b><br>
        1 kWh d'électricité au collège, ça permet de faire quoi chez toi ?<br>
        • Jouer à la <b>CONSOLE (PS5 ou Xbox Series X) pendant 8 HEURES</b> non-stop.<br>
        • Laisser la télévision du salon allumée pendant 15 heures.<br>
        • Recharger ton smartphone de 0% à 100% tous les soirs pendant <b>2 ANS</b> !
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="anecdote" style="background-color: #991b1b; border-left-color: #ef4444;">
        <b>⚠️ Le piège du Chauffage (Gaz et Fioul) :</b><br>
        Le gaz et le fioul polluent <b>4 à 5 fois plus</b> que l'électricité chez nous. <br>
        Ouvrir les fenêtres de la classe en plein hiver alors que le chauffage tourne à fond pendant 1 heure, c'est jeter en l'air l'équivalent carbone de <b>2 paires de jeans neufs</b> en pur gaspillage d'énergie.
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("🚌 Pôle Transports (Mes déplacements)")
        
        st.markdown("""
        <div class="anecdote">
        <b>La Voiture de la famille (1 km = 0,26 kg CO2e) :</b><br>
        Faire un petit trajet de 4 km en voiture thermique pour venir au collège émet 1 kg de CO2. C'est autant que :<br>
        • Fabriquer <b>15 BOUTEILLES EN PLASTIQUE</b> de 1,5L.<br>
        • Envoyer <b>250 SNAPS</b> avec de grosses vidéos.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="methode">
        <b>🚌 Pourquoi le Bus scolaire gagne le match ?</b><br>
        Quand tu partages un autocar avec 50 camarades pour une sortie scolaire, ta part de pollution par kilomètre devient minuscule. C'est comme si tu venais au collège en <b>trottinette électrique</b> !
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("🗑️ Pôle Déchets (Ce qu'on jette à la poubelle)")
        
        st.markdown("""
        <div class="anecdote">
        <b>Le Gaspillage Alimentaire (1 kg de nourriture jeté = 1,2 kg CO2e) :</b><br>
        Quand on jette de la nourriture à la cantine, on jette l'énergie qu'il a fallu pour faire pousser les légumes ou élever les animaux. <br>
        • Jeter <b>2 kg de nourriture</b> (l'équivalent de quelques plateaux mal finis), c'est polluer autant que de fabriquer <b>1 HAMBURGER AU BŒUF COMPLET</b> pour le mettre directement à la poubelle.<br>
        • Si une table de copains gaspille 5 kg de pain et de restes ce midi, c'est l'équivalent carbone de fabriquer <b>un T-SHIRT NEUF</b> et de le découper en morceaux sans jamais l'avoir porté.
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("📦 Pôle Biens & Consommables (Le matériel du collège)")
        
        st.markdown("""
        <div class="anecdote">
        <b>L'Énergie Grise (Le poids caché de la fabrication) :</b><br>
        Un appareil électronique pollue énormément au moment où on le fabrique à l'usine, bien avant d'arriver dans notre classe.<br>
        • Acheter <b>1 ORDINATEUR PORTABLE</b> de classe (161 kg CO2e) = Fabriquer <b>7 PAIRES DE JEANS</b> neufs.<br>
        • Installer <b>1 GRAND ÉCRAN PLAT</b> dans une salle (1 283 kg CO2e) = Acheter <b>55 PAIRES DE JEANS</b> ou faire <b>5 000 km en scooter</b> !<br>
        • Consommer <b>1 000 ramettes de papier A4</b> au collège dans l'année = Couper une forêt de <b>10 ARBRES ADULTES</b>.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="methode">
        <b>🔧 L'éco-geste ultime :</b> Prendre soin du matériel (tables, chaises, ordis, projecteurs) pour qu'ils durent 2 ans de plus, c'est le meilleur moyen de faire chuter le score carbone de ton établissement !
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("Sources des équivalents ados : Base Empreinte ADEME / Simulateur National 'Nos Gestes Climat' - Mai 2026")
