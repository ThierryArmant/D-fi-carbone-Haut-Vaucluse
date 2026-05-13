import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", layout="wide")

# 2. STYLE CSS (BANDEAU DISCRET + FOND BLANC OPAQUE)
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
        /* Style du bandeau de mise à jour réduit */
        [data-testid="stExpanderSummary"] {{
            background-color: white !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            min-height: 40px !important;
            padding: 0px 10px !important;
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

# 4. CHARGEMENT DES DONNÉES
@st.cache_data(ttl=60)
def load_data():
    try:
        raw = pd.read_csv(url, header=None)
        for i, row in raw.iterrows():
            row_str = [str(x).strip() for x in row.values]
            if "Etablissements" in row_str:
                data = raw.iloc[i+1:].copy()
                new_cols = []
                for j, val in enumerate(row.values):
                    c_name = str(val).strip() if pd.notnull(val) else f"Col_{j}"
                    new_cols.append(c_name)
                data.columns = new_cols
                return data.loc[:, ~data.columns.duplicated()].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
    return pd.DataFrame()

# 5. EXECUTION
df = load_data()

if not df.empty:
    # Nettoyage des colonnes numériques
    cols_to_fix = ["Total émissions", "conso carbone  par personne", "Effectif total"]
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

    st.markdown("<h2 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h2>", unsafe_allow_html=True)

    # --- LIGNE 1 : CLASSEMENT ET RETOUR DE LA JAUGE ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<p class="inner-title">📊 Classement (kg/pers)</p>', unsafe_allow_html=True)
        if "Etablissements" in df.columns:
            st.dataframe(df[["Etablissements", "conso carbone  par personne"]].sort_values("conso carbone  par personne", ascending=False), hide_index=True, use_container_width=True, height=350)
    
    with col2:
        st.markdown('<p class="inner-title">🚀 Moyenne Réelle du Réseau</p>', unsafe_allow_html=True)
        total_co2 = df["Total émissions"].sum()
        total_pop = df["Effectif total"].sum()
        moyenne = total_co2 / total_pop if total_pop > 0 else 0
        
        # LA JAUGE PLOTLY REVIENT ICI
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = moyenne,
            number = {'suffix': " kg", 'font': {'size': 35}},
            gauge = {
                'axis': {'range': [None, 5000]},
                'bar': {'color': "#1e3d59"},
                'steps': [
                    {'range': [0, 1500], 'color': "#2ecc71"},
                    {'range': [1500, 2500], 'color': "#fbc02d"},
                    {'range': [2500, 5000], 'color': "#ff8a80"}
                ],
                'threshold': {'line': {'color': "red", 'width': 5}, 'value': 2500}
            }
        ))
        fig.update_layout(height=350, margin=dict(t=20, b=0, l=30, r=30))
        st.plotly_chart(fig, use_container_width=True)

    # --- LIGNE 2 : BANDEAU MISE À JOUR ---
    with st.expander("📝 Mettre à jour les données"):
        c_p1, c_p2 = st.columns([1, 1])
        with c_p1:
            pwd = st.text_input("Code établissement :", type="password", key="pwd_input")
        with c_p2:
            st.write("Accès au formulaire de saisie pour l'année en cours.")
            
        if pwd == "CARBONE2026":
            st.success("Code valide")
            st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)

    # --- LIGNE 3 : TABLEAU DÉTAILLÉ ---
    st.markdown("<p style='font-weight: bold; color: #1e3d59;'>📋 Détails complets</p>", unsafe_allow_html=True)
    st.dataframe(df, hide_index=True, use_container_width=True)

else:
    st.warning("⚠️ Aucune donnée trouvée. Vérifiez l'onglet Bilan et le partage du fichier.")
