import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# 1. CONFIGURATION INITIALE DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# Moteur de recherche absolu pour ton fichier "image_1" à la racine
def get_base64_image(file_name_without_ext):
    current_dir = os.path.dirname(__file__)
    for ext in ["", ".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
        path = os.path.join(current_dir, file_name_without_ext + ext)
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return ""

# Chargement immédiat de la ressource image pour écarter les NameError
img_base64 = get_base64_image("image_1")

# 2. INJECTION DU FILTRE GLASSMORPHISM UNIVERSEL
def inject_glass_theme(img_b64):
    bg_style = f"""
    [data-testid="stAppViewContainer"], .stAppViewContainer {{
        background-image: url("data:image/jpeg;base64,{img_b64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
    }}
    """ if img_b64 else """
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%) !important;
    }}
    """
    
    st.markdown(
        f"""
        <style>
        {bg_style}

        /* Nettoyage complet des fonds par défaut de Streamlit */
        .stApp, [data-testid="stMain"], .main, [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockContainer"] {{
            background-color: transparent !important;
        }}
        
        /* 📐 AMÉNAGEMENT DU CADRE */
        [data-testid="stMainBlockContainer"], .main .block-container, .block-container {{
            background-color: transparent !important;
            padding-top: 0rem !important; 
            padding-bottom: 6rem !important; 
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 54% !important; 
            width: 54% !important;
            margin-left: auto !important; 
            margin-right: 2% !important;  
            margin-top: 5.5rem !important; 
        }}

        /* 💎 LES BLOCS DE VERRE */
        div[data-testid="stColumn"], 
        div[data-testid="stBorderedContainer"],
        .stDataFrame,
        div[role="tabpanel"] {{
            background-color: rgba(22, 32, 49, 0.15) !important; 
            backdrop-filter: blur(20px) saturate(130%) !important; 
            -webkit-backdrop-filter: blur(20px) saturate(130%) !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important; 
            padding: 10px !important; 
            border-radius: 10px !important;
            margin-bottom: 6px !important;
        }}

        /* 🛡️ SÉCURISATION DES EXPANDERS ET DE LEURS CHEVRONS */
        div[data-testid="stExpander"], .stExpander {{
            background-color: rgba(17, 24, 39, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 6px !important;
            padding: 6px 10px !important;
            margin-top: 3px !important;
            margin-bottom: 3px !important;
            box-shadow: none !important;
        }}
        
        div[data-testid="stExpander"] svg, .stExpander svg, [data-testid="stExpanderToggleIcon"] {{
            fill: #ffffff !important;
            color: #ffffff !important;
            display: inline-block !important;
        }}

        /* --- 🎛️ BOUTONS DE NAVIGATION DU HAUT --- */
        div[data-baseweb="tab-list"] {{
            gap: 6px !important;
            background-color: transparent !important;
            margin-bottom: 10px !important;
            position: fixed !important; 
            top: 55px !important; 
            right: 2% !important;
            width: 52% !important; 
            z-index: 99999 !important; 
        }}
        div[data-baseweb="tab-list"] button {{
            background-color: rgba(22, 32, 49, 0.85) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 6px 6px 0 0 !important;
            padding: 5px 12px !important; 
            color: #cbd5e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: all 0.2s ease !important;
            font-weight: bold !important;
            font-size: 13px !important; 
        }}
        div[data-baseweb="tab-list"] button:hover {{
            background-color: rgba(55, 65, 81, 0.9) !important;
            border-color: #22d3ee !important;
            color: #ffffff !important;
        }}
        div[data-baseweb="tab-list"] button[aria-selected="true"] {{
            background-color: #22d3ee !important;
            color: #0f172a !important;
            border-color: #22d3ee !important;
            box-shadow: 0 4px 12px rgba(34, 211, 238, 0.4) !important;
        }}

        /* 🛡️ TEXTES ET TITRES GÉNÉRAUX */
        h1, h2, h3, h4, h5, h6, label, p, .stMarkdown p, [data-testid="stWidgetLabel"] p, summary {{
            color: #f8fafc !important;
            font-weight: bold !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7) !important;
        }}
        
        h1 {{ font-size: 20px !important; margin-bottom: 6px !important; }}
        h2 {{ font-size: 16px !important; margin-bottom: 4px !important; }}
        
        .pole-header, .sub-pole-header {{ 
            display: flex !important; 
            justify-content: space-between !important; 
            flex-wrap: wrap !important;
            gap: 2px !important;
            color: #f8fafc !important; 
            font-weight: bold !important; 
            font-size: 13px !important;
        }}
        
        .inner-title {{ text-align: center; font-weight: bold; font-size: 13px; color: #38bdf8 !important; margin-bottom: 4px; }}
        [data-testid="stHeader"] {{ height: 0px; }}
        
        /* ⚡ LABELS GRAPHIQUE */
        .js-plotly-plot .plotly .yaxislayer-above .tick text {{
            fill: #0f172a !important;
            font-weight: 900 !important;
            font-size: 12px !important;
        }}
        .js-plotly-plot .plotly .xaxislayer-above .tick text {{
            fill: #0f172a !important;
            font-weight: 900 !important;
            font-size: 11px !important;
        }}
        
        .anecdote {{ background-color: rgba(2, 132, 199, 0.25); padding: 8px 10px; border-left: 4px solid #0284c7; border-radius: 4px; color: #ffffff !important; font-size: 12px; margin-top: 3px; }}
        .unit-box {{ background-color: rgba(17, 24, 39, 0.55) !important; padding: 6px 8px; border-radius: 6px; border: 1px dashed rgba(255,255,255,0.2); font-size: 12px; color: #ffffff !important; margin-bottom: 3px; }}
        
        .bar-container {{ background-color: rgba(255, 255, 255, 0.15); border-radius: 4px; height: 8px; width: 100%; margin-bottom: 4px; overflow: hidden; }}
        .sub-bar-container {{ background-color: rgba(255, 255, 255, 0.08); border-radius: 3px; height: 6px; width: 100%; margin-bottom: 3px; overflow: hidden; }}
        
        .js-plotly-plot .plotly .main-svg {{ background: transparent !important; }}
        .stDataFrame div {{ background-color: transparent !important; }}
        hr {{ margin-top: 6px !important; margin-bottom: 6px !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )

inject_glass_theme(img_base64)

# 3. INTERFACE DE CONSTRUCTION DES JAUGE ADEME
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

# 4. TUNNEL D'ACCÈS GOOGLE SHEETS
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

@st.cache_data(ttl=30)
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
        st.error(f"Erreur de synchronisation Google Sheets : {e}")
    return pd.DataFrame()

df = load_data()

def safe_get_val(row_data, col_name):
    if col_name in row_data.index:
        return row_data[col_name]
    for c in row_data.index:
        if str(c).lower().replace('é','e').strip() == str(col_name).lower().replace('é','e').strip():
            return row_data[c]
    return 0.0

def safe_sum_val(dataframe, col_name):
    if col_name in dataframe.columns:
        return dataframe[col_name].sum()
    for c in dataframe.columns:
        if str(c).lower().replace('é','e').strip() == str(col_name).lower().replace('é','e').strip():
            return dataframe[c].sum()
    return 0.0

if not df.empty:
    df.columns = [str(c).replace('\xa0', ' ').replace('\n', ' ').strip() for c in df.columns]
    df.columns = [" ".join(c.split()) for c in df.columns]

# 5. INITIALISATION DES ONGLETS DE NAVIGATION
tab_dashboard, tab_conso_graph, tab_glossaire = st.tabs(["📊 Tableau de Bord", "🌱 Empreinte carbone", "📖 Référentiel Éléves"])

# ==========================================
# ---          1. ONGLET DASHBOARD       ---
# ==========================================
with tab_dashboard:
    if not df.empty:
        col_etab = "Etablissements" if "Etablissements" in df.columns else df.columns[0]
        col_total = "Total émissions" if "Total émissions" in df.columns else df.columns[7]
        col_eff = "Effectif total" if "Effectif total" in df.columns else df.columns[1]
        col_conso = "conso carbone par personne" if "conso carbone par personne" in df.columns else df.columns[8]

        cols_to_convert = [c for c in df.columns if c != col_etab]
        for col in cols_to_convert:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df_active = df[df[col_etab].astype(str).str.strip() != ""].copy()
        df_active = df_active[~df_active[col_etab].astype(str).str.lower().str.contains("total|moyenne")].copy()

        st.markdown("<h1 style='text-align: center; color: #22d3ee; margin-bottom: 5px;'>🌱 Défi Carbone - Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        with st.expander("🔐 Saisie de nouvelles données", expanded=False):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire Google Forms", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)

        col_top1, col_top2 = st.columns([1, 1])
        with col_top1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements (kg/personne)</p>', unsafe_allow_html=True)
            if not df_active.empty:
                df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                st.dataframe(df_ranking, hide_index=True, width="stretch", height=215)
            else:
                st.info("En attente de données...")
                
        with col_top2:
            st.markdown('<p class="inner-title">🚀 Moyenne Globale du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            if not df_active.empty and df_active[col_eff].sum() > 0:
                moyenne = df_active[col_total].sum() / df_active[col_eff].sum()
            else:
                moyenne = 0

            fig = go.Figure(go.Indicator(
                mode = "gauge+number", 
                value = moyenne, 
                domain = {'x': [0.1, 0.9], 'y': [0, 1]},
                number = {
                    'suffix': " kg", 
                    'font': {'color': '#f1f5f9', 'size': 18}
                }, 
                gauge = {
                    'axis': {'range': [None, 2000], 'tickfont': {'color': '#cbd5e1', 'size': 9}}, 
                    'bar': {'color': "#22d3ee"}, 
                    'steps': [{'range': [0, 500], 'color': "rgba(34, 197, 94, 0.25)"}, {'range': [500, 1000], 'color': "rgba(249, 115, 22, 0.25)"}, {'range': [1000, 2000], 'color': "rgba(239, 68, 68, 0.25)"}], 
                    'threshold': {'line': {'color': "red", 'width': 3}, 'value': 1000}
                }
            ))
            fig.update_layout(height=160, margin=dict(t=20, b=5, l=5, r=5), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        st.markdown("<h2 style='text-align: center; color: #22d3ee; margin-bottom: 5px;'>🔍 Analyse Comparative des Pôles</h2>", unsafe_allow_html=True)
        
        if not df_active.empty:
            col_mid1, col_mid2 = st.columns([1, 1])
            
            # --- 🏫 COLONNE DE GAUCHE : ÉTABLISSEMENT UNIQUE ---
            with col_mid1:
                selected_school = st.selectbox("Établissement audité :", df_active[col_etab].unique(), key="left_school_selector")
                st.markdown(f'<p class="inner-title" style="color: #38bdf8; text-align: left; font-size: 15px; margin-bottom: 4px;">🏫 Établissement Audité : {selected_school}</p>', unsafe_allow_html=True)
                
                school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
                tot_sch = school_data[col_total]
                
                if tot_sch >= 0:
                    sch_energie = safe_get_val(school_data, "Electricité française") + safe_get_val(school_data, "Fioul") + safe_get_val(school_data, "Gaz Naturel")
                    sch_alimentation = safe_get_val(school_data, "Repas moyen") + safe_get_val(school_data, "Repas végétarien") + safe_get_val(school_data, "Repas viande rouge") + safe_get_val(school_data, "Repas viande blanche") + safe_get_val(school_data, "Repas POISSON")
                    sch_transport = safe_get_val(school_data, "Voiture à essence") + safe_get_val(school_data, "Autobus (ville)") + safe_get_val(school_data, "Autobus (sortie scolaire)")
                    b_pap = safe_get_val(school_data, "Paper") if safe_get_val(school_data, "Paper") > 0 else safe_get_val(school_data, "Papier")
                    sch_biens = b_pap + safe_get_val(school_data, "Plastique") + safe_get_val(school_data, "Carton") + safe_get_val(school_data, "Ordinateur à écran plat") + safe_get_val(school_data, "Imprimante") + safe_get_val(school_data, "Photocopieurs") + safe_get_val(school_data, "Vidéo projecteur")
                    sch_dechets = safe_get_val(school_data, "Déchets Papier") + safe_get_val(school_data, "Déchets alimentaire") + safe_get_val(school_data, "Déchets plastique")

                    # Énergie
                    draw_custom_bar("❄️ Énergie & Bâtiments", sch_energie, tot_sch, "#4ade80")
                    with st.expander("🔍 Détails Énergie"):
                        draw_custom_bar("• Électricité française", safe_get_val(school_data, "Electricité française"), sch_energie, "#22c55e", is_sub=True)
                        draw_custom_bar("• Gaz Naturel", safe_get_val(school_data, "Gaz Naturel"), sch_energie, "#22c55e", is_sub=True)
                        draw_custom_bar("• Fioul de chauffage", safe_get_val(school_data, "Fioul de chauffage"), sch_energie, "#22c55e", is_sub=True)

                    # Alimentation
                    draw_custom_bar("🍎 Alimentation & Cantine", sch_alimentation, tot_sch, "#fb923c")
                    with st.expander("🔍 Détails Restauration"):
                        draw_custom_bar("• Repas Viande Rouge", safe_get_val(school_data, "Repas viande rouge"), sch_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Poisson", safe_get_val(school_data, "Repas POISSON"), sch_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Standard Moyen", safe_get_val(school_data, "Repas moyen"), sch_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Végétarien", safe_get_val(school_data, "Repas végétarien"), sch_alimentation, "#f97316", is_sub=True)

                    # Transports
                    draw_custom_bar("🚌 Déplacements & Transports", sch_transport, tot_sch, "#60a5fa")
                    with st.expander("🔍 Détails Transports"):
                        draw_custom_bar("• Voiture à essence", safe_get_val(school_data, "Voiture à essence"), sch_transport, "#3b82f6", is_sub=True)
                        draw_custom_bar("• Autobus (sorties / voyages)", safe_get_val(school_data, "Autobus (sortie scolaire)"), sch_transport, "#3b82f6", is_sub=True)

                    # Biens & Équipements
                    draw_custom_bar("📦 Biens, Consommables & Équipements", sch_biens, tot_sch, "#c084fc")
                    with st.expander("🔍 Détails Consommables & Matériel"):
                        draw_custom_bar("• Papier & Carton", b_pap + safe_get_val(school_data, "Carton"), sch_biens, "#a855f7", is_sub=True)
                        draw_custom_bar("• Plastiques & Fournitures", safe_get_val(school_data, "Plastique"), sch_biens, "#a855f7", is_sub=True)
                        draw_custom_bar("• Appareils Numériques", safe_get_val(school_data, "Ordinateur à écran plat") + safe_get_val(school_data, "Imprimante") + safe_get_val(school_data, "Photocopieurs") + safe_get_val(school_data, "Vidéo projecteur"), sch_biens, "#a855f7", is_sub=True)

                    # Déchets
                    draw_custom_bar("🗑️ Gestion des Déchets", sch_dechets, tot_sch, "#818cf8")
                    with st.expander("🔍 Détails Élimination Déchets"):
                        draw_custom_bar("• Déchets Papier / Carton", safe_get_val(school_data, "Déchets Papier"), sch_dechets, "#6366f1", is_sub=True)
                        draw_custom_bar("• Déchets Alimentaires", safe_get_val(school_data, "Déchets alimentaire"), sch_dechets, "#6366f1", is_sub=True)
                        draw_custom_bar("• Déchets Plastiques", safe_get_val(school_data, "Déchets plastique"), sch_dechets, "#6366f1", is_sub=True)

            # --- 🌍 COLONNE DE DROITE : TOTAL RÉSEAU CENTRALISÉ ---
            with col_mid2:
                st.markdown('<p class="inner-title" style="color: #38bdf8; text-align: left; font-size: 15px;">🌍 Global : Secteurs d\'impact du Réseau</p>', unsafe_allow_html=True)
                
                tot_net = df_active[col_total].sum()
                if tot_net >= 0:
                    net_elec = safe_sum_val(df_active, "Electricité française")
                    net_fioul = safe_sum_val(df_active, "Fioul") + safe_sum_val(df_active, "Fioul de chauffage")
                    net_gaz = safe_sum_val(df_active, "Gaz Naturel")
                    net_energie = net_elec + net_fioul + net_gaz

                    net_alimentation = safe_sum_val(df_active, "Repas moyen") + safe_sum_val(df_active, "Repas végétarien") + safe_sum_val(df_active, "Repas viande rouge") + safe_sum_val(df_active, "Repas viande blanche") + safe_sum_val(df_active, "Repas POISSON")
                    net_transport = safe_sum_val(df_active, "Voiture à essence") + safe_sum_val(df_active, "Autobus (ville)") + safe_sum_val(df_active, "Autobus (sortie scolaire)")
                    
                    net_pap = safe_sum_val(df_active, "Paper") + safe_sum_val(df_active, "Papier")
                    net_carton = safe_sum_val(df_active, "Carton")
                    net_plast = safe_sum_val(df_active, "Plastique")
                    net_num = safe_sum_val(df_active, "Ordinateur à écran plat") + safe_sum_val(df_active, "Imprimante") + safe_sum_val(df_active, "Photocopieurs") + safe_sum_val(df_active, "Vidéo projecteur")
                    net_biens = net_pap + net_carton + net_plast + net_num
                    
                    net_dec_pap = safe_sum_val(df_active, "Déchets Papier")
                    net_dec_alim = safe_sum_val(df_active, "Déchets alimentaire")
                    net_dec_plast = safe_sum_val(df_active, "Déchets plastique")
                    net_dechets = net_dec_pap + net_dec_alim + net_dec_plast

                    # Énergie Globale
                    draw_custom_bar("❄️ Énergie & Bâtiments (Total Réseau)", net_energie, tot_net, "#4ade80")
                    with st.expander("🔍 Détails Énergie Globaux"):
                        draw_custom_bar("• Électricité française", net_elec, net_energie, "#22c55e", is_sub=True)
                        draw_custom_bar("• Gaz Naturel", net_gaz, net_energie, "#22c55e", is_sub=True)
                        draw_custom_bar("• Fioul de chauffage", net_fioul, net_energie, "#22c55e", is_sub=True)

                    # Alimentation Globale
                    draw_custom_bar("🍎 Alimentation & Cantine (Total Réseau)", net_alimentation, tot_net, "#fb923c")
                    with st.expander("🔍 Détails Restauration Globaux"):
                        draw_custom_bar("• Repas Viande Rouge", safe_sum_val(df_active, "Repas viande rouge"), net_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Poisson", safe_sum_val(df_active, "Repas POISSON"), net_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Standard Moyen", safe_sum_val(df_active, "Repas moyen"), net_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Végétarien", safe_sum_val(df_active, "Repas végétarien"), net_alimentation, "#f97316", is_sub=True)

                    # Transports Globaux
                    draw_custom_bar("🚌 Déplacements & Transports (Total Réseau)", net_transport, tot_net, "#60a5fa")
                    with st.expander("🔍 Détails Transports Globaux"):
                        draw_custom_bar("• Voiture à essence", safe_sum_val(df_active, "Voiture à essence"), net_transport, "#3b82f6", is_sub=True)
                        draw_custom_bar("• Autobus", safe_sum_val(df_active, "Autobus (sortie scolaire)") + safe_sum_val(df_active, "Autobus (ville)"), net_transport, "#3b82f6", is_sub=True)

                    # Biens Globaux
                    draw_custom_bar("📦 Biens & Équipements (Total Réseau)", net_biens, tot_net, "#c084fc")
                    with st.expander("🔍 Détails Biens Globaux"):
                        draw_custom_bar("• Papier & Carton", net_pap + net_carton, net_biens, "#a855f7", is_sub=True)
                        draw_custom_bar("• Plastiques consommables", net_plast, net_biens, "#a855f7", is_sub=True)
                        draw_custom_bar("• Parc informatique & numérique", net_num, net_biens, "#a855f7", is_sub=True)

                    # Déchets Globaux
                    draw_custom_bar("🗑️ Élimination des Déchets (Total Réseau)", net_dechets, tot_net, "#818cf8")
                    with st.expander("🔍 Détails Déchets Globaux"):
                        draw_custom_bar("• Déchets Papier / Carton", net_dec_pap, net_dechets, "#6366f1", is_sub=True)
                        draw_custom_bar("• Déchets Alimentaires", net_dec_alim, net_dechets, "#6366f1", is_sub=True)
                        draw_custom_bar("• Déchets Plastiques", net_dec_plast, net_dechets, "#6366f1", is_sub=True)

# ==========================================
# ---    2. ONGLET EMPREINTE CARBONNE    ---
# ==========================================
with tab_conso_graph:
    if not df.empty:
        st.markdown("<h2 style='text-align: center; color: #22d3ee; margin-bottom: 12px;'>📊 Comparatif Graphique Interactif du Réseau</h2>", unsafe_allow_html=True)
        
        df_sorted_graph = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=True)
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=df_sorted_graph[col_etab],
            x=df_sorted_graph[col_conso],
            orientation='h',
            marker=dict(color='#22d3ee', line=dict(color='rgba(255,255,255,0.2)', width=1)),
            hovertemplate="<b>%{y}</b><br>Empreinte : <b>%{x:.1f} kg CO2e/pers</b><extra></extra>"
        ))
        
        fig_bar.update_layout(
            margin=dict(l=20, r=20, t=10, b=10),
            height=460,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Consommation Carbone (kg / personne)", color="#f1f5f9", gridcolor="rgba(255,255,255,0.1)", showgrid=True),
            yaxis=dict(color="#f1f5f9", showgrid=False)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        st.markdown('<p class="inner-title" style="color:#38bdf8;">📋 Synthèse Globale Centralisée KgCo2e</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch", height=280)

# ==========================================
# ---          3. ONGLET GLOSSAIRE       ---
# ==========================================
with tab_glossaire:
    st.markdown("<h2 style='color: #22d3ee; text-align: center; margin-bottom: 12px;'>📖 Dictionnaire Carbone : Unités & Équivalents Enfants</h2>", unsafe_allow_html=True)
    
    g_tabs = st.tabs(["🍎 Cantine", "❄️ Énergie", "🚌 Transports", "📦 Biens & Équipements", "🗑️ Déchets"])
    
    with g_tabs[0]:
        st.subheader("🍎 Référentiel Restauration (ADEME)")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Valeurs d\'empreinte de la Cantine :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Repas viande rouge (bœuf) :</b> 7.26 kg CO2e<br>• <b>Repas poisson :</b> 2.00 kg CO2e<br>• <b>Repas moyen / standard :</b> 2.10 kg CO2e<br>• <b>Repas végétarien :</b> 0.50 kg CO2e</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>1 seul repas au bœuf (7,2 kg)</b> = Fabriquer une paire de baskets de marque neuve 👟<br>
            • <b>1 seul repas au bœuf</b> = Envoyer 15 000 SMS ou scroller non-stop 150 heures sur TikTok 📱<br>
            • <b>Prendre le repas Végétarien</b> = Économiser le carbone d'un trajet de 30 km en voiture familiale 🚗
            </div>""", unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("❄️ Référentiel Énergie & Fluides (ADEME)")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Facteurs d\'émissions des Bâtiments :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Fioul de chauffage :</b> 3.24 kg CO2e par litre<br>• <b>Gaz naturel :</b> 0.24 kg CO2e par kWh<br>• <b>Électricité française :</b> 0.06 kg CO2e par kWh</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>Chauffer une classe au fioul pendant 1 jour</b> = Parcourir 80 km en voiture thermique 🚘<br>
            • <b>Laisser un radiateur tourner avec la fenêtre ouverte 1h</b> = Laisser une console PS5 allumée pendant 6 mois 🎮<br>
            • <b>1 kWh d'Électricité en France (très bas)</b> = Regarder 25 heures de vidéos YouTube en Haute Définition 🎬
            </div>""", unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("🚌 Référentiel Déplacements (ADEME)")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Empreinte des Transports :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Voiture thermique (Moyenne) :</b> 0.22 kg CO2e par km<br>• <b>Autobus (Sortie scolaire / Voyage) :</b> 0.11 kg CO2e par km et par élève</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>Venir au collège à pied ou à vélo à l'année</b> = Économiser la capacité d'absorption de 5 arbres plantés 🌳<br>
            • <b>Un trajet de 15 km en voiture (3,3 kg)</b> = Regarder 30 heures de séries en streaming HD sur sa tablette 📺<br>
            • <b>Partir en voyage scolaire en bus blindé</b> = Diviser par deux sa pollution carbone par rapport au covoiturage 🚌
            </div>""", unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("📦 Biens, Consommables & Équipements")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Empreinte du matériel :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Paper (neuf) :</b> 1.20 kg CO2e par kg<br>• <b>Ordinateur portable :</b> ~250 kg CO2e (fabrication)<br>• <b>Vidéo projecteur :</b> ~180 kg CO2e (fabrication)</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>Fabriquer un seul ordinateur portable (250 kg)</b> = Rouler 1200 km en voiture ou fabriquer 150 t-shirts en coton 💻<br>
            • <b>Garder son smartphone 4 ans au lieu de 2 ans</b> = Éviter l'équivalent carbone de 400 repas végétariens 📱<br>
            • <b>Gâcher une ramette de papier blanc (3 kg)</b> = Laisser la lumière de sa chambre allumée pendant 2 mois non-stop 💡
            </div>""", unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("🗑️ Gestion des Déchets")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Empreinte des déchets :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Déchets papier/carton :</b> 0.15 kg CO2e par kg (trié)<br>• <b>Déchets plastiques :</b> 0.30 kg CO2e par kg (trié)<br>• <b>Déchets alimentaires :</b> 0.20 kg CO2e par kg</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>Trier 1 kg de bouteilles en plastique (0,30 kg évités)</b> = Économiser l'énergie de 3 cycles complets de machine à laver 🧺<br>
            • <b>Jeter un plateau repas entier à la poubelle</b> = Gaspiller l'équivalent en carbone d'une douche chaude de 6 minutes 🚿<br>
            • <b>Recycler le carton et le papier du collège</b> = Éviter l'incinération directe qui rejette des nuages de CO2 dans l'atmosphère 🗑️
            </div>""", unsafe_allow_html=True)

st.divider()
st.caption("Sources : Base Empreinte ADEME / Contexte Réseau Climat Haut Vaucluse - Juin 2026")
