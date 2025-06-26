# **MCP Server README File**

MCP Server -LLaMA Integration Framework

## **Introduction**

Welcome to the mcp-llama-integration project! This repository provides a reference implementation for integrating Meta’s LLaMA 3 language model with the Model Context Protocol (MCP) framework. MCP acts as a universal adapter between large language models (LLMs) and external tools, enabling seamless orchestration of tool usage, context retrieval, and API execution through a standardized JSON-RPC interface.

This integration demonstrates how to:

Connect LLaMA 3 (via Ollama) to an MCP-compliant tool server.
Define and expose tools with structured metadata for LLM invocation.
Handle tool execution, context injection, and response transformation.
Build a scalable, secure, and extensible server architecture for AI agents.
Whether you're building intelligent assistants, automating workflows, or experimenting with tool-augmented LLMs, this project offers a practical foundation for deploying LLaMA in real-world, tool-rich environments.

## **Project Structure**

Project structure is defined inside **'structure.txt'**.

## **Installation**

To install the MCP Server:

1. Ensure Python 3 is intalled
    Make sure Python 3.1 or higher is installed
        Verify:
            **'python --version'**

2. Install FastAPI
    **'pip install fastapi'**

    Ensure FastAPI is up to date 
        **'pip install --upgrade fastapi'**

3. Install Pydantic
    **'pip install pydantic'**

4. Install Yaml
    **'pipenv install pyyaml'**

5. Download and start Ollama:
    Download:
        visit: https://ollama.com
        follow the installation instructions for your OS 
    Once installed, pull the model:
        **'ollama pull llama3 '**
    Once pulled run the model:
        **'ollama run llama3.2'**

5. Start the server locally: 
    **'pipenv run start'**

## **Usage**

Once the MCP server is running, you can interact with it using any client that supports JSON-RPC 2.0. The server listens for requests that invoke tools or retrieve context, and routes them to the appropriate logic handlers.

Docker Access: 
Once everything is downloaded:
    1. Build Docker Image: 
        **'build -t mcp-server'**
    2. Run your container:
        **'docker run -p 8000:8000 mcp-server'**
    3. Type http://localhost:8000 into a new browser tab and hit enter
    4. Deleting a Docker Container: 
        **' docker rm <container_id_or_name> '**
    5. Deleting a Docker Images: 
        **' docker rmi <timage_id_or_name> '**
        
## **Use Cases**

1. Internal tooling agents using LLaMA with custom context
2. Prompt-driven workflows for non-technical users
3. Agent backends for enterprise LLM applications
4. Interactive knowledge retrieval from your tools, not just text

## **Contributing**

To contribute:

1. Fork the repo
2. Create a feature branch
3. Submit a pull request with a clear description
4. Tag a maintainer for review

## **Authors and Acknowledgment

Rita Brokhman, Connor Pletikapich, and Sawyer Cartwright

## **Future Suggestions**

The mcp-llama-integration project is designed to be a skeleton, enabling a wide range of future applications. Here are some directions this integration can support:
1. Tool Expansion:
    - Add new tools to the tools/ directory with custom schemas and execution logic.
    - Support multi-step toolchains and conditional tool invocation.
    - Integrate with enterprise APIs, databases, or internal systems.
2.  Model Flexibility
    - Swap out LLaMA 3 for other local or hosted models
    - Add support for model selection and fallback strategies.
3. Agent Frameworks
    - Wrap the MCP server into a full agent runtime.
