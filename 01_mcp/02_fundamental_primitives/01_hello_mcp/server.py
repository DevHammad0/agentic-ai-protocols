from mcp.server.fastmcp import FastMCP
import uvicorn

# Initialize FastMCP server with enhanced metadata for 2025-06-18 spec
mcp = FastMCP(
    name="hello-server",
    stateless_http=True # When true we don't need handshake or initialize things.
)

mcp_app = mcp.streamable_http_app()


if __name__ == "__main__":
    print("Starting MCP server...")
    uvicorn.run("server:mcp_app", host="0.0.0.0", port=8000, reload=True)