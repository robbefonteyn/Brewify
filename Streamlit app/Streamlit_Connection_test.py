import streamlit as st
conn = st.connection('mysql', type="sql")


df = conn.query("Select * from beers;", ttl=0)
st.write(df["beer_name"])
