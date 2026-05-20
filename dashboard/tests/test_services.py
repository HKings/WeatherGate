import pytest
from unittest.mock import patch, Mock
from dashboard.services import get_weather


class TestGetWeather:

    def test_get_weather_returns_correct_data(self):
        # Simulates a successful API response without making a real HTTP request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Lisbon',
            'sys': {'country': 'PT'},
            'main': {
                'temp': 18.4,
                'feels_like': 17.1,
                'humidity': 65
            },
            'weather': [{'description': 'scattered clouds', 'icon': '03d'}]
        }

        with patch('dashboard.services.requests.get', return_value=mock_response):
            result = get_weather('Lisbon')

        assert result['city'] == 'Lisbon'
        assert result['country'] == 'PT'
        assert result['temperature'] == 18
        assert result['feels_like'] == 17
        assert result['humidity'] == 65
        assert result['description'] == 'Scattered clouds'
        assert result['icon'] == '03d'

    def test_get_weather_returns_none_when_city_not_found(self):
        # Simulates a 404 response from the API (city not found)
        mock_response = Mock()
        mock_response.status_code = 404

        with patch('dashboard.services.requests.get', return_value=mock_response):
            result = get_weather('InvalidCityXYZ')

        assert result is None

    def test_get_weather_returns_none_on_connection_error(self):
        # Simulates a network error (timeout, no connection, etc.)
        import requests
        with patch('dashboard.services.requests.get', side_effect=requests.exceptions.RequestException):
            result = get_weather('Lisbon')

        assert result is None