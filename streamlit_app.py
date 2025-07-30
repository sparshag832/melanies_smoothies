# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"This Is My First Streamlit App :cup_with_straw: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_on_order=st.text_input('Name On Smoothie')
st.write("The name on your Smoothie will be",name_on_order)


cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list=st.multiselect('Choosing upto 5 ingredients:',my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+' '
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True) 

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

# Button to trigger insert
time_to_insert = st.button("Submit Order")

if time_to_insert:
    # Run the query
    session.sql(my_insert_stmt).collect()

    # Show success message
    st.success(f"✅Your Smoothie is ordered, {name_on_order}!")




