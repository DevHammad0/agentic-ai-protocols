## 🧪 Agent SDK Tool Listing Behavior (MCP Server)

This document outlines the behavior of the Agent SDK when connected to a shared MCP server, specifically focusing on how it interacts with tools (`tools/list` calls) during agent initialization and runtime.

---

### ✅ Setup Summary

* **Language:** Python
* **Agent SDK:** `agents` with `MCPServerStreamableHttp`
* **LLM:** Gemini via OpenAI-compatible API
* **MCP Server URL:** `http://localhost:8001/mcp/`
* **Agent config:** Uses `cache_tools_list` flag to control tool listing behavior

---

### 🔁 Normal Flow Without Caching

By default, when the agent is created **without** `cache_tools_list=True`, here’s what happens:

1. On **agent initialization**, the SDK sends a `tools/list` request to discover available tools.
2. On every **agent run**, the SDK again sends:

   * A `tools/list` before calling any tool.
   * The actual `tool/call` request(s).
   * Another `tools/list` after tool execution.
3. This means:

   * For a single question, you might see 3-4 repeated `tools/list` requests in the logs.
   * This creates noise and slight overhead in local or stable environments.

#### Example Logs (No Caching):

```
Processing request of type ListToolsRequest  ← during init
Processing request of type CallToolRequest   ← call 'moo'
Processing request of type ListToolsRequest  ← again
Processing request of type ListToolsRequest  ← again
Processing request of type CallToolRequest   ← call 'greet_from_shared_server'
Processing request of type ListToolsRequest  ← again
```

---

### ✅ Flow With Caching Enabled

When `cache_tools_list=True` is passed during agent creation:

* The SDK **fetches the tool list once** during initialization.
* All subsequent calls use the **cached tool schema**, and no additional `tools/list` requests are made during the agent’s run.

#### Example Logs (With Caching):

```
Processing request of type ListToolsRequest   ← during init only
Processing request of type CallToolRequest    ← call 'moo'
Processing request of type CallToolRequest    ← call 'greet_from_shared_server'
```

---

### 🔍 Why Does This Happen?

The SDK does repeated `tools/list` calls by default to:

* Ensure tools haven’t changed between runs.
* Validate tool schema before and after each execution.
* Support dynamic tool availability (if tools are registered/unregistered on the fly).

But in most dev/test setups, the tool list is static. So:

> **Using `cache_tools_list=True` is the recommended setting for stable environments.**

---

### 🧠 Key Takeaways

* Agent SDK is cautious by default — it doesn’t assume tool stability.
* Without caching: tool list is fetched multiple times per agent run.
* With caching: tool list is fetched once per agent lifecycle.
* You can safely enable caching if your tools are fixed at runtime.

---

### ✅ How to Enable Tool Caching

When creating the `Agent` instance:

```python
assistant = Agent(
    name="MyMCPConnectedAssistant",
    mcp_servers=[mcp_server_client],
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    cache_tools_list=True  # ← this is the key
)
```
