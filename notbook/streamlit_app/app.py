import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Meu App", layout="wide")

st.title("Exemplo de App Streamlit com Pandas & NumPy")

st.write("""
Este é um exemplo simples para validar execução local.
Carregue um CSV e veja os dados tratados.
""")

uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📌 Dados originais")
    st.dataframe(df)

    st.subheader("📌 Estatísticas Numéricas (NumPy)")
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) > 0:
        stats = df[numeric_cols].describe()
        st.dataframe(stats)
    else:
        st.warning("Não há colunas numéricas para análise.")

st.write("---")
st.write("Feito com ❤️ usando Streamlit + Pandas + NumPy")
