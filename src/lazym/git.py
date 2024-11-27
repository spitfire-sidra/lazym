import logging
import os
import subprocess
import sys
from pathlib import Path

import pyperclip

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def clean_diff(diff: str) -> str:
    # remove unnecessary informations
    return '\n'.join([
        l for l in diff.split('\n')
        if not l.startswith('index ')
    ])


def get_diff(repo_root):
    current_dir = os.getcwd()
    os.chdir(repo_root)
    try:
        cmd = ['git', 'diff', '--staged', '--minimal', '--no-color']
        output = subprocess.run(cmd, capture_output=True, text=True)
        return clean_diff(output.stdout)
    except Exception as e:
        logger.error(f'Error: Unable to get git diff. {str(e)}')
        sys.exit(1)
    finally:
        os.chdir(current_dir)


def has_commit_history(repo_root):
    return Path(f'{repo_root}/.git/logs/HEAD').exists()


def commit(msg):
    result = subprocess.run(['git', 'commit', '-m', msg], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f'Commit failed: {result.stderr.strip()}')
        pyperclip.copy(msg)
        logger.info('Commit message copied to clipboard')
    else:
        logger.info('Commit successful')
    return result.returncode == 0
