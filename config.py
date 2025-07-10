import os

# Import unsubscribe functionality
try:
    from unsubscribe_manager import get_active_emails
except ImportError:
    # Fallback if unsubscribe_manager is not available
    def get_active_emails(email_list):
        return email_list

# SMTP Configuration for Email Notifications
SMTP_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": os.getenv("SMTP_USER", "your-email@gmail.com"),        # Replace with your Gmail
    "pass": os.getenv("SMTP_PASS", "your-app-password-here")       # Replace with your Gmail app password
}

# Email Recipients - support both environment variable and hardcoded list
recipient_emails = os.getenv("RECIPIENT_EMAILS")
if recipient_emails:
    # If environment variable exists (GitHub Actions), parse it
    email_list = [email.strip() for email in recipient_emails.split(",")]
else:
    # Fallback to hardcoded list (local development) - REPLACE WITH YOUR EMAILS
    email_list = ["recipient1@example.com", "recipient2@example.com"]

# Filter out unsubscribed emails
active_email_list = get_active_emails(email_list)

SUBSCRIBERS = {
    "emails": active_email_list
}

# Custom message template for batched internships
BATCH_MESSAGE_TEMPLATE = """🚀Internship Alert - Notes Shaala! 

hi,

Great news! We have discovered {total_count} new internship opportunities that match your career interests.

{internships_list}

Best of luck with your applications we at Notes Shaala wish your success!

---
Internship Bot | Brought to you by Swayam
Automated & Spam-Free
---
Manage Your Subscription:
• To unsubscribe from these alerts, click here: https://forms.gle/k9DHTg8w6Gg5LMh89
• Or reply to this email with "UNSUBSCRIBE" in the subject line


🔒 Your email privacy is protected - we never share it.
Team Notes Shaala"""

