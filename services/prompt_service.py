from typing import Dict, Tuple
from models.prompt_model import Prompt

# Creates in-memory storage for prompts
prompt_store: Dict[Tuple[str, str], Prompt] = {}

# Function to register a new prompt
def register_prompt(prompt: Prompt) -> Dict[str, str]:
    key = (prompt.name, prompt.version)
    # New prompts are saved
    if key in prompt_store:
        return {"error": "Prompt with this name and version already exists."}
    prompt_store[key] = prompt
    return {"message": "Prompt registered successfully"}
