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

# 2. STYLE CSS (Gris Crystal Opaque Universel - Protection maximale)
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
        background: linear-gradient(135deg, #090d16 0%, #0f172a 100%);
    }}
    """
    
    st.markdown(
        f"""
        <style>
        {bg_style}
        
        /* Force la transparence des rideaux natifs de Streamlit */
        .stApp, [data-testid="stMain"], .main {{
            background-color: transparent !important;
        }}
        
        /* Conteneur général de la zone centrale */
        .main .block-container {{
            background-color: rgba(9, 13, 22, 0.4) !important; /* Sombre légèrement le fond pour faire ressortir les blocs */
            border-radius: 16px;
            padding: 1rem 2rem !important;
            color: #f1f5f9;
        }}
        
        /* --- 🛡️ CHARTE DE PROTECTION TOTAL : FONDS DES TABLEAUX ET ZONE DE TEXTES --- */
        div[data-testid="stBorderedContainer"], .stExpander {{
            background-color: rgba(15, 23, 42, 0.95) !important; /* Fond Gris Sombre opaque à 95% pour bloquer l'image */
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important; /* Liseré Crystal */
            padding: 16px 20px !important;
            border-radius: 14px !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important;
            margin-bottom: 12px !important;
        }}
        
        /* Personnalisation des liserés spécifiques */
        div[data-testid="stBorderedContainer"]:has(.card-mid-left) {{
            border-left: 4px solid #22d3ee !important; /* Ligne turquoise signature */
        }}
        div[data-testid="stBorderedContainer"]:has(.card-mid-right) {{
            border-left: 4px solid #475569 !important; /* Ligne acier signature */
        }}
        
        /* --- 🎛️ STYLE DES ONGLETS PRINCIPAUX --- */
        div[data-baseweb="tab-list"] {{
            gap: 12px !important;
            background-color: transparent !important;
            margin-bottom: 16px !important;
        }}
        div[data-baseweb="tab"], button[data-baseweb="tab"] {{
            background-color: rgba(15, 23, 42, 0.95) !important;
            border-radius: 8px !important;
            padding: 10px 22px !important;
            color: #cbd5e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: all 0.2s ease !important;
            font-weight: bold !important;
            font-size: 14px !important;
        }}
        div[data-baseweb="tab"]:hover, button[data-baseweb="tab"]:hover {{
            background-color: rgba(30, 41, 59, 1) !important;
            border-color: #22d3ee !important;
            color: #ffffff !important;
        }}
        div[data-baseweb="tab"][aria-selected="true"], button[data-baseweb="tab"][aria-selected="true"] {{
            background-color: #22d3ee !important;
            color: #0f172a !important; 
            border-color: #22d3ee !important;
            box-shadow: 0 4px 14px rgba(34, 211, 238, 0.5) !important;
        }}
        [data-baseweb="tab-border"] {{ display: none !important; }}
        div[role="tabpanel"] {{ border: none !important; }}
        
        /* Libellés de widgets */
        [data-testid="stWidgetLabel"] p {{ color: #e2e8f0 !important; font-weight: 600; font-size: 14px; }}
        .inner-title {{ text-align: center; font-weight: bold; font-size: 16px; color: #38bdf8; margin-bottom: 8px; }}
        
        [data-testid="stHeader"] {{ height: 0px; }}
        
        /* Éléments internes */
        .anecdote {{ background-color: rgba(30, 58, 138, 0.9); padding: 12px 14px; border-left: 4px solid #3b82f6; border-radius: 4px; color: #eff6ff; font-size: 13px; }}
        .unit-box {{ background-color: rgba(9, 13, 22, 0.9); padding: 10px; border-radius: 6px; border: 1px dashed #475569; font-size: 13px; }}
        
        .pole-header {{ display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; margin-bottom: 4px; margin-top: 4px; color: #f1f5f9; }}
        .sub-pole-header {{ display: flex; justify-content: space-between; font-size: 12px; color: #cbd5e1; margin-bottom: 2px; margin-top: 4px; }}
        .bar-container {{ background-color: #475569; border-radius: 4px; height: 12px; width: 100%; margin-bottom: 8px; overflow: hidden; }}
        .sub-bar-container {{ background-color: #334155; border-radius: 3px; height: 8px; width: 100%; margin-bottom: 6px; overflow: hidden; }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_style(img_base64)

# Alerte si problème de fichier
if not img_base64:
    st.error("⚠️ Fichier 'image_1' non détecté à la racine de ton projet.")

# Fonction de rendu des barres
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

# Connexion Sheets
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

# Onglets principaux
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

        # 💎 SHIELD DE COULEUR POUR LE TITRE PRINCIPAL
        st.markdown(
            """
            <div style="background-color: rgba(15, 23, 42, 0.95); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin-bottom: 15px;">
                <h1 style='text-align: center; color: #22d3ee; margin: 0; font-size: 26px; font-weight: bold;'>🌱 Défi Carbone - Réseau Haut Vaucluse</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        with st.expander("🔐 Saisie de nouvelles données", expanded=False):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire Google Forms", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)

        # Blocs du haut sous coques protectrices
        col_top1, col_top2 = st.columns([1, 1])
        with col_top1:
            with st.container(border=True):
                st.markdown('<p class="inner-title">📊 Classement des Établissements (kg/personne)</p>', unsafe_allow_html=True)
                if not df_active.empty:
                    df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                    st.dataframe(df_ranking, hide_index=True, width="stretch", height=210)
                else:
                    st.info("En attente de données...")
                
        with col_top2:
            with st.container(border=True):
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
                        'font': {'color': '#f1f5f9', 'size': 24}
                    }, 
                    gauge = {
                        'axis': {'range': [None, 2000], 'tickfont': {'color': '#f1f5f9', 'size': 10}}, 
                        'bar': {'color': "#22d3ee"}, 
                        'steps': [{'range': [0, 500], 'color': "#1e3a8a"}, {'range': [500, 1000], 'color': "#b45309"}, {'range': [1000, 2000], 'color': "#991b1b"}], 
                        'threshold': {'line': {'color': "red", 'width': 3}, 'value': 1000}
                    }
                ))
                fig.update_layout(height=210, margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # 💎 SHIELD DE COULEUR POUR LE TITRE DES PÔLES
        st.markdown(
            """
            <div style="background-color: rgba(15, 23, 42, 0.95); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin-bottom: 15px;">
                <h2 style='text-align: center; color: #22d3ee; margin: 0; font-size: 20px; font-weight: bold;'>🔍 Analyse Comparative des Pôles</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if not df_active.empty:
            col_mid1, col_mid2 = st.columns([1, 1])
            
            with col_mid1:
                with st.container(border=True):
                    st.markdown('<div class="card-mid-left"></div>', unsafe_allow_html=True)
                    selected_school = st.selectbox("Établissement audité :", df_active[col_etab].unique(), key="left_school_selector")
                    st.markdown(f'<p class="inner-title" style="color: #22d3ee; text-align: left; margin-top: 5px; margin-bottom: 10px; font-size: 18px; font-weight: bold;">🏫 Établissement Audité : {selected_school}</p>', unsafe_allow_html=True)
                    
                    school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
                    tot_sch = school_data[col_total]
                    
                    if tot_sch >= 0:
                        sch_energie = safe_get_val(school_data, "Electricité française") + safe_get_val(school_data, "Fioul") + safe_get_val(school_data, "Gaz Naturel")
                        sch_alimentation = safe_get_val(school_data, "Repas moyen") + safe_get_val(school_data, "Repas végétarien") + safe_get_val(school_data, "Repas viande rouge") + safe_get_val(school_data, "Repas viande blanche") + safe_get_val(school_data, "Repas POISSON")
                        sch_transport = safe_get_val(school_data, "Voiture à essence") + safe_get_val(school_data, "Autobus (ville)") + safe_get_val(school_data, "Autobus (sortie scolaire)")
                        
                        b_pap = safe_get_val(school_data, "Paper") if safe_get_val(school_data, "Paper") > 0 else safe_get_val(school_data, "Papier")
                        sch_biens = b_pap + safe_get_val(school_data, "Plastique") + safe_get_val(school_data, "Carton") + safe_get_val(school_data, "Ordinateur à écran plat") + safe_get_val(school_data, "Imprimante") + safe_get_val(school_data, "Photocopieurs") + safe_get_val(school_data, "Vidéo projecteur")
                        sch_dechets = safe_get_val(school_data, "Déchets Papier") + safe_get_val(school_data, "Déchets alimentaire") + safe_get_val(school_data, "Déchets plastique")

                        draw_custom_bar("❄️ Énergie & Bâtiments", sch_energie, tot_sch, "#4ade80")
                        with st.expander("Détails Énergie (cliquez pour ouvrir)"):
                            draw_custom_bar("• Électricité française", safe_get_val(school_data, "Electricité française"), sch_energie, "#22c55e", is_sub=True)
                            draw_custom_bar("• Gaz Naturel", safe_get_val(school_data, "Gaz Naturel"), sch_energie, "#22c55e", is_sub=True)
                            draw_custom_bar("• Fioul de chauffage", safe_get_val(school_data, "Fioul de chauffage"), sch_energie, "#22c55e", is_sub=True)

                        draw_custom_bar("🍎 Alimentation & Cantine", sch_alimentation, tot_sch, "#fb923c")
                        with st.expander("Détails Restauration (cliquez pour ouvrir)"):
                            draw_custom_bar("• Repas Viande Rouge", safe_get_val(school_data, "Repas viande rouge"), sch_alimentation, "#f97316", is_sub=True)
                            draw_custom_bar("• Repas Poisson", safe_get_val(school_data, "Repas POISSON"), sch_alimentation, "#f97316", is_sub=True)
                            draw_custom_bar("• Repas Standard", safe_get_val(school_data, "Repas moyen"), sch_alimentation, "#f97316", is_sub=True)
                            draw_custom_bar("• Repas Végétarien", safe_get_val(school_data, "Repas végétarien"), sch_alimentation, "#f97316", is_sub=True)

                        draw_custom_bar("🚌 Déplacements & Transports", sch_transport, tot_sch, "#60a5fa")
                        with st.expander("Détails Transports (cliquez pour ouvrir)"):
                            draw_custom_bar("• Voiture", safe_get_val(school_data, "Voiture à essence"), sch_transport, "#3b82f6", is_sub=True)
                            draw_custom_bar("• Bus (voyages / sorties)", safe_get_val(school_data, "Autobus (sortie scolaire)"), sch_transport, "#3b82f6", is_sub=True)

                        draw_custom_bar("📦 Biens, Consommables & Équipements", sch_biens, tot_sch, "#c084fc")
                        draw_custom_bar("🗑️ Gestion des Déchets", sch_dechets, tot_sch, "#818cf8")

            with col_mid2:
                with st.container(border=True):
                    st.markdown('<div class="card-mid-right"></div>', unsafe_allow_html=True)
                    st.markdown('<p class="inner-title" style="color: #cbd5e1; text-align: left; margin-bottom: 45px; font-size: 18px; font-weight: bold;">🌍 Global : Secteurs d\'impact du Réseau</p>', unsafe_allow_html=True)
                    
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

                        draw_custom_bar("❄️ Énergie & Bâtiments (Total Réseau)", net_energie, tot_net, "#4ade80")
                        draw_custom_bar("🍎 Alimentation & Cantine (Total Réseau)", net_alimentation, tot_net, "#fb923c")
                        draw_custom_bar("🚌 Déplacements & Transports (Total Réseau)", net_transport, tot_net, "#60a5fa")
                        draw_custom_bar("📦 Biens & Équipements (Total Réseau)", net_biens, tot_net, "#c084fc")
                        draw_custom_bar("🗑️ Élimination des Déchets (Total Réseau)", net_dechets, tot_net, "#818cf8")

# ==========================================
# ---    2. ONGLET EMPREINTE CARBONNE    ---
# ==========================================
with tab_conso_graph:
    if not df.empty:
        st.markdown(
            """
            <div style="background-color: rgba(15, 23, 42, 0.95); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin-bottom: 15px;">
                <h2 style='text-align: center; color: #22d3ee; margin: 0; font-size: 20px; font-weight: bold;'>📊 Comparatif Graphique Interactif du Réseau</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        with st.container(border=True):
            df_sorted_graph = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=True)
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                y=df_sorted_graph[col_etab],
                x=df_sorted_graph[col_conso],
                orientation='h',
                marker=dict(color='#22d3ee', line=dict(color='rgba(0,0,0,0.5)', width=1)),
                hovertemplate="<b>%{y}</b><br>Empreinte : <b>%{x:.1f} kg CO2e/pers</b><extra></extra>"
            ))
            
            fig_bar.update_layout(
                margin=dict(l=20, r=20, t=10, b=10),
                height=450,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title="Consommation Carbone (kg / personne)", color="#cbd5e1", gridcolor="rgba(255,255,255,0.1)", showgrid=True),
                yaxis=dict(color="#f1f5f9", tickfont=dict(size=12))
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        with st.container(border=True):
            st.markdown('<p class="inner-title">📋 Synthèse Globale Centralisée (Données Brutes)</p>', unsafe_allow_html=True)
            st.dataframe(df, hide_index=True, width="stretch", height=250)

# ==========================================
# ---          3. ONGLET GLOSSAIRE       ---
# ==========================================
with tab_glossaire:
    st.markdown(
        """
        <div style="background-color: rgba(15, 23, 42, 0.95); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin-bottom: 15px;">
            <h2 style='color: #22d3ee; text-align: center; margin: 0; font-size: 20px; font-weight: bold;'>📖 Dictionnaire Carbone : Unités & Équivalents Enfants</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    with st.container(border=True):
        g_tabs = st.tabs(["🍎 Cantine", "❄️ Énergie", "🚌 Transports"])
        
        with g_tabs[0]:
            st.subheader("🍎 Référentiel carbone (ADEME)")
            st.markdown('<div class="unit-box">• <b>Viande Rouge :</b> 7.26 kg CO2e | • <b>Poisson :</b> 2.00 kg CO2e | • <b>Végétarien :</b> 0.50 kg CO2e</div>', unsafe_allow_html=True)
            st.markdown('<div class="anecdote"><b>💡 Équivalent élève :</b> 1 repas bœuf = Fabriquer 1 paire de baskets neuve ou scroller sur TikTok pendant 150 heures !</div>', unsafe_allow_html=True)

st.divider()
st.caption("Sources : Base Empreinte ADEME / Contexte Réseau Climat Haut Vaucluse - Juin 2026")
