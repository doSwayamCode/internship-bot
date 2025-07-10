# 🔧 RESUBSCRIBE FEATURE SETUP GUIDE

## 🚨 **Issue Found**: Email Configuration Missing

The resubscribe feature isn't working because your email credentials aren't configured yet. Here's how to fix it:

## ✅ **Step 1: Set Up Gmail App Password**

1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to **Google Account Settings**: https://myaccount.google.com/
3. Navigate to **Security** → **2-Step Verification** → **App passwords**
4. Generate a new app password for "InternBot"
5. **Copy the 16-character password** (like: `abcd efgh ijkl mnop`)

## ✅ **Step 2: Update config.py**

Replace these lines in your `config.py`:

```python
# BEFORE (current):
"user": os.getenv("SMTP_USER", "your-email@gmail.com"),
"pass": os.getenv("SMTP_PASS", "your-app-password-here")

# AFTER (replace with your actual details):
"user": os.getenv("SMTP_USER", "youractual@gmail.com"),
"pass": os.getenv("SMTP_PASS", "your-16-char-app-password")
```

## ✅ **Step 3: Test the Setup**

Run the debugger again:
```bash
python test_resubscribe.py
```

All tests should pass now!

## ✅ **Step 4: Test Resubscribe Manually**

### **Method 1: Using the Dashboard**
```bash
python dashboard.py
# Choose option 4 (Re-subscription Management)
# Then option 2 (Manual Re-subscription)
```

### **Method 2: Using Direct Commands**
```bash
# Add someone to unsubscribe list
python unsubscribe_manager.py

# Then re-subscribe them
python unsubscribe_manager.py
# Choose option 2 (re-subscribe)
```

### **Method 3: Email-based (Real Test)**
1. Send an email from the unsubscribed person's email to your bot's email
2. Include "RESUBSCRIBE" or "SUBSCRIBE" in the message
3. Run: `python email_resubscribe_processor.py`

## 🔍 **How to Troubleshoot**

### **If email connection fails:**
- ✅ Make sure you're using the **App Password**, not your regular Gmail password
- ✅ Check that 2-factor authentication is enabled
- ✅ Try generating a new App Password

### **If keywords aren't detected:**
```bash
# Test keyword detection
python -c "from email_resubscribe_processor import is_resubscribe_request; print(is_resubscribe_request('RESUBSCRIBE'))"
```

### **If resubscribe doesn't work:**
```bash
# Test unsubscribe functions
python -c "from unsubscribe_manager import add_unsubscribe, remove_unsubscribe, is_unsubscribed; email='test@test.com'; add_unsubscribe(email); print('Before:', is_unsubscribed(email)); remove_unsubscribe(email); print('After:', is_unsubscribed(email))"
```

## 📧 **How Users Can Resubscribe**

Once configured, users can resubscribe by:

1. **Email Reply Method**:
   - Reply to any previous InternBot email
   - Include any of these keywords:
     - RESUBSCRIBE
     - SUBSCRIBE
     - SUBSCRIBE AGAIN
     - SIGN ME UP
     - OPT IN
     - REJOIN
     - RESUME EMAILS
     - START EMAILS

2. **New Email Method**:
   - Send new email to your bot's email address
   - Include any of the above keywords

3. **Manual Method**:
   - Contact you directly
   - You can re-subscribe them using the dashboard

## 🤖 **GitHub Actions Integration**

Once configured locally, GitHub Actions will automatically:
- Process resubscribe emails every 5 hours
- Re-subscribe users automatically
- Send confirmation emails

No additional setup needed for GitHub Actions!

## 🎯 **Next Steps**

1. **Fix config.py** with your actual Gmail credentials
2. **Run test_resubscribe.py** to verify everything works
3. **Test manually** with a real email
4. **Enjoy automatic resubscription!** 🚀

---

**Need help?** Run `python test_resubscribe.py` for detailed diagnostics!
