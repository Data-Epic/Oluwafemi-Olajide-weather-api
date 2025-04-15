import sys   # sys lets us interact with the Python interpreter (e.g., to change the module search path)
import os    # os lets us work with file paths, directories, and operating system functions

# This line adds the parent directory of the current file to Python’s module search path.
# It allows us to import modules from the main package directory (e.g., `weather.core`)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from datetime import datetime  # We import datetime in case we want to format or compare time
from weather.core import WeatherClient  # This is our custom class that handles fetching and processing weather data


def run_cmd_line():
    """
    This is the main function that runs the Weather App from the command line.
    It continuously prompts the user for city names and displays weather info.
    """
    client = WeatherClient()  # Create an instance of WeatherClient to handle API requests

    # Display a welcome message
    print("======= Weather APP =======")
    print("Enter one or more city names separated by commas")
    print("Example: Lagos, Paris, New York\n")

    # Start an infinite loop that keeps running until the user types 'quit'
    while True:
        # Ask the user for city names, separated by commas
        cities_input = input("\nEnter cities (or 'quit'): ").strip()

        # If the user types 'quit' (case-insensitive), exit the program
        if cities_input.lower() == 'quit':
            print("Goodbye! ")
            break  # Exit the loop and stop the program

        # Split the input string by commas, remove any extra spaces, and filter out empty strings
        cities = [city.strip() for city in cities_input.split(",") if city.strip()]

        # Loop through each city the user entered
        for city in cities:
            try:
                # Print a header with the city name in uppercase
                print(f"\n{'=' * 30}")  # prints "=============================="
                print(f"=== {city.upper()} ===")  # prints "=== LAGOS ===" for example
                print(f"{'=' * 30}")

                # --------- CURRENT WEATHER ----------
                # Step 1: Get raw weather data using the WeatherClient
                # Step 2: Process the current weather part of the data
                current = client.process_current_weather(client.get_weather(city))
                if current:
                    # Display the processed current weather data
                    print("\nCURRENT WEATHER")
                    print(f"Location   : {current['city']}")
                    print(f"Temperature: {current['temp']}°C")
                    print(f"Conditions : {current['conditions'].capitalize()}")  # Make the first letter uppercase
                    print(f"Humidity   : {current['humidity']}%")
                    print(f"Wind Speed : {current['wind']} m/s")

                # --------- 5-DAY FORECAST ----------
                # Similar process but for forecasted data (future weather)
                forecast = client.process_forecast(client.get_weather(city, forecast=True))
                if forecast:
                    print("\n5-DAY FORECAST")
                    current_date = ""  # Keeps track of the last date printed so we don’t repeat it
                    for entry in forecast:
                        # If we’ve reached a new date, print it
                        if entry['date'] != current_date:
                            print(f"\n{entry['date']}:")  # prints date only once per day
                            current_date = entry['date']
                        # Show time, temperature, and conditions (e.g., 12:00: 28°C | sunny)
                        print(f"{entry['time']}: {entry['temp']}°C | {entry['conditions']}")

            except Exception as e:
                # Catch any error that happens during processing
                error_message = str(e)

                # If the error message contains "404" and "city not found", show a friendly message
                if "404" in error_message and "city not found" in error_message.lower():
                    print(f" Invalid city: '{city}' not found. Please check the spelling and try again.")
                else:
                    # Otherwise, show a generic error message
                    print(f"  Error getting weather for '{city}': {error_message}")

            # Separate the output visually for each city
            print("\n" + "-" * 70)  # prints a line like -----------------------------


# This special check ensures that the run_cmd_line function only runs
# when this file is executed directly, not when it's imported as a module.
if __name__ == "__main__":
    run_cmd_line()
