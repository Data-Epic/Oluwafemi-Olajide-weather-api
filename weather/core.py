# Import built-in and external modules
import os  # For accessing environment variables (like API key)
import requests  # For sending HTTP requests to the API
from datetime import datetime  # For handling and formatting date/time
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load the .env file where API key is stored
load_dotenv()

# Define a class to handle weather-related functionality
class WeatherClient:
    def __init__(self):
        # Get API key from the environment (.env file)
        self.api_key = os.getenv("WEATHER_API_KEY")

        # Define base URLs for current weather and 5-day forecast
        self.current_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    def get_weather(self, city, forecast=False):
        """
        This method fetches weather data from the API.
        - If forecast=False, it fetches current weather.
        - If forecast=True, it fetches 5-day forecast.
        """
        params = {
            'q': city,                # City name entered by the user
            'appid': self.api_key,   # API key for authentication
            'units': 'metric'        # Use Celsius instead of Kelvin
        }

        # Choose the correct API URL depending on whether forecast is requested
        url = self.forecast_url if forecast else self.current_url

        # Make a GET request to the OpenWeatherMap API
        response = requests.get(url, params=params)

        # Raise an error if something went wrong (e.g., wrong city name or invalid key)
        response.raise_for_status()

        # Return the JSON response (converted to a Python dictionary)
        return response.json()

    def process_current_weather(self, data):
        """
        This method extracts and formats data from the current weather response.
        Returns a dictionary with only the useful weather info.
        """
        if not data:
            return None  # Handle empty or missing data safely

        return {
            'city': data['name'],  # Name of the city
            'temp': data['main']['temp'],  # Temperature in Celsius
            'conditions': data['weather'][0]['description'],  # Description (e.g., "clear sky")
            'humidity': data['main']['humidity'],  # Humidity percentage
            'wind': data['wind']['speed']  # Wind speed
        }

    def process_forecast(self, data):
        """
        This method extracts and formats data from the 5-day forecast response.
        It loops through the forecast list and prepares readable info.
        """
        if not data:
            return None  # Handle if forecast data is missing

        forecasts = []  # Create a list to store each time-slot's forecast

        for entry in data['list']:  # Loop through each 3-hour forecast entry
            # Convert the date/time string to a Python datetime object
            time = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')

            # Add cleaned-up forecast data to the list
            forecasts.append({
                'date': time.strftime('%A, %b %d'),  # Format: e.g., "Tuesday, Apr 10"
                'time': time.strftime('%I:%M %p').lstrip('0'),  # Format: e.g., "9:00 AM"
                'temp': entry['main']['temp'],  # Temperature
                'conditions': entry['weather'][0]['description']  # Weather description
            })

        return forecasts  # Return the list of forecasts
