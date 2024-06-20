import streamlit as st
import plotly.express as px
import pandas as pd

# Load filtros
from filtros import agravo, ano, municipio, raca, regiao, sexo


# Configuração da página
st.set_page_config(
    layout="wide",
    page_title="NIVS - Dashboards"
)

# Logo
st.image('img/logo-sespa.jpg')

# Título
st.title("Painel SINAN")

# Cabeçalho da página

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
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        ano = st.multiselect(label='Ano',
                             options=ano.ANO,
                             default=ano.ANO)

    with col2:
        sexo = st.multiselect(label='Sexo',
                              options=['Masculino', 'Feminino', 'Ignorado'],
                              default=['Masculino', 'Feminino', 'Ignorado'])

    with col3:
        raca = st.multiselect(label='Raça',
                              options=list(raca.RACA.values()),
                              default=list(raca.RACA.values()))
    with col4:
        agravo = st.selectbox(label='Agravo',
                              options=list(agravo.AGRAVO.values()),
                              index=None,
                              placeholder='Selecione um agravo')
        macro_reg_saude = st.selectbox(label='Macro Região de Saúde',
                                       options=regiao.MACRO_REG_SAUDE,
                                       index=None,
                                       placeholder='Selecione uma macro região de saúde')
        reg_saude = st.selectbox(label='Região de Saúde',
                                 options=regiao.REG_SAUDE,
                                 index=None,
                                 placeholder='Selecione uma região de saúde')
    with col5:
        centro_reg_saude = st.selectbox(label='Centro de Regional de Saúde',
                                        options=regiao.CENTRO_REG_SAUDE,
                                        index=None,
                                        placeholder='Selecione um centro de regional de saúde')
        reg_integracao = st.selectbox(label='Região de Integração',
                                      options=regiao.REG_INTEGRACAO,
                                      index=None,
                                      placeholder='Selecione uma região de integração')
        municipio = st.selectbox(label='Município',
                                 options=municipio.MUNICIPIO,
                                 index=None,
                                 placeholder='Selecione um município')


with (st.container(border=False)):
    # Filtrando o DataFrame
    df_filtrado = df[df['NU_ANO'].isin(ano)]
    df_filtrado = df_filtrado[df_filtrado['CS_SEXO'].isin(sexo)]
    df_filtrado = df_filtrado[df_filtrado['CS_RACA'].isin(raca)]
    df_filtrado = df_filtrado[df_filtrado['ID_AGRAVO'] == agravo]
    df_filtrado = df_filtrado[df_filtrado['MACRO_REG_SAUDE'] == macro_reg_saude] if macro_reg_saude != None else df_filtrado
    df_filtrado = df_filtrado[df_filtrado['REG_SAUDE'] == reg_saude] if reg_saude != None else df_filtrado
    df_filtrado = df_filtrado[df_filtrado['CENTRO_REG_SAUDE'] == centro_reg_saude] if centro_reg_saude != None else df_filtrado
    df_filtrado = df_filtrado[df_filtrado['REG_INTEGRACAO'] == reg_integracao] if reg_integracao != None else df_filtrado
    df_filtrado = df_filtrado[df_filtrado['MUN_NOME'] == municipio] if municipio != None else df_filtrado

# Métricas
    with st.container(border=True):
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric(label='Total',
                      value=df_filtrado.shape[0])
        with m2:
            st.metric(label='Masculino',
                      value=df_filtrado[df_filtrado['CS_SEXO'] == 'Masculino'].shape[0])
        with m3:
            st.metric(label='Feminino',
                      value=df_filtrado[df_filtrado['CS_SEXO'] == 'Feminino'].shape[0])
        with m4:
            st.metric(label='Ignorado',
                      value=df_filtrado[df_filtrado['CS_SEXO'] == 'Ignorado'].shape[0])
        with m5:
            st.metric(label='Óbitos',
                      value=df_filtrado[df_filtrado['DT_OBITO'] != 'IGNORADO'].shape[0])

# Gráficos
    with st.container(border=True):
        g1, g2 = st.columns(2)
        with g1:
            # Gráfico - Sexo

            fig = px.pie(data_frame=df_filtrado,
                         names='CS_SEXO',
                         title='Sexo',
                         hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         width=600,
                         height=400)

            st.plotly_chart(fig)

        with g2:
            # Gráfico - Raça
            st.markdown('**Raça**')
            st.bar_chart(data=df_filtrado['CS_RACA'].value_counts(),
                         height=400,
                         width=600,
                         use_container_width=False)

# Tabelas
    with st.container(border=True):
        tb1, tb2 = st.columns(2)
        with tb1:
            # Tabela filtrada
            st.markdown('**Tabela Filtrada**')
            st.dataframe(df_filtrado)
