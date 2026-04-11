# 🎯 Bronze Tier - Quick Start Guide

## ✅ What You've Built

Your Bronze Tier AI Employee is now operational with:
- **Obsidian Vault**: Structured knowledge base with Dashboard and Company Handbook
- **File System Watcher**: Monitors Inbox folder for new files
- **Agent Skills**: `/process-tasks` and `/update-dashboard`
- **Automated Workflow**: Drop file → Detect → Process → Complete

## 🚀 How to Use Your AI Employee

### Method 1: Automatic File Monitoring

**Step 1: Start the Watcher**
```bash
# Open a terminal in your vault directory
cd "D:\GIAIC\Hackathon\Hackathon_0\AI_Employee_Vault"

# Start the file system watcher
python filesystem_watcher.py
```

**Step 2: Drop Files**
- Copy any file into the `Inbox/` folder
- The watcher automatically creates a task in `Needs_Action/`

**Step 3: Process Tasks**
```bash
# In Claude Code, run:
/process-tasks
```

**Step 4: Check Dashboard**
- Open `Dashboard.md` in Obsidian to see updated stats
- Or run: `/update-dashboard`

### Method 2: Manual Task Creation

**Create a task file directly in Needs_Action:**

```markdown
---
type: task
priority: high
status: pending
---

## Task Title

Description of what needs to be done.

**Actions:**
- [ ] Step 1
- [ ] Step 2
```

Then run `/process-tasks` to process it.

## 📋 Common Workflows

### Workflow 1: Document Analysis
1. Drop a document into `Inbox/`
2. Watcher creates task in `Needs_Action/`
3. Run `/process-tasks`
4. AI analyzes document and creates summary
5. Task moved to `Done/`

### Workflow 2: Daily Briefing
```bash
# Ask Claude to create a daily summary
claude "Read all completed tasks from Done/ today and create a daily briefing"
```

### Workflow 3: Task Planning
1. Create complex task in `Needs_Action/`
2. Run `/process-tasks`
3. AI creates detailed plan in `Plans/`
4. Execute plan steps
5. Move to `Done/` when complete

## 🎮 Try It Now

**Test the complete workflow:**

1. **Create a test file:**
```bash
echo "This is a test document for AI processing" > Inbox/test_document.txt
```

2. **Start the watcher** (if not running):
```bash
python filesystem_watcher.py
```

3. **Process the task:**
```bash
/process-tasks
```

4. **Check results:**
- View `Dashboard.md` for updated stats
- Check `Done/` folder for completed task
- Review `Logs/events_*.log` for audit trail

## 📊 Monitoring Your AI Employee

### Dashboard View
Open `Dashboard.md` in Obsidian to see:
- Pending tasks count
- Completed tasks today
- Recent activity log
- System status

### Log Files
Check `Logs/` folder for:
- `events_YYYYMMDD.log` - Daily event log
- `watcher.log` - File system watcher activity

## 🔧 Troubleshooting

**Watcher not detecting files?**
- Ensure watcher is running: `ps aux | grep filesystem_watcher`
- Check watcher.log for errors
- Verify Inbox folder exists

**Tasks not processing?**
- Check file format (must be .md with frontmatter)
- Verify file is in Needs_Action folder
- Run `/process-tasks` manually

**Dashboard not updating?**
- Run `/update-dashboard` manually
- Check Dashboard.md file permissions

## 🎓 Next Steps

### Enhance Bronze Tier
- Add more task types
- Create custom processing rules
- Add email notifications

### Progress to Silver Tier
- Add Gmail watcher
- Add WhatsApp watcher
- Implement MCP servers
- Add scheduling (cron/Task Scheduler)
- Human-in-the-loop approval workflow

## 📝 Bronze Tier Checklist

- ✅ Obsidian vault structure
- ✅ Dashboard.md and Company_Handbook.md
- ✅ File system watcher (filesystem_watcher.py)
- ✅ Agent Skills (/process-tasks, /update-dashboard)
- ✅ Folder structure (Inbox, Needs_Action, Done, Plans, Logs)
- ✅ Claude Code integration tested
- ✅ Complete workflow verified

**🎉 Congratulations! Your Bronze Tier AI Employee is ready for production use!**

---
*For questions or issues, refer to README.md or the main hackathon document*
