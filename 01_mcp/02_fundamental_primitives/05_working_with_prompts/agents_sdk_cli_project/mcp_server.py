from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR", stateless_http=True)

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    print(f"Reading document tool called with {doc_id}...")
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(
        description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(
        description="The new text to insert in place of the old text.")
):
    print(f"Editing document tool called with {doc_id}...")
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Successfully updated document {doc_id}"


@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    print(f"Listing resources called")
    return list(docs.keys())


@mcp.resource(
    "docs://{doc_id}",
    mime_type="text/plain"
)
def get_doc(doc_id: str) -> str:
    print(f"Getting document resource called with {doc_id}")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    
    print(f"Formatting document prompt called with {doc_id}...")
    
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
    Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
    """
    return [base.UserMessage(prompt)]



@mcp.prompt(
    name="summarize",
    description="summarizes the contents of the document."
)
def summarize_document(
    doc_id: str = Field(description="Id of the document to summarize")
) -> list :
    from mcp.types import PromptMessage, TextContent
    print(f"Summarizing document prompt called with {doc_id}...")

    prompt = f"""
    Your goal is to summarize a document.

    The id of the document you need to summarize is:
    <document_id>
    {doc_id}
    </document_id>

    Provide a concise summary of the document's contents, highlighting the key points and findings.
    """
    return [PromptMessage(role="user", content=TextContent(type="text", text=prompt))]


mcp_app = mcp.streamable_http_app()


if __name__ == "__main__":
    import uvicorn
    print("Starting MCP server...")
    uvicorn.run("mcp_server:mcp_app", host="0.0.0.0", port=8000, reload=True)