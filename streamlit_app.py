# Import python packages
import streamlit as st
import requests
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

st.title("🥤 My Parents New Healthy Diner")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Create Snowflake session using Streamlit secrets
connection_parameters = st.secrets["snowflake"]
session = Session.builder.configs(connection_parameters).create()

rows = (
    session
        .table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
        .select(col("FRUIT_NAME"))
        .sort(col("FRUIT_NAME"))
        .collect()
)

fruit_list = [r["FRUIT_NAME"] for r in rows if r["FRUIT_NAME"] is not None]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
