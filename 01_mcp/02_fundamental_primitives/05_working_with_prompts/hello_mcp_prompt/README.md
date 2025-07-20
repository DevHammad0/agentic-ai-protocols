# MCP Prompts Implementation

A demonstration project implementing **Model Context Protocol (MCP) Prompts** using FastMCP. Shows how to create pre-built, high-quality prompt templates that provide better results than users writing prompts from scratch.

## What are MCP Prompts?

MCP Prompts are **pre-built, thoroughly tested instructions** that servers expose to clients. Instead of users crafting their own prompts, they leverage expertly designed templates that handle edge cases and follow best practices.

**Key Benefits**: Higher quality results, domain expertise encoded, consistency, better user experience.

## Available Prompts

1. **Format Document** (`format`) - Converts plain text to well-structured Markdown
2. **Summarize Document** (`summarize`) - Creates concise summaries of longer documents

## Protocols Included

- **JSON-RPC 2.0** over HTTP with Server-Sent Events (SSE)
- **MCP Prompts Protocol**:
  - `prompts/list` - Discover available prompts
  - `prompts/get` - Execute prompt with arguments

## Project Structure

```
hello_mcp_prompt/
├── server.py          # MCP server with prompt definitions
├── client.py          # HTTP client for testing prompts
├── pyproject.toml     # Project dependencies
└── README.md          # This file
```

## Setup and Installation

### Prerequisites
- Python 3.13+
- UV package manager

### Create & Activate Virtual Environment

```bash
uv venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
uv sync
```

Installs:
- `mcp[cli]` - Model Context Protocol library
- `requests` - HTTP client library
- `types-requests` - Type stubs for requests

## Running the Project

### 1. Start the MCP Server

```bash
python server.py
```

Server starts on `http://localhost:8000`

### 2. Test with Client

```bash
python client.py
```

Shows available prompts and executes the format prompt with sample content.

## JSON-RPC Examples

### List Prompts

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "prompts/list",
  "id": 1,
  "params": {}
}
```

**Response (SSE format):**
```
event: message
data: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "prompts": [
      {
        "name": "format",
        "description": "Rewrites the contents of the document in Markdown format.",
        "arguments": [
          {
            "name": "doc_content",
            "description": "Contents of the document to format",
            "required": true
          }
        ]
      },
      {
        "name": "summarize",
        "description": "Summarizes the contents of the document.",
        "arguments": [
          {
            "name": "doc_content",
            "description": "Contents of the document to summarize",
            "required": true
          }
        ]
      }
    ]
  }
}
```

### Execute Prompt

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "prompts/get",
  "id": 2,
  "params": {
    "name": "format",
    "arguments": {
      "doc_content": "Agentic AI is a new paradigm in AI that is based on the idea that AI should be able to learn and adapt to new tasks and environments."
    }
  }
}
```

**Response (SSE format):**
```
event: message
data: {
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "description": "Rewrites the contents of the document in Markdown format.",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "\n    Your goal is to reformat a document to be written with markdown syntax.\n\n    The contents of the document you need to reformat is:\n    <document_content>\n    Agentic AI is a new paradigm in AI that is based on the idea that AI should be able to learn and adapt to new tasks and environments.\n    </document_content>\n\n    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.\n    After the document has been edited, respond with the final version of the doc. Don't explain your changes.\n    "
        }
      }
    ]
  }
}
```

## Transport Protocol

This implementation uses **stateless streamable HTTP transport** with Server-Sent Events (SSE):

- **Stateless**: Each request is independent, no session state maintained
- **Streamable**: Supports streaming responses via SSE format  
- **HTTP**: Standard HTTP POST requests to `/mcp/` endpoint

Response format:
```
event: message
data: {JSON-RPC response}
```

The client includes a `parse_sse_response()` function to extract JSON data from the SSE format.

## References

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [MCP Prompts Documentation](https://modelcontextprotocol.io/docs/concepts/prompts)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
