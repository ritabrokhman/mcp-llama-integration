from pydantic import BaseModel
from typing import Dict, Any

# Represents a prompt in the system
class Prompt(BaseModel):
    name: str
    version: str
    content: str
    variables: Dict[str, Any]

