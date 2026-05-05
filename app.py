import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration de la page en mode large
st.set_page_config(page_title="Défi Carbone : Réseau Haut Vaucluse", layout="wide")

st.title("🌍 Défi Carbone : Réseau Haut Vaucluse")

# 2. Identifiant de ton Google Sheets
sheet_id = "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"
# On cible l'onglet principal qui contient le tableau récapitulatif
onglet_global = "GIONO" # Modifie ce nom si l'onglet global s'appelle autrement

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={onglet_global}"

try:
    # Lecture des données
    df = pd.read_csv(url)
    
    # Nettoyage des noms de colonnes
    df.columns = [str(c).strip() for c in df.columns]

    # --- MISE EN PAGE : TABLEAU À GAUCHE (2/3), DASHBOARD À DROITE (1/3) ---
    col_gauche, col_droite = st.columns([2, 1])

    with col_gauche:
        st.subheader("📑 Détail des résultats")
        # Affichage du grand tableau
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Ajout du graphique en barres (comme sur ton image du haut)
        st.subheader("📊 Analyse des émissions par établissement")
        if 'Etablissement' in df.columns and 'Total' in df.columns:
            fig_bar = px.bar(df, x='Etablissement', y='Total', color_discrete_sequence=['#e74c3c'])
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_droite:
        st.subheader("🎯 Dashboard")
        
        # On vérifie si les colonnes nécessaires existent pour les graphiques
        # Note : Adapte 'Poste' et 'Total' si tes colonnes s'appellent différemment
        if 'Poste' in df.columns and 'Total' in df.columns:
            # 1. LE CAMEMBERT
            fig_pie = px.pie(df, values='Total', names='Poste', hole=0.4)
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.divider()
            
            # 2. LA FUSÉE (Jauge de consommation globale)
            total_global = df['Total'].sum()
            st.metric("Émissions Totales Réseau", f"{total_global:,.0f} kg CO2e")
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_global,
                gauge = {
                    'axis': {'range': [None, 100000]}, # Limite à adapter selon ton réseau
                    'bar': {'color': "#e74c3c"},
                    'steps': [
                        {'range': [0, 50000], 'color': "#f4f9f4"},
                        {'range': [50000, 100000], 'color': "#fdf2f2"}
                    ],
                }
            ))
            fig_gauge.update_layout(height=300, margin=dict(t=30, b=0, l=30, r=30))
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.info("💡 Pour afficher le Camembert et la Fusée, assurez-vous d'avoir des colonnes nommées 'Poste' et 'Total'.")

except Exception as e:
    st.error(f"Erreur d'affichage : {e}")

st.caption("Données synchronisées en temps réel avec le Google Sheets de l'OCE.")
