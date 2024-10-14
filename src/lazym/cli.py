import os
import shutil
import sys


def _get_repo_root():
    try:
        repo_root = os.popen('git rev-parse --show-toplevel').read().strip()
    except Exception:
        print("Error: Not a git repository or git is not installed.")
        sys.exit(1)
    return repo_root

def install_hook():
    # Get the current git repository root
    repo_root = _get_repo_root()

    # Define source and destination paths
    source_path = os.path.join(os.path.dirname(__file__), 'prepare-commit-msg')
    dest_path = os.path.join(repo_root, '.git', 'hooks', 'prepare-commit-msg')

    # Copy the hook file
    try:
        shutil.copy2(source_path, dest_path)
        os.chmod(dest_path, 0o755)  # Make the script executable
        print(f"Successfully installed prepare-commit-msg hook to {dest_path}")
    except Exception as e:
        print(f"Error installing hook: {str(e)}")
        sys.exit(1)

def uninstall_hook():
    # Get the current git repository root
    repo_root = _get_repo_root()

    # Define the hook path
    hook_path = os.path.join(repo_root, '.git', 'hooks', 'prepare-commit-msg')

    # Remove the hook file
    try:
        if os.path.exists(hook_path):
            os.remove(hook_path)
            print(f"Successfully uninstalled prepare-commit-msg hook from {hook_path}")
        else:
            print("Hook not found. Nothing to uninstall.")
    except Exception as e:
        print(f"Error uninstalling hook: {str(e)}")
        sys.exit(1)


def generate_commit_message(summary):
    from .chain import generate_commit_message
    from .git import get_diff
    from .prompt import PROMPT

    repo_root = _get_repo_root()
    diff = get_diff(repo_root)
    if not diff:
        print("No changes to commit.")
        sys.exit(0)
    
    prompt_with_summary = f"{PROMPT}\n\nAdditional context: {summary}"
    commit_message = generate_commit_message(prompt_with_summary, diff)
    print(f"Generated commit message:\n\n{commit_message}")


def main():
    if len(sys.argv) < 2:
        print("Usage: lazym <command> <args>")
        print("Available commands:")
        print("\tinstall - Install the prepare-commit-msg hook")
        print("\tuninstall - Uninstall the prepare-commit-msg hook")
        print("\tci - Generate commit message with additional context")
        sys.exit(0)

    command = sys.argv[1]
    if command == 'install':
        install_hook()
    elif command == 'uninstall':
        uninstall_hook()
    elif command == 'ci':
        generate_commit_message(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
