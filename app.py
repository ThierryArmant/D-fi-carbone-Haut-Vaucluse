import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Défi Carbone", layout="wide")

# --- STYLE ET FOND D'ÉCRAN ---
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
            padding: 1.5rem !important;
            border-radius: 12px;
            margin-top: 10px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
            max-width: 95% !important;
        }}
        /* Zone scrollable pour le graphique du haut */
        .scroll-graph {{
            height: 300px;
            overflow-y: auto;
            border: 1px solid #eee;
            padding: 10px;
            border-radius: 8px;
        }}
        [data-testid="stHeader"] {{ height: 0px; }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_and_style()

# --- CONNEXION ET NETTOYAGE ---
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    df_raw = pd.read_csv(sheet_url)
    for i in range(len(df_raw)):
        if "Etablissements" in df_raw.iloc[i].values:
            new_cols = df_raw.iloc[i].values
            cleaned_cols = [str(c) if pd.notnull(c) else f"vide_{idx}" for idx, c in enumerate(new_cols)]
            df = df_raw.iloc[i+1:].copy()
            df.columns = cleaned_cols
            break

    df = df.loc[:, ~df.columns.str.contains('vide_')]
    col_nom = "Etablissements"
    col_pers = "conso carbone  par personne"
    df.columns = [str(c).strip() for c in df.columns]

    if col_pers in df.columns:
        df[col_pers] = df[col_pers].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_pers] = pd.to_numeric(df[col_pers], errors='coerce').fillna(0)
    
    df = df.dropna(subset=[col_nom])
    # On trie et on s'assure qu'il n'y a pas de doublons bizarres
    df_sorted = df.groupby(col_nom)[col_pers].sum().reset_index().sort_values(by=col_pers)

    st.markdown("<h3 style='text-align: center; color: #1e3d59; margin-bottom: 20px;'>🌱 Consommation Carbone : Réseau Haut Vaucluse</h3>", unsafe_allow_html=True)
    
    # --- GRAPHIQUES ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 14px;'>🏆 kg CO2e / personne (déroulant)</p>", unsafe_allow_html=True)
        # Création du graphique avec une hauteur calculée selon le nombre d'établissements
        # pour forcer le scroll dans la "div" parente
        nb_etab = len(df_sorted)
        hauteur_reelle = max(250, nb_etab * 40) # 40px par ligne pour que ce soit bien lisible
        
        fig_indiv = px.bar(df_sorted, x=col_pers, y=col_nom, orientation='h', text=col_pers, 
                           color=col_pers, color_continuous_scale='RdYlGn_r')
        fig_indiv.update_traces(texttemplate='%{text:.1f}', textposition='outside', textfont_size=14)
        fig_indiv.update_layout(
            height=hauteur_reelle, 
            margin=dict(t=0, b=0, l=0, r=50), 
            showlegend=False, 
            coloraxis_showscale=False,
            xaxis={'title': ''},
            yaxis={'title': '', 'tickfont': {'size': 12}}
        )
        
        # On place le graphique dans la zone scrollable
        st.markdown('<div class="scroll-graph">', unsafe_allow_html=True)
        st.plotly_chart(fig_indiv, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 14px;'>🎯 Répartition par Poste</p>", unsafe_allow_html=True)
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        cols_valides = [c for c in postes if c in df.columns]
        if cols_valides:
            temp_df = df[cols_valides].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce')).sum().reset_index()
            temp_df.columns = ['Poste', 'Valeur']
            fig_pie = px.pie(temp_df, values='Valeur', names='Poste', hole=0.4, 
                             color_discrete_sequence=['#2ecc71', '#ff8a80', '#fbc02d', '#3498db', '#f39c12'])
            fig_pie.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- TABLEAU ---
    st.markdown("<p style='font-weight: bold; font-size: 14px;'>📋 Détails Complets</p>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=350, hide_index=True)

except Exception as e:
    st.error(f"Erreur : {e}")
