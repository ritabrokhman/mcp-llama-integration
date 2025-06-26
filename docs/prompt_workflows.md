# Prompt Management Workflows

## Registering a Prompt
POST /prompt/register  
Payload:
```json
{
  "name": "daily_summary",
  "version": "v1",
  "content": "Summarize: {input}",
  "variables": {
    "input": "Text to summarize"
  }
}
