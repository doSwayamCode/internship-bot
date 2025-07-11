# 📧 Subscriber Management System

## Overview

Your internship bot now uses a dynamic subscriber management system that makes it easy to add/remove email subscribers without touching GitHub secrets.

## How It Works

### 1. **subscribers.json** (Main Source)

- Located in your project root
- Contains the list of email subscribers
- Easy to edit manually or via the management tool
- Gets committed to your repository

### 2. **Automatic Unsubscribe Filtering**

- The system automatically filters out unsubscribed emails
- Uses `unsubscribe_manager.py` to check against unsubscribed list
- No manual intervention needed

### 3. **Fallback System**

- If `subscribers.json` doesn't exist, falls back to `RECIPIENT_EMAILS` environment variable
- If that doesn't exist, uses hardcoded fallback emails

## Managing Subscribers

### Option 1: Use the Management Tool (Recommended)

```bash
python manage_subscribers.py
```

This gives you an interactive menu to:

- List all subscribers
- Add new subscribers
- Remove subscribers
- Bulk add from file

### Option 2: Edit subscribers.json Manually

```json
{
  "emails": ["user1@example.com", "user2@example.com", "user3@example.com"],
  "last_updated": "2025-01-11",
  "notes": "Add or remove emails from the 'emails' array"
}
```

### Option 3: Bulk Add from File

Create a text file with one email per line:

```
user1@example.com
user2@example.com
user3@example.com
```

Then use option 4 in the management tool.

## GitHub Actions Setup

### ✅ What You Need in GitHub Secrets:

- `SMTP_USER` - Your Gmail address
- `SMTP_PASS` - Your Gmail app password

### ❌ What You DON'T Need Anymore:

- ~~`RECIPIENT_EMAILS`~~ - No longer required!

## Benefits of New System

1. **Easy Updates**: Add/remove subscribers without touching GitHub
2. **Version Control**: Subscriber list is tracked in git
3. **Automatic Filtering**: Unsubscribes are handled automatically
4. **No Secrets Management**: No need to update GitHub secrets for email changes
5. **Tools Provided**: Interactive management tool for easy administration

## Migration Steps

1. ✅ Update your `subscribers.json` with your actual email list
2. ✅ Remove `RECIPIENT_EMAILS` from GitHub secrets (optional)
3. ✅ Test locally: `python send_batch_email_only.py`
4. ✅ Push changes to GitHub

## Testing

Test the new system:

```bash
# Test subscriber loading
python -c "from config import SUBSCRIBERS; print(f'Loaded {len(SUBSCRIBERS[\"emails\"])} subscribers:', SUBSCRIBERS['emails'])"

# Test management tool
python manage_subscribers.py

# Test email sending (if you have internships in batch)
python send_batch_email_only.py
```

Your subscriber management is now much more flexible and easier to maintain! 🎉
