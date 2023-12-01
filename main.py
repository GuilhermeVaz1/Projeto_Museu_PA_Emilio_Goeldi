import pandas as pd
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')


def interpolate(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


df = pd.read_csv("C:/Users/23300037/Documents/Projeto_Museu_PA_Emilio_Goeldi/tabela.csv", sep=";")

st.header('Mapa')
map = df[['decimalLatitude', 'decimalLongitude']]
map = map[map.notnull().all(1)]

map = map * 10e-7
map.loc[abs(map['decimalLongitude']) <= 10.0, 'decimalLongitude'] = map.loc[abs(
    map['decimalLongitude']) <= 10.0, 'decimalLongitude'] * 10.0
map.loc[abs(map['decimalLongitude']) <= 10.0, 'decimalLongitude'] = map.loc[abs(
    map['decimalLongitude']) <= 10.0, 'decimalLongitude'] * 10.0
map.loc[abs(map['decimalLongitude']) <= 10.0, 'decimalLongitude'] = map.loc[abs(
    map['decimalLongitude']) <= 10.0, 'decimalLongitude'] * 10.0
map = map.groupby(map.columns.tolist(), as_index=False).size()
colors = []
for size in map['size']:
    color_tuple = (interpolate(size, 10, 100, 0, 1), interpolate(size, 10, 100, 1, 0), 0.0)
    colors.append(color_tuple)

map['size'] = map['size'] * 30

map['colors'] = colors
c = st.empty()
c.map(map, latitude='decimalLatitude', longitude='decimalLongitude', color='colors', size='size',
      use_container_width=True)

tab1, tab2 = st.tabs(['Ranks Taxonômicos', 'Análise por Estados'])

with tab1:
    st.header('Ranks Taxonômicos')
    taxon_rank = df[['taxonRank']]
    taxon_rank = taxon_rank.groupby(taxon_rank.columns.tolist(), as_index=False).size()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(taxon_rank['size'], labels=taxon_rank['taxonRank'], autopct='%1.1f%%', radius=0.6,
                                      textprops={'size': 'xx-small'})
    ax.legend(wedges, taxon_rank['taxonRank'],
              title="Taxon Ranks",
              loc="best",
              bbox_to_anchor=(1, 0, 0.5, 1))
    st.pyplot(fig, use_container_width=False)

with tab2:
    st.header('Análise por Estados')
    option = st.selectbox('Selecione o estado:', df['stateProvince'].dropna().unique())
    df01 = df[['stateProvince', 'county']]
    fig, ax = plt.subplots(2)
    matplotlib.rc('ytick', labelsize=5)
    ax[0].barh(df.loc[df['stateProvince'] == option, 'county'].dropna().unique().tolist(),
           df.loc[df['stateProvince'] == option, 'county'].dropna().value_counts().tolist(), height=0.8)
    ax[0].set_title(f'Análise do {option}')
    ax[0].set_xlabel('Número de ocorrências')
    ax[0].set_ylabel('Cidades')
    fig.set_figwidth(4)
    fig.set_figheight(10)
    df02 = df['stateProvince'].value_counts()
    ax[1].pie(df02.tolist(), labels=df['stateProvince'].dropna().unique(), textprops={'size': 'xx-small'}, wedgeprops=dict(width=0.5))
    ax[1].set_title(f'Estados')
    st.pyplot(fig, use_container_width=False)

