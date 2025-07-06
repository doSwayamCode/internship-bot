import smtplib
from email.mime.text import MIMEText
import time

def send_email(to, subject, body, smtp_cfg):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_cfg['user']
    msg['To'] = to
    with smtplib.SMTP(smtp_cfg['host'], smtp_cfg['port']) as s:
        s.starttls()
        s.login(smtp_cfg['user'], smtp_cfg['pass'])
        s.send_message(msg)
    print(f"📧 Sent email to {to}")


# WhatsApp functionality removed - Email-only bot

def send_batch_email(to, internships_list, custom_message, smtp_cfg):
    """Send a batch of internships in a single email with custom formatting"""
    try:
        # If custom_message is already formatted, use it directly
        if isinstance(custom_message, str) and "{internships_list}" not in custom_message:
            final_message = custom_message
        else:
            # Format the internships list for email if needed
            formatted_internships = ""
            for i, job in enumerate(internships_list, 1):
                formatted_internships += f"{i}. {job['title']} at {job['company']}\n   Link: {job['link']}\n\n"
            
            # Create the final message using the template
            final_message = custom_message.format(internships_list=formatted_internships)
        
        subject = f"🎯 New Internship Alert - {len(internships_list)} Fresh Opportunities!"
        
        msg = MIMEText(final_message)
        msg['Subject'] = subject
        msg['From'] = smtp_cfg['user']
        msg['To'] = to
        
        with smtplib.SMTP(smtp_cfg['host'], smtp_cfg['port']) as s:
            s.starttls()
            s.login(smtp_cfg['user'], smtp_cfg['pass'])
            s.send_message(msg)
        print(f"📧 Sent internship batch to {to} ({len(internships_list)} opportunities)")
    except Exception as e:
        print(f"❌ Failed to send batch email to {to}: {e}")
        raise  # Re-raise to handle in calling function
