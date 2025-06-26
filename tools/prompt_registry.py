
# Initialize an empty dictionary to store registered prompts
PROMPT_REGISTRY = {}


# Register a new prompt with a name, version, content, and optional variables
def register_prompt(name: str, version: str, content: str, variables: dict = None):
    PROMPT_REGISTRY[name] = {
        "version": version,
        "content": content,
        "variables": variables or {}
    }


# Retrieve a registered prompt by name
def get_prompt(name: str):
    return PROMPT_REGISTRY.get(name)
