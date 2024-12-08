import logging

import requests

logging.basicConfig(level=logging.INFO)


def create_github_release(
    owner,
    repo,
    tag_name,
    release_name,
    body=None,
    token=None,
    draft=False,
    prerelease=False,
    generate_release_notes=True
):
    if not token:
        raise ValueError('GitHub API token is required to create a release.')

    url = f'https://api.github.com/repos/{owner}/{repo}/releases'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    payload = {
        'tag_name': tag_name,
        'name': release_name,
        'draft': draft,
        'prerelease': prerelease,
        'generate_release_notes': generate_release_notes,
    }
    if body:
        payload['body'] = body
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        logging.info('Release created successfully!')
        return response.json()
    else:
        logging.error(f'Failed to create release: {response.status_code}')
        logging.error(response.json())
        return None


def get_latest_release(owner, repo, token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logging.info('Latest release fetched successfully!')
        return response.json()
    
    logging.error(f'Failed to fetch latest release: {response.status_code}')
    logging.error(response.json())
    return None
