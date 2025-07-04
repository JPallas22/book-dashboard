import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv("livros.csv")
df.columns = df.columns.str.strip()  # remover espaços extras

st.set_page_config(page_title="Meu Painel de Leitura", layout="wide")
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

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("📘 Total de livros", len(df_filtrado))
col2.metric("✅ Lidos", len(df_filtrado[df_filtrado['Status'].str.lower() == "lido"]))
col3.metric("📖 Lendo", len(df_filtrado[df_filtrado['Status'].str.lower() == "lendo"]))

st.markdown("---")

# Gráfico de status
st.subheader("📊 Distribuição por Status")
fig_status = px.pie(df_filtrado, names='Status', title='Distribuição dos Livros por Status', hole=0.4)
st.plotly_chart(fig_status, use_container_width=True)

# Gráfico de categorias
st.subheader("📚 Livros por Categoria")
fig_categoria = px.bar(df_filtrado['Categoria'].value_counts().reset_index(),
                       x='index', y='Categoria',
                       labels={'index': 'Categoria', 'Categoria': 'Quantidade'},
                       title='Quantidade de Livros por Categoria')
st.plotly_chart(fig_categoria, use_container_width=True)

# Tabela
st.subheader("📋 Tabe
