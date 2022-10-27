import streamlit as st
import pandas as pd
import numpy as np
import os
import snowflake.connector  #upm package(snowflake-connector-python==2.7.0)

st.title('Windmills in the US')

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


conn = init_connection()

# Perform query, using st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

query = "select * from TABLE(USWT_DB.conformed.weather_hourly_h3agg_tf(4)) where temp_avg_c <= 0;"
rows = run_query(query)
 
# Print results.
for row in rows:
    st.write(row)       