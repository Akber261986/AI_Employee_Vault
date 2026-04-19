# LinkedIn Integration - Silver Tier
# Auto-posts business content to LinkedIn for lead generation

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
        logging.FileHandler('Logs/linkedin_poster.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('LinkedInPoster')


class LinkedInPoster:
    """Automatically posts content to LinkedIn"""

    def __init__(self, vault_path: str, session_path: str):
        self.vault_path = Path(vault_path)
        self.posts_queue = self.vault_path / 'LinkedIn_Posts'
        self.posted = self.vault_path / 'LinkedIn_Posts' / 'Posted'
        self.logs = self.vault_path / 'Logs'
        self.session_path = Path(session_path)

        # Ensure folders exist
        self.posts_queue.mkdir(exist_ok=True)
        self.posted.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

        logger.info('LinkedIn Poster initialized')

    def login_to_linkedin(self, page):
        """Navigate to LinkedIn and wait for login"""
        try:
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded')
            time.sleep(3)

            # Check if we're on the feed page (already logged in)
            current_url = page.url
            if '/feed/' in current_url:
                logger.info('Already logged in to LinkedIn')
                return True

            # Not logged in - wait for user to login
            logger.info('=' * 60)
            logger.info('PLEASE LOG IN TO LINKEDIN IN THE BROWSER WINDOW')
            logger.info('DO NOT CLOSE THE BROWSER!')
            logger.info('After logging in, you will be redirected to the feed.')
            logger.info('The script will automatically continue...')
            logger.info('=' * 60)

            # Wait for URL to contain /feed/ (indicates successful login)
            max_wait = 300  # 5 minutes
            start_time = time.time()

            while time.time() - start_time < max_wait:
                current_url = page.url
                if '/feed/' in current_url:
                    logger.info('Login successful! Session saved for future runs.')
                    time.sleep(2)  # Give page time to fully load
                    return True
                time.sleep(2)

            logger.error('Login timeout - please try again')
            return False

        except Exception as e:
            logger.error(f'Error during LinkedIn login: {e}')
            return False

    def get_pending_posts(self):
        """Get all pending posts from queue"""
        posts = []
        for file in self.posts_queue.glob('*.md'):
            if file.is_file() and file.parent == self.posts_queue:
                posts.append(file)

        logger.info(f'Found {len(posts)} pending posts')
        return posts

    def parse_post_file(self, filepath: Path):
        """Parse a post file and extract content"""
        try:
            content = filepath.read_text(encoding='utf-8')

            # Extract frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    # Parse frontmatter (simple key: value parsing)
                    frontmatter = {}
                    for line in parts[1].strip().split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip()

                    # Get post content (everything after second ---)
                    post_content = parts[2].strip()

                    return {
                        'frontmatter': frontmatter,
                        'content': post_content,
                        'filepath': filepath
                    }

            # If no frontmatter, use entire content
            return {
                'frontmatter': {},
                'content': content.strip(),
                'filepath': filepath
            }

        except Exception as e:
            logger.error(f'Error parsing post file {filepath}: {e}')
            return None

    def create_linkedin_post(self, page, post_content: str):
        """Create a post on LinkedIn"""
        try:
            # Wait for page to fully load
            time.sleep(5)

            # Try multiple selectors for "Start a post" button
            start_post_selectors = [
                'button:has-text("Start a post")',
                'button:has-text("start a post")',
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-test-id="share-box-open-btn"]',
                '.artdeco-button.share-box-feed-entry__trigger',
                'button[aria-label*="Start a post"]',
                'button[aria-label*="start a post"]',
                '.share-box-feed-entry',
                'div.share-box-feed-entry__trigger',
                'button.artdeco-button--tertiary',
                'button >> text=/start a post/i'
            ]

            start_post_btn = None
            for selector in start_post_selectors:
                try:
                    start_post_btn = page.wait_for_selector(selector, timeout=5000, state='visible')
                    if start_post_btn and start_post_btn.is_visible():
                        logger.info(f'Found start post button: {selector}')
                        break
                except PlaywrightTimeout:
                    continue
                except Exception as e:
                    logger.debug(f'Selector {selector} failed: {e}')
                    continue

            if not start_post_btn:
                logger.error('Could not find "Start a post" button with any selector')
                # Take screenshot for debugging
                page.screenshot(path='Logs/linkedin_error.png')
                logger.info('Screenshot saved to Logs/linkedin_error.png')

                # Try to log all buttons on the page for debugging
                try:
                    buttons = page.query_selector_all('button')
                    logger.info(f'Found {len(buttons)} buttons on page')
                    for i, btn in enumerate(buttons[:10]):  # Log first 10 buttons
                        text = btn.inner_text()
                        aria_label = btn.get_attribute('aria-label')
                        logger.debug(f'Button {i}: text="{text}", aria-label="{aria_label}"')
                except Exception as e:
                    logger.debug(f'Could not enumerate buttons: {e}')

                return False

            # Click the button
            start_post_btn.click()
            logger.info('Clicked "Start a post" button')
            time.sleep(4)

            # Wait for editor to appear - try multiple selectors
            editor_selectors = [
                'div[contenteditable="true"]',
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
                '.ql-editor',
                'div[role="textbox"]',
                '[contenteditable="true"]',
                '.share-creation-state__text-editor',
                'div.ql-editor.ql-blank',
                '[data-placeholder*="share"]',
                'div[aria-label*="share"]',
                'div.editor-content'
            ]

            editor = None
            for selector in editor_selectors:
                try:
                    editor = page.wait_for_selector(selector, timeout=8000, state='visible')
                    if editor and editor.is_visible():
                        logger.info(f'Found editor: {selector}')
                        break
                except PlaywrightTimeout:
                    continue
                except Exception as e:
                    logger.debug(f'Editor selector {selector} failed: {e}')
                    continue

            if not editor:
                logger.error('Could not find post editor')
                # Take screenshot for debugging
                page.screenshot(path='Logs/linkedin_editor_error.png')
                logger.info('Screenshot saved to Logs/linkedin_editor_error.png')

                # Try to log contenteditable elements for debugging
                try:
                    editables = page.query_selector_all('[contenteditable="true"]')
                    logger.info(f'Found {len(editables)} contenteditable elements')
                    for i, elem in enumerate(editables[:5]):
                        classes = elem.get_attribute('class')
                        role = elem.get_attribute('role')
                        logger.debug(f'Editable {i}: class="{classes}", role="{role}"')
                except Exception as e:
                    logger.debug(f'Could not enumerate editables: {e}')

                return False

            # Type the post content
            editor.click()
            time.sleep(1)
            editor.fill(post_content)
            logger.info('Post content entered')
            time.sleep(2)

            # Click Post button - try multiple selectors
            post_btn_selectors = [
                'button.share-actions__primary-action',
                'button[aria-label*="Post"]',
                'button:has-text("Post")',
                '.share-actions__primary-action'
            ]

            post_btn = None
            for selector in post_btn_selectors:
                try:
                    post_btn = page.wait_for_selector(selector, timeout=3000)
                    if post_btn and post_btn.is_enabled():
                        logger.info(f'Found post button: {selector}')
                        break
                except PlaywrightTimeout:
                    continue

            if post_btn:
                post_btn.click()
                logger.info('Post button clicked')
                time.sleep(5)
                return True
            else:
                logger.error('Could not find Post button')
                return False

        except Exception as e:
            logger.error(f'Error creating LinkedIn post: {e}')
            return False

    def move_to_posted(self, filepath: Path):
        """Move posted file to Posted folder"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_name = f'POSTED_{timestamp}_{filepath.name}'
            new_path = self.posted / new_name

            filepath.rename(new_path)
            logger.info(f'Moved to Posted: {new_name}')

            # Log the event
            self._log_event(filepath.name, 'posted')

        except Exception as e:
            logger.error(f'Error moving file: {e}')

    def _log_event(self, post_name: str, status: str):
        """Log LinkedIn posting event"""
        log_entry = f"{datetime.now().isoformat()} - LINKEDIN_{status.upper()} - Post: {post_name}\n"
        log_file = self.logs / f'events_{datetime.now().strftime("%Y%m%d")}.log'

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def run_once(self):
        """Run once to post all pending posts"""
        logger.info('Starting LinkedIn Poster (single run)...')

        with sync_playwright() as p:
            # Launch browser with persistent context
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.session_path),
                headless=False,
                args=['--no-sandbox']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Login to LinkedIn
            if not self.login_to_linkedin(page):
                logger.error('Failed to login to LinkedIn')
                browser.close()
                return

            # Get pending posts
            pending_posts = self.get_pending_posts()

            if not pending_posts:
                logger.info('No pending posts to publish')
                browser.close()
                return

            # Post each one
            for post_file in pending_posts:
                logger.info(f'Processing: {post_file.name}')

                post_data = self.parse_post_file(post_file)
                if not post_data:
                    continue

                # Create the post
                success = self.create_linkedin_post(page, post_data['content'])

                if success:
                    logger.info(f'Successfully posted: {post_file.name}')
                    self.move_to_posted(post_file)

                    # Wait between posts to avoid rate limiting
                    time.sleep(10)
                else:
                    logger.error(f'Failed to post: {post_file.name}')

            logger.info('LinkedIn posting complete')
            browser.close()


def create_sample_post(vault_path: Path):
    """Create a sample LinkedIn post file"""
    posts_folder = vault_path / 'LinkedIn_Posts'
    posts_folder.mkdir(exist_ok=True)

    sample_file = posts_folder / 'SAMPLE_linkedin_post.md'

    if not sample_file.exists():
        content = """---
type: linkedin_post
scheduled: manual
status: pending
---

🚀 Excited to share my latest project: Building an AI Employee!

I've been working on an autonomous AI assistant that:
✅ Monitors emails and messages 24/7
✅ Processes tasks automatically
✅ Maintains its own dashboard
✅ Follows defined behavior rules

This is part of the Personal AI Employee Hackathon, where we're building "Digital FTEs" (Full-Time Equivalents) that work alongside us.

The future of work is here, and it's about augmentation, not replacement.

What are your thoughts on AI assistants in the workplace?

#AI #Automation #FutureOfWork #Innovation #Productivity
"""
        sample_file.write_text(content, encoding='utf-8')
        logger.info(f'Created sample post: {sample_file}')


if __name__ == '__main__':
    # Get vault path
    vault_path = Path(__file__).parent

    # Session path for LinkedIn
    session_path = vault_path / 'sessions' / 'linkedin'

    # Create sample post if none exist
    create_sample_post(vault_path)

    # Create and run poster
    poster = LinkedInPoster(
        vault_path=str(vault_path),
        session_path=str(session_path)
    )

    poster.run_once()
