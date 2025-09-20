# Complete Chatbot Deployment Guide

## Overview
This guide provides step-by-step instructions to deploy a fully functional, bug-free chatbot built with Django backend and Vue.js frontend.

## Prerequisites
- Python 3.8+
- Node.js 16+
- Git
- A code editor (VS Code recommended)

## 🚀 Quick Setup (5 Minutes)

### 1. Backend Setup (Django)

```bash
# Create project directory
mkdir chatbot-project
cd chatbot-project

# Create virtual environment
python -m venv chatbot_env

# Activate virtual environment
# Windows:
chatbot_env\Scripts\activate
# macOS/Linux:
source chatbot_env/bin/activate

# Install Django and dependencies
pip install django djangorestframework django-cors-headers

# Create Django project
django-admin startproject chatbot_backend
cd chatbot_backend

# Create chatbot app
python manage.py startapp chatbot
```

### 2. Configure Django Settings

Create `chatbot_backend/settings.py`:
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'chatbot',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatbot_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'chatbot_backend.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'chatbot.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'chatbot': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### 3. Create Django URLs

Create `chatbot_backend/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chatbot/', include('chatbot.urls')),
]
```

Create `chatbot/urls.py`:
```python
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('api/chat/', views.ChatbotView.as_view(), name='chatbot_api'),
    path('api/faqs/', views.get_faqs, name='get_faqs'),
    path('api/quick-replies/', views.get_quick_replies, name='get_quick_replies'),
    path('api/analytics/', views.get_analytics, name='get_analytics'),
]
```

### 4. Database Setup

```bash
# Create migrations
python manage.py makemigrations chatbot

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Populate sample data
python manage.py populate_faqs
```

### 5. Frontend Setup (Vue.js)

```bash
# In a new terminal, go to project root
cd .. # back to chatbot-project directory

# Create Vue.js app
npm create vue@latest chatbot-frontend
cd chatbot-frontend

# Install dependencies
npm install
npm install axios

# Start development server
npm run dev
```

### 6. Integration

Replace the content of `chatbot-frontend/src/App.vue`:
```vue
<template>
  <div id="app">
    <div class="main-content">
      <h1>Welcome to Our Support Portal</h1>
      <p>Need help? Our AI assistant is here to support you 24/7!</p>
    </div>
    <ChatBot />
  </div>
</template>

<script>
import ChatBot from './components/ChatBot.vue'

export default {
  name: 'App',
  components: {
    ChatBot
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-content {
  padding: 4rem 2rem;
