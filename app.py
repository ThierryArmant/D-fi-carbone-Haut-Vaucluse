import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS (Mode Sombre / Reposant avec Onglets en boutons et Blocs 3D contrastés)
def set_style():
    st.markdown(
        """
        <style>
        /* Fond global de l'application (Gris-noir très doux) */
        .stApp { background-color: #0f172a; color: #f1f5f9; }
        
        /* Conteneur principal */
        .main .block-container {
            background-color: #1e293b;
            padding: 2rem 3rem !important;
            border-radius: 8px;
            color: #f1f5f9;
        }
        
        /* --- STYLE DES ONGLETS EN BOUTONS --- */
        div[data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
            margin-bottom: 25px;
        }
        div[data-baseweb="tab"] {
            background-color: #334155 !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            color: #cbd5e1 !important;
            border: 1px solid #475569 !important;
            transition: all 0.3s ease !important;
            height: auto !important;
        }
        div[data-baseweb="tab"]:hover {
            background-color: #475569 !important;
            border-color: #38bdf8 !important;
            color: #ffffff !important;
            cursor: pointer;
        }
        div[data-baseweb="tab"][aria-selected="true"] {
            background-color: #38bdf8 !important;
            color: #0f172a !important;
            border-color: #38bdf8 !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
        }
        div[role="tabpanel"] { border: none !important; }
        div[data-baseweb="tab-border"] { display: none !important; }
        
        /* --- 💎 DESIGN DES BLOCS EN RELIEF ET À TRÈS FORT CONTRASTE (STYLE SLIDES) --- */
        div[data-testid="stBorderedContainer"] {
            border-radius: 16px !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4) !important;
        }
        
        /* Table de Gauche (Établissement sélectionné) : Fond bleu-gris distinct + Contour Cyan Pop */
        div[data-testid="stBorderedContainer"]:has(.card-mid-left) {
            background-color: #233044 !important;
            border: 2px solid #38bdf8 !important;
            padding: 25px !important;
        }
        
        /* Table de Droite (Cumul global du réseau) : Fond anthracite sombre distinct + Contour Acier Muted */
        div[data-testid="stBorderedContainer"]:has(.card-mid-right) {
            background-color: #141c29 !important;
            border: 2px solid #475569 !important;
            padding: 25px !important;
        }
        
        /* Titres des sections */
        .inner-title {
            text-align: center; font-weight: bold; font-size: 20px; color: #38bdf8; margin-bottom: 15px;
        }
        [data-testid="stHeader"] { height: 0px; }
        
        /* Blocs explicatifs */
        .anecdote { background-color: #1e3a8a; padding: 15px; border-left: 5px solid #3b82f6; border-radius: 5px; margin: 10px 0; color: #eff6ff; }
        .methode { background-color: #14532d; padding: 10px; border-left: 5px solid #22c55e; border-radius: 5px; font-size: 0.9em; margin-top: 10px; color: #f0fdf4; }
        
        /* Styles des barres de progression */
        .pole-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1em; margin-bottom: 5px; margin-top: 5px; color: #f1f5f9; }
        .sub-pole-header { display: flex; justify-content: space-between; font-size: 0.95em; color: #cbd5e1; margin-bottom: 3px; margin-top: 8px; }
        .bar-container { background-color: #475569; border-radius: 6px; height: 16px; width: 100%; margin-bottom: 15px; overflow: hidden; }
        .sub-bar-container { background-color: #334155; border-radius: 4px; height: 10px; width: 100%; margin-bottom: 10px; overflow: hidden; }
        </style>
        """,
        unsafe_allow_html=True
    )

set_style()

