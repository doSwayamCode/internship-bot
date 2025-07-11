#!/usr/bin/env python3
"""
Subscriber Management Tool
Easy way to add/remove email subscribers without editing JSON manually
"""

import json
import os
from datetime import datetime

SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    """Load current subscribers"""
    if not os.path.exists(SUBSCRIBERS_FILE):
        return {"emails": [], "last_updated": "", "notes": ""}
    
    with open(SUBSCRIBERS_FILE, "r") as f:
        return json.load(f)

def save_subscribers(data):
    """Save subscribers to file"""
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved to {SUBSCRIBERS_FILE}")

def add_subscriber(email):
    """Add a new subscriber"""
    data = load_subscribers()
    
    if email in data["emails"]:
        print(f"⚠️ {email} is already subscribed!")
        return False
    
    data["emails"].append(email)
    save_subscribers(data)
    print(f"✅ Added {email} to subscribers")
    return True

def remove_subscriber(email):
    """Remove a subscriber"""
    data = load_subscribers()
    
    if email not in data["emails"]:
        print(f"⚠️ {email} is not in subscriber list!")
        return False
    
    data["emails"].remove(email)
    save_subscribers(data)
    print(f"✅ Removed {email} from subscribers")
    return True

def list_subscribers():
    """List all current subscribers"""
    data = load_subscribers()
    emails = data["emails"]
    
    if not emails:
        print("📭 No subscribers found")
        return
    
    print(f"📧 Current Subscribers ({len(emails)}):")
    for i, email in enumerate(emails, 1):
        print(f"  {i}. {email}")
    
    print(f"\nLast updated: {data.get('last_updated', 'Unknown')}")

def main():
    """Main interactive menu"""
    while True:
        print("\n" + "="*50)
        print("📧 SUBSCRIBER MANAGEMENT TOOL")
        print("="*50)
        print("1. List all subscribers")
        print("2. Add new subscriber")
        print("3. Remove subscriber")
        print("4. Bulk add from file")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            list_subscribers()
            
        elif choice == "2":
            email = input("Enter email to add: ").strip()
            if email:
                add_subscriber(email)
            else:
                print("⚠️ Please enter a valid email")
                
        elif choice == "3":
            list_subscribers()
            email = input("Enter email to remove: ").strip()
            if email:
                remove_subscriber(email)
            else:
                print("⚠️ Please enter a valid email")
                
        elif choice == "4":
            filename = input("Enter filename with emails (one per line): ").strip()
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    emails = [line.strip() for line in f if line.strip()]
                
                data = load_subscribers()
                added = 0
                for email in emails:
                    if email not in data["emails"]:
                        data["emails"].append(email)
                        added += 1
                        print(f"  ✅ Added: {email}")
                    else:
                        print(f"  ⚠️ Already exists: {email}")
                
                if added > 0:
                    save_subscribers(data)
                    print(f"\n✅ Added {added} new subscribers")
                else:
                    print("\n📭 No new subscribers added")
            else:
                print(f"⚠️ File {filename} not found")
                
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
