import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Défi Carbone", layout="wide")
st.title("🌱 Défi Carbone : Réseau Haut Vaucluse")

# --- CONNEXION ---
votre_gid = "169103083" 
sheet_url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

try:
    # Lecture des données
    df = pd.read_csv(sheet_url)
    
    # Recherche automatique de la ligne de titre (pour sauter les en-têtes vides)
    for i in range(len(df)):
        if "Etablissements" in df.iloc[i].values:
            df.columns = df.iloc[i]
            df = df.iloc[i+1:].reset_index(drop=True)
            break

    # --- NETTOYAGE ET FORMATAGE ---
    col_nom = "Etablissements"
    col_data = "Total émissions"

    # Nettoyage des noms de colonnes (espaces invisibles)
    df.columns = [str(c).strip() for c in df.columns]

    if col_data in df.columns:
        # Conversion des chiffres (gestion des virgules et espaces)
        df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
    
    # Suppression des lignes vides
    df = df.dropna(subset=[col_nom])
    df = df.loc[:, df.columns.notnull()]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', na=False)]

    # --- CALCUL DES COULEURS DE SEUILS ---
    def determiner_couleur(valeur):
        if valeur < 2000:
            return "#2ecc71" # Vert
        elif valeur <= 4000:
            return "#f39c12" # Orange
        else:
            return "#e74c3c" # Rouge

    df['color_hex'] = df[col_data].apply(determiner_couleur)

    st.success("Données synchronisées !")

    # --- 📊 GRAPHIQUE PRINCIPAL (AGRANDI) ---
    st.subheader("📊 Analyse des émissions par établissement")

    # Création du graphique avec Altair
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{col_nom}:N", sort='-y', title="Établissements", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(f"{col_data}:Q", title="Émissions (kg CO2e)"),
        color=alt.Color('color_hex:N', scale=None),
        tooltip=[col_nom, col_data]
    ).properties(height=500).interactive() # Taille augmentée pour voir les scores

    st.altair_chart(chart, use_container_width=True)
    st.info("💡 **Seuils :** 🟢 < 2000 kg | 🟡 2000-4000 kg | 🔴 > 4000 kg")

    # --- 📋 TABLEAU (2/3) ET RÉPARTITION (1/3) ---
    col_gauche, col_droite = st.columns([2, 1])

    with col_gauche:
        st.subheader("📋 Détail des résultats")
        # Affichage du tableau (sans la colonne de couleur technique)
        st.dataframe(df.drop(columns=['color_hex']), use_container_width=True, height=400)
    
    with col_droite:
        st.subheader("🎯 Répartition Globale")
        
        # Liste des postes de consommation
        postes = ['Electricité', 'Combustible', 'Transport', 'Biens et consommables', 'Alimentation']
        cols_valides = [c for c in postes if c in df.columns]
        
        if cols_valides:
            # Conversion numérique de tous les postes
            for c in cols_valides:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            
            # Somme globale de tous les collèges pour le camembert
            totaux = df[cols_valides].sum().reset_index()
            totaux.columns = ['Poste', 'Valeur']

            # Camembert avec légende
            fig_pie = px.pie(
                totaux, 
                values='Valeur', 
                names='Poste', 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent')
            fig_pie.update_layout(
                height=400, 
                margin=dict(t=0, b=0, l=0, r=0),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Postes de consommation non détectés.")

except Exception as e:
    st.error(f"Erreur technique : {e}")
