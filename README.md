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

Once installed and set up, lazym works in two ways:

1. Automatically when you make a commit:
   Simply stage your changes as usual and run `git commit`. lazym will generate a commit message based on your staged changes.

2. Manually by running `lazym ci "<hints for LLM>"`:
   This command allows you to generate a commit message with additional context provided to the LLM.

After generating the commit message, you'll be presented with three options:

1. Accept and commit: Use the generated message as-is and commit.
2. Edit message: Modify the generated message before committing.
3. Cancel commit: Abort the commit process.

This allows you to benefit from the AI-generated suggestions while maintaining full control over your commit messages. When editing, you can start with the AI-generated message and make any necessary adjustments.

## Commands

- `lazym install`: Install the prepare-commit-msg hook in the current Git repository.
- `lazym uninstall`: Uninstall the prepare-commit-msg hook from the current Git repository.
- `lazym ci "<optional hints>"`: Generate a commit message with optional additional context.
