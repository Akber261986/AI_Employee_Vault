You are updating the AI Employee Dashboard.

## Steps

1. **Count Tasks**
   - Count .md files in /Needs_Action (pending tasks)
   - Count .md files in /Done modified today (completed today)
   - Count .md files in /Plans (active projects)

2. **Read Current Dashboard**
   - Read Dashboard.md
   - Preserve the structure
   - Update only the stats and activity sections

3. **Update Stats**
   - Update "Pending Tasks" count
   - Update "Completed Today" count
   - Update "Active Projects" count
   - Update "last_updated" timestamp

4. **Add Recent Activity**
   - Keep last 10 activity entries
   - Add new entries at the top
   - Format: `- [YYYY-MM-DD HH:MM] Activity description`

5. **Save Dashboard**
   - Write updated content back to Dashboard.md
   - Ensure proper markdown formatting

## Output Format

Provide a brief summary:
```
Dashboard updated:
- Pending: X tasks
- Completed today: X tasks
- Active projects: X
```

Now update the Dashboard.md file.
