# 🚫 Unsubscribe System Setup Guide

## Quick Setup Options

### Option 1: Google Form (Recommended - Easiest)

1. **Create a Google Form:**

   - Go to [Google Forms](https://forms.google.com)
   - Create a new form titled "InternBot Unsubscribe"
   - Add one question: "Email Address" (short answer, required)
   - Add description: "Enter your email address to unsubscribe from InternBot alerts"

2. **Get the form link:**

   - Click "Send" → "Link" → Copy the link
   - Replace `YOUR_GOOGLE_FORM_ID` in config.py with this link

3. **Handle responses:**
   - Check form responses regularly
   - Use `python unsubscribe_manager.py` to manually add emails to unsubscribe list

### Option 2: Email-Based Unsubscribe

Users can reply to any email with "UNSUBSCRIBE" in the subject line. You can:

1. Check your email regularly for unsubscribe requests
2. Run `python unsubscribe_manager.py` to add them to the unsubscribe list

### Option 3: Simple Website (Advanced)

Create a simple webpage with an unsubscribe form that calls your unsubscribe system.

## How It Works

1. **Email Template**: Includes unsubscribe link in every email
2. **Unsubscribe Manager**: Tracks unsubscribed emails in `unsubscribed_emails.json`
3. **Automatic Filtering**: Config automatically filters out unsubscribed emails
4. **Manual Management**: Use the unsubscribe_manager.py script

## Usage

### Add an unsubscribe:

```bash
python unsubscribe_manager.py
# Choose option 1, enter email address
```

### List unsubscribed emails:

```bash
python unsubscribe_manager.py
# Choose option 2
```

### Check if email is unsubscribed:

```python
from unsubscribe_manager import is_unsubscribed
if is_unsubscribed("user@example.com"):
    print("User is unsubscribed")
```

## Files Created

- `unsubscribe_manager.py` - Unsubscribe management system
- `unsubscribed_emails.json` - List of unsubscribed emails (auto-created)
- `UNSUBSCRIBE_SETUP.md` - This guide

## GitHub Actions Compatibility

✅ This system works with GitHub Actions
✅ Unsubscribed emails are automatically filtered out
✅ No changes needed to your automation workflow

The unsubscribe system is completely optional and doesn't break anything if not used.
