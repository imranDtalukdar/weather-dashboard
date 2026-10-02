import streamlit as st
import requests

st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="centered")

st.title("🌤️ Live Weather Dashboard")
st.write("Type in any city name to get the current temperature, wind speed, and weather conditions!")

# City input box
city = st.text_input("Enter City Name:", "London")

if st.button("Get Weather"):
    try:
        # Step 1: Get latitude and longitude for the city using Open-Meteo's geocoding API
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url).json()

        if "results" not in geo_response:
            st.error(f"City '{city}' not found. Please try another name!")
        else:
            location = geo_response["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            country = location.get("country", "")

            # Step 2: Get current weather using coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_2m"
            weather_data = requests.get(weather_url).json()

            current = weather_data["current"]
            temp = current["temperature_2m"]
            humidity = current["relative_humidity_2m"]
            wind = current["wind_speed_2m"]

            # Step 3: Display results nicely on the website
            st.success(f"Weather for {location['name']}, {country}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{temp}°C")
            col2.metric("Humidity", f"{humidity}%")
            col3.metric("Wind Speed", f"{wind} km/h")

    except Exception as e:
        st.error("An error occurred while fetching the weather. Please try again.")

st.markdown("---")
st.write("Built with Python & Streamlit")