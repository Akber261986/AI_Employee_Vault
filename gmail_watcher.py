# Gmail Watcher - Silver Tier
# Monitors Gmail inbox for important/unread emails and creates tasks

import time
import logging
import pickle
import os.path
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/gmail_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('GmailWatcher')


class GmailWatcher:
    """Monitors Gmail inbox for important/unread emails"""

    def __init__(self, vault_path: str, credentials_path: str, check_interval: int = 300):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'
        self.credentials_path = credentials_path
        self.token_path = self.vault_path / 'tokens' / 'gmail_token.pickle'
        self.check_interval = check_interval  # 5 minutes default
        self.processed_ids = set()
        self.service = None

        # Ensure folders exist
        self.needs_action.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)
        (self.vault_path / 'tokens').mkdir(exist_ok=True)

        logger.info('Gmail Watcher initialized')

    def authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        creds = None

        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info('Refreshing expired credentials')
                creds.refresh(Request())
            else:
                logger.info('Starting OAuth2 flow - browser will open')
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
            logger.info('Credentials saved')

        try:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info('Gmail API service created successfully')
            return True
        except HttpError as error:
            logger.error(f'Failed to create Gmail service: {error}')
            return False

    def get_unread_important_emails(self):
        """Fetch unread important emails from inbox"""
        try:
            # Query for unread important emails
            query = 'is:unread is:important in:inbox'
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=10
            ).execute()

            messages = results.get('messages', [])
            new_messages = [m for m in messages if m['id'] not in self.processed_ids]

            logger.info(f'Found {len(new_messages)} new important emails')
            return new_messages

        except HttpError as error:
            logger.error(f'Error fetching emails: {error}')
            return []

    def get_message_details(self, message_id):
        """Get full details of an email message"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            # Extract headers
            headers = {h['name']: h['value']
                      for h in message['payload']['headers']}

            # Extract body
            body = self._get_message_body(message['payload'])

            return {
                'id': message_id,
                'from': headers.get('From', 'Unknown'),
                'to': headers.get('To', 'Unknown'),
                'subject': headers.get('Subject', 'No Subject'),
                'date': headers.get('Date', 'Unknown'),
                'snippet': message.get('snippet', ''),
                'body': body
            }

        except HttpError as error:
            logger.error(f'Error getting message details: {error}')
            return None

    def _get_message_body(self, payload):
        """Extract email body from payload"""
        body = ''

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        break
        elif 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(
                payload['body']['data']
            ).decode('utf-8')

        return body[:500]  # Limit to 500 chars

    def create_task_file(self, email_data):
        """Create a task file in Needs_Action folder"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'EMAIL_{timestamp}_{email_data["id"][:8]}.md'
        filepath = self.needs_action / filename

        content = f"""---
type: email
email_id: {email_data['id']}
from: {email_data['from']}
subject: {email_data['subject']}
received: {datetime.now().isoformat()}
priority: high
status: pending
---

## New Important Email

An important email has been received and requires attention.

**Email Details:**
- From: {email_data['from']}
- To: {email_data['to']}
- Subject: {email_data['subject']}
- Date: {email_data['date']}

**Preview:**
{email_data['snippet']}

**Body (first 500 chars):**
```
{email_data['body']}
```

## Suggested Actions
- [ ] Read full email
- [ ] Draft reply (requires approval)
- [ ] Forward if needed
- [ ] Archive after processing

## Notes
Add processing notes here.
"""

        filepath.write_text(content, encoding='utf-8')
        logger.info(f'Created task file: {filename}')

        # Log the event
        self._log_event(email_data['from'], email_data['subject'], filename)

        return filepath

    def _log_event(self, sender: str, subject: str, task_file: str):
        """Log email detection event"""
        log_entry = f"{datetime.now().isoformat()} - EMAIL_DETECTED - From: {sender} | Subject: {subject} | Task: {task_file}\n"
        log_file = self.logs / f'events_{datetime.now().strftime("%Y%m%d")}.log'

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def run(self):
        """Start the Gmail watcher"""
        logger.info('Starting Gmail Watcher...')

        # Authenticate first
        if not self.authenticate():
            logger.error('Authentication failed. Exiting.')
            return

        logger.info(f'Monitoring Gmail inbox every {self.check_interval} seconds')
        logger.info('Press Ctrl+C to stop')

        try:
            while True:
                try:
                    # Check for new emails
                    messages = self.get_unread_important_emails()

                    for message in messages:
                        email_data = self.get_message_details(message['id'])
                        if email_data:
                            self.create_task_file(email_data)
                            self.processed_ids.add(message['id'])

                    # Wait before next check
                    time.sleep(self.check_interval)

                except HttpError as error:
                    logger.error(f'API error: {error}')
                    time.sleep(60)  # Wait 1 minute on error

                except Exception as e:
                    logger.error(f'Unexpected error: {e}')
                    time.sleep(60)

        except KeyboardInterrupt:
            logger.info('Gmail Watcher stopped by user')


if __name__ == '__main__':
    # Get vault path (current directory)
    vault_path = Path(__file__).parent

    # Path to credentials file (you need to download this from Google Cloud Console)
    credentials_path = vault_path / 'credentials' / 'gmail_credentials.json'

    if not credentials_path.exists():
        print('ERROR: Gmail credentials not found!')
        print(f'Please download OAuth2 credentials and save to: {credentials_path}')
        print('See GMAIL_SETUP.md for instructions')
        exit(1)

    # Create and run watcher
    watcher = GmailWatcher(
        vault_path=str(vault_path),
        credentials_path=str(credentials_path),
        check_interval=300  # Check every 5 minutes
    )

    watcher.run()
