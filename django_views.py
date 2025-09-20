# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import ValidationError
import json
import uuid
import logging
from datetime import datetime, timedelta
from .models import ChatSession, Message, FAQ, QuickReply, ChatAnalytics, UserFeedback
from .chatbot_engine import ChatbotEngine

# Set up logging
logger = logging.getLogger(__name__)

class ChatbotView(View):
    """Main chatbot API view"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chatbot = ChatbotEngine()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """Handle POST requests for chatbot interactions"""
        try:
            # Parse JSON data
            data = json.loads(request.body)
            action = data.get('action')
            
            # Route to appropriate handler
            if action == 'start_session':
                return self.start_session(request, data)
            elif action == 'send_message':
                return self.send_message(request, data)
            elif action == 'submit_feedback':
                return self.submit_feedback(request, data)
            elif action == 'get_session_history':
                return self.get_session_history(request, data)
            else:
                return JsonResponse({
                    'error': 'Invalid action',
                    'valid_actions': ['start_session', 'send_message', 'submit_feedback', 'get_session_history']
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error(f"Chatbot API error: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

    def start_session(self, request, data):
        """Start a new chat session"""
        try:
            session_id = str(uuid.uuid4())
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            ip_address = self.get_client_ip(request)
            
            # Create new session
            session = ChatSession.objects.create(
                session_id=session_id,
                user_agent=user_agent,
                ip_address=ip_address
            )
            
            # Create welcome message
            welcome_content = (
                "Hello! I'm your virtual assistant. I can help you with:\n\n"
                "🔐 Login and authentication issues\n"
                "🔑 Password recovery and reset\n"
                "👤 Account management\n"
                "💳 Billing and payments\n"
                "🛡️ Security settings\n"
                "🔧 Technical support\n\n"
                "What can I help you with today?"
            )
            
            welcome_message = Message.objects.create(
                session=session,
                message_type='bot',
                content=welcome_content,
                metadata={
                    'quick_replies': self.get_initial_quick_replies(),
                    'type': 'welcome_message'
                }
            )
            
            # Log analytics
            ChatAnalytics.objects.create(
                session=session,
                event_type='session_started',
                event_data={
                    'user_agent': user_agent,
                    'ip_address': ip_address,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            return JsonResponse({
                'success': True,
                'session_id': session_id,
                'message': {
                    'id': str(welcome_message.id),
                    'content': welcome_message.content,
                    'timestamp': welcome_message.timestamp.isoformat(),
                    'type': 'bot',
                    'metadata': welcome_message.metadata
                }
            })
            
        except Exception as e:
            logger.error(f"Error starting session: {str(e)}")
            return JsonResponse({'error': 'Failed to start session'}, status=500)

    def send_message(self, request, data):
        """Process user message and return bot response"""
        try:
            session_id = data.get('session_id')
            content = data.get('content', '').strip()
            
            # Validate input
            if not session_id:
                return JsonResponse({'error': 'Session ID is required'}, status=400)
            if not content:
                return JsonResponse({'error': 'Message content is required'}, status=400)
            if len(content) > 1000:  # Prevent spam
                return JsonResponse({'error': 'Message too long (max 1000 characters)'}, status=400)
                
            # Get session
            session = get_object_or_404(
                ChatSession, 
                session_id=session_id, 
                is_active=True
            )
            
            # Check session age (expire after 24 hours)
            if (datetime.now() - session.created_at.replace(tzinfo=None)).days > 1:
                session.is_active = False
                session.save()
                return JsonResponse({'error': 'Session expired. Please start a new session.'}, status=401)
            
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
            
            # Update session timestamp
            session.updated_at = datetime.now()
            session.save()
            
            # Log analytics
            ChatAnalytics.objects.create(
                session=session,
                event_type='message_sent',
                event_data={
                    'user_message': content,
                    'bot_response': bot_response['content'],
                    'intent': bot_response.get('intent'),
                    'confidence': bot_response.get('confidence'),
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            return JsonResponse({
                'success': True,
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
            
        except ChatSession.DoesNotExist:
            return JsonResponse({'error': 'Invalid session ID'}, status=404)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return JsonResponse({'error': 'Failed to process message'}, status=500)

    def submit_feedback(self, request, data):
        """Submit user feedback for a message"""
        try:
            session_id = data.get('session_id')
            message_id = data.get('message_id')
            rating = data.get('rating')
            comment = data.get('comment', '')
            
            # Validate input
            if not session_id:
                return JsonResponse({'error': 'Session ID is required'}, status=400)
            if rating not in [1, 2, 3, 4, 5]:
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
            
            # Get session
            session = get_object_or_404(ChatSession, session_id=session_id)
            message = None
            
            # Get message if provided
            if message_id:
                message = get_object_or_404(
                    Message, 
                    id=message_id, 
                    session=session
                )
                
                # Update FAQ helpful votes if this was an FAQ response
                if message.metadata.get('type') == 'faq_response':
                    faq_id = message.metadata.get('faq_id')
                    if faq_id:
                        try:
                            faq = FAQ.objects.get(id=faq_id)
                            if rating >= 4:
                                faq.helpful_votes += 1
                            else:
                                faq.not_helpful_votes += 1
                            faq.save()
                        except FAQ.DoesNotExist:
                            pass
            
            # Create feedback record
            feedback = UserFeedback.objects.create(
                session=session,
                message=message,
                rating=rating,
                comment=comment[:500]  # Limit comment length
            )
            
            # Log analytics
            ChatAnalytics.objects.create(
                session=session,
                event_type='feedback_submitted',
                event_data={
                    'rating': rating,
                    'comment': comment,
                    'message_id': str(message_id) if message_id else None,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            return JsonResponse({
                'success': True,
                'feedback_id': str(feedback.id),
                'message': 'Thank you for your feedback!'
            })
            
        except Exception as e:
            logger.error(f"Error submitting feedback: {str(e)}")
            return JsonResponse({'error': 'Failed to submit feedback'}, status=500)

    def get_session_history(self, request, data):
        """Get message history for a session"""
        try:
            session_id = data.get('session_id')
            limit = data.get('limit', 50)  # Default to 50 messages
            
            if not session_id:
                return JsonResponse({'error': 'Session ID is required'}, status=400)
            
            # Get session
            session = get_object_or_404(ChatSession, session_id=session_id)
            
            # Get messages
            messages = Message.objects.filter(session=session).order_by('timestamp')[:limit]
            
            # Format messages
            message_list = []
            for msg in messages:
                message_list.append({
                    'id': str(msg.id),
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'type': msg.message_type,
                    'metadata': msg.metadata
                })
            
            return JsonResponse({
                'success': True,
                'messages': message_list,
                'session_info': {
                    'id': session_id,
                    'created_at': session.created_at.isoformat(),
                    'updated_at': session.updated_at.isoformat()
                }
            })
            
        except Exception as e:
            logger.error(f"Error getting session history: {str(e)}")
            return JsonResponse({'error': 'Failed to get session history'}, status=500)

    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_initial_quick_replies(self):
        """Get initial quick reply options"""
        return [
            {'title': '🔐 Login Issues', 'payload': 'login_help'},
            {'title': '🔑 Password Reset', 'payload': 'password_reset'},
            {'title': '👤 Account Details', 'payload': 'account_details'},
            {'title': '📝 Sign Up Help', 'payload': 'signup_help'},
            {'title': '💳 Billing Help', 'payload': 'billing'},
            {'title': '❓ Other Questions', 'payload': 'other_questions'}
        ]


@csrf_exempt
@require_http_methods(["GET"])
def get_faqs(request):
    """Get FAQs with optional filtering"""
    try:
        category = request.GET.get('category', 'all')
        search = request.GET.get('search', '')
        limit = int(request.GET.get('limit', 20))
        
        # Start with active FAQs
        faqs = FAQ.objects.filter(is_active=True)
        
        # Filter by category
        if category != 'all' and category:
            faqs = faqs.filter(category=category)
        
        # Search in questions and answers
        if search:
            faqs = faqs.filter(
                models.Q(question__icontains=search) |
                models.Q(answer__icontains=search) |
                models.Q(keywords__icontains=search)
            )
        
        # Order by priority and helpfulness
        faqs = faqs.order_by('-priority', '-helpful_votes')[:limit]
        
        # Format response
        faqs_data = []
        for faq in faqs:
            faqs_data.append({
                'id': str(faq.id),
                'category': faq.category,
                'question': faq.question,
                'answer': faq.answer,
                'helpful_votes': faq.helpful_votes,
                'not_helpful_votes': faq.not_helpful_votes,
                'helpfulness_score': faq.helpfulness_score,
                'view_count': faq.view_count
            })
        
        return JsonResponse({
            'success': True,
            'faqs': faqs_data,
            'total_count': len(faqs_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting FAQs: {str(e)}")
        return JsonResponse({'error': 'Failed to get FAQs'}, status=500)


@csrf_exempt 
@require_http_methods(["GET"])
def get_quick_replies(request):
    """Get quick reply options by category"""
    try:
        category = request.GET.get('category', 'general')
        
        # Get quick replies for category
        replies = QuickReply.objects.filter(
            category=category, 
            is_active=True
        ).order_by('order')
        
        # Format response
        replies_data = []
        for reply in replies:
            replies_data.append({
                'title': reply.title,
                'payload': reply.payload,
                'icon': reply.icon
            })
        
        return JsonResponse({
            'success': True,
            'quick_replies': replies_data
        })
        
    except Exception as e:
        logger.error(f"Error getting quick replies: {str(e)}")
        return JsonResponse({'error': 'Failed to get quick replies'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_analytics(request):
    """Get basic analytics (admin only)"""
    try:
        # This would typically require admin authentication
        # For demo purposes, we'll return basic stats
        
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        
        # Basic stats
        total_sessions = ChatSession.objects.count()
        active_sessions = ChatSession.objects.filter(
            created_at__gte=week_ago
        ).count()
        total_messages = Message.objects.count()
        avg_rating = UserFeedback.objects.aggregate(
            avg_rating=models.Avg('rating')
        )['avg_rating'] or 0
        
        return JsonResponse({
            'success': True,
            'analytics': {
                'total_sessions': total_sessions,
                'active_sessions_this_week': active_sessions,
                'total_messages': total_messages,
                'average_rating': round(avg_rating, 2),
                'generated_at': now.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        return JsonResponse({'error': 'Failed to get analytics'}, status=500)
