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

def get_active_emails(email_list):
    """Filter out unsubscribed emails from a list"""
    return [email for email in email_list if not is_unsubscribed(email)]

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
    print("2. List unsubscribed emails")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        manual_unsubscribe()
    elif choice == "2":
        list_unsubscribed()
    else:
        print("❌ Invalid choice")
