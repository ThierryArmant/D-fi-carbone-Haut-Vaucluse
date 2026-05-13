# --- STYLE CSS (VERSION BANDEAU DISCRET) ---
def set_bg_and_style():
    st.markdown(
        f"""
        <style>
        /* Fond d'écran */
        .stApp {{
            background-image: url("https://lh3.googleusercontent.com/d/1KA5uUEwfkuW99zl93_ngwq1dJ115zXrK");
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 60%;
            background-color: #f0f2f6;
        }}
        
        /* Conteneur principal */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.9); 
            padding: 1rem 2rem !important; 
            border-radius: 12px;
            margin-top: 10px;
        }}

        /* RÉDUCTION DU BANDEAU "METTRE À JOUR" */
        [data-testid="stExpanderSummary"] {{
            background-color: white !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            min-height: 40px !important; /* Hauteur réduite */
        }}
        
        /* Réduction de la taille du texte dans le bandeau */
        [data-testid="stExpanderSummary"] p {{
            font-size: 14px !important;
            margin-top: 5px !important;
        }}

        /* Fond blanc de l'intérieur quand c'est ouvert */
        [data-testid="stExpanderDetails"] {{
            background-color: white !important;
            padding: 15px !important;
            border: 1px solid #e0e0e0;
            border-top: none;
            border-radius: 0 0 8px 8px !important;
        }}

        [data-testid="stHeader"] {{ height: 0px; }}
        .inner-title {{
            text-align: center; font-weight: bold; font-size: 18px; color: #1e3d59; margin-bottom: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
