import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# 2. STYLE CSS (Lisibilité et design des encadrés)
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
        
        /* Style des anecdotes (Bleu) */
        .anecdote {
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 5px solid #2196f3;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        /* Style de la méthode (Vert) */
        .methode {
            background-color: #f1f8e9;
            padding: 10px;
            border-left: 5px solid #8bc34a;
            border-radius: 5px;
            font-size: 0.9em;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_style()

# 3. VARIABLES DE CONNEXION
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

# 4. CHARGEMENT DES DONNÉES (Direct et robuste pour Form_Responses)
@st.cache_data(ttl=60)
def load_data():
    try:
        # Lecture directe du CSV des réponses au formulaire
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
        st.error(f"Erreur de connexion Sheets : {e}")
    return pd.DataFrame()

df = load_data()

# 5. NAVIGATION PAR ONGLETS
tab_dashboard, tab_glossaire = st.tabs(["📊 Tableau de Bord", "📖 Référentiel consommations carbone (5 Pôles)"])

# --- ONGLET DASHBOARD ---
with tab_dashboard:
    if not df.empty:
        # --- RECHERCHE ET ADAPTATION AUTOMATIQUE DES COLONNES ---
        # Détecte la colonne établissement (qu'elle s'appelle 'Etablissements' ou 'Sélectionnez votre établissement')
        col_etab = [c for c in df.columns if "etab" in c.lower() or "Étab" in c][0] if any("etab" in c.lower() or "Étab" in c for c in df.columns) else df.columns[1]
        
        # Détection des autres colonnes clés par mots-clés
        col_total = [c for c in df.columns if "total" in c.lower() or "émission" in c.lower()][0] if any("total" in c.lower() or "émission" in c.lower() for c in df.columns) else None
        col_eff = [c for c in df.columns if "effectif" in c.lower() or "nombre" in c.lower()][0] if any("effectif" in c.lower() or "nombre" in c.lower() for c in df.columns) else None
        col_conso = [c for c in df.columns if "conso" in c.lower() and "personne" in c.lower()][0] if any("conso" in c.lower() and "personne" in c.lower() for c in df.columns) else None

        # Nettoyage automatique de toutes les colonnes numériques du formulaire
        for col in df.columns:
            if col != col_etab and col != "Horodateur" and col != "Colonne 2":
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        # --- CALCUL AUTOMATIQUE ET AGRÉGATION DYNAMIQUE ---
        # On prépare les règles de calcul pour le regroupement
        rules = {}
        for col in df.columns:
            if col != col_etab and col != "Horodateur" and col != "Colonne 2":
                if col_eff and col == col_eff:
                    rules[col] = "max"  # On prend l'effectif max de l'établissement (on ne l'additionne pas entre les lignes !)
                else:
                    rules[col] = "sum"  # On additionne automatiquement toutes les consommations saisies !

        # Regroupement automatique par établissement
        if rules:
            df_grouped = df.groupby(col_etab).agg(rules).reset_index()
            
            # Si les colonnes de calcul global existent, on recalcule le ratio par personne en direct
            if col_total and col_eff:
                df_grouped[col_conso if col_conso else "conso carbone  par personne"] = df_grouped.apply(
                    lambda r: r[col_total] / r[col_eff] if r[col_eff] > 0 else 0, axis=1
                )
                final_conso_col = col_conso if col_conso else "conso carbone  par personne"
            else:
                # Si le fichier est brut, on prend la première colonne numérique disponible pour le classement
                final_conso_col = list(rules.keys())[0]
        else:
            df_grouped = df.copy()
            final_conso_col = df.columns[2]

        st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🌱 Réseau Haut Vaucluse</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="inner-title">📊 Classement des Établissements</p>', unsafe_allow_html=True)
            st.dataframe(df_grouped[[col_etab, final_conso_col]].sort_values(final_conso_col, ascending=False), hide_index=True, width="stretch", height=380)
        with col2:
            st.markdown('<p class="inner-title">🚀 Moyenne du Réseau</p>', unsafe_allow_html=True)
            
            # Calcul de la moyenne globale du réseau
            if col_total in df_grouped.columns and col_eff in df_grouped.columns:
                moyenne = df_grouped[col_total].sum() / df_grouped[col_eff].sum() if df_grouped[col_eff].sum() > 0 else 0
                suffixe = " kg/pers"
            else:
                moyenne = df_grouped[final_conso_col].mean()
                suffixe = " u."

            fig = go.Figure(go.Indicator(mode = "gauge+number", value = moyenne, number = {'suffix': suffixe}, gauge = {'axis': {'range': [None, 5000]}, 'bar': {'color': "#1e3d59"}, 'steps': [{'range': [0, 1500], 'color': "#d4edda"}, {'range': [1500, 2500], 'color': "#fff3cd"}, {'range': [2500, 5000], 'color': "#f8d7da"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 2500}}))
            fig.update_layout(height=380, margin=dict(t=30, b=0, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("🔐 Mise à jour des données"):
            pwd = st.text_input("Code secret :", type="password", key="main_pwd")
            if pwd == "CARBONE2026":
                st.link_button("🚀 Ouvrir le formulaire", "https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform")
        
        st.markdown('<p class="inner-title">📋 Liste Complète des Saisies Brutes (Formulaire)</p>', unsafe_allow_html=True)
        st.dataframe(df, hide_index=True, width="stretch")

# --- ONGLET GLOSSAIRE (Avec Anecdotes & Méthodes) ---
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
        st.markdown('<div class="methode"><b>📝 Méthode :</b> On multiplie le nombre de repas servis par l\'empreinte de production des ingrédients.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>💡 Le saviez-vous ?</b> Manger 1 seul steak de bœuf émet autant de CO2 que de parcourir 32 km en voiture ! À l\'inverse, un repas végétarien équivaut à seulement 2 km.</div>', unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("Pôle Énergie & Fluides")
        st.write("- **Électricité :** 0.06 kgCO2e / kWh")
        st.write("- **Gaz Naturel :** 0.227 kgCO2e / kWh")
        st.write("- **Climatisation (R410A) :** 2088 kgCO2e / kg")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Consommation réelle des compteurs. Pour la clim, on mesure la recharge de gaz (1kg rajouté = 1kg de fuite polluante).</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>❄️ L\'anecdote glaçante :</b> 1 kg de fuite de clim = 10 000 km en voiture (un aller-retour Paris-Pékin) ! L\'entretien est vital.</div>', unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("Pôle Transports")
        st.write("- **Autocar Scolaire :** 0.030 kgCO2e / km / élève")
        st.write("- **Voiture thermique :** 0.218 kgCO2e / km")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Distance parcourue x facteur d\'émission / nombre de passagers.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>🚌 Union :</b> Venir en bus scolaire permet de retirer virtuellement 43 voitures de la route.</div>', unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("Pôle Déchets Alimentaires")
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            st.metric("Assiette jetée (moyenne)", "1.20 kg", "CO2e / kg jeté")
        with c_d2:
            st.metric("Gaspillage Pain", "0.63 kg", "CO2e / kg jeté")
        st.markdown('<div class="methode"><b>📝 Méthode :</b> Pesée des restes. L\'assiette est lourde en carbone car elle contient des produits transformés (viande, sauces) qui ont déjà coûté cher à produire.</div>', unsafe_allow_html=True)
        st.markdown('<div class="anecdote"><b>🍽️ L\'assiette fantôme :</b> Jeter 1 kg d\'assiettes pleines émet autant que de fabriquer 6 bouteilles en plastique ou de recharger un smartphone 150 fois !</div>', unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("Pôle Biens & Consommables")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.write("**Papier et Fin de vie :**")
            st.write("- **Ramette A4 neuve :** 2.62 kgCO2e")
            st.write("- **Papier jeté (poubelle grise) :** 0.45 kgCO2e / kg")
            st.write("- **Papier trié (recyclage) :** 0.02 kgCO2e / kg")
        with col_b2:
            st.write("**Équipements (Fabrication) :**")
            st.write("- **Photocopieur :** 850 kgCO2e")
            st.write("- **Ordinateur Portable :** 161 kgCO2e")
            st.write("- **Vidéoprojecteur :** 94 kgCO2e")
        
        st.markdown("""
        <div class="methode">
        <b>📝 Méthode ADEME :</b><br>
        On mesure la <b>FABRICATION</b> (énergie grise) pour le matériel durable. 80% de l'impact d'un ordi a lieu avant sa première utilisation ! Pour le papier, on cumule l'achat et le mode de traitement (tri ou non).
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="anecdote">
        <b>📄 Forêt de papier :</b> 1000 ramettes/an = une forêt de 10 arbres consommée. Trier le papier divise son impact par 20 !<br>
        <b>📹 Focus Vidéo :</b> Fabriquer un projecteur émet autant que 750 brosses à dents. L'éteindre économise l'énergie de 20 smartphones par heure.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("Sources : Méthodologie ADEME / GIEC / PEBC - Mise à jour Mai 2026")
