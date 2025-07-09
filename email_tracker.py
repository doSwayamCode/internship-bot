#!/usr/bin/env python3
"""
Email Tracking System for InternBot
Tracks all email sends and internship data in CSV format
"""

import csv
import os
import pandas as pd
from datetime import datetime

EMAIL_TRACKING_FILE = 'email_tracking.csv'
INTERNSHIP_DATA_FILE = 'internship_data.csv'

def init_tracking_files():
    """Initialize CSV files with headers if they don't exist"""
    
    # Email tracking CSV
    if not os.path.exists(EMAIL_TRACKING_FILE):
        with open(EMAIL_TRACKING_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'recipient_email', 'num_internships_sent', 
                'email_subject', 'delivery_status', 'bot_run_id'
            ])
    
    # Internship data CSV
    if not os.path.exists(INTERNSHIP_DATA_FILE):
        with open(INTERNSHIP_DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'title', 'company', 'link', 'source_site',
                'recipients_sent_to', 'bot_run_id'
            ])

def log_email_send(recipient_email, num_internships, email_subject, delivery_status='success', bot_run_id=None):
    """Log an email send event"""
    if bot_run_id is None:
        bot_run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    with open(EMAIL_TRACKING_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            recipient_email,
            num_internships,
            email_subject,
            delivery_status,
            bot_run_id
        ])

def log_internship_data(internships_list, recipients_list, bot_run_id=None):
    """Log internship data that was sent"""
    if bot_run_id is None:
        bot_run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    with open(INTERNSHIP_DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for internship in internships_list:
            writer.writerow([
                datetime.now().isoformat(),
                internship.get('title', 'N/A'),
                internship.get('company', 'N/A'),
                internship.get('link', 'N/A'),
                internship.get('source', 'N/A'),
                len(recipients_list),
                bot_run_id
            ])

def get_email_stats():
    """Get email sending statistics"""
    try:
        df = pd.read_csv(EMAIL_TRACKING_FILE)
        
        stats = {
            'total_emails_sent': len(df),
            'unique_recipients': df['recipient_email'].nunique(),
            'total_internships_shared': df['num_internships_sent'].sum(),
            'success_rate': (df['delivery_status'] == 'success').mean() * 100,
            'last_email_sent': df['timestamp'].max() if len(df) > 0 else 'None',
            'most_active_recipient': df['recipient_email'].value_counts().head(1).to_dict()
        }
        
        return stats
    except FileNotFoundError:
        return {'error': 'No tracking data found'}

def get_internship_stats():
    """Get internship data statistics"""
    try:
        df = pd.read_csv(INTERNSHIP_DATA_FILE)
        
        stats = {
            'total_internships_tracked': len(df),
            'unique_companies': df['company'].nunique(),
            'top_companies': df['company'].value_counts().head(5).to_dict(),
            'internships_by_source': df['source_site'].value_counts().to_dict(),
            'latest_internship': df['timestamp'].max() if len(df) > 0 else 'None'
        }
        
        return stats
    except FileNotFoundError:
        return {'error': 'No internship data found'}

def export_to_excel():
    """Export all tracking data to Excel with multiple sheets"""
    try:
        with pd.ExcelWriter('internbot_tracking_data.xlsx', engine='openpyxl') as writer:
            # Email tracking sheet
            if os.path.exists(EMAIL_TRACKING_FILE):
                email_df = pd.read_csv(EMAIL_TRACKING_FILE)
                email_df.to_excel(writer, sheet_name='Email_Tracking', index=False)
            
            # Internship data sheet
            if os.path.exists(INTERNSHIP_DATA_FILE):
                internship_df = pd.read_csv(INTERNSHIP_DATA_FILE)
                internship_df.to_excel(writer, sheet_name='Internship_Data', index=False)
            
            # Statistics sheet
            email_stats = get_email_stats()
            internship_stats = get_internship_stats()
            
            stats_data = []
            for key, value in email_stats.items():
                stats_data.append(['Email Stats', key, str(value)])
            for key, value in internship_stats.items():
                stats_data.append(['Internship Stats', key, str(value)])
            
            stats_df = pd.DataFrame(stats_data, columns=['Category', 'Metric', 'Value'])
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        
        print("✅ Data exported to internbot_tracking_data.xlsx")
        return True
    except Exception as e:
        print(f"❌ Error exporting to Excel: {e}")
        return False

def display_stats():
    """Display current statistics"""
    print("\n📊 InternBot Email Statistics:")
    print("=" * 40)
    
    email_stats = get_email_stats()
    if 'error' not in email_stats:
        for key, value in email_stats.items():
            print(f"📧 {key.replace('_', ' ').title()}: {value}")
    
    print("\n📊 InternBot Internship Statistics:")
    print("=" * 40)
    
    internship_stats = get_internship_stats()
    if 'error' not in internship_stats:
        for key, value in internship_stats.items():
            if isinstance(value, dict):
                print(f"🏢 {key.replace('_', ' ').title()}:")
                for k, v in value.items():
                    print(f"   • {k}: {v}")
            else:
                print(f"🏢 {key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    init_tracking_files()
    display_stats()
    
    print("\n" + "=" * 50)
    print("📁 Tracking files created:")
    print(f"   • {EMAIL_TRACKING_FILE}")
    print(f"   • {INTERNSHIP_DATA_FILE}")
    print("\n💡 Run 'python email_tracker.py' anytime to see stats")
    print("💡 Excel export available with export_to_excel() function")
