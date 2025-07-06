import time
import schedule
import subprocess
import logging
from datetime import datetime, timedelta
import os
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('internship_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class SmartInternshipScheduler:
    def __init__(self):
        self.last_email_sent = None
        self.emails_sent_today = 0
        self.max_emails_per_day = 3
        self.min_hours_between_emails = 4
        self.state_file = 'scheduler_state.json'
        self.load_state()
    
    def load_state(self):
        """Load scheduler state from file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.last_email_sent = datetime.fromisoformat(state.get('last_email_sent', '')) if state.get('last_email_sent') else None
                    self.emails_sent_today = state.get('emails_sent_today', 0)
                    
                    # Reset daily counter if it's a new day
                    if self.last_email_sent and self.last_email_sent.date() != datetime.now().date():
                        self.emails_sent_today = 0
                        logging.info("New day detected - resetting email counter")
            except Exception as e:
                logging.warning(f"Could not load state: {e}")
                self.reset_state()
    
    def save_state(self):
        """Save scheduler state to file"""
        state = {
            'last_email_sent': self.last_email_sent.isoformat() if self.last_email_sent else None,
            'emails_sent_today': self.emails_sent_today
        }
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            logging.warning(f"Could not save state: {e}")
    
    def reset_state(self):
        """Reset state for new day"""
        self.last_email_sent = None
        self.emails_sent_today = 0
    
    def can_send_email(self):
        """Check if we can send an email based on frequency limits"""
        now = datetime.now()
        
        # Check daily limit
        if self.emails_sent_today >= self.max_emails_per_day:
            logging.info(f"Daily email limit reached ({self.max_emails_per_day}). No more emails today.")
            return False
        
        # Check time since last email
        if self.last_email_sent:
            hours_since_last = (now - self.last_email_sent).total_seconds() / 3600
            if hours_since_last < self.min_hours_between_emails:
                logging.info(f"Too soon since last email ({hours_since_last:.1f}h < {self.min_hours_between_emails}h). Waiting...")
                return False
        
        return True

def has_new_internships():
    """Check if there are internships in the batch waiting to be sent"""
    batch_file = 'batch.json'
    if os.path.exists(batch_file):
        try:
            with open(batch_file, 'r') as f:
                batch = json.load(f)
                return len(batch) > 0
        except Exception as e:
            logging.warning(f"Error reading batch file: {e}")
            return False
    return False

def run_collection():
    """Run the collection script with error handling"""
    try:
        logging.info("Starting internship collection from all sources...")
        result = subprocess.run(['python', 'collect.py'], 
                              capture_output=True, text=True, timeout=600, encoding='utf-8')
        
        if result.returncode == 0:
            logging.info("Collection completed successfully")
            print(result.stdout)
            return True
        else:
            logging.error(f"Collection failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error("Collection timed out after 10 minutes")
        return False
    except Exception as e:
        logging.error(f"Collection error: {str(e)}")
        return False

def run_email_send():
    """Run the email-only batch send script with error handling"""
    try:
        logging.info("Starting email batch send...")
        result = subprocess.run(['python', 'send_batch_email_only.py'], 
                              capture_output=True, text=True, timeout=300, encoding='utf-8')
        
        if result.returncode == 0:
            logging.info("Email batch send completed successfully")
            print(result.stdout)
            return True
        else:
            logging.error(f"Email batch send failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error("Email batch send timed out after 5 minutes")
        return False
    except Exception as e:
        logging.error(f"Email batch send error: {str(e)}")
        return False

def smart_check_and_send():
    """Smart function that only sends emails when new internships are found and frequency allows"""
    scheduler = SmartInternshipScheduler()
    
    logging.info("Starting smart internship check...")
    print(f"\n=== SMART INTERNSHIP CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"📊 Emails sent today: {scheduler.emails_sent_today}/{scheduler.max_emails_per_day}")
    
    # Check if we can send an email today
    if not scheduler.can_send_email():
        return False
    
    # Run collection to find new internships
    print(f"\n🔍 Collecting internships... (Check at {datetime.now().strftime('%H:%M:%S')})")
    collection_success = run_collection()
    
    if not collection_success:
        logging.warning("Collection failed. Will try again next scheduled time.")
        return False
    
    # Check if we have new internships
    if has_new_internships():
        logging.info("New internships found! Sending email notifications...")
        print("\n📧 NEW internships found! Sending notifications...")
        
        # Send emails
        email_success = run_email_send()
        
        if email_success:
            # Update scheduler state
            scheduler.last_email_sent = datetime.now()
            scheduler.emails_sent_today += 1
            scheduler.save_state()
            
            logging.info(f"✅ Email sent successfully! ({scheduler.emails_sent_today}/{scheduler.max_emails_per_day} today)")
            print(f"✅ Email sent successfully! ({scheduler.emails_sent_today}/{scheduler.max_emails_per_day} today)")
            return True
        else:
            logging.warning("Email sending failed.")
            return False
    else:
        logging.info("No new internships found. No email sent.")
        print("📭 No new internships found. No email sent (as intended).")
        return False

def github_actions_check_and_send():
    """
    Single execution function for GitHub Actions
    Collects internships and sends emails if new ones found
    """
    logging.info("=== GITHUB ACTIONS - SMART CHECK ===")
    
    try:
        # Run collection
        collection_success = run_collection()
        
        if collection_success and has_new_internships():
            logging.info("✅ New internships found - sending email batch")
            email_success = run_email_send()
            
            if email_success:
                logging.info("🎯 Smart check completed successfully - emails sent")
                return True
            else:
                logging.warning("⚠️ Collection succeeded but email sending failed")
                return False
        else:
            logging.info("ℹ️ No new internships found - no emails sent")
            return True
            
    except Exception as e:
        logging.error(f"❌ Smart check failed: {str(e)}")
        return False

def main():
    """Main scheduler function with smart frequency-based checking"""
    print("\n" + "="*80)
    print("        SMART INTERNSHIP BOT - FREQUENCY-CONTROLLED AUTOMATION")
    print("="*80)
    print("Strategy: Check for new internships 2-3 times per day (every 4-5 hours)")
    print("Email: Only when NEW internships found | No repeats | No spam")
    print("Sources: Internshala, LinkedIn, TimesJobs, AngelList + more")
    print("Daily limit: 3 emails max | Min 4 hours between emails")
    print("Press Ctrl+C to stop")
    print("="*80 + "\n")
    
    logging.info("Starting Smart Internship Bot with Frequency Control")
    
    # Schedule smart checks 3 times per day (every 8 hours, with flexibility)
    schedule.every(5).hours.do(smart_check_and_send)  # Primary schedule: every 5 hours
    schedule.every().day.at("09:00").do(smart_check_and_send)  # Morning check
    schedule.every().day.at("14:00").do(smart_check_and_send)  # Afternoon check  
    schedule.every().day.at("19:00").do(smart_check_and_send)  # Evening check
    
    # Run initial check
    logging.info("Running initial smart check...")
    smart_check_and_send()
    
    # Keep the scheduler running
    logging.info("Smart scheduler running. Next checks: 09:00, 14:00, 19:00 daily + every 5 hours.")
    print("🤖 Smart bot is now running!")
    print("⏰ Next scheduled checks: 09:00, 14:00, 19:00 (+ every 5 hours)")
    print("📧 Will only send emails when NEW internships are found")
    print("🚫 No spam, no repeats, max 3 emails per day\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(600)  # Check every 10 minutes for scheduled tasks
            
    except KeyboardInterrupt:
        print("\nStopping smart internship bot...")
        logging.info("Smart scheduler stopped by user")
    except Exception as e:
        logging.error(f"Scheduler error: {str(e)}")

if __name__ == "__main__":
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
