#!/usr/bin/env python3
"""
Automated Unsubscribe Processor for GitHub Actions
This script automatically processes Google Form responses and updates the unsubscribe list
"""

import os
import json
import requests
from datetime import datetime
from unsubscribe_manager import add_unsubscribe, load_unsubscribed

def get_google_sheets_data():
    """Fetch data from Google Sheets using API"""
    api_key = os.getenv('GOOGLE_SHEETS_API_KEY')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    if not api_key or not sheet_id:
        print("❌ Missing Google Sheets API credentials")
        print("Please set GOOGLE_SHEETS_API_KEY and GOOGLE_SHEET_ID in GitHub secrets")
        return None
    
    # Google Sheets API URL
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Sheet1?key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'values' not in data:
            print("📭 No data found in Google Sheet")
            return None
        
        return data['values']
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Google Sheets data: {e}")
        return None

def process_sheet_responses():
    """Process responses from Google Sheets"""
    print("🔄 Fetching latest Google Form responses...")
    
    rows = get_google_sheets_data()
    if not rows:
        return
    
    # First row is usually headers
    if len(rows) < 2:
        print("📭 No responses found")
        return
    
    headers = rows[0]
    data_rows = rows[1:]
    
    # Find email column index
    email_col_index = None
    for i, header in enumerate(headers):
        if 'email' in header.lower() or 'mail' in header.lower():
            email_col_index = i
            break
    
    if email_col_index is None:
        print("❌ No email column found in the sheet")
        print(f"Available columns: {headers}")
        return
    
    # Load existing unsubscribes to avoid duplicates
    existing_unsubscribes = load_unsubscribed()
    existing_emails = [item['email'] if isinstance(item, dict) else item for item in existing_unsubscribes]
    
    new_unsubscribes = 0
    
    print(f"📊 Processing {len(data_rows)} form responses...")
    
    for row in data_rows:
        if len(row) > email_col_index:
            email = row[email_col_index].strip().lower()
            
            if email and '@' in email and email not in existing_emails:
                try:
                    # Add to unsubscribe list
                    if add_unsubscribe(email):
                        new_unsubscribes += 1
                        existing_emails.append(email)  # Avoid duplicates in this run
                        
                        # Log feedback if available (usually in column after email)
                        if len(row) > email_col_index + 1:
                            feedback = row[email_col_index + 1].strip()
                            if feedback:
                                print(f"   📝 Feedback from {email}: {feedback}")
                
                except Exception as e:
                    print(f"❌ Error processing {email}: {e}")
    
    print(f"✅ Processed {new_unsubscribes} new unsubscribes")
    
    if new_unsubscribes > 0:
        print("📧 Updated unsubscribe list will be committed to repository")
    else:
        print("ℹ️ No new unsubscribes to process")

def create_status_report():
    """Create a status report"""
    unsubscribed = load_unsubscribed()
    
    report = {
        "last_processed": datetime.now().isoformat(),
        "total_unsubscribes": len(unsubscribed),
        "status": "success"
    }
    
    with open('unsubscribe_status.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📊 Status: {len(unsubscribed)} total unsubscribes")

if __name__ == "__main__":
    print("🤖 Automated Unsubscribe Processor")
    print("=" * 50)
    
    try:
        process_sheet_responses()
        create_status_report()
        print("✅ Automation completed successfully")
    
    except Exception as e:
        print(f"❌ Automation failed: {e}")
        
        # Create error report
        error_report = {
            "last_processed": datetime.now().isoformat(),
            "status": "error",
            "error_message": str(e)
        }
        
        with open('unsubscribe_status.json', 'w') as f:
            json.dump(error_report, f, indent=2)
        
        exit(1)
