import os

# SMTP Configuration for Email Notifications
SMTP_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": os.getenv("SMTP_USER", "swayamgupta999@gmail.com"),        # Your Gmail address
    "pass": os.getenv("SMTP_PASS", "bfoy dyjv sjvl bhrx")              # Your Gmail app password
}

# Email Recipients - support both environment variable and hardcoded list
recipient_emails = os.getenv("RECIPIENT_EMAILS")
if recipient_emails:
    # If environment variable exists (GitHub Actions), parse it
    email_list = [email.strip() for email in recipient_emails.split(",")]
else:
    # Fallback to hardcoded list (local development)
    email_list = ["swayamgupta2003@gmail.com", "vanshagarwal0144@gmail.com", "vaibhavwork0725@gmail.com", "dev.pant13@gmail.com", "pushpendrasingh9753@gmail.com"]

SUBSCRIBERS = {
    "emails": email_list
}

# ...existing code...

# Custom message template for batched internships
BATCH_MESSAGE_TEMPLATE = """🎯 **Fresh Internship Opportunities Alert- Notes Shaala** 🎯

Hello there,

I hope this email finds you well! Here are the latest handpicked internship opportunities that perfectly match your interests in Software Engineering, AI/ML, Data Analytics, Business Development, UI/UX, and specialized roles:

{internships_list}

📈 **What's Next?**
You'll receive fresh opportunities every time new relevant internships are found across all platforms. No spam, no repeats - just quality opportunities!

Best of luck with your applications! 🌟

---
Automated Internship Alert System

💌 This message was sent to you by Notes Shaala because you subscribed to our exclusive internship alerts."""

# Scheduling configuration
BATCH_INTERVAL_HOURS = 5  # Check every 5 hours (2-3 times per day)
MAX_EMAILS_PER_DAY = 3    # Maximum 3 emails per day to avoid spam
MIN_HOURS_BETWEEN_EMAILS = 4  # Minimum 4 hours between emails

