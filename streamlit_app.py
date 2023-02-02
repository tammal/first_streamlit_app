import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("Training")
streamlit.header('Fruityvice Fruit Advice')
streamlit.text('Omega 3 & Blueberry oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruit_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruit_selected]
streamlit.dataframe(fruits_to_show)
try:
  fruit_choice = streamlit.text_input('Chose fruit','Kiwi')

  streamlit.write('The user entered ',fruit_choice)

  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

  streamlit.dataframe(fruityvice_normalized)

  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  my_cur.execute("select * from fruit_load_list")
  my_data_row = my_cur.fetchall()
  streamlit.header("The fruit list contains:")
  streamlit.dataframe(my_data_row)

  fruit_to_add = streamlit.text_input('what fruit would you like to add?' ,'jackfruit')
  my_cur.execute("insert into fruit_load_list values('%').format(fruit_to_add)")
  
error URLError as e:
  streamlit.error()
                                    
