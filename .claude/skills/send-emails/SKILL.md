# AI Employee - Send Approved Emails Skill

This skill sends all approved emails via Gmail API.

## Usage
```
/send-emails
```

## What it does
1. Scans Approved/ folder for email approvals
2. Authenticates with Gmail API
3. Sends each approved email
4. Moves sent emails to Done/
5. Logs all email activity

## When to use
- After approving email drafts
- To send queued emails
- As part of scheduled workflow
