import os
import sys
import time
import logging
import subprocess
from datetime import datetime, timedelta
import json

# Add the script directory to path so we can import our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Set up logging for the background service
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(script_dir, 'background_service.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class BackgroundInternshipService:
    def __init__(self):
        self.script_dir = script_dir
        self.running = True
        self.check_interval_hours = 5  # Check every 5 hours
        
    def run_smart_scheduler(self):
        """Run the smart scheduler script"""
        try:
            logging.info("Running smart scheduler check...")
            
            # Change to script directory and run smart_scheduler.py
            result = subprocess.run(
                [sys.executable, 'smart_scheduler.py'], 
                cwd=self.script_dir,
                capture_output=True, 
                text=True, 
                timeout=1800  # 30 minute timeout
            )
            
            if result.returncode == 0:
                logging.info("Smart scheduler completed successfully")
                if result.stdout:
                    print(result.stdout)
            else:
                logging.error(f"Smart scheduler failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logging.error("Smart scheduler timed out after 30 minutes")
        except Exception as e:
            logging.error(f"Error running smart scheduler: {str(e)}")
    
    def run_service(self):
        """Main service loop"""
        logging.info("🚀 Background Internship Service Started")
        logging.info(f"📅 Will check for internships every {self.check_interval_hours} hours")
        logging.info("🛑 Press Ctrl+C to stop the service")
        
        try:
            while self.running:
                current_time = datetime.now()
                logging.info(f"🔍 Starting scheduled check at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Run the smart scheduler
                self.run_smart_scheduler()
                
                # Calculate next run time
                next_run = current_time + timedelta(hours=self.check_interval_hours)
                logging.info(f"⏰ Next check scheduled for {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Sleep for the interval (in seconds)
                sleep_seconds = self.check_interval_hours * 3600
                time.sleep(sleep_seconds)
                
        except KeyboardInterrupt:
            logging.info("🛑 Service stopped by user")
            self.running = False
        except Exception as e:
            logging.error(f"Service error: {str(e)}")
            self.running = False

if __name__ == "__main__":
    print("===============================================")
    print("    INTERNSHIP BOT - BACKGROUND SERVICE")
    print("===============================================")
    print("🤖 Starting automated internship monitoring...")
    print("📧 Will send emails only when new opportunities are found")
    print("⏰ Checks every 5 hours automatically")
    print("🛑 Press Ctrl+C to stop")
    print("===============================================")
    print()
    
    service = BackgroundInternshipService()
    service.run_service()
