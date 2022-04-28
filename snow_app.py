import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np

# Initialize connection.
# Uses st.experimental_singleton to only run once.

@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

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

rows = run_query("SELECT COUNT(1) AS QTDE, MONTH(DATAHORA) AS MONTH, YEAR(DATAHORA) AS YEAR, ID_DATABASE FROM PEDIDOS GROUP BY ID_DATABASE, MONTH(DATAHORA), YEAR(DATAHORA) ORDER BY YEAR, MONTH")

df = pd.DataFrame(rows)

# Print results.
st.header("Logs de execução das procedures no Snowflake")
st.subheader("últimos 10")
st.write(df)

rows2 = run_query("SELECT * FROM LOG_VERIFICA_MACHADO")

df2 = pd.DataFrame(rows2)

st.header("Verifica Machado")
st.write(df2)
