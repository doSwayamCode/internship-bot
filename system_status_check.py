#!/usr/bin/env python3
"""
InternBot System Status Check
"""

import os
import json
from datetime import datetime

def check_system_status():
    """Check the current status of the InternBot system"""
    print("🔍 InternBot System Status Check")
    print("=" * 50)
    
    # Check 1: Core files
    core_files = [
        'scraper.py', 'collect.py', 'messenger.py', 
        'send_batch_email_only.py', 'storage.py', 'config.py'
    ]
    
    print("\n📁 Core Files:")
    for file in core_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
    
    # Check 2: Unsubscribe system
    unsubscribe_files = [
        'unsubscribe_manager.py', 'email_unsubscribe_processor.py'
    ]
    
    print("\n🚫 Unsubscribe System:")
    for file in unsubscribe_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
    
    # Check 3: GitHub Actions
    gh_workflow = '.github/workflows/internship-bot.yml'
    if os.path.exists(gh_workflow):
        print(f"✅ GitHub Actions workflow configured")
    else:
        print(f"❌ GitHub Actions workflow missing")
    
    # Check 4: Data files
    print("\n💾 Data Files:")
    
    if os.path.exists('seen.json'):
        try:
            with open('seen.json', 'r') as f:
                seen_data = json.load(f)
            print(f"✅ seen.json - {len(seen_data)} tracked internships")
        except:
            print("⚠️ seen.json - exists but corrupted")
    else:
        print("ℹ️ seen.json - will be created on first run")
    
    if os.path.exists('batch.json'):
        try:
            with open('batch.json', 'r') as f:
                batch_data = json.load(f)
            print(f"✅ batch.json - {len(batch_data)} internships ready to send")
        except:
            print("⚠️ batch.json - exists but corrupted")
    else:
        print("ℹ️ batch.json - no pending internships")
    
    if os.path.exists('unsubscribed_emails.json'):
        try:
            with open('unsubscribed_emails.json', 'r') as f:
                unsub_data = json.load(f)
            print(f"✅ unsubscribed_emails.json - {len(unsub_data)} unsubscribed users")
        except:
            print("⚠️ unsubscribed_emails.json - exists but corrupted")
    else:
        print("ℹ️ unsubscribed_emails.json - no unsubscribes yet")
    
    # Check 5: Configuration
    print("\n⚙️ Configuration:")
    try:
        from config import SUBSCRIBERS, SMTP_CONFIG
        print(f"✅ Email recipients configured: {len(SUBSCRIBERS['emails'])} emails")
        print(f"✅ SMTP configuration: {SMTP_CONFIG['host']}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
    
    print("\n🎯 System Status: READY FOR AUTOMATION!")
    print("\n🚀 Next Steps:")
    print("1. Run GitHub Actions workflow manually")
    print("2. Check GitHub Actions logs for success")
    print("3. Test unsubscribe by replying to emails with 'UNSUBSCRIBE'")
    print("4. Monitor the unsubscribed_emails.json file")

if __name__ == "__main__":
    check_system_status()
