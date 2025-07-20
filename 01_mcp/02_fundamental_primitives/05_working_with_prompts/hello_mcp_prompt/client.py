import requests 
import json

url = "http://localhost:8000/mcp/"

headers = {"Accept": "application/json,text/event-stream"}

def get_body(method: str, params: dict = {}, id: int = 1):
    return {
        "jsonrpc": "2.0",
        "method": method,
        "id": id,
        "params": params,
    }

def parse_sse_response(response_text: str):
    """Parse Server-Sent Events response to extract JSON data"""
    lines = response_text.strip().split('\n')
    for line in lines:
        if line.startswith('data: '):
            return json.loads(line[6:])  # Remove 'data: ' prefix
    return None

print("Listing prompts...")

response_list = requests.post(url, headers=headers, json=get_body("prompts/list", id=1))
print("Raw response:", response_list.text)

# Parse and display prompts nicely
data = parse_sse_response(response_list.text)
if data and 'result' in data and 'prompts' in data['result']:
    print("\n=== Available Prompts ===")
    for prompt in data['result']['prompts']:
        print(f"\nName: {prompt['name']}")
        print(f"Description: {prompt['description']}")
else:
    print("No prompts found or invalid response format")
print("\n")
print("="*60)

print("Reading prompt...")

response_read = requests.post(url, headers=headers, json=get_body("prompts/get", {"name": "format", "arguments": {"doc_content": "Agentic AI is a new paradigm in AI that is based on the idea that AI should be able to learn and adapt to new tasks and environments."}}, id=2))
print("Raw response:", response_read.text)

# Parse and display prompt response nicely
data = parse_sse_response(response_read.text)
if data and 'result' in data:
    result = data['result']
    print("\n=== Prompt Response ===")
    print(f"Description: {result.get('description', 'N/A')}")
    
    if 'messages' in result:
        print("\nMessages:")
        for i, message in enumerate(result['messages'], 1):
            print(f"\n  Message {i}:")
            print(f"    Role: {message.get('role', 'N/A')}")
            if 'content' in message and 'text' in message['content']:
                print(f"    Content: {message['content']['text']}")
else:
    print("No prompt data found or invalid response format")