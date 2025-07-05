import streamlit as st
import pandas as pd
import plotly.express as px

# Cores personalizadas
colors = ['#809671', '#b3b792', '#d2ab80', '#725c3a', '#5d624c', '#868b6b', '#e5d2b8', '#9ca089', '#e1dbcb', '#c5beab']

# Configurações da página
st.set_page_config(page_title="Painel de Leitura", layout="wide", page_icon="📚")
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
status_filter = st.sidebar.multiselect("Filtrar por status:", status_list, default=status_list)

# Filtrando
df_filtrado = df[df['Status'].isin(status_filter)]

# Métricas
total = len(df_filtrado)
lidos = len(df_filtrado[df_filtrado['Status'].str.lower() == "lido"])
desejados = len(df_filtrado[df_filtrado['Status'].str.lower() == "desejado"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("📘 Total de livros", total)
col2.metric("✅ Lidos", lidos)
col4.metric("📝 Desejados", desejados)

st.markdown("---")

# Gráfico de Status
st.subheader("📊 Distribuição por Status")
fig_status = px.pie(df_filtrado, names='Status', hole=0.4,
                    title='Distribuição dos Livros por Status',
                    color_discrete_sequence=colors)
st.plotly_chart(fig_status, use_container_width=True)

# Tabela de livros
st.subheader("📋 Lista de Livros")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
