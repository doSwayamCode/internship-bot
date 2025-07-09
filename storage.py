import json
import os
from datetime import datetime

FILE = 'seen.json'
BATCH_FILE = 'batch.json'

def load_seen():
    return set(json.load(open(FILE))) if os.path.exists(FILE) else set()

def save_seen(seen):
    with open(FILE,'w') as f:
        json.dump(list(seen), f)

def load_batch():
    """Load the current batch of internships waiting to be sent"""
    if os.path.exists(BATCH_FILE):
        with open(BATCH_FILE, 'r') as f:
            return json.load(f)
    return []

def save_batch(batch_data):
    """Save the current batch of internships"""
    with open(BATCH_FILE, 'w') as f:
        json.dump(batch_data, f, indent=2)

def add_to_batch(internship):
    """Add a new internship to the current batch (with duplicate checking)"""
    batch = load_batch()
    
    # Check for duplicates in current batch
    for existing in batch:
        if (existing.get('id') == internship.get('id') or 
            (existing.get('title') == internship.get('title') and 
             existing.get('company') == internship.get('company'))):
            # Duplicate found, don't add
            return False
    
    # Add timestamp to track when it was added
    internship['added_at'] = datetime.now().isoformat()
    batch.append(internship)
    save_batch(batch)
    return True

def clear_batch():
    """Clear the batch after sending"""
    if os.path.exists(BATCH_FILE):
        os.remove(BATCH_FILE)
