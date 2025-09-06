# chatbot_engine.py
import re
import json
import random
from datetime import datetime
from .models import FAQ, QuickReply, ChatAnalytics

class ChatbotEngine:
    def __init__(self):
        self.intents = {
            'login_help': {
                'patterns': ['login', 'log in', 'sign in', 'signin', 'cant login', 'unable to login', 'login problem'],
                'keywords': ['login', 'signin', 'access', 'account', 'credentials']
            },
            'password_reset': {
                'patterns': ['password', 'forgot password', 'reset password', 'change password', 'lost password'],
                'keywords': ['password', 'reset', 'forgot', 'change', 'recover']
            },
            'account_details': {
                'patterns': ['account', 'profile', 'update account', 'change email', 'personal information'],
                'keywords': ['account', 'profile', 'email', 'phone', 'information', 'details']
            },
            'signup_help': {
                'patterns': ['signup', 'sign up', 'register', 'create account', 'new account'],
                'keywords': ['signup', 'register', 'create', 'new', 'account']
            },
            'security': {
                'patterns': ['security', '2fa', 'two factor', 'secure', 'safety', 'protection'],
                'keywords': ['security', 'safe', '2fa', 'authentication', 'protection']
            },
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
                'keywords': ['hello', 'hi', 'hey', 'morning', 'afternoon', 'evening']
            },
            'goodbye': {
                'patterns': ['bye', 'goodbye', 'see you', 'thanks', 'thank you', 'thats all'],
                'keywords': ['bye', 'goodbye', 'thanks', 'thank']
            },
            'escalate': {
                'patterns': ['human', 'agent', 'representative', 'speak to someone', 'talk to human'],
                'keywords': ['human', 'agent', 'representative', 'person', 'help']
            }
        }
        
        self.responses = {
            'login_help': {
                'message': "I can help you with login issues! Here are the most common solutions:",
                'quick_replies': [
                    {'title': 'Forgot Username', 'payload': 'forgot_username'},
                    {'title': 'Account Locked', 'payload': 'account_locked'},
                    {'title': 'Invalid Credentials', 'payload': 'invalid_credentials'},
                    {'title': 'Two-Factor Issues', 'payload': '2fa_issues'}
                ]
            },
            'password_reset': {
                'message': "I'll guide you through the password reset process:\n\n1. Go to the login page\n2. Click 'Forgot Password?'\n3. Enter your email address\n4. Check your email for reset instructions\n5. Follow the link and create a new password\n\nIf you don't receive the email, check your spam folder or try again in a few minutes.",
                'quick_replies': [
                    {'title': 'No Reset Email', 'payload': 'no_reset_email'},
                    {'title': 'Reset Link Expired', 'payload': 'reset_link_expired'},
                    {'title': 'Password Requirements', 'payload': 'password_requirements'}
                ]
            },
            'account_details': {
                'message': "You can update your account information in several ways:",
                'quick_replies': [
                    {'title': 'Change Email', 'payload': 'change_email'},
                    {'title': 'Update Phone', 'payload': 'update_phone'},
                    {'title': 'Personal Info', 'payload': 'personal_info'},
                    {'title': 'Delete Account', 'payload': 'delete_account'}
                ]
            },
            'signup_help': {
                'message': "Creating a new account is easy! Here's what you need:",
                'quick_replies': [
                    {'title': 'Email Verification', 'payload': 'email_verification'},
                    {'title': 'Account Activation', 'payload': 'account_activation'},
                    {'title': 'Registration Issues', 'payload': 'registration_issues'}
                ]
            },
            'security': {
                'message': "Security is important! Here are our security features:",
                'quick_replies': [
                    {'title': 'Enable 2FA', 'payload': 'enable_2fa'},
                    {'title': 'Security Tips', 'payload': 'security_tips'},
                    {'title': 'Suspicious Activity', 'payload': 'suspicious_activity'}
                ]
            },
            'greeting': {
                'message': "Hello! I'm here to help you with any questions about login, passwords, account details, and more. What can I assist you with today?",
                'quick_replies': [
                    {'title': '🔐 Login Issues', 'payload': 'login_help'},
                    {'title': '🔑 Password Reset', 'payload': 'password_reset'},
                    {'title': '👤 Account Details', 'payload': 'account_details'},
                    {'title': '📝 Sign Up Help', 'payload': 'signup_help'}
                ]
            },
            'goodbye': {
                'message': "Thank you for using our support chat! If you need more help, just start a new conversation. Have a great day! 😊",
                'quick_replies': []
            },
            'escalate': {
                'message': "I understand you'd like to speak with a human agent. I'm transferring you now...\n\n⏱️ **Estimated wait time: 3-5 minutes**\n\nWhile you wait, I can still help with common questions. Is there anything specific I can assist with?",
                'quick_replies': [
                    {'title': 'Continue with Bot', 'payload': 'continue_bot'},
                    {'title': 'Cancel Transfer', 'payload': 'cancel_transfer'}
                ]
            }
        }

        self.specific_responses = {
            'forgot_username': "To recover your username:\n\n1. Visit the login page\n2. Click 'Forgot Username?'\n3. Enter your email address\n4. Check your email for your username\n\nIf you don't receive it, contact support at support@company.com",
            
            'account_locked': "If your account is locked:\n\n1. Wait 15 minutes and try again\n2. Ensure you're using the correct credentials\n3. Clear your browser cache\n4. Try from a different device\n\nIf it's still locked, I can help unlock it for you.",
            
            'invalid_credentials': "For invalid credential errors:\n\n✅ Check your username/email spelling\n✅ Ensure Caps Lock is off\n✅ Try copying and pasting your password\n✅ Clear browser cache and cookies\n\nStill having trouble? Let me know!",
            
            '2fa_issues': "Two-Factor Authentication troubleshooting:\n\n📱 **App Issues:**\n• Sync your device time\n• Try backup codes\n• Reinstall authenticator app\n\n📞 **SMS Issues:**\n• Check signal strength\n• Try calling instead of SMS\n• Update phone number",
            
            'no_reset_email': "If you're not receiving the reset email:\n\n1. Check your spam/junk folder\n2. Wait 5-10 minutes (emails can be delayed)\n3. Ensure you entered the correct email\n4. Try a different email if you have multiple accounts\n5. Add noreply@company.com to your contacts",
            
            'enable_2fa': "To enable Two-Factor Authentication:\n\n1. Go to Account Settings > Security\n2. Click 'Enable 2FA'\n3. Download an authenticator app (Google Authenticator, Authy)\n4. Scan the QR code\n5. Enter the verification code\n6. Save your backup codes securely\n\n🔒 This adds an extra layer of security to your account!"
        }

    def process_message(self, message, session):
        message_lower = message.lower().strip()
        
        # Check for specific payload responses first
        if message_lower in self.specific_responses:
            return {
                'content': self.specific_responses[message_lower],
                'intent': message_lower,
                'confidence': 1.0,
                'metadata': {'type': 'specific_response'}
            }
        
        # Detect intent
        intent = self.detect_intent(message_lower)
        confidence = self.calculate_confidence(message_lower, intent)
        
        # Get response based on intent
        if intent in self.responses:
            response_data = self.responses[intent]
            return {
                'content': response_data['message'],
                'intent': intent,
                'confidence': confidence,
                'metadata': {
                    'quick_replies': response_data.get('quick_replies', []),
                    'type': 'intent_response'
                }
            }
        
        # Search FAQs if no intent matched
        faq_result = self.search_faqs(message_lower)
        if faq_result:
            return {
                'content': f"**{faq_result['question']}**\n\n{faq_result['answer']}",
                'intent': 'faq_match',
                'confidence': 0.8,
                'metadata': {
                    'faq_id': faq_result['id'],
                    'type': 'faq_response',
                    'quick_replies': [
                        {'title': '👍 Helpful', 'payload': f"helpful_{faq_result['id']}"},
                        {'title': '👎 Not Helpful', 'payload': f"not_helpful_{faq_result['id']}"},
                        {'title': 'More Help', 'payload': 'escalate'}
                    ]
                }
            }
        
        # Default response
        return self.get_default_response(message_lower)

    def detect_intent(self, message):
        best_intent = None
        best_score = 0
        
        for intent, data in self.intents.items():
            score = 0
            
            # Check patterns
            for pattern in data['patterns']:
                if pattern in message:
                    score += 2
            
            # Check keywords
            for keyword in data['keywords']:
                if keyword in message:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_intent = intent
        
        return best_intent if best_score > 0 else None

    def calculate_confidence(self, message, intent):
        if not intent:
            return 0.0
        
        word_count = len(message.split())
        matches = sum(1 for pattern in self.intents[intent]['patterns'] if pattern in message)
        keyword_matches = sum(1 for keyword in self.intents[intent]['keywords'] if keyword in message)
        
        confidence = (matches * 0.4 + keyword_matches * 0.2) / max(word_count * 0.1, 1)
        return min(confidence, 1.0)

    def search_faqs(self, message):
        # Simple keyword matching for FAQs
        faqs = FAQ.objects.filter(is_active=True)
        
        best_faq = None
        best_score = 0
        
        for faq in faqs:
            score = 0
            
            # Check question similarity
            if any(word in faq.question.lower() for word in message.split()):
                score += 2
            
            # Check keywords
            for keyword in faq.keywords:
                if keyword.lower() in message:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_faq = faq
        
        if best_faq and best_score >= 2:
            # Increment view count
            best_faq.view_count += 1
            best_faq.save()
            
            return {
                'id': str(best_faq.id),
                'question': best_faq.question,
                'answer': best_faq.answer,
                'category': best_faq.category
            }
        
        return None

    def get_default_response(self, message):
        default_responses = [
            "I'm not sure I understand that question. Could you please rephrase it or choose from the options below?",
            "I'd like to help, but I need a bit more information. What specific issue are you facing?",
            "That's an interesting question! Let me suggest some common topics I can help with:",
        ]
        
        return {
            'content': random.choice(default_responses),
            'intent': 'unknown',
            'confidence': 0.0,
            'metadata': {
                'type': 'default_response',
                'quick_replies': [
                    {'title': '🔐 Login Help', 'payload': 'login_help'},
                    {'title': '🔑 Password Issues', 'payload': 'password_reset'},
                    {'title': '👤 Account Questions', 'payload': 'account_details'},
                    {'title': '🙋 Speak to Human', 'payload': 'escalate'}
                ]
            }
        }