import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

# Tests that the "hello-world" tool returns the expected static string
def test_hello_world():
    response = client.post("/mcp", json={"input": "hello-world"})
    assert response.status_code == 200
    assert response.json() == {"output": "Hello World!"}

# Tests that "get-user" returns the correct user data for an existing user
def test_get_existing_user():
    response = client.post("/mcp", json={
        "input": "get-user",
        "parameters": {"user_id": "rita"}
    })
    assert response.status_code == 200
    data = response.json()["output"]
    assert data["name"] == "Rita Brokhman"
    assert data["role"] == "Tech Architecture Analyst"
    assert data["location"] == "Columbus"

# Tests that "get-user" returns an error when the user is not found
def test_get_unknown_user():
    response = client.post("/mcp", json={
        "input": "get-user",
        "parameters": {"user_id": "unknown"}
    })
    assert response.status_code == 200
    assert "error" in response.json()["output"]

# Tests that "list-users" returns a list of all valid user IDs
def test_list_users():
    response = client.post("/mcp", json={"input": "list-users"})
    assert response.status_code == 200
    users = response.json()["output"]
    assert isinstance(users, list)
    assert "rita" in users

# Tests that "llama-chat" tool works and returns a mocked response
def test_llama_chat_mock(monkeypatch):
    # Monkeypatch ollama.chat to avoid calling the real model
    def mock_chat(**kwargs):
        return {"message": {"content": "This is a mock response"}}

    import server
    monkeypatch.setattr(server.ollama, "chat", mock_chat)

    response = client.post("/mcp", json={
        "input": "llama-chat",
        "parameters": {"prompt": "Tell me a joke"}
    })
    assert response.status_code == 200
    assert response.json()["output"] == "This is a mock response"

# Tests that providing an invalid tool name returns an error message
def test_invalid_tool():
    response = client.post("/mcp", json={"input": "unknown-tool"})
    assert response.status_code == 200
    assert "error" in response.json()

# Tests that the server returns a 404 for an invalid endpoint
def test_invalid_endpoint():
    response = client.post("/mcp/invalid-endpoint", json={"input": "hello-world"})
    assert response.status_code == 404
    assert "detail" in response.json()

# Tests that malformed JSON input returns a 422 Unprocessable Entity error
def test_bad_json_format():
    response = client.post("/mcp", content=b'{"input": "hello-world"')
    assert response.status_code == 422

# Tests that a POST request missing the required "input" field fails validation
def test_missing_input_field():
    response = client.post("/mcp", json={})
    assert response.status_code == 422
    assert "detail" in response.json()

# Tests that a GET request to /mcp is rejected with 405 Method Not Allowed
def test_get_request_not_allowed():
    response = client.get("/mcp")
    assert response.status_code == 405
