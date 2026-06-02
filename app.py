import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# 1. CONFIGURATION DE LA PAGE
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

img_base64 = get_base64_image("image_1")

# 2. STYLE CSS (Moteur Pure Glassmorphism - Cristal Givré Blanc Lumineux)
def set_style(img_b64):
    bg_style = f"""
    [data-testid="stAppViewContainer"], .stAppViewContainer {{
        background-image: url("data:image/jpeg;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    """ if img_b64 else """
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }}
    """
    
    st.markdown(
        f"""
        <style>
        {bg_style}
        
        /* Nettoyage complet de tous les voiles opaques par défaut de Streamlit */
        .stApp, [data-testid="stMain"], .main, [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockContainer"] {{
            background-color: transparent !important;
        }}
        
        /* --- 💎 LE CADRE GLOSSY UNIQUE "SATIN GIVRÉ BLANC" LUNINEUX --- */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.48) !important; /* Transparence blanche cristalline et lumineuse */
            backdrop-filter: blur(25px) saturate(150%) !important; /* Magnifique effet givré translucide */
            -webkit-backdrop-filter: blur(25px) saturate(150%) !important;
            border: 1px solid rgba(255, 255, 255, 0.7) !important; /* Liseré blanc pur très net */
            padding: 2.5rem !important;
            border-radius: 24px !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1) !important;
            margin-top: 1rem !important;
        }}
        
        /* Sous-boîtes internes translucides pour structurer l'espace sans assombrir */
        div[data-testid="stBorderedContainer"], 
        div[data-testid="stColumn"],
        [data-testid="stExpander"], 
        .stExpander {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 14px !important;
            box-shadow: none !important;
            padding: 15px !important;
            margin-bottom: 10px !important;
        }}
        
        /* --- 🎛️ STYLE DES BOUTONS DE NAVIGATION INTER-ONGLETS --- */
        div[data-baseweb="tab-list"] {{
            gap: 12px !important;
            background-color: transparent !important;
            margin-bottom: 20px !important;
        }}
        div[data-baseweb="tab"], button[data-baseweb="tab"] {{
            background-color: rgba(255, 255, 255, 0.3) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            padding: 10px 22px !important;
            color: #0f172a !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            transition: all 0.2s ease !important;
            font-weight: bold !important;
            font-size: 14px !important;
        }}
        div[data-baseweb="tab"]:hover, button[data-baseweb="tab"]:hover {{
            background-color: rgba(255, 255, 255, 0.55) !important;
            border-color: #22d3ee !important;
        }}
        div[data-baseweb="tab"][aria-selected="true"], button[data-baseweb="tab"][aria-selected="true"] {{
            background-color: #22d3ee !important;
            color: #0f172a !important; 
            border-color: #22d3ee !important;
            box-shadow: 0 4px 14px rgba(34, 211, 238, 0.4) !important;
        }}
        [data-baseweb="tab-border"] {{ display: none !important; }}
        div[role="tabpanel"] {{ border: none !important; }}
        
        /* 🛡️ TEXTES ULTRA-NETS EN NOIR ARDOISE PROFOND SUR LE FOND CLAIR */
        h1, h2, h3, label, .stMarkdown p, [data-testid="stWidgetLabel"] p, .pole-header, .sub-pole-header {{
            color: #0f172a !important;
            font-weight: bold !important;
        }}
        
        .inner-title {{ text-align: center; font-weight: bold; font-size: 16px; color: #0284c7; margin-bottom: 12px; }}
        [data-testid="stHeader"] {{ height: 0px; }}
        
        /* Composants internes */
        .anecdote {{ background-color: rgba(2, 132, 199, 0.12); padding: 12px 14px; border-left: 4px solid #0284c7; border-radius: 4px; color: #0f172a; font-size: 13px; }}
        .unit-box {{ background-color: rgba(255, 255, 255, 0.5) !important; padding: 10px; border-radius: 6px; border: 1px dashed rgba(15, 23, 42, 0.35); font-size: 13px; color: #0f172a; }}
        
        /* Jauges et barres horizontales */
        .bar-container {{ background-color: rgba(15, 23, 42, 0.08); border-radius: 4px; height: 12px; width: 100%; margin-bottom: 8px; overflow: hidden; }}
        .sub-bar-container {{ background-color: rgba(15, 23, 42, 0.05); border-radius: 3px; height: 8px; width: 100%; margin-bottom: 6px; overflow: hidden; }}
        .stDataFrame div {{ background-color: transparent !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_style(img_base64)

# Dessin HTML des barres de progression
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

# 4. CHARGEMENT UNIVERSEL DES DONNÉES
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
        st.error(f"Erreur de connexion Sheets : {e}")
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

# 5. ASSIGNATION DES ONGLETS PRINCIPAUX
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

        # Titre principal
        st.markdown("<h1 style='text-align: center; margin-bottom: 15px;'>🌱 Défi Carbone - Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        with st.expander("🔐 Saisie de nouvelles données", expanded=False):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire Google Forms", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)

        # Les deux fiches du haut
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

            fig = go.Figure(go.Indicator(
                mode = "gauge+number", 
                value = moyenne, 
                domain = {'x': [0.1, 0.9], 'y': [0, 1]},
                number = {
                    'suffix': " kg", 
                    'font': {'color': '#0f172a', 'size': 24}
                }, 
                gauge = {
                    'axis': {'range': [None, 2000], 'tickfont': {'color': '#475569', 'size': 10}}, 
                    'bar': {'color': "#0284c7"}, 
                    'steps': [{'range': [0, 500], 'color': "rgba(34, 197, 94, 0.25)"}, {'range': [500, 1000], 'color': "rgba(249, 115, 22, 0.25)"}, {'range': [1000, 2000], 'color': "rgba(239, 68, 68, 0.25)"}], 
                    'threshold': {'line': {'color': "red", 'width': 3}, 'value': 1000}
                }
            ))
            fig.update_layout(height=210, margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        st.markdown("<h2 style='text-align: center; margin-bottom: 15px;'>🔍 Analyse Comparative des Pôles</h2>", unsafe_allow_html=True)
        
        # Double fiche inférieure analytique
        if not df_active.empty:
            col_mid1, col_mid2 = st.columns([1, 1])
            
            with col_mid1:
                selected_school = st.selectbox("Établissement audité :", df_active[col_etab].unique(), key="left_school_selector")
                st.markdown(f'<p class="inner-title" style="color: #0284c7; text-align: left; margin-top: 5px; margin-bottom: 10px; font-size: 18px; font-weight: bold;">🏫 Établissement Audité : {selected_school}</p>', unsafe_allow_html=True)
                
                school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
                tot_sch = school_data[col_total]
                
                if tot_sch >= 0:
                    sch_energie = safe_get_val(school_data, "Electricité française") + safe_get_val(school_data, "Fioul") + safe_get_val(school_data, "Gaz Naturel")
                    sch_alimentation = safe_get_val(school_data, "Repas moyen") + safe_get_val(school_data, "Repas végétarien") + safe_get_val(school_data, "Repas viande rouge") + safe_get_val(school_data, "Repas viande blanche") + safe_get_val(school_data, "Repas POISSON")
                    sch_transport = safe_get_val(school_data, "Voiture à essence") + safe_get_val(school_data, "Autobus (ville)") + safe_get_val(school_data, "Autobus (sortie scolaire)")
                    
                    b_pap = safe_get_val(school_data, "Paper") if safe_get_val(school_data, "Paper") > 0 else safe_get_val(school_data, "Papier")
                    sch_biens = b_pap + safe_get_val(school_data, "Plastique") + safe_get_val(school_data, "Carton") + safe_get_val(school_data, "Ordinateur à écran plat") + safe_get_val(school_data, "Imprimante") + safe_get_val(school_data, "Photocopieurs") + safe_get_val(school_data, "Vidéo projecteur")
                    sch_dechets = safe_get_val(school_data, "Déchets Papier") + safe_get_val(school_data, "Déchets alimentaire") + safe_get_val(school_data, "Déchets plastique")

                    draw_custom_bar("❄️ Énergie & Bâtiments", sch_energie, tot_sch, "#16a34a")
                    with st.expander("Détails Énergie (cliquez pour ouvrir)"):
                        draw_custom_bar("• Électricité française", safe_get_val(school_data, "Electricité française"), sch_energie, "#22c55e", is_sub=True)
                        draw_custom_bar("• Gaz Naturel", safe_get_val(school_data, "Gaz Naturel"), sch_energie, "#22c55e", is_sub=True)
                        draw_custom_bar("• Fioul de chauffage", safe_get_val(school_data, "Fioul de chauffage"), sch_energie, "#22c55e", is_sub=True)

                    draw_custom_bar("🍎 Alimentation & Cantine", sch_alimentation, tot_sch, "#ea580c")
                    with st.expander("Détails Restauration (cliquez pour ouvrir)"):
                        draw_custom_bar("• Repas Viande Rouge", safe_get_val(school_data, "Repas viande rouge"), sch_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Poisson", safe_get_val(school_data, "Repas POISSON"), sch_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Standard Moyen", safe_get_val(school_data, "Repas moyen"), sch_alimentation, "#f97316", is_sub=True)
                        draw_custom_bar("• Repas Végétarien", safe_get_val(school_data, "Repas végétarien"), sch_alimentation, "#f97316", is_sub=True)

                    draw_custom_bar("🚌 Déplacements & Transports", sch_transport, tot_sch, "#1d4ed8")
                    with st.expander("Détails Transports (cliquez pour ouvrir)"):
                        draw_custom_bar("• Voiture à essence", safe_get_val(school_data, "Voiture à essence"), sch_transport, "#3b82f6", is_sub=True)
                        draw_custom_bar("• Autobus (sorties / voyages)", safe_get_val(school_data, "Autobus (sortie scolaire)"), sch_transport, "#3b82f6", is_sub=True)

                    draw_custom_bar("📦 Biens, Consommables & Équipements", sch_biens, tot_sch, "#7e22ce")
                    draw_custom_bar("🗑️ Gestion des Déchets", sch_dechets, tot_sch, "#4f46e5")

            with col_mid2:
                st.markdown('<p class="inner-title" style="color: #0284c7; text-align: left; margin-bottom: 25px; font-size: 18px; font-weight: bold;">🌍 Global : Secteurs d\'impact du Réseau</p>', unsafe_allow_html=True)
                
                tot_net = df_active[col_total].sum()
                if tot_net >= 0:
                    net_elec = safe_sum_val(df_active, "Electricité française")
                    net_fioul = safe_sum_val(df_active, "Fioul")
                    net_gaz = safe_sum_val(df_active, "Gaz Naturel")
                    net_energie = net_elec + net_fioul + net_gaz

                    net_alimentation = safe_sum_val(df_active, "Repas moyen") + safe_sum_val(df_active, "Repas végétarien") + safe_sum_val(df_active, "Repas viande rouge") + safe_sum_val(df_active, "Repas viande blanche") + safe_sum_val(df_active, "Repas POISSON")
                    net_transport = safe_sum_val(df_active, "Voiture à essence") + safe_sum_val(df_active, "Autobus (ville)") + safe_sum_val(df_active, "Autobus (sortie scolaire)")
                    net_biens = safe_sum_val(df_active, "Paper") + safe_sum_val(df_active, "Papier") + safe_sum_val(df_active, "Plastique") + safe_sum_val(df_active, "Ordinateur à écran plat")
                    net_dechets = safe_sum_val(df_active, "Déchets Papier") + safe_sum_val(df_active, "Déchets alimentaire") + safe_sum_val(df_active, "Déchets plastique")

                    draw_custom_bar("❄️ Énergie & Bâtiments (Total Réseau)", net_energie, tot_net, "#16a34a")
                    draw_custom_bar("🍎 Alimentation & Cantine (Total Réseau)", net_alimentation, tot_net, "#ea580c")
                    draw_custom_bar("🚌 Déplacements & Transports (Total Réseau)", net_transport, tot_net, "#1d4ed8")
                    draw_custom_bar("📦 Biens & Équipements (Total Réseau)", net_biens, tot_net, "#7e22ce")
                    draw_custom_bar("🗑️ Élimination des Déchets (Total Réseau)", net_dechets, tot_net, "#4f46e5")

# ==========================================
# ---    2. ONGLET EMPREINTE CARBONNE    ---
# ==========================================
with tab_conso_graph:
    if not df.empty:
        st.markdown("<h2 style='text-align: center; color: #0f172a; margin-bottom: 20px;'>📊 Comparatif Graphique Interactif du Réseau</h2>", unsafe_allow_html=True)
        
        df_sorted_graph = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=True)
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=df_sorted_graph[col_etab],
            x=df_sorted_graph[col_conso],
            orientation='h',
            marker=dict(color='#0284c7', line=dict(color='rgba(15,23,42,0.2)', width=1)),
            hovertemplate="<b>%{y}</b><br>Empreinte : <b>%{x:.1f} kg CO2e/pers</b><extra></extra>"
        ))
        
        fig_bar.update_layout(
            margin=dict(l=20, r=20, t=10, b=10),
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Consommation Carbone (kg / personne)", color="#0f172a", gridcolor="rgba(0,0,0,0.08)", showgrid=True),
            yaxis=dict(color="#0f172a", tickfont=dict(size=12, weight="bold"))
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        st.markdown('<p class="inner-title" style="color:#0284c7;">📋 Synthèse Globale Centralisée (Données Brutes)</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch", height=250)

# ==========================================
# ---          3. ONGLET GLOSSAIRE       ---
# ==========================================
with tab_glossaire:
    st.markdown("<h2 style='color: #0f172a; text-align: center; margin-bottom: 20px;'>📖 Dictionnaire Carbone : Unités & Équivalents Enfants</h2>", unsafe_allow_html=True)
    
    g_tabs = st.tabs(["🍎 Cantine", "❄️ Énergie", "🚌 Transports"])
    with g_tabs[0]:
        st.subheader("🍎 Référentiel carbone (ADEME)")
        st.markdown('<div class="unit-box">• <b>Viande Rouge :</b> 7.26 kg CO2e | • <b>Poisson :</b> 2.00 kg CO2e | • <b>Végétarien :</b> 0.50 kg CO2e</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 Équivalent élève :</b> 1 repas bœuf = Fabriquer 1 paire de baskets neuve ou scroller sur TikTok pendant 150 heures !</div>', unsafe_allow_html=True)

st.divider()
st.caption("Sources : Base Empreinte ADEME / Contexte Réseau Climat Haut Vaucluse - Juin 2026")
