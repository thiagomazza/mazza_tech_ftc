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
st.set_page_config(page_title="Tipos_Culinários",page_icon="🍽️", layout="wide")

# Função para criar a barra lateral
image = Image.open("./img/Logo_2.png")
col1, col2 = st.sidebar.columns([1, 2], gap="small")
col1.image(image, width=100)
col2.markdown("# Fome Zero")
countries = st.sidebar.multiselect(
    "Escolha os Paises que deseja filtrar:",
    df_aux.loc[:, "Country Code"].unique().tolist(),
    default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
)

# Filtro do DataFrame com base nos países selecionados
df_aux_filtrado = df_aux[df_aux['Country Code'].isin(countries)]

st.markdown('# 🍽️ Visão Restaurantes')
st.markdown('## Melhores Restaurantes por Tipo Culinário: ')

with st.container():
    # Definição colunas de exibição
    col1, col2, col3, col4, col5 = st.columns(5)
    colunas = ['Restaurant Name', 'Aggregate rating']
    with col1:
        # Melhor Restaurante Italiano
        cozinha_italiana = df[df['Cuisines'] == 'Italian']
        restaurante_italiano = cozinha_italiana.loc[:, colunas].groupby(['Restaurant Name']).mean().reset_index().sort_values(by='Aggregate rating', ascending=False).head(1)
        italia1 = restaurante_italiano.loc[:, 'Restaurant Name' ]
        italia2 = restaurante_italiano.loc[:, 'Aggregate rating' ]
        # Obtenha o valor da série
        nome_italia1 = italia1.iloc[0]
        nota_italia1 = italia2.iloc[0]
        st.markdown(f'<p style="font-size: 17px;">Melhor Restaurante Italiano:</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 24px;">{nome_italia1} / {nota_italia1}</p>', unsafe_allow_html=True)

    with col2:
        # Melhor Restaurante Indiano
        cozinha_indiana = df[df['Cuisines'] == 'Indian']
        restaurante_indiano = cozinha_indiana.loc[:, colunas].groupby(['Restaurant Name']).mean().reset_index().sort_values(by='Aggregate rating', ascending=False).head(1)
        india1 = restaurante_indiano.loc[:, 'Restaurant Name' ]
        india2 = restaurante_indiano.loc[:, 'Aggregate rating' ]
        # Obtenha o valor da série
        nome_india1 = india1.iloc[0]
        nota_india1 = india2.iloc[0]
        st.markdown(f'<p style="font-size: 17px;">Melhor Restaurante Indiano:</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 24px;">{nome_india1} / {nota_india1}</p>', unsafe_allow_html=True)

    with col3:
        # Melhor Restaurante Brasileiro
        cozinha_brasileira = df[df['Cuisines'] == 'Brazilian']
        restaurante_brasileiro = cozinha_brasileira.loc[:, colunas].groupby(['Restaurant Name']).mean().reset_index().sort_values(by='Aggregate rating', ascending=False).head(1)
        brasil1 = restaurante_brasileiro.loc[:, 'Restaurant Name' ]
        brasil2 = restaurante_brasileiro.loc[:, 'Aggregate rating' ]
        # Obtenha o valor da série
        nome_brasil1 = brasil1.iloc[0]
        nota_brasil1 = brasil2.iloc[0]
        st.markdown(f'<p style="font-size: 17px;">Melhor Restaurante Brasileiro:</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 24px;">{nome_brasil1} / {nota_brasil1}</p>', unsafe_allow_html=True)

    with col4:
        # Melor Restaurante Japonês
        cozinha_japones = df[df['Cuisines'] == 'Japanese']
        restaurante_japones = cozinha_japones.loc[:, colunas].groupby(['Restaurant Name']).mean().reset_index().sort_values(by='Aggregate rating', ascending=False).head(1)
        japao1 = restaurante_japones.loc[:, 'Restaurant Name' ]
        japao2 = restaurante_japones.loc[:, 'Aggregate rating' ]
        # Obtenha o valor da série
        nome_japao1 = japao1.iloc[0]
        nota_japao1 = japao2.iloc[0]
        st.markdown(f'<p style="font-size: 17px;">Melhor Restaurante Japonês:</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 24px;">{nome_japao1} / {nota_japao1}</p>', unsafe_allow_html=True)

    with col5:
        # Melhor Restaurante Americano
        cozinha_americano = df[df['Cuisines'] == 'American']
        restaurante_americano = cozinha_americano.loc[:, colunas].groupby(['Restaurant Name']).mean().reset_index().sort_values(by='Aggregate rating', ascending=False).head(1)
        america1 = restaurante_americano.loc[:, 'Restaurant Name' ]
        america2 = restaurante_americano.loc[:, 'Aggregate rating' ]
        # Obtenha o valor da série
        nome_america1 = america1.iloc[0]
        nota_america1 = america2.iloc[0]
        st.markdown(f'<p style="font-size: 17px;">Melhor Restaurante EUA:</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 24px;">{nome_america1} / {nota_america1}</p>', unsafe_allow_html=True)

st.markdown("""___""")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        colunas = ['Restaurant Name', 'Aggregate rating']
        top10_restaurantes = df_aux_filtrado.loc[:, colunas].groupby(['Restaurant Name']).mean().reset_index().sort_values(by='Aggregate rating', ascending=False).head(10)
        # Definição título do gráfico
        st.markdown("<h4 style='text-align: center; font-size: 22px;'>TOP 10 Melhores Restaurantes</h4>", unsafe_allow_html=True)

        # Geração do gráfico
        fig = px.bar(
        top10_restaurantes,
        x="Restaurant Name",
        y="Aggregate rating",
        color="Restaurant Name",
        color_continuous_scale="reds",
        labels={"Restaurant Name": "Restaurante"},
        )
        # Personalizando os nomes dos eixos X e Y e o título do gráfico
        fig.update_layout(
        xaxis_title="Restaurante",
        yaxis_title="Nota Média"
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
    with col2:
        colunas = ['Restaurant Name', 'Aggregate rating']
        df_aux_filtrado2 = df_aux_filtrado[df_aux_filtrado['Aggregate rating'] != 0]
        top10_restaurantes = df_aux_filtrado2.loc[:, colunas].groupby(['Restaurant Name']).mean().reset_index().sort_values(by='Aggregate rating', ascending=True).head(10)
        # Definição título do gráfico
        st.markdown("<h4 style='text-align: center; font-size: 22px;'>TOP 10 Piores Restaurantes</h4>", unsafe_allow_html=True)

        # Geração do gráfico
        fig = px.bar(
        top10_restaurantes,
        x="Restaurant Name",
        y="Aggregate rating",
        color="Restaurant Name",
        color_continuous_scale="reds",
        labels={"Restaurant Name": "Restaurante"},
        )
        # Personalizando os nomes dos eixos X e Y e o título do gráfico
        fig.update_layout(
        xaxis_title="Restaurante",
        yaxis_title="Nota Média"
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)        
