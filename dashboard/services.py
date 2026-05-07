import requests
from django.conf import settings

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
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon']
            }
        return None
    
    except requests.exceptions.RequestException:
        return None