import pytest  # Pytest is the testing framework we use
from unittest.mock import MagicMock  # Used to create fake/mock objects
from weather.core import WeatherClient  # Import the main class we are testing
import requests  # This is the library used to make HTTP requests in the app


# --- REUSABLE MOCK CREATOR --- #

def make_mock_response(status_code):
    """
    This helper function creates a mock version of a requests.get response
    that simulates an error happening with a specific status code (like 500 or 504).
    
    Why? Instead of actually calling the internet/API, we "fake" it in tests.

    Args:
        status_code (int): The HTTP error code you want to simulate (e.g., 500 or 504).

    Returns:
        MagicMock: A mocked response that will raise an HTTPError with that code.
    """
    response = MagicMock()  # Create a fake response object
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        f"{status_code} Server Error"
    )  # When .raise_for_status() is called, it will raise an HTTPError
    return response


# --- TEST: Server error on CURRENT weather request --- #

def test_current_weather_server_error(monkeypatch):
    """
    This test checks how WeatherClient behaves when the API returns a 500 error
    (which means 'Internal Server Error') while fetching **current** weather data.

    We mock the API call to simulate this error and verify that our app raises the right exception.
    """
    client = WeatherClient()  # Create an instance of our app class

    # Monkeypatch replaces the real requests.get function with our fake one
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: make_mock_response(500))

    # We expect an HTTPError to be raised because of the 500 mock
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.get_weather("London", forecast=False)  # Try to get current weather

    # Make sure the error message contains "500"
    assert "500" in str(exc_info.value)


# --- TEST: Server error on FORECAST weather request --- #

def test_forecast_weather_server_error(monkeypatch):
    """
    Similar to the test above, but this time we're checking how the client reacts
    to a 504 Gateway Timeout when trying to get the **forecast**.

    Again, we simulate the API error and check that the right exception is raised.
    """
    client = WeatherClient()

    # Simulate a 504 error for forecast
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: make_mock_response(504))

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.get_weather("London", forecast=True)  # Try to get 5-day forecast

    assert "504" in str(exc_info.value)


# --- TEST: Invalid city triggers 404 --- #

def test_invalid_city(monkeypatch):
    """
    This test checks what happens when the user inputs a city name that doesn't exist.

    We simulate a 404 error response from the API to make sure our app handles it gracefully.
    """
    client = WeatherClient()

    def mock_get(*args, **kwargs):
        # Simulate a 404 error when .raise_for_status() is called
        response = MagicMock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: city not found"
        )
        return response

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.get_weather("NoCityWithThisName123")  # Use a fake city

    assert "404" in str(exc_info.value)
