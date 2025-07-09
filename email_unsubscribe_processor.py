#!/usr/bin/env python3
"""
Simple Email-Based Unsubscribe Processor
Alternative method: Users email you directly to unsubscribe
"""

import imaplib
import email
import os
from datetime import datetime
from unsubscribe_manager import add_unsubscribe

def process_unsubscribe_emails():
    """Check email inbox for unsubscribe requests"""
    
    # Email configuration (use your Gmail credentials)
    imap_server = "imap.gmail.com"
    imap_port = 993
    username = os.getenv('SMTP_USER')  # Same as your sending email
    password = os.getenv('SMTP_PASS')  # Same as your app password
    
    if not username or not password:
        print("❌ Email credentials not configured")
        print("ℹ️ This is normal if running locally without environment variables")
        return
    
    try:
        print(f"🔍 Checking {username} inbox for unsubscribe requests...")
        
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(username, password)
        mail.select('inbox')
        
        # Search for unsubscribe emails
        search_criteria = '(SUBJECT "UNSUBSCRIBE")'
        result, data = mail.search(None, search_criteria)
        
        if result != 'OK':
            print("❌ Failed to search emails")
            return
        
        email_ids = data[0].split()
        new_unsubscribes = 0
        
        print(f"📧 Found {len(email_ids)} unsubscribe emails")
        
        for email_id in email_ids:
            # Fetch email
            result, data = mail.fetch(email_id, '(RFC822)')
            
            if result == 'OK':
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                # Get sender email
                sender = email_message['From']
                
                # Extract email address from sender field
                if '<' in sender and '>' in sender:
                    sender_email = sender.split('<')[1].split('>')[0].strip().lower()
                else:
                    sender_email = sender.strip().lower()
                
                # Add to unsubscribe list
                if add_unsubscribe(sender_email):
                    new_unsubscribes += 1
                    print(f"✅ Processed unsubscribe: {sender_email}")
                    
                    # Mark email as read/processed
                    mail.store(email_id, '+FLAGS', '\\Seen')
        
        mail.close()
        mail.logout()
        
        print(f"✅ Processed {new_unsubscribes} new email-based unsubscribes")
        
    except Exception as e:
        print(f"❌ Error processing emails: {e}")
        print("ℹ️ This is normal if no emails are available or credentials are incorrect")

if __name__ == "__main__":
    print("📧 Email-Based Unsubscribe Processor")
    print("=" * 40)
    process_unsubscribe_emails()
