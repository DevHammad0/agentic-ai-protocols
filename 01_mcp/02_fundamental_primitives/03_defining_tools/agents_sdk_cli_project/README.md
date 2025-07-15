# MCP Chat

MCP Chat is a command-line interface application. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Any Chat Completions LLM API Key and Provider (i.e: Gemini)

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
LLM_API_KEY=""  # Enter your GEMINI API secret key
LLM_CHAT_COMPLETION_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
LLM_MODEL="gemini-2.0-flash"
```

### Step 2: Install dependencies

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv sync
```


4. Start MCP Server:
```bash
uv run mcp_server.py
```

5. Run the project with ChatAgent in CLI

```bash
uv run main.py
```

6. Optionally start inspector

```bash
npx @modelcontextprotocol/inspector
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model. The agent can now use MCP tools to read and edit documents.

### Tool-based Document Operations

The agent can now use tool calls to read and edit documents. You can ask the agent to:

- Read a specific document: `"Read the content of report.pdf"`
- Edit a document: `"Edit the deposition.md document and replace 'Angela Smith' with 'John Doe'"`

Available documents:
- `deposition.md` - Testimony of Angela Smith, P.E.
- `report.pdf` - Details of a 20m condenser tower
- `financials.docx` - Project budget and expenditures
- `outlook.pdf` - Projected future performance of the system
- `plan.md` - Project implementation steps
- `spec.txt` - Technical requirements for equipment

### Document Retrieval (Not Yet Implemented)

**Note:** Document retrieval using the @ symbol is not yet implemented as prompts and resources are not fully implemented.

~~Use the @ symbol followed by a document ID to include document content in your query:~~

```
> Tell me about @deposition.md  # This won't work yet
```

### Commands (Not Yet Implemented)

**Note:** Commands using the / prefix are not yet implemented as prompts and resources are not fully implemented.

~~Use the / prefix to execute commands defined in the MCP server:~~

```
> /summarize deposition.md  # This won't work yet
```

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`
3. Implement prompts and resources for @ document retrieval and / commands

### Linting and Typing Check

There are no lint or type checks implemented.
