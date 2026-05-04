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

base_url = "https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid="
sheet_url = f"{base_url}{votre_gid}"

try:
    # On utilise mangle_dupe_cols=True pour éviter l'erreur des 'nan'
    df_raw = pd.read_csv(sheet_url)
    
    # Nettoyage immédiat des noms de colonnes pour éviter les erreurs Pandas
    df_raw.columns = [f"Col_{i}" if pd.isna(c) or 'Unnamed' in str(c) else c for i, c in enumerate(df_raw.columns)]

    # --- CAS 1 : PAGE D'ACCUEIL GLOBAL ---
    if selection == "ACCUEIL (Global)":
        for i in range(len(df_raw)):
            if any("Etablissements" in str(val) for val in df_raw.iloc[i].values):
                df = df_raw.iloc[i:].copy()
                df.columns = df.iloc[0]
                # On rend les colonnes uniques après avoir défini les nouveaux titres
                df.columns = [f"{c}_{i}" if list(df.columns).count(c) > 1 else c for i, c in enumerate(df.columns)]
                df = df.iloc[1:].reset_index(drop=True)
                break
        
        col_nom = "Etablissements"
        col_data = "Total émissions"
        
        # On s'assure de trouver la colonne même avec des espaces
        col_nom = [c for c in df.columns if "Etablissements" in str(c)][0]
        col_data = [c for c in df.columns if "Total émissions" in str(c)][0]

        df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
        df = df.dropna(subset=[col_nom])

        def get_color(v):
            if v < 2000: return "#2ecc71"
            elif v <= 4000: return "#f39c12"
            else: return "#e74c3c"
        
        df['color_hex'] = df[col_data].apply(get_color)

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f"{col_nom}:N", sort='-y', title="Établissements"),
            y=alt.Y(f"{col_data}:Q", title="Émissions (kg CO2e)"),
            color=alt.Color('color_hex:N', scale=None),
            tooltip=[col_nom, col_data]
        ).properties(height=450).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        st.info("💡 Seuils : 🟢 < 2000 | 🟡 2000-4000 | 🔴 > 4000")
        
        st.subheader("📋 Récapitulatif")
        # On cache les colonnes de travail et les 'Col_x' générées
        cols_to_show = [c for c in df.columns if 'color_hex' not in str(c) and 'Col_' not in str(c)]
        st.dataframe(df[cols_to_show], use_container_width=True)

    # --- CAS 2 : PAGES INDIVIDUELLES ---
    else:
        st.info(f"Fiche de saisie : **{selection}**")
        # On affiche uniquement les colonnes qui ont du contenu
        df_indiv = df_raw.dropna(how='all', axis=1)
        st.dataframe(df_indiv, use_container_width=True)
        st.warning("🔒 Modification bientôt disponible.")

except Exception as e:
    st.error(f"Erreur technique : {e}")
