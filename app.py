import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", layout="wide")

# --- STYLE CSS (FOND ET BLOC BLANC) ---
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
            background-color: #ffffff; 
            padding: 2rem 2rem !important; 
            border-radius: 12px;
            margin-top: 20px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
        }}
        [data-testid="stHeader"] {{ height: 0px; }}
        .inner-title {{
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            color: #1e3d59;
            margin-bottom: 15px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_and_style()

# --- CHARGEMENT DES DONNÉES (AVEC GESTION DES DOUBLONS DE L'IMAGE) ---
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    # Lecture brute sans header pour éviter l'erreur Duplicate Column Names
    df_raw = pd.read_csv(sheet_url, header=None)
    
    # Recherche de la ligne d'entête "Etablissements"
    df = None
    for i in range(len(df_raw)):
        row_values = [str(val).strip() for val in df_raw.iloc[i].values]
        if "Etablissements" in row_values:
            header = row_values
            df = df_raw.iloc[i+1:].copy()
            
            # Gestion des noms de colonnes en double (nan, Electricité, etc.)
            new_cols = []
            counts = {}
            for col in header:
                clean_col = col if col != "nan" else "Champ_Vide"
                if clean_col not in counts:
                    new_cols.append(clean_col)
                    counts[clean_col] = 1
                else:
                    new_cols.append(f"{clean_col}_{counts[clean_col]}")
                    counts[clean_col] += 1
            df.columns = new_cols
            break

    if df is not None:
        # Définition des colonnes clés
        col_nom = "Etablissements"
        col_total_brut = "Total émissions" 
        col_pers = "conso carbone  par personne"
        
        # Identification de la colonne Effectif (souvent 'Effectif total' ou contenant 'personnes')
        possible_pop_cols = [c for c in df.columns if 'effectif' in c.lower() or 'personnes' in c.lower()]
        col_nb_gens = possible_pop_cols[0] if possible_pop_cols else df.columns[1]

        # Nettoyage numérique
        for c in [col_total_brut, col_pers, col_nb_gens]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df = df.dropna(subset=[col_nom])

        # --- AFFICHAGE DU DASHBOARD ---
        st.markdown("<h2 style='text-align: center; color: #1e3d59; margin-bottom: 25px;'>🌱 Consommation Carbone : Réseau Haut Vaucluse</h2>", unsafe_allow_html=True)

        # LIGNE 1 : CLASSEMENT ET JAUGE
        col_left, col_right = st.columns([1.1, 0.9])

        with col_left:
            st.markdown('<p class="inner-title">📊 Classement par Établissement (Individuel)</p>', unsafe_allow_html=True)
            st.dataframe(
                df[[col_nom, col_pers]].sort_values(by=col_pers, ascending=False),
                column_config={
                    col_nom: "Établissement",
                    col_pers: st.column_config.ProgressColumn("Emissions / Pers", format="%.0f kg", min_value=0, max_value=5000)
                },
                hide_index=True, use_container_width=True, height=350 
            )

        with col_right:
            st.markdown('<p class="inner-title">🚀 Moyenne Réelle du Réseau (par personne)</p>', unsafe_allow_html=True)
            total_co2 = df[col_total_brut].sum()
            total_pop = df[col_nb_gens].sum()
            valeur_jauge = total_co2 / total_pop if total_pop > 0 else 0
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = valeur_jauge,
                number = {'suffix': " kg", 'font': {'size': 40}},
                gauge = {
                    'axis': {'range': [None, 5000]},
                    'bar': {'color': "#1e3d59"},
                    'steps': [
                        {'range': [0, 1500], 'color': "#2ecc71"},
                        {'range': [1500, 2500], 'color': "#fbc02d"},
                        {'range': [2500, 5000], 'color': "#ff8a80"}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 6}, 'thickness': 0.8, 'value': 2500}
                }
            ))
            fig.update_layout(height=350, margin=dict(t=20, b=0, l=30, r=30))
            st.plotly_chart(fig, use_container_width=True)

        # LIGNE 2 : SAISIE SÉCURISÉE
        st.markdown("---")
        with st.expander("📝 Mettre à jour les données de mon établissement"):
            c1, c2 = st.columns([1, 1])
            with c1:
                pwd = st.text_input("Code d'accès établissement :", type="password")
            with c2:
                st.info("La saisie s'effectue via le formulaire sécurisé Google Forms.")
                
            if pwd == "CARBONE2026":
                st.success("Accès autorisé")
                url_form = "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform"
                st.link_button("🚀 Ouvrir le formulaire de saisie", url_form, use_container_width=True, type="primary")
            elif pwd != "":
                st.error("Code incorrect")

        # LIGNE 3 : TABLEAU COMPLET
        st.markdown("<p style='font-weight: bold; color: #1e3d59; margin-top: 15px;'>📋 Détails Complets des Emissions (Source : Onglet Bilan)</p>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=400, hide_index=True)
    else:
        st.error("Impossible de trouver la colonne 'Etablissements' dans votre fichier.")

except Exception as e:
    st.error(f"Une erreur est survenue lors de la synchronisation : {e}")
