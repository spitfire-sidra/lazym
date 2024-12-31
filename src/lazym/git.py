import logging
import os
import re
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


def get_repo_info():
    """Get repository owner and name from git remote URL."""
    try:
        # Get the remote URL
        remote_url = os.popen('git config --get remote.origin.url').read().strip()
        
        # Handle SSH URL format: git@github.com:owner/repo.git
        ssh_pattern = r'git@github\.com:([^/]+)/([^.]+)\.git'
        # Handle HTTPS URL format: https://github.com/owner/repo.git
        https_pattern = r'https://github\.com/([^/]+)/([^.]+)\.git'
        
        for pattern in [ssh_pattern, https_pattern]:
            match = re.match(pattern, remote_url)
            if match:
                return match.group(1), match.group(2)
        logger.error(f'Could not parse repository info from remote URL: {remote_url}')
    except Exception as e:
        logger.error(f'Error getting repository info: {str(e)}')
    return None, None


def get_local_latest_tags(limit=5):
    return os.popen('git tag --sort=-creatordate').read().strip().split('\n')[:limit]


def get_repo_root():
    try:
        repo_root = os.popen('git rev-parse --show-toplevel').read().strip()
    except Exception:
        print("Error: Not a git repository or git is not installed.")
        sys.exit(1)
    return repo_root


def create_tag(tag):
    try:
        subprocess.run(
            ['git', 'tag', '-a', tag, '-m', tag], 
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to create tag {tag}: {e}")
        sys.exit(1)


def push_tag_to_origin(tag):
    try:
        subprocess.run(['git', 'push', 'origin', tag], check=True)
        print(f"Tag {tag} pushed to remote successfully.")
    except Exception as e:
        print(f"Failed to push tag {tag} to remote: {e}")
        sys.exit(1)
