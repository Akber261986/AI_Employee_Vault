# WhatsApp Sender - Silver Tier
# Sends WhatsApp messages with approval workflow

import time
import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/whatsapp_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('WhatsAppSender')


class WhatsAppSender:
    """Sends WhatsApp messages through WhatsApp Web with approval workflow"""

    def __init__(self, vault_path: str, session_path: str):
        self.vault_path = Path(vault_path)
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        self.rejected = self.vault_path / 'Rejected'
        self.logs = self.vault_path / 'Logs'
        self.session_path = Path(session_path)

        # Ensure folders exist
        self.pending_approval.mkdir(exist_ok=True)
        self.approved.mkdir(exist_ok=True)
        self.done.mkdir(exist_ok=True)
        self.rejected.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

        logger.info('WhatsApp Sender initialized')

    def wait_for_whatsapp_ready(self, page):
        """Wait for WhatsApp Web to be fully loaded"""
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
            logger.info('WhatsApp Web loaded successfully')
            return True
        except PlaywrightTimeout:
            logger.error('WhatsApp Web did not load')
            return False

    def parse_message_file(self, filepath: Path):
        """Parse a WhatsApp message file"""
        try:
            content = filepath.read_text(encoding='utf-8')

            # Extract frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = {}
                    for line in parts[1].strip().split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip()

                    # Get message content
                    message_content = parts[2].strip()

                    return {
                        'frontmatter': frontmatter,
                        'content': message_content,
                        'filepath': filepath
                    }

            return None

        except Exception as e:
            logger.error(f'Error parsing message file {filepath}: {e}')
            return None

    def search_and_open_chat(self, page, contact_name: str):
        """Search for and open a chat with a contact"""
        try:
            # Click search box
            search_selectors = [
                '[data-testid="chat-list-search"]',
                'div[contenteditable="true"][data-tab="3"]',
                '[title="Search input textbox"]'
            ]

            search_box = None
            for selector in search_selectors:
                try:
                    search_box = page.wait_for_selector(selector, timeout=5000)
                    if search_box:
                        logger.info(f'Found search box: {selector}')
                        break
                except PlaywrightTimeout:
                    continue

            if not search_box:
                logger.error('Could not find search box')
                return False

            # Type contact name
            search_box.click()
            time.sleep(1)
            search_box.fill(contact_name)
            logger.info(f'Searching for: {contact_name}')
            time.sleep(2)

            # Click on first result
            chat_selectors = [
                f'span[title="{contact_name}"]',
                '[data-testid="cell-frame-container"]',
                'div[role="listitem"]'
            ]

            chat_found = False
            for selector in chat_selectors:
                try:
                    chat = page.wait_for_selector(selector, timeout=5000)
                    if chat:
                        chat.click()
                        logger.info(f'Opened chat with: {contact_name}')
                        time.sleep(2)
                        chat_found = True
                        break
                except PlaywrightTimeout:
                    continue

            return chat_found

        except Exception as e:
            logger.error(f'Error opening chat: {e}')
            return False

    def send_message(self, page, message_text: str):
        """Send a message in the currently open chat"""
        try:
            # Find message input box
            input_selectors = [
                '[data-testid="conversation-compose-box-input"]',
                'div[contenteditable="true"][data-tab="10"]',
                'div[contenteditable="true"][role="textbox"]'
            ]

            input_box = None
            for selector in input_selectors:
                try:
                    input_box = page.wait_for_selector(selector, timeout=5000)
                    if input_box:
                        logger.info(f'Found input box: {selector}')
                        break
                except PlaywrightTimeout:
                    continue

            if not input_box:
                logger.error('Could not find message input box')
                return False

            # Type message
            input_box.click()
            time.sleep(1)

            # Handle multi-line messages
            lines = message_text.split('\n')
            for i, line in enumerate(lines):
                input_box.type(line)
                if i < len(lines) - 1:
                    page.keyboard.press('Shift+Enter')
                    time.sleep(0.2)

            logger.info('Message typed')
            time.sleep(1)

            # Click send button
            send_selectors = [
                '[data-testid="send"]',
                'button[aria-label="Send"]',
                'span[data-icon="send"]'
            ]

            send_btn = None
            for selector in send_selectors:
                try:
                    send_btn = page.wait_for_selector(selector, timeout=3000)
                    if send_btn:
                        logger.info(f'Found send button: {selector}')
                        break
                except PlaywrightTimeout:
                    continue

            if send_btn:
                send_btn.click()
                logger.info('Message sent')
                time.sleep(2)
                return True
            else:
                logger.error('Could not find send button')
                return False

        except Exception as e:
            logger.error(f'Error sending message: {e}')
            return False

    def move_to_done(self, filepath: Path):
        """Move sent message file to Done folder"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_name = f'SENT_{timestamp}_{filepath.name}'
            new_path = self.done / new_name

            filepath.rename(new_path)
            logger.info(f'Moved to Done: {new_name}')

            # Log the event
            self._log_event(filepath.name, 'sent')

        except Exception as e:
            logger.error(f'Error moving file: {e}')

    def _log_event(self, message_file: str, status: str):
        """Log WhatsApp sending event"""
        log_entry = f"{datetime.now().isoformat()} - WHATSAPP_{status.upper()} - Message: {message_file}\n"
        log_file = self.logs / f'events_{datetime.now().strftime("%Y%m%d")}.log'

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def get_approved_messages(self):
        """Get all approved WhatsApp messages"""
        messages = []
        for file in self.approved.glob('WHATSAPP_REPLY_*.md'):
            if file.is_file():
                messages.append(file)

        logger.info(f'Found {len(messages)} approved WhatsApp messages')
        return messages

    def run_once(self):
        """Run once to send all approved messages"""
        logger.info('Starting WhatsApp Sender (single run)...')

        # Get approved messages
        approved_messages = self.get_approved_messages()

        if not approved_messages:
            logger.info('No approved messages to send')
            return

        with sync_playwright() as p:
            # Launch browser with persistent context
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.session_path),
                headless=False,
                args=['--no-sandbox']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Navigate to WhatsApp Web
            page.goto('https://web.whatsapp.com')
            logger.info('WhatsApp Web opened')

            # Wait for WhatsApp to be ready
            if not self.wait_for_whatsapp_ready(page):
                logger.error('Failed to load WhatsApp Web')
                browser.close()
                return

            # Send each message
            for msg_file in approved_messages:
                logger.info(f'Processing: {msg_file.name}')

                msg_data = self.parse_message_file(msg_file)
                if not msg_data:
                    continue

                # Extract contact name and message
                contact = msg_data['frontmatter'].get('to', 'Unknown')
                message = msg_data['frontmatter'].get('message', '')

                if not message:
                    logger.error(f'No message content in {msg_file.name}')
                    continue

                # Open chat
                if not self.search_and_open_chat(page, contact):
                    logger.error(f'Could not open chat with {contact}')
                    continue

                # Send message
                if self.send_message(page, message):
                    logger.info(f'Successfully sent message to {contact}')
                    self.move_to_done(msg_file)
                    time.sleep(3)  # Wait between messages
                else:
                    logger.error(f'Failed to send message to {contact}')

            logger.info('WhatsApp sending complete')
            browser.close()


if __name__ == '__main__':
    # Get vault path
    vault_path = Path(__file__).parent

    # Session path for WhatsApp
    session_path = vault_path / 'sessions' / 'whatsapp'

    # Create and run sender
    sender = WhatsAppSender(
        vault_path=str(vault_path),
        session_path=str(session_path)
    )

    sender.run_once()
