# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

st.title("🥤 My Parents New Healthy Diner")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Create Snowflake session using Streamlit secrets
connection_parameters = st.secrets["snowflake"]
session = Session.builder.configs(connection_parameters).create()

# Pull FRUIT_NAME and SEARCH_ON from Snowflake
my_dataframe = (
    session
        .table("smoothies.public.fruit_options")
        .select(col("FRUIT_NAME"), col("SEARCH_ON"))
)

# Convert Snowpark DataFrame to Pandas DataFrame
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

        # Look up the API search value from the SEARCH_ON column
        search_on = pd_
