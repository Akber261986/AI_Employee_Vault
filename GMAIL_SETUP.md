# Gmail API Setup Guide - Silver Tier

This guide walks you through setting up Gmail API access for your AI Employee.

## Prerequisites
- Google account (Gmail)
- Python 3.13+ installed
- AI Employee vault set up

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Project name: `AI-Employee-Gmail`
4. Click "Create"

## Step 2: Enable Gmail API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Gmail API"
4. Click "Enable"

## Step 3: Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: `AI Employee`
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Scopes: Skip for now
   - Test users: Add your Gmail address
   - Click "Save and Continue"

4. Back to "Create OAuth client ID":
   - Application type: **Desktop app**
   - Name: `AI Employee Gmail Watcher`
   - Click "Create"

5. Download the credentials:
   - Click "Download JSON"
   - Save as `gmail_credentials.json`

## Step 4: Install Credentials

1. Create credentials folder in your vault:
```bash
mkdir credentials
```

2. Move the downloaded file:
```bash
# Move gmail_credentials.json to credentials folder
move gmail_credentials.json credentials/
```

## Step 5: Install Dependencies

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Or use the project dependencies:
```bash
pip install -e .
```

## Step 6: First Run (Authentication)

```bash
python gmail_watcher.py
```

**What happens:**
1. Browser opens automatically
2. Sign in with your Google account
3. Grant permissions to the app
4. Token saved to `tokens/gmail_token.pickle`
5. Watcher starts monitoring

**Note:** You only need to authenticate once. The token is saved for future runs.

## Step 7: Verify It's Working

1. Send yourself a test email
2. Mark it as important (star it)
3. Keep it unread
4. Wait up to 5 minutes
5. Check `Needs_Action/` folder for new task file

## Configuration

### Change Check Interval

Edit `gmail_watcher.py`:
```python
check_interval=300  # 300 seconds = 5 minutes
```

### Customize Email Query

Edit the query in `get_unread_important_emails()`:
```python
# Current: unread + important
query = 'is:unread is:important in:inbox'

# Options:
query = 'is:unread in:inbox'  # All unread
query = 'is:unread from:client@example.com'  # From specific sender
query = 'is:unread subject:urgent'  # With keyword in subject
```

## Troubleshooting

### "credentials not found" error
- Ensure `credentials/gmail_credentials.json` exists
- Check the file path is correct

### "Authentication failed" error
- Delete `tokens/gmail_token.pickle`
- Run watcher again to re-authenticate

### "API not enabled" error
- Go to Google Cloud Console
- Enable Gmail API for your project

### No emails detected
- Check email is marked as important (starred)
- Check email is unread
- Wait 5 minutes (default check interval)
- Check `Logs/gmail_watcher.log` for errors

## Security Notes

⚠️ **Important:**
- Never commit `credentials/` folder to Git
- Never commit `tokens/` folder to Git
- These are already in `.gitignore`
- Keep your credentials secure

## Testing

Send yourself a test email:
1. From another account, email yourself
2. Mark as important (star)
3. Keep unread
4. Wait for watcher to detect it
5. Check `Needs_Action/` for task file

## Next Steps

Once Gmail watcher is working:
- Run `/process-tasks` to handle email tasks
- Set up Email MCP server for sending replies
- Configure approval workflow for email actions

---
*Part of Silver Tier AI Employee implementation*
