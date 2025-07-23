# 🧠 Context-Aware Tool Filtering with MCP Agent

This README documents the internal flow and reasoning behind how tool filtering works in an MCP agent setup using the `ToolFilterContext`. It explains when the tool list is fetched, how filtering is applied, and what happens during tool invocation.

---

## 📦 Project Overview

You have an agent connected to a shared MCP tool server. The agent is designed to **only allow specific tools** based on custom logic.

### 🔧 Example Tools

* `greet_from_shared_server`
* `mood_from_shared_server`

Only the tool `mood_from_shared_server` should be available to the agent named `"MyMCPConnectedAssistant"`.

---

## 🛠️ Filtering Logic

```python
def context_aware_filter(context: ToolFilterContext, tool) -> bool:
    print(f"Filtering: {tool.name}")
    print(f"Tool: {tool.name}, Is Allowed: {context.agent.name == 'MyMCPConnectedAssistant' and tool.name == 'mood_from_shared_server'}")
    return context.agent.name == "MyMCPConnectedAssistant" and tool.name == "mood_from_shared_server"
```

This function checks whether:

* The agent name matches `"MyMCPConnectedAssistant"`
* The tool name is `"mood_from_shared_server"`

If both are true, the tool is **allowed** (i.e., `True` is returned); otherwise, it's **filtered out**.

---

## 🔄 Execution Flow

### ✅ Step-by-Step Breakdown

1. **Agent Run is Triggered**

   ```python
   result = await Runner.run(assistant, query)
   ```

2. **First-Time Tool Listing Request**

   * A `ListToolsRequest` is made to the server (only once per agent session due to caching).
   * This fetches all tools from the MCP server.

3. **Filter Applied to Each Tool**

   * The `context_aware_filter` function is run **once for each tool**.
   * Output shows something like:

     ```
     Filtering: greet_from_shared_server
     Tool: greet_from_shared_server, Is Allowed: False
     Filtering: mood_from_shared_server
     Tool: mood_from_shared_server, Is Allowed: True
     ```

4. **If Tool Usage is Needed** (e.g., query: "Share Junaid's mood?")

   * Agent plans a tool call.
   * **Filter is re-applied** on the cached tool list to ensure the selected tool is still allowed.
   * This leads to a second set of `Filtering:` logs.

5. **If Tool Usage is NOT Needed** (e.g., "hello, how are you?")

   * No tool is called.
   * Only **one** round of filtering happens.

---

## 🧪 Example Run

### 🔹 Query 1: Tool Required

```python
query_1 = "Share Junaid's mood?"
```

#### Output:

```
[QUERY]: Share Junaid's mood?
Filtering: greet_from_shared_server  ←× filtered
Filtering: mood_from_shared_server   ←✓ allowed
Filtering: greet_from_shared_server  ←× filtered
Filtering: mood_from_shared_server   ←✓ allowed

[AGENT RESPONSE]: Junaid is happy.
```

✅ Tool filter applied twice:

* Once when fetching tool list
* Once when deciding whether to call a tool

---

### 🔹 Query 2: No Tool Required

```python
query_2 = "hello, how are you?"
```

#### Output:

```
[QUERY]: hello, how are you?
Filtering: greet_from_shared_server  ←× filtered
Filtering: mood_from_shared_server   ←✓ allowed

[AGENT RESPONSE]: I am doing well, thank you for asking!
```

✅ Tool filter applied only once (no tool call needed)

---

## 🧠 Key Takeaways

| Concept                        | Behavior                                                              |
| ------------------------------ | --------------------------------------------------------------------- |
| First tool list request        | Happens once per session (cached afterward)                           |
| `ToolFilterContext` usage      | Provided automatically when filtering each tool                       |
| Filter re-applied on tool call | Yes, when a tool is about to be called, filter is re-applied on cache |
| Server log for ListToolRequest | Seen only once in logs if cache is used                               |
| Filtering on every agent run   | Yes, even for simple queries, to determine availability of tools      |

---

## ✅ Conclusion

Your understanding is **correct**. Here's a summary:

* **First call** to server returns tool list → **cached**
* **Filtering logic** is applied using `ToolFilterContext` to create filtered list
* **Filter re-applied** when tool is about to be invoked
* **Filtered list shows all tools**, but agent only uses those where filter returns `True`
* **ListToolsRequest** log appears **once per session** due to caching

