import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os
from saisie_carbone import afficher_saisie_carbone

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
    background = (
        f"url('data:image/jpeg;base64,{img_b64}')"
        if img_b64 else "linear-gradient(135deg, #12372b, #102b36)"
    )
    st.markdown(
        f"<style>[data-testid='stAppViewContainer'] {{background-image: {background}; background-size: cover; background-position: center; background-attachment: fixed;}}</style>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <style>
    .stApp, [data-testid="stMain"] { background: transparent; }
    [data-testid="stMainBlockContainer"], .main .block-container {
        max-width: 1240px !important; width: 100% !important;
        margin: 0 auto !important; padding: 1.6rem 2rem 4rem !important;
    }
    [data-testid="stHeader"] { background: transparent; }
    h1, h2, h3, h4, h5, h6, .stMarkdown p,
    [data-testid="stWidgetLabel"] p, summary { color: #f3f8f5 !important; }
    h1, h2, h3, h4, h5, h6, [data-heading-text] { color: #f3f8f5 !important; }
    [role="tab"] p { color: #e6f0e9 !important; font-weight: 600; }
    [role="tab"][aria-selected="true"] p { color: #123a29 !important; }
    [role="tab"] { flex-shrink: 0; cursor: pointer; }
    h1 { font-size: clamp(1.8rem, 3vw, 2.5rem) !important; line-height: 1.15 !important; }
    h2 { font-size: 1.3rem !important; margin-top: 1rem !important; }
    .stMarkdown p { font-weight: 400; line-height: 1.6; }
    div[data-testid="stColumn"] {
        background: rgba(14, 35, 29, 0.38); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,.16);
        border-radius: 16px; padding: 18px; min-width: 0;
    }
    div[role="tablist"], div[data-baseweb="tab-list"] {
        position: static !important; top: auto !important; right: auto !important;
        width: 100% !important; gap: 8px !important; margin: 12px 0 20px !important;
        background: transparent !important; overflow-x: auto !important;
    }
    [role="tablist"] [role="tab"] {
        color: #e6f0e9 !important; background: rgba(14,35,29,.90) !important;
        border: 1px solid rgba(255,255,255,.25) !important; border-radius: 9px !important;
        padding: 10px 16px !important; min-height: 46px !important; font-size: 14px !important;
    }
    [role="tablist"] [role="tab"][aria-selected="true"] {
        background: #c8e8d4 !important; color: #123a29 !important; border-color: #c8e8d4 !important;
    }
    [role="tablist"] [role="tab"][aria-selected="true"] p { color: #123a29 !important; }
    div[data-testid="stExpander"] {
        background: rgba(10,28,23,.86); border: 1px solid rgba(255,255,255,.20);
        border-radius: 10px; margin: 8px 0 14px;
    }
    div[data-testid="stExpander"] summary svg { color: #f3f8f5; fill: #f3f8f5; }
    .inner-title { color: #a9dded !important; font-weight: 700; font-size: 15px; margin: 0 0 12px; }
    .pole-header, .sub-pole-header {
        display: flex; justify-content: space-between; flex-wrap: wrap; gap: 6px;
        color: #f3f8f5; font-weight: 600; font-size: 15px; margin: 6px 0;
    }
    .sub-pole-header { font-size: 14px; }
    .bar-container, .sub-bar-container { background: rgba(255,255,255,.14); height: 10px; border-radius: 6px; overflow: hidden; margin-bottom: 12px; }
    .sub-bar-container { height: 7px; }
    .unit-box { background: rgba(255,255,255,.08); color: #f3f8f5; border: 1px solid rgba(255,255,255,.20); border-radius: 10px; padding: 14px; font-size: 15px; line-height: 1.7; margin: 12px 0; }
    .anecdote { background: rgba(34,140,168,.17); color: #f3f8f5; border-left: 4px solid #73c7df; border-radius: 6px; padding: 14px; font-size: 14px; line-height: 1.7; margin: 12px 0; }
    .js-plotly-plot .plotly .main-svg { background: transparent !important; }
    hr { border-color: rgba(255,255,255,.20); margin: 24px 0; }
    [data-testid="stCaptionContainer"] p { color: #d0e1d5 !important; font-size: 13px; }
    @media (max-width: 760px) {
        [data-testid="stMainBlockContainer"], .main .block-container { padding: 1rem .85rem 3rem !important; }
        [data-testid="stHorizontalBlock"] { flex-direction: column !important; gap: 16px !important; }
        div[data-testid="stColumn"] { width: 100% !important; flex: 1 1 100% !important; padding: 14px; }
        [role="tablist"] [role="tab"] { padding: 9px 12px !important; font-size: 13px !important; }
        #eco-navigation { margin-bottom: 20px; }
    }
    h1, h2, h3, [data-testid="stMarkdownContainer"] > p { text-shadow: 0 1px 4px rgba(0,0,0,.85); }
    @media (min-width: 1100px) {
        [data-testid="stMainBlockContainer"], .main .block-container {
            width: 58% !important; max-width: 1050px !important;
            margin-left: auto !important; margin-right: 2% !important;
            padding-left: 1rem !important; padding-right: 1rem !important;
        }
    }
    .unit-box, .anecdote {
        background: rgba(10, 28, 23, .88) !important;
        color: #ffffff !important; backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px); box-shadow: 0 4px 16px rgba(0,0,0,.18);
    }
    .unit-box { border: 1px solid rgba(255,255,255,.30); }
    .anecdote { border-left: 4px solid #73c7df; }
    @media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; } }
    </style>
    """, unsafe_allow_html=True)

inject_glass_theme(img_base64)

# Navigation commune aux trois espaces du projet.
st.markdown('''<style id="eco-navigation-style">#eco-navigation{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:9px 12px;margin:0 0 16px;background:#f7faf8;color:#173e30;border:1px solid #ceded5;border-radius:10px;font:600 13px/1.3 system-ui,sans-serif;flex-shrink:0}#eco-navigation a{display:block;padding:9px 12px;border-radius:7px;color:#234b3b;text-decoration:none;white-space:normal}#eco-navigation a:hover,#eco-navigation a:focus-visible{background:#e1ede5;outline:2px solid #39785a;outline-offset:1px}#eco-navigation a[aria-current="page"]{background:#215e44;color:white}.main-container>#eco-navigation{margin:0;border-radius:0;border:0;border-bottom:1px solid #ceded5}@media print{#eco-navigation{display:none!important}}@media(max-width:600px){#eco-navigation{gap:3px;padding:6px;font-size:11px}#eco-navigation a{padding:8px}}#eco-navigation a:first-of-type{background:#eef1ef;color:#43534b}#eco-navigation a:first-of-type[aria-current="page"]{background:#d3dad6;color:#213d2e}#eco-navigation a:nth-of-type(2){background:#e0f2e3;color:#215e44;border-bottom:3px solid #3e7b4f}#eco-navigation a:nth-of-type(3){background:#fbefd5;color:#795217;border-bottom:3px solid #bf8b2e}#eco-navigation a:nth-of-type(4){background:#e3edfa;color:#234f79;border-bottom:3px solid #2f5d8a}#eco-navigation a:nth-of-type(2)[aria-current="page"]{background:#215e44;color:#fff}#eco-navigation a:nth-of-type(3)[aria-current="page"]{background:#93681e;color:#fff}#eco-navigation a:nth-of-type(4)[aria-current="page"]{background:#2f5d8a;color:#fff}</style><nav id="eco-navigation" aria-label="Changer d’espace"><a target="_blank" rel="noopener noreferrer" href="https://thierryarmant.github.io/Le-coin-des-ecodelegues/">Accueil</a><a target="_blank" rel="noopener noreferrer" href="https://thierryarmant.github.io/Le-coin-des-ecodelegues/cantine/">Planning</a><a target="_blank" rel="noopener noreferrer" href="https://thierryarmant.github.io/E3D-cantine/">A.B.C. Cantine Bas Carbone</a><span aria-current="page" title="Vous êtes dans les enquêtes" style="display:block;padding:9px 12px;border-radius:7px;background:#2f5d8a;color:white;font-weight:700">Enquêtes</span></nav>''', unsafe_allow_html=True)

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

# Accès rapide : relire les données sans modifier les réponses des établissements.
st.title("Défi Carbone · Haut Vaucluse")
st.markdown("Explorez les consommations des établissements, comparez les postes d’émission et retrouvez les repères pour les élèves.")
if st.button("↻ Actualiser les données", key="actualiser_donnees"):
    load_data.clear()
    st.rerun()
if df.empty:
    st.info("Aucune donnée disponible pour le moment. Vous pouvez consulter le référentiel et réessayer avec le bouton Actualiser.")

# 5. INITIALISATION DES ONGLETS DE NAVIGATION
tab_dashboard, tab_conso_graph, tab_saisie, tab_glossaire = st.tabs(["📊 Tableau de bord", "🌱 Comparer les établissements", "📝 Saisie", "📖 Référentiel élèves"])

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

        st.subheader("Vue d’ensemble du réseau")
        
        st.caption("Pour transmettre vos consommations, ouvrez l’onglet 📝 Saisie.")

        col_top1, col_top2 = st.columns([1, 1])
        with col_top1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements (kg/personne)</p>', unsafe_allow_html=True)
            if not df_active.empty:
                df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                recherche_etab = st.text_input("Rechercher un établissement", placeholder="Nom du collège, lycée ou école", key="recherche_classement")
                if recherche_etab.strip():
                    df_ranking = df_ranking[df_ranking[col_etab].astype(str).str.contains(recherche_etab.strip(), case=False, regex=False, na=False)]
                st.dataframe(df_ranking, hide_index=True, width="stretch", height=300)
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
            fig.update_layout(height=240, margin=dict(t=20, b=5, l=5, r=5), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
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
        
        etabs_graphique = st.multiselect("Établissements à comparer", options=df_active[col_etab].tolist(), default=df_active[col_etab].tolist(), help="Retirez des établissements pour concentrer le graphique. Le tableau complet reste disponible plus bas.")
        df_sorted_graph = df_active[df_active[col_etab].isin(etabs_graphique)][[col_etab, col_conso]].sort_values(col_conso, ascending=True)
        
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
            height=max(340, min(900, 90 + 30 * len(df_sorted_graph))),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Consommation Carbone (kg / personne)", color="#f1f5f9", gridcolor="rgba(255,255,255,0.1)", showgrid=True),
            yaxis=dict(color="#f1f5f9", showgrid=False)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        st.markdown('<p class="inner-title" style="color:#38bdf8;">📋 Synthèse Globale Centralisée KgCo2e</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch", height=360)
        st.download_button("Télécharger le bilan complet (CSV)", data=df.to_csv(index=False, sep=";").encode("utf-8-sig"), file_name="bilan-carbone-haut-vaucluse.csv", mime="text/csv", key="export_bilan_carbone")

# ==========================================
# ---          3. ONGLET GLOSSAIRE       ---
# ==========================================

# Saisie native : réutilise les établissements et le code de collecte existants.
with tab_saisie:
    code_saisie = st.text_input("Code de saisie du réseau", type="password", key="main_pwd")
    if code_saisie == "CARBONE2026":
        if afficher_saisie_carbone(df):
            load_data.clear()
    else:
        st.caption("Utilisez le code de collecte habituel du réseau pour renseigner les consommations.")

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
