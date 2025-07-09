#!/usr/bin/env python3
"""
Email-based Re-subscription Processor for InternBot
Processes "RESUBSCRIBE" or "SUBSCRIBE" emails to re-activate subscriptions
"""

import imaplib
import email
import re
from datetime import datetime
from unsubscribe_manager import remove_unsubscribe, is_unsubscribed
from config import EMAIL_CONFIG

def process_resubscribe_emails():
    """Process emails looking for resubscribe requests"""
    if not EMAIL_CONFIG:
        print("⚠️ Email configuration not found. Skipping resubscribe processing.")
        return []
    
    resubscribed = []
    
    try:
        # Connect to email server
        mail = imaplib.IMAP4_SSL(EMAIL_CONFIG['imap_server'])
        mail.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        mail.select('inbox')
        
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        
        if status == 'OK' and messages[0]:
            email_ids = messages[0].split()
            print(f"📧 Found {len(email_ids)} unread emails to check for resubscribe requests")
            
            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                
                if status == 'OK':
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    # Get sender email
                    sender = email_message['From']
                    sender_email = extract_email_address(sender)
                    
                    # Get email content
                    content = get_email_content(email_message)
                    
                    # Check if this is a resubscribe request
                    if is_resubscribe_request(content):
                        print(f"📬 Resubscribe request from: {sender_email}")
                        
                        # Check if email is actually unsubscribed
                        if is_unsubscribed(sender_email):
                            if remove_unsubscribe(sender_email):
                                resubscribed.append(sender_email)
                                print(f"✅ Re-subscribed: {sender_email}")
                            else:
                                print(f"⚠️ Failed to re-subscribe: {sender_email}")
                        else:
                            print(f"ℹ️ {sender_email} was not unsubscribed")
                        
                        # Mark as read to avoid reprocessing
                        mail.store(email_id, '+FLAGS', '\\Seen')
        
        mail.logout()
        
    except Exception as e:
        print(f"❌ Error processing resubscribe emails: {e}")
    
    return resubscribed

def extract_email_address(from_field):
    """Extract clean email address from 'From' field"""
    if '<' in from_field and '>' in from_field:
        return re.search(r'<(.+?)>', from_field).group(1).lower()
    else:
        return from_field.strip('<>').lower()

def get_email_content(email_message):
    """Extract text content from email message"""
    content = ""
    
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                try:
                    content += part.get_payload(decode=True).decode('utf-8')
                except:
                    content += str(part.get_payload())
    else:
        try:
            content = email_message.get_payload(decode=True).decode('utf-8')
        except:
            content = str(email_message.get_payload())
    
    return content.lower()

def is_resubscribe_request(content):
    """Check if email content contains resubscribe keywords"""
    resubscribe_keywords = [
        'resubscribe',
        'subscribe',
        'subscribe again',
        'sign me up',
        'opt in',
        'rejoin',
        'resume emails',
        'start emails'
    ]
    
    content_lower = content.lower().strip()
    
    for keyword in resubscribe_keywords:
        if keyword in content_lower:
            return True
    
    return False

def send_resubscribe_confirmation(email_address, smtp_config):
    """Send confirmation email for successful re-subscription"""
    try:
        from messenger import send_email
        
        subject = "🎉 Welcome Back to InternBot Alerts!"
        
        body = f"""
Hello!

You have successfully re-subscribed to InternBot internship alerts! 🎯

You will now receive notifications about new internship opportunities directly to this email address.

If you ever want to unsubscribe again, simply reply to any internship alert email with "UNSUBSCRIBE".

Happy job hunting! 🚀

Best regards,
InternBot Team

---
This is an automated message from InternBot.
        """.strip()
        
        send_email(email_address, subject, body, smtp_config)
        print(f"📧 Sent resubscribe confirmation to {email_address}")
        
    except Exception as e:
        print(f"❌ Failed to send confirmation to {email_address}: {e}")

if __name__ == "__main__":
    print("🔄 Processing Resubscribe Requests...")
    resubscribed_emails = process_resubscribe_emails()
    
    if resubscribed_emails:
        print(f"\n✅ Successfully re-subscribed {len(resubscribed_emails)} email(s):")
        for email in resubscribed_emails:
            print(f"   • {email}")
        
        # Optionally send confirmation emails
        try:
            from config import SMTP_CONFIG
            for email in resubscribed_emails:
                send_resubscribe_confirmation(email, SMTP_CONFIG)
        except Exception as e:
            print(f"⚠️ Could not send confirmation emails: {e}")
    else:
        print("📭 No resubscribe requests found")
