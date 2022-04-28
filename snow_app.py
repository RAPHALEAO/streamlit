import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

rows = run_query("SELECT COUNT(1) AS QTDE, TO_VARCHAR(YEAR(DATAHORA)) AS YEAR, ID_DATABASE FROM PEDIDOS GROUP BY ID_DATABASE, YEAR(DATAHORA) ORDER BY YEAR")

df = pd.DataFrame(rows)

st.header("EVOLUÇÃO DE PEDIDOS DO TRADE")

if st.checkbox('Show raw data'):
    
    st.write(df)

st.subheader("Graficozinho")
    
x = [1, 2, 3, 4]

fig = go.Figure()
fig.add_trace(go.Bar(x=x, y=[1, 4, 9, 16]))
fig.add_trace(go.Bar(x=x, y=[6, -8, -4.5, 8]))
fig.add_trace(go.Bar(x=x, y=[-15, -3, 4.5, -8]))
fig.add_trace(go.Bar(x=x, y=[-1, 3, -3, -4]))

fig.update_layout(barmode='relative', title_text='Relative Barmode')
fig.show()
