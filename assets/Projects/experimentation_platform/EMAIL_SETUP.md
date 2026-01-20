# 📧 Email Alerts Setup Guide

## Quick Start

Your experiment platform now checks for significant results **every 5 minutes** and sends email alerts!

## Setup Instructions

### 1. Configure Email Settings

Edit `email_results.py` and update the `EMAIL_CONFIG` section:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'YOUR_EMAIL@gmail.com',      # ← Your Gmail address
    'sender_password': 'YOUR_APP_PASSWORD',      # ← App password (see below)
    'recipient_email': 'YOUR_EMAIL@gmail.com',   # ← Where to receive alerts
}
```

### 2. Get Gmail App Password

**Important:** Don't use your regular Gmail password!

1. Go to: https://myaccount.google.com/apppasswords
2. Click "Create app password"
3. Name it "Experiment Platform"
4. Copy the 16-character password
5. Paste it in `email_results.py` as `sender_password`

### 3. Start Email Alerts

Run in PowerShell:

```powershell
.\start_email_alerts.ps1
```

This will:
- Check experiments every 5 minutes
- Send email when significant results are found
- Run continuously until you press Ctrl+C

### 4. Test Immediately

To test right now:

```powershell
.\venv\Scripts\python.exe email_results.py
```

## What You'll Receive

Email alerts include:
- ✅ Winner detection
- 📊 Conversion rates (Control vs Variant)
- 📈 Lift percentage
- 🎯 Confidence level
- 📋 Sample sizes
- 🚀 Recommendations

## Using Other Email Providers

**Outlook/Office 365:**
```python
'smtp_server': 'smtp.office365.com',
'smtp_port': 587,
```

**Yahoo:**
```python
'smtp_server': 'smtp.mail.yahoo.com',
'smtp_port': 587,
```

**Custom SMTP:**
```python
'smtp_server': 'your.smtp.server.com',
'smtp_port': 587,
```

## Current Status

✅ Email script created: `email_results.py`
✅ Auto-check script created: `start_email_alerts.ps1`
✅ Checking every 5 minutes
✅ Lowered confidence threshold (80%) for faster results
⚠️  Email credentials needed (update EMAIL_CONFIG)

## Commands

| Action | Command |
|--------|---------|
| Start email alerts | `.\start_email_alerts.ps1` |
| Test email now | `.\venv\Scripts\python.exe email_results.py` |
| Stop alerts | Press `Ctrl+C` in the terminal |

---

**Note:** The system currently found **2 significant results** ready to email you!
