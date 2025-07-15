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
├── server.py                              # MCP server implementation
├── client.py                              # MCP client implementation  
├── Hello_MCP_Server.postman_collection.json # Postman collection for API testing
├── pyproject.toml                         # Project dependencies
├── .python-version                        # Python 3.13 requirement
└── README.md                              # This file
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

### Expected Output:
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



## 🧪 Testing with Postman (Alternative Method)

For a more interactive testing experience, use the included Postman collection:

### Step 1: Import the Collection
1. Open **Postman**
2. Click **Import** → **Files** → Select `Hello_MCP_Server.postman_collection.json`
3. The collection will appear with 3 requests

### Step 2: Start the Server
```bash
uv run server.py
```
✅ Server runs at `http://localhost:8000` (collection pre-configured)

### Step 3: Test the MCP Protocol Flow
Run these requests **in sequence**:

1. **01. Initialize Session**
   - Establishes MCP protocol connection
   - Required first step per MCP 2025-06-18 spec

2. **02. Send Initialized Notification** 
   - Completes the MCP session setup
   - Required after successful initialization

3. **03. List Available Tools**
   - Queries what tools the server provides
   - Returns `{"tools": []}` (no tools in this basic demo)

### Expected Postman Responses:
```json
// 01. Initialize Session
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "2025-06-18",
    "serverInfo": {"name": "hello-server"},
    "capabilities": {}
  },
  "id": 1
}

// 02. Send Initialized Notification
// (No response - it's a notification)

// 03. List Available Tools  
{
  "jsonrpc": "2.0",
  "result": {"tools": []},
  "id": 3
}
```

**🎯 Why Use Postman?**
- Interactive testing of MCP protocol
- Clear visualization of JSON-RPC requests/responses
- Easy experimentation with different parameters
- Better understanding of the full MCP lifecycle


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