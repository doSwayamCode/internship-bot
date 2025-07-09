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
• Sources Monitored: Internshala, LinkedIn, TimesJobs (reliable sources only)
• Next Check: In 5 hours
• Alert Frequency: Smart (only when new opportunities found)

🔮 **What's Next?**
You'll receive the next alert only when fresh opportunities are discovered. No spam, no repeats - just quality internships delivered to your inbox!

Best of luck with your applications! 🌟

---
**Smart Internship Bot** | Powered by AI
🤖 Automated • 🎯 Targeted • 📧 Spam-Free

💡 *This intelligent system monitors the job market 24/7 so you don't have to.*

---
📧 **Manage Your Subscription:**
• To unsubscribe from these alerts, click here: https://forms.gle/k9DHTg8w6Gg5LMh89
• Or reply to this email with "UNSUBSCRIBE" in the subject line

🔒 Your email privacy is protected - we never share your information."""