# Fonction utilitaire pour dessiner les barres de progression en HTML
def draw_custom_bar(label, value_kg, total_kg, color, is_sub=False):
    pct = (value_kg / total_kg * 100) if total_kg > 0 else 0
    display_weight = f"{value_kg/1000:.2f} tonne" if value_kg >= 1000 else f"{value_kg:.1f} kg"
    
    if not is_sub:
        st.markdown(f"""
            <div class="pole-header"><span>{label}</span><span>{display_weight} - {pct:.1f} %</span></div>
            <div class="bar-container"><div style="background-color: {color}; height: 100%; width: {pct}%;"></div></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="sub-pole-header"><span>{label}</span><span>{display_weight} - {pct:.1f} %</span></div>
            <div class="sub-bar-container"><div style="background-color: {color}; height: 100%; width: {pct}%;"></div></div>
        """, unsafe_allow_html=True)

# 3. VARIABLES DE CONNEXION
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

# 4. CHARGEMENT DES DONNÉES
@st.cache_data(ttl=60)
def load_data():
    try:
        raw = pd.read_csv(url, header=None)
        for i, row in raw.iterrows():
            row_str = [str(x).strip() for x in row.values]
            if any("etablissement" in x.lower() for x in row_str):
                data = raw.iloc[i+1:].copy()
                new_cols = [str(val).strip() if pd.notnull(val) else f"Col_{j}" for j, val in enumerate(row.values)]
                data.columns = new_cols
                return data.loc[:, ~data.columns.duplicated()].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
    return pd.DataFrame()

df = load_data()

# Nettoyage global des colonnes
if not df.empty:
    df.columns = [str(c).replace('\xa0', ' ').replace('\n', ' ').strip() for c in df.columns]
    df.columns = [" ".join(c.split()) for c in df.columns]

# 5. NAVIGATION PAR ONGLETS PRINCIPAUX
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel consommations carbone (5 Pôles)"])

