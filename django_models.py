# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)  # For storing quick replies, attachments, etc.

    class Meta:
        ordering = ['timestamp']

class FAQ(models.Model):
    CATEGORIES = [
        ('login', 'Login & Authentication'),
        ('password', 'Password Management'),
        ('account', 'Account Details'),
        ('signup', 'Sign Up Process'),
        ('security', 'Security'),
        ('general', 'General')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    question = models.CharField(max_length=500)
    answer = models.TextField()
    keywords = models.JSONField(default=list)  # List of keywords for matching
    priority = models.IntegerField(default=0)  # Higher priority shows first
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    helpful_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-helpful_votes', 'question']

class QuickReply(models.Model):
    title = models.CharField(max_length=100)
    payload = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=FAQ.CATEGORIES)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

class ChatAnalytics(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)  # 'message_sent', 'faq_viewed', 'escalated', etc.
    event_data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserFeedback(models.Model):
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent')
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
