# AI Employee - Process WhatsApp Tasks Skill

This skill processes WhatsApp message tasks and creates draft replies.

## Usage
```
/process-whatsapp
```

## What it does
1. Scans Needs_Action for WhatsApp message tasks
2. Reads message content and context
3. Drafts appropriate replies
4. Creates approval requests in Pending_Approval
5. Updates Dashboard with WhatsApp activity

## When to use
- After WhatsApp watcher detects new messages
- To handle WhatsApp message backlog
- For automated WhatsApp triage

## Workflow
1. WhatsApp watcher creates task: `WHATSAPP_*.md` in Needs_Action
2. This skill drafts reply and saves to Pending_Approval
3. Human reviews and moves to Approved folder
4. Use `/send-whatsapp` to send approved messages
