# Prompt Authoring Guide

This guide explains how to write and register prompts for the MCP server.

## Prompt Structure

Each prompt must include the following fields:

- `name`: A unique name for the prompt (e.g., "daily_summary")
- `version`: A version identifier (e.g., "v1")
- `content`: The actual prompt text, using placeholders for variables (e.g., "Summarize: {input}")
- `variables`: A dictionary describing each variable used in the prompt

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
