import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry 


st.set_page_config(
    page_title="Dashboard de Salários na Área de Engenharia de Redes",
    page_icon="👷‍♂️",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/luisalbertool/engenheiroderedes/refs/heads/main/salarios_engenheiro_redes_mensal.csv")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# --- Filtro de Mês ---
meses_disponiveis = sorted(df['mes'].unique())
meses_selecionados = st.sidebar.multiselect("Mês", meses_disponiveis, default=meses_disponiveis)

# --- Filtro de País ---
paises_disponiveis = sorted(df['pais'].unique())
paises_selecionados = st.sidebar.multiselect("País", paises_disponiveis, default=paises_disponiveis)

# --- Filtro de Moeda Local ---
moedas_disponiveis = sorted(df['moeda_local'].unique())
moedas_selecionadas = st.sidebar.multiselect("Moeda Local", moedas_disponiveis, default=moedas_disponiveis)

# --- Media anual por dolár ---
media_anual = df.groupby("pais")["salario_medio_usd"].mean().reset_index()


#Filtragem do DF

df_filtrado = df[
    (df['mes'].isin(meses_selecionados)) &
    (df['pais'].isin(paises_selecionados)) &
    (df['moeda_local'].isin(moedas_selecionadas))
]

empresa_pais = df_filtrado.groupby('pais')['salario_medio_usd'].mean().reset_index()

# Função para traduzir nomes de países do português para o inglês
def traduzir_pais(nome_pt):
    mapping = {
        "Brasil": "Brazil",
        "Estados Unidos": "United States",
        "Reino Unido": "United Kingdom",
        "Alemanha": "Germany",
        "Canadá": "Canada",
        "Austrália": "Australia",
        "Índia": "India",
        "Japão": "Japan",
        "Emirados Árabes Unidos": "United Arab Emirates",
        "África do Sul": "South Africa"
    }
    return mapping.get(nome_pt, nome_pt)
empresa_pais = df_filtrado.groupby('pais')['salario_medio_usd'].mean().reset_index()
empresa_pais['pais_en'] = empresa_pais['pais'].apply(traduzir_pais)

# -- Titulo da pagina ---
st.title("🥅 Dashboard de Salários na Área de Engenharia de Redes")
st.markdown(' Veja a média salarial mensal de pessoas envolvidas com a área de Engenharia de Redes, filtrando por mês, país e moeda local.')

# --- Metrica principal ---
st.subheader("💰 Média Salarial Mensal (USD)")

if not df_filtrado.empty:
    media_salarial = df_filtrado['salario_medio_usd'].mean()
    max_salarial = df_filtrado['salario_medio_usd'].max()
    min_salarial = df_filtrado['salario_medio_usd'].min()
    total_registros = df_filtrado.shape[0]
else:
    media_salarial = 0
    max_salarial = 0
    min_salarial = 0
    total_registros = 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Média Salarial (USD)", f"${media_salarial:,.2f}")
col2.metric("Máximo Salarial (USD)", f"${max_salarial:,.2f}")
col3.metric("Mínimo Salarial (USD)", f"${min_salarial:,.2f}")
col4.metric("Total de Registros", total_registros)

st.markdown("---")


# Filtragem e agrupamento (antes dos gráficos)
if not df_filtrado.empty:
    empresa_pais = df_filtrado.groupby('pais')['salario_medio_usd'].mean().reset_index()
    empresa_pais['pais_en'] = empresa_pais['pais'].apply(traduzir_pais)
else:
    empresa_pais = pd.DataFrame(columns=['pais', 'salario_medio_usd', 'pais_en'])

# --- Gráficos ---
col_graf1, col_graf2 = st.columns(2)
with col_graf1:
    if not empresa_pais.empty:
        grafico_empresas = px.choropleth(
            empresa_pais,
            locations='pais_en',
            locationmode='country names',
            color='salario_medio_usd',
            title="Média Salarial Mensal por País",
            labels={'pais': 'País', 'salario_medio_usd': 'Média Salarial (USD)'},
            color_continuous_scale=px.colors.sequential.Viridis
        )
        grafico_empresas.update_layout(
            title_x=0.25,
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular')
        )
        st.plotly_chart(grafico_empresas, use_container_width=True)
    else:
        st.write('Nenhum dado disponível para o gráfico de média salarial por país.')


with col_graf2:
    if not df_filtrado.empty:
        fig2 = px.bar(media_anual, x='pais', y='salario_medio_usd',
            color='pais',
            title='Média Salarial Mensal por País',
            labels= {'media_anual': 'Média Salarial (USD)', 'pais': 'País', 'salario_medio_usd': 'Dólar'},
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig2.update_layout(title_x=0.25, xaxis_title='País', yaxis_title='Média Salarial (USD)')
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.write('Nenhum dado disponível para o gráfico de média salarial anual por país e moeda local.')


