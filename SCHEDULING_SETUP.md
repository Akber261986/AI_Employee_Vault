# Scheduling Setup Guide - Silver Tier

This guide shows you how to schedule your AI Employee watchers to run automatically.

## Windows - Task Scheduler

### Step 1: Open Task Scheduler

1. Press `Win + R`
2. Type `taskschd.msc`
3. Press Enter

### Step 2: Create Basic Task

1. Click "Create Basic Task" in the right panel
2. Name: `AI Employee - Gmail Watcher`
3. Description: `Monitors Gmail for important emails`
4. Click "Next"

### Step 3: Set Trigger

**For continuous monitoring:**
- Trigger: "When the computer starts"
- Click "Next"

**For scheduled checks:**
- Trigger: "Daily"
- Start time: 8:00 AM
- Recur every: 1 day
- Click "Next"

### Step 4: Set Action

1. Action: "Start a program"
2. Program/script: `python`
3. Add arguments: `gmail_watcher.py`
4. Start in: `D:\GIAIC\Hackathon\Hackathon_0\AI_Employee_Vault`
5. Click "Next"

### Step 5: Finish

1. Check "Open the Properties dialog"
2. Click "Finish"

### Step 6: Configure Advanced Settings

In the Properties dialog:

**General tab:**
- ✅ Run whether user is logged on or not
- ✅ Run with highest privileges

**Triggers tab:**
- Edit trigger
- ✅ Enabled
- For "At startup": Add delay of 1 minute

**Actions tab:**
- Verify paths are correct

**Conditions tab:**
- ❌ Start only if on AC power (uncheck for laptops)
- ✅ Wake the computer to run this task

**Settings tab:**
- ✅ Allow task to be run on demand
- ✅ Run task as soon as possible after scheduled start is missed
- If task fails, restart every: 10 minutes
- Attempt to restart up to: 3 times

Click "OK" and enter your Windows password if prompted.

### Step 7: Repeat for Other Watchers

Create separate tasks for:
- `AI Employee - WhatsApp Watcher` → `whatsapp_watcher.py`
- `AI Employee - LinkedIn Poster` → `linkedin_poster.py` (daily at 9 AM)
- `AI Employee - Email Processor` → `email_mcp.py` (every 30 minutes)

## Mac/Linux - Cron

### Step 1: Edit Crontab

```bash
crontab -e
```

### Step 2: Add Cron Jobs

```bash
# AI Employee Watchers
# Format: minute hour day month weekday command

# Gmail Watcher - Run at startup
@reboot cd /path/to/AI_Employee_Vault && python3 gmail_watcher.py >> Logs/cron_gmail.log 2>&1

# WhatsApp Watcher - Run at startup
@reboot cd /path/to/AI_Employee_Vault && python3 whatsapp_watcher.py >> Logs/cron_whatsapp.log 2>&1

# LinkedIn Poster - Daily at 9 AM
0 9 * * * cd /path/to/AI_Employee_Vault && python3 linkedin_poster.py >> Logs/cron_linkedin.log 2>&1

# Email Processor - Every 30 minutes
*/30 * * * * cd /path/to/AI_Employee_Vault && python3 email_mcp.py >> Logs/cron_email.log 2>&1

# Task Processor - Every hour
0 * * * * cd /path/to/AI_Employee_Vault && python3 -c "from process_tasks import process_all; process_all()" >> Logs/cron_tasks.log 2>&1
```

### Step 3: Save and Exit

- Press `Esc`
- Type `:wq`
- Press `Enter`

### Step 4: Verify Cron Jobs

```bash
crontab -l
```

## Cron Schedule Examples

```bash
# Every 5 minutes
*/5 * * * * command

# Every hour
0 * * * * command

# Every day at 8 AM
0 8 * * * command

# Every weekday at 9 AM
0 9 * * 1-5 command

# Every Monday at 10 AM
0 10 * * 1 command

# Twice a day (9 AM and 5 PM)
0 9,17 * * * command
```

## Master Orchestrator Script

Create `orchestrator.py` to manage all watchers:

```python
#!/usr/bin/env python3
import subprocess
import time
from pathlib import Path

vault_path = Path(__file__).parent

# Start all watchers
watchers = [
    'gmail_watcher.py',
    'whatsapp_watcher.py',
]

processes = []

for watcher in watchers:
    proc = subprocess.Popen(['python', watcher], cwd=vault_path)
    processes.append(proc)
    print(f'Started: {watcher}')

# Keep running
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print('Stopping all watchers...')
    for proc in processes:
        proc.terminate()
```

Then schedule just the orchestrator:
```bash
@reboot cd /path/to/vault && python3 orchestrator.py
```

## Recommended Schedule

**Continuous (Always Running):**
- Gmail Watcher
- WhatsApp Watcher

**Periodic (Scheduled):**
- LinkedIn Poster: Daily at 9 AM
- Email Processor: Every 30 minutes
- Task Processor: Every hour
- Dashboard Update: Every 6 hours

## Monitoring Scheduled Tasks

### Windows
1. Open Task Scheduler
2. Click "Task Scheduler Library"
3. Find your tasks
4. Check "Last Run Result" column
5. View "History" tab for details

### Mac/Linux
```bash
# View cron logs
tail -f /var/log/syslog | grep CRON

# Or check your custom logs
tail -f Logs/cron_*.log
```

## Troubleshooting

### Task doesn't run on Windows
- Check Task Scheduler History
- Verify Python path is correct
- Test command manually first
- Check "Last Run Result" code

### Cron job doesn't run
```bash
# Check cron service is running
sudo service cron status

# Check system logs
grep CRON /var/log/syslog

# Test command manually
cd /path/to/vault && python3 gmail_watcher.py
```

### Watcher stops unexpectedly
- Check logs in `Logs/` folder
- Add error handling
- Use orchestrator with auto-restart
- Monitor with watchdog script

## Best Practices

1. **Test manually first** before scheduling
2. **Use absolute paths** in scheduled tasks
3. **Log everything** to track issues
4. **Set up notifications** for failures
5. **Monitor resource usage** (CPU, memory)
6. **Stagger start times** to avoid conflicts
7. **Use orchestrator** for complex setups

## Next Steps

- Set up email notifications for failures
- Create health check script
- Monitor watcher uptime
- Optimize check intervals
- Add auto-restart on failure

---
*Part of Silver Tier AI Employee implementation*
