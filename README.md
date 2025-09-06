# ChatBot
ChatBot in Django and Vue.js

# Complete Chatbot Setup Instructions

##  Quick Start Guide

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL or SQLite
- Git

### 1. Django Backend Setup

```bash
# Create and activate virtual environment
python -m venv chatbot_env
source chatbot_env/bin/activate  # On Windows: chatbot_env\Scripts\activate

# Install Django and dependencies
pip install django djangorestframework django-cors-headers psycopg2-binary

# Create Django project
django-admin startproject chatbot_project
cd chatbot_project

# Create chatbot app
python manage.py startapp chatbot
```

### 2. Configure Django Settings

Add to `settings.py`:
```python
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

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
CORS_ALLOW_CREDENTIALS = True
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations chatbot
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate sample data
python manage.py populate_faqs
```

### 4. Vue.js Frontend Setup

```bash
# Create Vue project
npm create vue@latest chatbot-frontend
cd chatbot-frontend

# Install dependencies
npm install axios

# Copy the ChatBot.vue component to src/components/
# Update App.vue and main.js as shown in the artifacts
```

### 5. Run the Applications

**Terminal 1 - Django Backend:**
```bash
cd chatbot_project
python manage.py runserver
```

**Terminal 2 - Vue.js Frontend:**
```bash
cd chatbot-frontend
npm run dev
```

##  Features Overview

### Core Features
-> **AI-Powered Responses** - Intelligent intent detection and contextual replies
✅ **Real-time Chat** - Smooth, responsive messaging interface
✅ **Quick Replies** - Predefined buttons for common questions
✅ **Typing Indicators** - Visual feedback during bot responses
✅ **Message History** - Persistent conversation storage
✅ **FAQ Search** - Automatic FAQ matching based on user queries
✅ **User Feedback** - Like/dislike system for continuous improvement
✅ **Session Management** - Secure session handling with unique IDs
✅ **Analytics** - Comprehensive tracking of user interactions
✅ **Responsive Design** - Works perfectly on desktop and mobile
✅ **Accessibility** - WCAG compliant with keyboard navigation
✅ **Dark Mode** - Automatic dark/light mode detection

### Advanced Features
✅ **Multi-step Conversations** - Context-aware dialog management
✅ **Escalation to Human** - Seamless handoff to support agents
✅ **Customizable Themes** - Easy branding and styling
✅ **Offline Support** - Graceful handling of network issues
✅ **Performance Optimized** - Lazy loading and efficient rendering
✅ **Security Hardened** - CSRF protection and input sanitization

##  Customization Guide

### Adding New FAQs

1. **Via Django Admin:**
   - Go to `http://localhost:8000/admin`
   - Navigate to Chatbot → FAQs
   - Click "Add FAQ"

2. **Via Management Command:**
   ```python
   # Add to populate_faqs.py
   FAQ.objects.create(
       category='login',
       question='Your new question?',
       answer='Your detailed answer...',
       keywords=['keyword1', 'keyword2'],
       priority=5
   )
   ```

### Customizing Bot Responses

Edit `chatbot_engine.py`:
```python
# Add new intents
self.intents['custom_intent'] = {
    'patterns': ['custom', 'pattern', 'matching'],
    'keywords': ['custom', 'keywords']
}

# Add corresponding responses
self.responses['custom_intent'] = {
    'message': 'Your custom response',
    'quick_replies': [
        {'title': 'Option 1', 'payload': 'option1'},
        {'title': 'Option 2', 'payload': 'option2'}
    ]
}
```

### Styling the Chatbot

Modify the CSS variables in `ChatBot.vue`:
```css
:root {
  --chatbot-primary: #667eea;
  --chatbot-secondary: #764ba2;
  --chatbot-background: #ffffff;
  --chatbot-text: #333333;
}
```

### Integrating with External APIs

Add to `chatbot_engine.py`:
```python
import requests

def call_external_api(self, query):
    try:
        response = requests.get(
            'https://api.example.com/search',
            params={'q': query},
            timeout=5
        )
        return response.json()
    except requests.RequestException:
        return None
```

## Analytics & Monitoring

