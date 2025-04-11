import builtins
import pytest
from unittest.mock import patch, MagicMock
from weather import cmd_line


def mock_input_sequence(inputs):
    """Returns a function that mimics built-in input() with a sequence of responses."""
    def mock_input(_prompt=""):
        return inputs.pop(0)
    return mock_input


def test_invalid_city_prints_message(monkeypatch, capsys):
    # Simulate user typing a wrong city, then 'quit'
    inputs = ["FakeCityName", "quit"]
    monkeypatch.setattr(builtins, 'input', mock_input_sequence(inputs))

    # Mock WeatherClient to raise a 404 error for invalid city
    mock_client = MagicMock()
    mock_client.get_weather.side_effect = Exception("404 city not found")

    monkeypatch.setattr(cmd_line, 'WeatherClient', lambda: mock_client)

    # Run the CLI
    cmd_line.run_cmd_line()

    captured = capsys.readouterr()

    # Check that the error message appears
    assert "Invalid city: 'FakeCityName' not found" in captured.out


def test_quit_exits_cleanly(monkeypatch, capsys):
    inputs = ["quit"]
    monkeypatch.setattr(builtins, 'input', mock_input_sequence(inputs))

    # Mock WeatherClient to prevent real API calls
    mock_client = MagicMock()
    monkeypatch.setattr(cmd_line, 'WeatherClient', lambda: mock_client)

    cmd_line.run_cmd_line()

    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out
