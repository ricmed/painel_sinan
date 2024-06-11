import streamlit as st
import pandas as pd

# Load filtros
from filtros import agravo, ano, municipio, raca, regiao, sexo


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
    return pd.read_parquet("painel.parquet")


df = load_data()

# Filtros da página
with st.container(border=True):
    st.markdown('**Filtros**')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ano = st.multiselect(label='Ano',
                             options=ano.ANO,
                             default=ano.ANO)
    with col2:
        sexo = st.multiselect(label='Sexo',
                              options=['Masculino', 'Feminino', 'Ignorado'],
                              default=['Masculino', 'Feminino', 'Ignorado'])
        municipio = st.selectbox(label='Município',
                                 options=municipio.MUNICIPIO)
    with col3:
        raca = st.multiselect(label='Raça',
                              options=list(raca.RACA.values()),
                              default=list(raca.RACA.values()))
    with col4:
        agravo = st.selectbox(label='Agravo',
                              options=list(agravo.AGRAVO.values()))

with st.container(border=False):
    # Filtrando o DataFrame
    df_filtrado = df[df['NU_ANO'].isin(ano)]
    df_filtrado = df_filtrado[df_filtrado['CS_SEXO'].isin(sexo)]
    df_filtrado = df_filtrado[df_filtrado['CS_RACA'].isin(raca)]
    df_filtrado = df_filtrado[df_filtrado['ID_AGRAVO'] == agravo]
    df_filtrado = df_filtrado[df_filtrado['MUN_NOME'] == municipio]

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

    with st.container(border=True):
        tb1, tb2 = st.columns(2)
        with tb1:
            # Tabela filtrada
            st.markdown('**Tabela Filtrada**')
            st.dataframe(df_filtrado)
