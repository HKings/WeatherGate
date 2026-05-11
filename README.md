# WeatherGate

A web application that lets you check the current weather for any city in the world, after a secure login.

I built this project because I wanted to work with a real external API and understand how data from the outside world can be integrated into a web application. It turned out to be one of the most practical things I have built so far.

## What it does

After registering and confirming your email, you can log in and search for any city. The app fetches real-time weather data and displays the temperature, humidity and weather description.

## Tech stack

- Python 3.12
- Django 6.0
- PostgreSQL
- OpenWeatherMap API
- pytest + pytest-django
- Tailwind CSS
- Mailtrap (email testing)

## Features

- User registration with email confirmation
- MFA authentication on every login (6-digit code sent by email)
- Token expiration after 10 minutes
- Real-time weather data from any city in the world
- Automated tests for authentication (8 tests passing)

## What I learned

Integrating the OpenWeatherMap API was the moment this stopped feeling like an exercise. Seeing real data appear on the screen for the first time was the kind of thing that makes you want to keep building.

Writing tests with pytest was the biggest challenge. Understanding how to isolate the test database from the real one, and why that matters, took time but was worth it.

## Setup

```bash
git clone https://github.com/HKings/WeatherGate.git
cd WeatherGate
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Create a `.env` file with your credentials:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=your-email-host
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
OPENWEATHER_API_KEY=your-api-key
```

## Then run:

```bash
python manage.py migrate
python manage.py runserver
```