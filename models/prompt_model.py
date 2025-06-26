from pydantic import BaseModel
from typing import Dict

class Prompt(BaseModel):
    name: str
    version: str
    content: str
    variables: Dict[str, str]

