# 🚀 GitHub Actions Deployment Guide

## ✨ **What You Get**

- 🤖 **Fully Automated**: Runs every 5 hours in the cloud
- 🆓 **Completely Free**: Uses GitHub's free Actions minutes
- 📧 **Smart Email Control**: Only sends when new internships found
- 🔒 **Secure**: Email credentials stored as encrypted secrets
- 🌍 **Global**: Runs 24/7 from GitHub's servers

---

## 📋 **Step-by-Step Setup**

### **Step 1: Create GitHub Repository**

1. Go to [GitHub.com](https://github.com) and sign in
2. Click **"New Repository"**
3. Name it: `internship-bot` (or any name you prefer)
4. Set to **Public** (for free Actions) or **Private** (if you have GitHub Pro)
5. Click **"Create repository"**

### **Step 2: Upload Your Code**

**Option A: Using GitHub Web Interface**

1. Click **"uploading an existing file"**
2. Drag and drop ALL files from your `internship-mcp-main` folder
3. Write commit message: "Initial bot setup"
4. Click **"Commit changes"**

**Option B: Using Git Commands**

```bash
git init
git add .
git commit -m "Initial bot setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/internship-bot.git
git push -u origin main
```

### **Step 3: Set Up GitHub Secrets** 🔐

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **"New repository secret"** for each:

#### **Required Secrets:**

| Secret Name        | Value                      | Example                                              |
| ------------------ | -------------------------- | ---------------------------------------------------- |
| `SMTP_USER`        | Your Gmail address         | `swayamgupta999@gmail.com`                           |
| `SMTP_PASS`        | Your Gmail App Password    | `bfoy dyjv sjvl bhrx`                                |
| `RECIPIENT_EMAILS` | Comma-separated email list | `email1@gmail.com,email2@gmail.com,email3@gmail.com` |

#### **🔑 Gmail App Password Setup:**

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification (enable if not already)
3. App passwords → Generate new app password
4. Use this 16-character password as `SMTP_PASS`

### **Step 4: Enable GitHub Actions**

1. Go to **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. You should see "Automated Internship Bot" workflow

### **Step 5: Test the Deployment** 🧪

1. Go to **Actions** tab
2. Click **"Automated Internship Bot"**
3. Click **"Run workflow"** → **"Run workflow"** (manual trigger)
4. Watch the workflow run - should complete in 2-5 minutes

---

## 📅 **Automatic Schedule**

Your bot will now run automatically:

- **Every 5 hours**: 00:00, 05:00, 10:00, 15:00, 20:00 UTC
- **Time Zones**:
  - UTC 00:00 = IST 05:30 AM
  - UTC 05:00 = IST 10:30 AM
  - UTC 10:00 = IST 03:30 PM
  - UTC 15:00 = IST 08:30 PM
  - UTC 20:00 = IST 01:30 AM

---

## 🔧 **Managing Your Bot**

### **View Activity:**

- Go to **Actions** tab to see all runs
- Click any workflow run to see logs and details

### **Modify Schedule:**

- Edit `.github/workflows/internship-bot.yml`
- Change the `cron:` value
- Examples:
  - Every 3 hours: `"0 */3 * * *"`
  - Twice daily: `"0 9,21 * * *"` (9 AM & 9 PM UTC)
  - Daily at 9 AM UTC: `"0 9 * * *"`

### **Update Recipients:**

- Go to Settings → Secrets → Actions
- Edit `RECIPIENT_EMAILS` secret
- Format: `email1@gmail.com,email2@gmail.com,email3@gmail.com`

### **Pause/Resume:**

- Go to Actions tab
- Click on "Automated Internship Bot"
- Click "Disable workflow" to pause
- Click "Enable workflow" to resume

---

## 🎯 **Benefits of GitHub Actions**

✅ **Free**: 2000 minutes/month for free accounts
✅ **Reliable**: GitHub's infrastructure, 99.9% uptime
✅ **Secure**: Encrypted secrets, isolated environments  
✅ **Maintenance-free**: No server management needed
✅ **Scalable**: Automatic resource allocation
✅ **Logs**: Complete activity tracking and debugging

---

## 🚨 **Troubleshooting**

### **Common Issues:**

**1. Workflow doesn't run:**

- Check if repository is public (private needs GitHub Pro for free Actions)
- Verify `.github/workflows/internship-bot.yml` file exists

**2. Email sending fails:**

- Verify Gmail App Password is correct
- Check if 2-Factor Authentication is enabled on Gmail
- Ensure secrets are named exactly: `SMTP_USER`, `SMTP_PASS`, `RECIPIENT_EMAILS`

**3. No internships found:**

- Check workflow logs for scraping errors
- Verify websites are accessible (some may block GitHub IPs)

**4. Quota exceeded:**

- Free accounts get 2000 Action minutes/month
- Each run takes ~3-5 minutes
- 5-hour schedule = ~144 runs/month = ~720 minutes (well within limit)

---

## 📊 **Monitoring Your Bot**

Your bot automatically:

- ✅ Logs all activity to workflow runs
- ✅ Shows success/failure status
- ✅ Tracks emails sent vs skipped
- ✅ Filters old internships (>2 weeks)
- ✅ Prevents duplicate notifications
- ✅ Respects daily email limits

**View logs:** Actions tab → Click any workflow run → Expand steps

---

## 🎉 **You're All Set!**

Your internship bot is now:

- 🤖 Running automatically in the cloud
- 📧 Sending smart email notifications
- 🔄 Checking for fresh opportunities every 5 hours
- 🆓 Completely free and maintenance-free

**No more manual terminal commands needed!** 🎯
