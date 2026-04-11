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
            page.goto('https://www.linkedin.com/feed/')

            # Check if already logged in
            try:
                page.wait_for_selector('[data-test-id="feed-tab"]', timeout=5000)
                logger.info('Already logged in to LinkedIn')
                return True
            except PlaywrightTimeout:
                logger.info('Please log in to LinkedIn manually')
                # Wait for user to log in
                page.wait_for_selector('[data-test-id="feed-tab"]', timeout=120000)
                logger.info('Login successful')
                return True

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
            # Click "Start a post" button
            start_post_btn = page.query_selector('[data-test-id="share-box-open-btn"]')
            if not start_post_btn:
                start_post_btn = page.query_selector('button:has-text("Start a post")')

            if start_post_btn:
                start_post_btn.click()
                time.sleep(2)
            else:
                logger.error('Could not find "Start a post" button')
                return False

            # Wait for editor to appear
            editor = page.wait_for_selector('.ql-editor', timeout=10000)

            # Type the post content
            editor.fill(post_content)
            time.sleep(1)

            # Click Post button
            post_btn = page.query_selector('button:has-text("Post")')
            if post_btn:
                post_btn.click()
                logger.info('Post button clicked')
                time.sleep(3)
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
