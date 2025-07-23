import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams, ToolFilterContext

from agents.run_context import RunContextWrapper

set_tracing_disabled(True)

_: bool = load_dotenv(find_dotenv())

# URL of our standalone MCP server (from shared_mcp_server)
MCP_SERVER_URL = "http://localhost:8001/mcp/" # Ensure this matches your running server

gemini_api_key = os.getenv("GEMINI_API_KEY")

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

def custom_filter(context: ToolFilterContext, tool) -> bool:
    # Only allow tools that start with "mood"
    print(f"\n\nContext: {context}\n\n")
    print(f"Tool: {tool.name}, Is Allowed: {tool.name.startswith("mood")}")
    return tool.name.startswith("mood")

def context_aware_filter(context: ToolFilterContext, tool) -> bool:
    # Only allow tools for a specific agent
    # print(f"\n\nContext: {context}\n\n")
    print(f"Filtering: {tool.name}")
    print(f"Tool: {tool.name}, Is Allowed: {context.agent.name == 'MyMCPConnectedAssistant' and tool.name == 'mood_from_shared_server'}")
    return context.agent.name == "MyMCPConnectedAssistant" and tool.name == "mood_from_shared_server"


async def main():
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
    async with MCPServerStreamableHttp(params=mcp_params, name="MySharedMCPServerClient", 
    tool_filter=context_aware_filter, 
    # tool_filter=custom_filter,
    cache_tools_list=True,
    ) as mcp_server_client:
        print(f"[INFO] MCPServerStreamableHttp client '{mcp_server_client.name}' created and entered context.")

        try:
            assistant = Agent(
                name="MyMCPConnectedAssistant",
                mcp_servers=[mcp_server_client],
                model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client),
                instructions="You are a helpful assistant that can use tools to share information.",
            )

            # run_ctx = RunContextWrapper(context=None)
            # tools = await mcp_server_client.list_tools(run_ctx, assistant)
            # print(f"\n\n[TOOLS]: {[tool.name for tool in tools]}\n\n")

            # # First query
            query_1 = "Share Junaid's mood?"
            print(f"\n\n[QUERY]: {query_1}")
            result = await Runner.run(assistant, query_1)
            print(f"\n\n[AGENT RESPONSE]: {result.final_output}")
            
            # # Second query
            # query_2 = "hello, how are you?"
            # print(f"\n\n[QUERY]: {query_2}")
            # result = await Runner.run(assistant, query_2)
            # print(f"\n\n[AGENT RESPONSE]: {result.final_output}")
            
            # # Third query
            # # query_3 = "call get_time tool to get the current time"
            # query_3 =  "Share Junaid's mood?"
            # print(f"\n\n[QUERY]: {query_3}")
            # # mcp_server_client.invalidate_tools_cache()
            # result = await Runner.run(assistant, query_3)
            # print(f"\n\n[AGENT RESPONSE]: {result.final_output}")

        except Exception as e:
            print(f"An error occurred during agent setup or tool listing: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An unhandled error occurred in the agent script: {e}")
