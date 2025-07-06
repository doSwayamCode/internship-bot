# 🎯 SMART INTERNSHIP BOT - COMPLETE SETUP GUIDE

## ✨ What You Get

### 🔥 **Intelligent Features:**

- **No Repetition**: Only sends NEW internships, never duplicates
- **Smart Waiting**: Keeps searching until fresh opportunities are found
- **Multi-Source**: Scrapes Internshala, Naukri, Glassdoor, Unstop
- **Perfect Filtering**: Only your specified roles (Software, AI/ML, Data, UI/UX, Business Dev, ESG, etc.)
- **Email Only**: Clean, professional email notifications
- **100% FREE**: No paid services required

### 📊 **Targeted Roles:**

✅ Software Engineering & Development
✅ AI/ML & Data Science/Analytics  
✅ UI/UX Design
✅ Business Development
✅ ESG & Environmental Engineering
✅ Non-tech specialized roles (CCaSS, Compliance, etc.)

---

## 🚀 QUICK START (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Email (Edit config.py)

```python
SMTP_CONFIG = {
    "user": "your-email@gmail.com",     # Your Gmail
    "pass": "your-app-password"         # Gmail App Password
}

SUBSCRIBERS = {
    "emails": ["recipient1@gmail.com", "recipient2@gmail.com"]  # Who gets notifications
}
```

### Step 3: Start the Bot

**Double-click:** `start_smart_bot.bat`

**Or run in terminal:**

```bash
python smart_scheduler.py
```

---

## 🧠 HOW IT WORKS

### Smart Cycle Logic:

1. **Searches** all 4 platforms for relevant internships
2. **Filters** using comprehensive keyword matching
3. **Checks** if any are genuinely NEW (not sent before)
4. **Waits** if no new internships found (checks every hour)
5. **Sends** beautiful email when new opportunities discovered
6. **Repeats** cycle every 4 hours

### No Spam Guarantee:

- Only sends when NEW internships are found
- Maximum 12-hour search per cycle
- No duplicate notifications ever
- Quality over quantity approach

---

## 📧 EMAIL PREVIEW

**Subject:** 🎯 New Internship Alert - X Fresh Opportunities!

```
🎯 Fresh Internship Opportunities Alert! 🎯

Hello there,

I hope this email finds you well! Here are the latest handpicked
internship opportunities that perfectly match your interests...

📍 INTERNSHALA:
1. Software Developer Intern at TechCorp
   🔗 Apply here: https://internshala.com/...

2. Data Scientist at AI Startup
   🔗 Apply here: https://internshala.com/...

📍 NAUKRI:
3. UI/UX Designer at DesignCo
   🔗 Apply here: https://naukri.com/...

💡 Why these opportunities?
These internships have been carefully filtered from multiple
platforms to ensure they align with your career goals...

🚀 Application Tips:
- Apply as soon as possible...
- Customize your resume...

Best of luck with your applications! 🌟
```

---

## ⚙️ CONFIGURATION OPTIONS

### Add More Email Recipients:

Edit `config.py`:

```python
SUBSCRIBERS = {
    "emails": [
        "person1@gmail.com",
        "person2@gmail.com",
        "person3@gmail.com"
    ]
}
```

### Modify Keywords:

Edit `scraper.py` - `TECH_KEYWORDS` list to add/remove terms

### Change Timing:

Edit `smart_scheduler.py`:

```python
# Current: Every 4 hours
schedule.every(4).hours.do(intelligent_cycle)

# Options:
schedule.every(6).hours.do(intelligent_cycle)  # Every 6 hours
schedule.every().day.at("09:00").do(intelligent_cycle)  # Daily at 9 AM
```

---

## 🛠️ TROUBLESHOOTING

### "No emails received?"

1. Check Gmail app password is correct
2. Verify email addresses in config.py
3. Check spam/junk folder
4. Look at console output for errors

### "Not finding internships?"

1. Check internet connection
2. Some sites may temporarily block requests
3. Keywords might be too restrictive
4. Check log file: `internship_bot.log`

### "Want to stop the bot?"

- Press `Ctrl+C` in the terminal
- Close the command window
- The bot stops immediately

---

## 📁 FILES OVERVIEW

### Core Files:

- `smart_scheduler.py` - Intelligent scheduling logic
- `scraper.py` - Multi-source internship scraping
- `collect.py` - Collects and batches internships
- `send_batch_email_only.py` - Email-only notifications
- `start_smart_bot.bat` - Easy startup script

### Configuration:

- `config.py` - Email settings and recipients
- `requirements.txt` - Python dependencies

### Generated Files:

- `seen.json` - Tracks sent internships (prevents duplicates)
- `batch.json` - Temporary storage for new internships
- `internship_bot.log` - Activity log file

---

## 🎯 SUCCESS METRICS

After setup, you'll get:

- ✅ Only NEW, relevant internships
- ✅ Beautiful, professional email format
- ✅ Multi-platform coverage
- ✅ Zero duplicates guaranteed
- ✅ Intelligent timing (no empty emails)
- ✅ Complete automation
- ✅ 100% FREE operation

---

## 💡 PRO TIPS

1. **Run overnight**: Let it search while you sleep
2. **Multiple recipients**: Share with friends/study groups
3. **Check logs**: Monitor activity in `internship_bot.log`
4. **Whitelist email**: Add sender to safe senders list
5. **Backup settings**: Keep a copy of `config.py` settings

---

## 🆘 NEED HELP?

If you encounter any issues:

1. Check the log file: `internship_bot.log`
2. Verify all files are present
3. Ensure Python 3.7+ is installed
4. Check internet connectivity

**The bot is designed to be completely autonomous - set it up once and let it find opportunities for you!** 🚀
