import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS (Mode Sombre / Ultra-Compact avec boutons universels et cadres contrastés)
def set_style():
    st.markdown(
        """
        <style>
        /* Compression globale des interlignes et textes */
        .stApp { background-color: #0f172a; color: #f1f5f9; line-height: 1.25 !important; }
        
        /* Conteneur principal */
        .main .block-container {
            background-color: #1e293b;
            padding: 0.8rem 1.5rem !important;
            border-radius: 8px;
            color: #f1f5f9;
        }
        
        /* --- 🎛️ TOUS LES ONGLETS PRINCIPAUX ET SECONDAIRES EN BOUTONS --- */
        div[data-baseweb="tab-list"] {
            gap: 10px !important;
            background-color: transparent !important;
            margin-bottom: 12px !important;
        }
        [data-baseweb="tab"] {
            background-color: #334155 !important;
            border-radius: 8px !important;
            padding: 8px 18px !important;
            color: #cbd5e1 !important;
            border: 1px solid #475569 !important;
            transition: all 0.2s ease !important;
            height: auto !important;
            font-weight: bold !important;
            font-size: 14px !important;
            margin-right: 4px !important;
        }
        [data-baseweb="tab"]:hover {
            background-color: #475569 !important;
            border-color: #22d3ee !important;
            color: #ffffff !important;
            cursor: pointer !important;
        }
        [data-baseweb="tab"][aria-selected="true"] {
            background-color: #22d3ee !important; /* Turquoise */
            color: #0f172a !important; /* Texte sombre pour un contraste maximal */
            border-color: #22d3ee !important;
            box-shadow: 0 4px 12px rgba(34, 211, 238, 0.4) !important;
        }
        [data-baseweb="tab-border"] { display: none !important; }
        div[role="tabpanel"] { border: none !important; }
        
        /* --- 🔍 INTITULÉ DE LA SÉLECTION D'ÉCOLE --- */
        [data-testid="stWidgetLabel"] p {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }
        
        /* --- 💎 CELLULES EN RELIEF AVEC BORDURES DE COULEURS DISTINCTES --- */
        div[data-testid*="column"]:has(.card-mid-left),
        div[class*="stVerticalBlock"]:has(.card-mid-left) {
            background-color: #1e293b !important;
            border: 2px solid #22d3ee !important; /* Cadre Turquoise */
            padding: 14px 18px !important;
            border-radius: 12px !important;
            box-shadow: 0 15px 20px -5px rgba(0, 0, 0, 0.5) !important;
        }
        
        div[data-testid*="column"]:has(.card-mid-right),
        div[class*="stVerticalBlock"]:has(.card-mid-right) {
            background-color: #111827 !important;
            border: 2px solid #475569 !important; /* Cadre Acier Mat */
            padding: 14px 18px !important;
            border-radius: 12px !important;
            box-shadow: 0 15px 20px -5px rgba(0, 0, 0, 0.5) !important;
        }
        
        /* Ajustements généraux des en-têtes */
        .inner-title { text-align: center; font-weight: bold; font-size: 16px; color: #38bdf8; margin-bottom: 6px; }
        h1 { font-size: 24px !important; margin-top: 0px !important; margin-bottom: 8px !important; }
        h2 { font-size: 18px !important; margin-top: 4px !important; margin-bottom: 8px !important; }
        [data-testid="stHeader"] { height: 0px; }
        
        /* Blocs anecdotes et méthodologies */
        .anecdote { background-color: #1e3a8a; padding: 10px 14px; border-left: 4px solid #3b82f6; border-radius: 4px; margin: 6px 0; color: #eff6ff; font-size: 13px; }
        .methode { background-color: #14532d; padding: 8px 12px; border-left: 4px solid #22c55e; border-radius: 4px; font-size: 12px; margin-top: 6px; color: #f0fdf4; }
        
        /* Barres de progression d'émissions affinées */
        .pole-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; margin-bottom: 3px; margin-top: 3px; color: #f1f5f9; }
        .sub-pole-header { display: flex; justify-content: space-between; font-size: 12px; color: #cbd5e1; margin-bottom: 2px; margin-top: 4px; }
        .bar-container { background-color: #475569; border-radius: 4px; height: 11px; width: 100%; margin-bottom: 8px; overflow: hidden; }
        .sub-bar-container { background-color: #334155; border-radius: 3px; height: 7px; width: 100%; margin-bottom: 6px; overflow: hidden; }
        
        /* Style des listes de référentiels d'unités */
        .unit-box { background-color: #1e293b; padding: 10px; border-radius: 6px; border: 1px dashed #475569; margin-bottom: 10px; font-size: 13px; }
        </style>
        """,
        unsafe_allow_html=True
    )

