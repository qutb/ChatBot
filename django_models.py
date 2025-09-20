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

    def __str__(self):
        return f"Session {self.session_id[:8]}"

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
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['session', 'timestamp']),
            models.Index(fields=['message_type', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.message_type} - {self.content[:50]}"

class FAQ(models.Model):
    CATEGORIES = [
        ('login', 'Login & Authentication'),
        ('password', 'Password Management'),
        ('account', 'Account Details'),
        ('signup', 'Sign Up Process'),
        ('security', 'Security'),
        ('billing', 'Billing & Payments'),
        ('technical', 'Technical Support'),
        ('general', 'General')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='general')
    question = models.CharField(max_length=500)
    answer = models.TextField()
    keywords = models.JSONField(default=list)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    helpful_votes = models.IntegerField(default=0)
    not_helpful_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-helpful_votes', 'question']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['priority', 'helpful_votes']),
        ]

    def __str__(self):
        return self.question[:100]

    @property
    def helpfulness_score(self):
        total_votes = self.helpful_votes + self.not_helpful_votes
        if total_votes == 0:
            return 0
        return (self.helpful_votes / total_votes) * 100

class QuickReply(models.Model):
    title = models.CharField(max_length=100)
    payload = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=FAQ.CATEGORIES, default='general')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon class")

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = 'Quick Replies'

    def __str__(self):
        return self.title

class ChatAnalytics(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    event_data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Chat Analytics'
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['session', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

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

    class Meta:
        verbose_name_plural = 'User Feedback'

    def __str__(self):
        return f"Rating: {self.rating}/5 - {self.timestamp.strftime('%Y-%m-%d')}"
