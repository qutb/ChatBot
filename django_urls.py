# urls.py
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('api/chat/', views.ChatbotView.as_view(), name='chatbot_api'),
    path('api/faqs/', views.get_faqs, name='get_faqs'),
    path('api/quick-replies/', views.get_quick_replies, name='get_quick_replies'),
]

# In your main project urls.py, include:
# path('chatbot/', include('chatbot.urls')),