import streamlit as st

# Configuration de la page Streamlit pour occuper tout l'écran
st.set_page_config(
    page_title="Eco-Cantine 700 - ODD",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injection du code HTML adapté au projet éco-collège
st.markdown(
    """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Éco-Cantine - Collège du Vaucluse</title>
        <style>
            :root { 
                --dd-green: #27ae60; 
                --dd-blue: #2980b9;
            }
            body {
                font-family: 'Segoe UI', Tahoma, sans-serif;
                margin: 0; padding: 0;
                background: linear-gradient(180deg, #e8f5e9 0%, #f0f4f8 100%);
                height: 100vh; display: flex; flex-direction: column; overflow: hidden;
            }
            header {
                background-color: var(--dd-green); color: white;
                padding: 0.5rem 1.5rem; display: flex; align-items: center;
                justify-content: space-between; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 10;
            }
            .logo-odd { height: 60px; background: white; padding: 5px; border-radius: 4px; }
            .logo-college { height: 60px; border-radius: 50%; border: 2px solid white; background: white; }
            .titles { text-align: center; flex-grow: 1; }
            h1 { margin: 0; font-size: 1.4rem; }
            .subtitle { opacity: 0.9; margin: 0; font-size: 0.8rem; }
            
            .hub-container {
                display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;
                max-width: 1500px; margin: 1rem auto; padding: 0 1rem; flex: 1; width: 96%;
                overflow: hidden;
            }
            .bot-card {
                background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(8px);
                border-radius: 16px; display: flex; flex-direction: column;
                border: 1px solid rgba(255,255,255,0.8); box-shadow: 0 8px 32px rgba(39,174,96,0.08);
                overflow: hidden;
            }
            .bot-header {
                padding: 0.8rem; text-align: center; background: rgba(39, 174, 96, 0.1);
                border-bottom: 1px solid rgba(0, 0, 0, 0.1); font-weight: bold; color: var(--dd-green);
            }
            .content-section { flex: 1; background: white; padding: 1.5rem; overflow-y: auto; }
            
            /* Styles pour les listes et badges de tri */
            .tri-item { display: flex; justify-content: space-between; padding: 10px; margin-bottom: 8px; border-radius: 8px; background: #f8f9fa; border-left: 5px solid var(--dd-green); }
            .tri-pain { border-left-color: #f39c12; }
            .tri-fruits { border-left-color: #e74c3c; }
            .tri-emballage { border-left-color: #3498db; }
            
            /* Masquer les éléments natifs de Streamlit superflus */
            #MainMenu, viewerBadge, footer, header { visibility: hidden; display: none !important; }
            .stApp { background: transparent; }
            
            @media (max-width: 1000px) {
                .hub-container { grid-template-columns: 1fr; overflow-y: auto; }
                .bot-card { height: auto; min-height: 400px; }
                body { overflow-y: auto; }
            }
        </style>
    </head>
    <body>

        <header>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 2rem;">♻️</span>
                <div style="font-size: 0.8rem; font-weight: bold; line-height: 1;">ODD 12<br>PRODUCTION<br>RESPONSABLE</div>
            </div>
            
            <div class="titles">
                <h1>Objectif Zéro Gâchis - Cantine du Vaucluse</h1>
                <p class="subtitle">Analyse et quantification pour nos 700 demi-pensionnaires</p>
            </div>
            
            <span style="font-size: 2rem;">🏫</span>
        </header>

        <div class="hub-container">
            <div class="bot-card">
                <div class="bot-header">🗑️ Suivi de nos 5 Bornes de Tri</div>
                <div class="content-section">
                    <p>Chaque jour, nous mesurons le gaspillage généré par les 700 élèves sur nos 5 catégories :</p>
                    
                    <div class="tri-item">
                        <span>🍲 <strong>Déchets Alimentaires</strong> (Restes d'assiettes)</span>
                        <strong>En cours...</strong>
                    </div>
                    <div class="tri-item tri-pain">
                        <span>🥖 <strong>Le Pain</strong> (Gâchis pain entier/entamé)</span>
                        <strong>En cours...</strong>
                    </div>
                    <div class="tri-item tri-fruits">
                        <span>🍏 <strong>Fruits Entamés</strong> (Non terminés)</span>
                        <strong>En cours...</strong>
                    </div>
                    <div class="tri-item tri-emballage">
                        <span>🧃 <strong>Emballages Plastiques/Cartons</strong></span>
                        <strong>En cours...</strong>
                    </div>
                    <div class="tri-item" style="border-left-color: #7f8c8d;">
                        <span>🧻 <strong>Serviettes en Papier</strong></span>
                        <strong>En cours...</strong>
                    </div>
                </div>
            </div>

            <div class="bot-card">
                <div class="bot-header">📊 Analyse de l'Impact & ODD 12</div>
                <div class="content-section" style="text-align: center;">
                    <h3>Objectif de Développement Durable n°12</h3>
                    <p style="text-align: left; color: #555;">
                        D'ici 2030, l'ONU a pour objectif de réduire de moitié le gaspillage alimentaire mondial par habitant. 
                        Au collège, cela commence dans notre assiette !
                    </p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 1.5rem 0;">
                    
                    <h4>Visualisation des données</h4>
                    <p style="color: #7f8c8d; font-style: italic; margin-top: 2rem;">
                        [ Les graphiques de nos premières pesées apparaîtront ici dès que les données de la semaine seront collectées ]
                    </p>
                </div>
            </div>
        </div>

        <footer style="text-align: center; padding: 0.5rem; font-size: 0.75rem; color: #5d6d7e;">
            &copy; 2026 - Projet Éco-Délégués - Collège du Vaucluse
        </footer>

    </body>
    </html>
    """,
    unsafe_allow_html=True
)
