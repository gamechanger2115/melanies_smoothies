import requests
import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Smoothie !!   """ )

name_on_order = st.text_input('Name on Smoothie :')
st.write('The Name on Your Smoothie will be :', name_on_order)

cnx = st.connection("snowflake") 
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + '  '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
      
     
    my_insert_stmt = f"INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES ('{ingredients_string}', '{name_on_order}')"

    time_to_insert =  st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    st.success(' Your Smoothie is Ordered !', icon='✅')






