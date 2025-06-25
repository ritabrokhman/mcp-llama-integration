from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import ollama

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
app.mount("/frontend", StaticFiles(directory="Frontend"), name="frontend")

# Make frontend.html accessible at root "/"
@app.get("/")
def get_frontend():
    return FileResponse("Frontend/frontend.html")

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
    if request.input == "hello-world":
        return {"output": "Hello World!"}
    elif request.input == "get-user":
        user_id = request.parameters.get("user_id", "").lower()
        return {"output": USERS.get(user_id, {"error": "User not found"})}
    elif request.input == "list-users":
        return {"output": list(USERS.keys())}
    # This integrates llama3 
    elif request.input == "llama-chat":
        prompt = request.parameters.get("prompt", "")
        resp = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
        return {"output": resp["message"]["content"]}
    else:
        return {"error": f"Unknown tool: {request.input}"}
