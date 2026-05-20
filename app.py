import streamlit as st

# 1. Configuration de la page en mode plein écran
st.set_page_config(page_title="Hub Défi Carbone", layout="wide")

# 2. Création des onglets (Tout le monde voit les onglets)
onglet_public, onglet_prive = st.tabs(["📊 Résultats & ODD 12 (Public)", "🔒 Saisie des Pesées (Sécurisé)"])

# ==========================================
# PARTIE 1 : ONGLET PUBLIC (Visible par tous)
# ==========================================
with onglet_public:
    st.markdown("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <style>
            :root { --am-blue: #002060; }
            body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; }
            header {
                background-color: var(--am-blue); color: white;
                padding: 0.5rem 1.5rem; display: flex; align-items: center;
                justify-content: space-between; box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }
            .logo-box { height: 60px; background: white; padding: 5px; border-radius: 4px; display:flex; align-items:center; justify-content:center; font-size:1.5rem; }
            .titles { text-align: center; flex-grow: 1; }
            h1 { margin: 0; font-size: 1.4rem; }
            .subtitle { opacity: 0.9; margin: 0; font-size: 0.8rem; }
            .hub-container-public {
                max-width: 1500px; margin: 1rem auto; padding: 0 1rem; height: 75vh;
            }
            .bot-card {
                background: white; border-radius: 16px; display: flex; flex-direction: column;
                border: 1px solid rgba(0,0,0,0.1); box-shadow: 0 8px 32px rgba(0,32,96,0.08);
                height: 100%; overflow: hidden;
            }
            .bot-header {
                padding: 0.8rem; text-align: center; background: rgba(0, 32, 96, 0.05);
                border-bottom: 1px solid rgba(0, 0, 0, 0.1); font-weight: bold; color: var(--am-blue);
            }
            .chat-section { flex: 1; background: white; }
            iframe { width: 100%; height: 100%; border: none; }
        </style>
    </head>
    <body>
        <header>
            <div class="logo-box">♻️</div>
            <div class="titles">
                <h1>Hub - Défi Carbone Cantine</h1>
                <p class="subtitle">Résultats publics de nos pesées (ODD 12)</p>
            </div>
            <div class="logo-box">🏫</div>
        </header>

        <div class="hub-container-public">
            <div class="bot-card">
                <div class="bot-header">📈 Tableau Général de Suivi des Déchets</div>
                <div class="chat-section">
                    <iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vSCa-ml7NJO07Wb09U6ULv4HmHzzKABue1XVeZ7rkW-13vQKm_EjwblGiumu9N1A8X5G2HfpJUX-VPU/pubhtml?gid=717694895&amp;single=true"></iframe>
                </div>
            </div>
        </div>
    </body>
    </html>
    """, unsafe_allow_html=True)

# ==========================================
# PARTIE 2 : ONGLET PRIVÉ (Bloqué par mot de passe)
# ==========================================
with onglet_prive:
    st.subheader("🔑 Espace Administration de la Cantine")
    
    # Zone de saisie du mot de passe
    code_saisie = st.text_input("Entrez le code pour accéder au formulaire d'enregistrement :", type="password")
    
    if code_saisie == "CARBONE2026":
        st.success("Accès autorisé au panneau de configuration.")
        
        # Le contenu secret s'affiche UNIQUEMENT si le mot de passe est bon
        st.markdown("""
        <div style="background-color: #f4f9f4; padding: 20px; border-radius: 10px; border-left: 5px solid #27ae60;">
            <h3>📝 Formulaire d'enregistrement des pesées</h3>
            <p>Cet espace est réservé au personnel de cantine et aux éco-délégués autorisés pour inscrire les données quotidiennes.</p>
            <p><i>[Ici, nous intégrerons la méthode pour ajouter des lignes dans la base de données]</i></p>
        </div>
        """, unsafe_allow_html=True)
        
    elif code_saisie != "":
        st.error("Code incorrect. Seul le personnel autorisé peut accéder à la saisie.")
