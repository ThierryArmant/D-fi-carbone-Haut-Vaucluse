import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS (Mode Sombre / Reposant)
def set_style():
    st.markdown(
        """
        <style>
        /* Fond global de l'application (Gris-noir très doux) */
        .stApp { background-color: #0f172a; color: #f1f5f9; }
        
        /* Conteneur principal (Gris ardoise reposant) */
        .main .block-container {
            background-color: #1e293b;
            padding: 2rem 3rem !important;
            border-radius: 8px;
            color: #f1f5f9;
        }
        
        /* Titres des sections (Bleu ciel doux) */
        .inner-title {
            text-align: center; font-weight: bold; font-size: 20px; color: #38bdf8; margin-bottom: 15px;
        }
        [data-testid="stHeader"] { height: 0px; }
        .stTabs [data-baseweb="tab"] { font-weight: bold; color: #f1f5f9; }
        
        /* Style des anecdotes adaptées au fond sombre (Bleu nuit) */
        .anecdote {
            background-color: #1e3a8a;
            padding: 15px;
            border-left: 5px solid #3b82f6;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 10px;
            color: #eff6ff;
        }
        /* Style de la méthode adaptée au fond sombre (Vert forêt) */
        .methode {
            background-color: #14532d;
            padding: 10px;
            border-left: 5px solid #22c55e;
            border-radius: 5px;
            font-size: 0.9em;
            margin-top: 10px;
            color: #f0fdf4;
        }
        
        /* Styles des barres de progression adaptées au fond sombre */
        .pole-header {
            display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1em; margin-bottom: 5px; margin-top: 5px; color: #f1f5f9;
        }
        .sub-pole-header {
            display: flex; justify-content: space-between; font-size: 0.95em; color: #cbd5e1; margin-bottom: 3px; margin-top: 8px;
        }
        .bar-container {
            background-color: #475569; border-radius: 6px; height: 16px; width: 100%; margin-bottom: 15px; overflow: hidden;
        }
        .sub-bar-container {
            background-color: #334155; border-radius: 4px; height: 10px; width: 100%; margin-bottom: 10px; overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_style()

# Fonction utilitaire pour dessiner les barres de progression en HTML
def draw_custom_bar(label, value_kg, total_kg, color, is_sub=False):
    pct = (value_kg / total_kg * 100) if total_kg > 0 else 0
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

# --- ONGLET DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        col_etab = "Etablissements" if "Etablissements" in df.columns else df.columns[0]
        col_total = "Total émissions" if "Total émissions" in df.columns else df.columns[7]
        col_eff = "Effectif total" if "Effectif total" in df.columns else df.columns[1]
        col_conso = "conso carbone par personne" if "conso carbone par personne" in df.columns else df.columns[8]

        # Conversion numérique
        cols_to_convert = [c for c in df.columns if c != col_etab]
        for col in cols_to_convert:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        df_active = df[(df[col_etab].astype(str).str.strip() != "") & (df[col_conso] > 0)].copy()

        st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        # --- 🛠️ NOUVEL EMPLACEMENT : ACCÈS FORMULAIRE TOUT EN HAUT ---
        with st.expander("🔐 ESPACE ENSEIGNANTS : Saisie de nouvelles données", expanded=False):
            st.markdown("<p style='color: #cbd5e1; margin-bottom: 5px;'>Entrez le code secret pour déverrouiller l'accès direct au formulaire Google Forms de votre établissement.</p>", unsafe_allow_html=True)
            pwd = st.text_input("Code secret de déploiement :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.success("Accès autorisé ! Cliquez sur le bouton ci-dessous :")
                st.link_button("🚀 Ouvrir le formulaire de saisie mensuelle", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True) # Petit espace visuel douillet

        # --- BLOC : CLASSEMENT ET JAUGE GLOBALE ---
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

            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': " kg", 'font': {'color': '#f1f5f9'}}, gauge = {'axis': {'range': [None, 2000], 'tickfont': {'color': '#f1f5f9'}}, 'bar': {'color': "#38bdf8"}, 'steps': [{'range': [0, 500], 'color': "#1e3a8a"}, {'range': [500, 1000], 'color': "#b45309"}, {'range': [1000, 2000], 'color': "#991b1b"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 1000}}))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()

        # --- BLOC DU MILIEU : LE BILAN GRAPHIQUE DÉTAILLÉ ---
        st.markdown('<p class="inner-title">🔍 Analyse détaillée par Établissement</p>', unsafe_allow_html=True)
        
        if not df_active.empty:
            selected_school = st.selectbox("Sélectionnez un établissement pour explorer ses statistiques :", df_active[col_etab].unique())
            
            school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
            total_school_emissions = school_data[col_total]
            
            if total_school_emissions > 0:
                # Énergie
                elec_val = school_data.get("Electricité française", 0)
                fioul_val = school_data.get("Fioul", 0)
                gaz_val = school_data.get("Gaz Naturel", 0)
                total_energie = elec_val + fioul_val + gaz_val

                # Transports
                voit_val = school_data.get("Voiture à essence", 0)
                bus_v_val = school_data.get("Autobus (ville)", 0)
                bus_s_val = school_data.get("Autobus (sortie scolaire)", 0)
                total_transport = voit_val + bus_v_val + bus_s_val

                # Alimentation
                rep_m = school_data.get("Repas moyen", 0)
                rep_v = school_data.get("Repas végétarien", 0)
                rep_r = school_data.get("Repas viande rouge", 0)
                rep_b = school_data.get("Repas viande blanche", 0)
                rep_p = school_data.get("Repas POISSON", 0)
                total_alimentation = rep_m + rep_v + rep_r + rep_b + rep_p

                # Déchets
                dech_p = school_data.get("Déchets Papier", 0)
                dech_a = school_data.get("Déchets alimentaire", 0)
                dech_pl = school_data.get("Déchets plastique", 0)
                total_dechets = dech_p + dech_a + dech_pl

                # Biens & Consommables
                pap_val = school_data.get("Paper", 0) if "Paper" in df.columns else school_data.get("Papier", 0)
                plas_val = school_data.get("Plastique", 0)
                cart_val = school_data.get("Carton", 0)
                ordi_val = school_data.get("Ordinateur à écran plat", 0)
                imp_val = school_data.get("Imprimante", 0)
                phot_val = school_data.get("Photocopieurs", 0)
                vid_val = school_data.get("Vidéo projecteur", 0)
                total_biens = pap_val + plas_val + cart_val + ordi_val + imp_val + phot_val + vid_val

                # Rendu des barres colorées
                draw_custom_bar("❄️ Énergie & Bâtiments", total_energie, total_school_emissions, "#22c55e")
                with st.expander("Détails du poste Énergie"):
                    draw_custom_bar("• Électricité française", elec_val, total_energie, "#4ade80", is_sub=True)
                    draw_custom_bar("• Gaz Naturel", gaz_val, total_energie, "#4ade80", is_sub=True)
                    draw_custom_bar("• Fioul de chauffage", fioul_val, total_energie, "#4ade80", is_sub=True)

                draw_custom_bar("🍎 Alimentation & Cantine", total_alimentation, total_school_emissions, "#f97316")
                with st.expander("Détails du poste Alimentation"):
                    draw_custom_bar("• Repas avec Viande Rouge", rep_r, total_alimentation, "#fb923c", is_sub=True)
                    draw_custom_bar("• Repas avec Poisson", rep_p, total_alimentation, "#fb923c", is_sub=True)
                    draw_custom_bar("• Repas avec Viande Blanche", rep_b, total_alimentation, "#fb923c", is_sub=True)
                    draw_custom_bar("• Repas Standard Moyen", rep_m, total_alimentation, "#fb923c", is_sub=True)
                    draw_custom_bar("• Repas Végétarien", rep_v, total_alimentation, "#fb923c", is_sub=True)

                draw_custom_bar("🚌 Déplacements & Transports", total_transport, total_school_emissions, "#3b82f6")
                with st.expander("Détails du poste Transports"):
                    draw_custom_bar("• Trajets en Voiture thermique", voit_val, total_transport, "#60a5fa", is_sub=True)
                    draw_custom_bar("• Autobus (sorties scolaires)", bus_s_val, total_transport, "#60a5fa", is_sub=True)
                    draw_custom_bar("• Autobus (lignes régulières / ville)", bus_v_val, total_transport, "#60a5fa", is_sub=True)

                draw_custom_bar("📦 Biens, Consommables & Équipements", total_biens, total_school_emissions, "#a855f7")
                with st.expander("Détails du poste Équipements & Consommables"):
                    draw_custom_bar("• Photocopieurs (Empreinte de fabrication)", phot_val, total_biens, "#c084fc", is_sub=True)
                    draw_custom_bar("• Ordinateurs portables / écrans plats", ordi_val, total_biens, "#c084fc", is_sub=True)
                    draw_custom_bar("• Ramettes de papier consommées", pap_val, total_biens, "#c084fc", is_sub=True)
                    draw_custom_bar("• Vidéoprojecteurs", vid_val, total_biens, "#c084fc", is_sub=True)
                    draw_custom_bar("• Plastiques d'emballage", plas_val, total_biens, "#c084fc", is_sub=True)
                    draw_custom_bar("• Imprimantes laser", imp_val, total_biens, "#c084fc", is_sub=True)
                    draw_custom_bar("• Emballages Carton", cart_val, total_biens, "#c084fc", is_sub=True)

                draw_custom_bar("🗑️ Gestion des Déchets", total_dechets, total_school_emissions, "#6366f1")
                with st.expander("Détails du poste Déchets"):
                    draw_custom_bar("• Gaspillage alimentaire (restes de cantine)", dech_a, total_dechets, "#818cf8", is_sub=True)
                    draw_custom_bar("• Déchets plastiques non recyclés", dech_pl, total_dechets, "#818cf8", is_sub=True)
                    draw_custom_bar("• Déchets Papier jetés", dech_p, total_dechets, "#818cf8", is_sub=True)
            else:
                st.warning("Cet établissement n'a pas encore de données carbone calculées.")
        else:
            st.info("Aucune donnée disponible pour l'analyse par établissement.")

        st.divider()
        
        # --- BLOC DU BAS : TABLEAU CENTRALISÉ ---
        st.markdown('<p class="inner-title">📋 Synthèse Globale des Établissements (Données Centralisées)</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch")

# --- ONGLET GLOSSAIRE (Version Spéciale Élèves / Vie Quotidienne) ---
with tab_glossaire:
    st.markdown("<h2 style='color: #38bdf8; text-align: center;'>📖 Traducteur Carbone : Ça représente quoi dans ma vie ?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>Parce que les 'kg de CO2' c'est abstrait, voici ce que nos consommations représentent en objets ou activités de ton quotidien !</p>", unsafe_allow_html=True)
    
    g_tabs = st.tabs(["🍎 1. À la Cantine", "❄️ 2. Chauffage & Lumière", "🚌 3. Transports & Sorties", "🗑️ 4. Le Gaspillage", "📦 5. Matériel & Ordis"])
    
    with g_tabs[0]:
        st.subheader("🍎 Pôle Alimentation (L'impact de mon plateau)")
        st.markdown("""
        <div class="anecdote">
        <b>Si tu prends l'option VIANDE ROUGE (Bœuf) :</b><br>
        L'impact est de 7,26 kg CO2e. C'est l'équivalent exact de :<br>
        • Fabriquer <b>1 PAIRE DE BASKETS neuve</b> pour aller en EPS.<br>
        • Regarder des vidéos en streaming 4G sur ton téléphone pendant <b>150 HEURES d'affilée</b>.<br>
        • L'empreinte de fabrication de <b>300 canettes de soda</b> en aluminium.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="methode">
        <b>💡 Le réflexe malin :</b> En choisissant l'option <b>Poisson</b> (2 kg) ou <b>Viande Blanche</b> (1,6 kg), tu divises l'impact par 3. Si tu choisis le repas <b>Végétarien</b> (0,5 kg), c'est comme si tu ne lançais ton jeu vidéo préféré que pendant quelques heures. L'effort est énorme !
        </div>
        """, unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("❄️ Pôle Énergie (L'électricité et le chauffage du collège)")
        st.markdown("""
        <div class="anecdote">
        <b>Pour comprendre l'Électricité (1 kWh = 0,06 kg CO2e) :</b><br>
        1 kWh d'électricité au collège, ça permet de faire quoi chez toi ?<br>
        • Jouer à la <b>CONSOLE (PS5 ou Xbox Series X) pendant 8 HEURES</b> non-stop.<br>
        • Laisser la télévision du salon allumée pendant 15 heures.<br>
        • Recharger ton smartphone de 0% à 100% tous les soirs pendant <b>2 ANS</b> !
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="anecdote" style="background-color: #991b1b; border-left-color: #ef4444;">
        <b>⚠️ Le piège du Chauffage (Gaz et Fioul) :</b><br>
        Le gaz et le fioul polluent <b>4 à 5 fois plus</b> que l'électricité chez nous. <br>
        Ouvrir les fenêtres de la classe en plein hiver alors que le chauffage tourne à fond pendant 1 heure, c'est jeter en l'air l'équivalent carbone de <b>2 paires de jeans neufs</b> en pur gaspillage d'énergie.
        </div>
        """, unsafe_allow_html=True)

    with g_tabs
