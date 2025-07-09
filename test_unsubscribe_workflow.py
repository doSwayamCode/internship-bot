#!/usr/bin/env python3
"""
Test the complete unsubscribe workflow
"""

from unsubscribe_manager import add_unsubscribe, get_active_emails
from config import SUBSCRIBERS
import json

def test_complete_workflow():
    """Test the complete unsubscribe workflow"""
    print("🧪 Testing Complete Unsubscribe Workflow")
    print("=" * 50)
    
    # Original email list
    original_emails = SUBSCRIBERS['emails'].copy()
    print(f"📧 Original email recipients: {len(original_emails)}")
    for email in original_emails:
        print(f"   • {email}")
    
    # Add a test unsubscribe
    test_email = original_emails[0] if original_emails else "test@example.com"
    print(f"\n🚫 Adding unsubscribe for: {test_email}")
    add_unsubscribe(test_email)
    
    # Test filtering
    print(f"\n🔍 Testing email filtering...")
    
    # Reload config to get filtered emails
    from importlib import reload
    import config
    reload(config)
    
    filtered_emails = config.SUBSCRIBERS['emails']
    print(f"📧 Filtered email recipients: {len(filtered_emails)}")
    for email in filtered_emails:
        print(f"   • {email}")
    
    # Verify the test email was filtered out
    if test_email not in filtered_emails:
        print(f"✅ SUCCESS: {test_email} was filtered out correctly!")
    else:
        print(f"❌ ERROR: {test_email} was NOT filtered out!")
    
    print(f"\n📊 Summary:")
    print(f"   Original count: {len(original_emails)}")
    print(f"   Filtered count: {len(filtered_emails)}")
    print(f"   Difference: {len(original_emails) - len(filtered_emails)}")
    
    # Clean up
    print(f"\n🧹 Cleaning up test data...")
    import os
    if os.path.exists('unsubscribed_emails.json'):
        os.remove('unsubscribed_emails.json')
        print("✅ Test unsubscribe data removed")

if __name__ == "__main__":
    test_complete_workflow()
