from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from .prompt import PROMPT


def get_llm():
    return OllamaLLM(model="llama3.1:8b")


def get_chain(prompt):
    prompt = PromptTemplate(template=prompt)
    llm = get_llm()
    return prompt | llm


def generate_commit_message(prompt, diff):
    return get_chain(prompt).invoke({'diff': diff})
