import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

st.write("""
        Choose the frutis you want in your custom smoothie!
        """)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

nameOnOrder = st.text_input("Name on Smoothie Order:")
st.write("The name on your Smoothie will be:", nameOnOrder)

ingredient_list = st.multiselect('Choose up to 5 ingredients:', 
                                my_dataframe, 
                                max_selections=5)

if ingredient_list:
    ingredients_string = ""
    
    for fruit in ingredient_list:
        ingredients_string += fruit + " "
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
        insert_statment = """INSERT INTO smoothies.public.orders(ingredients,orderName) 
        VALUES ('""" + ingredients_string + """','""" +nameOnOrder+ """')"""
    
     
        # st.write(insert_statment)
        # st.stop()
        insert = st.button("Submit Order")    
        if insert: 
            session.sql(insert_statment).collect()
            st.success('Your Smoothie ordered!', icon='✅')
