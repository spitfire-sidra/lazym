# lazym

lazym is an AI-powered tool that automatically generates meaningful commit messages for your Git repositories.

*lazym is inspired by [jen-Ya/commitgpt](https://github.com/jen-Ya/commitgpt)*

## Features

- Generates commit messages based on staged changes
- Without the risk of leaking code snippets to external LLM services
- Integrates seamlessly with your Git workflow
- Uses advanced language models for intelligent message generation

## Requirements

- [Ollama](https://ollama.ai/) with [Llama 3.1:8b](https://ollama.com/library/llama3.1:8b) model
- Git (version 2.0 or higher)
- Python 3.7 or above

Command to pull Llama 3.1:8b model for Ollama:

```
$ ollama run llama3.1:8b
```

## Installation

To install lazym, follow these steps:

1. Ensure you have Python 3.7+ and pip installed on your system.
2. Install lazym using pip:

   ```
   pip install lazym
   ```

3. After installation, navigate to any Git repository and run the following command to set up the Git hook:

   ```
   lazym install
   ```

   This will install the necessary Git hook to enable automatic commit message generation.

## Usage

Once installed and set up, lazym works automatically when you make a commit. Simply stage your changes as usual and run `git commit`. lazym will generate a commit message based on your staged changes.

If you want to modify the generated message, you can edit it in the commit message editor that opens after generation.
