import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration large pour le confort visuel
st.set_page_config(page_title="Défi Carbone EPLE", layout="wide")

st.title("🌍 Mon Défi Carbone - Haut Vaucluse")

# 2. Identifiant de ton Google Sheets
sheet_id = "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"

# 3. Menu latéral pour choisir l'établissement
etablissement = st.sidebar.selectbox("Choisir un établissement", ["GIONO", "EXUPERY"])

# 4. URL de lecture directe (très rapide)
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={etablissement}"

try:
    # Lecture des données
    df = pd.read_csv(url)
    
    # NETTOYAGE : On enlève les colonnes vides et on normalise les noms
    df = df.dropna(axis=1, how='all') 
    df.columns = [str(c).strip().capitalize() for c in df.columns]

    # --- MISE EN PAGE 2/3 (Tableau) et 1/3 (Dashboard) ---
    col_table, col_dash = st.columns([2, 1])

    with col_table:
        st.subheader(f"📊 Données : {etablissement}")
        # On affiche le tableau proprement
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col_dash:
        st.subheader("🎯 Dashboard")
        
        # On vérifie si les colonnes Poste et Total existent bien
        if 'Poste' in df.columns and 'Total' in df.columns:
            # --- LE CAMEMBERT ---
            fig_pie = px.pie(
                df, 
                values='Total', 
                names='Poste',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.divider()
            
            # --- LA FUSÉE / JAUGE ---
            total_conso = pd.to_numeric(df['Total'], errors='coerce').sum()
            st.metric("Consommation Totale", f"{total_conso:,.0f} kg CO2e")
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_conso,
                gauge = {
                    'axis': {'range': [None, 5000]}, # Limite max à 5000, modifiable
                    'bar': {'color': "#e74c3c"}, # Rouge
                    'steps': [
                        {'range': [0, 2500], 'color': "#f4f9f4"},
                        {'range': [2500, 5000], 'color': "#fdf2f2"}
                    ],
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.warning("⚠️ Pour voir les graphiques, nommez vos colonnes 'Poste' et 'Total' dans votre Sheets.")

except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.info("Vérifiez que le partage du fichier est bien sur 'Tous les utilisateurs disposant du lien'.")

st.caption(f"Source : {etablissement} - Projet EPLE Bas Carbone")
