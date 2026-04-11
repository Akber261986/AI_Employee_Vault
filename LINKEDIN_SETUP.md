# LinkedIn Integration Setup Guide - Silver Tier

This guide walks you through setting up LinkedIn auto-posting for your AI Employee.

## Prerequisites
- LinkedIn account
- Python 3.13+ installed
- Playwright installed
- AI Employee vault set up

## Step 1: Install Dependencies

```bash
# Install Playwright (if not already installed)
pip install playwright

# Install Playwright browsers
playwright install chromium
```

## Step 2: Create LinkedIn Posts Folder

The folder structure is created automatically, but you can verify:

```
LinkedIn_Posts/
├── SAMPLE_linkedin_post.md  # Example post
└── Posted/                   # Completed posts
```

## Step 3: First Run (Login)

```bash
python linkedin_poster.py
```

**What happens:**
1. Chrome browser opens
2. LinkedIn loads
3. **Log in manually** if not already logged in
4. Session saved to `sessions/linkedin/`
5. Sample post will be published (if exists)

**Note:** You only need to log in once. The session is saved for future runs.

## Step 4: Create Your First Post

Create a file in `LinkedIn_Posts/` folder:

**Example: `LinkedIn_Posts/my_first_post.md`**

```markdown
---
type: linkedin_post
scheduled: manual
status: pending
---

🎉 Just completed my Bronze Tier AI Employee!

Built an autonomous assistant that:
✅ Monitors files automatically
✅ Processes tasks with AI
✅ Updates its own dashboard
✅ Maintains complete audit logs

This is the future of personal productivity!

#AI #Automation #Productivity
```

## Step 5: Post to LinkedIn

```bash
python linkedin_poster.py
```

The script will:
1. Find all `.md` files in `LinkedIn_Posts/`
2. Post each one to LinkedIn
3. Move posted files to `Posted/` folder
4. Log all activities

## Post Format

### Frontmatter (Optional)
```yaml
---
type: linkedin_post
scheduled: manual
status: pending
---
```

### Content
Everything after the frontmatter is posted to LinkedIn.

**Tips for engagement:**
- Use emojis (✅ 🚀 💡 🎯)
- Add hashtags (#AI #Tech)
- Ask questions
- Keep it under 1300 characters
- Use line breaks for readability

## Scheduling Posts

### Manual Posting
```bash
# Post all pending posts now
python linkedin_poster.py
```

### Scheduled Posting (Windows Task Scheduler)
See SCHEDULING_SETUP.md for automated daily posting.

### Scheduled Posting (Mac/Linux cron)
```bash
# Edit crontab
crontab -e

# Add line to post daily at 9 AM
0 9 * * * cd /path/to/vault && python linkedin_poster.py
```

## Content Ideas for Lead Generation

### 1. Project Updates
Share your AI Employee progress, features, achievements.

### 2. Industry Insights
Comment on AI trends, automation, productivity tools.

### 3. Problem-Solving
Share how you solved a technical challenge.

### 4. Tips & Tricks
Quick productivity hacks, coding tips, tool recommendations.

### 5. Case Studies
Real examples of how your AI Employee helped you.

### 6. Questions
Engage your network with thought-provoking questions.

## Best Practices

**Posting Frequency:**
- 3-5 times per week
- Consistent schedule (same time each day)
- Don't spam (max 1-2 posts per day)

**Content Quality:**
- Original content performs best
- Add personal insights
- Use relevant hashtags (3-5)
- Include call-to-action

**Engagement:**
- Respond to comments
- Engage with others' posts
- Build genuine connections

## Troubleshooting

### "Could not find Start a post button"
- LinkedIn UI may have changed
- Check if you're on the feed page
- Try refreshing the page

### "Login failed"
- Delete `sessions/linkedin/` folder
- Run script again
- Log in manually when prompted

### Post not appearing
- Check LinkedIn for rate limits
- Wait 10 seconds between posts
- Verify you're logged in

### "Session expired"
- Delete `sessions/linkedin/` folder
- Run script again to re-login

## Security Notes

⚠️ **Important:**
- Never commit `sessions/` folder to Git
- Already in `.gitignore`
- Keep your LinkedIn session secure
- Don't share session files

## Monitoring Results

**Check engagement:**
1. Visit your LinkedIn profile
2. View post analytics
3. Track likes, comments, shares
4. Adjust content strategy based on performance

**Log files:**
- `Logs/linkedin_poster.log` - Posting activity
- `Logs/events_YYYYMMDD.log` - Event log

## Integration with AI Employee

### Auto-generate posts
Create a task in `Needs_Action/`:

```markdown
---
type: content_creation
priority: normal
---

## Generate LinkedIn Post

Create a LinkedIn post about [topic].

Target audience: [describe]
Key message: [describe]
Call to action: [describe]
```

Run `/process-tasks` and AI will draft a post for you to review.

## Next Steps

- Create 5-7 posts in advance
- Schedule daily posting
- Monitor engagement
- Adjust content strategy
- Integrate with CRM (Gold Tier)

---
*Part of Silver Tier AI Employee implementation*
