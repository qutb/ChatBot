# management/commands/populate_faqs.py
from django.core.management.base import BaseCommand
from chatbot.models import FAQ, QuickReply

class Command(BaseCommand):
    help = 'Populate the database with comprehensive FAQs and quick replies for the chatbot'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing FAQs and Quick Replies before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            FAQ.objects.all().delete()
            QuickReply.objects.all().delete()

        # Login & Authentication FAQs
        login_faqs = [
            {
                'question': 'I forgot my username. How can I recover it?',
                'answer': '''To recover your username:

**Method 1: Email Recovery**
1. Go to the login page
2. Click "Forgot Username?"
3. Enter your registered email address
4. Check your email for a message containing your username
5. If you don't receive it within 10 minutes, check your spam folder

**Method 2: Phone Recovery**
• If you have a phone number on file, you can also receive your username via SMS

**Still need help?** Contact our support team at support@company.com with:
• Your full name
• Email address associated with the account
• Any other identifying information''',
                'keywords': ['username', 'forgot', 'recover', 'email', 'login', 'remember'],
                'priority': 10
            },
            {
                'question': 'My account is locked. How do I unlock it?',
                'answer': '''Your account gets locked after 5 failed login attempts for security reasons.

**Unlock Options:**

**Option 1: Wait (Automatic)**
• Wait 30 minutes for automatic unlock
• Account will unlock automatically

**Option 2: Password Reset**
• Use "Forgot Password?" link on login page
• This immediately unlocks your account
• Create a new secure password

**Option 3: Contact Support**
• For immediate assistance
• We can unlock your account after identity verification

**Prevention Tips:**
• Double-check credentials before entering
• Use copy-paste for complex passwords
• Consider using a password manager
• Enable two-factor authentication for extra security''',
                'keywords': ['locked', 'unlock', 'account', 'security', 'failed', 'attempts', 'blocked'],
                'priority': 9
            },
            {
                'question': 'I keep getting "Invalid credentials" error. What should I do?',
                'answer': '''Try these troubleshooting steps in order:

**1. Check Your Input**
• Verify username/email spelling carefully
• Ensure Caps Lock is OFF
• Try typing password manually instead of copy-paste
• Check for extra spaces before or after your credentials

**2. Browser Issues**
• Clear browser cookies and cache
• Try incognito/private browsing mode
• Test with a different browser
• Disable browser extensions temporarily

**3. Account Status**
• Ensure your account hasn't been suspended
• Verify your email address is confirmed
• Check if you're using the correct login portal

**4. Password Issues**
• Try resetting your password if unsure
• Ensure you're using the current password (not an old one)

**Still having trouble?** Contact support with:
• Your username/email
• Browser and device information
• Screenshot of the error (without showing password)''',
                'keywords': ['invalid', 'credentials', 'error', 'username', 'password', 'login', 'wrong'],
                'priority': 8
            },
            {
                'question': 'I cannot access my account from a new device. Why?',
                'answer': '''Security measures may require additional verification on new devices:

**Common Causes:**
• Two-factor authentication required
• Device not recognized by our system
• Location-based security restrictions
• Account security settings

**Solutions:**

**For 2FA Issues:**
• Enter your 2FA code from authenticator app
• Use backup codes if app unavailable
• Request SMS code if enabled

**For Device Recognition:**
• Check email for device verification link
• Allow up to 24 hours for device approval
• Ensure you're using HTTPS connection

**For Location Issues:**
• VPN might be causing location conflicts
• Travel can trigger security measures
• Contact support if traveling internationally

**Contact Support If:**
• You can't access your 2FA device
• No verification email received
• Still blocked after following steps''',
                'keywords': ['new', 'device', 'access', 'blocked', 'verification', '2fa', 'location'],
                'priority': 7
            }
        ]

        # Password Management FAQs
        password_faqs = [
            {
                'question': 'How do I reset my password?',
                'answer': '''**Step-by-Step Password Reset:**

**Method 1: Email Reset**
1. Go to the login page
2. Click "Forgot Password?" or "Reset Password"
3. Enter your email address exactly as registered
4. Click "Send Reset Email"
5. Check your email (including spam/junk folders)
6. Click the reset link in the email
7. Create a new secure password
8. Confirm the new password
9. Log in with your new credentials

**Method 2: SMS Reset** (if enabled)
• Choose SMS option during reset
• Enter your registered phone number
• Use the code sent via text message

**Important Notes:**
• Reset links expire after 24 hours
• You can only request a new reset every 5 minutes
• Use a strong, unique password
• Don't close your browser during the process

**Not receiving emails?** Check our troubleshooting guide below.''',
                'keywords': ['reset', 'password', 'forgot', 'change', 'new', 'recover'],
                'priority': 10
            },
            {
                'question': 'What are the password requirements?',
                'answer': '''**Password Requirements:**

**Minimum Requirements:**
✅ At least 8 characters long
✅ At least one uppercase letter (A-Z)
✅ At least one lowercase letter (a-z)  
✅ At least one number (0-9)
✅ At least one special character (!@#$%^&*-_=+)

**Additional Security Guidelines:**
• Avoid common passwords (password123, admin, etc.)
• Don't use personal information (birthdate, name, etc.)
• Use a unique password not used elsewhere
• Consider using a passphrase for better security

**Examples of Strong Passwords:**
• `Coffee!Morning2024` (passphrase style)
• `Tr4il&Run#85` (mixed characters)
• `My$ecur3P@ss` (personal but secure)

**Password Manager Recommendation:**
We highly recommend using a password manager to generate and store unique, strong passwords for all your accounts.

**Need Help Creating One?**
Our password strength checker will guide you when you're setting up your new password.''',
                'keywords': ['password', 'requirements', 'strong', 'security', 'characters', 'rules'],
                'priority': 7
            },
            {
                'question': 'I am not receiving the password reset email. What should I do?',
                'answer': '''**Email Delivery Troubleshooting:**

**Immediate Steps:**
1. **Check spam/junk folder** - Reset emails often end up there
2. **Wait 10-15 minutes** - Email delivery can be delayed
3. **Check email address** - Ensure you entered it correctly
4. **Try again** - Request another reset email

**Email Provider Issues:**
**Gmail Users:**
• Check "Promotions" and "Updates" tabs
• Search for "password reset" or "noreply@company.com"

**Outlook/Hotmail Users:**
• Check "Junk Email" folder
• Add noreply@company.com to safe senders

**Yahoo Users:**
• Check "Bulk" folder
• Review spam filter settings

**Advanced Troubleshooting:**
• Try a different email address if available
• Contact your email provider about blocking
• Check if company emails are being filtered
• Try from a different device/network

**Whitelist Our Emails:**
Add these to your email whitelist:
• noreply@company.com
• support@company.com
• security@company.com

**Still No Email After 1 Hour?**
Contact support directly:
• Live chat available 24/7
• Phone: 1-800-XXX-XXXX
• Email: support@company.com''',
                'keywords': ['reset', 'email', 'not', 'received', 'spam', 'delivery', 'missing'],
                'priority': 8
            },
            {
                'question': 'My password reset link has expired. What now?',
                'answer': '''**Reset Link Expiration Info:**

**Why Links Expire:**
• Security measure to protect your account
• Links are valid for 24 hours only
• Prevents unauthorized access to old links

**What to Do:**

**Step 1: Request New Link**
1. Go back to the login page
2. Click "Forgot Password?" again
3. Enter your email address
4. Request a fresh reset link

**Step 2: Act Quickly**
• Use the new link within 24 hours
• Complete the reset in one session
• Don't close your browser during the process
• Save your new password immediately

**Step 3: Best Practices**
• Check email immediately after requesting
• Don't wait to use the reset link
• Complete the entire process at once
• Test your new password right away

**Pro Tips:**
• Set up password recovery options in advance
• Keep your recovery email up to date
• Consider using a password manager
• Enable two-factor authentication for extra security

**Multiple Expired Links?**
If you keep missing the deadline, contact support for assistance with immediate password reset.''',
                'keywords': ['reset', 'link', 'expired', 'timeout', '24', 'hours', 'new'],
                'priority': 6
            }
        ]

        # Account Management FAQs
        account_faqs = [
            {
                'question': 'How do I change my email address?',
                'answer': '''**Email Change Process:**

**Requirements:**
• Access to your current email address
• Access to the new email address
• Current account password

**Step-by-Step Instructions:**

**Step 1: Initiate Change**
1. Log into your account
2. Go to "Account Settings" or "Profile"
3. Find "Email Address" section
4. Click "Change Email" or "Edit"

**Step 2: Verification Process**
1. Enter your new email address
2. Enter your current password for security
3. Click "Save Changes" or "Update"
4. Check your NEW email for verification link
5. Click the verification link

**Step 3: Confirm Change**
• You'll receive confirmations at both email addresses
• Old email: "Email address changed" notification
• New email: "Welcome to your new email" message

**Important Security Notes:**
• Change will not take effect until verified
• You have 24 hours to complete verification
• Old email remains active until verification
• All future communications will go to new email

**Troubleshooting:**
• Not receiving verification email? Check spam folder
• Can't access old email? Contact support immediately
• Verification link expired? Start the process over

**Business Accounts:**
Additional approval may be required from your administrator.''',
                'keywords': ['email', 'change', 'update', 'address', 'modify', 'new'],
                'priority': 6
            },
            {
                'question': 'How do I update my phone number?',
                'answer': '''**Phone Number Update Process:**

**Why Update Your Phone Number:**
• Two-factor authentication (2FA)
• Account recovery via SMS
• Security notifications
• Emergency account access

**Step-by-Step Instructions:**

**Step 1: Account Settings**
1. Log into your account
2. Navigate to "Account Settings" 
3. Select "Contact Information" or "Security"
4. Find "Phone Number" section

**Step 2: Add/Update Number**
1. Click "Edit Phone Number"
2. Select your country code
3. Enter your new phone number (no dashes or spaces)
4. Choose verification method (SMS or Call)
5. Click "Update"

**Step 3: Verification**
1. You'll receive a verification code via SMS or call
2. Enter the 6-digit code in the verification field
3. Click "Verify" to confirm
4. Your phone number is now updated

**Phone Number Uses:**
• **2FA Authentication:** Secure login codes
• **Account Recovery:** Reset password via SMS
• **Security Alerts:** Suspicious activity notifications
• **Marketing:** Optional promotional messages (you can opt-out)

**International Numbers:**
• Include proper country code
• Format: +1234567890 (no spaces)
• Some regions may have restrictions

**Troubleshooting:**
• **Not receiving SMS?** Check signal strength, try calling option
• **Wrong format?** Remove all spaces, dashes, parentheses
• **Carrier blocking?** Contact your mobile provider''',
                'keywords': ['phone', 'number', 'update', 'change', 'mobile', 'sms', '2fa'],
                'priority': 5
            },
            {
                'question': 'How do I delete or deactivate my account?',
                'answer': '''**Account Deletion vs Deactivation:**

**Temporary Deactivation** (Recommended)
✅ Account is hidden but data preserved
✅ Can be reactivated anytime
✅ Subscriptions paused (not cancelled)
✅ Data remains for easy restoration

**Permanent Deletion**
❌ All data permanently removed
❌ Cannot be undone after grace period
❌ Subscriptions cancelled immediately
❌ Recovery impossible after deletion

**Temporary Deactivation Steps:**
1. Go to Account Settings
2. Select "Privacy & Security"
3. Click "Deactivate Account"
4. Choose deactivation period:
   • 1 week
   • 1 month  
   • 3 months
   • 6 months
5. Confirm your decision
6. Account immediately hidden from others

**Permanent Deletion Process:**
1. Contact our support team (cannot be done self-service)
2. Verify your identity for security
3. Understand 30-day grace period
4. Receive confirmation email
5. Data permanently deleted after grace period

**What Gets Deleted:**
• Profile information
• Messages and content
• Connections and relationships
• Purchase history (where legally allowed)
• Analytics and usage data

**What May Be Retained:**
• Legal compliance data (tax records, etc.)
• Anonymized usage statistics
• Data backup copies (securely destroyed within 90 days)

**Before You Delete:**
• Download your data using our export tool
• Cancel active subscriptions
• Inform important contacts of your decision
• Consider deactivation as an alternative

**Need Help Deciding?**
Contact our support team to discuss your options and concerns.''',
                'keywords': ['delete', 'deactivate', 'account', 'remove', 'close', 'cancel'],
                'priority': 4
            }
        ]

        # Security FAQs
        security_faqs = [
            {
                'question': 'How do I enable two-factor authentication (2FA)?',
                'answer': '''**Two-Factor Authentication Setup:**

Two-factor authentication adds an extra security layer to your account by requiring a second form of verification.

**Setup Process:**

**Step 1: Access Security Settings**
1. Log into your account
2. Go to "Account Settings"
3. Select "Security" or "Privacy & Security"
4. Find "Two-Factor Authentication" section

**Step 2: Choose Your Method**

**Authenticator App (Most Secure):**
• Download Google Authenticator, Authy, or Microsoft Authenticator
• Scan the QR code with your app
• Enter the 6-digit verification code
• Save your backup codes securely

**SMS Text Messages:**
• Enter your mobile phone number
• Receive verification codes via text
• Less secure than app method

**Email Codes:**
• Use your registered email for codes
• Backup option only

**Step 3: Test Your Setup**
1. Log out of your account
2. Log back in with username/password
3. Enter the 2FA code when prompted
4. Confirm successful login

**Important Security Notes:**
• **Save backup codes** in a secure location
• Set up multiple 2FA methods if possible
• Keep your authenticator device secure
• Report lost devices immediately

**Benefits of 2FA:**
• 99.9% reduction in account takeover risk
• Protection even if password is compromised
• Required for accessing sensitive features
• Peace of mind for your digital security

**Backup Codes:**
• Generate 10 single-use backup codes
• Use if your 2FA device is unavailable
• Store securely (not on your phone)
• Generate new ones after using''',
                'keywords': ['2fa', 'two', 'factor', 'authentication', 'security', 'enable', 'setup'],
                'priority': 9
            },
            {
                'question': 'I lost my 2FA device. How can I access my account?',
                'answer': '''**Emergency 2FA Access:**

Don't panic! There are several recovery options available.

**Immediate Options:**

**Option 1: Use Backup Codes**
• Locate your saved backup codes
• Use any unused backup code to log in
• Generate new backup codes immediately after login
• Each code can only be used once

**Option 2: Alternative 2FA Method**
• Try SMS if you set up text message 2FA
• Use email codes if configured
• Try a different authenticator app if you have multiple

**Option 3: Trusted Device**
• If you're still logged in on another device
• Go to Security Settings
• Temporarily disable 2FA
• Re-enable with new device

**Account Recovery Process:**

**When Other Options Don't Work:**
1. **Contact Support Immediately**
   • Use "Account Recovery" option
   • Provide detailed account information
   • Include proof of identity

2. **Identity Verification Required:**
   • Government-issued ID
   • Account creation details
   • Recent account activity
   • Security questions (if set up)

3. **Recovery Timeline:**
   • Standard recovery: 24-48 hours
   • Complex cases: Up to 5 business days
   • Expedited service available for premium accounts

**Prevention for Future:**

**Set Up Multiple Methods:**
• Primary: Authenticator app
• Backup: SMS to phone
• Emergency: Backup codes
• Alternative: Recovery email

**Secure Storage:**
• Store backup codes in password manager
• Keep physical copy in safe location
• Don't store codes on the same device as authenticator
• Update recovery information regularly

**Device Management:**
• Register multiple trusted devices
• Keep recovery information current
• Test backup methods periodically

**What NOT to Do:**
• Don't create new accounts
• Don't ignore the problem hoping it resolves
• Don't share account details with unauthorized helpers''',
                'keywords': ['2fa', 'lost', 'device', 'backup', 'codes', 'recovery', 'access'],
                'priority': 10
            }
        ]

        # Billing FAQs
        billing_faqs = [
            {
                'question': 'How do I view and download my invoices?',
                'answer': '''**Invoice Access:**

**Viewing Invoices Online:**
1. Log into your account
2. Navigate to "Account Settings" or "Billing"
3. Select "Billing History" or "Invoices"
4. View list of all invoices by date
5. Click any invoice to view details

**Downloading Invoices:**
• Click the "Download PDF" button next to any invoice
• Choose "Print" option for physical copies
• Bulk download available for multiple invoices
• Invoices saved in standard PDF format

**Invoice Information Includes:**
• Invoice number and date
• Billing period covered
• Itemized charges and descriptions
• Payment method used
• Tax information (where applicable)
• Company billing address

**Getting Copies Sent to Email:**
• Invoices automatically sent to billing email
• Add additional recipients in billing settings
• Request copies for specific date ranges
• Historical invoices available for 7 years

**For Businesses:**
• VAT/Tax ID included where applicable
• Purchase order numbers can be added
• Custom billing information supported
• Integration with accounting software available

**Need Help Finding Specific Invoices?**
Contact billing support with:
• Account information
• Approximate date range
• Invoice number (if known)
• Purpose (expense reports, tax filing, etc.)''',
                'keywords': ['invoice', 'billing', 'download', 'view', 'receipt', 'statement'],
                'priority': 6
            },
            {
                'question': 'How do I update my payment method?',
                'answer': '''**Payment Method Management:**

**Adding New Payment Method:**
1. Go to Account Settings > Billing
2. Click "Payment Methods" or "Cards & Banking"
3. Select "Add Payment Method"
4. Choose your payment type:
   • Credit/Debit Card
   • Bank Account (ACH)
   • Digital Wallet (PayPal, Apple Pay, etc.)
5. Enter payment details securely
6. Verify the payment method

**Updating Existing Cards:**
• Update expiration date
• Change billing address
• Replace lost/stolen cards
• Switch primary payment method

**Setting Primary Payment Method:**
1. View all saved payment methods
2. Select preferred method
3. Click "Set as Primary" or "Make Default"
4. Confirm the change

**Accepted Payment Types:**
• **Credit Cards:** Visa, MasterCard, American Express
• **Debit Cards:** Most major banks supported
• **Bank Transfers:** ACH (US), SEPA (EU)
• **Digital Wallets:** PayPal, Apple Pay, Google Pay
• **Corporate Cards:** Business accounts accepted

**Payment Security:**
• All payment info encrypted with industry standards
• PCI DSS compliant processing
• No card details stored on our servers
• Tokenized payments for recurring charges

**International Payments:**
• Multi-currency support
• Foreign transaction fees may apply (from your bank)
• Exchange rates updated daily
• Local payment methods in select regions

**Troubleshooting Payment Issues:**
• **Card Declined:** Contact your bank first
• **Expired Card:** Update expiration date
• **Insufficient Funds:** Check account balance
• **Billing Address Mismatch:** Update address information

**Removing Payment Methods:**
• Can only remove if not set as primary
• Must have at least one active payment method
• Removed cards cannot be recovered (re-add if needed)''',
                'keywords': ['payment', 'method', 'card', 'billing', 'update', 'credit', 'debit'],
                'priority': 5
            }
        ]

        # Technical Support FAQs
        technical_faqs = [
            {
                'question': 'The website/app is running slowly. How can I fix this?',
                'answer': '''**Performance Troubleshooting:**

**Quick Fixes to Try First:**

**Browser Issues:**
• Clear browser cache and cookies
• Disable unnecessary browser extensions
• Update to the latest browser version
• Try incognito/private browsing mode
• Restart your browser completely

**Internet Connection:**
• Test your internet speed (use speedtest.net)
• Try different network (mobile data vs WiFi)
• Restart your router/modem
• Move closer to WiFi router
• Contact ISP if speeds are consistently slow

**Device Performance:**
• Close other applications and browser tabs
• Restart your device
• Check available storage space
• Update your operating system
• Scan for malware/viruses

**Advanced Troubleshooting:**

**DNS Issues:**
• Try switching DNS servers:
  - Google DNS: 8.8.8.8, 8.8.4.4
  - Cloudflare DNS: 1.1.1.1, 1.0.0.1
• Flush DNS cache on your computer

**Browser Settings:**
• Disable hardware acceleration if enabled
• Reset browser to default settings
• Try a different browser (Chrome, Firefox, Safari, Edge)
• Check if JavaScript is enabled

**Network Optimization:**
• Use ethernet instead of WiFi when possible
• Close streaming services and downloads
• Limit other devices using the network
• Check for background app updates

**When to Contact Support:**

**Provide This Information:**
• Device type and operating system
• Browser name and version
• Internet connection type and speed
• Specific pages/features that are slow
• Error messages (if any)
• Steps you've already tried

**System Status Check:**
• Visit our status page: status.company.com
• Check for ongoing maintenance or outages
• Subscribe to status updates

**Performance may also be affected by:**
• High traffic periods (usually business hours)
• Scheduled maintenance windows
• Your geographic location
• Large file uploads or downloads in progress''',
                'keywords': ['slow', 'performance', 'loading', 'speed', 'lag', 'website', 'app'],
                'priority': 7
            },
            {
                'question': 'I am getting error messages. What do they mean?',
                'answer': '''**Common Error Messages & Solutions:**

**Connection Errors:**

**"Unable to connect" / "Network Error"**
• Check your internet connection
• Try refreshing the page (Ctrl+F5 or Cmd+Shift+R)
• Clear browser cache
• Try a different browser or device

**"Timeout Error" / "Request Timed Out"**
• Your connection is too slow or unstable
• Try again in a few minutes
• Switch to a more stable network
• Contact support if error persists

**Authentication Errors:**

**"Session Expired"**
• You've been logged out for security
• Simply log in again
• Enable "Remember Me" to stay logged in longer

**"Access Denied" / "Unauthorized"**
• Check if you're logged into the correct account
• Verify you have permission for this action
• Contact your administrator if this is a business account

**Application Errors:**

**"500 Internal Server Error"**
• Temporary server issue on our end
• Try again in a few minutes
• If persistent, contact support

**"404 Not Found"**
• The page you're looking for doesn't exist
• Check the URL for typos
• Use our search feature to find what you need

**"403 Forbidden"**
• You don't have permission to access this resource
• Log in if you haven't already
• Contact support if you believe you should have access

**Form/Input Errors:**

**"Invalid Input" / "Required Field"**
• Check for missing required information
• Ensure data format is correct (email, phone, etc.)
• Remove special characters if not allowed

**"File Upload Error"**
• File may be too large (check size limits)
• File type not supported
• Try a different file or compress large files

**Payment Errors:**

**"Payment Failed" / "Card Declined"**
• Contact your bank first
• Verify billing address matches card
• Check if card is expired or has sufficient funds

**Getting Help:**

**When Contacting Support, Include:**
• Exact error message (screenshot helpful)
• What you were trying to do when error occurred
• Your browser and device information
• Steps to reproduce the error
• Your account information (but never passwords)

**Browser Console Errors:**
• Press F12 to open developer tools
• Check Console tab for technical errors
• This helps our technical team diagnose issues

**Error Code Reference:**
• Many errors include specific codes (like Error 1001)
• Reference these codes when contacting support
• Check our error code documentation online''',
                'keywords': ['error', 'message', 'bug', 'problem', 'issue', '404', '500', 'timeout'],
                'priority': 8
            }
        ]

        # Compile all FAQs
        all_faqs = [
            ('login', login_faqs),
            ('password', password_faqs),
            ('account', account_faqs),
            ('security', security_faqs),
            ('billing', billing_faqs),
            ('technical', technical_faqs)
        ]

        # Create FAQ entries
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
        quick_replies_data = [
            # Login category
            ('login', '🔐 Forgot Username', 'forgot_username', 1, '🔐'),
            ('login', '🔒 Account Locked', 'account_locked', 2, '🔒'),
            ('login', '❌ Invalid Credentials', 'invalid_credentials', 3, '❌'),
            ('login', '📱 2FA Issues', '2fa_issues', 4, '📱'),
            
            # Password category
            ('password', '🔑 Reset Password', 'password_reset', 1, '🔑'),
            ('password', '📋 Password Requirements', 'password_requirements', 2, '📋'),
            ('password', '📧 No Reset Email', 'no_reset_email', 3, '📧'),
            ('password', '⏰ Reset Link Expired', 'reset_link_expired', 4, '⏰'),
            
            # Account category
            ('account', '📧 Change Email', 'change_email', 1, '📧'),
            ('account', '📞 Update Phone', 'update_phone', 2, '📞'),
            ('account', 'ℹ️ Personal Info', 'personal_info', 3, 'ℹ️'),
            ('account', '🗑️ Delete Account', 'delete_account', 4, '🗑️'),
            
            # Security category
            ('security', '🔐 Enable 2FA', 'enable_2fa', 1, '🔐'),
            ('security', '💡 Security Tips', 'security_tips', 2, '💡'),
            ('security', '📱 Lost 2FA Device', 'lost_2fa_device', 3, '📱'),
            ('security', '⚠️ Suspicious Activity', 'suspicious_activity', 4, '⚠️'),
            
            # Billing category
            ('billing', '📄 View Invoices', 'view_invoice', 1, '📄'),
            ('billing', '💳 Update Payment', 'update_payment', 2, '💳'),
            ('billing', '↩️ Refund Request', 'refund_request', 3, '↩️'),
            ('billing', '❓ Billing Issues', 'billing_issues', 4, '❓'),
            
            # Technical category
            ('technical', '🐛 Report Bug', 'report_bug', 1, '🐛'),
            ('technical', '⚡ Performance Issues', 'performance_issues', 2, '⚡'),
            ('technical', '🔧 Feature Not Working', 'feature_not_working', 3, '🔧'),
            ('technical', '🌐 Browser Issues', 'browser_issues', 4, '🌐'),
            
            # General category
            ('general', '🔐 Login Help', 'login_help', 1, '🔐'),
            ('general', '🔑 Password Issues', 'password_reset', 2, '🔑'),
            ('general', '👤 Account Questions', 'account_details', 3, '👤'),
            ('general', '🛡️ Security Settings', 'security', 4, '🛡️'),
            ('general', '💳 Billing Help', 'billing', 5, '💳'),
            ('general', '🔧 Technical Support', 'technical', 6, '🔧'),
            ('general', '🙋 Speak to Human', 'escalate', 7, '🙋'),
        ]

        reply_count = 0
        for category, title, payload, order, icon in quick_replies_data:
            QuickReply.objects.create(
                category=category,
                title=title,
                payload=payload,
                order=order,
                icon=icon
            )
            reply_count += 1

        # Display results
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {faq_count} FAQs and {reply_count} quick replies!'
            )
        )

        # Display summary by category
        self.stdout.write('\n📊 FAQs by category:')
        categories = FAQ.CATEGORIES
        for category_code, category_name in categories:
            count = FAQ.objects.filter(category=category_code).count()
            if count > 0:
                self.stdout.write(f'  • {category_name}: {count} FAQs')

        self.stdout.write(f'\n📋 Total Quick Replies: {reply_count}')
        self.stdout.write(self.style.SUCCESS('\n✅ Database population completed!'))
        self.stdout.write('💡 You can now run the server and test the chatbot.')
        self.stdout.write('\n📝 To add more questions, edit this file and run: python manage.py populate_faqs --clear')
