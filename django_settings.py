# Add to your settings.py

INSTALLED_APPS = [
    # ... your existing apps
    'chatbot',
    'corsheaders',  # For CORS support with Vue.js frontend
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... your existing middleware
]

# CORS settings for Vue.js frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",  # If using different port
]

CORS_ALLOW_CREDENTIALS = True

# For development only - remove in production
CORS_ALLOW_ALL_ORIGINS = True

# Database configuration (example for PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chatbot_db',
        'USER': 'bakwas',
        'PASSWORD': 'kuchbhii',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'chatbot.log',
        },
    },
    'loggers': {
        'chatbot': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
