from fastapi import FastAPI
from .adapters.gemini import GeminiAdapter
from .adapters.base import BaseAdapter

app = FastAPI(title="MCP Server")

# In a real app, you might have a factory or a more dynamic way to select this
llm_adapter: BaseAdapter = GeminiAdapter()

@app.post("/chat")
async def chat(message: str):
    """Receives a message and returns a response from the configured LLM."""
    response = await llm_adapter.send_message(message)
    return {"response": response}

@app.get("/")
def read_root():
    """Root endpoint for the MCP Server."""
    return {"message": "MCP Server is running. Go to /docs for API documentation."}
