# WhatsApp Integration Setup - Step by Step Guide

## Overview

WhatsApp integration uses browser automation (Playwright) to monitor WhatsApp Web for messages with specific keywords.

**Time Required:** 10-15 minutes  
**Difficulty:** Medium  
**Requirements:** Active WhatsApp account on your phone

---

## Step 1: Install Dependencies (3 minutes)

```bash
# Install Playwright (if not already installed)
pip install playwright

# Install Chromium browser
playwright install chromium
```

**Verify installation:**
```bash
playwright --version
# Should show: Version 1.40.0 or higher
```

---

## Step 2: Customize Keywords (2 minutes)

Edit `whatsapp_watcher.py` to monitor keywords relevant to you:

**Open the file and find this section:**
```python
self.keywords = [
    'urgent', 'asap', 'help', 'invoice', 'payment',
    'quote', 'pricing', 'order', 'delivery', 'issue'
]
```

**Customize for your needs:**

**For Business:**
```python
self.keywords = [
    'urgent', 'asap', 'help',
    'invoice', 'payment', 'quote', 'pricing',
    'order', 'delivery', 'client', 'meeting'
]
```

**For Personal:**
```python
self.keywords = [
    'urgent', 'emergency', 'help',
    'important', 'asap', 'call me'
]
```

**For Tech Support:**
```python
self.keywords = [
    'urgent', 'down', 'error', 'bug',
    'broken', 'not working', 'help', 'issue'
]
```

**Save the file** after editing.

---

## Step 3: First Run - QR Code Scan (5 minutes)

```bash
python whatsapp_watcher.py
```

**What happens:**

### 1. Chrome Browser Opens
- WhatsApp Web loads automatically
- You'll see a QR code on screen

### 2. Scan QR Code with Your Phone

**On your phone:**
1. Open WhatsApp
2. Tap the **menu** (⋮ on Android, Settings on iPhone)
3. Tap **"Linked Devices"**
4. Tap **"Link a Device"**
5. **Scan the QR code** on your computer screen

**Important:**
- Keep your phone connected to internet
- Don't close WhatsApp on your phone
- QR code expires after 60 seconds (refresh if needed)

### 3. WhatsApp Web Loads
- Your chats appear
- Script detects successful login
- Session saved to `sessions/whatsapp/`

### 4. Monitoring Starts

**You'll see in terminal:**
```
2026-04-11 - WhatsAppWatcher - INFO - WhatsApp Watcher initialized
2026-04-11 - WhatsAppWatcher - INFO - Monitoring keywords: urgent, asap, help...
2026-04-11 - WhatsAppWatcher - INFO - Opening WhatsApp Web...
2026-04-11 - WhatsAppWatcher - INFO - WhatsApp Web loaded successfully
2026-04-11 - WhatsAppWatcher - INFO - Monitoring WhatsApp every 30 seconds
2026-04-11 - WhatsAppWatcher - INFO - Press Ctrl+C to stop
```

**Keep the browser window open!** WhatsApp Web requires a visible browser.

---

## Step 4: Test It (3 minutes)

### Send a Test Message

**Option 1: From Another Phone**
1. Have someone send you: "This is urgent, please help!"
2. Keep the message unread
3. Wait 30 seconds

**Option 2: Send to Yourself**
1. Create a group with just you
2. Send: "Test urgent message"
3. Keep unread
4. Wait 30 seconds

### Check for Detection

**Watch the terminal:**
```
2026-04-11 - WhatsAppWatcher - INFO - Found 1 unread chats
2026-04-11 - WhatsAppWatcher - INFO - Created task file: WHATSAPP_20260411_080000_TestContact.md
```

**Check the vault:**
```bash
ls Needs_Action/
# Should see: WHATSAPP_YYYYMMDD_HHMMSS_ContactName.md
```

**Read the task file:**
```bash
cat Needs_Action/WHATSAPP_*.md
```

---

## Step 5: Process WhatsApp Tasks

```bash
/process-tasks
```

**What happens:**
1. AI reads the WhatsApp message
2. Understands the context
3. Suggests appropriate actions
4. Creates a response plan
5. Moves to Done/ when complete

