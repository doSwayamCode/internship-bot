# 🤖 Automated Unsubscribe Processing Setup

## 🚀 **Option 1: Google Sheets API + GitHub Actions (Recommended)**

### Step 1: Set up Google Sheets API

1. **Go to Google Cloud Console**: https://console.cloud.google.com
2. **Create a new project** (or use existing)
3. **Enable Google Sheets API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. **Create API Key**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the API key

### Step 2: Get Google Sheet ID

1. **Open your Google Form responses**
2. **Click the Google Sheets icon** to create a linked sheet
3. **Copy the Sheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
   ```

### Step 3: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

- `GOOGLE_SHEETS_API_KEY`: Your API key from Step 1
- `GOOGLE_SHEET_ID`: Your sheet ID from Step 2

### Step 4: Make Sheet Public (Read-Only)

1. **Open your Google Sheet**
2. **Click "Share"**
3. **Change to "Anyone with the link can view"**
4. **Copy the sharing link** (for verification)

### ✅ **How it works:**

- GitHub Actions runs daily at 9 AM UTC
- Checks Google Sheet for new form responses
- Automatically adds unsubscribes to `unsubscribed_emails.json`
- Commits changes back to repository
- Your bot automatically filters out unsubscribed emails

---

## 📧 **Option 2: Email-Based Processing (Simpler)**

### Step 1: Update your email template

Tell users to reply with "UNSUBSCRIBE" in subject line.

### Step 2: Set up automated email checking

Add to your GitHub Actions workflow:

```yaml
- name: Process unsubscribe emails
  env:
    SMTP_USER: ${{ secrets.SMTP_USER }}
    SMTP_PASS: ${{ secrets.SMTP_PASS }}
  run: |
    python email_unsubscribe_processor.py
```

### ✅ **How it works:**

- Users reply to emails with "UNSUBSCRIBE" in subject
- GitHub Actions checks your inbox daily
- Automatically processes unsubscribe requests
- No Google APIs needed

---

## 🔧 **Option 3: Manual Processing (Backup)**

### If automation fails, use manual processing:

```bash
# Download CSV from Google Forms
python process_form_responses.py

# Or manually add emails
python unsubscribe_manager.py
```

---

## 🎯 **Recommended Setup:**

1. **Start with Option 2** (Email-based) - it's simpler
2. **Add Option 1** later if you get many unsubscribes
3. **Keep Option 3** as backup

---

## ✅ **Current Status:**

Your system now has:

- ✅ Unsubscribe links in every email
- ✅ Google Form for easy unsubscribing
- ✅ Automated processing options
- ✅ Manual processing backup
- ✅ GitHub Actions integration

---

## 🚀 **Next Steps:**

1. **Choose your automation method** (Option 1 or 2)
2. **Set up the required secrets** in GitHub
3. **Test the automation** with a test unsubscribe
4. **Monitor the unsubscribe logs**

The automation will run alongside your existing internship bot without any conflicts!
