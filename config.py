import os

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

SUBSCRIBERS = {
    "emails": email_list
}

# ...existing code...

# Custom message template for batched internships
BATCH_MESSAGE_TEMPLATE = """🚀 **Smart Internship Alert - Fresh Opportunities Found!** 

Dear Future Professional,

Great news! Our intelligent system has discovered {total_count} new internship opportunities that match your career interests. These positions have been carefully filtered and verified to ensure they're fresh (posted within the last 2 weeks) and relevant to your skills.

{internships_list}

📊 **Why These Opportunities?**
• ✅ **Fresh Postings**: All opportunities are less than 2 weeks old
• ✅ **AI-Filtered**: Automatically matched to your tech interests
• ✅ **Duplicate-Free**: Each opportunity is unique and verified
• ✅ **Multi-Source**: Scraped from 10+ premium job platforms

🎯 **Quick Application Tips:**
• Apply within 24-48 hours for best response rates
• Tailor your resume to highlight relevant skills
• Research the company before applying
• Follow up professionally after 1 week

📈 **System Stats:**
• Sources Monitored: Internshala, LinkedIn, TimesJobs, Foundit, FreshersWorld, Instahyre, Wellfound & more
• Next Check: In 5 hours
• Alert Frequency: Smart (only when new opportunities found)

� **What's Next?**
You'll receive the next alert only when fresh opportunities are discovered. No spam, no repeats - just quality internships delivered to your inbox!

Best of luck with your applications! 🌟

---
**Smart Internship Bot** | Powered by AI
🤖 Automated • 🎯 Targeted • 📧 Spam-Free

� *This intelligent system monitors the job market 24/7 so you don't have to.*"""

# Scheduling configuration
BATCH_INTERVAL_HOURS = 5  # Check every 5 hours (2-3 times per day)
MAX_EMAILS_PER_DAY = 3    # Maximum 3 emails per day to avoid spam
MIN_HOURS_BETWEEN_EMAILS = 4  # Minimum 4 hours between emails

