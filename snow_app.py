import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# Initialize connection.
# Uses st.experimental_singleton to only run once.

@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

st.snow()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
run_query("USE ROLE MONITORAMENTO")   
run_query("USE DATABASE TRADE")
run_query("USE WAREHOUSE WH_PBI")
run_query("USE SCHEMA CURATED_DATA")

rows = run_query("SELECT COUNT(1) AS QTDE, TO_VARCHAR(YEAR(DATAHORA)) AS YEAR, ID_DATABASE FROM PEDIDOS WHERE YEAR(DATAHORA) = 2021 GROUP BY ID_DATABASE, YEAR(DATAHORA) ORDER BY QTDE DESC")

df = pd.DataFrame(rows)

st.header("EVOLUÇÃO DE PEDIDOS DO TRADE ! Baratona!")

if st.checkbox('Show raw data'):
    
    st.write(df)

st.subheader("Visual")

# Qtd. Pedidos 2021
fig = px.bar(x = df[2],
            y = df[0],
            orientation='v', title=" Qtd. Pedidos 2021 x Indústria",
             labels={'x':'Indústria','y':'Qtd. Pedidos'})
st.plotly_chart(fig)

rows2 = run_query("SELECT COUNT(1) AS QTDE, TO_VARCHAR(YEAR(DATAHORA)) AS YEAR FROM PEDIDOS WHERE YEAR(DATAHORA) BETWEEN '2016' AND '2021' GROUP BY YEAR(DATAHORA) ORDER BY YEAR")

df2 = pd.DataFrame(rows2)

# Qtd. Pedidos 2021
fig = px.bar(x = df2[1],
            y = df2[0],
            orientation='v', title=" Qtd. Pedidos por ano(Entre 2016 e 2021)",
             labels={'x':'Ano','y':'Qtd. Pedidos'})
st.plotly_chart(fig)
st.caption('* Dados não calculados!')
