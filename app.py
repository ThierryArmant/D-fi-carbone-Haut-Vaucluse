# Injection du filtre Gloss/Glassmorphism Universel
def inject_glass_theme(img_b64):
    st.markdown(
        f"""
        <style>
        /* 1. Application du fond d'écran global */
        [data-testid="stAppViewContainer"], .stAppViewContainer {{
            background-image: url("data:image/jpeg;base64,{img_b64}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
        }}

        /* 2. Neutralisation complète des masques Streamlit par défaut */
        .stApp, [data-testid="stMain"], .main, [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockContainer"] {{
            background-color: transparent !important;
        }}
        
        .main .block-container {{
            background-color: transparent !important;
            padding: 1rem 2rem !important;
        }}

        /* 3. 💎 LE BOUCLIER GLOSSY "BLEU ARDOISE" (Appliqué partout sur les 3 pages) */
        div[data-testid="stColumn"], 
        div[data-testid="stBorderedContainer"],
        div[data-testid="stExpander"], 
        .stExpander,
        div[data-testid="stDataFrame"],
        .stTabs {{
            background-color: rgba(22, 32, 53, 0.78) !important; /* Teinte ardoise dense pour isoler les écritures */
            backdrop-filter: blur(22px) saturate(140%) !important; /* Puissant effet de texture givrée */
            -webkit-backdrop-filter: blur(22px) saturate(140%) !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important; /* Liseré cristal léger */
            padding: 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
            margin-bottom: 14px !important;
        }}

        /* Ajustement spécifique pour les expanders imbriqués (taille normale d'origine) */
        div[data-testid="stExpander"] {{
            padding: 6px 12px !important;
            background-color: rgba(15, 23, 42, 0.4) !important;
            box-shadow: none !important;
        }}

        /* 4. 🛡️ SÉCURISATION INTÉGRALE DES TEXTES (Contraste maximal Blanc Pur) */
        h1, h2, h3, h4, h5, h6, label, p, .stMarkdown p, [data-testid="stWidgetLabel"] p, .pole-header, .sub-pole-header, summary {{
            color: #ffffff !important;
            font-weight: bold !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.6) !important; /* Ombre portée pour décoller le texte du fond */
        }}
        
        .inner-title {{ text-align: center; font-weight: bold; font-size: 16px; color: #38bdf8 !important; margin-bottom: 12px; }}

        /* 5. PROTECTION DES ÉLÉMENTS INTERACTIFS NATIFS */
        /* Forcer les flèches des expanders à rester blanches et visibles */
        [data-testid="stExpander"] svg {{
            fill: #ffffff !important;
            color: #ffffff !important;
        }}

        /* Menu des onglets (tabs) harmonisé en mode cockpit pro */
        div[data-baseweb="tab-list"] button {{
            background-color: rgba(30, 41, 59, 0.85) !important;
            color: #cbd5e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px 8px 0 0 !important;
        }}
        div[data-baseweb="tab-list"] button[aria-selected="true"] {{
            background-color: #22d3ee !important;
            color: #0f172a !important;
        }}

        /* Fond des graphiques transparent pour fusionner parfaitement avec le filtre ardoise */
        .js-plotly-plot .plotly .main-svg {{
            background: transparent !important;
        }}
        
        /* Rendre transparent le fond des tableaux de données natifs */
        .stDataFrame div {{ background-color: transparent !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Appel de la fonction de style juste après avoir récupéré ton image
inject_glass_theme(img_base64)
