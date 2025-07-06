# 🛡️ SECURITY INCIDENT RESPONSE GUIDE

## ⚠️ **CREDENTIALS WERE EXPOSED ON GITHUB**

If you've already pushed your code to GitHub with sensitive information, follow these steps immediately:

---

## 🚨 **Step 1: IMMEDIATE Actions (Do This NOW!)**

### **Change Your Gmail App Password:**

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → App passwords
3. **REVOKE** the exposed app password: `bfoy dyjv sjvl bhrx`
4. **Generate a NEW app password**
5. Save it securely (don't put it in code!)

### **Check for Unauthorized Access:**

1. Go to [Google Account Activity](https://myaccount.google.com/security)
2. Check "Recent security activity"
3. Look for any suspicious login attempts

---

## 🧹 **Step 2: Clean Up Repository**

### **Option A: Remove Sensitive History (Recommended)**

```bash
# WARNING: This rewrites Git history!
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch config.py' \
--prune-empty --tag-name-filter cat -- --all

# Force push the cleaned history
git push origin --force --all
```

### **Option B: Delete and Recreate Repository**

1. Delete the GitHub repository
2. Create a new one
3. Push only the cleaned files

---

## 🔒 **Step 3: Secure Configuration**

### **For Local Development:**

1. Use `config_local.py` with your real credentials
2. **Never commit** `config_local.py` (it's in .gitignore)

### **For GitHub Actions:**

1. Use GitHub Secrets ONLY
2. Never hardcode credentials in any file

---

## 📋 **Step 4: GitHub Secrets Setup**

### **Required Secrets (NEW passwords):**

| Secret Name        | Value                                   |
| ------------------ | --------------------------------------- |
| `SMTP_USER`        | `swayamgupta999@gmail.com`              |
| `SMTP_PASS`        | `YOUR_NEW_APP_PASSWORD`                 |
| `RECIPIENT_EMAILS` | `email1@gmail.com,email2@gmail.com,...` |

---

## ✅ **Step 5: Verification**

### **Check That Credentials Are Secure:**

1. ✅ Old app password revoked from Google
2. ✅ New app password generated
3. ✅ GitHub Secrets configured with NEW password
4. ✅ No hardcoded credentials in any committed files
5. ✅ config_local.py in .gitignore

---

## 🛡️ **Best Practices Going Forward**

### **DO:**

- ✅ Use environment variables for secrets
- ✅ Use GitHub Secrets for automation
- ✅ Keep sensitive files in .gitignore
- ✅ Use config_local.py for local development
- ✅ Regularly rotate passwords

### **DON'T:**

- ❌ Never commit passwords/tokens to Git
- ❌ Never share app passwords
- ❌ Never hardcode credentials in source code
- ❌ Never ignore security warnings

---

## 🔍 **What Was Exposed?**

From your committed files:

- ❌ Gmail address: `swayamgupta999@gmail.com`
- ❌ Gmail app password: `bfoy dyjv sjvl bhrx`
- ❌ Recipient email addresses
- ❌ SMTP configuration

---

## 📞 **If You Need Help**

1. **Google Support**: If you see suspicious activity
2. **GitHub Support**: For repository security questions
3. **Change all related passwords**: If you use similar passwords elsewhere

---

## 🎯 **After Following This Guide**

Your bot will be:

- ✅ Secure and private
- ✅ Using fresh, uncompromised credentials
- ✅ Following security best practices
- ✅ Safe to run in GitHub Actions

**Remember: Security is ongoing, not a one-time fix!** 🛡️
