import os
import shutil
import sys
from typing import Optional

import typer
from beaupy import confirm, select
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from lazym.configs import configurations
from lazym.git import (
    commit,
    create_tag,
    get_local_latest_tags,
    get_repo_info,
    get_repo_root,
    push_tag_to_origin,
)
from lazym.github import create_github_release, get_latest_tags
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


def generate_commit_message(summary):
    from .chain import generate_commit_message
    from .git import get_diff
    from .prompt import PROMPT

    repo_root = get_repo_root()
    diff = get_diff(repo_root)
    if not diff:
        print("No changes to commit.")
        sys.exit(0)
    
    prompt_with_summary = f"{PROMPT}\n\nHere is a summary of the changes: {summary}"
    return generate_commit_message(prompt_with_summary, diff)


def highlight(s):
    return f'\033[1;33m{s}\033[0m'


app = typer.Typer()

@app.command()
def install():
    '''
    Install the Git prepare-commit-msg hook for managing commit messages.
    This hook will automatically populate the commit message template when 
    a commit is made.
    '''
    # Get the current git repository root
    repo_root = get_repo_root()

    # Define source and destination paths
    source = os.path.join(os.path.dirname(__file__), 'prepare-commit-msg')
    dest = os.path.join(repo_root, '.git', 'hooks', 'prepare-commit-msg')

    # Copy the hook file
    try:
        shutil.copy2(source, dest)
        os.chmod(dest, 0o755)  # Make the script executable
        print(f'Successfully installed prepare-commit-msg hook to {dest}')
    except Exception as e:
        print(f'Error installing hook: {str(e)}')
        sys.exit(1)


@app.command()
def uninstall():
    '''
    Uninstall the Git prepare-commit-msg hook.
    '''
    # Get the current git repository root
    repo_root = get_repo_root()

    # Define the hook path
    hook_path = os.path.join(repo_root, '.git', 'hooks', 'prepare-commit-msg')

    # Remove the hook file
    try:
        if os.path.exists(hook_path):
            os.remove(hook_path)
            print(f'Successfully uninstalled the prepare-commit-msg hook from: {hook_path}')
        else:
            print('Hook not found. Nothing to uninstall.')
    except Exception as e:
        print(f'Error uninstalling hook: {str(e)}')
        sys.exit(1)


def select_base_tag(local_tag, remote_tag):
    tags = (local_tag, remote_tag, )
    if local_tag == remote_tag:
        tags = (local_tag, )
    options = [t for t in tags if t]
    options.extend(["Specify a new tag", "Abort"])
    return select(options)


def get_new_tag_version(base_tag):
    options = [bump_version(base_tag, btype) for btype in ['main', 'minor', 'patch']]
    options.append('abort')
    return select(options)


@app.command()
def tag():
    '''
    Automatically generate a new git tag.
    '''
    # Get the latest local tag
    latest_local_tag = get_local_latest_tags()[0] if get_local_latest_tags() else None
    
    # Get the latest remote tag
    repo_owner, repo_name = get_repo_info()
    latest_remote_tags = get_latest_tags(repo_owner, repo_name, configurations.get('token', ''))
    latest_remote_tag = latest_remote_tags[0] if latest_remote_tags else None

    print("Latest local tag:", latest_local_tag if latest_local_tag else "No local tags found.")
    print("Latest remote tag:", latest_remote_tag if latest_remote_tag else "No remote tags found.")

    # Prepare options for selection
    selected = select_base_tag(latest_local_tag, latest_remote_tag)
    if selected in ['Abort', None]:
        sys.exit(0)

    # Ask user to select a tag
    final_tag = None
    if selected == "Specify a new tag":
        final_tag = custom_prompt("Enter the new tag name:", initial_value="")
    else:
        final_tag = get_new_tag_version(selected)

    if not final_tag or final_tag == 'abort':
        print("No tag selected or specified. Aborting.")
        sys.exit(1)
    
    # Create a local tag
    create_tag(final_tag)

    if push_tag := confirm("Do you want to push the tag to the remote repository?"):
        push_tag_to_origin(final_tag)
    else:
        print("Tag not pushed to remote.")

@app.command()
def release():
    '''
    Create a new release on GitHub based on the selected tag.
    This command allows you to publish a new version of your project.
    '''
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
        return
    raise NotImplementedError


@app.command()
def ci(hint: str):
    '''
    Generate a commit message with additional context or hints.
    '''
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
            commit_message = edited if edited else commit_message
            print(f"Edited commit message:\n\n{highlight(commit_message)}\n")
            if confirm("Commit with this edited message?"):
                commit(commit_message)
                break
        elif choice == "Cancel commit":
            print("Commit aborted.")
            break


if __name__ == "__main__":
    app()
