import requests
from django.conf import settings
from datetime import datetime, timezone


def get_weather(city):
    """
    Fetches current weather data from OpenWeatherMap API.
    Returns a dictionary with weather details or None if the request fails.
    """
    api_key = settings.OPENWEATHER_API_KEY
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en'

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            # Convert sunrise and sunset from Unix timestamp to readable time
            sunrise = datetime.fromtimestamp(data['sys']['sunrise'], tz=timezone.utc).strftime('%H:%M')
            sunset = datetime.fromtimestamp(data['sys']['sunset'], tz=timezone.utc).strftime('%H:%M')

            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
                'wind_speed': round(data['wind']['speed'] * 3.6),
                'pressure': data['main']['pressure'],
                'visibility': round(data.get('visibility', 0) / 1000),
                'sunrise': sunrise,
                'sunset': sunset,
            }
        return None

    except requests.exceptions.RequestException:
        return None