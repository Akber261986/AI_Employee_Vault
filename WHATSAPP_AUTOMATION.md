# WhatsApp Automation - Complete Setup Guide

## Overview

Full WhatsApp automation with monitoring, reply drafting, approval workflow, and sending through WhatsApp Web.

## Features

- **Monitor**: Detects messages with keywords (urgent, help, invoice, etc.)
- **Draft**: AI drafts contextual replies
- **Approve**: Human-in-the-loop approval workflow
- **Send**: Automated sending through WhatsApp Web

## Quick Start

### 1. Initial Setup (One-Time)

```bash
# Install dependencies
pip install playwright
playwright install chromium

# Authenticate WhatsApp Web
python whatsapp_watcher.py
# Scan QR code with your phone
# Session saved to sessions/whatsapp/
```

### 2. Complete Workflow

**Step 1: Monitor for Messages**
```bash
# Start watcher (runs continuously)
python whatsapp_watcher.py

# Or use orchestrator for all watchers
python orchestrator.py
```

**Step 2: Process Detected Messages**
```bash
# In Claude Code
/process-whatsapp
```
This will:
- Read WhatsApp tasks from Needs_Action/
- Draft appropriate replies
- Save to Pending_Approval/ for review

**Step 3: Review and Approve**
- Open files in Pending_Approval/
- Review the draft reply
- Edit if needed (modify the `message:` field)
- Move to Approved/ folder to approve
- Or move to Rejected/ to reject

**Step 4: Send Approved Messages**
```bash
# In Claude Code
/send-whatsapp

# Or run directly
python whatsapp_sender.py
```
This will:
- Open WhatsApp Web (browser window)
- Send each approved message
- Move sent messages to Done/

## File Structure

```
Needs_Action/
  └── WHATSAPP_20260419_133000_Contact.md    # Detected message

Pending_Approval/
  └── WHATSAPP_REPLY_20260419_133500_Contact.md    # Draft reply

Approved/
  └── WHATSAPP_REPLY_20260419_133500_Contact.md    # Approved reply

Done/
  ├── PROCESSED_20260419_133000_Contact.md    # Original task
  └── SENT_20260419_134000_WHATSAPP_REPLY_...md    # Sent message
```

## Message File Format

### Detected Message (from watcher)
```yaml
---
type: whatsapp_message
chat_name: Contact Name
received: 2026-04-19T13:30:00
priority: high
status: pending
---

Recent Messages:
- Message text here
```

### Draft Reply (for approval)
```yaml
---
type: whatsapp_reply
to: Contact Name
message: Your reply text here
original_task: WHATSAPP_20260419_133000_Contact.md
created: 2026-04-19T13:35:00
status: pending_approval
---
```

## Customization

### Keywords to Monitor

Edit `whatsapp_watcher.py`:
```python
self.keywords = [
    'urgent', 'asap', 'help', 'invoice', 'payment',
    'quote', 'pricing', 'order', 'delivery', 'issue',
    # Add your keywords here
]
```

### Check Interval

```python
check_interval=30  # Check every 30 seconds
```

## Skills Available

- `/process-whatsapp` - Process detected messages and draft replies
- `/send-whatsapp` - Send approved messages

## Troubleshooting

### WhatsApp Web Session Expired
```bash
# Delete session and re-authenticate
rm -rf sessions/whatsapp/
python whatsapp_watcher.py
# Scan QR code again
```

### Message Not Sending
- Verify contact name matches exactly as in WhatsApp
- Check WhatsApp Web is loaded (browser window open)
- Ensure message is in Approved/ folder
- Check logs: `Logs/whatsapp_sender.log`

### Browser Closes Immediately
- WhatsApp Web requires visible browser (headless=False)
- Don't minimize the browser window
- Keep it in background while sending

## Security

- Session files in `sessions/whatsapp/` (in .gitignore)
- Never commit session data
- All messages require human approval before sending
- Complete audit trail in Logs/

## Integration with Orchestrator

The orchestrator automatically runs:
- WhatsApp Watcher (continuous monitoring)
- Gmail Watcher
- File System Watcher

To start all watchers:
```bash
python orchestrator.py
```

## Next Steps

- Test with real WhatsApp messages
- Customize keywords for your use case
- Set up scheduled automation (Task Scheduler/cron)
- Integrate with CRM (Gold Tier)

---
*Part of Silver Tier AI Employee - WhatsApp Automation Complete*
