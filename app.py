import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS (Pour calquer le design épuré des barres et des blocs)
def set_style():
    st.markdown(
        """
        <style>
        .stApp { background-color: #f8f9fa; }
        .main .block-container {
            background-color: #ffffff;
            padding: 2rem 3rem !important;
            border-radius: 0px;
        }
        .inner-title {
            text-align: center; font-weight: bold; font-size: 20px; color: #1e3d59; margin-bottom: 15px;
        }
        [data-testid="stHeader"] { height: 0px; }
        .stTabs [data-baseweb="tab"] { font-weight: bold; }
        
        /* Styles des barres de progression personnalisées */
        .pole-header {
            display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1em; margin-bottom: 5px; margin-top: 5px;
        }
        .sub-pole-header {
            display: flex; justify-content: space-between; font-size: 0.95em; color: #555; margin-bottom: 3px; margin-top: 8px;
        }
        .bar-container {
            background-color: #e9ecef; border-radius: 6px; height: 16px; width: 100%; margin-bottom: 15px; overflow: hidden;
        }
        .sub-bar-container {
            background-color: #f1f3f5; border-radius: 4px; height: 10px; width: 100%; margin-bottom: 10px; overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_style()

# Fonction utilitaire pour dessiner les barres de progression en HTML
def draw_custom_bar(label, value_kg, total_kg, color, is_sub=False):
    pct = (value_kg / total_kg * 100) if total_kg > 0 else 0
    # Formatage intelligent : affiche en Tonnes si >= 1000 kg, sinon en kg
    display_weight = f"{value_kg/1000:.2f} tonne" if value_kg >= 1000 else f"{value_kg:.1f} kg"
    
    if not is_sub:
        st.markdown(f"""
            <div class="pole-header"><span>{label}</span><span>{display_weight} - {pct:.1f} %</span></div>
            <div class="bar-container"><div style="background-color: {color}; height: 100%; width: {pct}%;"></div></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="sub-pole-header"><span>{label}</span><span>{display_weight} - {pct:.1f} %</span></div>
            <div class="sub-bar-container"><div style="background-color: {color}; height: 100%; width: {pct}%;"></div></div>
        """, unsafe_allow_html=True)

# 3. VARIABLES DE CONNEXION
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

# 4. CHARGEMENT DES DONNÉES
@st.cache_data(ttl=60)
def load_data():
    try:
        raw = pd.read_csv(url, header=None)
        for i, row in raw.iterrows():
            row_str = [str(x).strip() for x in row.values]
            if any("etablissement" in x.lower() for x in row_str):
                data = raw.iloc[i+1:].copy()
                new_cols = [str(val).strip() if pd.notnull(val) else f"Col_{j}" for j, val in enumerate(row.values)]
                data.columns = new_cols
                return data.loc[:, ~data.columns.duplicated()].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
    return pd.DataFrame()

df = load_data()

# Nettoyage global des colonnes
if not df.empty:
    df.columns = [str(c).replace('\xa0', ' ').replace('\n', ' ').strip() for c in df.columns]
    df.columns = [" ".join(c.split()) for c in df.columns]

# 5. NAVIGATION PAR ONGLETS
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel consommations carbone (5 Pôles)"])

with tab_dashboard:
    if not df.empty:
        # Noms des colonnes cibles
        col_etab = "Etablissements" if "Etablissements" in df.columns else df.columns[0]
        col_total = "Total émissions" if "Total émissions" in df.columns else df.columns[7]
        col_eff = "Effectif total" if "Effectif total" in df.columns else df.columns[1]
        col_conso = "conso carbone par personne" if "conso carbone par personne" in df.columns else df.columns[8]

        # Conversion numérique de TOUTES les colonnes de données pour les calculs graphiques
        cols_to_convert = [c for c in df.columns if c != col_etab]
        for col in cols_to_convert:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        # Filtrage des lignes actives
        df_active = df[(df[col_etab].astype(str).str.strip() != "") & (df[col_conso] > 0)].copy()

        st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        # --- BLOC DU HAUT : CLASSEMENT ET JAUGE GLOBALE ---
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements (kg/personne)</p>', unsafe_allow_html=True)
            if not df_active.empty:
                df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                st.dataframe(df_ranking, hide_index=True, width="stretch", height=380)
            else:
                st.info("En attente de données calculées...")
                
        with col2:
            st.markdown('<p class="inner-title">🚀 Moyenne du Réseau (kg/pers)</p>', unsafe_allow_html=True)
            if not df_active.empty and df_active[col_eff].sum() > 0:
                moyenne = df_active[col_total].sum() / df_active[col_eff].sum()
            else:
                moyenne = 0

            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg"}, gauge = {'axis': {'range': [None, 2000]}, 'bar': {'color': "#1e3d59"}, 'steps': [{'range': [0, 500], 'color': "#d4edda"}, {'range': [500, 1000], 'color': "#fff3cd"}, {'range': [1000, 2000], 'color': "#f8d7da"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 1000}}))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()

        # --- NOUVEAU BLOC DU MILIEU : LE BILAN GRAPHIQUE DÉTAILLÉ (Style Nos Gestes Climat) ---
        st.markdown('<p class="inner-title">🔍 Analyse détaillée par Établissement</p>', unsafe_allow_html=True)
        
        if not df_active.empty:
            # Menu déroulant pour choisir l'établissement à analyser
            selected_school = st.selectbox("Sélectionnez un établissement pour explorer ses statistiques :", df_active[col_etab].unique())
            
            # Extraction de la ligne de l'établissement choisi
            school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
            total_school_emissions = school_data[col_total]
            
            if total_school_emissions > 0:
                # 1. Définition des sous-composants basés STRICTEMENT sur les colonnes de calcul de ton Sheets
                # Pôle Énergie
                elec_val = school_data.get("Electricité française", 0)
                fioul_val = school_data.get("Fioul", 0)
                gaz_val = school_data.get("Gaz Naturel", 0)
                total_energie = elec_val + fioul_val + gaz_val

                # Pôle Transports
                voit_val = school_data.get("Voiture à essence", 0)
                bus_v_val = school_data.get("Autobus (ville)", 0)
                bus_s_val = school_data.get("Autobus (sortie scolaire)", 0)
                total_transport = voit_val + bus_v_val + bus_s_val

                # Pôle Alimentation
                rep_m = school_data.get("Repas moyen", 0)
                rep_v = school_data.get("Repas végétarien", 0)
                rep_r = school_data.get("Repas viande rouge", 0)
                rep_b = school_data.get("Repas viande blanche", 0)
                rep_p = school_data.get("Repas POISSON", 0)
                total_alimentation = rep_m + rep_v + rep_r + rep_b + rep_p

                # Pôle Déchets
                dech_p = school_data.get("Déchets Papier", 0)
                dech_a = school_data.get("Déchets alimentaire", 0)
                dech_pl = school_data.get("Déchets plastique", 0)
                total_dechets = dech_p + dech_a + dech_pl

                # Pôle Biens & Consommables
                pap_val = school_data.get("Papier", 0)
                plas_val = school_data.get("Plastique", 0)
                cart_val = school_data.get("Carton", 0)
                ordi_val = school_data.get("Ordinateur à écran plat", 0)
                imp_val = school_data.get("Imprimante", 0)
                phot_val = school_data.get("Photocopieurs", 0)
                vid_val = school_data.get("Vidéo projecteur", 0)
                total_biens = pap_val + plas_val + cart_val + ordi_val + imp_val + phot_val + vid_val

                # 2. Rendu Graphique des Menus Déroulants (Expanders)
                
                # --- ÉNERGIE & LOGEMENT ---
                draw_custom_bar("❄️ Énergie & Bâtiments", total_energie, total_school_emissions, "#2b8a3e")
                with st.expander("Détails du poste Énergie"):
                    draw_custom_bar("• Électricité française", elec_val, total_energie, "#40c057", is_sub=True)
                    draw_custom_bar("• Gaz Naturel", gaz_val, total_energie, "#40c057", is_sub=True)
                    draw_custom_bar("• Fioul de chauffage", fioul_val, total_energie, "#40c057", is_sub=True)

                # --- ALIMENTATION ---
                draw_custom_bar("🍎 Alimentation & Cantine", total_alimentation, total_school_emissions, "#e67e22")
                with st.expander("Détails du poste Alimentation"):
                    draw_custom_bar("• Repas avec Viande Rouge", rep_r, total_alimentation, "#f39c12", is_sub=True)
                    draw_custom_bar("• Repas avec Poisson", rep_p, total_alimentation, "#f39c12", is_sub=True)
                    draw_custom_bar("• Repas avec Viande Blanche", rep_b, total_alimentation, "#f39c12", is_sub=True)
                    draw_custom_bar("• Repas Standard Moyen", rep_m, total_alimentation, "#f39c12", is_sub=True)
                    draw_custom_bar("• Repas Végétarien", rep_v, total_alimentation, "#f39c12", is_sub=True)

                # --- TRANSPORTS ---
                draw_custom_bar("🚌 Déplacements & Transports", total_transport, total_school_emissions, "#228be6")
                with st.expander("Détails du poste Transports"):
                    draw_custom_bar("• Trajets en Voiture thermique", voit_val, total_transport, "#339af0", is_sub=True)
                    draw_custom_bar("• Autobus (sorties scolaires)", bus_s_val, total_transport, "#339af0", is_sub=True)
                    draw_custom_bar("• Autobus (lignes régulières / ville)", bus_v_val, total_transport, "#339af0", is_sub=True)

                # --- BIENS & MATÉRIEL ---
                draw_custom_bar("📦 Biens, Consommables & Équipements", total_biens, total_school_emissions, "#9c36b5")
                with st.expander("Détails du poste Équipements & Consommables"):
                    draw_custom_bar("• Photocopieurs (Empreinte de fabrication)", phot_val, total_biens, "#be4bdb", is_sub=True)
                    draw_custom_bar("• Ordinateurs portables / écrans plats", ordi_val, total_biens, "#be4bdb", is_sub=True)
                    draw_custom_bar("• Ramettes de papier consommées", pap_val, total_biens, "#be4bdb", is_sub=True)
                    draw_custom_bar("• Vidéoprojecteurs", vid_val, total_biens, "#be4bdb", is_sub=True)
                    draw_custom_bar("• Plastiques d'emballage", plas_val, total_biens, "#be4bdb", is_sub=True)
                    draw_custom_bar("• Imprimantes laser", imp_val, total_biens, "#be4bdb", is_sub=True)
                    draw_custom_bar("• Emballages Carton", cart_val, total_biens, "#be4bdb", is_sub=True)

                # --- DÉCHETS ---
                draw_custom_bar("🗑️ Gestion des Déchets", total_dechets, total_school_emissions, "#7950f2")
                with st.expander("Détails du poste Déchets"):
                    draw_custom_bar("• Gaspillage alimentaire (restes de cantine)", dech_a, total_dechets, "#94d82d", is_sub=True)
                    draw_custom_bar("• Déchets plastiques non recyclés", dech_pl, total_dechets, "#94d82d", is_sub=True)
                    draw_custom_bar("• Déchets Papier jetés", dech_p, total_dechets, "#94d82d", is_sub=True)
            else:
                st.warning("Cet établissement n'a pas encore de données carbone calculées.")
        else:
            st.info("Aucune donnée disponible pour l'analyse par établissement.")

        st.divider()
        
        # --- BLOC DU BAS : TABLEAU BRUT ---
        with st.expander("🔐 Saisie de nouvelles données"):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform")
        
        st.markdown('<p class="inner-title">📋 Synthèse Globale des Établissements (Données Centralisées)</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch")

# --- ONGLET GLOSSAIRE ---
with tab_glossaire:
    st.markdown("<h2 style='color: #1e3d59;'>📖 Référentiel des 5 Pôles Carbone</h2>", unsafe_allow_html=True)
    g_tabs = st.tabs(["🍎 1. Alimentation", "❄️ 2. Énergie & Clim", "🚌 3. Transports", "🗑️ 4. Déchets Alimentaires", "📦 5. Biens & Conso"])
    
    with g_tabs[0]:
        st.subheader("Pôle Restauration (Production)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Viande Rouge", "7.26 kg", "CO2e/repas")
        c2.metric("Viande Blanche", "1.60 kg", "CO2e/repas")
        c3.metric("Poisson", "2.00 kg", "CO2e/repas")
        c4.metric("Végétarien", "0.50 kg", "CO2e/repas")

    with g_tabs[1]:
        st.subheader("Pôle Énergie & Fluides")
        st.write("- **Électricité :** 0.06 kgCO2e / kWh")
        st.write("- **Gaz Naturel :** 0.227 kgCO2e / kWh")

    with g_tabs[2]:
        st.subheader("Pôle Transports")
        st.write("- **Autocar Scolaire :** 0.030 kgCO2e / km / élève")
        st.write("- **Voiture thermique :** 0.218 kgCO2e / km")

    with g_tabs[3]:
        st.subheader("Pôle Déchets Alimentaires")
        c_d1, c_d2 = st.columns(2)
        c_d1.metric("Assiette jetée (moyenne)", "1.20 kg", "CO2e / kg jeté")
        c_d2.metric("Gaspillage Pain", "0.63 kg", "CO2e / kg jeté")

    with g_tabs[4]:
        st.subheader("Pôle Biens & Consommables")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.write("**Papier et Fin de vie :**")
            st.write("- **Ramette A4 neuve :** 2.62 kgCO2e")
        with col_b2:
            st.write("**Équipements (Fabrication) :**")
            st.write("- **Photocopieur :** 850 kgCO2e")
            st.write("- **Ordinateur Portable :** 161 kgCO2e")

    st.divider()
    st.caption("Sources : Méthodologie ADEME / GIEC / PEBC - Mise à jour Mai 2026")
