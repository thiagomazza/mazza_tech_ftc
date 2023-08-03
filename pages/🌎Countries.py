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
st.set_page_config(page_title="Countries",page_icon="🌎", layout="wide")

# Função para criar a barra lateral
image = Image.open("../img/logo_2.png")
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
st.markdown('# 🌎 Visão Países')

with st.container():
    # Definição das colunas para pesquisa
    colunas = ['Country Code', 'City']
    contagem_por_pais = df_aux_filtrado.loc[:, colunas].groupby(['Country Code']).count().reset_index()

    # Ordenar pelo maior valor (em ordem decrescente)
    contagem_por_pais_sorted = contagem_por_pais.sort_values(by='City', ascending=False).head(10)
    
    # Definição título do gráfico
    st.markdown("<h4 style='text-align: center; font-size: 26px;'>TOP 10 Países com mais Cidades</h4>", unsafe_allow_html=True)
    
    # Geração do gráfico
    fig = px.bar(
    contagem_por_pais_sorted,
    x="Country Code",
    y="City",
    color="Country Code",
    color_continuous_scale="reds",
    labels={"Country Code": "País"},
    )
    # Personalizando os nomes dos eixos X e Y e o título do gráfico
    fig.update_layout(
    xaxis_title="Países",
    yaxis_title="Qtde de Cidades"
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Definição das colunas para pesquisa
        colunas = ['Country Code', 'Restaurant ID']
        paises_contagem_cidades = df_aux_filtrado.loc[:, colunas].groupby(['Country Code']).count().reset_index().sort_values(by='Restaurant ID', ascending=False).head(10)

        # Definição título do gráfico
        st.markdown("<h4 style='text-align: center; font-size: 16px;'>TOP 10 Países com mais Restaurantes</h4>", unsafe_allow_html=True)

        # Geração do gráfico
        fig = px.bar(
        paises_contagem_cidades,
        x="Country Code",
        y="Restaurant ID",
        color="Restaurant ID",
        color_continuous_scale="reds",
        labels={"Restaurant ID": "Qtde Restaurantes"},
        )
        # Personalizando os nomes dos eixos X e Y e o título do gráfico
        fig.update_layout(
        xaxis_title="Países",
        yaxis_title="Qtde de Restaurantes"
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with col2:
        # Definição das colunas para pesquisa
        colunas = ['Country Code', 'Cuisines']
        paises_contagem_culinarias = df_aux_filtrado.loc[:, colunas].groupby(['Country Code']).nunique().reset_index().sort_values(by='Cuisines', ascending=False).head(10)
        
        # Definição título do gráfico
        st.markdown("<h4 style='text-align: center; font-size: 16px;'>TOP 10 Países com mais Tipos Culinários</h4>", unsafe_allow_html=True)

        # Geração do gráfico
        fig = px.bar(
        paises_contagem_culinarias,
        x="Country Code",
        y="Cuisines",
        color="Cuisines",
        color_continuous_scale="reds",
        labels={"Cuisines": "Tipos Culinários"},
        )
        # Personalizando os nomes dos eixos X e Y e o título do gráfico
        fig.update_layout(
        xaxis_title="Países",
        yaxis_title="Qtde de Tipos Culinários"
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with st.container():
    # Definição das colunas para pesquisa
    colunas = ['Country Code', 'Votes']
    paises_quantidade_votos = df_aux_filtrado.loc[:, colunas].groupby(['Country Code']).sum().reset_index().sort_values(by='Votes', ascending=False).head(10)
    # Definição título do gráfico
    st.markdown("<h4 style='text-align: center; font-size: 26px;'>TOP 10 Países com mais Votos</h4>", unsafe_allow_html=True)

    # Geração do gráfico
    fig = px.bar(
    paises_quantidade_votos,
    x="Country Code",
    y="Votes",
    color="Country Code",
    color_continuous_scale="reds",
    labels={"Country Code": "País"},
    )
    # Personalizando os nomes dos eixos X e Y e o título do gráfico
    fig.update_layout(
    xaxis_title="Países",
    yaxis_title="Qtde de Votos"
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
