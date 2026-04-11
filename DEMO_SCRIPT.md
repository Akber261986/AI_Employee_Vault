# Bronze Tier AI Employee - Demo Script

This script demonstrates the complete Bronze Tier workflow.

## Demo Scenario: Processing a Business Document

### Setup
```bash
cd "D:\GIAIC\Hackathon\Hackathon_0\AI_Employee_Vault"
```

### Demo Steps

#### 1. Start the AI Employee
```bash
# Terminal 1: Start the file system watcher
python filesystem_watcher.py
```

#### 2. Create a Sample Business Document
```bash
# Create a sample invoice request
cat > Inbox/invoice_request.txt << 'EOF'
Client: Acme Corporation
Project: Website Redesign
Amount: $2,500
Due Date: 2026-04-15
Status: Pending

Please process this invoice request and prepare the necessary documentation.
EOF
```

#### 3. Watch the Watcher Detect It
The watcher will automatically:
- Detect the new file in Inbox/
- Create a task file in Needs_Action/
- Log the event

#### 4. Process the Task
```bash
# In Claude Code:
/process-tasks
```

The AI will:
- Read the task from Needs_Action/
- Analyze the invoice request
- Create a summary or plan
- Move completed task to Done/
- Update Dashboard.md

#### 5. Review Results
```bash
# Check the dashboard
cat Dashboard.md

# Check completed task
ls -la Done/

# Check logs
cat Logs/events_$(date +%Y%m%d).log
```

## Expected Output

### Watcher Console
```
2026-04-10 22:55:00 - FileSystemWatcher - INFO - File System Watcher started
2026-04-10 22:55:05 - FileSystemWatcher - INFO - Created action file: FILE_20260410_225505_invoice_request.md
```

### Dashboard.md
```markdown
## Quick Stats
- **Pending Tasks**: 0
- **Completed Today**: 2
- **Active Projects**: 0

## Recent Activity
- [2026-04-10 22:56] ✅ Completed: Invoice request processing
- [2026-04-10 22:55] 📥 New task received: invoice_request
```

### Done Folder
```
Done/
├── TEST_system_verification.md
└── FILE_20260410_225505_invoice_request.md
```

## Demo Variations

### Variation 1: Multiple Files
```bash
# Drop multiple files at once
cp document1.pdf Inbox/
cp document2.txt Inbox/
cp spreadsheet.xlsx Inbox/

# Process all
/process-tasks
```

### Variation 2: Priority Tasks
Create a high-priority task:
```markdown
---
type: urgent_request
priority: high
status: pending
---

## Urgent: Client Follow-up Required

Client ABC needs immediate response about project timeline.
```

### Variation 3: Complex Task with Plan
```markdown
---
type: project
priority: normal
status: pending
---

## Project: Q1 Report Preparation

Multi-step project requiring:
1. Data collection
2. Analysis
3. Report writing
4. Review and approval
```

The AI will create a detailed plan in Plans/ folder.

## Success Criteria

✅ Watcher detects files in Inbox/
✅ Task files created in Needs_Action/
✅ AI processes tasks successfully
✅ Dashboard updates automatically
✅ Completed tasks moved to Done/
✅ Logs capture all events

## Troubleshooting Demo Issues

**File not detected:**
- Wait 1-2 seconds for watcher to detect
- Check watcher is running
- Verify file is in Inbox/ not a subfolder

**Task not processing:**
- Ensure task file has proper frontmatter
- Check file is .md format
- Verify Claude Code has vault access

**Dashboard not updating:**
- Run /update-dashboard manually
- Check file permissions

---
*Demo script for Bronze Tier AI Employee*
