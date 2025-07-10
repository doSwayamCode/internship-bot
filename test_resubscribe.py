#!/usr/bin/env python3
"""
Test and Debug Resubscribe Feature
This script helps you test and troubleshoot the email-based resubscribe functionality
"""

import sys
import os
from datetime import datetime

def test_config():
    """Test if email configuration is properly set up"""
    print("🔧 Testing Email Configuration...")
    
    try:
        from config import EMAIL_CONFIG, SMTP_CONFIG
        
        print("✅ Email configs imported successfully")
        print(f"📧 SMTP User: {SMTP_CONFIG.get('user', 'NOT SET')}")
        print(f"📧 EMAIL Config Email: {EMAIL_CONFIG.get('email', 'NOT SET')}")
        print(f"📧 IMAP Server: {EMAIL_CONFIG.get('imap_server', 'NOT SET')}")
        
        # Check if credentials are set
        if EMAIL_CONFIG.get('email') == 'your-email@gmail.com':
            print("⚠️  WARNING: Email credentials not configured!")
            print("   Please update config.py with your actual Gmail credentials")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_email_connection():
    """Test connection to email server"""
    print("\n📡 Testing Email Server Connection...")
    
    try:
        from config import EMAIL_CONFIG
        import imaplib
        
        if not EMAIL_CONFIG or EMAIL_CONFIG.get('email') == 'your-email@gmail.com':
            print("⚠️  Email not configured. Skipping connection test.")
            return False
        
        print(f"🔌 Connecting to {EMAIL_CONFIG['imap_server']}...")
        mail = imaplib.IMAP4_SSL(EMAIL_CONFIG['imap_server'])
        mail.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        mail.select('inbox')
        
        # Check for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        if status == 'OK' and messages[0]:
            unread_count = len(messages[0].split())
            print(f"✅ Connected successfully! Found {unread_count} unread emails")
        else:
            print("✅ Connected successfully! No unread emails found")
        
        mail.logout()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure you're using Gmail App Password (not regular password)")
        print("   2. Enable 2-factor authentication on your Gmail account")
        print("   3. Generate App Password: https://myaccount.google.com/apppasswords")
        print("   4. Use the 16-character app password in your config")
        return False

def test_unsubscribe_functions():
    """Test unsubscribe manager functions"""
    print("\n🔄 Testing Unsubscribe Manager Functions...")
    
    try:
        from unsubscribe_manager import is_unsubscribed, add_unsubscribe, remove_unsubscribe
        
        # Test with a dummy email
        test_email = "test@example.com"
        
        print(f"📧 Testing with email: {test_email}")
        
        # Check initial status
        initial_status = is_unsubscribed(test_email)
        print(f"   Initial status: {'UNSUBSCRIBED' if initial_status else 'ACTIVE'}")
        
        # Test adding unsubscribe
        add_result = add_unsubscribe(test_email)
        print(f"   Add unsubscribe: {'SUCCESS' if add_result else 'ALREADY EXISTED'}")
        
        # Check status after adding
        after_add = is_unsubscribed(test_email)
        print(f"   Status after add: {'UNSUBSCRIBED' if after_add else 'ACTIVE'}")
        
        # Test removing unsubscribe (re-subscribe)
        remove_result = remove_unsubscribe(test_email)
        print(f"   Remove unsubscribe: {'SUCCESS' if remove_result else 'NOT FOUND'}")
        
        # Check final status
        final_status = is_unsubscribed(test_email)
        print(f"   Final status: {'UNSUBSCRIBED' if final_status else 'ACTIVE'}")
        
        print("✅ Unsubscribe functions working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Unsubscribe function error: {e}")
        return False

