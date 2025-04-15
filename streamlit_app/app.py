# 🔧 Import core libraries and modules
import os  
import sys  # Used to manipulate Python runtime environment (e.g., system paths)
from pathlib import Path  # Helps work with file system paths across operating systems
import streamlit as st  # Streamlit library for creating interactive web apps
from datetime import datetime  # Used for handling and formatting date/time data
from weather.core import WeatherClient

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




#  Create an instance of the WeatherClient to make API calls
client = WeatherClient()

#  Streamlit page title
st.title("🌦️ Weather Dashboard")

#  Input box for user to type a city name (e.g., "London", "Tokyo", etc.)
city = st.text_input("Enter city name", placeholder="E.g., London, Tokyo, New York")

#  Forecast interval dropdown selection
interval = st.selectbox(
    "Forecast interval",  # Label text
    options=["3 hours", "6 hours", "12 hours"],  # Available choices
    index=2  # Default selection is "12 hours"
)

#  Convert the selected interval (e.g., "12 hours") into number of 3-hour API blocks
interval_hours = int(interval.split()[0])  # Extract number (e.g., "12")
entries_to_skip = interval_hours // 3  # Since the API returns data in 3-hour chunks

#  If a city is entered, fetch and display weather data
if city:
    try:
        #  Get current weather for the city
        current = client.process_current_weather(client.get_weather(city))
        
        #  Get forecast weather (next 5 days in 3-hour intervals)
        forecast_data = client.get_weather(city, forecast=True)
        
        #  Handle missing/invalid responses
        if not current or not forecast_data:
            st.error(f"Could not get weather data for {city}")
            st.stop()  # Stop further processing

        #  Process forecast data to match the user's chosen interval
        def process_custom_interval_forecast(forecast_data, skip):
            forecast_items = forecast_data['list']  # List of all forecast entries
            custom_forecast = []  # To store reduced forecast list
            
            # Loop through the data at intervals (e.g., every 4th item for 12 hours)
            for i in range(0, len(forecast_items), skip):
                item = forecast_items[i]
                time = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')  # Convert string to datetime
                
                # Extract relevant details into a cleaner format
                custom_forecast.append({
                    'date': time.strftime('%A, %b %d'),  # e.g., "Sunday, Apr 13"
                    'time': time.strftime('%I:%M %p').lstrip('0'),  # e.g., "3:00 PM"
                    'temp': item['main']['temp'],  # Temperature
                    'conditions': item['weather'][0]['description'],  # Weather conditions
                    'icon': item['weather'][0]['icon'],  # Icon ID for weather image
                    'humidity': item['main']['humidity'],  # Humidity %
                    'wind': item['wind']['speed']  # Wind speed
                })
            return custom_forecast

        #  Apply custom interval processing
        forecast = process_custom_interval_forecast(forecast_data, entries_to_skip)

        #  Create two columns: one for current weather, one for forecast
        col1, col2 = st.columns(2)

        #  Column 1: Current weather info
        with col1:
            st.header(f"Current Weather in {current['city']}")
            st.metric("Temperature", f"{current['temp']}°C")  # Big bold number
            st.write(f"**Conditions:** {current['conditions'].capitalize()}")  # Weather description
            st.write(f"**Humidity:** {current['humidity']}%")  # Humidity %
            st.write(f"**Wind:** {current['wind']} m/s")  # Wind speed

        #  Column 2: Forecast info
        with col2:
            st.header(f"{interval} Forecast for {current['city']}")

            current_date = ""  # Track date to group forecasts by day

            for entry in forecast:
                # If new day, display date header
                if entry['date'] != current_date:
                    st.subheader(entry['date'])  # e.g., "Sunday, Apr 13"
                    current_date = entry['date']

                # Divide each forecast entry into icon + info columns
                col1, col2 = st.columns([1, 3])
                with col1:
                    icon_url = f"http://openweathermap.org/img/wn/{entry['icon']}@2x.png"
                    st.image(icon_url, width=40)  # Weather icon

                with col2:
                    st.write(
                        f"{entry['time']}: "
                        f"**{entry['temp']}°C** | "
                        f"{entry['conditions'].capitalize()}"
                    )
                    st.caption(f"💧 {entry['humidity']}% | 🌬️ {entry['wind']} m/s")

                st.write("---")  # Divider between entries

    #  Handle unexpected errors gracefully
    except Exception as e:
        st.error(f"Error getting weather data: {str(e)}")
