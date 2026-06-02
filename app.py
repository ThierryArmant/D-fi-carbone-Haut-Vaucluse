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
        
        /* --- 🎛️ NAVIGATION PRINCIPALE À 3 BOUTONS DESIGN SLIDES --- */
        div[data-baseweb="tab-list"] {
            gap: 10px !important;
            background-color: transparent !important;
            margin-bottom: 12px !important;
        }
        div[data-baseweb="tab"], button[data-baseweb="tab"] {
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
        div[data-baseweb="tab"]:hover, button[data-baseweb="tab"]:hover {
            background-color: #475569 !important;
            border-color: #22d3ee !important;
            color: #ffffff !important;
            cursor: pointer !important;
        }
        div[data-baseweb="tab"][aria-selected="true"], button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #22d3ee !important; /* Turquoise */
            color: #0f172a !important; /* Texte sombre pour un contraste maximal */
            border-color: #22d3ee !important;
            box-shadow: 0 4px 12px rgba(34, 211, 238, 0.4) !important;
        }
        div[data-baseweb="tab-border"] { display: none !important; }
        div[role="tabpanel"] { border: none !important; }
        
        /* --- 🔍 INTITULÉ DE LA SÉLECTION D'ÉCOLE --- */
        [data-testid="stWidgetLabel"] p {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }
        
        /* --- 💎 CELLULES EN RELIEF ÉTANCHE STYLE DIAPOSITIVES --- */
        div[data-testid="stBorderedContainer"]:has(.card-mid-left) {
            background-color: #233044 !important;
            border: 2px solid #22d3ee !important; /* Cadre Turquoise */
            padding: 14px 18px !important;
            border-radius: 12px !important;
            box-shadow: 0 15px 20px -5px rgba(0, 0, 0, 0.5) !important;
        }
        
        div[data-testid="stBorderedContainer"]:has(.card-mid-right) {
            background-color: #141c29 !important;
            border: 2px solid #475569 !important; /* Cadre Acier Mat */
            padding: 14px 18px !important;
            border-radius: 12px !important;
            box-shadow: 0 15px 20px -5px rgba(0, 0, 0, 0.5) !important;
        }
        
        /* Ajustements généraux */
        .inner-title { text-align: center; font-weight: bold; font-size: 16px; color: #38bdf8; margin-bottom: 6px; }
        h1 { font-size: 24px !important; margin-top: 0px !important; margin-bottom: 8px !important; }
        h2 { font-size: 18px !important; margin-top: 4px !important; margin-bottom: 8px !important; }
        [data-testid="stHeader"] { height: 0px; }
        
        .stExpander {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 6px !important;
            margin-bottom: 4px !important;
        }
        
        .anecdote { background-color: #1e3a8a; padding: 10px 14px; border-left: 4px solid #3b82f6; border-radius: 4px; margin: 6px 0; color: #eff6ff; font-size: 13px; }
        .unit-box { background-color: #1e293b; padding: 10px; border-radius: 6px; border: 1px dashed #475569; margin-bottom: 10px; font-size: 13px; }
        
        /* Ajustement des barres de progression */
        .pole-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; margin-bottom: 3px; margin-top: 3px; color: #f1f5f9; }
        .sub-pole-header { display: flex; justify-content: space-between; font-size: 12px; color: #cbd5e1; margin-bottom: 2px; margin-top: 4px; }
        .bar-container { background-color: #475569; border-radius: 4px; height: 11px; width: 100%; margin-bottom: 8px; overflow: hidden; }
        .sub-bar-container { background-color: #334155; border-radius: 3px; height: 7px; width: 100%; margin-bottom: 6px; overflow: hidden; }
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

# 3. VARIABLES DE CONNEXION GOOGLE SHEETS
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

# 4. CHARGEMENT UNIVERSEL DES DONNÉES (Anti-Coupures et tolérant aux accents)
@st.cache_data(ttl=30)
def load_data():
    try:
        raw = pd.read_csv(url, header=None)
        for i, row in raw.iterrows():
            row_str = [str(x).lower().replace('é','e').replace('è','e').strip() for x in row.values]
            if any("etablissement" in x or "ecole" in x for x in row_str):
                data = raw.iloc[i+1:].copy()
                new_cols = [str(val).strip() if pd.notnull(val) else f"Col_{j}" for j, val in enumerate(row.values)]
                data.columns = new_cols
                return data.loc[:, ~data.columns.duplicated()].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
    return pd.DataFrame()

df = load_data()

# 🎛️ EXTRACTEURS ET EXTRACTEURS SÉCURISÉS DYNAMIQUES ANTI-KEYERROR (Tolérance totale aux labels)
def get_row_val(row_data, keywords, exclude=None):
    for col_name in row_data.index:
        c_clean = str(col_name).lower().replace('é','e').replace('è','e').replace('â','a').replace('ô','o').strip()
        if exclude and any(ex in c_clean for ex in exclude):
            continue
        if any(k.lower() in c_clean for k in keywords):
            return row_data[col_name]
    return 0

def get_col_sum(dataframe, keywords, exclude=None):
    for col_name in dataframe.columns:
        c_clean = str(col_name).lower().replace('é','e').replace('è','e').replace('â','a').replace('ô','o').strip()
        if exclude and any(ex in c_clean for ex in exclude):
            continue
        if any(k.lower() in c_clean for k in keywords):
            return dataframe[col_name].sum()
    return 0

# Identification automatique des pivots de colonnes
if not df.empty:
    df.columns = [str(c).replace('\xa0', ' ').replace('\n', ' ').strip() for c in df.columns]
    df.columns = [" ".join(c.split()) for c in df.columns]
    
    col_etab = next((c for c in df.columns if any(k in c.lower() for k in ["etab", "étab", "ecole", "école"])), df.columns[0])
    
    max_idx = len(df.columns) - 1
    col_total = next((c for c in df.columns if "total émission" in c.lower() or "total emission" in c.lower() or "total" in c.lower()), df.columns[7 if max_idx >= 7 else max_idx])
    col_eff = next((c for c in df.columns if "effectif" in c.lower()), df.columns[1 if max_idx >= 1 else max_idx])
    col_conso = next((c for c in df.columns if "conso" in c.lower() or "personne" in c.lower()), df.columns[8 if max_idx >= 8 else max_idx])

    # Conversion numérique globale
    cols_to_convert = [c for c in df.columns if c != col_etab]
    for col in cols_to_convert:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
    
    # Filtre souple pour garder TOUTES les lignes saisies sans blocage
    df_active = df[df[col_etab].astype(str).str.strip() != ""].copy()
    df_active = df_active[~df_active[col_etab].astype(str).str.lower().str.contains("total|moyenne")].copy()

# 5. CONFIGURATION DE L'INTERFACE À 3 ONGLETS AVEC LE NOM MODIFIÉ
tab_dashboard, tab_conso_graph, tab_glossaire = st.tabs(["📊 Tableau de Bord", "🌱 Empreinte carbone", "📖 Référentiel Éléves"])

# ==========================================
# ---          1. ONGLET DASHBOARD       ---
# ==========================================
with tab_dashboard:
    if not df.empty:
        st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
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

        # --- 2️⃣ BLOC DU MILIEU : DOUBLE TUILE EN FACE-À-FACE SÉCURISÉE ---
        st.markdown('<h2 style="text-align: center; color: #38bdf8;">🔍 Analyse Comparative des Pôles</h2>', unsafe_allow_html=True)
        
        if not df_active.empty:
            col_mid1, col_mid2 = st.columns([1, 1])
            
            # --- 🅰️ TABLEAU GAUCHE : ÉTABLISSEMENT UNIQUE (CADRE TURQUOISE) ---
            with col_mid1:
                with st.container(border=True):
                    st.markdown('<div class="card-mid-left"></div>', unsafe_allow_html=True)
                    selected_school = st.selectbox("Sélectionnez votre établissement :", df_active[col_etab].unique(), key="left_school_selector")
                    st.markdown(f'<p class="inner-title" style="color: #22d3ee; text-align: left; margin-top: 5px; margin-bottom: 10px; font-size: 18px; font-weight: bold;">🏫 Établissement Audité : {selected_school}</p>', unsafe_allow_html=True)
                    
                    school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
                    tot_sch = school_data[col_total]
                    
                    if tot_sch >= 0:
                        # Extractions blindées via listes de mots-clés
                        e_elec = get_row_val(school_data, ["electricite"])
                        e_fioul = get_row_val(school_data, ["fioul", "fuel"])
                        e_gaz = get_row_val(school_data, ["gaz"])
                        sch_energie = e_elec + e_fioul + e_gaz

                        a_m = get_row_val(school_data, ["repas moyen"])
                        a_v = get_row_val(school_data, ["vegetarien", "vege"])
                        a_r = get_row_val(school_data, ["viande rouge", "boeuf", "bœuf"])
                        a_b = get_row_val(school_data, ["viande blanche", "poulet"])
                        a_p = get_row_val(school_data, ["poisson"])
                        sch_alimentation = a_m + a_v + a_r + a_b + a_p

                        t_voit = get_row_val(school_data, ["voiture"])
                        t_bus_v = get_row_val(school_data, ["ville"])
                        t_bus_s = get_row_val(school_data, ["sortie"])
                        sch_transport = t_voit + t_bus_v + t_bus_s

                        # Exclusion des "dechets" pour ne pas fausser le calcul matériel
                        b_pap = get_row_val(school_data, ["papier", "paper"], exclude=["dechet", "déchet"])
                        b_plas = get_row_val(school_data, ["plastique"], exclude=["dechet", "déchet"])
                        b_cart = get_row_val(school_data, ["carton"], exclude=["dechet", "déchet"])
                        b_ord = get_row_val(school_data, ["ordinateur", "ecran", "écran"])
                        b_imp = get_row_val(school_data, ["imprimante"])
                        b_phot = get_row_val(school_data, ["photocopieur"])
                        b_vid = get_row_val(school_data, ["video", "projecteur"])
                        sch_biens = b_pap + b_plas + b_cart + b_ord + b_imp + b_phot + b_vid

                        d_p = get_row_val(school_data, ["dechets papier", "déchets papier"])
                        d_a = get_row_val(school_data, ["dechets alimentaire", "déchets alimentaire", "gaspillage"])
                        d_pl = get_row_val(school_data, ["dechets plastique", "déchets plastique"])
                        sch_dechets = d_p + d_a + d_pl

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
                            draw_custom_bar("• Voiture individuelle", t_voit, sch_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Bus / Autocar (sorties)", t_bus_s, sch_transport, "#60a5fa", is_sub=True)

                        draw_custom_bar("📦 Biens, Consommables & Équipements", sch_biens, tot_sch, "#a855f7")
                        with st.expander("Détails Équipements"):
                            draw_custom_bar("• Ordinateur à écran plat", b_ord, sch_biens, "#c084fc", is_sub=True)
                            draw_custom_bar("• Ramettes de papier consommées", b_pap, sch_biens, "#c084fc", is_sub=True)

                        draw_custom_bar("🗑️ Gestion des Déchets", sch_dechets, tot_sch, "#6366f1")
                        with st.expander("Détails Déchets"):
                            draw_custom_bar("• Restes alimentaires", d_a, sch_dechets, "#818cf8", is_sub=True)
                            draw_custom_bar("• Déchets plastique", d_pl, sch_dechets, "#818cf8", is_sub=True)

            # --- 🆂 TABLEAU DROIT : PÔLES CUMULÉS DU RÉSEAU (CADRE ACIER SOMBRE) ---
            with col_mid2:
                with st.container(border=True):
                    st.markdown('<div class="card-mid-right"></div>', unsafe_allow_html=True)
                    st.markdown('<p class="inner-title" style="color: #cbd5e1; text-align: left; margin-bottom: 45px; font-size: 18px; font-weight: bold;">🌍 Global : Secteurs d\'impact du Réseau</p>', unsafe_allow_html=True)
                    
                    tot_net = df_active[col_total].sum()
                    
                    if tot_net >= 0:
                        net_elec = get_col_sum(df_active, ["electricite"])
                        net_fioul = get_col_sum(df_active, ["fioul", "fuel"])
                        net_gaz = get_col_sum(df_active, ["gaz"])
                        net_energie = net_elec + net_fioul + net_gaz

                        net_a_m = get_col_sum(df_active, ["repas moyen"])
                        net_a_v = get_col_sum(df_active, ["vegetarien", "vege"])
                        net_a_r = get_col_sum(df_active, ["viande rouge", "boeuf", "bœuf"])
                        net_a_b = get_col_sum(df_active, ["viande blanche", "poulet"])
                        net_a_p = get_col_sum(df_active, ["poisson"])
                        net_alimentation = net_a_m + net_a_v + net_a_r + net_a_b + net_a_p

                        net_t_voit = get_col_sum(df_active, ["voiture"])
                        net_t_bus_v = get_col_sum(df_active, ["ville"])
                        net_t_bus_s = get_col_sum(df_active, ["sortie"])
                        net_transport = net_t_voit + net_t_bus_v + net_t_bus_s

                        net_b_pap = get_col_sum(df_active, ["papier", "paper"], exclude=["dechet", "déchet"])
                        net_b_plas = get_col_sum(df_active, ["plastique"], exclude=["dechet", "déchet"])
                        net_b_cart = get_col_sum(df_active, ["carton"], exclude=["dechet", "déchet"])
                        net_b_ord = get_col_sum(df_active, ["ordinateur", "ecran", "écran"])
                        net_b_imp = get_col_sum(df_active, ["imprimante"])
                        net_b_phot = get_col_sum(df_active, ["photocopi"])
                        net_b_vid = get_col_sum(df_active, ["video", "projecteur"])
                        net_biens = net_b_pap + net_b_plas + net_b_cart + net_b_ord + net_b_imp + net_b_phot + net_b_vid

                        net_d_p = get_col_sum(df_active, ["dechets papier", "déchets papier"])
                        net_d_a = get_col_sum(df_active, ["dechets alimentaire", "déchets alimentaire", "gaspillage"])
                        net_d_pl = get_col_sum(df_active, ["dechets plastique", "déchets plastique"])
                        net_dechets = net_d_p + net_d_a + net_d_pl

                        # Rendu des barres globales
                        draw_custom_bar("❄️ Énergie & Bâtiments (Total Réseau)", net_energie, tot_net, "#22c55e")
                        with st.expander("Détails Énergie Réseau"):
                            draw_custom_bar("• Électricité française totale", net_elec, net_energie, "#4ade80", is_sub=True)
                            draw_custom_bar("• Gaz Naturel global", net_gaz, net_energie, "#4ade80", is_sub=True)

                        draw_custom_bar("🍎 Alimentation & Cantine (Total Réseau)", net_alimentation, tot_net, "#f97316")
                        with st.expander("Détails Restauration Réseau"):
                            draw_custom_bar("• Viande Rouge cumulée", net_a_r, net_alimentation, "#fb923c", is_sub=True)
                            draw_custom_bar("• Poisson cumulé", net_a_p, net_alimentation, "#fb923c", is_sub=True)

                        draw_custom_bar("🚌 Déplacements & Transports (Total Réseau)", net_transport, tot_net, "#3b82f6")
                        with st.expander("Détails Transports Réseau"):
                            draw_custom_bar("• Voiture à essence totale", net_t_voit, net_transport, "#60a5fa", is_sub=True)
                            draw_custom_bar("• Autobus scolaires total", net_t_bus_s, net_transport, "#60a5fa", is_sub=True)

                        draw_custom_bar("📦 Biens & Équipements (Total Réseau)", net_biens, tot_net, "#a855f7")
                        with st.expander("Détails Équipements Réseau"):
                            draw_custom_bar("• Total Ordinateurs / Écrans", net_b_ord, net_biens, "#c084fc", is_sub=True)

                        draw_custom_bar("🗑️ Gestion des Déchets (Total Réseau)", net_dechets, tot_net, "#6366f1")
                        with st.expander("Détails Déchets Réseau"):
                            draw_custom_bar("• Restes de cantine globaux", net_d_a, net_dechets, "#818cf8", is_sub=True)

# ==========================================
# ---    2. ONGLET EMPREINTE CARBONNE    ---
# ==========================================
with tab_conso_graph:
    if not df.empty:
        st.markdown("<h2 style='text-align: center; color: #22d3ee;'>📊 Comparatif Graphique Interactif du Réseau</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #cbd5e1;'>Classement global par établissement (kg CO2e par personne).</p>", unsafe_allow_html=True)
        
        # Graphique à barres horizontales moderne trié de manière ascendante
        df_sorted_graph = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=True)
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=df_sorted_graph[col_etab],
            x=df_sorted_graph[col_conso],
            orientation='h',
            marker=dict(color='#22d3ee', line=dict(color='#0f172a', width=1)),
            hovertemplate="<b>%{y}</b><br>Empreinte : <b>%{x:.1f} kg CO2e/pers</b><extra></extra>"
        ))
        
        fig_bar.update_layout(
            margin=dict(l=20, r=20, t=10, b=10),
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Consommation Carbone (kg / personne)", color="#cbd5e1", gridcolor="rgba(255,255,255,0.05)", showgrid=True),
            yaxis=dict(color="#f1f5f9", tickfont=dict(size=12))
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        
        # Grande table de synthèse déplacée ici
        st.markdown('<p class="inner-title">📋 Synthèse Globale Centralisée (Données Brutes du Réseau)</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch", height=250)

# ==========================================
# ---          3. ONGLET GLOSSAIRE       ---
# ==========================================
with tab_glossaire:
    st.markdown("<h2 style='color: #38bdf8; text-align: center; margin-bottom: 15px;'>📖 Dictionnaire Carbone : Unités & Équivalents Enfants</h2>", unsafe_allow_html=True)
    g_tabs = st.tabs(["🍎 1. Cantine", "❄️ 2. Énergie", "🚌 3. Transports", "🗑️ 4. Gaspillage", "📦 5. Matériel"])
    
    with g_tabs[0]:
        st.subheader("🍎 Référentiel carbone (ADEME)")
        st.markdown('<div class="unit-box">• <b>Repas Bœuf :</b> 7.26 kg CO2e | • <b>Poisson :</b> 2.00 kg CO2e | • <b>Viande Blanche :</b> 1.60 kg CO2e</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 3 Comparaisons Chocs :</b><br>1. 👟 <b>Baskets :</b> 1 repas bœuf = Fabriquer 1 paire de baskets neuve.<br>2. 📱 <b>TikTok :</b> Équivaut à 150 heures de streaming 4G.<br>3. 🥤 <b>Canettes :</b> Équivaut à l\'impact de 300 canettes en alu.</div>', unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("❄️ Référentiel carbone (ADEME)")
        st.markdown('<div class="unit-box">• <b>Électricité :</b> 0.06 kg CO2e/kWh | • <b>Gaz :</b> 0.24 kg CO2e/kWh</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 3 Comparaisons Chocs :</b><br>1. 🎮 <b>Gaming :</b> 1 kWh = Faire tourner une PS5 pendant 8 heures.<br>2. 🔋 <b>Recharge :</b> Recharger un smartphone tous les soirs pendant 2 ans.<br>3. 👕 <b>Fenêtres :</b> Ouvrir en hiver avec chauffage = Jeter l\'impact de 2 t-shirts neufs.</div>', unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("🚌 Référentiel carbone (ADEME)")
        st.markdown('<div class="unit-box">• <b>Voiture :</b> 0.26 kg CO2e/km | • <b>Autobus de ville :</b> 0.18 kg CO2e/km</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 3 Comparaisons Chocs :</b><br>1. 💬 <b>Snaps :</b> 4 km en voiture = Envoyer 250 Snaps vidéo.<br>2. 🧴 <b>Bouteilles plastique :</b> Pollution de 15 bouteilles de 1.5L.<br>3. 🚌 <b>Car scolaire :</b> Partager le car divise l\'impact par 50 !</div>', unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("🗑️ Référentiel carbone (ADEME)")
        st.markdown('<div class="unit-box">• <b>Gaspillage alimentaire :</b> 1.20 kg CO2e/kg | • <b>Gaspillage Pain :</b> 0.63 kg CO2e/kg</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 3 Comparaisons Chocs :</b><br>1. 🍔 <b>Burger :</b> Jeter 2 kg de nourriture = Jeter un double cheeseburger complet.<br>2. ✂️ <b>Sweat :</b> Gâcher 5 kg de restes = Découper un sweat neuf sans le porter.<br>3. 🛴 <b>Trottinette :</b> Jeter son plateau = Équivaut à rouler 40 km en trottinette électrique.</div>', unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("📦 Énergie Grise (ADEME)")
        st.markdown('<div class="unit-box">• <b>Grand Écran Plat :</b> 1 283 kg CO2e | • <b>Ordinateur Portable :</b> 161 kg CO2e</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 3 Comparaisons Chocs :</b><br>1. 👖 <b>Jeans :</b> 1 ordinateur portable = Fabriquer 7 jeans neufs.<br>2. 🛵 <b>Scooter :</b> 1 grand écran = Rejeter le CO2 de 5 000 km en scooter.<br>3. 🌳 <b>Forêt :</b> Utiliser 1 000 ramettes de papier = Abattre 10 arbres adultes.</div>', unsafe_allow_html=True)

st.divider()
st.caption("Sources des référentiels : Base Empreinte ADEME / Simulateur National 'Nos Gestes Climat' - Juin 2026")
