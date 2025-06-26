from typing import Dict, Tuple
from models.prompt_model import Prompt

# In-memory store for prompts
prompt_store: Dict[Tuple[str, str], Prompt] = {}

def register_prompt(prompt: Prompt) -> Dict[str, str]:
    key = (prompt.name, prompt.version)
    if key in prompt_store:
        return {"error": "Prompt with this name and version already exists."}
    prompt_store[key] = prompt
    return {"message": "Prompt registered successfully"}
