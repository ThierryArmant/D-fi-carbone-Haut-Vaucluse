import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Défi Carbone", layout="wide")

# --- DICTIONNAIRE DES GIDs ---
ETABLISSEMENTS = {
    "ACCUEIL (Global)": "169103083",
    "LYCEE DE L’ARC": "424429658",
    "COLLEGE ARAUSIO": "1079800482",
    "COLLEGE B. HENDRICKS": "413375690",
    "COLLEGE J. GIONO": "848288657",
    "LP A. BRIAND": "1890998348",
    "LP ARGENSOL": "1856139655",
    "LYCEE VITICOLE": "1275913125",
    "ES SAINT LOUIS": "1284271428",
    "LYCEE L. AUBRAC": "1075832409",
    "COLLEGE H. BOUDON": "1926531695",
    "COLLEGE P. ELUARD": "1779665525",
    "COLLEGE VALLIS AERIA": "1912810443",
    "LP F. REVOUL": "1215829245",
    "ES SAINT-JEAN-LE-BAPTISTE": "864334585",
    "COLLEGE V. SCHOELCHER": "1941498887",
    "COLLEGE SAINT-EXUPERY": "1790573676",
    "ECOLE JULES FERRY": "1186020464",
    "ECOLE DU GRILLON": "1100355066",
    "ECOLE CURIE": "977476270"
}

# --- BARRE LATÉRALE ---
st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Choisir un établissement :", list(ETABLISSEMENTS.keys()))
votre_gid = ETABLISSEMENTS[selection]

st.title(f"🌱 {selection}")

# URL de base
base_url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid="
sheet_url = f"{base_url}{votre_gid}"

try:
    df_raw = pd.read_csv(sheet_url)

    # --- CAS 1 : PAGE D'ACCUEIL GLOBAL ---
    if selection == "ACCUEIL (Global)":
        # On cherche la ligne de titre
        for i in range(len(df_raw)):
            if "Etablissements" in df_raw.iloc[i].values:
                df = df_raw.iloc[i:].copy()
                df.columns = df.iloc[0]
                df = df.iloc[1:].reset_index(drop=True)
                break
        
        col_nom = "Etablissements"
        col_data = "Total émissions"
        df.columns = [str(c).strip() for c in df.columns]
        
        if col_data in df.columns:
            # Nettoyage des chiffres
            df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
            df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
            df = df.dropna(subset=[col_nom])

            # CALCUL DE LA COULEUR (Méthode robuste)
            def get_color(v):
                if v < 2000: return "#2ecc71"
                elif v <= 4000: return "#f39c12"
                else: return "#e74c3c"
            
            df['color_hex'] = df[col_data].apply(get_color)

            # GRAPHIQUE
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(f"{col_nom}:N", sort='-y', title="Établissements"),
                y=alt.Y(f"{col_data}:Q", title="Émissions (kg CO2e)"),
                color=alt.Color('color_hex:N', scale=None),
                tooltip=[col_nom, col_data]
            ).properties(height=450).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            st.info("💡 Seuils : 🟢 < 2000 | 🟡 2000-4000 | 🔴 > 4000")
            
            st.subheader("📋 Récapitulatif")
            # Nettoyage des colonnes Unnamed pour le tableau
            df_display = df.drop(columns=['color_hex'])
            df_display = df_display.loc[:, ~df_display.columns.str.contains('^Unnamed|^nan', na=False)]
            st.dataframe(df_display, use_container_width=True)

    # --- CAS 2 : PAGES INDIVIDUELLES ---
    else:
        st.info(f"Visualisation de la fiche de saisie pour : **{selection}**")
        
        # On affiche la fiche telle qu'elle apparaît sur l'image_47f0e3.png
        st.subheader(f"📊 Données en direct (Onglet GID {votre_gid})")
        
        # Nettoyage rapide pour l'affichage de la fiche individuelle
        df_indiv = df_raw.dropna(how='all', axis=0).dropna(how='all', axis=1)
        st.dataframe(df_indiv, use_container_width=True)
        
        st.warning("🔒 Pour modifier ces chiffres, vous devrez saisir le code d'accès de l'établissement (Prochainement).")

except Exception as e:
    st.error(f"Erreur technique : {e}")
