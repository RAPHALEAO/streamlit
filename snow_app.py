import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

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

# ugly hack to embed fonts
matplotlib.rc("pdf", fonttype=42)

edgecolor = "black"

bar_scale = 0.8

plt.figure(figsize=(14, 4))

things = [
    {
        "label": "Quantidade",
        "values": df[0],
        "color": "#00ff00",
    },
    {
        "label": "Ano",
        "values": df[1],
        "color": "#dddddd",
    },
    {
        "label": "Indústria",
        "values": df[2],
        "color": "#afafaf",
    },
]

group_labels = ["Group #1", "Group #2", "Group #3", "Group #4", "Group #5"]

for i, data in enumerate(things):
    x = 1 + np.arange(len(group_labels)) + (i - (len(things) - 1) / 2) * bar_scale / len(things)

    plt.bar(
        x=x,
        height=data["values"],
        width=bar_scale / len(things),
        label=data["label"],
        color=data["color"],
        edgecolor=edgecolor,
        linewidth=0.5,
    )

plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
plt.xticks(1 + np.arange(len(group_labels)), group_labels)
plt.xlim([0.5, len(group_labels) + 0.5])
plt.ylabel("Goodness")
plt.legend()
plt.tight_layout()
plt.show()

st.write(things)