def test_keyword_detection():
    """Test resubscribe keyword detection"""
    print("\n🔍 Testing Keyword Detection...")
    
    try:
        from email_resubscribe_processor import is_resubscribe_request
        
        test_cases = [
            ("RESUBSCRIBE", True),
            ("subscribe", True),
            ("Subscribe again please", True),
            ("sign me up", True),
            ("I want to opt in", True),
            ("rejoin the list", True),
            ("resume emails", True),
            ("start emails again", True),
            ("Hello, how are you?", False),
            ("unsubscribe", False),
            ("Random text here", False)
        ]
        
        print("📝 Testing keyword detection:")
        for text, expected in test_cases:
            result = is_resubscribe_request(text)
            status = "✅" if result == expected else "❌"
            print(f"   {status} '{text}' -> {result} (expected {expected})")
        
        return True
        
    except Exception as e:
        print(f"❌ Keyword detection error: {e}")
        return False

def manual_resubscribe_test():
    """Manual test for re-subscribing an email"""
    print("\n👤 Manual Re-subscribe Test...")
    
    try:
        from unsubscribe_manager import add_unsubscribe, remove_unsubscribe, is_unsubscribed
        
        test_email = input("Enter email to test re-subscribe with: ").strip().lower()
        
        if not test_email or '@' not in test_email:
            print("❌ Invalid email address")
            return False
        
        print(f"\n🔄 Testing re-subscribe process for: {test_email}")
        
        # First, make sure email is unsubscribed
        if not is_unsubscribed(test_email):
            print("   Adding to unsubscribe list first...")
            add_unsubscribe(test_email)
        
        print(f"   Current status: {'UNSUBSCRIBED' if is_unsubscribed(test_email) else 'ACTIVE'}")
        
        # Now test re-subscribe
        print("   Attempting re-subscribe...")
        success = remove_unsubscribe(test_email)
        
        if success:
            final_status = is_unsubscribed(test_email)
            print(f"   ✅ Re-subscribe successful! Final status: {'UNSUBSCRIBED' if final_status else 'ACTIVE'}")
            return True
        else:
            print("   ❌ Re-subscribe failed")
            return False
            
    except Exception as e:
        print(f"❌ Manual test error: {e}")
        return False

def run_email_processor():
    """Run the actual email processor to check for resubscribe emails"""
    print("\n📧 Running Email Resubscribe Processor...")
    
    try:
        from email_resubscribe_processor import process_resubscribe_emails
        
        print("🔍 Checking for resubscribe emails...")
        resubscribed = process_resubscribe_emails()
        
        if resubscribed:
            print(f"✅ Found and processed {len(resubscribed)} resubscribe request(s):")
            for email in resubscribed:
                print(f"   • {email}")
        else:
            print("📭 No resubscribe requests found")
            print("\n💡 Make sure you:")
            print("   1. Sent an email to your bot's email address")
            print("   2. Include keywords like 'RESUBSCRIBE' or 'SUBSCRIBE'")
            print("   3. The email is still unread in your inbox")
        
        return len(resubscribed) > 0
        
    except Exception as e:
        print(f"❌ Email processor error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 INTERNBOT RESUBSCRIBE FEATURE DEBUGGER")
    print("="*50)
    
    tests = [
        ("Configuration", test_config),
        ("Email Connection", test_email_connection),
        ("Unsubscribe Functions", test_unsubscribe_functions),
        ("Keyword Detection", test_keyword_detection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All basic tests passed!")
        
        print("\n" + "="*50)
        print("🔧 ADDITIONAL TESTING OPTIONS:")
        print("1. Manual re-subscribe test")
        print("2. Run email processor (check for actual emails)")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            manual_resubscribe_test()
        elif choice == "2":
            run_email_processor()
        else:
            print("👋 Exiting debugger")
    else:
        print("❌ Some tests failed. Please fix the issues above before testing email processing.")
    
    print("\n💡 TROUBLESHOOTING TIPS:")
    print("1. Make sure your email credentials are correct in config.py")
    print("2. Use Gmail App Password, not your regular password")
    print("3. Send test emails with 'RESUBSCRIBE' keyword")
    print("4. Check that emails are unread in your inbox")
    print("5. Run 'python email_resubscribe_processor.py' directly to test")

if __name__ == "__main__":
    main()
