import streamlit as st
import pandas as pd
import plotly.express as px

# Cores personalizadas
colors = ['#809671', '#b3b792', '#d2ab80', '#725c3a', '#5d624c', '#868b6b', '#e5d2b8', '#9ca089', '#e1dbcb', '#c5beab']

# Configurações da página
st.set_page_config(page_title="Meu Painel de Leitura", layout="wide", page_icon="📚")
st.markdown("""
    <style>
    body {
        background-color: #e5e0d8;
        color: #5d624c;
    }
    .stApp {
        background-color: #e5e0d8;
    }
    .stDataFrame {
        background-color: #e1dbcb;
    }
    </style>
    """, unsafe_allow_html=True)

# Carregar dados
df = pd.read_csv("livros.csv")
df.columns = df.columns.str.strip()

st.title("📚 Meu Dashboard de Leitura")

# Filtros
status_list = df['Status'].dropna().unique().tolist()
categoria_list = df['Categoria'].dropna().unique().tolist()

with st.sidebar:
    st.header("🔎 Filtros")
    status_filter = st.multiselect("Status", status_list, default=status_list)
    categoria_filter = st.multiselect("Categoria", categoria_list, default=categoria_list)

# Filtrando
df_filtrado = df[df['Status'].isin(status_filter) & df['Categoria'].isin(categoria_filter)]

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("📘 Total de livros", len(df_filtrado))
col2.metric("✅ Lidos", len(df_filtrado[df_filtrado['Status'].str.lower() == "lido"]))
col3.metric("📖 Lendo", len(df_filtrado[df_filtrado['Status'].str.lower() == "lendo"]))

st.markdown("---")

# Gráfico de status
st.subheader("📊 Distribuição por Status")
fig_status = px.pie(df_filtrado, names='Status', hole=0.4,
                    title='Distribuição dos Livros por Status',
                    color_discrete_sequence=colors)
st.plotly_chart(fig_status, use_container_width=True)

# Gráfico de categorias
st.subheader("📚 Livros por Categoria")
categoria_count = df_filtrado['Categoria'].value_counts().reset_index()
categoria_count.columns = ['Categoria', 'Quantidade']

fig_categoria = px.bar(categoria_count,
                       x='Categoria', y='Quantidade',
                       labels={'Categoria': 'Categoria', 'Quantidade': 'Quantidade'},
                       title='Quantidade de Livros por Categoria',
                       color='Categoria',
                       color_discrete_sequence=colors)
st.plotly_chart(fig_categoria, use_container_width=True)

# Tabela
st.subheader("📋 Tabela de Livros")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
