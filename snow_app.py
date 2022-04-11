import streamlit as st
import snowflake.connector

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
run_query("USE DATABASE MONITORAMENTO")
run_query("USE WAREHOUSE WHDEV")
run_query("USE SCHEMA LOG")

rows = run_query("SELECT * FROM LOG LIMIT 1")

# Print results.
for row in rows:
    st.write(f"{row[0]}")
