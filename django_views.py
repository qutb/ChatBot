# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator
import json
import uuid
import re
from datetime import datetime, timedelta
from .models import ChatSession, Message, FAQ, QuickReply, ChatAnalytics, UserFeedback
from .chatbot_engine import ChatbotEngine

class ChatbotView(View):
    def __init__(self):
        super().__init__()
        self.chatbot = ChatbotEngine()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'start_session':
                return self.start_session(request, data)
            elif action == 'send_message':
                return self.send_message(request, data)
            elif action == 'get_messages':
                return self.get_messages(request, data)
            elif action == 'typing_indicator':
                return self.typing_indicator(request, data)
            elif action == 'submit_feedback':
                return self.submit_feedback(request, data)
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def start_session(self, request, data):
        session_id = str(uuid.uuid4())
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = self.get_client_ip(request)
        
        session = ChatSession.objects.create(
            session_id=session_id,
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        # Create welcome message
        welcome_message = Message.objects.create(
            session=session,
            message_type='bot',
            content="Hi! I'm your virtual assistant. I can help you with login issues, password recovery, account details, and more. How can I assist you today?",
            metadata={
                'quick_replies': self.get_initial_quick_replies()
            }
        )
        
        # Log analytics
        ChatAnalytics.objects.create(
            session=session,
            event_type='session_started',
            event_data={'user_agent': user_agent, 'ip_address': ip_address}
        )
        
        return JsonResponse({
            'session_id': session_id,
            'message': {
                'id': str(welcome_message.id),
                'content': welcome_message.content,
                'timestamp': welcome_message.timestamp.isoformat(),
                'type': 'bot',
                'metadata': welcome_message.metadata
            }
        })

    def send_message(self, request, data):
        session_id = data.get('session_id')
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Message content is required'}, status=400)
            
        session = get_object_or_404(ChatSession, session_id=session_id, is_active=True)
        
        # Create user message
        user_message = Message.objects.create(
            session=session,
            message_type='user',
            content=content
        )
        
        # Process message with chatbot engine
        bot_response = self.chatbot.process_message(content, session)
        
        # Create bot response message
        bot_message = Message.objects.create(
            session=session,
            message_type='bot',
            content=bot_response['content'],
            metadata=bot_response.get('metadata', {})
        )
        
        # Log analytics
        ChatAnalytics.objects.create(
            session=session,
            event_type='message_sent',
            event_data={
                'user_message': content,
                'bot_response': bot_response['content'],
                'intent': bot_response.get('intent'),
                'confidence': bot_response.get('confidence')
            }
        )
        
        return JsonResponse({
            'user_message': {
                'id': str(user_message.id),
                'content': user_message.content,
                'timestamp': user_message.timestamp.isoformat(),
                'type': 'user'
            },
            'bot_message': {
                'id': str(bot_message.id),
                'content': bot_message.content,
                'timestamp': bot_message.timestamp.isoformat(),
                'type': 'bot',
                'metadata': bot_message.metadata
            }
        })

    def get_messages(self, request, data):
        session_id = data.get('session_id')
        page = data.get('page', 1)
        
        session = get_object_or_404(ChatSession, session_id=session_id)
        messages = Message.objects.filter(session=session)
        
        paginator = Paginator(messages, 50)
        page_obj = paginator.get_page(page)
        
        messages_data = []
        for message in page_obj:
            messages_data.append({
                'id': str(message.id),
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'type': message.message_type,
                'metadata': message.metadata
            })
        
        return JsonResponse({
            'messages': messages_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'total_pages': paginator.num_pages
        })

    def typing_indicator(self, request, data):
        # In a real implementation, you'd use WebSockets for real-time updates
        return JsonResponse({'status': 'received'})

    def submit_feedback(self, request, data):
        session_id = data.get('session_id')
        message_id = data.get('message_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        session = get_object_or_404(ChatSession, session_id=session_id)
        message = None
        
        if message_id:
            message = get_object_or_404(Message, id=message_id, session=session)
        
        feedback = UserFeedback.objects.create(
            session=session,
            message=message,
            rating=rating,
            comment=comment
        )
        
        ChatAnalytics.objects.create(
            session=session,
            event_type='feedback_submitted',
            event_data={'rating': rating, 'comment': comment}
        )
        
        return JsonResponse({'status': 'success', 'feedback_id': str(feedback.id)})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_initial_quick_replies(self):
        return [
            {'title': '🔐 Login Issues', 'payload': 'login_help'},
            {'title': '🔑 Password Reset', 'payload': 'password_reset'},
            {'title': '👤 Account Details', 'payload': 'account_details'},
            {'title': '📝 Sign Up Help', 'payload': 'signup_help'},
            {'title': '❓ Other Questions', 'payload': 'other_questions'}
        ]

@csrf_exempt
@require_http_methods(["GET"])
def get_faqs(request):
    category = request.GET.get('category', 'all')
    search = request.GET.get('search', '')
    
    faqs = FAQ.objects.filter(is_active=True)
    
    if category != 'all':
        faqs = faqs.filter(category=category)
    
    if search:
        faqs = faqs.filter(question__icontains=search)
    
    faqs_data = []
    for faq in faqs[:20]:  # Limit to 20 results
        faqs_data.append({
            'id': str(faq.id),
            'category': faq.category,
            'question': faq.question,
            'answer': faq.answer,
            'helpful_votes': faq.helpful_votes
        })
    
    return JsonResponse({'faqs': faqs_data})

@csrf_exempt 
@require_http_methods(["GET"])
def get_quick_replies(request):
    category = request.GET.get('category', 'general')
    
    replies = QuickReply.objects.filter(
        category=category, 
        is_active=True
    )
    
    replies_data = []
    for reply in replies:
        replies_data.append({
            'title': reply.title,
            'payload': reply.payload
        })
    
    return JsonResponse({'quick_replies': replies_data})