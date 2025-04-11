import sys
from pathlib import Path
import streamlit as st
from datetime import datetime

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from weather.core import WeatherClient

client = WeatherClient()

st.title("🌦️ Weather Dashboard")

# City input
city = st.text_input("Enter city name", placeholder="E.g., London, Tokyo, New York")

# Forecast interval selector
interval = st.selectbox(
    "Forecast interval",
    options=["3 hours", "6 hours", "12 hours"],
    index=2  # Default to 12 hours
)

# Convert interval selection to API units
interval_hours = int(interval.split()[0])
entries_to_skip = interval_hours // 3  # Since API gives 3-hour intervals

if city:
    try:
        # Get weather data
        current = client.process_current_weather(client.get_weather(city))
        forecast_data = client.get_weather(city, forecast=True)
        
        if not current or not forecast_data:
            st.error(f"Could not get weather data for {city}")
            st.stop()
        
        # Process forecast with selected interval
        def process_custom_interval_forecast(forecast_data, skip):
            forecast_items = forecast_data['list']
            custom_forecast = []
            
            for i in range(0, len(forecast_items), skip):
                item = forecast_items[i]
                time = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
                custom_forecast.append({
                    'date': time.strftime('%A, %b %d'),
                    'time': time.strftime('%I:%M %p').lstrip('0'),
                    'temp': item['main']['temp'],
                    'conditions': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'humidity': item['main']['humidity'],
                    'wind': item['wind']['speed']
                })
            return custom_forecast
        
        forecast = process_custom_interval_forecast(forecast_data, entries_to_skip)
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        # Current weather column
        with col1:
            st.header(f"Current Weather in {current['city']}")
            st.metric("Temperature", f"{current['temp']}°C")
            st.write(f"**Conditions:** {current['conditions'].capitalize()}")
            st.write(f"**Humidity:** {current['humidity']}%")
            st.write(f"**Wind:** {current['wind']} m/s")
        
        # Forecast column
        with col2:
            st.header(f"{interval} Forecast for {current['city']}")
            
            current_date = ""
            for entry in forecast:
                if entry['date'] != current_date:
                    st.subheader(entry['date'])
                    current_date = entry['date']
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    icon_url = f"http://openweathermap.org/img/wn/{entry['icon']}@2x.png"
                    st.image(icon_url, width=40)
                
                with col2:
                    st.write(
                        f"{entry['time']}: "
                        f"**{entry['temp']}°C** | "
                        f"{entry['conditions'].capitalize()}"
                    )
                    st.caption(f"💧 {entry['humidity']}% | 🌬️ {entry['wind']} m/s")
                
                st.write("---")
    
    except Exception as e:
        st.error(f"Error getting weather data: {str(e)}")