# Importando bibliotecas
import folium
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static
import plotly.express as px

# Lendo do Arquivo
df = pd.read_csv( 'zomato.csv' )

# Criação de lista para substituir o código dos países por nomes
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
df_aux = df.copy()
# Substituir todos os países de códigos para nomes
df_aux['Country Code'] = df['Country Code'].replace(COUNTRIES)


# Categorizar os restaurantes por um tipo de culinária
df_aux["Cuisines"] = df_aux.loc[:, "Cuisines"].apply(lambda x: str(x).split(",")[0])

# Mudar nome coluna para gerar mapa
df_aux.rename(columns={'Latitude': 'latitude'}, inplace=True) 
df_aux.rename(columns={'Longitude': 'longitude'}, inplace=True) 

###################################################################
###################### Montando Streamlit #########################
###################################################################

# Define título e tamanho ocupado na página
st.set_page_config(page_title="Cities",page_icon="🏙️", layout="wide")

# Função para criar a barra lateral
image = Image.open("img/logo_2.png")
col1, col2 = st.sidebar.columns([1, 2], gap="small")
col1.image(image, width=100)
col2.markdown("# Fome Zero")
st.sidebar.markdown("## Filtros")
countries = st.sidebar.multiselect(
    "Escolha os Paises que deseja filtrar:",
    df_aux.loc[:, "Country Code"].unique().tolist(),
    default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

# Filtro do DataFrame com base nos países selecionados
df_aux_filtrado = df_aux[df_aux['Country Code'].isin(countries)]

# Título Visão
st.markdown('# 🏙️ Visão Cidades')

with st.container():
    colunas1 = ['City', 'Restaurant ID']
    top10_cidades = df_aux_filtrado.loc[:, colunas1].groupby(['City']).count().reset_index().sort_values(by='Restaurant ID', ascending=False).head(10)
    st.markdown("<h4 style='text-align: center; font-size: 26px;'>TOP 10 Cidades com mais Restaurantes</h4>", unsafe_allow_html=True)
    df = px.data.iris()
    fig = px.bar(
    top10_cidades,
    x="City",
    y="Restaurant ID",
    color="City",
    color_continuous_scale="reds",
    labels={"City": "Cidade"},
)
    # Personalizando os nomes dos eixos X e Y e o título do gráfico
    fig.update_layout(
    xaxis_title="Cidades",
    yaxis_title="Qtde de Restaurantes"
)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        colunas2 = ['City', 'Aggregate rating']
        top_cidades_nota4 = df_aux_filtrado.loc[:, colunas2].groupby(['City']).mean().reset_index().sort_values(by='Aggregate rating', ascending=False).head(10)
        st.markdown("<h4 style='text-align: center; font-size: 16px;'>TOP 10 Cidades com Restaurantes bem Avaliados</h4>", unsafe_allow_html=True)
        df = px.data.iris()
        fig = px.bar(
        top_cidades_nota4,
        x="City",
        y="Aggregate rating",
        color="Aggregate rating",
        color_continuous_scale="reds",
        labels={"Aggregate rating": "Nota Média"},
    )
        # Personalizando os nomes dos eixos X e Y e o título do gráfico
        fig.update_layout(
        xaxis_title="Cidades",
        yaxis_title="Avaliação"
    )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with col2:
        colunas3 = ['City', 'Aggregate rating']
        top_cidades_abaixo_25 = df_aux_filtrado.loc[:, colunas3].groupby(['City']).count().reset_index().sort_values(by='Aggregate rating', ascending=True).head(10)
        st.markdown("<h4 style='text-align: center; font-size: 16px;'>TOP 10 Cidades com Restaurantes mal Avaliados</h4>", unsafe_allow_html=True)
        df = px.data.iris()
        fig = px.bar(
        top_cidades_abaixo_25,
        x="City",
        y="Aggregate rating",
        color="Aggregate rating",
        color_continuous_scale="blues",
        labels={"Aggregate rating": "Nota Média"},
    )
        # Personalizando os nomes dos eixos X e Y e o título do gráfico
        fig.update_layout(
        xaxis_title="Cidades",
        yaxis_title="Avaliação"
    )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with st.container():
    st.markdown("<h4 style='text-align: center; font-size: 26px;'>TOP 10 Cidades com Maiores Diversidades de Culinárias</h4>", unsafe_allow_html=True)
    colunas = ['City', 'Cuisines']
    cidades_variedades_culinarias = df_aux_filtrado.loc[:, colunas].groupby(['City']).count().reset_index().sort_values(by='Cuisines', ascending=False).head(10)
    df = px.data.iris()
    fig = px.bar(
    cidades_variedades_culinarias,
    x="City",
    y="Cuisines",
    color="City",
    color_continuous_scale="blues",
    labels={"City": "Cidade"},
)
    # Personalizando os nomes dos eixos X e Y e o título do gráfico
    fig.update_layout(
    xaxis_title="Cidades",
    yaxis_title="Qtde de Tipos Culinários"
)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    