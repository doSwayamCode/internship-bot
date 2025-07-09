#!/usr/bin/env python3
"""
Simple Unsubscribe Management for InternBot
This script helps manage unsubscribe requests
"""

import json
import os
from datetime import datetime

UNSUBSCRIBED_FILE = 'unsubscribed_emails.json'

def load_unsubscribed():
    """Load list of unsubscribed emails"""
    try:
        with open(UNSUBSCRIBED_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_unsubscribed(unsubscribed_list):
    """Save list of unsubscribed emails"""
    with open(UNSUBSCRIBED_FILE, 'w') as f:
        json.dump(unsubscribed_list, f, indent=2)

def add_unsubscribe(email):
    """Add an email to unsubscribe list"""
    unsubscribed = load_unsubscribed()
    if email not in unsubscribed:
        unsubscribed.append({
            'email': email,
            'unsubscribed_at': datetime.now().isoformat()
        })
        save_unsubscribed(unsubscribed)
        print(f"✅ {email} has been unsubscribed")
        return True
    else:
        print(f"ℹ️ {email} was already unsubscribed")
        return False

def is_unsubscribed(email):
    """Check if an email is unsubscribed"""
    unsubscribed = load_unsubscribed()
    unsubscribed_emails = [item['email'] if isinstance(item, dict) else item for item in unsubscribed]
    return email in unsubscribed_emails

def remove_unsubscribe(email):
    """Remove an email from unsubscribe list (re-subscribe)"""
    unsubscribed = load_unsubscribed()
    original_count = len(unsubscribed)
    
    # Remove email from list (handle both dict and string formats)
    unsubscribed = [
        item for item in unsubscribed 
        if (item['email'] if isinstance(item, dict) else item) != email
    ]
    
    if len(unsubscribed) < original_count:
        save_unsubscribed(unsubscribed)
        print(f"✅ {email} has been re-subscribed")
        return True
    else:
        print(f"ℹ️ {email} was not in the unsubscribe list")
        return False

def get_active_emails(email_list):
    """Filter out unsubscribed emails from a list"""
    return [email for email in email_list if not is_unsubscribed(email)]

def get_unsubscribed_list():
    """Get list of all unsubscribed emails"""
    unsubscribed = load_unsubscribed()
    return [item['email'] if isinstance(item, dict) else item for item in unsubscribed]

def get_unsubscribe_count():
    """Get count of unsubscribed emails"""
    return len(load_unsubscribed())

def manual_unsubscribe():
    """Manual unsubscribe interface"""
    print("🚫 Manual Unsubscribe Tool")
    print("=" * 30)
    
    email = input("Enter email to unsubscribe: ").strip().lower()
    
    if not email or '@' not in email:
        print("❌ Invalid email address")
        return
    
    if add_unsubscribe(email):
        print(f"✅ {email} has been successfully unsubscribed")
        print("They will no longer receive internship alerts.")
    else:
        print(f"ℹ️ {email} was already unsubscribed")

def manual_resubscribe():
    """Manual re-subscribe interface"""
    print("🔄 Manual Re-subscribe Tool")
    print("=" * 30)
    
    # Show current unsubscribed emails
    unsubscribed_list = get_unsubscribed_list()
    if unsubscribed_list:
        print("\nCurrently unsubscribed emails:")
        for i, email in enumerate(unsubscribed_list, 1):
            print(f"{i}. {email}")
        print()
    else:
        print("No emails are currently unsubscribed.")
        return
    
    email = input("Enter email to re-subscribe: ").strip().lower()
    
    if not email or '@' not in email:
        print("❌ Invalid email address")
        return
    
    if remove_unsubscribe(email):
        print(f"✅ {email} has been successfully re-subscribed")
        print("They will now receive internship alerts again.")
    else:
        print(f"ℹ️ {email} was not in the unsubscribe list")

def list_unsubscribed():
    """List all unsubscribed emails"""
    unsubscribed = load_unsubscribed()
    
    if not unsubscribed:
        print("📭 No unsubscribed emails found")
        return
    
    print(f"🚫 Unsubscribed Emails ({len(unsubscribed)}):")
    print("=" * 40)
    
    for item in unsubscribed:
        if isinstance(item, dict):
            email = item['email']
            date = item.get('unsubscribed_at', 'Unknown date')
            print(f"• {email} (unsubscribed: {date})")
        else:
            print(f"• {item}")

if __name__ == "__main__":
    print("🔧 InternBot Unsubscribe Manager")
    print("1. Manually unsubscribe an email")
    print("2. Manually re-subscribe an email")
    print("3. List unsubscribed emails")
    print("4. Show statistics")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        manual_unsubscribe()
    elif choice == "2":
        manual_resubscribe()
    elif choice == "3":
        list_unsubscribed()
    elif choice == "4":
        print("\n📊 Unsubscribe Statistics:")
        print(f"Total unsubscribed emails: {get_unsubscribe_count()}")
        print(f"Unsubscribed emails: {', '.join(get_unsubscribed_list()) if get_unsubscribed_list() else 'None'}")
    else:
        print("❌ Invalid choice")
