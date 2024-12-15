import os
import shutil
import sys
from typing import Optional

from beaupy import confirm, select
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from lazym.configs import configurations
from lazym.constants import DEFAULT_VERSION
from lazym.git import commit, get_local_latest_tags, get_repo_info
from lazym.github import create_github_release, get_latest_release, get_latest_tags
from lazym.version import bump_version


def custom_prompt(message: str, initial_value: str = "") -> Optional[str]:
    # Create key bindings
    kb = KeyBindings()
    
    @kb.add('c-u')
    def _(event):
        # Clear the buffer
        event.current_buffer.text = ""
    
    # Create a session with the key bindings
    session = PromptSession(key_bindings=kb)
    
    # Show the prompt with initial value
    result = session.prompt(
        message + "\n(Ctrl+U to clear, Enter to submit)\n> ",
        default=initial_value
    )
    
    return result if result.strip() else None

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
    
    prompt_with_summary = f"{PROMPT}\n\nHere is a summary of the changes: {summary}"
    return generate_commit_message(prompt_with_summary, diff)


def highlight(s):
    return f'\033[1;33m{s}\033[0m'


def main():
    if len(sys.argv) < 2:
        print("Usage: lazym <command> <args>")
        print("Available commands:")
        print("\tinstall - Install the prepare-commit-msg hook")
        print("\tuninstall - Uninstall the prepare-commit-msg hook")
        print("\tci - Generate commit message with additional context")
        print("\trelease <type> - Bump version (type: main, minor, patch)")
        sys.exit(0)

    command = sys.argv[1]
    if command == 'tag':
        # Get the latest local tag
        local_tags = get_local_latest_tags()
        latest_local_tag = local_tags[0] if local_tags else None
        
        # Get the latest remote tag
        repo_owner, repo_name = get_repo_info()
        latest_remote_tags = get_latest_tags(repo_owner, repo_name, configurations.get('token', ''))
        latest_remote_tag_name = latest_remote_tags[0] if latest_remote_tags else None

        print("Latest local tag:", latest_local_tag if latest_local_tag else "No local tags found.")
        print("Latest remote tag:", latest_remote_tag_name if latest_remote_tag_name else "No remote tags found.")

        # Prepare options for selection
        options = []
        if latest_local_tag:
            options.append(latest_local_tag)
        if latest_remote_tag_name:
            options.append(latest_remote_tag_name)
        options.append("Specify a new tag")
        options.append('Abort')
        # Ask user to select a tag
        print('Please choose a tag to bump.')
        selected_tag = select(options)
        final_tag =  None
        if selected_tag == "Specify a new tag":
            if not (repo_owner and repo_name):
                print("Error: Could not determine repository information.")
                sys.exit(1)

            new_tag = custom_prompt("Enter the new tag name:", initial_value="")
            if new_tag:
                print(f"New tag specified: {new_tag}")
                final_tag = new_tag
            else:
                print("No new tag specified. Aborting.")
                sys.exit(1)
        elif selected_tag == 'Abort' or not selected_tag:
            sys.exit(0)
        else:
            print(f"Selected a tag to bump: {selected_tag}")
            options = []
            for bump_type in ['main', 'minor', 'patch']:
                new_version = bump_version(selected_tag, bump_type)
                options.append(new_version)
            options.append('abort')
            print("Choose a new version to bump to:")
            selected_tag = select(options)
            if selected_tag == 'abort':
                sys.exit(0)
            print(f"Selected tag: {selected_tag}")
            final_tag = selected_tag

        if not final_tag:
            print("No tag selected or specified. Aborting.")
            sys.exit(1)
        
        # Create a local tag
        try:
            os.system(f'git tag -a {final_tag} -m "{final_tag}"')
            print(f"Tag {final_tag} created successfully.")
        except Exception as e:
            print(f"Failed to create tag {final_tag}: {e}")
            sys.exit(1)

        push_tag = confirm("Do you want to push the tag to the remote repository?")
        if push_tag:
            try:
                os.system(f'git push origin {final_tag}')
                print(f"Tag {final_tag} pushed to remote successfully.")
            except Exception as e:
                print(f"Failed to push tag {final_tag} to remote: {e}")
                sys.exit(1)
        else:
            print("Tag not pushed to remote.")
    elif command == 'release':
        if configurations.get('service', '').lower() == 'github':
            repo_owner, repo_name = get_repo_info()
            if not (repo_owner and repo_name):
                print("Error: Could not determine repository information.")
                sys.exit(1)
            latest_tags = get_latest_tags(repo_owner, repo_name, limit=5)
            if not latest_tags:
                print("Failed to fetch latest tags.")
                sys.exit(1)
            print("Select a tag to release on GitHub:")
            selected_tag = select(latest_tags)
            print(f"Selected tag for release: {selected_tag}")
            create_github_release(
                repo_owner,
                repo_name,
                selected_tag,
                selected_tag,
                token=configurations.get('token', ''),
            )
        else:
            raise NotImplemented
    elif command == 'install':
        install_hook()
    elif command == 'uninstall':
        uninstall_hook()
    elif command == 'ci':
        hint = sys.argv[2] if len(sys.argv) > 2 else ""
        commit_message = generate_commit_message(hint)
        print(f"Generated commit message:\n\n{highlight(commit_message)}\n")
        
        options = ["Accept and commit", "Edit message", "Regenerate message", "Use different hint", "Cancel commit"]
        while True:
            choice = select(options)
            if choice == "Use different hint":
                hint = custom_prompt("Enter a new hint:", initial_value=hint)
                commit_message = generate_commit_message(hint)
                print(f"Generated commit message:\n\n{highlight(commit_message)}\n")
                continue
            if choice == "Regenerate message":
                commit_message = generate_commit_message(hint)
                print(f"Generated commit message:\n\n{highlight(commit_message)}\n")
                continue
            if choice == "Accept and commit":
                commit(commit_message)
                break
            elif choice == "Edit message":
                edited = custom_prompt("Edit the commit message:", initial_value=commit_message)
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
                commit_message = commit_message if not edited else edited
                print(f"Edited commit message:\n\n{highlight(commit_message)}\n")
                if confirm("Commit with this edited message?"):
                    commit(commit_message)
                    break
            elif choice == "Cancel commit":
                print("Commit aborted.")
                break
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
