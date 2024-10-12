import os
import shutil
import sys


def install_hook():
    # Get the current git repository root
    try:
        git_root = os.popen('git rev-parse --show-toplevel').read().strip()
    except Exception:
        print("Error: Not a git repository or git is not installed.")
        sys.exit(1)

    # Define source and destination paths
    source_path = os.path.join(os.path.dirname(__file__), 'prepare-commit-msg')
    dest_path = os.path.join(git_root, '.git', 'hooks', 'prepare-commit-msg')

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
    try:
        git_root = os.popen('git rev-parse --show-toplevel').read().strip()
    except Exception:
        print("Error: Not a git repository or git is not installed.")
        sys.exit(1)

    # Define the hook path
    hook_path = os.path.join(git_root, '.git', 'hooks', 'prepare-commit-msg')

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

def main():
    if len(sys.argv) < 2:
        print("Usage: lazym <command>")
        print("Available commands:")
        print("\tinstall - Install the prepare-commit-msg hook")
        print("\tuninstall - Uninstall the prepare-commit-msg hook")
        sys.exit(0)

    command = sys.argv[1]
    if command == 'install':
        install_hook()
    elif command == 'uninstall':
        uninstall_hook()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
