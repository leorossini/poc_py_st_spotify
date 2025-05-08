import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import time

# localização do dado
dirData = Path('data')
csvSpotify = dirData / '01 Spotify.csv'


# Definindo o estilo do Streamlit
# tem que ser definido antes de cache de dados senão chama mais de uma vez
st.set_page_config(layout="wide", page_title="Spotify - Análise de Dados")

# Carregar os dados em cache
@st.cache_data # decorador para cache
def carregarDadosSpotify():
    df = pd.read_csv(csvSpotify)
    time.sleep(3)
    # dados pesados e demorados ou repetitivos
    return df # vai parao cache

df_spotify= carregarDadosSpotify() # carraga os dados da função de cache e não executa mais a função
df_spotify_itrack = df_spotify.set_index('Track')
# artistas
artists = df_spotify['Artist'].value_counts().index

# Variáveis de sessão
st.session_state['df_spotify'] = df_spotify
st.session_state['df_spotify_itrack'] = df_spotify_itrack
st.session_state['artists'] = artists





# FILTROS
## artista
st.subheader('Filtros')
sel_artist = st.sidebar.selectbox('Artista', artists)
# aplicação de filtros
df_spotify_filtered = df_spotify_itrack[(df_spotify_itrack['Artist'] == sel_artist)]

## álbuns
albuns = df_spotify_filtered['Album'].unique()
sel_album = st.selectbox('Albuns', albuns, placeholder='Escolha um álbum')
# aplicação de filtros
df_spotify_filtered = df_spotify_filtered[(df_spotify_filtered['Artist'] == sel_artist) & (df_spotify_filtered['Album'] == sel_album)]

# personalizações
mostrarBarras = st.checkbox('Mostrar barras', value=True)


# Gráficos
if mostrarBarras:
    col1, col2 = st.columns(2)
    col1, col2 = st.columns([0.7, 0.3])
    col1.bar_chart(df_spotify_filtered['Stream'])
    col2.bar_chart(df_spotify_filtered['Danceability'])





# Tabulares
st.write(df_spotify_filtered)
# mesma coisa de colocar só o df

