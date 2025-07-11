# 🤖 Smart Internship Bot

![GitHub Actions](https://img.shields.io/github/workflow/status/YOUR_USERNAME/internship-bot/Automated%20Internship%20Bot?label=Cloud%20Automation&logo=github)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

> **Automated, intelligent internship discovery and email notification system. Runs 24/7 in the cloud, never miss a fresh opportunity again!**

---

## ✨ Features

- 🔍 **Multi-Source Scraping**: Internshala, Naukri, Glassdoor, Unstop, and more
- 🧠 **Smart Filtering**: Only sends new, relevant internships (no repeats, no spam)
- ⏰ **2-Week Freshness**: Never get old or expired listings
- 📧 **Email-Only Alerts**: Clean, professional notifications to your inbox
- 🚦 **Frequency Control**: Max 3 emails/day, min 4 hours apart
- 🔒 **Secure**: Credentials stored as encrypted GitHub secrets
- ☁️ **Cloud-Hosted**: Runs automatically every 5 hours via GitHub Actions
- 🆓 **100% Free**: No paid services, no server required

---

## 🚀 Quick Start

### 1. **Fork or Clone This Repo**

```bash
git clone https://github.com/YOUR_USERNAME/internship-bot.git
cd internship-bot
```

### 2. **Set Up GitHub Secrets**

Go to your repo → Settings → Secrets and variables → Actions → New repository secret:

| Name              | Example Value                                 |
|-------------------|-----------------------------------------------|
| `SMTP_USER`       | `your.email@gmail.com`                        |
| `SMTP_PASS`       | `your-gmail-app-password`                     |
| `RECIPIENT_EMAILS`| `email1@gmail.com,email2@gmail.com,...`       |

> **Tip:** See [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) for full instructions and screenshots.

### 3. **Enable GitHub Actions**

- Go to the **Actions** tab
- Enable workflows if prompted
- The bot will now run automatically every 5 hours!

---

## 📧 How It Works

1. **Scrapes** top internship sites for new listings
2. **Filters** out duplicates and old postings (>2 weeks)
3. **Batches** new opportunities
4. **Sends** a single, clean email to all recipients
5. **Logs** all activity for easy monitoring

---

## 🛠️ Configuration

- **Edit `config.py`** for local testing (uses environment variables in cloud)
- **Change recipient list** by updating the `RECIPIENT_EMAILS` secret
- **Modify schedule** by editing `.github/workflows/internship-bot.yml` (cron)

---

## 🧑‍💻 Local Development

```bash
pip install -r requirements.txt
python smart_scheduler.py
```

---

## 🏆 Why Use This Bot?

- **Never miss a new internship**
- **No manual searching or filtering**
- **No server or cloud account needed**
- **Works for teams, friends, or solo**
- **Easy to deploy, easy to maintain**

---

## 📚 Documentation

- [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) — Full cloud setup guide
- [SMART_BOT_GUIDE.md](SMART_BOT_GUIDE.md) — Advanced usage and customization

---

## 🙏 Credits

- Built by [Swayam](https://github.com/doSwayamCode)
- Inspired by the need for smarter, faster internship discovery

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.