set_style()

# Fonction utilitaire pour dessiner les barres de progression en HTML
def draw_custom_bar(label, value_kg, total_kg, color, is_sub=False):
    pct = (value_kg / total_kg * 100) if total_kg > 0 else 0
    display_weight = f"{value_kg/1000:.2f} t" if value_kg >= 1000 else f"{value_kg:.1f} kg"
    
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

if not df.empty:
    df.columns = [str(c).replace('\xa0', ' ').replace('\n', ' ').strip() for c in df.columns]
    df.columns = [" ".join(c.split()) for c in df.columns]

# 5. NAVIGATION PAR ONGLETS PRINCIPAUX
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel consommations carbone (5 Pôles)"])

# ==========================================
# ---          ONGLET DASHBOARD          ---
# ==========================================
with tab_dashboard:
    if not df.empty:
        col_etab = "Etablissements" if "Etablissements" in df.columns else df.columns[0]
        col_total = "Total émissions" if "Total émissions" in df.columns else df.columns[7]
        col_eff = "Effectif total" if "Effectif total" in df.columns else df.columns[1]
        col_conso = "conso carbone par personne" if "conso carbone par personne" in df.columns else df.columns[8]

        # Conversion numérique sécurisée
        cols_to_convert = [c for c in df.columns if c != col_etab]
        for col in cols_to_convert:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df_active = df[(df[col_etab].astype(str).str.strip() != "") & (df[col_conso] > 0)].copy()

        st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        # --- ESPACE ENSEIGNANTS : ACCÈS FORMULAIRE ---
        with st.expander("🔐 Saisie de nouvelles données", expanded=False):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire Google Forms", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)

        # --- 1️⃣ BLOC DU HAUT COMPACT ---
        col_top1, col_top2 = st.columns([1, 1])
        with col_top1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements (kg/personne)</p>', unsafe_allow_html=True)
            if not df_active.empty:
                df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                st.dataframe(df_ranking, hide_index=True, width="stretch", height=210)
            else:
                st.info("En attente de données...")
                
        with col_top2:
            st.markdown('<p class="inner-title">🚀 Moyenne Globale du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            if not df_active.empty and df_active[col_eff].sum() > 0:
                moyenne = df_active[col_total].sum() / df_active[col_eff].sum()
            else:
                moyenne = 0

            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg", 'font': {'color': '#f1f5f9', 'size': 24}}, gauge = {'axis': {'range': [None, 2000], 'tickfont': {'color': '#f1f5f9', 'size': 10}}, 'bar': {'color': "#38bdf8"}, 'steps': [{'range': [0, 500], 'color': "#1e3a8a"}, {'range': [500, 1000], 'color': "#b45309"}, {'range': [1000, 2000], 'color': "#991b1b"}], 'threshold': {'line': {'color': "red", 'width': 3}, 'value': 1000}}))
            fig.update_layout(height=210, margin=dict(t=20, b=10, l=30, r=30), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()

        # --- 2️⃣ BLOC DU MILIEU : DOUBLE TUILE EN FACE-À-FACE COMPLÈTE ---
        st.markdown('<h2 style="text-align: center; color: #38bdf8;">🔍 Analyse Comparative des Pôles</h2>', unsafe_allow_html=True)
        
        if not df_active.empty:
            col_mid1, col_mid2 = st.columns([1, 1])
            
            # --- 🅰️ TABLEAU GAUCHE : ÉTABLISSEMENT UNIQUE AVEC CLÉS EXACTES ---
            with col_mid1:
                with st.container():
                    st.markdown('<div class="card-mid-left"></div>', unsafe_allow_html=True)
                    selected_school = st.selectbox("Établissement audité :", df_active[col_etab].unique(), key="left_school_selector")
                    st.markdown(f'<p class="inner-title" style="color: #22d3ee; text-align: left; margin-top: 5px; margin-bottom: 10px; font-size: 18px; font-weight: bold;">🏫 Établissement Audité : {selected_school}</p>', unsafe_allow_html=True)
                    
                    school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
                    tot_sch = school_data[col_total]
                    
                    if tot_sch > 0:
                        # Rétablissement des pointeurs de colonnes exacts du Sheets
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
                        with st.expander("Détails Énergie"):
                            draw_custom_bar("• Électricité française", e_elec, sch_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Gaz Naturel", e_gaz, sch_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Fioul de chauffage", e_fioul, sch_energie, "#4ade80", is_sub=True)

                        draw_custom_bar("🍎 Alimentation & Cantine", sch_alimentation, tot_sch, "#f97316")
                        with st.expander("Détails Restauration"):
                            draw_custom_bar("• Repas Viande Rouge", a_r, sch_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Poisson", a_p, sch_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Viande Blanche", a_b, sch_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Standard Moyen", a_m, sch_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Végétarien", a_v, sch_alimentation, "#fb923c", is_sub=True)

                        draw_custom_bar("🚌 Déplacements & Transports", sch_transport, tot_sch, "#3b82f6")
                        with st.expander("Détails Transports"):
                            draw_custom_bar("• Voiture à essence", t_voit, sch_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus (sortie scolaire)", t_bus_s, sch_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus (ville)", t_bus_v, sch_transport, "#60a5fa", is_sub=True)

                        draw_custom_bar("📦 Biens, Consommables & Équipements", sch_biens, tot_sch, "#a855f7")
                        with st.expander("Détails Équipements"):
                            draw_custom_bar("• Photocopieurs (Fab)", b_phot, sch_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Ordinateur à écran plat", b_ord, sch_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Papier", b_pap, sch_biens, "#c084fc", is_sub=True)

                        draw_custom_bar("🗑️ Gestion des Déchets", sch_dechets, tot_sch, "#6366f1")
                        with st.expander("Détails Déchets"):
                            draw_custom_bar("• Déchets alimentaire", d_a, sch_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets plastique", d_pl, sch_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets Papier", d_p, sch_dechets, "#818cf8", is_sub=True)
                    else:
                        st.warning("Cet établissement n'a pas encore de données.")

            # --- 🆂 TABLEAU DROIT : CUMUL GLOBLAL SANS COUPE DE CLÉS ---
            with col_mid2:
                with st.container():
                    st.markdown('<div class="card-mid-right"></div>', unsafe_allow_html=True)
                    st.markdown('<p class="inner-title" style="color: #cbd5e1; text-align: left; margin-bottom: 45px; font-size: 18px; font-weight: bold;">🌍 Global : Secteurs d\'impact du Réseau</p>', unsafe_allow_html=True)
                    
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

                        # Rendu des barres cumulatives
                        draw_custom_bar("❄️ Énergie & Bâtiments (Total Réseau)", net_energie, tot_net, "#22c55e")
                        with st.expander("Détails Énergie (Réseau)"):
                            draw_custom_bar("• Électricité française totale", net_elec, net_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Gaz Naturel global", net_gaz, net_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Fioul global", net_fioul, net_energie, "#4ade80", is_sub=True)

                        draw_custom_bar("🍎 Alimentation & Cantine (Total Réseau)", net_alimentation, tot_net, "#f97316")
                        with st.expander("Détails Restauration (Réseau)"):
                            draw_custom_bar("• Viande Rouge cumulée", net_a_r, net_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Poisson cumulé", net_a_p, net_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Viande Blanche cumulée", net_a_b, net_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Standard Moyen global", net_a_m, net_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Repas Végétarien global", net_a_v, net_alimentation, "#fb923c", is_sub=True)

                        draw_custom_bar("🚌 Déplacements & Transports (Total Réseau)", net_transport, tot_net, "#3b82f6")
                        with st.expander("Détails Transports (Réseau)"):
                            draw_custom_bar("• Voiture à essence", net_t_voit, net_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus (sortie scolaire)", net_t_bus_s, net_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus (ville)", net_t_bus_v, net_transport, "#60a5fa", is_sub=True)

                        draw_custom_bar("📦 Biens & Équipements (Total Réseau)", net_biens, tot_net, "#a855f7")
                        with st.expander("Détails Équipements (Réseau)"):
                            draw_custom_bar("• Fabrication Photocopieurs", net_b_phot, net_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Total Ordinateur à écran plat", net_b_ord, net_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Total Papier", net_b_pap, net_biens, "#c084fc", is_sub=True)

                        draw_custom_bar("🗑️ Gestion des Déchets (Total Réseau)", net_dechets, tot_net, "#6366f1")
                        with st.expander("Détails Déchets (Réseau)"):
                            draw_custom_bar("• Déchets alimentaire", net_d_a, net_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets plastique", net_d_pl, net_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets Papier global", net_d_p, net_dechets, "#818cf8", is_sub=True)

        st.divider()
        st.markdown('<p class="inner-title">📋 Synthèse Globale des Établissements</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch", height=180)

# ==========================================
# ---          ONGLET GLOSSAIRE          ---
# ==========================================
with tab_glossaire:
    st.markdown("<h2 style='color: #38bdf8; text-align: center; margin-bottom: 15px;'>📖 Dictionnaire Carbone : Unités & Équivalents Enfants</h2>", unsafe_allow_html=True)
    
    g_tabs = st.tabs(["🍎 1. Cantine", "❄️ 2. Énergie", "🚌 3. Transports", "🗑️ 4. Gaspillage", "📦 5. Matériel"])
    
    with g_tabs[0]:
        st.subheader("🍎 Référentiel carbone (ADEME)")
        st.markdown("""
        <div class="unit-box">
        • <b>Repas Bœuf / Viande Rouge :</b> 7.26 kg CO2e / repas<br>
        • <b>Repas Poisson :</b> 2.00 kg CO2e / repas<br>
        • <b>Repas Viande Blanche :</b> 1.60 kg CO2e / repas<br>
        • <b>Repas Végétarien :</b> 0.50 kg CO2e / repas
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="anecdote">
        <b>💡 3 Comparaisons Chocs pour les élèves :</b><br>
        1. 👟 <b>La paire de baskets :</b> Choisir l'option viande rouge un seul midi émet autant de CO2 que de fabriquer <b>une paire de baskets de marque</b> neuve !<br>
        2. 📱 <b>Le marathon TikTok :</b> L'impact d'un steak de bœuf équivaut à regarder des vidéos en streaming 4G non-stop pendant <b>150 heures d'affilée</b>.<br>
        3. 🥤 <b>Les canettes de soda :</b> Ce seul repas équivaut à la pollution générée par la fabrication de <b>300 canettes en aluminium</b>.
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("❄️ Référentiel carbone (ADEME)")
        st.markdown("""
        <div class="unit-box">
        • <b>Électricité française :</b> 0.06 kg CO2e / kWh<br>
        • <b>Gaz Naturel :</b> 0.24 kg CO2e / kWh<br>
        • <b>Fioul de chauffage :</b> 0.32 kg CO2e / kWh
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="anecdote">
        <b>💡 3 Comparaisons Chocs pour les élèves :</b><br>
        1. 🎮 <b>La session Gaming :</b> 1 kWh d'électricité (un projecteur allumé 4h), c'est assez d'énergie pour faire tourner une <b>PS5 pendant 8 heures</b> non-stop.<br>
        2. 🔋 <b>La recharge infinie :</b> Ce même petit kWh permet de recharger un smartphone de 0% à 100% tous les soirs pendant <b>2 ans complets</b>.<br>
        3. 👕 <b>Le piège des fenêtres :</b> Ouvrir les fenêtres en hiver alors que le chauffage tourne à fond, c'est rejeter l'impact carbone de <b>2 t-shirts neufs</b> en pur gâchis.
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("🚌 Référentiel carbone (ADEME)")
        st.markdown("""
        <div class="unit-box">
        • <b>Voiture thermique (Moyenne) :</b> 0.26 kg CO2e / km<br>
        • <b>Autobus de ville :</b> 0.18 kg CO2e / passager.km<br>
        • <b>Autocar Scolaire (Rempli) :</b> Impact divisé par 50 (Ultra-faible)
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="anecdote">
        <b>💡 3 Comparaisons Chocs pour les élèves :</b><br>
        1. 💬 <b>L'usine à Snaps :</b> Faire un court trajet de 4 km en voiture pour venir au collège émet autant de CO2 que d'envoyer <b>250 Snaps vidéo</b>.<br>
        2. 🧴 <b>Les bouteilles plastique :</b> Ces mêmes 4 km en voiture polluent autant que la fabrication de <b>15 bouteilles en plastique</b> d'un litre et demi.<br>
        3. 🚌 <b>Le super-pouvoir du car :</b> Partager un bus à 50 camarades divise ton impact par 4. Ta part devient aussi légère que si tu venais en <b>trottinette électrique</b> !
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("🗑️ Référentiel carbone (ADEME)")
        st.markdown("""
        <div class="unit-box">
        • <b>Gaspillage alimentaire (Assiette globale) :</b> 1.20 kg CO2e / kg jeté<br>
        • <b>Gaspillage du Pain :</b> 0.63 kg CO2e / kg jeté<br>
        • <b>Plastiques et emballages associés :</b> 0.87 kg CO2e / kg jeté
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="anecdote">
        <b>💡 3 Comparaisons Chocs pour les élèves :</b><br>
        1. 🍔 <b>Le crash du Burger :</b> Jeter seulement 2 kg de nourriture à la poubelle de la cantine pollue autant que de fabriquer <b>un double cheeseburger au bœuf entier jeté direct à la benne</b> !<br>
        2. ✂️ <b>Le sweat de marque coupé :</b> Gaspiller 5 kg de nourriture sur une semaine, c'est comme acheter <b>un sweat neuf</b> pour le couper en morceaux sans jamais l'avoir porté.<br>
        3. 🛴 <b>Le raid gâché :</b> Jeter son plateau repas complet sans y toucher, c'est gaspiller l'équivalent carbone d'un voyage de <b>40 km en trottinette électrique</b>.
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("📦 Référentiel carbone - Énergie Grise (ADEME)")
        st.markdown("""
        <div class="unit-box">
        • <b>Photocopieur d'établissement (Fabrication) :</b> 2 935 kg CO2e<br>
        • <b>Grand Écran Plat de classe :</b> 1 283 kg CO2e<br>
        • <b>Ordinateur Portable d'élève :</b> 161 kg CO2e<br>
        • <b>Rame de papier A4 (Impact de production) :</b> 0.91 kg CO2e / kg
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="anecdote">
        <b>💡 3 Comparaisons Chocs pour les élèves :</b><br>
        1. 👖 <b>Le placard de Jeans :</b> Fabriquer un seul ordinateur portable (161 kg) rejette autant de CO2 que de fabriquer <b>7 paires de jeans neufs</b>.<br>
        2. 🛵 <b>Le tour de France en scooter :</b> Acheter un grand écran plat de salle pollue autant à la fabrication que de faire **5 000 km en scooter**.<br>
        3. 🌳 <b>Le massacre des arbres :</b> Utiliser 1 000 ramettes de papier dans l'année au collège équivaut à abattre une mini-forêt de **10 arbres adultes**.
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Sources des référentiels : Base Empreinte ADEME / Simulateur National 'Nos Gestes Climat' - Juin 2026")
