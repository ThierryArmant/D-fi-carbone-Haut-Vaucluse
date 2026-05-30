# 2. STYLE CSS (Mode Sombre / Reposant avec BOUTONS d'onglets)
def set_style():
    st.markdown(
        """
        <style>
        /* Fond global de l'application */
        .stApp { background-color: #0f172a; color: #f1f5f9; }
        
        /* Conteneur principal */
        .main .block-container {
            background-color: #1e293b;
            padding: 2rem 3rem !important;
            border-radius: 8px;
        }
        
        /* --- STYLE DES ONGLETS EN BOUTONS --- */
        /* On cible la liste des onglets */
        div[data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
            margin-bottom: 20px;
        }
        
        /* Le bouton d'onglet lui-même */
        div[data-baseweb="tab"] {
            background-color: #334155; /* Fond gris inactif */
            border-radius: 12px;
            padding: 12px 20px !important;
            color: #cbd5e1 !important;
            border: 1px solid #475569;
            transition: all 0.3s ease;
            height: auto;
        }
        
        /* Effet de survol (hover) */
        div[data-baseweb="tab"]:hover {
            background-color: #475569;
            border-color: #38bdf8;
            color: white !important;
        }
        
        /* L'onglet SÉLECTIONNÉ (Actif) */
        div[data-baseweb="tab"][aria-selected="true"] {
            background-color: #38bdf8 !important; /* Bleu vif */
            color: #0f172a !important; /* Texte sombre pour contraste */
            border-color: #38bdf8 !important;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
        }
        
        /* Supprimer la ligne rouge par défaut de Streamlit */
        div[role="tabpanel"] { border: none; }
        div[data-baseweb="tab-border"] { display: none; }
        
        /* Autres styles habituels */
        .inner-title { text-align: center; font-weight: bold; font-size: 20px; color: #38bdf8; margin-bottom: 15px; }
        .anecdote { background-color: #1e3a8a; padding: 15px; border-left: 5px solid #3b82f6; border-radius: 5px; margin: 10px 0; color: #eff6ff; }
        .methode { background-color: #14532d; padding: 10px; border-left: 5px solid #22c55e; border-radius: 5px; font-size: 0.9em; margin-top: 10px; color: #f0fdf4; }
        
        .pole-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1em; color: #f1f5f9; }
        .bar-container { background-color: #475569; border-radius: 6px; height: 16px; width: 100%; margin-bottom: 15px; overflow: hidden; }
        </style>
        """,
        unsafe_allow_html=True
    )

Tes onglets vont maintenant vraiment "ressortir" comme des boutons d'interface moderne. Dis-moi si le bleu te convient ou si tu préfères une autre nuance !
