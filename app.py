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

st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Choisir un établissement :", list(ETABLISSEMENTS.keys()))
votre_gid = ETABLISSEMENTS[selection]

st.title(f"🌱 {selection}")

base_url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid="
sheet_url = f"{base_url}{votre_gid}"

try:
    # Lecture brute
    df_raw = pd.read_csv(sheet_url)
    
    if selection == "ACCUEIL (Global)":
        # Tentative de nettoyage des colonnes vides
        df_raw = df_raw.loc[:, ~df_raw.columns.str.contains('^Unnamed|^nan', na=False)]
        
        # Étape 1 : Trouver la ligne où il y a "Etablissements"
        target_row = None
        for i in range(len(df_raw)):
            row_values = [str(x).lower() for x in df_raw.iloc[i].values]
            if any("etablissement" in x for x in row_values):
                target_row = i
                break
        
        # Étape 2 : Si on a trouvé la ligne, on redéfinit le tableau
        if target_row is not None:
            df = df_raw.iloc[target_row:].copy()
            df.columns = df.iloc[0]
            df = df.iloc[1:].reset_index(drop=True)
        else:
            # Plan B : On prend les titres actuels si la recherche échoue
            df = df_raw.copy()

        # Nettoyage des noms de colonnes
        df.columns = [str(c).strip() for c in df.columns]
        
        # Identification des colonnes vitales
        col_nom = next((c for c in df.columns if "etab" in c.lower()), df.columns[0])
        col_data = next((c for c in df.columns if "total" in c.lower()), None)

        if col_data:
            # Conversion numérique
            df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
            df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
            df = df.dropna(subset=[col_nom])

            # Application des couleurs
            def set_color(v):
                if v < 2000: return "#2ecc71"
                elif v <= 4000: return "#f39c12"
                else: return "#e74c3c"
            df['color_hex'] = df[col_data].apply(set_color)

            # Graphique Altair
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(f"{col_nom}:N", sort='-y', title="Établissements"),
                y=alt.Y(f"{col_data}:Q", title="Émissions (kg CO2e)"),
                color=alt.Color('color_hex:N', scale=None),
                tooltip=[col_nom, col_data]
            ).properties(height=450).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            st.info("💡 Seuils : 🟢 < 2000 | 🟡 2000-4000 | 🔴 > 4000")
            st.dataframe(df.drop(columns=['color_hex'], errors='ignore'), use_container_width=True)
        else:
            st.error("Impossible de trouver la colonne 'Total émissions'.")
            st.write("Colonnes détectées :", list(df.columns))

    else:
        # Pages individuelles (Jean Giono, etc.)
        st.info(f"Données brutes pour : **{selection}**")
        st.dataframe(df_raw.dropna(how='all', axis=1), use_container_width=True)

except Exception as e:
    st.error(f"Erreur : {e}")
