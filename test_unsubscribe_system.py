#!/usr/bin/env python3
"""
Complete workflow test for unsubscribe system
"""

from unsubscribe_manager import add_unsubscribe, is_unsubscribed, get_active_emails
from config import SUBSCRIBERS
import json

def test_complete_workflow():
    """Test the complete unsubscribe workflow"""
    print("🧪 Testing Complete Unsubscribe Workflow")
    print("=" * 50)
    
    # Test 1: Add unsubscribe
    print("\n1. Testing add unsubscribe...")
    test_email = "test-user@example.com"
    result = add_unsubscribe(test_email)
    print(f"Add unsubscribe result: {result}")
    
    # Test 2: Check if unsubscribed
    print("\n2. Testing unsubscribe check...")
    is_unsub = is_unsubscribed(test_email)
    print(f"Is {test_email} unsubscribed? {is_unsub}")
    
    # Test 3: Test email filtering
    print("\n3. Testing email filtering...")
    test_email_list = ["user1@example.com", test_email, "user2@example.com"]
    active_emails = get_active_emails(test_email_list)
    print(f"Original list: {test_email_list}")
    print(f"Filtered list: {active_emails}")
    
    # Test 4: Test config integration
    print("\n4. Testing config integration...")
    try:
        current_subscribers = SUBSCRIBERS['emails']
        print(f"Current active subscribers: {len(current_subscribers)} emails")
        print(f"Sample: {current_subscribers[:2] if current_subscribers else 'None'}")
    except Exception as e:
        print(f"Config integration error: {e}")
    
    # Test 5: Test JSON file creation
    print("\n5. Testing JSON file...")
    try:
        with open('unsubscribed_emails.json', 'r') as f:
            data = json.load(f)
            print(f"Unsubscribed emails file contains: {len(data)} entries")
            if data:
                print(f"Sample entry: {data[0]}")
    except FileNotFoundError:
        print("No unsubscribed emails file found")
    except Exception as e:
        print(f"JSON file error: {e}")
    
    print("\n✅ Workflow test completed!")
    print("\n🚀 Next steps:")
    print("1. Go to GitHub → Your Repository → Actions")
    print("2. Click 'Run workflow' on 'Automated Internship Bot'")
    print("3. Watch the logs for unsubscribe processing")
    print("4. Test by replying to an email with 'UNSUBSCRIBE'")

if __name__ == "__main__":
    test_complete_workflow()
