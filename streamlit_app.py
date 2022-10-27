import os
import streamlit as st
import numpy as np
import snowflake.connector  #upm package(snowflake-connector-python==2.7.0)
 
 
# Initialize connection, using st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    con = snowflake.connector.connect(
        user=os.getenv("SF_USER"),
        password=os.getenv("SF_PASSWORD"),
        account=os.getenv("SF_ACCOUNT"),
        role=os.getenv("SF_ROLE"),
        warehouse=os.getenv("SF_WAREHOUSE"),
    )
    return con
 
 
# Perform query, using st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()
 
 
# rows = run_query("SHOW TABLES;")
conn = init_connection()
 
query = "select city, state_id, ranking, lat, lng from citibike.geodemo.SIMPLEMAP_US_CITIES where rnaking = 1;"
rows = run_query(query)
 

st.subheader('Cities By Ranking')
st.map(rows)
