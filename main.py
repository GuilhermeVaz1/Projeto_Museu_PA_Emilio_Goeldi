import pandas as pd
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')


def interpolate(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


df = pd.read_csv("C:/Users/23300037/Downloads/Projeto_Museu_PA_Emilio_Goeldi/tabela.csv", sep=";")

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

with st.expander('Ranks taxonômicos e análise por estados'):
    column1, column2 = st.columns(2)

    with column1:
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
        st.pyplot(fig, use_container_width=True)

    with column2:
        st.header('Análise por Estados')
        option = st.selectbox('Selecione o estado:', df['stateProvince'].dropna().unique())
        df01 = df[['stateProvince', 'county']]
        fig, ax = plt.subplots()
        matplotlib.rc('ytick', labelsize=5)
        ax.barh(df.loc[df['stateProvince'] == option, 'county'].dropna().unique().tolist(),
                df.loc[df['stateProvince'] == option, 'county'].dropna().value_counts().tolist(), height=0.8)
        ax.set_title(f'Análise do {option}')
        ax.set_xlabel('Número de ocorrências')
        ax.set_ylabel('Cidades')
        st.pyplot(fig, use_container_width=True)

with st.expander('Por mês e pesquisadores'):
    column21, column22 = st.columns(2)

    with column21:
        st.header('Ocorrências por mês')
        series = df['month'].dropna().sort_values(ascending=True)
        count = series.value_counts().sort_index(ascending=True)
        df02 = pd.DataFrame([series.unique(), count], index=['month','count']).transpose()
        fig, ax = plt.subplots()
        ax.plot(df02['month'], df02['count'], '-o')
        plt.grid(visible=True, axis='x')
        plt.xticks(df02['month'])
        ax.set_xlabel('Mês')
        ax.set_ylabel('Número de ocorrências')
        for xy in zip(df02['month'], df02['count']):                                       # <--
            ax.annotate(f'({xy[1]:.0f})', xy=xy, textcoords='data')
        st.pyplot(fig, use_container_width=True)

    with column22:
        st.header('Pesquisadores x Ocorrências')
        names = []
        name_count = []
        for index, value in df['recordedBy'].items():
            if not isinstance(value, float):
                values = value.split(';')
                for each in values:
                    names.append(each.strip())
        name_set = set(names)
        for name in name_set:
            name_count.append((name, names.count(name)))
        df03 = pd.DataFrame(name_count, columns=['name', 'count']).sort_values(by='count', ascending=True)
        fig, ax = plt.subplots()
        ax.barh(df03['name'], df03['count'])
        for xy in zip(df03['count'], df03['name']):                                       # <--
            ax.annotate(f'{xy[0]:.0f}', xy=xy, textcoords='data', fontsize=4)
        ax.set_xlabel('Número de ocorrências')
        ax.set_ylabel('Pesquisadores')
        st.pyplot(fig)