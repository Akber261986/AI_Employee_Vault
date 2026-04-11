# Email MCP Server - Silver Tier
# Handles sending emails with approval workflow

import logging
from pathlib import Path
from datetime import datetime
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64

# Gmail API scopes (need send permission)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/email_mcp.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('EmailMCP')


class EmailMCP:
    """MCP Server for sending emails with approval workflow"""

    def __init__(self, vault_path: str, credentials_path: str):
        self.vault_path = Path(vault_path)
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.logs = self.vault_path / 'Logs'
        self.credentials_path = credentials_path
        self.token_path = self.vault_path / 'tokens' / 'gmail_token.pickle'
        self.service = None

        # Ensure folders exist
        self.pending_approval.mkdir(exist_ok=True)
        self.approved.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)
        (self.vault_path / 'tokens').mkdir(exist_ok=True)

        logger.info('Email MCP initialized')

    def authenticate(self):
        """Authenticate with Gmail API"""
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
                logger.info('Starting OAuth2 flow for email sending')
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials
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

    def create_message(self, to: str, subject: str, body: str):
        """Create an email message"""
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw}

    def send_email(self, to: str, subject: str, body: str):
        """Send an email via Gmail API"""
        try:
            message = self.create_message(to, subject, body)
            sent_message = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()

            logger.info(f'Email sent successfully. Message ID: {sent_message["id"]}')
            self._log_event(to, subject, 'sent')
            return True

        except HttpError as error:
            logger.error(f'Failed to send email: {error}')
            self._log_event(to, subject, 'failed')
            return False

    def create_approval_request(self, to: str, subject: str, body: str, context: str = ''):
        """Create an approval request for sending an email"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'EMAIL_APPROVAL_{timestamp}.md'
        filepath = self.pending_approval / filename

        content = f"""---
type: email_approval
action: send_email
to: {to}
subject: {subject}
created: {datetime.now().isoformat()}
status: pending
---

## Email Approval Required

An email is ready to be sent but requires your approval.

**Email Details:**
- To: {to}
- Subject: {subject}

**Email Body:**
```
{body}
```

**Context:**
{context if context else 'No additional context provided'}

## To Approve
Move this file to the `/Approved` folder.

## To Reject
Move this file to the `/Rejected` folder or delete it.

## Notes
- Email will only be sent after approval
- Check recipient and content carefully
- Add any notes below before approving

---
*Created by Email MCP Server*
"""

        filepath.write_text(content, encoding='utf-8')
        logger.info(f'Created approval request: {filename}')
        self._log_event(to, subject, 'approval_requested')

        return filepath

    def process_approved_emails(self):
        """Process all approved email requests"""
        approved_files = list(self.approved.glob('EMAIL_APPROVAL_*.md'))

        if not approved_files:
            logger.info('No approved emails to process')
            return

        logger.info(f'Processing {len(approved_files)} approved emails')

        for filepath in approved_files:
            try:
                # Parse the approval file
                content = filepath.read_text(encoding='utf-8')

                # Extract email details from frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = {}
                        for line in parts[1].strip().split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                frontmatter[key.strip()] = value.strip()

                        # Extract body from content
                        body_start = content.find('```', content.find('**Email Body:**'))
                        body_end = content.find('```', body_start + 3)
                        body = content[body_start + 3:body_end].strip()

                        # Send the email
                        success = self.send_email(
                            to=frontmatter.get('to', ''),
                            subject=frontmatter.get('subject', ''),
                            body=body
                        )

                        if success:
                            # Move to Done folder
                            done_folder = self.vault_path / 'Done'
                            done_folder.mkdir(exist_ok=True)
                            new_path = done_folder / f'SENT_{filepath.name}'
                            filepath.rename(new_path)
                            logger.info(f'Email sent and moved to Done: {filepath.name}')
                        else:
                            logger.error(f'Failed to send email: {filepath.name}')

            except Exception as e:
                logger.error(f'Error processing approval file {filepath}: {e}')

    def _log_event(self, to: str, subject: str, status: str):
        """Log email event"""
        log_entry = f"{datetime.now().isoformat()} - EMAIL_{status.upper()} - To: {to} | Subject: {subject}\n"
        log_file = self.logs / f'events_{datetime.now().strftime("%Y%m%d")}.log'

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)


# Example usage functions
def send_email_with_approval(to: str, subject: str, body: str, context: str = ''):
    """Helper function to create an email approval request"""
    vault_path = Path(__file__).parent
    credentials_path = vault_path / 'credentials' / 'gmail_credentials.json'

    mcp = EmailMCP(
        vault_path=str(vault_path),
        credentials_path=str(credentials_path)
    )

    return mcp.create_approval_request(to, subject, body, context)


def process_approved_emails():
    """Helper function to process all approved emails"""
    vault_path = Path(__file__).parent
    credentials_path = vault_path / 'credentials' / 'gmail_credentials.json'

    mcp = EmailMCP(
        vault_path=str(vault_path),
        credentials_path=str(credentials_path)
    )

    if mcp.authenticate():
        mcp.process_approved_emails()
    else:
        logger.error('Authentication failed')


if __name__ == '__main__':
    # Process approved emails
    process_approved_emails()
