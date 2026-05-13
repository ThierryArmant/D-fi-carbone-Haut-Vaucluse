import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", layout="wide")

# 2. STYLE CSS (TON BANDEAU DISCRET INTÉGRÉ)
def set_bg_and_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://lh3.googleusercontent.com/d/1KA5uUEwfkuW99zl93_ngwq1dJ115zXrK");
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            background-size: 60%;
            background-color: #f0f2f6;
        }}
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.9); 
            padding: 1rem 2rem !important; 
            border-radius: 12px;
            margin-top: 10px;
        }}
        [data-testid="stExpanderSummary"] {{
            background-color: white !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            min-height: 40px !important;
        }}
        [data-testid="stExpanderSummary"] p {{
            font-size: 14px !important;
            margin-top: 5px !important;
            color: #1e3d59 !important;
        }}
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

set_bg_and_style()

# 3. VARIABLES DE CONNEXION
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

# 4. CHARGEMENT DES DONNÉES (SÉCURISÉ)
@st.cache_data(ttl=60)
def load_data():
    try:
        raw = pd.read_csv(url, header=None)
        for i, row in raw.iterrows():
            if "Etablissements" in [str(x).strip() for x in row.values]:
                data = raw.iloc[i+1:].copy()
                # Nettoyage des noms de colonnes (doublons/vides)
                new_cols = []
                for j, val in enumerate(row.values):
                    c_name = str(val).strip() if pd.notnull(val) else f"Col_{j}"
                    new_cols.append(c_name)
                data.columns = new_cols
                return data.loc[:, ~data.columns.duplicated()].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
    return pd.DataFrame()

# 5. EXECUTION ET AFFICHAGE
df = load_data()

if not df.empty:
    # Nettoyage rapide des chiffres
    for col in ["Total émissions", "conso carbone  par personne", "Effectif total"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

    st.markdown("<h2 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h2>", unsafe_allow_html=True)

    # Dashboard
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<p class="inner-title">📊 Classement</p>', unsafe_allow_html=True)
        st.dataframe(df[["Etablissements", "conso carbone  par personne"]].sort_values("conso carbone  par personne", ascending=False), hide_index=True, use_container_width=True)
    
    with c2:
        st.markdown('<p class="inner-title">🚀 Moyenne Réseau</p>', unsafe_allow_html=True)
        total_co2 = df["Total émissions"].sum()
        total_pop = df["Effectif total"].sum()
        moyenne = total_co2 / total_pop if total_pop > 0 else 0
        st.metric("Consommation moyenne", f"{int(moyenne)} kg / pers")

    # BANDEAU DE MISE À JOUR (DISCRET)
    st.write("")
    with st.expander("📝 Mettre à jour les données"):
        pwd = st.text_input("Code établissement :", type="password")
        if pwd == "CARBONE2026":
            st.link_button("🚀 Ouvrir le formulaire de saisie", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)

    # Tableau détaillé
    st.write("### 📋 Détails complets")
    st.dataframe(df, hide_index=True, use_container_width=True)

else:
    st.warning("⚠️ Impossible de charger les données. Vérifiez que le partage du Google Sheets est activé sur 'Tous les utilisateurs disposant du lien'.")
