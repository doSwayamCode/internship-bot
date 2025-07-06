import smtplib
from email.mime.text import MIMEText
import pywhatkit as pwk
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

def send_whatsapp_to_group(group_name, message):
    try:
        pwk.sendwhatmsg_to_group_instantly(group_name, message, wait_time=10, tab_close=True)
        time.sleep(10)  # Give some buffer before closing tab
        print(f"💬 Sent WhatsApp message to group: {group_name}")
    except Exception as e:
        print(f"❌ Failed to send to group {group_name}: {e}")

def send_batch_whatsapp(group_name, internships_list, custom_message_template):
    """Send a batch of internships in a single WhatsApp message"""
    try:
        # Format the internships list
        formatted_internships = ""
        for i, job in enumerate(internships_list, 1):
            formatted_internships += f"{i}. **{job['title']}** at {job['company']}\n   🔗 {job['link']}\n\n"
        
        # Create the final message using the template
        final_message = custom_message_template.format(internships_list=formatted_internships)
        
        pwk.sendwhatmsg_to_group_instantly(group_name, final_message, wait_time=15, tab_close=True)
        time.sleep(15)  # Give some buffer before closing tab
        print(f"💬 Sent batch WhatsApp message to group: {group_name} with {len(internships_list)} internships")
    except Exception as e:
        print(f"❌ Failed to send batch message to group {group_name}: {e}")

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
