import unittest
from unittest.mock import patch, MagicMock
import builtins

# Import the run_cmd_line function from your cmd_line module
# Assuming your file structure looks like: weather/cmd_line.py
from weather.cmd_line import run_cmd_line


class TestCmdLineWeatherApp(unittest.TestCase):
    """
    Test class for the command-line weather app (run_cmd_line function).
    Uses mock input and output to simulate user behavior.
    """

    @patch('weather.cmd_line.WeatherClient')  # Mock the WeatherClient so no real API calls are made
    @patch('builtins.input')  # Mock input() to simulate user typing in the terminal
    @patch('builtins.print')  # Mock print() so we can capture output if needed
    def test_run_cmd_line_with_mocked_city(self, mock_print, mock_input, MockWeatherClient):
        """
        Test user entering a valid city and then quitting the app.
        """
        # Simulate user inputs:
        # First input: user enters "Lagos"
        # Second input: user enters "quit" to exit
        mock_input.side_effect = ["Lagos", "quit"]

        # Create a fake weather response for current weather
        fake_current = {
            "city": "Lagos",
            "temp": 30,
            "conditions": "clear",
            "humidity": 70,
            "wind": 5
        }

        # Create a fake forecast (shortened for demo)
        fake_forecast = [
            {"date": "2025-04-13", "time": "12:00", "temp": 30, "conditions": "clear"},
            {"date": "2025-04-13", "time": "15:00", "temp": 31, "conditions": "sunny"},
        ]

        # Setup the mocked WeatherClient behavior
        mock_client_instance = MockWeatherClient.return_value
        mock_client_instance.get_weather.side_effect = lambda city, forecast=False: "mocked_data"
        mock_client_instance.process_current_weather.return_value = fake_current
        mock_client_instance.process_forecast.return_value = fake_forecast

        # Run the command line function with the mocked inputs
        run_cmd_line()

        # Check that get_weather was called at least twice (once for current, once for forecast)
        self.assertEqual(mock_client_instance.get_weather.call_count, 2)
        mock_client_instance.process_current_weather.assert_called_once()
        mock_client_instance.process_forecast.assert_called_once()

        # Optional: Check if a specific message was printed
        mock_print.assert_any_call("======= Weather APP =======")
        mock_print.assert_any_call("Goodbye! ")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_quit_immediately(self, mock_print, mock_input):
        """
        Test that the program quits gracefully when user types 'quit' immediately.
        """
        mock_input.side_effect = ["quit"]
        run_cmd_line()

        # Check that goodbye message is printed
        mock_print.assert_any_call("Goodbye! ")

