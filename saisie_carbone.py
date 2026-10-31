"""Saisie native raccordée à la collecte Google Forms existante."""
import hashlib
import html
import json
import re
import unicodedata
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.request import Request, urlopen

FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSe6QOMdXWJPYHsbMkq41IyzM7Rc9izcqsFpZhQzWiaqygyykQ/viewform'
POST_URL = FORM_URL.replace('/viewform', '/formResponse')
SCHOOL_ENTRY = '1170300444'
GROUPS = [
    ('Énergie et eau', [
        ('1815777317', "Consommation d'Électricité (kWh)", False),
        ('333378229', 'Consommation de Fioul (Litres)', False),
        ('1807099731', 'Consommation de Gaz Naturel (kWh)', False),
        ('1664098211', 'Consommation d’Eau (m³)', False),
    ]),
    ('Transports', [('1367982532', 'Distance parcourue en bus (sortie scolaire) — km', False)]),
    ('Biens et consommables', [
        ('510769374', 'Quantité de Papier (kg)', False),
        ('1936256727', 'Quantité de Plastique (kg)', False),
        ('424784534', 'Quantité de Carton (kg)', False),
    ]),
    ('Équipements', [
        ('1043216010', "Nombre d'Ordinateurs à écran plat", True),
        ('1810342006', "Nombre d'Imprimantes", True),
        ('1080858499', 'Nombre de Photocopieurs', True),
        ('214723017', 'NOMBRE DE VIDEO PROJECTEURS', True),
    ]),
    ('Déchets', [
        ('260049976', 'Déchets Papier (kg)', False),
        ('390754953', 'Déchets Alimentaires (kg)', False),
        ('1870143307', 'Déchets Plastique (kg)', False),
    ]),
    ('Alimentation', [
        ('976881407', 'Nombre de Repas Moyens', True),
        ('1611570171', 'Nombre de Repas Végétariens', True),
        ('710688540', 'Nombre de Repas Viande Rouge', True),
        ('1948453484', 'Nombre de Repas Viande Blanche', True),
        ('1952739540', 'NOMBRE DE REPAS POISSON', True),
    ]),
]


def parse_number(raw, integer=False):
    """Une case vide reste absente ; zéro est une valeur explicite."""
    value = re.sub(r'\s+', '', str(raw or '')).replace(',', '.')
    if not value:
        return None
    if not re.fullmatch(r'\d+(?:\.\d+)?', value):
        raise ValueError('Indiquez un nombre positif, avec une virgule ou un point.')
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('Nombre non reconnu.') from exc
    if not number.is_finite() or number < 0:
        raise ValueError('La valeur doit être positive ou nulle.')
    if integer and number != number.to_integral_value():
        raise ValueError('Indiquez un nombre entier.')
    return format(number, 'f').replace('.', ',')


def build_payload(school, schools, values):
    if school not in schools:
        raise ValueError('Choisissez un établissement de la liste existante.')
    payload = {'entry.' + SCHOOL_ENTRY: school}
    recap = []
    for _group, fields in GROUPS:
        for entry, label, integer in fields:
            try:
                number = parse_number(values.get(entry, ''), integer)
            except ValueError as exc:
                raise ValueError(label + ' : ' + str(exc)) from exc
            if number is not None:
                payload['entry.' + entry] = number
                recap.append({'Donnée': label, 'Valeur': number})
    if not recap:
        raise ValueError('Renseignez au moins une consommation ou un nombre.')
    return payload, recap


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1

    def handle_data(self, text):
        if not self.hidden:
            self.parts.append(text)


def submission_confirmed(body):
    parser = VisibleText()
    parser.feed(body)
    text = unicodedata.normalize('NFKD', html.unescape(' '.join(parser.parts)))
    text = ''.join(c for c in text if not unicodedata.combining(c)).lower()
    return any(marker in text for marker in (
        'votre reponse a ete enregistree', 'your response has been recorded',
    ))


def send_response(payload, opener=urlopen):
    # Le destinataire et les champs sont ceux du formulaire public existant.
    request = Request(POST_URL + '?hl=fr', data=urlencode(payload).encode('utf-8'),
                      headers={'Content-Type': 'application/x-www-form-urlencoded'}, method='POST')
    with opener(request, timeout=35) as response:
        body = response.read().decode('utf-8', errors='replace')
        if response.status != 200 or not submission_confirmed(body):
            raise RuntimeError('Google n’a pas confirmé l’enregistrement. Vérifiez les réponses avant de renvoyer les données.')


