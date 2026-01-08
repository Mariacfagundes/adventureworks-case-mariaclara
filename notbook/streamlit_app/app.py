import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AdventureWorks Analytics", layout="wide")

st.title("📊 AdventureWorks - Data App (Item 9)")

# ======================================================
# Carregamento dos arquivos (fixos)
# ======================================================

import os

BASE = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "fact_sales": os.path.join(BASE, "fact_sales.csv"),
    "dim_product": os.path.join(BASE, "dim_product.csv"),
    "dim_categories": os.path.join(BASE, "dim_categories.csv"),
    "dim_calendar": os.path.join(BASE, "dim_calendar.csv"),
}

dfs = {}

st.subheader("📁 Carregando arquivos")
for name, path in FILES.items():
    try:
        df = pd.read_csv(path)
        dfs[name] = df
        st.success(f"Carregado: {path} ({len(df)} linhas)")
    except Exception as e:
        st.error(f"Erro ao carregar {path}: {e}")

# ======================================================
# Mostrar estruturas
# ======================================================
st.subheader("🧱 Estrutura das tabelas")
for name, df in dfs.items():
    st.write(f"### {name}")
    st.write("Colunas:", list(df.columns))
    st.dataframe(df.head(), use_container_width=True)

# ======================================================
# Função auto-detectora de chaves
# ======================================================
def detect_key(df, keys):
    cols = df.columns.str.lower()
    for k in keys:
        if k in cols.values:
            return df.columns[list(cols).index(k)]
    return None

fact = dfs["fact_sales"]
dim_prod = dfs["dim_product"]
dim_cat = dfs["dim_categories"]
dim_cal = dfs["dim_calendar"]

# ======================================================
# Listas de chaves candidatas
# ======================================================

st.subheader("🔗 Unindo tabelas (Star Schema)")

# join fact + product
df = fact.merge(dim_prod, on="product_key", how="left")

# join calendar
df = df.merge(dim_cal, left_on="order_date", right_on="date", how="left")

st.success("Join realizado com sucesso!")
st.dataframe(df.head(), use_container_width=True)

st.subheader("📈 Métricas Gerais")

total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()
total_margin = df["margin"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Receita Total", f"${total_revenue:,.0f}")
col2.metric("Lucro Total", f"${total_profit:,.0f}")
col3.metric("Margem Média", f"{total_margin:.2%}")

st.subheader("🎛 Filtros")

years = sorted(df["year"].dropna().unique())
selected_year = st.selectbox("Selecione o ano", [None] + list(years))

df_filtered = df.copy()
if selected_year:
    df_filtered = df_filtered[df_filtered["year"] == selected_year]

st.subheader("🏆 Top Produtos (por receita)")

top_prod = df_filtered.groupby("product_name")["revenue"].sum().sort_values(ascending=False).head(10)

st.bar_chart(top_prod)

st.subheader("📅 Receita por mês")

rev_month = df_filtered.groupby("month")["revenue"].sum()

st.line_chart(rev_month)

