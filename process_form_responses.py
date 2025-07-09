#!/usr/bin/env python3
"""
Google Form Response Processor for InternBot Unsubscribes
This script helps you process unsubscribe requests from Google Forms
"""

import csv
import json
from datetime import datetime
from unsubscribe_manager import add_unsubscribe, list_unsubscribed

def process_csv_responses(csv_file_path):
    """Process Google Form responses from downloaded CSV file"""
    print(f"📊 Processing Google Form responses from: {csv_file_path}")
    print("=" * 60)
    
    processed_count = 0
    error_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Google Forms typically has columns like:
                # "Timestamp", "Email Address", "Feedback" (if you added feedback field)
                
                # Try different possible column names for email
                email = None
                for col_name in row.keys():
                    if 'email' in col_name.lower() or 'mail' in col_name.lower():
                        email = row[col_name].strip().lower()
                        break
                
                if not email:
                    print("❌ No email column found. Available columns:", list(row.keys()))
                    break
                
                if email and '@' in email:
                    try:
                        # Get feedback if available
                        feedback = ""
                        for col_name in row.keys():
                            if 'feedback' in col_name.lower() or 'reason' in col_name.lower():
                                feedback = row[col_name].strip()
                                break
                        
                        # Add to unsubscribe list
                        if add_unsubscribe(email):
                            processed_count += 1
                            if feedback:
                                print(f"   📝 Feedback: {feedback}")
                        
                    except Exception as e:
                        print(f"❌ Error processing {email}: {e}")
                        error_count += 1
                else:
                    print(f"❌ Invalid email format: {email}")
                    error_count += 1
    
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file_path}")
        print("\n💡 How to get the CSV file:")
        print("1. Go to your Google Form responses")
        print("2. Click the Google Sheets icon")
        print("3. Download the sheet as CSV")
        print("4. Place the CSV file in this directory")
        return
    
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return
    
    print("\n" + "=" * 60)
    print(f"✅ Processing complete!")
    print(f"📧 Processed: {processed_count} unsubscribes")
    print(f"❌ Errors: {error_count}")
    
    if processed_count > 0:
        print(f"\n📋 Current unsubscribed count:")
        list_unsubscribed()

def quick_setup_guide():
    """Show setup guide for Google Forms"""
    print("🚀 Google Form Unsubscribe Setup Guide")
    print("=" * 50)
    print()
    print("✅ Step 1: Google Form Setup (DONE)")
    print("   You've already created your form!")
    print()
    print("📊 Step 2: Process Responses")
    print("   1. Go to your Google Form")
    print("   2. Click 'Responses' tab")
    print("   3. Click the Google Sheets icon (📊)")
    print("   4. This creates a linked spreadsheet")
    print()
    print("📥 Step 3: Download & Process")
    print("   1. Open the Google Sheet")
    print("   2. File → Download → CSV")
    print("   3. Save CSV in this directory")
    print("   4. Run: python process_form_responses.py")
    print("   5. Enter the CSV filename")
    print()
    print("🔄 Step 4: Regular Processing")
    print("   - Download CSV weekly/monthly")
    print("   - Process new unsubscribes")
    print("   - Delete processed CSV file")
    print()
    print("🎯 Alternative: Manual Entry")
    print("   - Run: python unsubscribe_manager.py")
    print("   - Manually enter emails from form responses")

def main():
    """Main function"""
    print("🔧 Google Form Response Processor")
    print("1. Process CSV file from Google Forms")
    print("2. Show setup guide")
    print("3. Manual unsubscribe (single email)")
    print("4. List current unsubscribes")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        csv_file = input("Enter CSV filename (e.g., 'form_responses.csv'): ").strip()
        if csv_file:
            process_csv_responses(csv_file)
        else:
            print("❌ No filename provided")
    
    elif choice == "2":
        quick_setup_guide()
    
    elif choice == "3":
        from unsubscribe_manager import manual_unsubscribe
        manual_unsubscribe()
    
    elif choice == "4":
        list_unsubscribed()
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