def afficher_saisie_carbone(df):
    import streamlit as st
    st.subheader('Saisie Carbone — Réseau Haut Vaucluse')
    st.write('Les mêmes questions que votre collecte, directement dans l’application. Laissez vide ce que vous ne connaissez pas ; écrivez 0 uniquement si la quantité est réellement nulle.')
    if df.empty:
        st.info('La liste des établissements est indisponible. Actualisez les données avant de saisir.')
        return False
    school_col = 'Etablissements' if 'Etablissements' in df.columns else df.columns[0]
    schools = [str(v) for v in df[school_col].dropna().unique()
               if str(v).strip() and not re.search(r'total|moyenne', str(v), re.I)]
    st.info('Cet envoi ajoute une réponse aux totaux existants ; il ne corrige pas une réponse antérieure. Ne renvoyez pas des consommations déjà transmises.')
    with st.form('saisie_carbone_native'):
        school = st.selectbox('Sélectionnez votre établissement', schools, index=None,
                              placeholder='Choisir dans la liste du bilan carbone')
        values = {}
        for group, fields in GROUPS:
            with st.expander(group, expanded=group in ('Énergie et eau', 'Biens et consommables', 'Équipements')):
                if group == 'Équipements':
                    st.caption('Conservez le même périmètre que vos enquêtes précédentes : distinguez le parc total des achats de l’année lors de la validation du bilan.')
                if group == 'Alimentation':
                    st.caption('À renseigner seulement si ces repas ne sont pas déjà comptabilisés via A.B.C. Ne comptez pas les mêmes repas à la fois comme repas moyens et par catégorie.')
                for entry, label, integer in fields:
                    values[entry] = st.text_input(label, key='carbone_' + entry,
                                                  placeholder='Non renseigné',
                                                  help='Nombre entier' if integer else 'Virgule ou point acceptés. Unité indiquée dans la question.')
        checked = st.form_submit_button('Vérifier ma saisie')
    if checked:
        st.session_state.pop('carbone_a_confirmer', None)
        try:
            payload, recap = build_payload(school, schools, values)
            st.session_state['carbone_a_confirmer'] = {'payload': payload, 'recap': recap}
        except ValueError as exc:
            st.error(str(exc))
    pending = st.session_state.get('carbone_a_confirmer')
    if not pending:
        return False
    # Une modification après la vérification exige un nouveau récapitulatif.
    try:
        current, _ = build_payload(school, schools, values)
    except ValueError:
        current = None
    if current != pending['payload']:
        st.info('Les champs ont changé : cliquez de nouveau sur Vérifier ma saisie.')
        return False
    st.markdown('#### Récapitulatif — ' + pending['payload']['entry.' + SCHOOL_ENTRY])
    st.dataframe(pending['recap'], hide_index=True, width='stretch')
    signature = hashlib.sha256(json.dumps(pending['payload'], sort_keys=True).encode()).hexdigest()
    sent = st.session_state.get('carbone_envois', {})
    if signature in sent:
        if sent[signature] == 'ok':
            st.success('Cette saisie a déjà été enregistrée. Elle ne sera pas renvoyée.')
        else:
            st.warning('Un envoi a déjà été tenté. Vérifiez les réponses dans Google Sheets avant toute nouvelle tentative, pour éviter un doublon.')
        return False
    agree = st.checkbox('Je confirme les valeurs et qu’elles ne sont pas déjà transmises.', key='carbone_confirmation')
    if st.button('Envoyer mes données', disabled=not agree, key='carbone_envoyer'):
        sent[signature] = 'incertain'
        st.session_state['carbone_envois'] = sent
        try:
            with st.spinner('Enregistrement dans la collecte du réseau…'):
                send_response(pending['payload'])
        except Exception as exc:
            st.error(str(exc))
            st.link_button('Vérifier dans le formulaire habituel', FORM_URL)
            return False
        sent[signature] = 'ok'
        st.success('Google a confirmé l’enregistrement. Actualisez les données du bilan pour voir les résultats.')
        st.caption('L’eau est collectée en m³ ; sa conversion carbone reste à valider. Les repas viande blanche doivent aussi être reliés au bilan avant d’y apparaître.')
        return True
    return False
