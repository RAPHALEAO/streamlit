import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import plotly.express as px
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

# Valores ausentes
fig = px.bar(x = [0,0,0,0,0,177,0,0,0,0,687,2],
            y = ['PassengerId','Survived','Pclass','Name' ,
     'Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked'],
            orientation='h', title=" Valores faltantes ",
             labels={'x':'Quantidade','y':'Dados'})
st.plotly_chart(fig)

#Tipos de variaveis
fig = px.bar(x = [6,5],
            y = ['Categóricas','Numéricas'],
            orientation='h', title=" Tipos de dados ",
             labels={'x':'Quantidade','y':'Variaves'},width=800, height=400)
st.plotly_chart(fig)

# Grafico de correlção
fig, ax = plt.subplots(figsize=(5, 5))
sns.heatmap(train.corr(), annot=True, cmap='Blues')
ax.set_title('Correlação dos dados')
fig.tight_layout()
st.pyplot(fig)


# Sobreviventes
fig = px.bar(x = ['Sobreviveu (1)' , 'Não Sobreviveu (0)'], y = [342,549],
            title=" Sobreviventes ",labels={'y':'Quantidade','x':'Dado'})
st.plotly_chart(fig)
