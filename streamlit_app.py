# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

st.title("🥤 My Parents New Healthy Diner")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# NEW for SniS: create session using Streamlit secrets (will be configured later)
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
    fruit_list,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!", icon="✅")

# New section to display SmoothieFroot nutrition information
import requests

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

# Put the JSON into a dataframe
sf_df = st.dataframe(
    data=smoothiefroot_response.json(),
    use_container_width=True
)
