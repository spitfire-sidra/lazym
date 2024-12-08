from pathlib import Path

from lazym.configs import configurations

_PROMPT = '''
You are an AI specialized in generating concise, high-quality git commit messages. Your task is to provide a single-line commit message summarizing the intent behind the changes, based on the provided diff and the conversation context.

Rules:
- One line only: The commit message must fit on a single line.
- Focus on intent: Clearly express the reason or purpose for the change (the "why"), not just the technical details (the "how").
- Be clear and concise: Use simple, precise language following standard git commit conventions.
- No filler: Avoid vague terms like "refactor" or "update" and do not include file statistics or fake issue numbers.
- Prioritize importance: Start with the most critical change if there are multiple updates.
- Contextual relevance: Take the full conversation into account when crafting the message, if provided.
- Diff structure: Use the GNU unified diff format details provided to interpret changes accurately.
    - (-) lines: Removed from original.
    - (+) lines: Added in modified version.
    - Unmarked lines: Unchanged context.
    - Focus only on the changes specified.

Diff Details:
The git diff will be enclosed in <diff> and </diff> below. 

Provide the commit message directly with no additional text, quotes, or explanation.

<diff>
{diff}
</diff>

COMMIT_MSG:
'''


def get_prompt():
    prompt_path = Path.home() / '.config' / 'lazym' / 'prompt.txt'
    if prompt_path.exists():
        return prompt_path.read_text()
    if configurations.get('prompt', ''):
        return configurations['prompt']
    return _PROMPT


PROMPT = get_prompt()
