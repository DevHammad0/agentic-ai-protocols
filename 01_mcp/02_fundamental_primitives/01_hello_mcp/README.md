# 🚀 Hello MCP - Basic Server & Client Demo

A minimal demonstration of **Model Context Protocol (MCP)** showing how to create a basic server and client using Python 3.13.

## 🎯 What This Demonstrates

- **MCP Server**: A minimal stateless HTTP server using FastMCP
- **MCP Client**: A simple client that queries server capabilities  
- **JSON-RPC Communication**: Shows the underlying protocol structure
- **Streaming Responses**: Handles MCP's streaming data format

## 📂 Project Structure

```
01_hello_mcp/
├── server.py          # MCP server implementation
├── client.py          # MCP client implementation  
├── pyproject.toml     # Project dependencies
├── .python-version    # Python 3.13 requirement
└── README.md          # This file
```

## 🔧 Setup & Installation

1. **Ensure Python 3.13 is installed**
2. **Install dependencies:**
   ```bash
   uv sync
   ```

## 🏃‍♂️ Running the Demo

### Step 1: Start the Server
```bash
uv run server.py
```
✅ Server starts at `http://localhost:8000`

### Step 2: Run the Client
```bash
uv run client.py
```

## 📋 Expected Output

**Client Output:**
```
[Step 1: Ask the server what it can do]
We send a 'tools/list' request to discover available tools.
   -> Sending tools/list request...
   <- Received raw data: data: {"jsonrpc": "2.0", "result": {"tools": []}, "id": 1}
   <- Received data: {"jsonrpc": "2.0", "result": {"tools": []}, "id": 1}

RESULT OF TOOLS:  {'jsonrpc': '2.0', 'result': {'tools': []}, 'id': 1}
```

**Key Points:**
- Server responds with empty `tools: []` (no tools implemented yet)
- Communication uses JSON-RPC 2.0 protocol
- Data streams as newline-delimited JSON

## 🔍 Understanding the Code

### Server (`server.py`)
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="hello-server",
    stateless_http=True  # No handshake needed
)
```
- Creates a minimal MCP server
- `stateless_http=True` simplifies communication (no initialization handshake)

### Client (`client.py`)
```python
payload = {
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 1
}
```
- Sends JSON-RPC requests to MCP server
- Handles streaming responses line by line
- Demonstrates basic MCP protocol interaction

## 🎓 Learning Outcomes

After running this demo, you'll understand:
1. **MCP Server Setup**: How to create a basic MCP server
2. **Client Communication**: How to query MCP servers via HTTP
3. **JSON-RPC Protocol**: The underlying message format
4. **Streaming Responses**: How MCP sends data back to clients

## 🔗 Next Steps

This is a foundation. To build on this:
- Add tools to the server (functions the client can call)
- Implement resources (data the server can provide)
- Add prompts (templates the server can offer)

---

**Dependencies:** Python 3.13, MCP library, httpx, uvicorn