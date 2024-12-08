import argparse
import re
from pathlib import Path

from lazym.version import bump_version


def get_current_version():
    setup_path = Path(__file__).parent / 'setup.py'
    with open(setup_path, 'r') as f:
        content = f.read()

    match = re.search(r'version="(\d+\.\d+\.\d+)"', content)
    if not match:
        raise ValueError('Version not found in setup.py')
    return match.group(1)


def update_version(new_version: str):
    setup_dot_py = Path(__file__).parent / 'setup.py'
    with open(setup_dot_py, 'r') as f:
        content = f.read()

    new_setup_dot_py = re.sub(
        r'version="(\d+\.\d+\.\d+)"',
        f'version="{new_version}"',
        content
    )

    with open(setup_dot_py, 'w') as f:
        f.write(new_setup_dot_py)


def main():
    parser = argparse.ArgumentParser(description='Release tool to update version in setup.py')
    parser.add_argument('bump', nargs='?', choices=['major', 'minor', 'patch'], default='patch',
                        help='Specify which part of the version to bump (default: patch)')
    
    args = parser.parse_args()
    
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    
    # Calculate new version
    new_version = bump_version(current_version, args.bump)
    
    # Confirm with user
    print(f"\nThis will update version from {current_version} to {new_version}")
    confirm = input("Proceed? (y/n): ").lower().strip()
    
    if confirm == 'y':
        update_version(new_version)
        print(f"\nVersion successfully updated to {new_version}")
    else:
        print("\nOperation cancelled")

if __name__ == '__main__':
    main()

