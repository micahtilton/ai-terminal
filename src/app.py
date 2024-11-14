import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
import argparse
import yaml
import re

default_config = """
n: 3
query_prompt: |
  Using {shell}, show me {n} different ways that I achieve this action.
  The command MUST be in one line.
  Do NOT explain your answers.
  You MUST use markdown

  {query}
model: "gpt-4o-mini" 
""".strip()

def get_or_create_config():
    home_dir = os.environ.get('HOME')
    config_path = os.path.join(home_dir, '.config', 'ai-term', 'config.yml')

    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as config_file:
            config_file.write(default_config)  # Example default content

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
        return config

def parse_markdown(text, code_type):
    pattern = fr'```{code_type}(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]

def main():
    parser = argparse.ArgumentParser(description="AI Assisted Command Generator")
    parser.add_argument('query', nargs='?', help='The query in natural language.')
    args = parser.parse_args()

    config = get_or_create_config()
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not openai_api_key:
        print("OPENAI_API_KEY environment variable not found")
        return

    if config["type"] == "openai":
        llm = ChatOpenAI(model=config["model"], api_key=openai_api_key, temperature=0)
    elif config["type"] == "local":
        llm = ChatOllama(model=config["model"], temperature=0)

    template = ChatPromptTemplate([
        ("system", "You are a helpful assistant."),
        ("user", config["query_prompt"])
    ])

    output_parser = StrOutputParser()

    chain = template | llm | output_parser

    shell = os.environ.get("SHELL").split("/")[-1]
    output = chain.invoke({"shell": shell, "query": args.query, "n": config["n"]})
    commands = parse_markdown(output, shell)
    
    if args.query:
        print("\n".join(commands))

if __name__ == "__main__":
    main()