**For replies (future feature):**
- AI will draft a reply
- Create approval request
- You approve
- Reply sent via WhatsApp

---

## Running in Background

### Option 1: Keep Terminal Open
- Simple but requires terminal to stay open
- Good for testing

### Option 2: Screen/Tmux (Mac/Linux)
```bash
# Start screen session
screen -S whatsapp

# Run watcher
python whatsapp_watcher.py

# Detach: Press Ctrl+A then D

# Reattach later
screen -r whatsapp
```

### Option 3: Task Scheduler (Windows)
See `SCHEDULING_SETUP.md` for details.

**Note:** Browser window must stay visible (can't run headless).

---

## Important Limitations

### WhatsApp Web Restrictions

**Must Keep Browser Open:**
- WhatsApp Web doesn't work headless
- Browser window must be visible
- Can minimize but not close

**Session Expires:**
- After ~2 weeks of inactivity
- Need to scan QR code again
- Delete `sessions/whatsapp/` and restart

**Read-Only (For Now):**
- Can detect messages
- Can create tasks
- Cannot send replies yet (future feature)

**Internet Required:**
- Both computer and phone need internet
- Phone must have WhatsApp running

---

## Troubleshooting

### QR Code Not Appearing
```bash
# Close everything and try again
# Delete session
rm -rf sessions/whatsapp/
python whatsapp_watcher.py
```

### "Session expired" Error
```bash
# Delete session and re-scan
rm -rf sessions/whatsapp/
python whatsapp_watcher.py
# Scan QR code again
```

### Messages Not Detected
**Check:**
- Message contains a monitored keyword
- Message is unread
- Wait 30 seconds (check interval)
- Browser window is open

**Debug:**
```bash
# Check logs
cat Logs/whatsapp_watcher.log
```

### Browser Closes Immediately
- Ensure `headless=False` in code
- Check Playwright is installed
- Try: `playwright install chromium`

### "Playwright not installed"
```bash
pip install playwright
playwright install chromium
```

---

## Advanced Configuration

### Change Check Interval

Edit `whatsapp_watcher.py`:
```python
check_interval=30  # Default: 30 seconds

# Options:
check_interval=15  # More frequent (uses more resources)
check_interval=60  # Less frequent (saves resources)
```

### Add More Keywords

Edit `whatsapp_watcher.py`:
```python
self.keywords = [
    'urgent', 'asap', 'help',
    # Add your keywords:
    'deadline', 'meeting', 'call',
    'important', 'emergency', 'now'
]
```

Keywords are case-insensitive:
- "URGENT" = "urgent" = "Urgent"

### Monitor Specific Contacts Only

Edit `whatsapp_watcher.py` and add:
```python
self.monitored_contacts = [
    'John Doe',
    'Client ABC',
    'Boss Name'
]
```

Then modify the detection logic to filter by contact name.

---

## Security & Privacy

**What's Stored:**
- Session data in `sessions/whatsapp/`
- Message previews in task files
- Event logs

**What's NOT Stored:**
- Full message history
- Media files
- Contact information

**Best Practices:**
- Don't commit `sessions/` folder
- Review task files before sharing
- Clear old logs periodically

---

## Next Steps

✅ WhatsApp monitoring working
- Test with real messages
- Adjust keywords as needed
- Set up auto-responses (future)
- Integrate with CRM (Gold Tier)

Then complete:
- Gmail integration
- LinkedIn posting
- Full orchestration
- Scheduling

---

## FAQ

**Q: Can I send messages?**
A: Not yet. Current version is read-only. Sending feature coming in future update.

**Q: Does this work on WhatsApp Business?**
A: Yes! Same process, just use WhatsApp Business Web.

**Q: Can I monitor multiple accounts?**
A: One account per session. For multiple accounts, run separate instances with different session folders.

**Q: Will this drain my phone battery?**
A: No more than normal WhatsApp usage. The monitoring happens on your computer.

**Q: Is this against WhatsApp ToS?**
A: This uses WhatsApp Web (official interface). However, use responsibly and don't spam.

---

*You only need to scan QR code once. Future runs will use the saved session.*
