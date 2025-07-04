import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('livros.csv')

# Título
st.title("📚 Meu KindleLícia")

# Limpar nomes de colunas
df.columns = df.columns.str.strip()

# Filtros
status_options = st.multiselect("Filtrar por status:", df['Status'].unique(), default=df['Status'].unique())
categoria_options = st.multiselect("Filtrar por categoria:", df['Categoria'].dropna().unique(), default=df['Categoria'].dropna().unique())

df_filtrado = df[df['Status'].isin(status_options) & df['Categoria'].isin(categoria_options)]

# Métricas principais
st.metric("Total de livros", len(df_filtrado))
st.metric("Livros lidos", len(df_filtrado[df_filtrado['Status'].str.lower() == 'lido']))

# Gráfico de status
st.subheader("📊 Distribuição por Status")
status_count = df_filtrado['Status'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(status_count, labels=status_count.index, autopct='%1.1f%%')
ax1.axis('equal')
st.pyplot(fig1)

# Gráfico de categorias
st.subheader("📚 Categorias mais lidas")
categoria_count = df_filtrado['Categoria'].value_counts().head(10)
st.bar_chart(categoria_count)

# Tabela com detalhes
st.subheader("📋 Lista de Livros")
st.dataframe(df_filtrado.reset_index(drop=True))
