# AI Employee - Send WhatsApp Messages Skill

This skill sends approved WhatsApp messages through WhatsApp Web.

## Usage
```
/send-whatsapp
```

## What it does
1. Scans Approved folder for WhatsApp reply files
2. Opens WhatsApp Web with saved session
3. Sends each approved message
4. Moves sent messages to Done folder
5. Logs all sending activity

## When to use
- After reviewing and approving WhatsApp replies
- To send queued WhatsApp messages
- For batch sending approved messages

## Requirements
- WhatsApp Web session must be active
- Messages must be in Approved folder
- Browser window will open (not headless)

## File Format
Approved messages should have:
```yaml
---
to: Contact Name
message: Your message text here
---
```
