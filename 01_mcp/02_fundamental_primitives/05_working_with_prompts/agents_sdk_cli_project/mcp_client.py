import sys
import asyncio
import json
from pydantic import AnyUrl
from typing import Optional, Any
from contextlib import AsyncExitStack
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:
    def __init__(
        self,
        server_url: str,
    ):
        self._server_url = server_url
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    async def connect(self):
        streamable_transport = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        _read, _write, _get_session_id = streamable_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read, _write)
        )
        await self._session.initialize()

    def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError(
                "Client session not initialized or cache not populated. Call connect_to_server first."
            )
        return self._session

    async def list_tools(self) -> list[types.Tool]:
        # Core function: Retrieve the list of tools from the MCP server.
        # This follows the MCP client lifecycle (see MCP Lifecycle Specification: https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)
        result = await self.session().list_tools()
        return result.tools

    async def call_tool(
        self, tool_name: str, tool_input: dict
    ) -> types.CallToolResult | None:
        # Core function: Execute a specific tool on the MCP server using its name and input parameters.
        # This call is part of the MCP lifecycle's Operation phase.
        return await self.session().call_tool(tool_name, tool_input)

    async def list_prompts(self) -> list[types.Prompt]:
        # Return a list of prompts defined by the MCP server
        
        result = await self.session().list_prompts()
        return result.prompts
        

    async def get_prompt(self, prompt_name, args: dict[str, str]):
        # Get a particular prompt defined by the MCP server
        
        result = await self.session().get_prompt(prompt_name,args)
        return result.messages

    async def read_resource(self, uri: str) -> Any:
        # TODO: Read a resource, parse the contents and return it
        result = await self.session().read_resource(AnyUrl(uri))
        resource = result.contents[0]

        if isinstance(resource, types.TextResourceContents):
            if resource.mimeType == "application/json":
                return json.loads(resource.text)

        return resource

    async def cleanup(self):
        await self._exit_stack.aclose()
        self._session = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()

# ----------------------------------------------------------------------
# MCP Lifecycle Overview:
# This MCPClient class adheres to the MCP lifecycle for robust connection management.
# - Initialization: The connect() method sets up the client session.
# - Operation: Core functions like list_tools() and call_tool() enable tool invocations.
# - Shutdown: The cleanup() method ensures the connection is gracefully closed.
#
# To test your implementation, run main.py to start the chat agent and see your tools in action.
# ----------------------------------------------------------------------

# For testing


async def main():
    async with MCPClient(
        server_url="http://localhost:8000/mcp/",
    ) as _client:
        # Example usage:
        # Retrieve and print available tools to verify the client implementation.
        print("Listing prompts...")
        prompts = await _client.list_prompts()
        for i,prompt in enumerate(prompts):
            print(f"Prompt {i+1}: {prompt.name}")
            print(f"Description: {prompt.description}")
            print("-" * 50)
       
            
        print("=" * 50)  # Add separator after listing prompts section

        
        # Example usage:
        # Test getting a prompt
        print("Getting prompt...")
        prompt = await _client.get_prompt("format", {"doc_id": "report.pdf"})
        print(f"Prompt: {prompt[0].content.text}")
        print("-" * 50)
        
        
if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
