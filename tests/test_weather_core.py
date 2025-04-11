import pytest
from unittest.mock import patch, MagicMock
from weather.core import WeatherClient
import requests


# Simulate HTTP 500 and 504 errors using mock
@pytest.mark.parametrize("status_code", [500, 504])
def test_server_errors(monkeypatch, status_code):
    client = WeatherClient()

    def mock_get(*args, **kwargs):
        response = MagicMock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"{status_code} Server Error")
        return response

    # Patch 'requests.get' to raise server error
    monkeypatch.setattr("requests.get", mock_get)

    # Test current weather call
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.get_weather("London", forecast=False)
    assert str(status_code) in str(exc_info.value)

    # Test forecast call
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.get_weather("London", forecast=True)
    assert str(status_code) in str(exc_info.value)


# Simulate a 404 error for invalid city
def test_invalid_city(monkeypatch):
    client = WeatherClient()

    def mock_get(*args, **kwargs):
        response = MagicMock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: city not found")
        return response

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.get_weather("NoCityWithThisName123")
    assert "404" in str(exc_info.value)