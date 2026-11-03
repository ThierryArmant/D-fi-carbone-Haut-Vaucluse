# Interface de saisie : panneau opaque et consignes simplifiées.
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os
import html
import unicodedata
from saisie_carbone import afficher_saisie_carbone

# 1. CONFIGURATION INITIALE DE LA PAGE
st.set_page_config(page_title="Défi Carbone - Haut Vaucluse", page_icon="🌱", layout="wide")

# Moteur de recherche absolu pour ton fichier "image_1" à la racine
def get_base64_image(file_name_without_ext):
    current_dir = os.path.dirname(__file__)
    for ext in ["", ".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
        path = os.path.join(current_dir, file_name_without_ext + ext)
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return ""

# Chargement immédiat de la ressource image pour écarter les NameError
img_base64 = get_base64_image("image_1")

# 2. INJECTION DU FILTRE GLASSMORPHISM UNIVERSEL
def inject_glass_theme(img_b64):
    background = (
        f"url('data:image/jpeg;base64,{img_b64}')"
        if img_b64 else "linear-gradient(135deg, #12372b, #102b36)"
    )
    st.markdown(
        f"<style>[data-testid='stAppViewContainer'] {{background-image: {background}; background-size: cover; background-position: center; background-attachment: fixed;}}</style>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <style>
    .stApp, [data-testid="stMain"] { background: transparent; }
    [data-testid="stMainBlockContainer"], .main .block-container {
        max-width: 1000px !important; width: 100% !important;
        margin-left: 0 !important; margin-right: auto !important; padding: 1rem 1.1rem 2.5rem !important;
    }
    [data-testid="stHeader"] { background: transparent; }
    h1, h2, h3, h4, h5, h6, .stMarkdown p,
    [data-testid="stWidgetLabel"] p, summary { color: #f3f8f5 !important; }
    h1, h2, h3, h4, h5, h6, [data-heading-text] { color: #f3f8f5 !important; }
    [role="tab"] p { color: #e6f0e9 !important; font-weight: 600; }
    [role="tab"][aria-selected="true"] p { color: #123a29 !important; }
    [role="tab"] { flex-shrink: 0; cursor: pointer; }
    h1 { font-size: clamp(1.8rem, 3vw, 2.5rem) !important; line-height: 1.15 !important; }
    h2 { font-size: 1.3rem !important; margin-top: 1rem !important; }
    .stMarkdown p { font-weight: 400; line-height: 1.6; }
    div[data-testid="stColumn"] {
        background: rgba(14, 35, 29, 0.38); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,.16);
        border-radius: 11px; padding: 11px; min-width: 0;
    }
    div[role="tablist"], div[data-baseweb="tab-list"] {
        position: static !important; top: auto !important; right: auto !important;
        width: 100% !important; gap: 5px !important; margin: 7px 0 12px !important;
        background: transparent !important; overflow-x: auto !important;
    }
    [role="tablist"] [role="tab"] {
        color: #e6f0e9 !important; background: rgba(14,35,29,.90) !important;
        border: 1px solid rgba(255,255,255,.25) !important; border-radius: 9px !important;
        padding: 7px 10px !important; min-height: 36px !important; font-size: 12px !important;
    }
    [role="tablist"] [role="tab"][aria-selected="true"] {
        background: #c8e8d4 !important; color: #123a29 !important; border-color: #c8e8d4 !important;
    }
    [role="tablist"] [role="tab"][aria-selected="true"] p { color: #123a29 !important; }
    div[data-testid="stExpander"] {
        background: rgba(10,28,23,.86); border: 1px solid rgba(255,255,255,.20);
        border-radius: 10px; margin: 8px 0 14px;
    }
    div[data-testid="stExpander"] summary svg { color: #f3f8f5; fill: #f3f8f5; }
    .inner-title { color: #a9dded !important; font-weight: 700; font-size: 15px; margin: 0 0 12px; }
    .pole-header, .sub-pole-header {
        display: flex; justify-content: space-between; flex-wrap: wrap; gap: 6px;
        color: #f3f8f5; font-weight: 600; font-size: 15px; margin: 6px 0;
    }
    .sub-pole-header { font-size: 14px; }
    .bar-container, .sub-bar-container { background: rgba(255,255,255,.14); height: 10px; border-radius: 6px; overflow: hidden; margin-bottom: 12px; }
    .sub-bar-container { height: 7px; }
    .unit-box { background: rgba(255,255,255,.08); color: #f3f8f5; border: 1px solid rgba(255,255,255,.20); border-radius: 9px; padding: 9px 11px; font-size: 13px; line-height: 1.5; margin: 7px 0; }
    .anecdote { background: rgba(34,140,168,.17); color: #f3f8f5; border-left: 4px solid #73c7df; border-radius: 6px; padding: 9px 11px; font-size: 13px; line-height: 1.5; margin: 7px 0; }
    .js-plotly-plot .plotly .main-svg { background: transparent !important; }
    hr { border-color: rgba(255,255,255,.20); margin: 24px 0; }
    [data-testid="stCaptionContainer"] p { color: #d0e1d5 !important; font-size: 13px; }
    @media (max-width: 760px) {
        [data-testid="stMainBlockContainer"], .main .block-container { padding: 1rem .85rem 3rem !important; }
        [data-testid="stHorizontalBlock"] { flex-direction: column !important; gap: 16px !important; }
        div[data-testid="stColumn"] { width: 100% !important; flex: 1 1 100% !important; padding: 14px; }
        [role="tablist"] [role="tab"] { padding: 9px 12px !important; font-size: 13px !important; }
        #eco-navigation { margin-bottom: 20px; }
    }
    h1, h2, h3, [data-testid="stMarkdownContainer"] > p { text-shadow: 0 1px 4px rgba(0,0,0,.85); }
    @media (min-width: 1100px) {
        [data-testid="stMainBlockContainer"], .main .block-container {
            width: min(64%, 950px) !important; max-width: 950px !important;
            margin-left: 1.5% !important; margin-right: auto !important;
            padding-left: .75rem !important; padding-right: .75rem !important;
        }
    }
    .comparison-sector {
        background: rgba(10, 28, 23, .88); border: 1px solid rgba(255,255,255,.24);
        border-radius: 10px; padding: 9px 12px; margin: 7px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,.17);
    }
    .comparison-title { font-weight: 800; color: #fff; font-size: 15px; margin-bottom: 6px; }
    .comparison-grid { display:grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 10px; }
    .comparison-label { font-size: 12px; color: #cde7db; margin-bottom: 3px; }
    .comparison-value { color:#fff; font-size:clamp(13px,1.25vw,17px); font-weight:800; font-variant-numeric:tabular-nums; }
    .comparison-track { height:8px; border-radius:99px; overflow:hidden; background:rgba(255,255,255,.19); margin:5px 0 3px; }
    .comparison-fill { height:100%; border-radius:99px; }
    .comparison-ratio { font-size:11px; color:#d4e4dc; }
    .comparison-summary { background:rgba(10,28,23,.88); border:1px solid rgba(255,255,255,.24); border-radius:10px; padding:9px 12px; margin:7px 0 10px; color:#fff; }
    .comparison-detail { display:flex; justify-content:space-between; gap:12px; padding:6px 0; border-bottom:1px solid rgba(255,255,255,.09); color:#fff; font-size:13px; }
    .comparison-detail span:last-child { font-weight:700; font-variant-numeric:tabular-nums; text-align:right; }
    @media(max-width:640px) { .comparison-grid { grid-template-columns:1fr; gap:12px; } .comparison-sector { padding:12px; } }
    .unit-box, .anecdote {
        background: rgba(10, 28, 23, .88) !important;
        color: #ffffff !important; backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px); box-shadow: 0 4px 16px rgba(0,0,0,.18);
    }
    .unit-box { border: 1px solid rgba(255,255,255,.30); }
    .anecdote { border-left: 4px solid #73c7df; }
    .st-key-navigation_collecte { background: #f7faf8; border: 1px solid #ceded5; border-radius: 9px; padding: 5px 7px; margin-bottom: 9px; }
    .st-key-navigation_collecte [data-testid="stColumn"] { background: transparent !important; backdrop-filter: none !important; border: 0 !important; padding: 0 !important; }
    .st-key-navigation_collecte #eco-navigation { background: transparent !important; border: 0 !important; margin: 0 !important; padding: 0 !important; gap: 4px !important; }
    .st-key-navigation_collecte #eco-navigation a { font-size: 11px; padding: 8px 9px; }
    .st-key-navigation_collecte #eco-navigation span { font-size: 11px; padding: 8px 9px !important; }
    .st-key-navigation_collecte [data-testid="stTextInput"] { margin: 0; }
    .intro-carbone { color: #fff; background: rgba(10,28,23,.82); border-radius: 9px; padding: 8px 11px; font-size: 13px; line-height: 1.45; }
    @media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; } }
    </style>
    """, unsafe_allow_html=True)

inject_glass_theme(img_base64)

# Navigation commune aux trois espaces du projet.
with st.container(key="navigation_collecte"):
    acces_col, code_col = st.columns([4, 1.2], gap="small", vertical_alignment="center")
    with acces_col:
        st.markdown('''<style id="eco-navigation-style">#eco-navigation{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:9px 12px;margin:0 0 16px;background:#f7faf8;color:#173e30;border:1px solid #ceded5;border-radius:10px;font:600 13px/1.3 system-ui,sans-serif;flex-shrink:0}#eco-navigation a{display:block;padding:9px 12px;border-radius:7px;color:#234b3b;text-decoration:none;white-space:normal}#eco-navigation a:hover,#eco-navigation a:focus-visible{background:#e1ede5;outline:2px solid #39785a;outline-offset:1px}#eco-navigation a[aria-current="page"]{background:#215e44;color:white}.main-container>#eco-navigation{margin:0;border-radius:0;border:0;border-bottom:1px solid #ceded5}@media print{#eco-navigation{display:none!important}}@media(max-width:600px){#eco-navigation{gap:3px;padding:6px;font-size:11px}#eco-navigation a{padding:8px}}#eco-navigation a:first-of-type{background:#eef1ef;color:#43534b}#eco-navigation a:first-of-type[aria-current="page"]{background:#d3dad6;color:#213d2e}#eco-navigation a:nth-of-type(2){background:#e0f2e3;color:#215e44;border-bottom:3px solid #3e7b4f}#eco-navigation a:nth-of-type(3){background:#fbefd5;color:#795217;border-bottom:3px solid #bf8b2e}#eco-navigation a:nth-of-type(4){background:#e3edfa;color:#234f79;border-bottom:3px solid #2f5d8a}#eco-navigation a:nth-of-type(2)[aria-current="page"]{background:#215e44;color:#fff}#eco-navigation a:nth-of-type(3)[aria-current="page"]{background:#93681e;color:#fff}#eco-navigation a:nth-of-type(4)[aria-current="page"]{background:#2f5d8a;color:#fff}</style><nav id="eco-navigation" aria-label="Changer d’espace"><a target="_blank" rel="noopener noreferrer" href="https://thierryarmant.github.io/Le-coin-des-ecodelegues/">Accueil</a><a target="_blank" rel="noopener noreferrer" href="https://thierryarmant.github.io/Le-coin-des-ecodelegues/cantine/">Planning</a><a target="_blank" rel="noopener noreferrer" href="https://thierryarmant.github.io/E3D-cantine/">A.B.C. Cantine Bas Carbone</a><span aria-current="page" title="Vous êtes dans les enquêtes" style="display:block;padding:9px 12px;border-radius:7px;background:#2f5d8a;color:white;font-weight:700">Enquêtes</span></nav>''', unsafe_allow_html=True)
    with code_col:
        code_saisie = st.text_input("Code d’accès saisies", type="password", key="main_pwd", label_visibility="collapsed", placeholder="Code d’accès saisies")


# 3. INTERFACE DE CONSTRUCTION DES JAUGE ADEME
def format_kg_co2e(value):
    """Unité unique pour les résultats carbone, sans conversion en tonnes."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0.0
    decimals = 1 if abs(number) < 10 and number != 0 else 0
    return f"{number:,.{decimals}f}".replace(",", "\u00a0").replace(".", ",") + " kg CO₂e"


def draw_custom_bar(label, value_kg, total_kg, color, is_sub=False):
    pct = (value_kg / total_kg * 100) if total_kg > 0 else 0
    display_weight = format_kg_co2e(value_kg)
    
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

# 4. TUNNEL D'ACCÈS GOOGLE SHEETS
votre_gid = "169103083" 
url = f"https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid={votre_gid}"

@st.cache_data(ttl=30)
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
        st.error(f"Erreur de synchronisation Google Sheets : {e}")
    return pd.DataFrame()

df = load_data()

@st.cache_data(ttl=60)
def load_import_abc():
    """Lecture seule de l'import des repas A.B.C., commun à tous les établissements."""
    url_abc = ("https://docs.google.com/spreadsheets/d/"
               "12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/"
               "export?format=csv&gid=2124365883")
    try:
        source = pd.read_csv(url_abc, dtype=str).fillna("")
        source.columns = [" ".join(str(c).split()) for c in source.columns]
        return source
    except Exception:
        return pd.DataFrame()

import_abc = load_import_abc()

def _normaliser_colonne(nom):
    txt = unicodedata.normalize("NFD", str(nom or "").casefold())
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")
    return " ".join(txt.split())


def _colonne_disponible(columns, nom):
    # Libellés historiques présents dans le Google Sheets : une seule source par poste.
    aliases = {
        "papier": ["Papier en kg 1 ramette = 2,5kg", "Paper"],
        "paper": ["Papier en kg 1 ramette = 2,5kg", "Papier"],
        "fioul de chauffage": ["Fioul"],
        "fioul": ["Fioul de chauffage"],
    }
    candidats = [nom] + aliases.get(_normaliser_colonne(nom), [])
    colonnes = {_normaliser_colonne(c): c for c in columns}
    for candidat in candidats:
        trouve = colonnes.get(_normaliser_colonne(candidat))
        if trouve is not None:
            return trouve
    return None


def _nombre_carbone(value):
    """Lit les décimales françaises sans transformer les erreurs en valeurs inventées."""
    if pd.isna(value) or str(value).strip() == "":
        return 0.0
    chaine = str(value).replace("\u00a0", "").replace("\u202f", "").replace(" ", "").strip()
    if "," in chaine:
        chaine = chaine.replace(".", "").replace(",", ".")
    try:
        resultat = float(chaine)
        return resultat if pd.notna(resultat) and abs(resultat) != float("inf") else 0.0
    except (ValueError, TypeError):
        return 0.0


def safe_get_val(row_data, col_name):
    col = _colonne_disponible(row_data.index, col_name)
    return _nombre_carbone(row_data[col]) if col is not None else 0.0


def safe_sum_val(dataframe, col_name):
    col = _colonne_disponible(dataframe.columns, col_name)
    return float(dataframe[col].sum()) if col is not None else 0.0

if not df.empty:
    df.columns = [str(c).replace('\xa0', ' ').replace('\n', ' ').strip() for c in df.columns]
    df.columns = [" ".join(c.split()) for c in df.columns]

# Accès rapide : relire les données sans modifier les réponses des établissements.
st.title("Défi Carbone · Haut Vaucluse")
st.markdown('''<div class="intro-carbone">Explorez les consommations des établissements, comparez les postes d’émission et retrouvez les repères pour les élèves.</div>''', unsafe_allow_html=True)
zone_saisie = st.container()
if st.button("↻ Actualiser les données", key="actualiser_donnees"):
    load_data.clear()
    st.cache_data.clear()
    st.rerun()
if df.empty:
    st.info("Aucune donnée disponible pour le moment. Vous pouvez consulter le référentiel et réessayer avec le bouton Actualiser.")

with zone_saisie:
    if code_saisie == "CARBONE2026":
        if afficher_saisie_carbone(df):
            load_data.clear()
    elif code_saisie:
        st.caption("Code de saisie non reconnu.")


@st.cache_data(ttl=30)
def charger_historique():
    lien = 'https://docs.google.com/spreadsheets/d/12fo8cluTH5DmI1dZJh2P_iJaso-NmplnEvxcyb5pS0M/export?format=csv&gid=717694895'
    return pd.read_csv(lien, dtype=str)

def afficher_suivi():
    st.subheader('Suivi par période')
    st.caption('Filtres sur la date d’envoi des réponses. Une facture annuelle saisie aujourd’hui reste rattachée à cet envoi, pas répartie sur les jours consommés. Le bilan général conserve son cumul complet.')
    try:
        historique = charger_historique().copy()
    except Exception:
        st.warning('Les réponses datées sont momentanément indisponibles. Réessayez avec Actualiser les données.')
        return
    if historique.empty or historique.shape[1] < 4:
        st.info('Aucune réponse datée disponible.')
        return
    historique.columns = [' '.join(str(c).split()) for c in historique.columns]
    date_col, ecole_col = historique.columns[:2]
    dates = pd.to_datetime(historique[date_col], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    invalides = int(dates.isna().sum())
    historique['_date'] = dates
    historique = historique.dropna(subset=['_date'])
    if invalides:
        st.warning(f'{invalides} réponse(s) sans date valide exclue(s) de ce suivi uniquement.')
    if historique.empty:
        st.info('Aucune date exploitable dans les réponses.')
        return
    etablissements = sorted(historique[ecole_col].dropna().unique())
    choix = st.selectbox('Établissement du suivi', ['Tous les établissements'] + etablissements, key='suivi_ecole')
    if choix != 'Tous les établissements':
        historique = historique[historique[ecole_col] == choix].copy()
    mode = st.selectbox('Période', ['Tout le cumul', 'Jour', 'Semaine', 'Mois', 'Année'], key='suivi_mode')
    debut = fin = None
    if mode != 'Tout le cumul':
        repere = pd.Timestamp(st.date_input('Date de référence', value=historique['_date'].max().date(), key='suivi_date'))
        if mode == 'Jour':
            debut, fin = repere, repere + pd.Timedelta(days=1)
        elif mode == 'Semaine':
            debut = repere - pd.Timedelta(days=repere.weekday())
            fin = debut + pd.Timedelta(days=7)
        elif mode == 'Mois':
            debut = repere.replace(day=1)
            fin = debut + pd.offsets.MonthBegin(1)
        else:
            debut = repere.replace(month=1, day=1)
            fin = debut + pd.offsets.YearBegin(1)
        historique = historique[(historique['_date'] >= debut) & (historique['_date'] < fin)].copy()
        st.write(f'Du {debut:%d/%m/%Y} au {(fin - pd.Timedelta(days=1)):%d/%m/%Y}')
    st.write(f'{len(historique)} réponse(s) dans la sélection')
    if historique.empty:
        st.info('Aucune saisie pour cette période et cet établissement.')
        return
    # Champs de consommation : exclure l’option sans libellé et les anciennes questions 2025.
    indices = list(range(3, min(21, len(historique.columns)-1))) + [i for i in (23, 24) if i < len(historique.columns)-1]
    champs = [historique.columns[i] for i in indices]
    nombres = pd.DataFrame(index=historique.index)
    for champ in champs:
        texte = historique[champ].astype('string').str.replace(r'\s+', '', regex=True).str.replace(',', '.', regex=False)
        nombres[champ] = pd.to_numeric(texte, errors='coerce')
    resume = pd.DataFrame({'Donnée (unité du formulaire)': champs, 'Cumul': [nombres[c].sum(min_count=1) for c in champs], 'Réponses renseignées': [int(nombres[c].count()) for c in champs]})
    st.dataframe(resume, hide_index=True, width='stretch')
    st.caption('Une case vide reste non renseignée. Les unités ne sont pas additionnées entre elles. Ces quantités ne sont pas une nouvelle estimation carbone.')
    indicateur = st.selectbox('Consommation à afficher', champs, key='suivi_indicateur')
    rythme = st.selectbox('Regrouper le graphique par', ['Jour', 'Semaine', 'Mois', 'Année'], key='suivi_rythme')
    frequence = {'Jour': 'D', 'Semaine': 'W-SUN', 'Mois': 'M', 'Année': 'Y'}[rythme]
    periodes = historique['_date'].dt.to_period(frequence).dt.start_time
    serie = nombres[indicateur].groupby(periodes).sum(min_count=1)
    if serie.notna().any():
        st.bar_chart(serie.rename(indicateur))
    else:
        st.info('Cette consommation n’est pas renseignée dans la sélection.')
    export = historique.drop(columns=['_date'])
    st.download_button('Télécharger les réponses filtrées', export.to_csv(index=False, sep=';').encode('utf-8-sig'), 'reponses_filtrees.csv', 'text/csv', key='export_suivi')
    with st.expander('Voir les réponses de la sélection'):
        st.dataframe(export, hide_index=True, width='stretch')


st.markdown('''<style>.st-key-suivi_lisible {background:#102c25;padding:22px;border-radius:12px;color:white}.st-key-suivi_lisible p,.st-key-suivi_lisible h3 {color:white!important}</style>''', unsafe_allow_html=True)

# 5. INITIALISATION DES ONGLETS DE NAVIGATION
tab_dashboard, tab_suivi, tab_conso_graph, tab_glossaire = st.tabs(["📊 Tableau de bord", "📅 Suivi par période", "🌱 Comparer les établissements", "📖 Référentiel élèves"])

with tab_suivi:
    with st.container(key="suivi_lisible"):
        afficher_suivi()

# ==========================================
# ---          1. ONGLET DASHBOARD       ---
# ==========================================
with tab_dashboard:
    if not df.empty:
        col_etab = "Etablissements" if "Etablissements" in df.columns else df.columns[0]
        col_total = "Total émissions" if "Total émissions" in df.columns else df.columns[7]
        col_eff = "Effectif total" if "Effectif total" in df.columns else df.columns[1]
        col_conso = "conso carbone par personne" if "conso carbone par personne" in df.columns else df.columns[8]

        cols_to_convert = [c for c in df.columns if c not in (col_etab, "Statut")]
        for col in cols_to_convert:
            df[col] = df[col].map(_nombre_carbone)
        
        df_active = df[df[col_etab].astype(str).str.strip() != ""].copy()
        df_active = df_active[~df_active[col_etab].astype(str).str.lower().str.contains("total|moyenne")].copy()

        st.subheader("Vue d’ensemble du réseau")
        

        col_top1, col_top2 = st.columns([1, 1])
        with col_top1:
            st.markdown('<p class="inner-title">📊 Classement des établissements (kg CO₂e/personne)</p>', unsafe_allow_html=True)
            if not df_active.empty:
                df_ranking = df_active[[col_etab, col_conso]].sort_values(col_conso, ascending=False)
                recherche_etab = st.text_input("Rechercher un établissement", placeholder="Nom du collège, lycée ou école", key="recherche_classement")
                if recherche_etab.strip():
                    df_ranking = df_ranking[df_ranking[col_etab].astype(str).str.contains(recherche_etab.strip(), case=False, regex=False, na=False)]
                st.dataframe(df_ranking, hide_index=True, width="stretch", height=300)
            else:
                st.info("En attente de données...")
                
        with col_top2:
            st.markdown('<p class="inner-title">🌍 Moyenne du réseau (kg CO₂e/personne)</p>', unsafe_allow_html=True)
            if not df_active.empty and df_active[col_eff].sum() > 0:
                moyenne = df_active[col_total].sum() / df_active[col_eff].sum()
            else:
                moyenne = 0

            fig = go.Figure(go.Indicator(
                mode = "gauge+number", 
                value = moyenne, 
                domain = {'x': [0.1, 0.9], 'y': [0, 1]},
                number = {
                    'suffix': " kg CO₂e/pers", 
                    'font': {'color': '#f1f5f9', 'size': 18}
                }, 
                gauge = {
                    'axis': {'range': [None, 2000], 'tickfont': {'color': '#cbd5e1', 'size': 9}}, 
                    'bar': {'color': "#22d3ee"}, 
                    'steps': [{'range': [0, 500], 'color': "rgba(34, 197, 94, 0.25)"}, {'range': [500, 1000], 'color': "rgba(249, 115, 22, 0.25)"}, {'range': [1000, 2000], 'color': "rgba(239, 68, 68, 0.25)"}], 
                    'threshold': {'line': {'color': "red", 'width': 3}, 'value': 1000}
                }
            ))
            fig.update_layout(height=240, margin=dict(t=20, b=5, l=5, r=5), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        st.markdown("<h2 style='text-align: center; color: #22d3ee; margin-bottom: 5px;'>🔍 Comparer l'établissement au réseau</h2>", unsafe_allow_html=True)

        if not df_active.empty:
            selected_school = st.selectbox(
                "Établissement à comparer",
                df_active[col_etab].unique(),
                key="left_school_selector",
            )
            school_data = df_active[df_active[col_etab] == selected_school].iloc[0]
            tot_sch = float(school_data[col_total])
            tot_net = float(df_active[col_total].sum())
            nb_contributeurs = int((df_active[col_total] > 0).sum())
            nb_etablissements = len(df_active)
            nb_a_valider = int(
                (df_active.loc[df_active[col_total] > 0, "Statut"].astype(str).str.casefold().str.contains("valider")).sum()
            ) if "Statut" in df_active.columns else 0

            # Une école est rattachée à A.B.C. uniquement si le nom du bilan
            # correspond et si au moins une journée a réellement été mesurée.
            abc_mesures = pd.DataFrame()
            if not import_abc.empty and {"Nom dans le bilan", "Jours mesurés"}.issubset(import_abc.columns):
                abc_mesures = import_abc.copy()
                abc_mesures["Jours mesurés"] = pd.to_numeric(
                    abc_mesures["Jours mesurés"].astype(str).str.replace(",", ".", regex=False),
                    errors="coerce",
                ).fillna(0)
                abc_mesures = abc_mesures[abc_mesures["Jours mesurés"] > 0].copy()
                abc_mesures["Nom dans le bilan"] = abc_mesures["Nom dans le bilan"].astype(str).str.strip()

            nom_ecole = html.escape(str(selected_school))
            if not abc_mesures.empty:
                ecole_abc = abc_mesures[
                    abc_mesures["Nom dans le bilan"] == str(selected_school).strip()
                ]
                if not ecole_abc.empty:
                    n_jours = int(ecole_abc["Jours mesurés"].sum())
                    st.caption(
                        f"🍽️ Source des cinq catégories de repas : A.B.C. "
                        f"({n_jours} jour(s) mesuré(s)). Le formulaire historique n'est pas additionné."
                    )
                else:
                    st.caption(
                        "🍽️ Source des catégories de repas : formulaire historique "
                        "(en attendant des journées mesurées et rattachées dans A.B.C.)."
                    )

            st.markdown(
                f'<div class="comparison-summary"><strong>🏫 {nom_ecole}</strong> : '
                f'{format_kg_co2e(tot_sch)}<br>'
                f'<strong>🌍 Ensemble du réseau</strong> : {format_kg_co2e(tot_net)}<br>'
                f'<small>{nb_contributeurs} établissement(s) avec émissions renseignées sur '
                f'{nb_etablissements} établissement(s) listés.'
                + (f' {nb_a_valider} bilan(s) encore à valider.' if nb_a_valider else '')
                + '</small></div>',
                unsafe_allow_html=True,
            )

            # Les cinq catégories sont exclusives ; le « repas moyen » désigne les autres repas.
            facteurs_repas = {
                "Repas viande rouge": 7.26,
                "Repas viande blanche": 1.58,
                "Repas Poisson": 2.00,
                "Repas végétarien": 0.51,
                "Repas moyen": 2.25,
            }
            # Les colonnes voisines du tableur alternent émissions (kg CO₂e) et quantités (repas).
            # On vérifie la cohérence sans recalculer ni écraser les résultats du Google Sheets.
            colonnes_repas = list(df_active.columns)
            anomalies_repas = []
            for nom_repas, facteur in facteurs_repas.items():
                col_emission = _colonne_disponible(colonnes_repas, nom_repas)
                if col_emission is None:
                    anomalies_repas.append(f"{nom_repas} : colonne d’émissions absente")
                    continue
                idx = colonnes_repas.index(col_emission)
                if idx + 1 >= len(colonnes_repas):
                    anomalies_repas.append(f"{nom_repas} : colonne du nombre de repas absente")
                    continue
                emission = safe_get_val(school_data, nom_repas)
                quantite = _nombre_carbone(school_data.iloc[idx + 1])
                attendu = quantite * facteur
                if abs(emission - attendu) > max(0.1, 0.001 * abs(attendu)):
                    anomalies_repas.append(
                        f"{nom_repas} : {format_kg_co2e(emission)} affichés "
                        f"pour {quantite:g} repas, contre {format_kg_co2e(attendu)} attendus"
                    )
            if anomalies_repas:
                with st.expander("⚠️ Vérification des cinq catégories de repas"):
                    for anomalie in anomalies_repas:
                        st.warning(anomalie)

            secteurs = [
                ("❄️ Énergie & Bâtiments", "#4ade80", [
                    ("Électricité", "Electricité française"),
                    ("Gaz naturel", "Gaz Naturel"),
                    ("Fioul de chauffage", "Fioul"),
                ]),
                ("🍎 Alimentation & Cantine", "#fb923c", [
                    ("Repas viande rouge", "Repas viande rouge"),
                    ("Repas poisson", "Repas Poisson"),
                    ("Repas standard moyen", "Repas moyen"),
                    ("Repas végétarien", "Repas végétarien"),
                    ("Repas viande blanche", "Repas viande blanche"),
                ]),
                ("🚌 Déplacements & Transports", "#60a5fa", [
                    ("Voiture à essence", "Voiture à essence"),
                    ("Autobus en ville", "Autobus (ville)"),
                    ("Autobus (sorties scolaires)", "Autobus (sortie scolaire)"),
                ]),
                ("📦 Biens & Équipements", "#c084fc", [
                    ("Papier", "Papier"),
                    ("Plastique", "Plastique"),
                    ("Carton", "Carton"),
                    ("Ordinateurs", "Ordinateur à écran plat"),
                    ("Imprimantes", "Imprimante"),
                    ("Photocopieurs", "Photocopieurs"),
                    ("Vidéoprojecteurs", "Vidéo projecteur"),
                ]),
                ("🗑️ Élimination des déchets", "#818cf8", [
                    ("Papier / carton", "Déchets Papier"),
                    ("Déchets alimentaires", "Déchets alimentaire"),
                    ("Déchets plastiques", "Déchets plastique"),
                ]),
            ]

            somme_ecole = 0.0
            somme_reseau = 0.0
            for titre, couleur, champs in secteurs:
                details = [
                    (libelle, safe_get_val(school_data, colonne), safe_sum_val(df_active, colonne))
                    for libelle, colonne in champs
                ]
                kg_ecole = sum(x[1] for x in details)
                kg_reseau = sum(x[2] for x in details)
                somme_ecole += kg_ecole
                somme_reseau += kg_reseau
                ratio_ecole = (100 * kg_ecole / tot_sch) if tot_sch > 0 else 0
                ratio_reseau = (100 * kg_reseau / tot_net) if tot_net > 0 else 0

                def colonne_comparaison(libelle, kg, ratio):
                    largeur = max(0, min(100, ratio))
                    return (
                        f'<div><div class="comparison-label">{libelle}</div>'
                        f'<div class="comparison-value">{format_kg_co2e(kg)}</div>'
                        f'<div class="comparison-track"><div class="comparison-fill" '
                        f'style="width:{largeur:.1f}%;background:{couleur}"></div></div>'
                        f'<div class="comparison-ratio">{ratio:.1f} % de l’empreinte totale</div></div>'
                    )

                st.markdown(
                    f'<div class="comparison-sector">'
                    f'<div class="comparison-title">{titre}</div>'
                    f'<div class="comparison-grid">'
                    + colonne_comparaison("🏫 Établissement", kg_ecole, ratio_ecole)
                    + colonne_comparaison("🌍 Réseau", kg_reseau, ratio_reseau)
                    + '</div></div>',
                    unsafe_allow_html=True,
                )
                details_actifs = [x for x in details if x[1] != 0 or x[2] != 0]
                if details_actifs:
                    with st.expander(f"🔎 Détails · {titre}"):
                        st.caption("Valeurs établissement et réseau, calculées à partir des mêmes postes.")
                        for libelle, individuel, global_ in details_actifs:
                            st.markdown(
                                '<div class="comparison-detail"><span>'
                                + html.escape(libelle)
                                + '</span><span>🏫 ' + format_kg_co2e(individuel)
                                + ' · 🌍 ' + format_kg_co2e(global_)
                                + '</span></div>',
                                unsafe_allow_html=True,
                            )

            st.caption(
                "Restauration : cinq catégories exclusives (viande rouge, viande blanche, poisson, "
                "végétarien, repas moyen). Le tableur privilégie A.B.C. lorsqu'une période mesurée "
                "est disponible pour l'établissement ; sinon, il reprend les saisies du formulaire. "
                "Les deux sources ne sont pas additionnées."
            )
            if abs(somme_ecole - tot_sch) > max(1.0, 0.01 * abs(tot_sch)):
                st.warning(
                    f"Écart de ventilation pour {selected_school} : "
                    f"{format_kg_co2e(somme_ecole)} répartis par poste, "
                    f"contre {format_kg_co2e(tot_sch)} dans le total du tableur. "
                    "Vérifier la correspondance des colonnes."
                )
            if abs(somme_reseau - tot_net) > max(1.0, 0.01 * abs(tot_net)):
                st.warning(
                    "Écart de ventilation pour le réseau : "
                    f"{format_kg_co2e(somme_reseau)} répartis par poste, "
                    f"contre {format_kg_co2e(tot_net)} dans le total du tableur."
                )

# ==========================================
# ---    2. ONGLET EMPREINTE CARBONNE    ---
# ==========================================
with tab_conso_graph:
    if not df.empty:
        st.markdown("### 📊 Comparer les établissements")
        st.caption("Empreinte carbone par personne · kg CO₂e/personne")

        # Un établissement sans bilan ne doit pas être interprété comme un bilan à zéro.
        avec_bilan = df_active[df_active[col_total] > 0].copy()
        inclure_absents = st.checkbox(
            "Afficher également les établissements sans bilan renseigné",
            value=False,
            key="comparaison_inclure_absents",
        )
        choix_disponibles = df_active if inclure_absents else avec_bilan
        noms_disponibles = choix_disponibles[col_etab].astype(str).tolist()
        st.caption(
            f"{len(avec_bilan)} établissement(s) avec bilan sur "
            f"{len(df_active)} inscrits dans le réseau."
        )
        if noms_disponibles:
            # Sélection simple par défaut : évite les 19 étiquettes qui occupaient toute la page.
            selection = st.selectbox(
                "Établissement à examiner",
                options=["Tous les établissements affichés"] + noms_disponibles,
                key="comparaison_etablissement",
            )
            if selection == "Tous les établissements affichés":
                df_sorted_graph = choix_disponibles[[col_etab, col_conso, col_total]].copy()
            else:
                df_sorted_graph = choix_disponibles[
                    choix_disponibles[col_etab].astype(str) == selection
                ][[col_etab, col_conso, col_total]].copy()

            df_sorted_graph = df_sorted_graph.sort_values(col_conso, ascending=True)
            if df_sorted_graph.empty:
                st.info("Aucun établissement à afficher.")
            else:
                labels = df_sorted_graph[col_etab].astype(str).str.strip()
                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(
                    y=labels,
                    x=df_sorted_graph[col_conso],
                    orientation="h",
                    marker=dict(color="#42d7d4", line=dict(color="#a9fff3", width=0.6)),
                    text=df_sorted_graph[col_conso].map(lambda v: f"{v:,.1f}".replace(",", " ").replace(".", ",")),
                    textposition="outside",
                    textfont=dict(color="#f4fff9", size=12),
                    cliponaxis=False,
                    customdata=df_sorted_graph[col_total],
                    hovertemplate=(
                        "<b>%{y}</b><br>Par personne : %{x:.1f} kg CO₂e"
                        "<br>Total : %{customdata:,.0f} kg CO₂e<extra></extra>"
                    ),
                ))
                valeur_max = float(df_sorted_graph[col_conso].max())
                fig_bar.update_layout(
                    height=max(270, min(790, 125 + 38 * len(df_sorted_graph))),
                    margin=dict(l=12, r=85, t=20, b=55),
                    paper_bgcolor="rgba(10,30,25,0.95)",
                    plot_bgcolor="rgba(10,30,25,0.95)",
                    font=dict(color="#f4fff9", size=12),
                    bargap=0.30,
                    showlegend=False,
                    xaxis=dict(
                        title="kg CO₂e par personne",
                        color="#f4fff9",
                        gridcolor="rgba(255,255,255,0.16)",
                        zeroline=False,
                        range=[0, max(1, valeur_max * 1.22)],
                    ),
                    yaxis=dict(color="#f4fff9", showgrid=False, automargin=True, tickfont=dict(size=11)),
                )
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
                if inclure_absents:
                    st.caption(
                        "Les établissements sans bilan apparaissent à zéro uniquement "
                        "pour signaler l'absence de données ; ce n'est pas une émission mesurée."
                    )
        else:
            st.info("Aucun établissement ne dispose encore d'un bilan renseigné.")

        st.divider()
        st.markdown('<p class="inner-title" style="color:#38bdf8;">📋 Synthèse du bilan carbone (kg CO₂e)</p>', unsafe_allow_html=True)
        # Les établissements ayant déclaré des émissions apparaissent en premier,
        # par total décroissant. Ceux sans bilan restent visibles ensuite.
        df_synthese = df_active.copy()
        df_synthese["_bilan_renseigne"] = df_synthese[col_total] > 0
        df_synthese = df_synthese.sort_values(
            by=["_bilan_renseigne", col_total, col_etab],
            ascending=[False, False, True],
            kind="stable",
        ).drop(columns=["_bilan_renseigne"])
        st.caption("Établissements avec données en premier, classés par émissions totales décroissantes ; établissements sans bilan ensuite.")
        st.dataframe(df_synthese, hide_index=True, width="stretch", height=360)
        st.download_button("Télécharger le bilan complet (CSV)", data=df_synthese.to_csv(index=False, sep=";").encode("utf-8-sig"), file_name="bilan-carbone-haut-vaucluse.csv", mime="text/csv", key="export_bilan_carbone")

# ==========================================
# ---          3. ONGLET GLOSSAIRE       ---
# ==========================================

with tab_glossaire:
    st.markdown("<h2 style='color: #22d3ee; text-align: center; margin-bottom: 12px;'>📖 Dictionnaire Carbone : Unités & Équivalents Enfants</h2>", unsafe_allow_html=True)
    
    g_tabs = st.tabs(["🍎 Cantine", "❄️ Énergie", "🚌 Transports", "📦 Biens & Équipements", "🗑️ Déchets"])
    
    with g_tabs[0]:
        st.subheader("🍎 Référentiel Restauration (facteurs du tableur réseau)")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Valeurs d\'empreinte de la Cantine :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Repas viande rouge :</b> 7,26 kg CO₂e<br>• <b>Repas viande blanche :</b> 1,58 kg CO₂e<br>• <b>Repas poisson :</b> 2,00 kg CO₂e<br>• <b>Repas végétarien :</b> 0,51 kg CO₂e<br>• <b>Repas moyen (autres repas) :</b> 2,25 kg CO₂e</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>1 seul repas au bœuf (7,2 kg)</b> = Fabriquer une paire de baskets de marque neuve 👟<br>
            • <b>1 seul repas au bœuf</b> = Envoyer 15 000 SMS ou scroller non-stop 150 heures sur TikTok 📱<br>
            • <b>Prendre le repas Végétarien</b> = Économiser le carbone d'un trajet de 30 km en voiture familiale 🚗
            </div>""", unsafe_allow_html=True)

    with g_tabs[1]:
        st.subheader("❄️ Référentiel Énergie & Fluides (facteurs du tableur réseau)")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Facteurs d\'émissions des Bâtiments :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Fioul :</b> 0,324 kg CO₂e/kWh dans la base du tableur (attention : le formulaire demande des litres ; coefficient et conversion à vérifier)<br>• <b>Gaz naturel :</b> 0,243 kg CO₂e/kWh<br>• <b>Électricité française :</b> 0,0647 kg CO₂e/kWh</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>Chauffer une classe au fioul pendant 1 jour</b> = Parcourir 80 km en voiture thermique 🚘<br>
            • <b>Laisser un radiateur tourner avec la fenêtre ouverte 1h</b> = Laisser une console PS5 allumée pendant 6 mois 🎮<br>
            • <b>1 kWh d'Électricité en France (très bas)</b> = Regarder 25 heures de vidéos YouTube en Haute Définition 🎬
            </div>""", unsafe_allow_html=True)

    with g_tabs[2]:
        st.subheader("🚌 Référentiel Déplacements (facteurs du tableur réseau)")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Empreinte des Transports :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Voiture à essence :</b> 0,259 kg CO₂e/km<br>• <b>Bus urbain :</b> 0,182 kg CO₂e/passager-km<br>• <b>Autobus (sortie scolaire) :</b> 3,64 kg CO₂e/km de véhicule</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>Venir au collège à pied ou à vélo à l'année</b> = Économiser la capacité d'absorption de 5 arbres plantés 🌳<br>
            • <b>Un trajet de 15 km en voiture (3,3 kg)</b> = Regarder 30 heures de séries en streaming HD sur sa tablette 📺<br>
            • <b>Partir en voyage scolaire en bus blindé</b> = Diviser par deux sa pollution carbone par rapport au covoiturage 🚌
            </div>""", unsafe_allow_html=True)

    with g_tabs[3]:
        st.subheader("📦 Biens, Consommables & Équipements")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Empreinte du matériel :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Papier :</b> le tableur indique 0,919 kg CO₂e/tonne, unité à vérifier par rapport aux kg saisis<br>• <b>Ordinateur à écran plat :</b> 1 283 kg CO₂e/appareil<br>• <b>Vidéoprojecteur :</b> 94 kg CO₂e/appareil</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>Fabriquer un seul ordinateur portable (250 kg)</b> = Rouler 1200 km en voiture ou fabriquer 150 t-shirts en coton 💻<br>
            • <b>Garder son smartphone 4 ans au lieu de 2 ans</b> = Éviter l'équivalent carbone de 400 repas végétariens 📱<br>
            • <b>Gâcher une ramette de papier blanc (3 kg)</b> = Laisser la lumière de sa chambre allumée pendant 2 mois non-stop 💡
            </div>""", unsafe_allow_html=True)

    with g_tabs[4]:
        st.subheader("🗑️ Gestion des Déchets")
        st.markdown('<p class="inner-title" style="text-align:left;">📊 Empreinte des déchets :</p>', unsafe_allow_html=True)
        st.markdown('<div class="unit-box">• <b>Déchets papier :</b> 0,0431 kg CO₂e/tonne dans la base du tableur (unité à vérifier)<br>• <b>Déchets plastiques :</b> 0,877 kg CO₂e/tonne dans la base (unité à vérifier)<br>• <b>Déchets alimentaires :</b> 0,0481 kg CO₂e/tonne dans la base (unité à vérifier)</div>', unsafe_allow_html=True)
        st.markdown("""<div class="anecdote">
            <b>💡 Équivalents frappants pour un élève :</b><br>
            • <b>Trier 1 kg de bouteilles en plastique (0,30 kg évités)</b> = Économiser l'énergie de 3 cycles complets de machine à laver 🧺<br>
            • <b>Jeter un plateau repas entier à la poubelle</b> = Gaspiller l'équivalent en carbone d'une douche chaude de 6 minutes 🚿<br>
            • <b>Recycler le carton et le papier du collège</b> = Éviter l'incinération directe qui rejette des nuages de CO2 dans l'atmosphère 🗑️
            </div>""", unsafe_allow_html=True)

st.divider()
st.caption("Facteurs affichés : onglet « base emission carbone » du Google Sheets « Projet EPLE bas carbone ». Certains facteurs et unités nécessitent une validation méthodologique avant une utilisation comme référence ADEME.")
