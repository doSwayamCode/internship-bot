import smtplib
from email.mime.text import MIMEText
import time
from datetime import datetime
from email_tracker import log_email_send, log_internship_data, init_tracking_files

# Initialize tracking files when module is imported
init_tracking_files()

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

def send_batch_email(to, internships_list, custom_message, smtp_cfg, bot_run_id=None):
    """Send a batch of internships in a single email with custom formatting"""
    if bot_run_id is None:
        bot_run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        # If custom_message is already formatted, use it directly
        if isinstance(custom_message, str) and "{internships_list}" not in custom_message:
            final_message = custom_message
        else:
            # Format the internships list for email with enhanced details
            formatted_internships = ""
            for i, job in enumerate(internships_list, 1):
                # Enhanced formatting with source and sector info
                sector_info = f" | {job.get('sector', 'General')}" if job.get('sector') else ""
                source_info = f" | via {job.get('source', 'Portal')}"
                location_info = f" | {job.get('location', 'Location TBD')}"
                
                formatted_internships += f"{i}. {job['title']} at {job['company']}\n"
                formatted_internships += f"   📍{location_info}{sector_info}{source_info}\n"
                formatted_internships += f"   🔗 Link: {job['link']}\n\n"
            
            # Create the final message using the template
            final_message = custom_message.format(
                total_count=len(internships_list),
                internships_list=formatted_internships
            )
        
        subject = f"🎯 New Internship Alert - {len(internships_list)} Fresh Opportunities!"
        
        msg = MIMEText(final_message)
        msg['Subject'] = subject
        msg['From'] = smtp_cfg['user']
        msg['To'] = to
        
        with smtplib.SMTP(smtp_cfg['host'], smtp_cfg['port']) as s:
            s.starttls()
            s.login(smtp_cfg['user'], smtp_cfg['pass'])
            s.send_message(msg)
        
        # Log successful email send
        log_email_send(to, len(internships_list), subject, 'success', bot_run_id)
        print(f"📧 Sent internship batch to {to} ({len(internships_list)} opportunities)")
        
    except Exception as e:
        # Log failed email send
        log_email_send(to, len(internships_list), f"Failed: {str(e)}", 'failed', bot_run_id)
        print(f"❌ Failed to send batch email to {to}: {e}")
        raise  # Re-raise to handle in calling function
