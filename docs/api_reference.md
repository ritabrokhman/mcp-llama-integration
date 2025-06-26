# API Reference

This document describes the available API endpoints for the MCP server.

---

## POST /prompt/register

Registers a new prompt.

### Request

**Method**: `POST`  
**URL**: `/prompt/register`  
**Content-Type**: `application/json`

### Payload

```json
{
  "name": "daily_summary",
  "version": "v1",
  "content": "Summarize the following: {input}",
  "variables": {
    "input": "The text to summarize"
  }
}
