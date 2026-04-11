# File System Watcher - Bronze Tier
# Monitors a drop folder and creates action files in Needs_Action

import time
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('FileSystemWatcher')

class DropFolderHandler(FileSystemEventHandler):
    """Handles new files dropped into the Inbox folder"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'

        # Ensure folders exist
        self.inbox.mkdir(exist_ok=True)
        self.needs_action.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)

        logger.info(f'Initialized watcher for: {self.inbox}')

    def on_created(self, event):
        """Called when a new file is created in the watched folder"""
        if event.is_directory:
            return

        try:
            source = Path(event.src_path)

            # Skip temporary files and hidden files
            if source.name.startswith('.') or source.name.startswith('~'):
                return

            # Wait a moment to ensure file is fully written
            time.sleep(1)

            # Create action file in Needs_Action
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            action_file = self.needs_action / f'FILE_{timestamp}_{source.stem}.md'

            # Create metadata file
            content = f"""---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size} bytes
received: {datetime.now().isoformat()}
priority: normal
status: pending
---

## New File Detected

A new file has been dropped into the Inbox folder and requires processing.

**File Details:**
- Name: {source.name}
- Size: {source.stat().st_size} bytes
- Type: {source.suffix}
- Location: Inbox/{source.name}

## Suggested Actions
- [ ] Review file content
- [ ] Determine appropriate action
- [ ] Process or categorize
- [ ] Move to Done when complete

## Notes
Add any processing notes here.
"""

            action_file.write_text(content, encoding='utf-8')
            logger.info(f'Created action file: {action_file.name} for {source.name}')

            # Log the event
            self._log_event(source.name, action_file.name)

        except Exception as e:
            logger.error(f'Error processing file {event.src_path}: {e}')

    def _log_event(self, source_file: str, action_file: str):
        """Log the file detection event"""
        log_entry = f"{datetime.now().isoformat()} - File detected: {source_file} -> {action_file}\n"
        log_file = self.logs / f'events_{datetime.now().strftime("%Y%m%d")}.log'

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

def run_watcher(vault_path: str):
    """Start the file system watcher"""
    vault = Path(vault_path)
    inbox = vault / 'Inbox'

    # Ensure inbox exists
    inbox.mkdir(exist_ok=True)

    event_handler = DropFolderHandler(vault_path)
    observer = Observer()
    observer.schedule(event_handler, str(inbox), recursive=False)
    observer.start()

    logger.info(f'File System Watcher started. Monitoring: {inbox}')
    logger.info('Press Ctrl+C to stop')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info('Watcher stopped by user')

    observer.join()

if __name__ == '__main__':
    # Get the vault path (current directory)
    vault_path = Path(__file__).parent
    run_watcher(str(vault_path))
