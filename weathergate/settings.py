import environ
import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Security
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = ['localhost','127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin', # Admin panel -- built-in Django interface to manage database records
    'django.contrib.auth', # Authentication system -- handles users, passwords and permissions
    'django.contrib.contenttypes', # Content types -- tracks all models installed in the project
    'django.contrib.sessions', # Sessions -- stores user session data in the database
    'django.contrib.messages', # Messages -- temporary notification system between requests
    'django.contrib.staticfiles', # Static files -- manages CSS, JS and image files
    # WeatherGate apps
    'accounts', # Handles user registration, login and MFA authentication
    'dashboard', # Handles weather data display and OpenWeatherMap API integration
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', # Enables HTTP security protections (HTTPS, security headers)
    'django.contrib.sessions.middleware.SessionMiddleware', # Manages user sessions (keeps the user "logged in" between pages)
    'django.middleware.common.CommonMiddleware', # Normalizes URLs (e.g. adds trailing "/") and manages basic HTTP headers
    'django.middleware.csrf.CsrfViewMiddleware', # Protects forms against CSRF attacks (Cross-Site Request Forgery). Ensures forms only accept requests from the site itself
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Associates the authenticated user with each request (request.user)
    'django.contrib.messages.middleware.MessageMiddleware', # Manages temporary messages between pages (e.g. "Login successful!")
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protects against Clickjacking attacks — prevents the site from being. # loaded inside an iframe on a malicious external site
]

ROOT_URLCONF = 'weathergate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'weathergate.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Authentication
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'