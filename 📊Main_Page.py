# Importando bibliotecas
import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static


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

# Define título e tamanho ocupado na página
st.set_page_config(page_title="Fome Zero!",page_icon="📊", layout="wide")

# Função para criar a barra lateral
image = Image.open("img/Logo_2.png")
col1, col2 = st.sidebar.columns([1, 2], gap="small")
col1.image(image, width=100)
col2.markdown("# Fome Zero")
st.sidebar.markdown("## Filtros")
countries = st.sidebar.multiselect(
    "Escolha os Paises que deseja filtrar:",
    df_aux.loc[:, "Country Code"].unique().tolist(),
    default=df_aux.loc[:, "Country Code"].unique().tolist(),
    )

# Filtro do DataFrame com base nos países selecionados
df_aux_filtrado = df_aux[df_aux['Country Code'].isin(countries)]

 
# Categorizar os restaurantes por um tipo de culinária
df_aux["Cuisines"] = df_aux.loc[:, "Cuisines"].apply(lambda x: str(x).split(",")[0])

# Mudar nome coluna para gerar mapa
df_aux_filtrado.rename(columns={'Latitude': 'latitude'}, inplace=True) 
df_aux_filtrado.rename(columns={'Longitude': 'longitude'}, inplace=True) 

###################################################################
###################### Montando Streamlit #########################
###################################################################

   
# Cabeçalho página principal
st.markdown('# 📊Fome Zero !')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')

# Definição colunas de exibição
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    # Quantidade de Restaurantes
    df_qtde_restaurantes = df_aux['Restaurant ID'].count()
    formatted_restaurantes = "{:,}".format(df_qtde_restaurantes).replace(",", ".")
    st.metric(label='Restaurantes Cadastrados', value=formatted_restaurantes)
with col2:
    # Quantidade de Países
    df_qtde_paises = df_aux['Country Code'].nunique()
    st.metric(label='Países Cadastrados', value=df_qtde_paises)   
with col3:
    # Quantidade de Cidades
    df_qtde_cidades = df_aux['City'].nunique()
    st.metric(label='Cidades Cadastradas', value=df_qtde_cidades)
with col4:
    # Quantidade de Avaliações
    df_qtde_votes = df_aux['Votes'].sum()
    formatted_votes = "{:,}".format(df_qtde_votes).replace(",", ".")
    st.metric(label='Avaliações Feitas na Plataforma', value=formatted_votes)
with col5:
    # Quantidade de Tipos de Culinária
    df_qtde_culinaria = df_aux['Cuisines'].nunique()
    st.metric(label='Tipos de Culinárias Oferecidas', value=df_qtde_culinaria)

st.markdown("""___""")
    
    
# # Gerando mapa interativo
f = folium.Figure(width=2000, height=900)

m = folium.Map(max_bounds=True, zoom_start=3, title = 'Teste').add_to(f)

marker_cluster = MarkerCluster().add_to(m)

for _, line in df_aux_filtrado.iterrows():

    name = line["Restaurant Name"]
    price_for_two = line["Average Cost for two"]
    cuisine = line["Cuisines"]
    currency = line["Currency"]
    rating = line["Aggregate rating"]
    color = 'blue'

    html = "<p><strong>{}</strong></p>"
    html += "<p>Price: {},00 ({}) para dois"
    html += "<br />Type: {}"
    html += "<br />Aggragate Rating: {}/5.0"
    html = html.format(name, price_for_two, currency, cuisine, rating)

    popup = folium.Popup(
        folium.Html(html, script=True),
        max_width=500,
    )

    folium.Marker(
        [line["latitude"], line["longitude"]],
        popup=popup,
        icon=folium.Icon(color=color, icon="home", prefix="fa"),
    ).add_to(marker_cluster)

folium_static(m, width=1150, height=450)

