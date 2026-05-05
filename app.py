import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration large
st.set_page_config(page_title="Défi Carbone : Réseau Haut Vaucluse", layout="wide")

st.title("🌍 Défi Carbone : Réseau Haut Vaucluse")

# 2. Lien direct Sheets (Onglet GIONO)
sheet_id = "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=GIONO"

try:
    # Lecture et nettoyage
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]

    # --- 📊 PARTIE 1 : GRAPHIQUE DE COMPARAISON (FORMAT RÉDUIT) ---
    st.markdown("### 📊 Analyse des émissions par établissement")
    if 'Etablissements' in df.columns and 'Total émissions' in df.columns:
        # On définit une hauteur fixe de 200 pour diviser par deux la taille
        fig_bar = px.bar(df, x='Etablissements', y='Total émissions', color_discrete_sequence=['#e74c3c'])
        fig_bar.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()

    # --- 🏗️ PARTIE 2 : TABLEAU ET DASHBOARD ---
    col_gauche, col_droite = st.columns([2, 1])

    with col_gauche:
        st.markdown("### 📑 Détail des résultats")
        # On limite la hauteur du tableau pour qu'il soit compact
        st.dataframe(df, use_container_width=True, hide_index=True, height=300)

    with col_droite:
        st.markdown("### 🎯 Dashboard Global")
        
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        cols_valides = [c for c in postes if c in df.columns]
        
        if cols_valides:
            totaux_par_poste = df[cols_valides].sum().reset_index()
            totaux_par_poste.columns = ['Poste', 'Valeur']

            # Camembert compact
            fig_pie = px.pie(totaux_par_poste, values='Valeur', names='Poste', hole=0.4)
            fig_pie.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Fusée compacte
            total_global = totaux_par_poste['Valeur'].sum()
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_global,
                number = {'font': {'size': 20}},
                gauge = {'axis': {'range': [None, 2000000]}, 'bar': {'color': "#e74c3c"}}
            ))
            fig_gauge.update_layout(height=150, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_gauge, use_container_width=True)

except Exception as e:
    st.error(f"Erreur : {e}")
