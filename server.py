from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import ollama
from tools.prompt_registry import register_prompt, get_prompt
from tools.prompt_loader import get_prompt_template

# Creates web app only on machine 
app = FastAPI()

# Get input from user- compatible with FastAPI
# Middleman
app.add_middleware(
    CORSMiddleware,
    # Allows all origins
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="interface")

# Make frontend.html accessible at root "/"
@app.get("/")
def get_frontend():
    return FileResponse("frontend/interface.html")

# Mock user data
# Test tool 
# Remove later
USERS = {
    "rita": {"name": "Rita Brokhman", "role": "Tech Architecture Analyst", "location": "Columbus"},
    "katie": {"name": "Katie Holcomb", "role": "Software Product Mgmt Manager", "location": "Columbus"},
    "sawyer": {"name": "Sawyer Cartwright", "role": "Tech Architecture Analyst", "location": "Columbus"},
    "connor": {"name": "Connor Pletikapich", "role": "Tech Architecture Analyst", "location": "Columbus"}
}

# Request schema
# front end, determines what can be inputted
class MCPRequest(BaseModel):
    input: str
    # Optional, can make not optional
    parameters: Optional[dict] = {}

# Defines logic 
# Post transfers user input for tool into respective output
@app.post("/mcp")
async def mcp_handler(request: MCPRequest):
    if request.input == "get-user":
        user_id = request.parameters.get("user_id", "").lower()
        return {"output": USERS.get(user_id, {"error": "User not found"})}
    elif request.input == "list-users":
        return {"output": list(USERS.keys())}
    elif request.input == "hello-world":
        return {"output": "Hello World!"}    
    # This integrates llama3 
    elif request.input == "llama-chat":
      prompt_data = get_prompt_template("llama_chat")
      template = prompt_data["template"]
      filled_prompt = template.replace("{{prompt}}", request.parameters.get("prompt", ""))
      resp = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": filled_prompt}],
      )
      return {"output": resp["message"]["content"]}
    else:
        return {"error": f"Unknown tool: {request.input}"}
    
# Registering prompts
@app.post("/prompt/register")
async def register_prompt_api(payload: dict):
    register_prompt(**payload)
    return {"status": "registered"}

@app.get("/prompt/{name}")
async def get_prompt_api(name: str):
    result = get_prompt(name)
    return result if result else {"error": "Prompt not found"}
