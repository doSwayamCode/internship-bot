#!/usr/bin/env python3
"""
InternBot Management Dashboard
A comprehensive tool to manage subscribers, view analytics, and control the bot
"""

import os
import json
from datetime import datetime
from email_tracker import display_stats, export_to_excel, get_email_stats, get_internship_stats
from unsubscribe_manager import (
    get_unsubscribed_list, get_unsubscribe_count, 
    manual_unsubscribe, manual_resubscribe, 
    add_unsubscribe, remove_unsubscribe
)

def show_main_menu():
    """Display the main dashboard menu"""
    print("\n" + "="*60)
    print("🤖 INTERNBOT MANAGEMENT DASHBOARD")
    print("="*60)
    print("1. 📊 View Analytics & Statistics")
    print("2. 👥 Manage Subscribers") 
    print("3. 📧 Email Tracking & Reports")
    print("4. 🔄 Re-subscription Management")
    print("5. 📁 Export Data to Excel")
    print("6. ⚙️  System Status")
    print("7. 🚪 Exit")
    print("="*60)

def show_analytics():
    """Show comprehensive analytics"""
    print("\n📊 INTERNBOT ANALYTICS")
    print("="*50)
    
    # Email statistics
    email_stats = get_email_stats()
    if 'error' not in email_stats:
        print("\n📧 EMAIL STATISTICS:")
        print("-"*30)
        for key, value in email_stats.items():
            if isinstance(value, dict):
                print(f"📈 {key.replace('_', ' ').title()}:")
                for k, v in value.items():
                    print(f"   • {k}: {v}")
            else:
                print(f"📈 {key.replace('_', ' ').title()}: {value}")
    
    # Internship statistics  
    internship_stats = get_internship_stats()
    if 'error' not in internship_stats:
        print("\n🏢 INTERNSHIP STATISTICS:")
        print("-"*30)
        for key, value in internship_stats.items():
            if isinstance(value, dict):
                print(f"📈 {key.replace('_', ' ').title()}:")
                for k, v in list(value.items())[:5]:  # Show top 5
                    print(f"   • {k}: {v}")
            else:
                print(f"📈 {key.replace('_', ' ').title()}: {value}")
    
    # Subscription statistics
    print(f"\n👥 SUBSCRIPTION STATISTICS:")
    print("-"*30)
    print(f"📧 Total Unsubscribed: {get_unsubscribe_count()}")
    
    try:
        from config import SUBSCRIBERS
        total_subscribers = len(SUBSCRIBERS['emails'])
        active_subscribers = total_subscribers - get_unsubscribe_count()
        print(f"📧 Total Configured: {total_subscribers}")
        print(f"📧 Active Subscribers: {active_subscribers}")
        print(f"📧 Unsubscribe Rate: {(get_unsubscribe_count()/total_subscribers*100):.1f}%")
    except:
        print("⚠️ Could not load subscriber config")

def manage_subscribers():
    """Subscriber management menu"""
    while True:
        print("\n👥 SUBSCRIBER MANAGEMENT")
        print("="*40)
        print("1. 📋 List All Unsubscribed Emails")
        print("2. 🚫 Add Unsubscribe")
        print("3. ✅ Remove Unsubscribe (Re-subscribe)")
        print("4. 📊 Subscription Statistics")
        print("5. 🔍 Check Email Status")
        print("6. ⬅️  Back to Main Menu")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            unsubscribed = get_unsubscribed_list()
            if unsubscribed:
                print(f"\n🚫 Unsubscribed Emails ({len(unsubscribed)}):")
                for i, email in enumerate(unsubscribed, 1):
                    print(f"{i}. {email}")
            else:
                print("📭 No unsubscribed emails found")
        
        elif choice == "2":
            manual_unsubscribe()
        
        elif choice == "3":
            manual_resubscribe()
        
        elif choice == "4":
            print(f"\n📊 Subscription Statistics:")
            print(f"Total unsubscribed: {get_unsubscribe_count()}")
            try:
                from config import SUBSCRIBERS
                total = len(SUBSCRIBERS['emails'])
                active = total - get_unsubscribe_count()
                print(f"Total configured: {total}")
                print(f"Active subscribers: {active}")
            except:
                print("Could not load total subscriber count")
        
        elif choice == "5":
            email = input("Enter email to check: ").strip().lower()
            if email:
                from unsubscribe_manager import is_unsubscribed
                if is_unsubscribed(email):
                    print(f"🚫 {email} is UNSUBSCRIBED")
                else:
                    print(f"✅ {email} is ACTIVE")
            
        elif choice == "6":
            break
        
        else:
            print("❌ Invalid choice")

