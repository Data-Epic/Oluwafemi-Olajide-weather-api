import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from datetime import datetime  # For future time formatting
from weather.core import WeatherClient  # Import weather client


def run_cmd_line():
    """Main function to run the Weather App from the command line."""
    client = WeatherClient()

    # Welcome message
    print("======= Weather APP =======")
    print("Enter one or more city names separated by commas")
    print("Example: Lagos, Paris, New York\n")

    while True:
        # Get user input
        cities_input = input("\nEnter cities (or 'quit'): ").strip()

        if cities_input.lower() == 'quit':
            print("Goodbye! ")
            break

        # Clean and split input into individual city names
        cities = [city.strip() for city in cities_input.split(",") if city.strip()]

        for city in cities:
            try:
                # Header for each city's result
                print(f"\n{'=' * 30}")
                print(f"=== {city.upper()} ===")
                print(f"{'=' * 30}")

                # Fetch and display current weather
                current = client.process_current_weather(client.get_weather(city))
                if current:
                    print("\nCURRENT WEATHER")
                    print(f"Location   : {current['city']}")
                    print(f"Temperature: {current['temp']}°C")
                    print(f"Conditions : {current['conditions'].capitalize()}")
                    print(f"Humidity   : {current['humidity']}%")
                    print(f"Wind Speed : {current['wind']} m/s")

                # Fetch and display 5-day forecast
                forecast = client.process_forecast(client.get_weather(city, forecast=True))
                if forecast:
                    print("\n5-DAY FORECAST")
                    current_date = ""
                    for entry in forecast:
                        if entry['date'] != current_date:
                            print(f"\n{entry['date']}:")
                            current_date = entry['date']
                        print(f"{entry['time']}: {entry['temp']}°C | {entry['conditions']}")

            except Exception as e:
                error_message = str(e)
                # Check if error is related to a city not found
                if "404" in error_message and "city not found" in error_message.lower():
                    print(f" Invalid city: '{city}' not found. Please check the spelling and try again.")
                else:
                    # For any other errors
                    print(f"  Error getting weather for '{city}': {error_message}")

            print("\n" + "-" * 70)


# Only run if executed directly
if __name__ == "__main__":
    run_cmd_line()
