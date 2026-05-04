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
    # 1. Chargement brut sans noms de colonnes imposés
    df_raw = pd.read_csv(sheet_url, header=None)
    
    if selection == "ACCUEIL (Global)":
        # 2. Scanner pour trouver la ligne de titres
        header_row_index = 0
        for i, row in df_raw.iterrows():
            row_str = " ".join([str(val).lower() for val in row.values])
            if "etablissement" in row_str or "lycée" in row_str or "collège" in row_str:
                header_row_index = i
                break
        
        # 3. Préparer les titres proprement (Anti-doublons)
        raw_headers = df_raw.iloc[header_row_index].values
        clean_headers = []
        for i, h in enumerate(raw_headers):
            h_str = str(h).strip()
            if h_str == "" or h_str.lower() == "nan":
                clean_headers.append(f"Vide_{i}") # On nomme les colonnes vides différemment
            else:
                clean_headers.append(h_str)

        # 4. Appliquer les titres au tableau
        df = df_raw.iloc[header_row_index + 1:].copy()
        df.columns = clean_headers
        df = df.reset_index(drop=True)

        # 5. Identifier les colonnes de données
        col_nom = next((c for c in df.columns if "etab" in str(c).lower()), df.columns[0])
        col_data = next((c for c in df.columns if "total" in str(c).lower() and "émis" in str(c).lower()), None)
        
        if not col_data:
            # Si on ne trouve pas par nom, on cherche la colonne qui contient le plus de chiffres
            col_data = df.columns[-1]

        # 6. Nettoyage numérique
        df[col_data] = df[col_data].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True)
        df[col_data] = pd.to_numeric(df[col_data], errors='coerce').fillna(0)
        df = df.dropna(subset=[col_nom])

        # 7. Couleurs et Graphique
        def set_color(v):
            if v < 2000: return "#2ecc71"
            elif v <= 4000: return "#f39c12"
            else: return "#e74c3c"
        df['color_hex'] = df[col_data].apply(set_color)

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f"{col_nom}:N", sort='-y', title="Établissements"),
            y=alt.Y(f"{col_data}:Q", title="Émissions (kg CO2e)"),
            color=alt.Color('color_hex:N', scale=None),
            tooltip=[col_nom, col_data]
        ).properties(height=450).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        st.info("💡 Seuils : 🟢 < 2000 | 🟡 2000-4000 | 🔴 > 4000")
        
        # Affichage du tableau final (en cachant les colonnes "Vide_x")
        cols_finales = [c for c in df.columns if "Vide_" not in str(c) and c != "color_hex"]
        st.dataframe(df[cols_finales], use_container_width=True)

    else:
        # Pages individuelles : on utilise la même logique de titres pour éviter le crash
        st.info(f"Fiche de données : **{selection}**")
        df_indiv = df_raw.dropna(how='all', axis=1).dropna(how='all', axis=0)
        st.dataframe(df_indiv, use_container_width=True)

except Exception as e:
    st.error(f"Erreur technique : {e}")