def email_tracking_menu():
    """Email tracking and reports menu"""
    while True:
        print("\n📧 EMAIL TRACKING & REPORTS")
        print("="*40)
        print("1. 📊 Display Current Statistics")
        print("2. 📁 Export Tracking Data to Excel")
        print("3. 📋 View Raw CSV Files")
        print("4. 🗑️  Clear Tracking Data")
        print("5. ⬅️  Back to Main Menu")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            display_stats()
        
        elif choice == "2":
            if export_to_excel():
                print("✅ Data exported successfully!")
            else:
                print("❌ Export failed")
        
        elif choice == "3":
            print("\n📁 Available Tracking Files:")
            files = ['email_tracking.csv', 'internship_data.csv']
            for file in files:
                if os.path.exists(file):
                    size = os.path.getsize(file)
                    print(f"   • {file} ({size} bytes)")
                else:
                    print(f"   • {file} (not found)")
        
        elif choice == "4":
            confirm = input("⚠️ Clear all tracking data? (yes/no): ").strip().lower()
            if confirm == 'yes':
                files = ['email_tracking.csv', 'internship_data.csv']
                for file in files:
                    if os.path.exists(file):
                        os.remove(file)
                        print(f"🗑️ Deleted {file}")
                print("✅ Tracking data cleared")
            else:
                print("❌ Operation cancelled")
        
        elif choice == "5":
            break
        
        else:
            print("❌ Invalid choice")

def resubscription_management():
    """Re-subscription management and tools"""
    print("\n🔄 RE-SUBSCRIPTION MANAGEMENT")
    print("="*40)
    print("1. 📧 Process Email-based Resubscribe Requests")
    print("2. 👤 Manual Re-subscription")
    print("3. 📋 View Re-subscription Instructions")
    print("4. ⬅️  Back to Main Menu")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        try:
            from email_resubscribe_processor import process_resubscribe_emails
            resubscribed = process_resubscribe_emails()
            if resubscribed:
                print(f"✅ Processed {len(resubscribed)} re-subscription requests")
            else:
                print("📭 No re-subscription requests found")
        except ImportError:
            print("❌ Email resubscribe processor not available")
    
    elif choice == "2":
        manual_resubscribe()
    
    elif choice == "3":
        show_resubscription_instructions()
    
    elif choice == "4":
        return
    
    else:
        print("❌ Invalid choice")

def show_resubscription_instructions():
    """Show how users can re-subscribe"""
    print("\n📋 RE-SUBSCRIPTION INSTRUCTIONS FOR USERS")
    print("="*50)
    print("Users can re-subscribe in the following ways:")
    print("\n1. 📧 EMAIL METHOD:")
    print("   • Reply to any previous InternBot email")
    print("   • Or send email to the bot's email address")
    print("   • Include one of these keywords in the email:")
    print("     - RESUBSCRIBE")
    print("     - SUBSCRIBE") 
    print("     - SUBSCRIBE AGAIN")
    print("     - SIGN ME UP")
    print("     - OPT IN")
    print("     - REJOIN")
    print("     - RESUME EMAILS")
    print("     - START EMAILS")
    print("\n2. 🔧 MANUAL METHOD:")
    print("   • Contact administrator")
    print("   • Use this management dashboard")
    print("\n3. 📝 GOOGLE FORM METHOD:")
    print("   • Create a Google Form for re-subscriptions")
    print("   • Process responses manually")

def show_system_status():
    """Show system status and health check"""
    print("\n⚙️  SYSTEM STATUS")
    print("="*40)
    
    # Check required files
    required_files = [
        'config.py', 'scraper.py', 'messenger.py', 
        'storage.py', 'collect.py', 'send_batch_email_only.py',
        'unsubscribe_manager.py', 'email_tracker.py'
    ]
    
    print("📁 CORE FILES:")
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (MISSING)")
    
    # Check data files
    data_files = [
        'seen.json', 'unsubscribed_emails.json',
        'email_tracking.csv', 'internship_data.csv'
    ]
    
    print("\n📊 DATA FILES:")
    for file in data_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size} bytes)")
        else:
            print(f"   📭 {file} (not created yet)")
    
    # Check configuration
    print("\n⚙️  CONFIGURATION:")
    try:
        from config import SMTP_CONFIG, SUBSCRIBERS
        print(f"   ✅ SMTP Config loaded")
        print(f"   ✅ {len(SUBSCRIBERS['emails'])} subscribers configured")
    except Exception as e:
        print(f"   ❌ Config error: {e}")
    
    print(f"\n🕒 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main dashboard loop"""
    print("🚀 Starting InternBot Management Dashboard...")
    
    while True:
        show_main_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            show_analytics()
        
        elif choice == "2":
            manage_subscribers()
        
        elif choice == "3":
            email_tracking_menu()
        
        elif choice == "4":
            resubscription_management()
        
        elif choice == "5":
            if export_to_excel():
                print("✅ Data exported to internbot_tracking_data.xlsx")
            else:
                print("❌ Export failed")
        
        elif choice == "6":
            show_system_status()
        
        elif choice == "7":
            print("👋 Goodbye! Thank you for using InternBot Dashboard.")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
