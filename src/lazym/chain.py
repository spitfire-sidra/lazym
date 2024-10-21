from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from .configs import configurations


def format_commit_message(message, fmt):
    if fmt == 'lowercase':
        return message[0].lower() + message[1:]
    elif fmt == 'sentence case':
        return message.capitalize()
    return message  # Keep original format if not specified


def get_llm():
    return OllamaLLM(model=configurations['model'])


def get_chain(prompt):
    prompt = PromptTemplate(template=prompt)
    llm = get_llm()
    return prompt | llm


def generate_commit_message(prompt, diff):
    msg = get_chain(prompt).invoke({'diff': diff})
    return format_commit_message(msg, configurations['message_format'])
