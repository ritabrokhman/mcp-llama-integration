# Import yaml 
import yaml

# Import Path from pathlib to handle file paths in a platform-independent way
from pathlib import Path

# Define the path to the prompts.yaml file located in the same directory as this script
PROMPT_FILE = Path(__file__).parent / "prompts.yaml"

# Load all prompts from the YAML file
def load_prompts():
    with open(PROMPT_FILE, "r") as f:
        return yaml.safe_load(f) 
# Retrieve a specific prompt template by name
def get_prompt_template(name: str):
    prompts = load_prompts() 
    if name not in prompts:
        raise ValueError(f"Prompt '{name}' not found.") 
    return prompts[name]  

