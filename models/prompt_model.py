from pydantic import BaseModel
from typing import Dict, Any

class Prompt(BaseModel):
    name: str
    version: str
    content: str
    variables: Dict[str, Any]

