# WhatsApp Integration Setup Guide - Silver Tier

This guide walks you through setting up WhatsApp monitoring for your AI Employee.

## Prerequisites
- WhatsApp account with active phone number
- Python 3.13+ installed
- Playwright installed
- AI Employee vault set up

## Step 1: Install Dependencies

```bash
# Install Playwright
pip install playwright

# Install Playwright browsers
playwright install chromium
```

Or use project dependencies:
```bash
pip install -e .
playwright install chromium
```

## Step 2: Configure Keywords

Edit `whatsapp_watcher.py` to customize monitored keywords:

```python
self.keywords = [
    'urgent', 'asap', 'help', 'invoice', 'payment',
    'quote', 'pricing', 'order', 'delivery', 'issue',
    # Add your custom keywords here
]
```

## Step 3: First Run (QR Code Scan)

```bash
python whatsapp_watcher.py
```

**What happens:**
1. Chrome browser opens automatically
2. WhatsApp Web loads
3. **Scan QR code with your phone:**
   - Open WhatsApp on your phone
   - Tap Menu (⋮) → Linked Devices
   - Tap "Link a Device"
   - Scan the QR code on screen
4. Session saved to `sessions/whatsapp/`
5. Watcher starts monitoring

**Note:** You only need to scan QR code once. The session is saved for future runs.

## Step 4: Test It

1. Send yourself a WhatsApp message from another phone
2. Include a keyword like "urgent" or "help"
3. Keep the message unread
4. Wait up to 30 seconds
5. Check `Needs_Action/` folder for new task file

## How It Works

**Monitoring Process:**
1. Watcher checks WhatsApp Web every 30 seconds
2. Looks for unread messages
3. Scans messages for keywords
4. Creates task file if keyword found
5. Logs the event

**What Gets Detected:**
- Unread messages only
- Messages containing monitored keywords
- Last 5 messages from each chat

## Configuration

### Change Check Interval

Edit `whatsapp_watcher.py`:
```python
check_interval=30  # 30 seconds (default)
```

### Add More Keywords

```python
self.keywords = [
    'urgent', 'asap', 'help',
    'client', 'meeting', 'deadline',
    'bug', 'error', 'down'
]
```

### Case Sensitivity

Keywords are case-insensitive by default:
- "URGENT" = "urgent" = "Urgent"

## Running in Background

### Windows (Task Scheduler)
See SCHEDULING_SETUP.md

### Mac/Linux (screen/tmux)
```bash
# Using screen
screen -S whatsapp
python whatsapp_watcher.py
# Press Ctrl+A then D to detach

# Reattach later
screen -r whatsapp
```

## Troubleshooting

### QR Code Not Appearing
- Check if Chrome browser opened
- Try closing and restarting the watcher
- Clear `sessions/whatsapp/` folder and try again

### "Session expired" error
- Delete `sessions/whatsapp/` folder
- Run watcher again
- Scan QR code again

### Messages Not Detected
- Check message contains a monitored keyword
- Check message is unread
- Wait 30 seconds (default check interval)
- Check `Logs/whatsapp_watcher.log` for errors

### Browser Closes Immediately
- Ensure `headless=False` in the code
- WhatsApp Web requires visible browser
- Don't minimize the browser window

### "Playwright not installed" error
```bash
playwright install chromium
```

## Security Notes

⚠️ **Important:**
- Never commit `sessions/` folder to Git
- Already in `.gitignore`
- Keep your WhatsApp session secure
- Don't share session files

## Limitations

**WhatsApp Web Restrictions:**
- Must keep browser window open (can't run headless)
- Session expires after ~2 weeks of inactivity
- Requires stable internet connection
- Can't send messages (read-only for now)

## Processing WhatsApp Tasks

Once a task is created:
```bash
# Process the task
/process-tasks

# AI will read the message and suggest actions
# For replies, use approval workflow
```

## Next Steps

- Set up approval workflow for WhatsApp replies
- Configure auto-responses (Silver Tier+)
- Integrate with CRM (Gold Tier)

---
*Part of Silver Tier AI Employee implementation*
