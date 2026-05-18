import streamlit as st

st.markdown(
    """
<header>
    <img src="logo%20AM.png" alt="Logo" class="logo-academie">
    <div class="titles">
        <h1>Hub IA - EPS Aix-Marseille</h1>
        <p class="subtitle">Espace Ressources & Assistance</p>
    </div>
    <img src="capture_decran_2025-09-08_191648.png" alt="Logo EPS" class="logo-eps">
</header>

<div class="hub-container">
    <div class="bot-card">
        <div class="bot-header">🤖 Assistant Expert iPack EPS</div>
        <div class="chat-section">
            <iframe src="https://www.chatbase.co/chatbot-iframe/lkAOJJxel7o6BllVD3_Xo"></iframe>
        </div>
    </div>

    <div class="bot-card">
        <div class="bot-header">🔍 Recherche Ressources & Site EPS</div>
        <div class="chat-section">
            <iframe src="https://www.chatbase.co/chatbot-iframe/zbzrnrmae7vcb06n24uhvddky9tfix71"></iframe>
        </div>
    </div>
</div>

<footer>
    &copy; 2026 - Académie d'Aix-Marseille
</footer>
    """,
    unsafe_allow_html=True
)
