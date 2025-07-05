import streamlit as st
import pandas as pd
import plotly.express as px

# Cores definidas
cor_fundo = "#e1dbcb"
cor_destaque = "#725c3a"
cor_texto = "#5d624c"
cores_plotly = [cor_destaque, cor_texto, "#a89c8a", "#c8bca8", "#918a7a"]

# Configuração visual do Streamlit
st.set_page_config(page_title="Meu KindleLícia", layout="wide", page_icon="📚")
st.markdown(f"""
    <style>
        html, body, [class*="css"] {{
            background-color: {cor_fundo};
            color: {cor_texto};
        }}
        .stApp {{
            background-color: {cor_fundo};
        }}
        .stDataFrame {{
            background-color: {cor_fundo};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {cor_destaque};
        }}
    </style>
    """, unsafe_allow_html=True)

# Carregar os dados
df = pd.read_csv("livros.csv")
df.columns = df.columns.str.strip()

st.title("📚 Meu KindleLícia")

# Filtros laterais
status_list = df['Status'].dropna().unique().tolist()
status_filter = st.sidebar.multiselect("Filtrar por status:", status_list, default=status_list)

# Aplicar filtros
df_filtrado = df[df['Status'].isin(status_filter)]

# Métricas principais
total = len(df_filtrado)
lidos = len(df_filtrado[df_filtrado['Status'].str.lower() == "lido"])
desejados = len(df_filtrado[df_filtrado['Status'].str.lower() == "desejado"])

col1, col2, col3 = st.columns(3)
col1.metric("📘 Total de livros", total)
col2.metric("✅ Lidos", lidos)
col3.metric("📝 Desejados", desejados)

st.markdown("---")

# Gráfico de pizza por status
st.subheader("📊 Distribuição por Status")
fig_status = px.pie(df_filtrado, names='Status', hole=0.4,
                    title='Distribuição dos Livros por Status',
                    color_discrete_sequence=cores_plotly)
st.plotly_chart(fig_status, use_container_width=True)

# Tabela
st.subheader("📋 Lista de Livros")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
