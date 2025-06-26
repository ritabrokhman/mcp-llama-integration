PROMPT_REGISTRY = {}

def register_prompt(name: str, version: str, content: str, variables: dict = None):
    PROMPT_REGISTRY[name] = {
        "version": version,
        "content": content,
        "variables": variables or {}
    }

def get_prompt(name: str):
    return PROMPT_REGISTRY.get(name)
