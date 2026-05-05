import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuration large pour avoir de la place
st.set_page_config(page_title="Défi Carbone EPLE", layout="wide")

st.title("🌍 Mon Défi Carbone - Haut Vaucluse")

# 2. Ta référence spécifique
sheet_id = "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M"

# 3. Menu latéral
etablissement = st.sidebar.selectbox("Choisir un établissement", ["GIONO", "EXUPERY"])

# 4. URL de lecture (format CSV pour la rapidité)
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={etablissement}"

try:
    # Lecture des données
    df = pd.read_csv(url)
    
    # NETTOYAGE : On enlève les colonnes vides et on uniformise les noms
    df = df.dropna(axis=1, how='all') 
    df.columns = [str(c).strip().capitalize() for c in df.columns]

    # --- MISE EN PAGE 2/3 (Tableau) et 1/3 (Dashboard) ---
    col_table, col_dash = st.columns([2, 1])

    with col_table:
        st.subheader(f"📊 Données : {etablissement}")
        # Affichage du tableau synthétique
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col_dash:
        st.subheader("🎯 Dashboard")
        
        # On cherche les colonnes Poste et Total même si elles ne sont pas parfaites
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
            
            # --- LA FUSÉE (JAUGE) ---
            total_conso = df['Total'].sum()
            st.metric("Consommation Totale", f"{total_conso:,.0f} kg CO2e")
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_conso,
                gauge = {
                    'axis': {'range': [None, 5000]}, # Limite à 5000kg
                    'bar': {'color': "#e74c3c"},
                    'steps': [
                        {'range': [0, 2500], 'color': "#f4f9f4"},
                        {'range': [2500, 5000], 'color': "#fdf2f2"}
                    ],
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.warning("⚠️ Attention : Pour voir les graphiques, nommez vos colonnes 'Poste' et 'Total' dans votre fichier Google Sheets.")

except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.info("Vérifiez que l'onglet porte bien le nom choisi dans le menu.")

st.caption(f"Lien source : {etablissement} - Projet EPLE Bas Carbone")
