# Prompt Authoring Guide


This guide explains how to write and register prompts for the MCP server, enabling structured and reusable interactions with LLaMA 3 via the Model Context Protocol (MCP).

## Prompt Structure

Each prompt must include the following fields:

- `name`: A unique name for the prompt (e.g., "daily_summary")
- `version`: A version identifier (e.g., "v1")
- `content`: The actual prompt text, using placeholders for variables (e.g., "Summarize: {input}")
- `variables`:A dictionary describing each placeholder used in the prompt, where the key is the variable name and the value is a description.

## Example Prompt

```json
{
  "name": "daily_summary",
  "version": "v1",
  "content": "Summarize the following: {input}",
  "variables": {
    "input": "The text to summarize"
  }
}

## **Registering a Prompt with the MCP server**
  1. Add the prompt definition to your prompt registry (e.g., a YAML or JSON file).
  2. Ensure the server loads this file at startup or via a dynamic endpoint.
  3. Use the prompts/list and prompts/get JSON-RPC methods to discover and invoke prompts.


## **Example Prompt**
  
  ```json
  {
  "jsonrpc": "2.0",
  "method": "prompts/get",
  "params": {
    "name": "daily_summary",
    "arguments": {
      "input": "Today we launched a new feature and fixed several bugs."
    }
  },
  "id": 1
}

