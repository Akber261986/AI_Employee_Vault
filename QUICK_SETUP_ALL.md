# 🚀 Quick Setup Guide - All Three Integrations

## Overview

This guide walks you through setting up Gmail, LinkedIn, and WhatsApp in the fastest way possible.

**Total Time:** 20-30 minutes  
**Recommended Order:** Gmail → LinkedIn → WhatsApp

---

## ⚡ Quick Setup Checklist

### Prerequisites (5 minutes)
```bash
# Install all dependencies at once
pip install -e .
playwright install chromium
```

### Create Required Folders
```bash
mkdir -p credentials tokens sessions/whatsapp sessions/linkedin LinkedIn_Posts
```

---

## 1️⃣ Gmail Setup (10 minutes)

### Quick Steps:
1. **Google Cloud Console** → https://console.cloud.google.com/
2. **Create project** → "AI-Employee-Gmail"
3. **Enable Gmail API** → APIs & Services → Library → Gmail API → Enable
4. **OAuth consent** → External → Fill basic info → Add yourself as test user
5. **Create credentials** → OAuth client ID → Desktop app → Download JSON
6. **Move file:**
   ```bash
   mv ~/Downloads/client_secret_*.json credentials/gmail_credentials.json
   ```
7. **Run and authenticate:**
   ```bash
   python gmail_watcher.py
   ```
8. **Browser opens** → Login → Grant permissions → Done!

### Test:
- Send yourself an email
- Mark as important (star it)
- Keep unread
- Wait 5 minutes
- Check `Needs_Action/` for task file

**Detailed guide:** `GMAIL_SETUP_DETAILED.md`

---

## 2️⃣ LinkedIn Setup (5 minutes)

### Quick Steps:
1. **Create a post:**
   ```bash
   cat > LinkedIn_Posts/test_post.md << 'EOF'
   ---
   type: linkedin_post
   ---
   
   🚀 Testing my AI Employee's LinkedIn integration!
   
   Just built an autonomous assistant that posts for me.
   
   #AI #Automation #Productivity
   EOF
   ```

2. **Run and login:**
   ```bash
   python linkedin_poster.py
   ```

3. **Browser opens** → Login to LinkedIn → Post publishes automatically!

### Test:
- Check LinkedIn feed for your post
- Check `LinkedIn_Posts/Posted/` for moved file

**Detailed guide:** `LINKEDIN_SETUP_DETAILED.md`

---

## 3️⃣ WhatsApp Setup (10 minutes)

### Quick Steps:
1. **Run the watcher:**
   ```bash
   python whatsapp_watcher.py
   ```

2. **Browser opens** → QR code appears

3. **On your phone:**
   - Open WhatsApp
   - Menu → Linked Devices
   - Link a Device
   - Scan QR code

4. **WhatsApp Web loads** → Monitoring starts!

### Test:
- Send yourself: "This is urgent!"
- Keep unread
- Wait 30 seconds
- Check `Needs_Action/` for task file

**Detailed guide:** `WHATSAPP_SETUP_DETAILED.md`

---

## 🎯 All Set Up? Run Everything!

### Start All Watchers:
```bash
# Windows
start_silver_tier.bat

# Mac/Linux
./start_silver_tier.sh
```

This starts:
- Gmail Watcher (checks every 5 min)
- File System Watcher (monitors Inbox/)
- Master Orchestrator (manages all)

### Process Tasks:
```bash
/process-tasks      # Process all tasks
/process-emails     # Process email tasks specifically
/send-emails        # Send approved emails
/update-dashboard   # Update dashboard
```

---

## 🔧 Troubleshooting Quick Fixes

### Gmail Issues:
```bash
# Re-authenticate
rm tokens/gmail_token.pickle
python gmail_watcher.py
```

### LinkedIn Issues:
```bash
# Re-login
rm -rf sessions/linkedin/
python linkedin_poster.py
```

### WhatsApp Issues:
```bash
# Re-scan QR code
rm -rf sessions/whatsapp/
python whatsapp_watcher.py
```

---

## 📋 Daily Workflow

### Morning (5 minutes):
1. Check Dashboard.md in Obsidian
2. Review Needs_Action/ folder
3. Run `/process-tasks`
4. Approve any pending actions

### Throughout Day:
- Watchers run automatically
- Tasks created automatically
- Process when convenient

### Evening (5 minutes):
1. Review Done/ folder
2. Check Logs/ for any issues
3. Plan tomorrow's LinkedIn posts

---

## 🎓 Next Steps

### After Setup:
- [ ] Test each integration
- [ ] Set up scheduling (SCHEDULING_SETUP.md)
- [ ] Create 5-7 LinkedIn posts in advance
- [ ] Monitor for 24 hours
- [ ] Adjust keywords and settings

### Progress to Gold Tier:
- [ ] Odoo accounting integration
- [ ] Facebook/Instagram integration
- [ ] Twitter (X) integration
- [ ] Weekly CEO briefing
- [ ] Ralph Wiggum autonomous loop

---

## 💡 Pro Tips

**Gmail:**
- Use filters to auto-star important emails
- Adjust check interval in code (default: 5 min)

**LinkedIn:**
- Post at 8-10 AM for best engagement
- Create posts in batches
- Use AI to draft posts: `/process-tasks`

**WhatsApp:**
- Customize keywords for your needs
- Keep browser window visible
- Session lasts ~2 weeks

---

## 🆘 Need Help?

**Detailed Guides:**
- `GMAIL_SETUP_DETAILED.md` - Step-by-step Gmail
- `LINKEDIN_SETUP_DETAILED.md` - Step-by-step LinkedIn
- `WHATSAPP_SETUP_DETAILED.md` - Step-by-step WhatsApp
- `SCHEDULING_SETUP.md` - Automated scheduling

**Common Issues:**
- Check `Logs/` folder for errors
- Verify dependencies: `pip list | grep -E "google|playwright"`
- Test individually before running orchestrator

---

*Setup once, run forever!*
