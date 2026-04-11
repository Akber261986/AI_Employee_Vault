# Master Orchestrator - Silver Tier
# Manages all watchers and periodic tasks

import subprocess
import time
import logging
from pathlib import Path
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Orchestrator')


class Orchestrator:
    """Manages all AI Employee watchers and tasks"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.processes = {}
        self.last_task_process = datetime.now()

    def start_watcher(self, name: str, script: str):
        """Start a watcher process"""
        try:
            proc = subprocess.Popen(
                [sys.executable, script],
                cwd=self.vault_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes[name] = {
                'process': proc,
                'script': script,
                'started': datetime.now()
            }
            logger.info(f'Started: {name} ({script})')
            return True
        except Exception as e:
            logger.error(f'Failed to start {name}: {e}')
            return False

    def check_process(self, name: str):
        """Check if a process is still running"""
        if name not in self.processes:
            return False

        proc = self.processes[name]['process']
        if proc.poll() is not None:
            # Process has stopped
            logger.warning(f'{name} has stopped. Exit code: {proc.returncode}')
            return False

        return True

    def restart_process(self, name: str):
        """Restart a stopped process"""
        if name in self.processes:
            script = self.processes[name]['script']
            logger.info(f'Restarting {name}...')
            del self.processes[name]
            return self.start_watcher(name, script)
        return False

    def run_periodic_task(self, script: str, description: str):
        """Run a one-time task"""
        try:
            logger.info(f'Running periodic task: {description}')
            result = subprocess.run(
                [sys.executable, script],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info(f'{description} completed successfully')
            else:
                logger.error(f'{description} failed: {result.stderr}')

            return result.returncode == 0

        except subprocess.TimeoutExpired:
            logger.error(f'{description} timed out')
            return False
        except Exception as e:
            logger.error(f'Error running {description}: {e}')
            return False

    def run(self):
        """Main orchestrator loop"""
        logger.info('='*50)
        logger.info('AI Employee Orchestrator Starting')
        logger.info('='*50)

        # Start continuous watchers
        watchers = [
            ('Gmail Watcher', 'gmail_watcher.py'),
            ('File System Watcher', 'filesystem_watcher.py'),
        ]

        for name, script in watchers:
            script_path = self.vault_path / script
            if script_path.exists():
                self.start_watcher(name, script)
            else:
                logger.warning(f'Skipping {name}: {script} not found')

        logger.info('All watchers started')
        logger.info('Press Ctrl+C to stop')

        try:
            while True:
                # Check all processes
                for name in list(self.processes.keys()):
                    if not self.check_process(name):
                        logger.warning(f'{name} stopped, restarting...')
                        self.restart_process(name)

                # Run periodic tasks every hour
                now = datetime.now()
                if (now - self.last_task_process).seconds >= 3600:
                    logger.info('Running periodic tasks...')

                    # Process approved emails
                    self.run_periodic_task(
                        'email_mcp.py',
                        'Email Processor'
                    )

                    self.last_task_process = now

                # Wait before next check
                time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            logger.info('Stopping orchestrator...')
            self.stop_all()

    def stop_all(self):
        """Stop all running processes"""
        for name, data in self.processes.items():
            logger.info(f'Stopping {name}...')
            data['process'].terminate()
            try:
                data['process'].wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f'{name} did not stop gracefully, killing...')
                data['process'].kill()

        logger.info('All processes stopped')


if __name__ == '__main__':
    vault_path = Path(__file__).parent

    orchestrator = Orchestrator(str(vault_path))
    orchestrator.run()
