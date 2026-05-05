import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration large
st.set_page_config(page_title="Défi Carbone : Réseau Haut Vaucluse", layout="wide")

st.title("🌍 Défi Carbone : Réseau Haut Vaucluse")

# 2. Lien direct vers ton Sheets (Onglet GIONO qui contient tout le réseau)
sheet_id = "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=GIONO"

try:
    # Lecture des données
    df = pd.read_csv(url)
    # Nettoyage automatique des noms de colonnes (enlève les espaces invisibles)
    df.columns = [str(c).strip() for c in df.columns]

    # --- 📊 PARTIE 1 : GRAPHIQUE DE COMPARAISON (EN HAUT) ---
    st.subheader("📊 Analyse des émissions par établissement")
    # On utilise 'Etablissement' pour les noms et 'Total émissions' pour les barres
    if 'Etablissement' in df.columns and 'Total émissions' in df.columns:
        fig_bar = px.bar(df, x='Etablissement', y='Total émissions', color_discrete_sequence=['#e74c3c'])
        fig_bar.update_layout(height=350, margin=dict(t=10, b=10, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()

    # --- 🏗️ PARTIE 2 : TABLEAU (GAUCHE) ET DASHBOARD (DROITE) ---
    col_gauche, col_droite = st.columns([2, 1])

    with col_gauche:
        st.subheader("📑 Détail des résultats")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col_droite:
        st.subheader("🎯 Dashboard Global")
        
        # Liste des colonnes à additionner pour le camembert
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        # On vérifie lesquelles existent réellement dans ton Sheets
        cols_valides = [c for c in postes if c in df.columns]
        
        if cols_valides:
            # Calcul des totaux cumulés de tous les établissements
            totaux_par_poste = df[cols_valides].sum().reset_index()
            totaux_par_poste.columns = ['Poste', 'Valeur']

            # 🥧 LE CAMEMBERT
            fig_pie = px.pie(totaux_par_poste, values='Valeur', names='Poste', hole=0.4)
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.divider()
            
            # 🚀 LA FUSÉE (JAUGE)
            total_global = totaux_par_poste['Valeur'].sum()
            st.metric("Total Réseau", f"{total_global:,.0f} kg CO2e")
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_global,
                gauge = {
                    'axis': {'range': [None, 2000000]}, # Limite haute adaptée au réseau
                    'bar': {'color': "#e74c3c"},
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.error("Colonnes de données non trouvées pour le dashboard.")

except Exception as e:
    st.error(f"Erreur technique : {e}")

st.caption("Données synchronisées - Réseau Haut Vaucluse")
