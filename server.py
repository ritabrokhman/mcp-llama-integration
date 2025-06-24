from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock user data
USERS = {
    "rita": {"name": "Rita Brokhman", "role": "Tech Architecture Analyst", "location": "Columbus"},
    "katie": {"name": "Katie Holcomb", "role": "Software Product Mgmt Manager", "location": "Columbus"},
    "sawyer": {"name": "Sawyer Cartwright", "role": "Tech Architecture Analyst", "location": "Columbus"},
    "connor": {"name": "Connor Pletikapich", "role": "Tech Architecture Analyst", "location": "Columbus"}
}

# Request schema
class MCPRequest(BaseModel):
    input: str
    parameters: Optional[dict] = {}

@app.post("/mcp")
async def mcp_handler(request: MCPRequest):
    if request.input == "hello-world":
        return {"output": "Hello World!"}
    elif request.input == "get-user":
        user_id = request.parameters.get("user_id", "").lower()
        return {"output": USERS.get(user_id, {"error": "User not found"})}
    elif request.input == "list-users":
        return {"output": list(USERS.keys())}
    elif request.input == "llama-chat":
        prompt = request.parameters.get("prompt", "")
        resp = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
        return {"output": resp["message"]["content"]}
    else:
        return {"error": f"Unknown tool: {request.input}"}
