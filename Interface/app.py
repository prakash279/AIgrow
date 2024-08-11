import streamlit as st
import json
from external_file import fetch_mapbox_image, fetch_openweather_data, process_weather_data, fetch_location, process_weather_data
from process_weather_data import process_weather_data
from make_json_format import json_format
from chatbot import bot_response


st.title("AIGrow")

with st.expander("ℹ️ Disclaimer"):
    st.caption(
        """This is a prototype sample of the idea that is created in the ideation
        with real data and values. The model can be used in real-time. The code for 
        now uses synthetic data values which are purely generated and are not something
        to be dependent on."""
    )

weather_data = ""
location = ""
user_query = ""

# Step 1: Input for Longitude and Latitude
if 'step' not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    with st.form("location_form"):
        longitude = st.text_input("Enter Longitude:")
        latitude = st.text_input("Enter Latitude:")
        
        submitted = st.form_submit_button("Next")
        
        if submitted and longitude and latitude:
            st.session_state.longitude = longitude
            st.session_state.latitude = latitude
            img = fetch_mapbox_image(float(latitude), float(longitude))
            weather_text = fetch_openweather_data(float(latitude), float(longitude))
            weather_data = process_weather_data(weather_text)
            location = fetch_location(float(latitude), float(longitude))
            if img:
                st.image(img, caption="Map Image")
                st.write("Weather Forecast:")
                st.write(weather_data)
                st.write(location)
            else:
                st.write("Failed to fetch image.")
            # json_query = json_format(weather_data, location)
            st.session_state.step = 2

if st.session_state.step == 2:
    with st.form("query_form"):
        user_query = st.text_input("Enter your query:")
        submitted = st.form_submit_button("Next")
        
        if submitted and user_query:
            st.session_state.user_query = user_query
            st.session_state.step = 3

if st.session_state.step == 3:
    json_query =  f"{weather_data} \n {location} \n User Query: {user_query}\n"
    st.text_area("Generated Message", value=json_query, height=100)
    if st.button("Next"):
        st.session_state.step = 4

if st.session_state.step == 4:
    output = bot_response(json_query)
    st.text_area("Bot's Response : \n", value=output, height=150)
