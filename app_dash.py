import streamlit as st
import pandas as pd

# Load config
colunas_painel = ['NU_NOTIFIC', 'ID_AGRAVO', 'NU_ANO', 'ID_REGIONA', 'ID_MUNICIP', 'CS_SEXO', 'CS_RACA']

anos = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
        2016, 2017, 2018, 2019, 2020]

racas = [
    "Branca", "Preta", "Amarela", "Parda", "Indígena", "Ignorado"
]

id_agravos = {
    'A90': 'DENGUE',
    'A630': 'Verrugas anogenitais',
    'A60':'Herpes',
    'A53': 'Sifilis',
    'A539': 'Sifilis',
    'A010': 'FEBRE TIFOIDE',
    'A379': 'COQUELUCHE',
    'A959': 'FEBRE AMARELA',
    'A509': 'Sifilis congenita',
    'A309': 'HANSNENIASE',
    'A279': 'LEPTOSPIROSE',
    'A35': 'TETANO',
    'A369': 'DIFTERIA',
    'A809': 'PARALISIA FLACIDA AGUDA POLIOMIELITE',
    'A988': 'HANTAVIROSE',
    'A169': 'TUBERCULOSE',
    'A080': 'ROTAVIRUS',
    'A009': 'COLERA',
    'A928': 'Febres por arbovírus e febres hemorrágicas virais',
    'A33': 'TETANO RECEN NASCIDO',
    'A779': 'FEBRE MACULOSA - RICKETTSIOSES',
    'A719': 'TRACOMA',
    'A920': 'Chikungunya',
    'A051': 'BOTULISMO',
    'A810': 'DOENCA DE CREUTZFELDT-JACOB',
    'A692': 'Doenca de Lyme',
    'A938': 'Febres virais transmitidas por artropodes',
    'A23': 'BRUCELOSE',
    'A923': 'FEBRE DO NILO',
    'A829': 'RAIVA HUMANA',
    'A219': 'TULAREMIA',
    'A969': 'Febre hemorragica por arenavirus',
    'A08': 'SINDROME DIARREICA AGUDA',
    'A209': 'PESTE',
    'A229': 'CARBUNCULO OU ANTRAZ',
    'B551': 'LEISHMANIOSE TEGUMENTAR AMERICANA',
    'B550': 'LEISHMANIOSE VISCERAL',
    'B24': 'Doença pelo vírus da imunodeficiência humana [HIV]',
    'B19': 'HEPATITES VIRAIS',
    'B09': 'DOENCAS EXANTEMATICAS',
    'B659': 'ESQUISTOSSOMOSE',
    'B571': 'DOENCA DE CHAGAS AGUDA',
    'B019': 'VARICELA',
    'B26': 'Caxumba',
    'B54': 'MALARIA',
    'B58': 'Toxoplasmose',
    'B01': 'Varicela',
    'B749': 'FILARIOSE NAO ESPECIFICADA',
    'B03': 'VARIOLA',
    'D593': 'Sindrome hemolitico-uremica',
    'D699': 'SINDROME DA FEBRE HEMORRAGICA AGUDA',
    'F99': 'Transtorno mental não especificado',
    'G039': 'MENINGITE',
    'G043': 'SINDROME NEUROLOGICA AGUDA',
    'H833': 'Doenças do ouvido interno',
    'J06': 'SINDROME GRIPAL',
    'J07': 'SINDROME RESPIRATORIA AGUDA',
    'J189': 'Influenza e pneumonia',
    'J11': 'INFLUENZA HUMANA POR NOVO SUBTIPO (PANDEMICO)',
    'J64': 'PNEUMONIA',
    'L989': 'Afeccoes da pele e do tecido subcutaneo',
    'N72': 'Doenca inflamatoria do colo do utero',
    'N485': 'Doenças dos órgãos genitais masculinos',
    'N199': 'SINDROME DA INSUFICIENCIA RENAL AGUDA',
    'O981': 'Complicacoes da gravidez',
    'O986': 'Doencas causadas por protozoarios complicando a gravidez, o parto e o puerperio',
    'P350': 'Sindrome da rubeola congenita',
    'P371': 'Toxoplasmose congenita',
    'R17': 'SINDROME ICTERICA AGUDA',
    'R36': 'Secrecao uretral',
    'R699': 'OUTRAS SINDROMES',
    'T659': 'INTOXICACAO EXOGENA',
    'Y59': 'EVENTOS ADVERSOS POS-VACINACAO',
    'Y09': 'AGRESSAO',
    'Y96': 'Circunstancia relativa as condicoes de trabalho',
    'X29': 'Contato com animais e plantas venenosos',
    'W64': 'Exposição a forças mecânicas animadas',
    'Z209': 'Contato com exposicao a doencas transmissiveis nao especificadas',
    'Z206': 'Contato com e exposicao ao virus da imunodeficiencia humana [HIV]',
    'Z21': 'Estado de infeccao assintomatica pelo virus da imunodeficiencia humana [HIV]',
    'Z579': 'Exposicao ocupacional a fatores de risco',
}


# Configuração da página
st.set_page_config(
    layout="wide",
    page_title="Painel - Dashboards"
)


# Título
st.title("Painel de Dashboards")

# Cabeçalho da página
st.title('Painel')
with st.container(border=True):
    st.write('Dashboard - Agravos')


# Leitura do arquivo
@st.cache_data
def load_data():
    return pd.read_csv("painel.csv", sep=',')


df = load_data()


# Filtros da página
with st.container(border=True):
    st.markdown('**Filtros**')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ano = st.multiselect(label='Ano', options=anos, default=anos)
    with col2:
        sexo = st.multiselect(label='Sexo', options=['Masculino', 'Feminino', 'Ignorado'],
                              default=['Masculino', 'Feminino', 'Ignorado'])
    with col3:
        raca = st.multiselect(label='Raça', options=racas,
                              default=racas)
    with col4:
        agravo = st.selectbox(label='Agravo', options=list(id_agravos.values()))

with st.container(border=False):
    # Filtrando o DataFrame
    df_filtrado = df[df['NU_ANO'].isin(ano)]
    df_filtrado = df_filtrado[df_filtrado['CS_SEXO'].isin(sexo)]
    df_filtrado = df_filtrado[df_filtrado['CS_RACA'].isin(raca)]
    df_filtrado = df_filtrado[df_filtrado['ID_AGRAVO'] == agravo]

    with st.container(border=True):
        g1, g2 = st.columns(2)
        with g1:
            # Gráfico - Sexo
            st.markdown('**Sexo**')
            st.bar_chart(data=df_filtrado['CS_SEXO'].value_counts(),
                         height=400,
                         width=600,
                         use_container_width=False)
        with g2:
            # Gráfico - Raça
            st.markdown('**Raça**')
            st.bar_chart(data=df_filtrado['CS_RACA'].value_counts(),
                         height=400,
                         width=600,
                         use_container_width=False)