# --- ONGLET DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        col_etab = "Etablissements" if "Etablissements" in df.columns else df.columns[0]
        col_total = "Total émissions" if "Total émissions" in df.columns else df.columns[7]
        col_eff = "Effectif total" if "Effectif total" in df.columns else df.columns[1]
        col_conso = "conso carbone par personne" if "conso carbone par personne" in df.columns else df.columns[8]

        # Conversion numérique
        cols_to_convert = [c for c in df.columns if c != col_etab]
        for col in cols_to_convert:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df_active = df[(df[col_etab].astype(str).str.strip() != "") & (df[col_conso] > 0)].copy()

        st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        # --- ESPACE ENSEIGNANTS : ACCÈS FORMULAIRE ---
        with st.expander("🔐 ESPACE ENSEIGNANTS : Saisie de nouvelles données", expanded=False):
            pwd = st.text_input("Code secret de déploiement :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.success("Accès autorisé !")
                st.link_button("🚀 Ouvrir le formulaire de saisie mensuelle", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # --- 1️⃣ BLOC DU HAUT : CLASSEMENT ET JAUGE GLOBALE ---
        col_top1, col_top2 = st.columns([1, 1])
        with col_top1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements (kg/personne)</p>', unsafe_allow_html=True)
            if not df_active.empty:
                df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                st.dataframe(df_ranking, hide_index=True, width="stretch", height=280)
            else:
                st.info("En attente de données calculées...")
                
        with col_top2:
            st.markdown('<p class="inner-title">🚀 Moyenne Globale du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            if not df_active.empty and df_active[col_eff].sum() > 0:
                moyenne = df_active[col_total].sum() / df_active[col_eff].sum()
            else:
                moyenne = 0

            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg", 'font': {'color': '#f1f5f9'}}, gauge = {'axis': {'range': [None, 2000], 'tickfont': {'color': '#f1f5f9'}}, 'bar': {'color': "#38bdf8"}, 'steps': [{'range': [0, 500], 'color': "#1e3a8a"}, {'range': [500, 1000], 'color': "#b45309"}, {'range': [1000, 2000], 'color': "#991b1b"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 1000}}))
            fig.update_layout(height=280, margin=dict(t=30, b=0, l=40, r=40), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()

        # --- 2️⃣ BLOC DU MILIEU : DOUBLE BOÎTE ÉTANCHE ET VISUELLE EN FACE-À-FACE ---
        st.markdown('<h2 style="text-align: center; color: #38bdf8; margin-bottom: 25px;">🔍 Analyse Comparative des Pôles de Consommation</h2>', unsafe_allow_html=True)
        
        if not df_active.empty:
            col_mid1, col_mid2 = st.columns([1, 1])
            
            # --- 🅰️ TABLEAU GAUCHE EN CAPSULE CYAN ---
            with col_mid1:
                with st.container(border=True):
                    # Injection du marqueur CSS interne
                    st.markdown('<div class="card-mid-left"></div>', unsafe_allow_html=True)
                    
                    # Le menu de sélection confiné ici à sa juste largeur
                    selected_school = st.selectbox("Sélectionnez votre établissement :", df_active[col_etab].unique(), key="left_school_selector")
                    st.markdown(f'<p class="inner-title" style="color: #ffffff; text-align: left; margin-top: 15px; margin-bottom: 20px;">🏫 Détail : {selected_school}</p>', unsafe_allow_html=True)
                    
                    school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
                    tot_sch = school_data[col_total]
                    
                    if tot_sch > 0:
                        e_elec = school_data.get("Electricité française", 0)
                        e_fioul = school_data.get("Fioul", 0)
                        e_gaz = school_data.get("Gaz Naturel", 0)
                        sch_energie = e_elec + e_fioul + e_gaz

                        a_m = school_data.get("Repas moyen", 0)
                        a_v = school_data.get("Repas végétarien", 0)
                        a_r = school_data.get("Repas viande rouge", 0)
                        a_b = school_data.get("Repas viande blanche", 0)
                        a_p = school_data.get("Repas POISSON", 0)
                        sch_alimentation = a_m + a_v + a_r + a_b + a_p

                        t_voit = school_data.get("Voiture à essence", 0)
                        t_bus_v = school_data.get("Autobus (ville)", 0)
                        t_bus_s = school_data.get("Autobus (sortie scolaire)", 0)
                        sch_transport = t_voit + t_bus_v + t_bus_s

                        b_pap = school_data.get("Paper", 0) if "Paper" in df.columns else school_data.get("Papier", 0)
                        b_plas = school_data.get("Plastique", 0)
                        b_cart = school_data.get("Carton", 0)
                        b_ord = school_data.get("Ordinateur à écran plat", 0)
                        b_imp = school_data.get("Imprimante", 0)
                        b_phot = school_data.get("Photocopieurs", 0)
                        b_vid = school_data.get("Vidéo projecteur", 0)
                        sch_biens = b_pap + b_plas + b_cart + b_ord + b_imp + b_phot + b_vid

                        d_p = school_data.get("Déchets Papier", 0)
                        d_a = school_data.get("Déchets alimentaire", 0)
                        d_pl = school_data.get("Déchets plastique", 0)
                        sch_dechets = d_p + d_a + d_pl

                        # Affichage des barres
                        draw_custom_bar("❄️ Énergie & Bâtiments", sch_energie, tot_sch, "#22c55e")
                        with st.expander("Détails Énergie de l'établissement"):
                            draw_custom_bar("• Électricité française", e_elec, sch_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Gaz Naturel", e_gaz, sch_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Fioul de chauffage", e_fioul, sch_energie, "#4ade80", is_sub=True)

                        draw_custom_bar("🍎 Alimentation & Cantine", sch_alimentation, tot_sch, "#f97316")
                        with st.expander("Détails Restauration de l'établissement"):
                            draw_custom_bar("• Repas Viande Rouge", a_r, sch_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Poisson", a_p, sch_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Viande Blanche", a_b, sch_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Standard Moyen", a_m, sch_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Végétarien", a_v, sch_alimentation, "#fb923c", is_sub=True)

                        draw_custom_bar("🚌 Déplacements & Transports", sch_transport, tot_sch, "#3b82f6")
                        with st.expander("Détails Transports de l'établissement"):
                            draw_custom_bar("• Voiture thermique individuelle", t_voit, sch_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus / Autocar (sorties)", t_bus_s, sch_transport, "#60a5fa", is_sub=True)

                        draw_custom_bar("📦 Biens, Consommables & Équipements", sch_biens, tot_sch, "#a855f7")
                        with st.expander("Détails Équipements de l'établissement"):
                            draw_custom_bar("• Photocopieurs d'établissement", b_phot, sch_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Ordinateurs & Écrans", b_ord, sch_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Ramettes de papier", b_pap, sch_biens, "#c084fc", is_sub=True)

                        draw_custom_bar("🗑️ Gestion des Déchets", sch_dechets, tot_sch, "#6366f1")
                        with st.expander("Détails Déchets de l'établissement"):
                            draw_custom_bar("• Gaspillage assiette cantine", d_a, sch_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets plastiques jetés", d_pl, sch_dechets, "#818cf8", is_sub=True)
                    else:
                        st.warning("Cet établissement n'a pas encore de données carbone calculées.")

            # --- 🆂 TABLEAU DROIT EN CAPSULE ACIER ANTHRACITE (CUMULÉ) ---
            with col_mid2:
                with st.container(border=True):
                    # Injection du marqueur CSS opposé
                    st.markdown('<div class="card-mid-right"></div>', unsafe_allow_html=True)
                    st.markdown('<p class="inner-title" style="color: #38bdf8; text-align: left; margin-bottom: 58px;">🌍 Global : Secteurs d\'impact du Réseau</p>', unsafe_allow_html=True)
                    
                    def safe_sum(col_name):
                        if col_name in df_active.columns:
                            return df_active[col_name].sum()
                        return 0

                    tot_net = df_active[col_total].sum()
                    
                    if tot_net > 0:
                        net_elec = safe_sum("Electricité française")
                        net_fioul = safe_sum("Fioul")
                        net_gaz = safe_sum("Gaz Naturel")
                        net_energie = net_elec + net_fioul + net_gaz

                        net_a_m = safe_sum("Repas moyen")
                        net_a_v = safe_sum("Repas végétarien")
                        net_a_r = safe_sum("Repas viande rouge")
                        net_a_b = safe_sum("Repas viande blanche")
                        net_a_p = safe_sum("Repas POISSON")
                        net_alimentation = net_a_m + net_a_v + net_a_r + net_a_b + net_a_p

                        net_t_voit = safe_sum("Voiture à essence")
                        net_t_bus_v = safe_sum("Autobus (ville)")
                        net_t_bus_s = safe_sum("Autobus (sortie scolaire)")
                        net_transport = net_t_voit + net_t_bus_v + net_t_bus_s

                        col_b_pap = "Paper" if "Paper" in df.columns else "Papier"
                        net_b_pap = safe_sum(col_b_pap)
                        net_b_plas = safe_sum("Plastique")
                        net_b_cart = safe_sum("Carton")
                        net_b_ord = safe_sum("Ordinateur à écran plat")
                        net_b_imp = safe_sum("Imprimante")
                        net_b_phot = safe_sum("Photocopieurs")
                        net_b_vid = safe_sum("Vidéo projecteur")
                        net_biens = net_b_pap + net_b_plas + net_b_cart + net_b_ord + net_b_imp + net_b_phot + net_b_vid

                        net_d_p = safe_sum("Déchets Papier")
                        net_d_a = safe_sum("Déchets alimentaire")
                        net_d_pl = safe_sum("Déchets plastique")
                        net_dechets = net_d_p + net_d_a + net_d_pl

                        # Barres cumulatives globales
                        draw_custom_bar("❄️ Énergie & Bâtiments (Total Réseau)", net_energie, tot_net, "#22c55e")
                        with st.expander("Détails Énergie du Réseau"):
                            draw_custom_bar("• Électricité globale", net_elec, net_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Gaz Naturel global", net_gaz, net_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Fioul global", net_fioul, net_energie, "#4ade80", is_sub=True)

                        draw_custom_bar("🍎 Alimentation & Cantine (Total Réseau)", net_alimentation, tot_net, "#f97316")
                        with st.expander("Détails Restauration du Réseau"):
                            draw_custom_bar("• Viande Rouge cumulée", net_a_r, net_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Poisson cumulé", net_a_p, net_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Viande Blanche cumulée", net_a_b, net_alimentation, "#fb923c", is_sub=True)

                        draw_custom_bar("🚌 Déplacements & Transports (Total Réseau)", net_transport, tot_net, "#3b82f6")
                        with st.expander("Détails Transports du Réseau"):
                            draw_custom_bar("• Voitures particulières", net_t_voit, net_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Bus et cars scolaires", net_t_bus_s, net_transport, "#60a5fa", is_sub=True)

                        draw_custom_bar("📦 Biens, Consommables & Équipements (Total Réseau)", net_biens, tot_net, "#a855f7")
                        with st.expander("Détails Équipements du Réseau"):
                            draw_custom_bar("• Fabrication Photocopieurs", net_b_phot, net_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Total Ordinateurs", net_b_ord, net_biens, "#c084fc", is_sub=True)

                        draw_custom_bar("🗑️ Gestion des Déchets (Total Réseau)", net_dechets, tot_net, "#6366f1")
                        with st.expander("Détails Déchets du Réseau"):
                            draw_custom_bar("• Total Restes alimentaires", net_d_a, net_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Plastiques non recyclés", net_d_pl, net_dechets, "#818cf8", is_sub=True)
                    else:
                        st.info("Aucune donnée agrégée disponible.")

        st.divider()
        
        # --- 3️⃣ BLOC DU BAS : SYNTHÈSE DES DONNÉES BRUTES ---
        st.markdown('<p class="inner-title">📋 Synthèse Globale des Établissements (Données Centralisées)</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch")

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

    with g_tabs[1]:
        st.subheader("❄️ Pôle Énergie (L'électricité et le chauffage du collège)")
        st.markdown("""
        <div class="anecdote">
        <b>Pour comprendre l'Électricité (1 kWh = 0,06 kg CO2e) :</b><br>
        1 kWh d'électricité au collège, ça permet de faire quoi chez toi ?<br>
        • Jouer à la <b>CONSOLE (PS5 ou Xbox Series X) pendant 8 HEURES</b> non-stop.<br>
        • Recharger ton smartphone de 0% à 100% tous les soirs pendant <b>2 ANS</b> !
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

    with g_tabs[3]:
        st.subheader("🗑️ Pôle Déchets (Ce qu'on jette à la poubelle)")
        st.markdown("""
        <div class="anecdote">
        <b>Le Gaspillage Alimentaire (1 kg de nourriture jeté = 1,2 kg CO2e) :</b><br>
        • Jeter <b>2 kg de nourriture</b> (l'équivalent de quelques plateaux mal finis), c'est polluer autant que de fabriquer <b>1 HAMBURGER AU BŒUF COMPLET</b> pour le mettre directement à la poubelle.<br>
        • Si une table de copains gaspille 5 kg de pain et de restes ce midi, c'est l'équivalent carbone de fabriquer <b>un T-SHIRT NEUF</b> et de le découper en morceaux sans jamais l'avoir porté.
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("📦 Pôle Biens & Consommables (Le matériel du collège)")
        st.markdown("""
        <div class="anecdote">
        • Acheter <b>1 ORDINATEUR PORTABLE</b> de classe (161 kg CO2e) = Fabriquer <b>7 PAIRES DE JEANS</b> neufs.<br>
        • Installer <b>1 GRAND ÉCRAN PLAT</b> dans une salle (1 283 kg CO2e) = Acheter <b>55 PAIRES DE JEANS</b> ou faire <b>5 000 km en scooter</b> !
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("Sources des équivalents ados : Base Empreinte ADEME / Simulateur National 'Nos Gestes Climat' - Mai 2026")
