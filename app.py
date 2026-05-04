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

# URL de base (on change juste le GID)
base_url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid="
sheet_url = f"{base_url}{votre_gid}"

try:
    df_raw = pd.read_csv(sheet_url)

    # --- CAS 1 : PAGE D'ACCUEIL GLOBAL ---
    if selection == "ACCUEIL (Global)":
        # (Ton code actuel pour le graphique global)
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
            df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
            df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
            
            df = df.dropna(subset=[col_nom])
            
            # Graphique
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(f"{col_nom}:N", sort='-y'),
                y=alt.Y(f"{col_data}:Q"),
                color=alt.condition(alt.datum[col_data] < 2000, alt.value("#2ecc71"), 
                     alt.condition(alt.datum[col_data] <= 4000, alt.value("#f39c12"), alt.value("#e74c3c"))),
                tooltip=[col_nom, col_data]
            ).properties(height=450).interactive()
            st.altair_chart(chart, use_container_width=True)
            st.info("💡 Seuils : 🟢 < 2000 | 🟡 2000-4000 | 🔴 > 4000")
            st.subheader("📋 Récapitulatif")
            st.dataframe(df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', na=False)], use_container_width=True)

    # --- CAS 2 : PAGES INDIVIDUELLES ---
    else:
        st.info(f"Visualisation des données pour {selection}")
        # Affichage des données brutes de l'onglet établissement
        st.subheader("📊 Fiche de saisie actuelle")
        st.dataframe(df_raw, use_container_width=True)
        
        st.warning("🔒 La modification directe sera disponible après configuration du code secret.")

except Exception as e:
    st.error(f"Erreur de chargement : {e}")
