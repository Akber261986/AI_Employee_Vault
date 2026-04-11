# WhatsApp Watcher - Silver Tier
# Monitors WhatsApp Web for messages with specific keywords

import time
import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/whatsapp_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('WhatsAppWatcher')


class WhatsAppWatcher:
    """Monitors WhatsApp Web for messages with keywords"""

    def __init__(self, vault_path: str, session_path: str, check_interval: int = 30):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'
        self.session_path = Path(session_path)
        self.check_interval = check_interval

        # Keywords to monitor (customize these)
        self.keywords = [
            'urgent', 'asap', 'help', 'invoice', 'payment',
            'quote', 'pricing', 'order', 'delivery', 'issue'
        ]

        self.processed_messages = set()

        # Ensure folders exist
        self.needs_action.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

        logger.info('WhatsApp Watcher initialized')
        logger.info(f'Monitoring keywords: {", ".join(self.keywords)}')

    def wait_for_whatsapp_ready(self, page):
        """Wait for WhatsApp Web to be fully loaded"""
        try:
            # Wait for chat list to appear (means logged in)
            page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
            logger.info('WhatsApp Web loaded successfully')
            return True
        except PlaywrightTimeout:
            logger.error('WhatsApp Web did not load. Please scan QR code.')
            return False

    def get_unread_chats(self, page):
        """Get all unread chats"""
        try:
            # Find all unread chat elements
            unread_chats = page.query_selector_all('[aria-label*="unread message"]')
            logger.info(f'Found {len(unread_chats)} unread chats')
            return unread_chats
        except Exception as e:
            logger.error(f'Error getting unread chats: {e}')
            return []

    def check_message_for_keywords(self, message_text: str) -> bool:
        """Check if message contains any monitored keywords"""
        message_lower = message_text.lower()
        for keyword in self.keywords:
            if keyword in message_lower:
                return True
        return False

    def extract_chat_info(self, page, chat_element):
        """Extract information from a chat"""
        try:
            # Click on the chat
            chat_element.click()
            time.sleep(1)

            # Get chat name
            chat_name_elem = page.query_selector('[data-testid="conversation-header"] span[dir="auto"]')
            chat_name = chat_name_elem.inner_text() if chat_name_elem else 'Unknown'

            # Get messages in the chat
            messages = page.query_selector_all('[data-testid="msg-container"]')

            # Get last few messages
            recent_messages = []
            for msg in messages[-5:]:  # Last 5 messages
                text_elem = msg.query_selector('span.selectable-text')
                if text_elem:
                    text = text_elem.inner_text()
                    recent_messages.append(text)

            return {
                'chat_name': chat_name,
                'messages': recent_messages,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f'Error extracting chat info: {e}')
            return None

    def create_task_file(self, chat_data):
        """Create a task file for WhatsApp message"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        chat_id = chat_data['chat_name'].replace(' ', '_')[:20]
        filename = f'WHATSAPP_{timestamp}_{chat_id}.md'
        filepath = self.needs_action / filename

        # Create message preview
        messages_preview = '\n'.join([f'- {msg}' for msg in chat_data['messages']])

        content = f"""---
type: whatsapp_message
chat_name: {chat_data['chat_name']}
received: {chat_data['timestamp']}
priority: high
status: pending
---

## New WhatsApp Message

An important WhatsApp message has been received and requires attention.

**Chat Details:**
- From: {chat_data['chat_name']}
- Time: {chat_data['timestamp']}
- Contains keywords: Yes

**Recent Messages:**
{messages_preview}

## Suggested Actions
- [ ] Read full conversation in WhatsApp
- [ ] Draft reply (requires approval)
- [ ] Take necessary action
- [ ] Mark as resolved when complete

## Notes
Add processing notes here.
"""

        filepath.write_text(content, encoding='utf-8')
        logger.info(f'Created task file: {filename}')

        # Log the event
        self._log_event(chat_data['chat_name'], filename)

        return filepath

    def _log_event(self, chat_name: str, task_file: str):
        """Log WhatsApp message detection event"""
        log_entry = f"{datetime.now().isoformat()} - WHATSAPP_DETECTED - From: {chat_name} | Task: {task_file}\n"
        log_file = self.logs / f'events_{datetime.now().strftime("%Y%m%d")}.log'

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def run(self):
        """Start the WhatsApp watcher"""
        logger.info('Starting WhatsApp Watcher...')
        logger.info(f'Session path: {self.session_path}')
        logger.info('Opening WhatsApp Web...')

        with sync_playwright() as p:
            # Launch browser with persistent context (saves login session)
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.session_path),
                headless=False,  # Must be False for WhatsApp Web
                args=['--no-sandbox']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Navigate to WhatsApp Web
            page.goto('https://web.whatsapp.com')
            logger.info('WhatsApp Web opened. Please scan QR code if needed.')

            # Wait for WhatsApp to be ready
            if not self.wait_for_whatsapp_ready(page):
                logger.error('Failed to load WhatsApp Web')
                browser.close()
                return

            logger.info(f'Monitoring WhatsApp every {self.check_interval} seconds')
            logger.info('Press Ctrl+C to stop')

            try:
                while True:
                    try:
                        # Get unread chats
                        unread_chats = self.get_unread_chats(page)

                        for chat in unread_chats:
                            # Extract chat info
                            chat_data = self.extract_chat_info(page, chat)

                            if chat_data:
                                # Check if any message contains keywords
                                has_keyword = any(
                                    self.check_message_for_keywords(msg)
                                    for msg in chat_data['messages']
                                )

                                if has_keyword:
                                    # Create unique ID for this chat
                                    chat_id = f"{chat_data['chat_name']}_{chat_data['timestamp']}"

                                    if chat_id not in self.processed_messages:
                                        self.create_task_file(chat_data)
                                        self.processed_messages.add(chat_id)

                        # Wait before next check
                        time.sleep(self.check_interval)

                    except Exception as e:
                        logger.error(f'Error in monitoring loop: {e}')
                        time.sleep(60)

            except KeyboardInterrupt:
                logger.info('WhatsApp Watcher stopped by user')
            finally:
                browser.close()


if __name__ == '__main__':
    # Get vault path
    vault_path = Path(__file__).parent

    # Session path for WhatsApp (stores login session)
    session_path = vault_path / 'sessions' / 'whatsapp'

    # Create and run watcher
    watcher = WhatsAppWatcher(
        vault_path=str(vault_path),
        session_path=str(session_path),
        check_interval=30  # Check every 30 seconds
    )

    watcher.run()
