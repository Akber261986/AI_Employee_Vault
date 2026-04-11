# AI Employee Vault - Silver Tier

**Status**: 🥈 Silver Tier Complete  
**Version**: 0.2.0  
**Tier**: Functional Assistant

## Quick Overview

A fully functional AI Employee that monitors multiple channels (Gmail, WhatsApp, Files), processes tasks autonomously, drafts and sends emails with approval, posts to LinkedIn automatically, and runs on a schedule 24/7.

## Features

### Bronze Tier (Foundation) ✅
- File system monitoring
- Task processing workflow
- Dashboard management
- Audit logging
- Agent Skills framework

### Silver Tier (Functional Assistant) ✅
- **Gmail Integration**: Monitors inbox for important emails
- **WhatsApp Monitoring**: Detects messages with keywords
- **LinkedIn Auto-Posting**: Generates business leads
- **Email MCP Server**: Sends emails with approval workflow
- **Master Orchestrator**: Manages all watchers
- **Scheduling System**: Runs automatically 24/7
- **Human-in-the-Loop**: Approval workflow for sensitive actions

## Quick Start

### Installation

```bash
# Install dependencies
pip install -e .
playwright install chromium
```

### Setup (One-Time)

1. **Gmail API** (5 minutes)
   - Follow `GMAIL_SETUP.md`
   - Download OAuth2 credentials
   - Save to `credentials/gmail_credentials.json`

2. **WhatsApp** (2 minutes)
   ```bash
   python whatsapp_watcher.py
   # Scan QR code with your phone
   ```

3. **LinkedIn** (2 minutes)
   ```bash
   python linkedin_poster.py
   # Log in manually when browser opens
   ```

### Running

**Option 1: All Watchers (Recommended)**
```bash
# Windows
start_silver_tier.bat

# Mac/Linux
./start_silver_tier.sh
```

**Option 2: Individual Watchers**
```bash
python gmail_watcher.py      # Gmail monitoring
python whatsapp_watcher.py   # WhatsApp monitoring
python filesystem_watcher.py # File monitoring
python linkedin_poster.py    # LinkedIn posting
```

**Option 3: Scheduled (Set and Forget)**
- Follow `SCHEDULING_SETUP.md`
- Set up Task Scheduler or cron
- Runs automatically in background

### Using Agent Skills

```bash
# Process all tasks
/process-tasks

# Process email tasks specifically
/process-emails

# Send approved emails
/send-emails

# Update dashboard
/update-dashboard
```

## Project Structure

```
AI_Employee_Vault/
├── 📊 Core Files
│   ├── Dashboard.md                    # Real-time dashboard
│   ├── Company_Handbook.md             # AI behavior rules
│   ├── orchestrator.py                 # Master process manager
│   └── pyproject.toml                  # Dependencies
│
├── 🔍 Watchers
│   ├── gmail_watcher.py                # Gmail monitoring
│   ├── whatsapp_watcher.py             # WhatsApp monitoring
│   ├── filesystem_watcher.py           # File monitoring
│   └── linkedin_poster.py              # LinkedIn posting
│
├── 🤖 MCP Servers
│   └── email_mcp.py                    # Email sending
│
├── 📁 Operational Folders
│   ├── Inbox/                          # Drop files here
│   ├── Needs_Action/                   # Pending tasks
│   ├── Done/                           # Completed tasks
│   ├── Pending_Approval/               # Awaiting approval
│   ├── Approved/                       # Approved actions
│   ├── LinkedIn_Posts/                 # Post queue
│   └── Logs/                           # System logs
│
├── 🔐 Credentials (not committed)
│   ├── credentials/                    # API credentials
│   ├── tokens/                         # OAuth tokens
│   └── sessions/                       # Browser sessions
│
├── 📚 Documentation
│   ├── README.md                       # This file
│   ├── QUICK_START.md                  # Quick reference
│   ├── SILVER_TIER_COMPLETE.md         # Silver tier summary
│   ├── GMAIL_SETUP.md                  # Gmail configuration
│   ├── WHATSAPP_SETUP.md               # WhatsApp setup
│   ├── LINKEDIN_SETUP.md               # LinkedIn setup
│   └── SCHEDULING_SETUP.md             # Scheduling guide
│
└── 🤖 Agent Skills
    ├── process-tasks/                  # Task processing
    ├── process-emails/                 # Email processing
    ├── send-emails/                    # Email sending
    └── update-dashboard/               # Dashboard updates
```

## Capabilities

### Email Management
- Monitor Gmail for important emails
- Create tasks automatically
- Draft professional replies
- Send emails after approval
- Track all email activity

### WhatsApp Monitoring
- Monitor messages with keywords
- Create tasks for urgent messages
- Track conversation context
- Log all detections

### LinkedIn Automation
- Auto-post business content
- Schedule posts in advance
- Track published posts
- Generate leads

### Workflow Automation
- Human-in-the-loop approval
- Multi-step task processing
- Automatic scheduling
- Error recovery

## Security

- OAuth2 for Gmail (secure, no passwords)
- Session persistence for WhatsApp/LinkedIn
- All secrets in .gitignore
- Approval workflow for sensitive actions
- Complete audit trail

## Tier Progression

- ✅ **Bronze Tier**: Foundation (File monitoring, basic tasks)
- ✅ **Silver Tier**: Functional Assistant (Multi-channel, automation)
- ⏳ **Gold Tier**: Autonomous Employee (Odoo, social media, CEO briefing)
- ⏳ **Platinum Tier**: Always-On Cloud + Local (24/7 cloud deployment)

## Documentation

- `README.md` - This file
- `QUICK_START.md` - Quick reference guide
- `SILVER_TIER_COMPLETE.md` - Silver tier achievement summary
- `GMAIL_SETUP.md` - Gmail API configuration
- `WHATSAPP_SETUP.md` - WhatsApp integration
- `LINKEDIN_SETUP.md` - LinkedIn posting
- `SCHEDULING_SETUP.md` - Task scheduling
- `DEMO_SCRIPT.md` - Demo walkthrough

## Troubleshooting

See individual setup guides for specific issues:
- Gmail: `GMAIL_SETUP.md`
- WhatsApp: `WHATSAPP_SETUP.md`
- LinkedIn: `LINKEDIN_SETUP.md`
- Scheduling: `SCHEDULING_SETUP.md`

## Next Steps

### Test Silver Tier
1. Set up Gmail API credentials
2. Authenticate WhatsApp and LinkedIn
3. Run orchestrator
4. Drop test files and send test emails
5. Monitor for 24 hours

### Progress to Gold Tier
- Odoo accounting integration
- Facebook/Instagram integration
- Twitter (X) integration
- Weekly CEO briefing
- Ralph Wiggum autonomous loop

## License

Built for Personal AI Employee Hackathon 0

---
*Silver Tier AI Employee - Built with Claude Code*
