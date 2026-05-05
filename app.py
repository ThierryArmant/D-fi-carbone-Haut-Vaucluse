import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# --- CONNEXION ---
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    df = pd.read_csv(sheet_url)
    
    # Recherche de la ligne de titre
    for i in range(len(df)):
        if "Etablissements" in df.iloc[i].values:
            df.columns = df.iloc[i]
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # --- NETTOYAGE ---
    col_nom = "Etablissements"
    col_data = "Total émissions"

    df.columns = [str(c).strip() for c in df.columns]
    if col_data in df.columns:
        df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    
    df = df.dropna(subset=[col_nom])
    df = df.loc[:, df.columns.notnull()]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', na=False)]

    # --- CALCUL DE LA COULEUR ---
    def determiner_couleur(valeur):
        if valeur < 2000:
            return "#2ecc71" # Vert
        elif valeur <= 4000:
            return "#f39c12" # Orange
        else:
            return "#e74c3c" # Rouge

    df['color_hex'] = df[col_data].apply(determiner_couleur)

    st.success("Données synchronisées !")

    # --- GRAPHIQUE (Taille réduite à 200 au lieu de 450) ---
    st.subheader("📊 Analyse des émissions par établissement")

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{col_nom}:N", sort='-y', title="Établissements"),
        y=alt.Y(f"{col_data}:Q", title="Émissions (kg CO2e)"),
        color=alt.Color('color_hex:N', scale=None),
        tooltip=[col_nom, col_data]
    ).properties(height=200).interactive() # <--- Taille divisée par deux ici

    st.altair_chart(chart, use_container_width=True)
    st.info("💡 **Seuils :** 🟢 < 2000 kg | 🟡 2000-4000 kg | 🔴 > 4000 kg")

    # --- TABLEAU (2/3) ET DASHBOARD (1/3) ---
    col_gauche, col_droite = st.columns([2, 1])

    with col_gauche:
        st.subheader("📋 Détail des résultats")
        # Taille du tableau fixée à 300 pour gagner de la place
        st.dataframe(df.drop(columns=['color_hex']), use_container_width=True, height=300)
    
    with col_droite:
        st.subheader("🎯 Dashboard Global")
        
        # Calcul global pour le camembert
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        cols_valides = [c for c in postes if c in df.columns]
        
        if cols_valides:
            # Conversion numérique pour sécurité
            for c in cols_valides:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            
            totaux = df[cols_valides].sum().reset_index()
            totaux.columns = ['Poste', 'Valeur']

            # Camembert compact
            fig_pie = px.pie(totaux, values='Valeur', names='Poste', hole=0.4)
            fig_pie.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Fusée (Jauge) compacte
            total_global = totaux['Valeur'].sum()
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_global,
                number = {'font': {'size': 20}},
                gauge = {'axis': {'range': [None, 2000000]}, 'bar': {'color': "#e74c3c"}}
            ))
            fig_gauge.update_layout(height=150, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_gauge, use_container_width=True)

except Exception as e:
    st.error(f"Erreur technique : {e}")
