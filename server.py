from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, Dict
from fastapi.middleware.cors import CORSMiddleware
import ollama
from tools.prompt_registry import register_prompt, get_prompt
from tools.prompt_loader import get_prompt_template
from tools.metrics import track_latency, track_tokens, track_tool_usage, track_error, track_context_hit, get_metrics
import time
from tools.context_storage import init_db
from tools.context_storage import save_context
from tools.metrics import init_metrics_db

# Initialize the database
# Use SQLite for context storage
init_db()

# Initialize the metrics database
# Use SQLite for metrics storage
# This is where we store tool usage, latency, and token stats
init_metrics_db()

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
    parameters: Optional[Dict[str, str]] = {}


# Ollama client setup
# Connects to Ollama server
ollama_client = ollama.Client(host='http://127.0.0.1:11434')
# ollama_client = ollama.Client(host='http://host.docker.internal:11434')

# Defines logic 
# Post transfers user input for tool into respective output
@app.post("/mcp")
async def mcp_handler(request: MCPRequest):
    start = time.time()
    try:
        # Get User tool
        if request.input == "get-user":
            track_tool_usage("get-user")
            user_id = request.parameters.get("user_id", "").lower()
            result = USERS.get(user_id)
            if result:
                return {"output": result}
            else:
                track_context_hit(False)
                return {"output": {"error": "User not found"}}

        # List all users tool
        elif request.input == "list-users":
            track_tool_usage("list-users")
            return {"output": list(USERS.keys())}

        # Hello World tool
        elif request.input == "hello-world":
            track_tool_usage("hello-world")
            return {"output": "Hello World!"}

        # Ollama chat tool
        elif request.input == "llama-chat":
            track_tool_usage("llama-chat")

            prompt_data = get_prompt_template("llama_chat")
            if prompt_data:
                track_context_hit(True)
            else:
                track_context_hit(False)
                return {"output": {"error": "Prompt template not found"}}

            template = prompt_data["template"]
            prompt = request.parameters.get("prompt", "")
            filled_prompt = template.replace("{{prompt}}", prompt)

            # Call the model
            resp = ollama_client.chat(
                model="llama3.2",
                messages=[{"role": "user", "content": filled_prompt}],
            )

            # Track token stats
            prompt_tokens = len(filled_prompt.split())
            response_tokens = len(resp["message"]["content"].split())
            track_tokens(prompt_tokens, response_tokens)

            # Save to SQLite
            save_context(
             tool_name="llama-chat",
             user_id=request.parameters.get("user_id", "anonymous"),
             prompt=prompt,
             response=resp["message"]["content"])

            return {"output": resp["message"]["content"]}

        else:
            track_tool_usage("unknown")
            track_context_hit(False)
            return {"error": f"Unknown tool: {request.input}"}

    except Exception as e:
        track_error()
        return {"error": str(e)}

    finally:
        track_latency(start)
    
# Registering prompts
@app.post("/prompt/register")
async def register_prompt_api(payload: dict):
    register_prompt(**payload)
    return {"status": "registered"}

@app.get("/prompt/{name}")
async def get_prompt_api(name: str):
    result = get_prompt(name)
    return result if result else {"error": "Prompt not found"}
