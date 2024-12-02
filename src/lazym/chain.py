from halo import Halo
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM

from .configs import configurations
from .constants import DEFAULT_TEMPERATURE


def format_commit_message(message, fmt):
    # First handle the period stripping if enabled
    if configurations.get('rstrip_period', 'true').lower() == 'true':
        message = message.rstrip('.')
    
    # Then handle the message format
    if fmt == 'lowercase':
        return message[0].lower() + message[1:]
    elif fmt == 'sentence case':
        return message.capitalize()
    return message  # Keep original format if not specified


def get_llm():
    temperature = float(configurations.get('temperature', DEFAULT_TEMPERATURE))
    if configurations['model'].startswith('groq:'):
        return ChatGroq(
            model=configurations['model'][5:],
            max_retries=2,
            temperature=temperature,
        )
    return OllamaLLM(model=configurations['model'], temperature=temperature)


def get_chain(prompt):
    prompt = PromptTemplate(template=prompt)
    llm = get_llm()
    return prompt | llm


def generate_commit_message(prompt, diff):
    with Halo(text='Generating commit message', spinner='spinner') as spinner:
        msg = get_chain(prompt).invoke({'diff': diff})
        spinner.succeed('Generated commit message')
    if hasattr(msg, 'content'):
        msg = msg.content
    return format_commit_message(msg, configurations['message_format'])
