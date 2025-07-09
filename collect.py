from scraper import scrape_all
from storage import load_seen, save_seen, add_to_batch
from config import SUBSCRIBERS
import re
from datetime import datetime, timedelta

def is_internship_too_old(posted_date):
    """Check if an internship is older than 2 weeks based on posted_date"""
    if not posted_date or posted_date == "Not specified":
        return False  # If no date info, allow it through
    
    posted_date_lower = posted_date.lower()
    
    # Extract number and time unit
    time_pattern = r'(\d+)\s+(day|week|month)s?\s+ago'
    match = re.search(time_pattern, posted_date_lower)
    
    if not match:
        return False  # If can't parse, allow it through
    
    number = int(match.group(1))
    unit = match.group(2)
    
    # Convert to days
    if unit == 'day':
        days_old = number
    elif unit == 'week':
        days_old = number * 7
    elif unit == 'month':
        days_old = number * 30  # Approximate
    else:
        return False  # Unknown unit, allow through
    
    # Filter out if older than 14 days (2 weeks)
    return days_old > 14

def collect_internships():
    """Collect new internships and add them to the batch"""
    seen_ids = load_seen()
    new_count = 0

    internships = scrape_all()
    print(f"📦 Found {len(internships)} internships total.")

    for job in internships:
        if job['id'] in seen_ids:
            continue
        
        # Filter out internships older than 2 weeks
        if is_internship_too_old(job.get('posted_date', '')):
            print(f"⏰ Skipped (too old): {job['title']} at {job['company']} - Posted: {job.get('posted_date', 'Unknown')}")
            continue

        # Add to batch instead of sending immediately
        if add_to_batch(job):
            seen_ids.add(job['id'])
            new_count += 1
            print(f"✅ Added to batch: {job['title']} at {job['company']}")
        else:
            print(f"🔄 Skipped (duplicate in batch): {job['title']} at {job['company']}")

    save_seen(seen_ids)
    print(f"📥 Added {new_count} new internships to batch.")
    print("✅ Collection cycle completed.")

if __name__ == "__main__":
    collect_internships()
