import streamlit as st

# Configuration de base pour le mode plein écran
st.set_page_config(page_title="Projet ODD Cantine", layout="wide")

# Injection du HTML/CSS propre (sans caractères invisibles)
st.markdown("""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hub ODD Cantine</title>
    <style>
        :root { --am-blue: #002060; }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            margin: 0; padding: 0;
            background: linear-gradient(180deg, #dae2ed 0%, #f0f4f8 100%);
            height: 100vh; display: flex; flex-direction: column; overflow: hidden;
        }
        header {
            background-color: var(--am-blue); color: white;
            padding: 0.5rem 1.5rem; display: flex; align-items: center;
            justify-content: space-between; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 10;
        }
        .logo-box { height: 60px; background: white; padding: 5px; border-radius: 4px; }
        .titles { text-align: center; flex-grow: 1; }
        h1 { margin: 0; font-size: 1.4rem; }
        .subtitle { opacity: 0.9; margin: 0; font-size: 0.8rem; }
        .hub-container {
            display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;
            max-width: 1500px; margin: 1rem auto; padding: 0 1rem; flex: 1; width: 96%;
        }
        .bot-card {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(8px);
            border-radius: 16px; display: flex; flex-direction: column;
            border: 1px solid rgba(255,255,255,0.8); box-shadow: 0 8px 32px rgba(0,32,96,0.08);
            overflow: hidden;
        }
        .bot-header {
            padding: 0.8rem; text-align: center; background: rgba(0, 32, 96, 0.05);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1); font-weight: bold; color: var(--am-blue);
        }
        .chat-section { flex: 1; background: white; padding: 20px; overflow-y: auto; }
        iframe { width: 100%; height: 100%; border: none; }
        footer { text-align: center; padding: 0.5rem; font-size: 0.75rem; color: #5d6d7e; }
    </style>
</head>
<body>
    <header>
        <div class="logo-box">♻️</div>
        <div class="titles">
            <h1>Objectif Zéro Gâchis - Collège</h1>
            <p class="subtitle">Analyse et Suivi des Déchets (ODD 12)</p>
        </div>
        <div class="logo-box">🏫</div>
    </header>

    <div class="hub-container">
        <div class="bot-card">
            <div class="bot-header">📊 Saisie des Données</div>
            <div class="chat-section">
                <p>Bienvenue sur l'outil de suivi de la cantine.</p>
                <p>Ici, nous quantifierons le pain, les fruits et les déchets triés.</p>
            </div>
        </div>
        <div class="bot-card">
            <div class="bot-header">📈 Visualisation</div>
            <div class="chat-section">
                <p>Les graphiques d'impact carbone seront affichés ici.</p>
            </div>
        </div>
    </div>

    <footer>
        &copy; 2026 - Projet Éco-Collège Vaucluse
    </footer>
</body>
</html>
""", unsafe_allow_html=True)
