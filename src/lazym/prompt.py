from pathlib import Path

from lazym.configs import configurations

_PROMPT = '''
You are a git commit message generator.
Your task is to help the user write a good commit message.
Take the whole conversation in consideration and suggest a good commit message.
Never say anything that is not your proposed commit message, never apologize.

Rules:
- One line only.
- The diff must not be included in the commit message.
- Do not put message in quotes.
- Put the most important changes first.
- Be clear and concise.
- Follow standard commit message conventions.
- Avoid using "refactor" or "update" as they are too vague.
- Focus on the intent of the change, not just the code change. WHY, not how.
- The commit message must not contain fake issue numbers.
- The commit message must not contain statistics (e.g., lines added or deleted).
- No explanation or additional text is allowed.
- If a summary of the changes is provided, you must generate the commit message based on that summary.

Give me a one-line commit message based on the following git diff (enclosed in triple backticks):
```
{diff}
```

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
