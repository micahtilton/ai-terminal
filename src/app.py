import os
import argparse
from openai import OpenAI
import yaml
import re

def get_or_create_config():
    home_dir = os.environ.get('HOME')
    config_path = os.path.join(home_dir, '.config', 'ai-term', 'config.yml')

    if not os.path.exists(config_path):
        default_config = open(os.path.join("./", "src", "default_config.yml"), "r").read()
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as config_file:
            config_file.write(default_config)

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    config["shell"] = os.environ.get("SHELL").split("/")[-1]

    return config

def parse_markdown(text, code_type):
    pattern = fr'```{code_type}(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]

def generate_query(query, config):
    return config["query_prompt"].format(**config, query=query)

def main():
    parser = argparse.ArgumentParser(description="AI Assisted Command Generator")
    parser.add_argument('query', nargs='?', help='The query in natural language.')
    args = parser.parse_args()

    config = get_or_create_config()
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not openai_api_key:
        print("OPENAI_API_KEY environment variable not found")
        return

    client = OpenAI(api_key=openai_api_key)
    message = client.chat.completions.create(
        messages=[
            {
                "role": "system", "content": config["query_prompt"]
            },
            {
                "role": "user",
                "content": generate_query(args.query, config),
            }
        ],
        model="gpt-4o-mini"
    )

    commands = parse_markdown(message.choices[0].message.content, config["shell"])

    if args.query:
        print("\n".join(commands))

if __name__ == "__main__":
    main()