### Built-in Analytics
The chatbot tracks:
- **Message volume** - Total messages per day/week/month
- **Intent distribution** - Most common user intents
- **FAQ performance** - Which FAQs are most helpful
- **User satisfaction** - Feedback ratings and comments
- **Session duration** - Average conversation length
- **Escalation rate** - How often users need human help

### Viewing Analytics
```python
# In Django shell (python manage.py shell)
from chatbot.models import ChatAnalytics, Message, UserFeedback

# Get message stats
total_messages = Message.objects.count()
bot_messages = Message.objects.filter(message_type='bot').count()
user_messages = Message.objects.filter(message_type='user').count()

# Get popular intents
from django.db.models import Count
popular_intents = ChatAnalytics.objects.filter(
    event_type='message_sent'
).values('event_data__intent').annotate(
    count=Count('id')
).order_by('-count')[:10]

# Get feedback stats
positive_feedback = UserFeedback.objects.filter(rating__gte=4).count()
total_feedback = UserFeedback.objects.count()
satisfaction_rate = positive_feedback / total_feedback * 100
```

## Advanced Configuration

### WebSocket Integration (Real-time Updates)
```python
# settings.py
INSTALLED_APPS += ['channels']
ASGI_APPLICATION = 'chatbot_project.asgi.application'

# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        # Handle real-time messages
        await self.send(text_data=json.dumps({
            'message': 'Bot response...'
        }))
```

### Redis Caching for Performance
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# In views.py
from django.core.cache import cache

def get_cached_response(self, query):
    cache_key = f"chatbot_response_{hash(query)}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response
    
    response = self.generate_response(query)
    cache.set(cache_key, response, timeout=3600)  # Cache for 1 hour
    return response
```

### Integration with Popular Platforms

#### Slack Integration
```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackChatbot:
    def __init__(self, token):
        self.client = WebClient(token=token)
    
    def send_message(self, channel, text):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text
            )
        except SlackApiError as e:
            print(f"Error: {e}")
```

#### Microsoft Teams Integration
```python
from botbuilder.core import TurnContext, ActivityHandler
from botbuilder.schema import ChannelAccount

class TeamsBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        bot_response = self.process_message(user_message)
        await turn_context.send_activity(bot_response)
```

## Troubleshooting

### Common Issues

**1. CORS Errors**
```python
# Add to settings.py
CORS_ALLOW_ALL_ORIGINS = True  # For development only
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

**2. Database Migration Issues**
```bash
# Reset migrations if needed
python manage.py migrate chatbot zero
python manage.py makemigrations chatbot
python manage.py migrate
```

**3. Vue.js Build Issues**
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**4. Static Files Not Loading**
```python
# In settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Run collectstatic
python manage.py collectstatic
```

### Performance Optimization

**Database Optimization:**
```python
# Add indexes to models.py
class Message(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['session', 'timestamp']),
            models.Index(fields=['message_type', 'timestamp']),
        ]

class FAQ(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['priority', 'helpful_votes']),
        ]
```

**Frontend Optimization:**
```javascript
// Lazy loading for better performance
const ChatBot = defineAsyncComponent(() => import('./components/ChatBot.vue'))

// Message pagination
const MESSAGES_PER_PAGE = 50
const loadMoreMessages = async () => {
  // Implement infinite scrolling
}
```

## Deployment Guide

### Production Settings
```python
# settings_prod.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Database for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### Docker Setup
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: chatbot_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /path/to/static/files/;
    }
}
```

## Scaling & Performance

### Load Testing
```python
# Simple load test script
import asyncio
import aiohttp
import time

async def send_message(session, message):
    async with session.post('http://localhost:8000/chatbot/api/chat/', 
                           json={'action': 'send_message', 'content': message}) as resp:
        return await resp.json()

async def load_test():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):  # 100 concurrent requests
            tasks.append(send_message(session, f"Test message {i}"))
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        print(f"Completed 100 requests in {end_time - start_time:.2f} seconds")

asyncio.run(load_test())
```

### Monitoring Setup
```python
# Add to settings.py for logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'chatbot.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
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
```


### Next Steps
1. **Customize** the responses for your specific use case
2. **Add** more FAQs relevant to your business
3. **Integrate** with your existing systems (CRM, helpdesk, etc.)
4. **Monitor** user interactions and improve responses
5. **Scale** based on usage patterns

**Happy chatting!**
