# Gmail API Setup - Step by Step Guide

## Step 1: Create Google Cloud Project (5 minutes)

1. **Go to Google Cloud Console**
   - Open: https://console.cloud.google.com/
   - Sign in with your Gmail account

2. **Create New Project**
   - Click "Select a project" dropdown (top left)
   - Click "NEW PROJECT"
   - Project name: `AI-Employee-Gmail`
   - Click "CREATE"
   - Wait for project creation (30 seconds)

3. **Select Your Project**
   - Click "Select a project" again
   - Choose "AI-Employee-Gmail"

## Step 2: Enable Gmail API (2 minutes)

1. **Open API Library**
   - In left menu: "APIs & Services" → "Library"
   - Or direct link: https://console.cloud.google.com/apis/library

2. **Find Gmail API**
   - Search box: Type "Gmail API"
   - Click "Gmail API" from results

3. **Enable It**
   - Click blue "ENABLE" button
   - Wait for activation (10 seconds)

## Step 3: Configure OAuth Consent Screen (3 minutes)

1. **Go to OAuth Consent**
   - Left menu: "APIs & Services" → "OAuth consent screen"
   - Or: https://console.cloud.google.com/apis/credentials/consent

2. **Choose User Type**
   - Select: ⚪ **External**
   - Click "CREATE"

3. **Fill App Information**
   - App name: `AI Employee`
   - User support email: (your email - auto-filled)
   - App logo: (skip)
   - App domain: (skip)
   - Developer contact: (your email)
   - Click "SAVE AND CONTINUE"

4. **Scopes Page**
   - Click "SAVE AND CONTINUE" (no changes needed)

5. **Test Users**
   - Click "+ ADD USERS"
   - Enter your Gmail address
   - Click "ADD"
   - Click "SAVE AND CONTINUE"

6. **Summary**
   - Review and click "BACK TO DASHBOARD"

## Step 4: Create OAuth Credentials (2 minutes)

1. **Go to Credentials**
   - Left menu: "APIs & Services" → "Credentials"
   - Or: https://console.cloud.google.com/apis/credentials

2. **Create Credentials**
   - Click "+ CREATE CREDENTIALS" (top)
   - Select "OAuth client ID"

3. **Configure OAuth Client**
   - Application type: **Desktop app**
   - Name: `AI Employee Gmail Watcher`
   - Click "CREATE"

4. **Download Credentials**
   - Pop-up appears with client ID and secret
   - Click "DOWNLOAD JSON"
   - File downloads as `client_secret_XXXXX.json`

## Step 5: Install Credentials in Your Vault

1. **Create credentials folder**
   ```bash
   mkdir credentials
   ```

2. **Move the downloaded file**
   - Find the downloaded file (usually in Downloads/)
   - Rename it to: `gmail_credentials.json`
   - Move it to: `AI_Employee_Vault/credentials/gmail_credentials.json`

   **Windows:**
   ```cmd
   move "%USERPROFILE%\Downloads\client_secret_*.json" credentials\gmail_credentials.json
   ```

   **Mac/Linux:**
   ```bash
   mv ~/Downloads/client_secret_*.json credentials/gmail_credentials.json
   ```

3. **Verify it's there**
   ```bash
   ls credentials/
   # Should show: gmail_credentials.json
   ```

## Step 6: Install Python Dependencies

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Or use project dependencies:
```bash
pip install -e .
```

## Step 7: First Run - Authenticate

```bash
python gmail_watcher.py
```

**What happens:**
1. ✅ Script starts
2. 🌐 Browser opens automatically
3. 🔐 Google login page appears
4. ⚠️ Warning: "Google hasn't verified this app"
   - Click "Advanced"
   - Click "Go to AI Employee (unsafe)" - it's YOUR app, it's safe!
5. ✅ Grant permissions:
   - ✅ Read your email messages
   - ✅ Send email on your behalf
   - Click "Continue"
6. 💾 Token saved to `tokens/gmail_token.pickle`
7. 🎉 Watcher starts monitoring!

**You'll see:**
```
2026-04-11 - GmailWatcher - INFO - Gmail Watcher initialized
2026-04-11 - GmailWatcher - INFO - Gmail API service created successfully
2026-04-11 - GmailWatcher - INFO - Monitoring Gmail inbox every 300 seconds
2026-04-11 - GmailWatcher - INFO - Press Ctrl+C to stop
```

## Step 8: Test It

1. **Send yourself a test email**
   - From another account (or same account)
   - Subject: "Test for AI Employee"
   - Mark it as **Important** (star it)
   - Keep it **unread**

2. **Wait up to 5 minutes**
   - Watcher checks every 5 minutes
   - Watch the terminal for activity

3. **Check for task file**
   ```bash
   ls Needs_Action/
   # Should see: EMAIL_YYYYMMDD_HHMMSS_XXXXXXXX.md
   ```

4. **Process the email**
   ```bash
   /process-emails
   ```

## Troubleshooting

**"credentials not found" error:**
- Check file exists: `ls credentials/gmail_credentials.json`
- Check filename is exactly: `gmail_credentials.json`

**"API not enabled" error:**
- Go back to Step 2
- Make sure Gmail API is enabled

**Browser doesn't open:**
- Check Python version: `python --version` (need 3.13+)
- Try running again

**"Access blocked" error:**
- You need to add yourself as a test user (Step 3.5)
- Go to OAuth consent screen → Test users → Add your email

## Success Indicators

✅ Browser opened and you logged in
✅ Permissions granted
✅ Token file created: `tokens/gmail_token.pickle`
✅ Watcher running without errors
✅ Test email detected and task created

## Next Steps

Once Gmail is working:
- Set up Email MCP for sending replies
- Configure WhatsApp watcher
- Set up LinkedIn posting
- Configure scheduling

---
*You only need to authenticate once. Future runs will use the saved token.*
