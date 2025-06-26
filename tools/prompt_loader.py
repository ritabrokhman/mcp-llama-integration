import yaml
from pathlib import Path

PROMPT_FILE = Path(__file__).parent / "prompts.yaml"

def load_prompts():
    with open(PROMPT_FILE, "r") as f:
        return yaml.safe_load(f)

def get_prompt_template(name: str):
    prompts = load_prompts()
    if name not in prompts:
        raise ValueError(f"Prompt '{name}' not found.")
    return prompts[name]
