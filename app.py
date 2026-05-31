import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS (Mode Sombre / Reposant avec Onglets transformés en Boutons)
def set_style():
    st.markdown(
        """
        <style>
        /* Fond global de l'application (Gris-noir très doux) */
        .stApp { background-color: #0f172a; color: #f1f5f9; }
        
        /* Conteneur principal (Gris ardoise reposant) */
        .main .block-container {
            background-color: #1e293b;
            padding: 2rem 3rem !important;
            border-radius: 8px;
            color: #f1f5f9;
        }
        
        /* --- STYLE DES CONTENEURS (CARTES DE COMPARAISON) --- */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #111827 !important; /* Fond sombre distinct pour séparer les deux tableaux */
            border: 1px solid #334155 !important;
            padding: 22px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        /* --- STYLE DES ONGLETS EN BOUTONS --- */
        /* Alignement et espacement de la liste des onglets */
        div[data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
            margin-bottom: 25px;
        }
        
        /* Le bouton d'onglet par défaut (Inactif) */
        div[data-baseweb="tab"] {
            background-color: #334155 !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            color: #cbd5e1 !important;
            border: 1px solid #475569 !important;
            transition: all 0.3s ease !important;
            height: auto !important;
        }
        
        /* Effet au survol des boutons */
        div[data-baseweb="tab"]:hover {
            background-color: #475569 !important;
            border-color: #38bdf8 !important;
            color: #ffffff !important;
            cursor: pointer;
        }
        
        /* Style du bouton sélectionné (Actif - Bleu électrique vibrant) */
        div[data-baseweb="tab"][aria-selected="true"] {
            background-color: #38bdf8 !important;
            color: #0f172a !important;
            border-color: #38bdf8 !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
        }
        
        /* Nettoyage des bordures par défaut de Streamlit */
        div[role="tabpanel"] { border: none !important; }
        div[data-baseweb="tab-border"] { display: none !important; }
        
        /* Titres des sections (Bleu ciel doux) */
        .inner-title {
            text-align: center; font-weight: bold; font-size: 20px; color: #38bdf8; margin-bottom: 15px;
        }
        [data-testid="stHeader"] { height: 0px; }
        
        /* Style des anecdotes adaptées au fond sombre (Bleu nuit) */
        .anecdote {
            background-color: #1e3a8a;
            padding: 15px;
            border-left: 5px solid #3b82f6;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 10px;
            color: #eff6ff;
        }
        /* Style de la méthode adaptée au fond sombre (Vert forêt) */
        .methode {
            background-color: #14532d;
            padding: 10px;
            border-left: 5px solid #22c55e;
            border-radius: 5px;
            font-size: 0.9em;
            margin-top: 10px;
            color: #f0fdf4;
        }
        
        /* Styles des barres de progression adaptées au fond sombre */
        .pole-header {
            display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1em; margin-bottom: 5px; margin-top: 5px; color: #f1f5f9;
        }
        .sub-pole-header {
            display: flex; justify-content: space-between; font-size: 0.95em; color: #cbd5e1; margin-bottom: 3px; margin-top: 8px;
        }
        .bar-container {
            background-color: #475569; border-radius: 6px; height: 16px; width: 100%; margin-bottom: 15px; overflow: hidden;
        }
        .sub-bar-container {
            background-color: #334155; border-radius: 4px; height: 10px; width: 100%; margin-bottom: 10px; overflow: hidden;
        }
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

# ==========================================
# ---         ONGLET DASHBOARD           ---
# ==========================================
with tab_dashboard:
    if not df.empty:
        col_etab = "Etablissements" if "Etablissements" in df.columns else df.columns[0]
        col_total = "Total émissions" if "Total émissions" in df.columns else df.columns[7]
        col_eff = "Effectif total" if "Effectif total" in df.columns else df.columns[1]
        col_conso = "conso carbone par personne" if "conso carbone par personne" in df.columns else df.columns[8]

        # Conversion numérique des scores
        cols_to_convert = [c for c in df.columns if c != col_etab]
        for col in cols_to_convert:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df_active = df[(df[col_etab].astype(str).str.strip() != "") & (df[col_conso] > 0)].copy()

        st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        # --- ESPACE ENSEIGNANTS : ACCÈS FORMULAIRE TOUT EN HAUT ---
        with st.expander("🔐 ESPACE ENSEIGNANTS : Saisie de nouvelles données", expanded=False):
            st.markdown("<p style='color: #cbd5e1; margin-bottom: 5px;'>Entrez le code secret pour déverrouiller l'accès direct au formulaire Google Forms de votre établissement.</p>", unsafe_allow_html=True)
            pwd = st.text_input("Code secret de déploiement :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.success("Accès autorisé ! Cliquez sur le bouton ci-dessous :")
                st.link_button("🚀 Ouvrir le formulaire de saisie mensuelle", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # --- BLOC : CLASSEMENT ET JAUGE GLOBALE ---
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements (kg/personne)</p>', unsafe_allow_html=True)
            if not df_active.empty:
                df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                st.dataframe(df_ranking, hide_index=True, width="stretch", height=380)
            else:
                st.info("En attente de données calculées...")
                
        with col2:
            st.markdown('<p class="inner-title">🚀 Moyenne du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            if not df_active.empty and df_active[col_eff].sum() > 0:
                moyenne = df_active[col_total].sum() / df_active[col_eff].sum()
            else:
                moyenne = 0

            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg", 'font': {'color': '#f1f5f9'}}, gauge = {'axis': {'range': [None, 2000], 'tickfont': {'color': '#f1f5f9'}}, 'bar': {'color': "#38bdf8"}, 'steps': [{'range': [0, 500], 'color': "#1e3a8a"}, {'range': [500, 1000], 'color': "#b45309"}, {'range': [1000, 2000], 'color': "#991b1b"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 1000}}))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()

        # --- BLOC DU MILIEU : LE BILAN GRAPHIQUE DÉTAILLÉ (COMPARAISON CÔTE À CÔTE) ---
        st.markdown('<p class="inner-title">🔍 Analyse Comparative des Émissions Carbone</p>', unsafe_allow_html=True)
        
        if not df_active.empty:
            
            # --- 1. CALCUL PRÉALABLE DES EMISSIONS TOTALES GLOBALES (RÉSEAU) ---
            total_global_emissions = df_active[col_total].sum()

            elec_global = df_active["Electricité française"].sum() if "Electricité française" in df_active.columns else 0
            fioul_global = df_active["Fioul"].sum() if "Fioul" in df_active.columns else 0
            gaz_global = df_active["Gaz Naturel"].sum() if "Gaz Naturel" in df_active.columns else 0
            total_energie_global = elec_global + fioul_global + gaz_global

            voit_global = df_active["Voiture à essence"].sum() if "Voiture à essence" in df_active.columns else 0
            bus_v_global = df_active["Autobus (ville)"].sum() if "Autobus (ville)" in df_active.columns else 0
            bus_s_global = df_active["Autobus (sortie scolaire)"].sum() if "Autobus (sortie scolaire)" in df_active.columns else 0
            total_transport_global = voit_global + bus_v_global + bus_s_global

            rep_m_global = df_active["Repas moyen"].sum() if "Repas moyen" in df_active.columns else 0
            rep_v_global = df_active["Repas végétarien"].sum() if "Repas végétarien" in df_active.columns else 0
            rep_r_global = df_active["Repas viande rouge"].sum() if "Repas viande rouge" in df_active.columns else 0
            rep_b_global = df_active["Repas viande blanche"].sum() if "Repas viande blanche" in df_active.columns else 0
            rep_p_global = df_active["Repas POISSON"].sum() if "Repas POISSON" in df_active.columns else 0
            total_alimentation_global = rep_m_global + rep_v_global + rep_r_global + rep_b_global + rep_p_global

            dech_p_global = df_active["Déchets Papier"].sum() if "Déchets Papier" in df_active.columns else 0
            dech_a_global = df_active["Déchets alimentaire"].sum() if "Déchets alimentaire" in df_active.columns else 0
            dech_pl_global = df_active["Déchets plastique"].sum() if "Déchets plastique" in df_active.columns else 0
            total_dechets_global = dech_p_global + dech_a_global + dech_pl_global

            pap_global = df_active["Paper"].sum() if "Paper" in df_active.columns else (df_active["Papier"].sum() if "Papier" in df_active.columns else 0)
            plas_global = df_active["Plastique"].sum() if "Plastique" in df_active.columns else 0
            cart_global = df_active["Carton"].sum() if "Carton" in df_active.columns else 0
            ordi_global = df_active["Ordinateur à écran plat"].sum() if "Ordinateur à écran plat" in df_active.columns else 0
            imp_global = df_active["Imprimante"].sum() if "Imprimante" in df_active.columns else 0
            phot_global = df_active["Photocopieurs"].sum() if "Photocopieurs" in df_active.columns else 0
            vid_global = df_active["Vidéo projecteur"].sum() if "Vidéo projecteur" in df_active.columns else 0
            total_biens_global = pap_global + plas_global + cart_global + ordi_global + imp_global + phot_global + vid_global

            # --- 2. SÉPARATION VISUELLE EN DEUX COLONNES ---
            col_gauche, col_droite = st.columns(2)

            # --- CÔTÉ GAUCHE : BASE INDIVIDUELLE (AVEC FOND EN CAPSULÉ) ---
            with col_gauche:
                with st.container(border=True): # Le container applique le fond sombre personnalisé défini dans le CSS
                    
                    # Le selectbox est maintenant ICI : il reste confiné à la largeur de sa colonne
                    selected_school = st.selectbox("Sélectionnez un établissement pour explorer ses statistiques :", df_active[col_etab].unique())
                    
                    # Extraction des données spécifiques
                    school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
                    total_school_emissions = school_data[col_total]
                    
                    elec_val = school_data.get("Electricité française", 0)
                    fioul_val = school_data.get("Fioul", 0)
                    gaz_val = school_data.get("Gaz Naturel", 0)
                    total_energie = elec_val + fioul_val + gaz_val

                    voit_val = school_data.get("Voiture à essence", 0)
                    bus_v_val = school_data.get("Autobus (ville)", 0)
                    bus_s_val = school_data.get("Autobus (sortie scolaire)", 0)
                    total_transport = voit_val + bus_v_val + bus_s_val

                    rep_m = school_data.get("Repas moyen", 0)
                    rep_v = school_data.get("Repas végétarien", 0)
                    rep_r = school_data.get("Repas viande rouge", 0)
                    rep_b = school_data.get("Repas viande blanche", 0)
                    rep_p = school_data.get("Repas POISSON", 0)
                    total_alimentation = rep_m + rep_v + rep_r + rep_b + rep_p

                    dech_p = school_data.get("Déchets Papier", 0)
                    dech_a = school_data.get("Déchets alimentaire", 0)
                    dech_pl = school_data.get("Déchets plastique", 0)
                    total_dechets = dech_p + dech_a + dech_pl

                    pap_val = school_data.get("Paper", 0) if "Paper" in df.columns else school_data.get("Papier", 0)
                    plas_val = school_data.get("Plastique", 0)
                    cart_val = school_data.get("Carton", 0)
                    ordi_val = school_data.get("Ordinateur à écran plat", 0)
                    imp_val = school_data.get("Imprimante", 0)
                    phot_val = school_data.get("Photocopieurs", 0)
                    vid_val = school_data.get("Vidéo projecteur", 0)
                    total_biens = pap_val + plas_val + cart_val + ordi_val + imp_val + phot_val + vid_val

                    st.markdown(f"### 🏫 Base Individuelle : <span style='color:#38bdf8;'>{selected_school}</span>", unsafe_allow_html=True)
                    st.write("---")
                    
                    if total_school_emissions > 0:
                        draw_custom_bar("❄️ Énergie & Bâtiments", total_energie, total_school_emissions, "#22c55e")
                        with st.expander("Détails du poste Énergie"):
                            draw_custom_bar("• Électricité française", elec_val, total_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Gaz Naturel", gaz_val, total_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Fioul de chauffage", fioul_val, total_energie, "#4ade80", is_sub=True)

                        draw_custom_bar("🍎 Alimentation & Cantine", total_alimentation, total_school_emissions, "#f97316")
                        with st.expander("Détails du poste Alimentation"):
                            draw_custom_bar("• Repas avec Viande Rouge", rep_r, total_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas avec Poisson", rep_p, total_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas avec Viande Blanche", rep_b, total_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Standard Moyen", rep_m, total_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Végétarien", rep_v, total_alimentation, "#fb923c", is_sub=True)

                        draw_custom_bar("🚌 Déplacements & Transports", total_transport, total_school_emissions, "#3b82f6")
                        with st.expander("Détails du poste Transports"):
                            draw_custom_bar("• Trajets en Voiture thermique", voit_val, total_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus (sorties scolaires)", bus_s_val, total_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus (lignes régulières / ville)", bus_v_val, total_transport, "#60a5fa", is_sub=True)

                        draw_custom_bar("📦 Biens, Consommables & Équipements", total_biens, total_school_emissions, "#a855f7")
                        with st.expander("Détails du poste Équipements & Consommables"):
                            draw_custom_bar("• Photocopieurs (Empreinte de fabrication)", phot_val, total_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Ordinateurs portables / écrans plats", ordi_val, total_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Ramettes de papier consommées", pap_val, total_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Vidéoprojecteurs", vid_val, total_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Plastiques d'emballage", plas_val, total_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Imprimantes laser", imp_val, total_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Emballages Carton", cart_val, total_biens, "#c084fc", is_sub=True)

                        draw_custom_bar("🗑️ Gestion des Déchets", total_dechets, total_school_emissions, "#6366f1")
                        with st.expander("Détails du poste Déchets"):
                            draw_custom_bar("• Gaspillage alimentaire (restes de cantine)", dech_a, total_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets plastiques non recyclés", dech_pl, total_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets Papier jetés", dech_p, total_dechets, "#818cf8", is_sub=True)
                    else:
                        st.warning("Cet établissement n'a pas encore de données carbone calculées.")

            # --- CÔTÉ DROIT : BASE GÉNÉRALE (AVEC FOND EN CAPSULÉ ÉGALEMENT) ---
            with col_droite:
                with st.container(border=True):
                    
                    # Un sous-titre clair et un espace vide pour s'aligner visuellement sur la hauteur du selectbox de gauche
                    st.markdown("<p style='margin-bottom: 12px; color: #cbd5e1; font-size: 14px;'>Comparatif global inter-établissements</p>", unsafe_allow_html=True)
                    st.markdown("### 🌍 Base Générale <span style='color: #38bdf8;'>(Total Réseau)</span>", unsafe_allow_html=True)
                    st.write("---")
                    
                    if total_global_emissions > 0:
                        draw_custom_bar("❄️ Énergie & Bâtiments", total_energie_global, total_global_emissions, "#22c55e")
                        with st.expander("Détails globaux du poste Énergie"):
                            draw_custom_bar("• Électricité française", elec_global, total_energie_global, "#4ade80", is_sub=True)
                            draw_custom_bar("• Gaz Naturel", gaz_global, total_energie_global, "#4ade80", is_sub=True)
                            draw_custom_bar("• Fioul de chauffage", fioul_global, total_energie_global, "#4ade80", is_sub=True)

                        draw_custom_bar("🍎 Alimentation & Cantine", total_alimentation_global, total_global_emissions, "#f97316")
                        with st.expander("Détails globaux du poste Alimentation"):
                            draw_custom_bar("• Repas avec Viande Rouge", rep_r_global, total_alimentation_global, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas avec Poisson", rep_p_global, total_alimentation_global, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas avec Viande Blanche", rep_b_global, total_alimentation_global, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Standard Moyen", rep_m_global, total_alimentation_global, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Végétarien", rep_v_global, total_alimentation_global, "#fb923c", is_sub=True)

                        draw_custom_bar("🚌 Déplacements & Transports", total_transport_global, total_global_emissions, "#3b82f6")
                        with st.expander("Détails globaux du poste Transports"):
                            draw_custom_bar("• Trajets en Voiture thermique", voit_global, total_transport_global, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus (sorties scolaires)", bus_s_global, total_transport_global, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus (lignes régulières / ville)", bus_v_global, total_transport_global, "#60a5fa", is_sub=True)

                        draw_custom_bar("📦 Biens, Consommables & Équipements", total_biens_global, total_global_emissions, "#a855f7")
                        with st.expander("Détails globaux du poste Équipements & Consommables"):
                            draw_custom_bar("• Photocopieurs (Empreinte de fabrication)", phot_global, total_biens_global, "#c084fc", is_sub=True)
                            draw_custom_bar("• Ordinateurs portables / écrans plats", ordi_global, total_biens_global, "#c084fc", is_sub=True)
                            draw_custom_bar("• Ramettes de papier consommées", pap_global, total_biens_global, "#c084fc", is_sub=True)
                            draw_custom_bar("• Vidéoprojecteurs", vid_global, total_biens_global, "#c084fc", is_sub=True)
                            draw_custom_bar("• Plastiques d'emballage", plas_global, total_biens_global, "#c084fc", is_sub=True)
                            draw_custom_bar("• Imprimantes laser", imp_global, total_biens_global, "#c084fc", is_sub=True)
                            draw_custom_bar("• Emballages Carton", cart_global, total_biens_global, "#c084fc", is_sub=True)

                        draw_custom_bar("🗑️ Gestion des Déchets", total_dechets_global, total_global_emissions, "#6366f1")
                        with st.expander("Détails globaux du poste Déchets"):
                            draw_custom_bar("• Gaspillage alimentaire (restes de cantine)", dech_a_global, total_dechets_global, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets plastiques non recyclés", dech_pl_global, total_dechets_global, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets Papier jetés", dech_p_global, total_dechets_global, "#818cf8", is_sub=True)
                    else:
                        st.warning("Aucune donnée globale disponible pour l'ensemble du réseau.")
        else:
            st.info("Aucune donnée disponible pour l'analyse par établissement.")

        st.divider()
        
        # --- BLOC DU BAS : TABLEAU CENTRALISÉ ---
        st.markdown('<p class="inner-title">📋 Synthèse Globale des Établissements (Données Centralisées)</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch")

# ==========================================
# ---          ONGLET GLOSSAIRE          ---
# ==========================================
with tab_glossaire:
    st.markdown("<h2 style='color: #38bdf8; text-align: center;'>📖 Traducteur Carbone : Ça représente quoi dans ma vie ?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>Parce que les 'kg de CO2' c'est abstrait, voici ce que nos consommations représentent en objets ou activités de ton quotidien !</p>", unsafe_allow_html=True)
    
    # Création des sous-onglets boutons du glossaire pédagogique
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
