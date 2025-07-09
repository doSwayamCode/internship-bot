from storage import load_batch, clear_batch
from messenger import send_batch_email
from config import BATCH_MESSAGE_TEMPLATE, SMTP_CONFIG, SUBSCRIBERS
from email_tracker import log_internship_data
from datetime import datetime

def send_batch_email_only():
    """Send batch via email only with enhanced formatting"""
    batch = load_batch()
    
    if not batch:
        print("📭 No new internships in batch to send.")
        return False  # Return False when no email sent
    
    print(f"📮 Preparing to send {len(batch)} internships via email...")
    
    # Get email recipients from config
    email_recipients = SUBSCRIBERS['emails']
    
    # Use SMTP config directly
    smtp_config = SMTP_CONFIG
    
    # Generate bot run ID for tracking
    bot_run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Enhanced formatting for better readability
    formatted_internships = ""
    
    # Group by source for better organization
    sources = {}
    for job in batch:
        source = job.get('source', 'Unknown') 
        if source not in sources:
            sources[source] = []
        sources[source].append(job)
    
    NOT_SPECIFIED = 'Not specified'
    counter = 1
    for source, jobs in sources.items():
        formatted_internships += f"\n📍 **{source.upper()}:**\n"
        for job in jobs:
            formatted_internships += f"{counter}. **{job['title']}** at {job['company']}\n"
            
            # Add date information if available
            posted_date = job.get('posted_date', NOT_SPECIFIED)
            deadline = job.get('deadline', NOT_SPECIFIED)
            
            if posted_date != NOT_SPECIFIED or deadline != NOT_SPECIFIED:
                formatted_internships += f"   📅 Posted: {posted_date}"
                if deadline != NOT_SPECIFIED:
                    formatted_internships += f" | ⏰ Deadline: {deadline}"
                formatted_internships += "\n"
            
            formatted_internships += f"   🔗 Apply here: {job['link']}\n\n"
            counter += 1
    
    # Create the final message using the template with total count
    final_message = BATCH_MESSAGE_TEMPLATE.format(
        internships_list=formatted_internships,
        total_count=len(batch)
    )
    
    # Log internship data for tracking
    log_internship_data(batch, email_recipients, bot_run_id)
    
    # Send email batch messages
    success_count = 0
    for email in email_recipients:
        email = email.strip()
        if email:
            try:
                send_batch_email(
                    email, 
                    batch, 
                    final_message,  # Use the formatted message directly
                    smtp_config,
                    bot_run_id
                )
                success_count += 1
            except Exception as e:
                print(f"❌ Failed to send to {email}: {e}")
    
    # Clear the batch after sending
    clear_batch()
    print(f"✅ Successfully sent to {success_count} recipients. Batch cleared.")
    return True

if __name__ == "__main__":
    send_batch_email_only()
