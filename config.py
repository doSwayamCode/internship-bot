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

# Dynamic Subscriber Management System
# Load subscriber emails from file-based system (supports dynamic add/remove)
def load_subscribers():
    """Load subscriber emails from various sources"""
    subscribers = []
    
    # Check if we have a subscribers file
    import json
    import os
    
    # Try to load from subscribers.json (main source)
    if os.path.exists("subscribers.json"):
        try:
            with open("subscribers.json", "r") as f:
                data = json.load(f)
                subscribers = data.get("emails", [])
                print(f"📧 Loaded {len(subscribers)} subscribers from subscribers.json")
        except Exception as e:
            print(f"⚠️ Error loading subscribers.json: {e}")
    
    # Fallback to environment variable if no file exists
    if not subscribers:
        recipient_emails = os.getenv("RECIPIENT_EMAILS")
        if recipient_emails:
            subscribers = [email.strip() for email in recipient_emails.split(",")]
            print(f"📧 Loaded {len(subscribers)} subscribers from environment variable")
        else:
            # Last resort - hardcoded list (REPLACE WITH YOUR EMAILS)
            subscribers = ["recipient1@example.com", "recipient2@example.com"]
            print("📧 Using fallback subscriber list - please update!")
    
    # Filter out unsubscribed emails
    active_subscribers = get_active_emails(subscribers)
    print(f"📧 Active subscribers after filtering unsubscribes: {len(active_subscribers)}")
    return active_subscribers

SUBSCRIBERS = load_subscribers()

# Custom message template for batched internships
BATCH_MESSAGE_TEMPLATE = """🚀Internships Alert - Intern wala! 

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
- Thanks for using Intern wala"""

