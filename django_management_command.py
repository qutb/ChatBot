# management/commands/populate_faqs.py
from django.core.management.base import BaseCommand
from chatbot.models import FAQ, QuickReply

class Command(BaseCommand):
    help = 'Populate the database with sample FAQs and quick replies'

    def handle(self, *args, **options):
        # Clear existing data
        FAQ.objects.all().delete()
        QuickReply.objects.all().delete()

        # Login & Authentication FAQs
        login_faqs = [
            {
                'question': 'I can\'t remember my username. How can I recover it?',
                'answer': 'To recover your username:\n\n1. Go to the login page\n2. Click "Forgot Username?"\n3. Enter the email address associated with your account\n4. Check your email for a message containing your username\n5. If you don\'t receive it within 10 minutes, check your spam folder\n\nIf you still can\'t find it, please contact our support team.',
                'keywords': ['username', 'forgot', 'recover', 'email', 'login'],
                'priority': 10
            },
            {
                'question': 'My account is locked. How do I unlock it?',
                'answer': 'Your account gets locked after 5 failed login attempts for security reasons.\n\n**To unlock your account:**\n1. Wait 30 minutes for automatic unlock, OR\n2. Reset your password using "Forgot Password?" link, OR\n3. Contact support for immediate assistance\n\n**Prevention tips:**\n• Double-check your credentials before entering\n• Use copy-paste for complex passwords\n• Enable password manager',
                'keywords': ['locked', 'unlock', 'account', 'security', 'failed', 'attempts'],
                'priority': 9
            },
            {
                'question': 'I\'m getting "Invalid credentials" error. What should I do?',
                'answer': '**Try these steps in order:**\n\n1. **Check your typing:**\n   • Verify username/email spelling\n   • Check if Caps Lock is on\n   • Try typing password manually\n\n2. **Clear browser data:**\n   • Clear cookies and cache\n   • Try incognito/private mode\n   • Try a different browser\n\n3. **Reset password:**\n   • Use "Forgot Password?" if still failing\n\n4. **Check account status:**\n   • Ensure account isn\'t suspended\n   • Verify email address is confirmed',
                'keywords': ['invalid', 'credentials', 'error', 'username', 'password', 'login'],
                'priority': 8
            }
        ]

        # Password Management FAQs
        password_faqs = [
            {
                'question': 'How do I reset my password?',
                'answer': '**Password Reset Process:**\n\n1. Go to the login page\n2. Click "Forgot Password?"\n3. Enter your email address\n4. Check your email (including spam folder)\n5. Click the reset link in the email\n6. Create a new password following our requirements\n7. Log in with your new password\n\n**Note:** Reset links expire after 24 hours for security.',
                'keywords': ['reset', 'password', 'forgot', 'change', 'new'],
                'priority': 10
            },
            {
                'question': 'What are the password requirements?',
                'answer': '**Your password must include:**\n\n✅ At least 8 characters long\n✅ At least one uppercase letter (A-Z)\n✅ At least one lowercase letter (a-z)\n✅ At least one number (0-9)\n✅ At least one special character (!@#$%^&*)\n\n**Security tips:**\n• Use a unique password you haven\'t used elsewhere\n• Consider using a passphrase (e.g., "Coffee!Morning123")\n• Enable two-factor authentication for extra security',
                'keywords': ['password', 'requirements', 'strong', 'security', 'characters'],
                'priority': 7
            },
            {
                'question': 'I didn\'t receive the password reset email. What now?',
                'answer': '**If you didn\'t receive the reset email:**\n\n1. **Check spam/junk folder** - emails sometimes end up there\n\n2. **Wait a few minutes** - delivery can take up to 10 minutes\n\n3. **Verify email address** - ensure you entered the correct email\n\n4. **Try again** - request another reset email\n\n5. **Check email settings** - some providers block automated emails\n\n6. **Contact support** - if still no email after trying above steps\n\n**Add to whitelist:** noreply@yourcompany.com',
                'keywords': ['reset', 'email', 'not', 'received', 'spam', 'delivery'],
                'priority': 8
            }
        ]

        # Account Details FAQs
        account_faqs = [
            {
                'question': 'How do I update my email address?',
                'answer': '**To change your email address:**\n\n1. Log into your account\n2. Go to "Account Settings" or "Profile"\n3. Click "Edit" next to your email address\n4. Enter your new email address\n5. Click "Save Changes"\n6. Check your NEW email for a verification link\n7. Click the verification link to confirm\n\n**Important:** You\'ll need access to both old and new email addresses for security verification.',
                'keywords': ['email', 'change', 'update', 'address', 'profile'],
                'priority': 6
            },
            {
                'question': 'How do I delete or deactivate my account?',
                'answer': '**Account Deletion Options:**\n\n**Temporary Deactivation:**\n• Go to Account Settings > Privacy\n• Select "Deactivate Account"\n• Choose duration (1 week to 6 months)\n• Can be reactivated anytime\n\n**Permanent Deletion:**\n• Contact support team\n• Verify identity for security\n• 30-day grace period before permanent deletion\n• All data will be permanently removed\n\n**Note:** Some information may be retained for legal/security purposes as outlined in our Privacy Policy.',
                'keywords': ['delete', 'deactivate', 'account', 'remove', 'close'],
                'priority': 4
            },
            {
                'question': 'How do I update my phone number?',
                'answer': '**To update your phone number:**\n\n1. Go to Account Settings > Contact Information\n2. Click "Edit" next to phone number\n3. Enter your new phone number\n4. Select your country code\n5. Click "Update"\n6. Verify via SMS code sent to new number\n7. Enter the verification code\n\n**Uses for phone number:**\n• Two-factor authentication\n• Account recovery\n• Important security notifications\n• Optional marketing (you can opt-out)',
                'keywords': ['phone', 'number', 'update', 'change', 'mobile', 'sms'],
                'priority': 5
            }
        ]

        # Sign Up Process FAQs
        signup_faqs = [
            {
                'question': 'I didn\'t receive my email verification. How do I get it?',
                'answer': '**If you didn\'t receive verification email:**\n\n1. **Check spam/junk folder** first\n2. **Wait 10 minutes** - emails can be delayed\n3. **Request new verification:**\n   • Go to login page\n   • Click "Resend verification"\n   • Enter your email address\n4. **Check email filters** - some block automated emails\n5. **Try different email** if available\n\n**Still having trouble?** Contact support with your email address.',
                'keywords': ['verification', 'email', 'signup', 'register', 'confirm'],
                'priority': 7
            },
            {
                'question': 'Why can\'t I create an account with my email?',
                'answer': '**Common registration issues:**\n\n**Email already exists:**\n• Try logging in instead\n• Use "Forgot Password?" if needed\n• Check if you have multiple accounts\n\n**Invalid email format:**\n• Ensure proper format: name@domain.com\n• Check for typos or extra spaces\n• Some special characters aren\'t allowed\n\n**Blocked domains:**\n• Temporary email services are blocked\n• Use permanent email address\n\n**Technical issues:**\n• Try different browser or device\n• Disable ad blockers temporarily',
                'keywords': ['create', 'account', 'email', 'register', 'signup', 'error'],
                'priority': 6
            }
        ]

        # Security FAQs
        security_faqs = [
            {
                'question': 'How do I enable two-factor authentication (2FA)?',
                'answer': '**Setting up Two-Factor Authentication:**\n\n1. **Go to Security Settings:**\n   • Account Settings > Security > Two-Factor Auth\n\n2. **Choose your method:**\n   • Authenticator app (recommended)\n   • SMS text messages\n   • Email codes\n\n3. **For Authenticator apps:**\n   • Download Google Authenticator or Authy\n   • Scan QR code with your phone\n   • Enter 6-digit code to verify\n\n4. **Save backup codes** somewhere safe\n\n**Benefits:** Protects against 99.9% of account takeover attempts!',
                'keywords': ['2fa', 'two', 'factor', 'authentication', 'security', 'enable'],
                'priority': 8
            },
            {
                'question': 'I lost my 2FA device. How can I access my account?',
                'answer': '**If you lost your 2FA device:**\n\n**Option 1: Use backup codes**\n• Use one of the backup codes you saved\n• Go to Settings > Security to generate new codes\n\n**Option 2: Use alternative method**\n• If you set up multiple 2FA methods, try others\n• SMS, email, or different authenticator app\n\n**Option 3: Account recovery**\n• Contact support team\n• Provide identity verification\n• May take 24-48 hours for security\n\n**Prevention:** Always save backup codes and set up multiple 2FA methods!',
                'keywords': ['2fa', 'lost', 'device', 'backup', 'codes', 'recovery'],
                'priority': 9
            }
        ]

        # Create FAQ entries
        all_faqs = [
            ('login', login_faqs),
            ('password', password_faqs),
            ('account', account_faqs),
            ('signup', signup_faqs),
            ('security', security_faqs)
        ]

        faq_count = 0
        for category, faqs in all_faqs:
            for faq_data in faqs:
                FAQ.objects.create(
                    category=category,
                    question=faq_data['question'],
                    answer=faq_data['answer'],
                    keywords=faq_data['keywords'],
                    priority=faq_data['priority']
                )
                faq_count += 1

        # Create Quick Replies
        quick_replies = [
            # Login category
            ('login', 'Forgot Username', 'forgot_username', 1),
            ('login', 'Account Locked', 'account_locked', 2),
            ('login', 'Invalid Credentials', 'invalid_credentials', 3),
            ('login', '2FA Issues', '2fa_issues', 4),
            
            # Password category
            ('password', 'Reset Password', 'password_reset', 1),
            ('password', 'Password Requirements', 'password_requirements', 2),
            ('password', 'No Reset Email', 'no_reset_email', 3),
            ('password', 'Reset Link Expired', 'reset_link_expired', 4),
            
            # Account category
            ('account', 'Change Email', 'change_email', 1),
            ('account', 'Update Phone', 'update_phone', 2),
            ('account', 'Personal Info', 'personal_info', 3),
            ('account', 'Delete Account', 'delete_account', 4),
            
            # Security category
            ('security', 'Enable 2FA', 'enable_2fa', 1),
            ('security', 'Security Tips', 'security_tips', 2),
            ('security', 'Lost 2FA Device', 'lost_2fa_device', 3),
            ('security', 'Suspicious Activity', 'suspicious_activity', 4),
            
            # General category
            ('general', '🔐 Login Help', 'login_help', 1),
            ('general', '🔑 Password Issues', 'password_reset', 2),
            ('general', '👤 Account Questions', 'account_details', 3),
            ('general', '🛡️ Security Settings', 'security', 4),
            ('general', '🙋 Speak to Human', 'escalate', 5),
        ]

        reply_count = 0
        for category, title, payload, order in quick_replies:
            QuickReply.objects.create(
                category=category,
                title=title,
                payload=payload,
                order=order
            )
            reply_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {faq_count} FAQs and {reply_count} quick replies'
            )
        )

        # Display summary
        self.stdout.write('\nFAQs by category:')
        for category, _ in FAQ.CATEGORIES:
            count = FAQ.objects.filter(category=category).count()
            self.stdout.write(f'  {category}: {count} FAQs')

        self.stdout.write(f'\nTotal Quick Replies: {reply_count}')
        self.stdout.write('\n✅ Database population completed!')
        self.stdout.write('\n💡 You can now run the server and test the chatbot.')