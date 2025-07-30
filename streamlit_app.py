# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

# Write directly to the app
st.title(f"Customize Your Smoothie!:cup_with_straw: {st.__version__}")

st.write("Choose The Fuits For Your Custom Smoothie")

name_on_order=st.text_input('Name On Smoothie')
st.write("The name on your Smoothie will be",name_on_order)


cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))

# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list=st.multiselect('Choosing upto 5 ingredients:',my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+' '
        st.subheader(fruit_chosen + ' Nutrition Information')
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




