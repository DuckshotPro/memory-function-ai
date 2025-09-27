from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .adapters.gemini import GeminiAdapter
from .adapters.base import BaseAdapter
from .database.db import db_pool
from .database.schema import Conversation, Message
from .embedding import generate_embedding
from .search import find_relevant_messages
from .summarize import summarize_messages
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title="MCP Server")

# Database and LLM Adapter setup
llm_adapter: BaseAdapter = GeminiAdapter()

class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str

class SearchRequest(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    # In a real app, you would properly manage the pool
    # For this example, we assume db.py handles it
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles a chat message, saves it, and returns a response from the LLM with context injection."""
    # 1. Find relevant past messages
    relevant_messages = await find_relevant_messages(request.message)

    # 2. Summarize the messages if any are found
    context_summary = ""
    if relevant_messages:
        context_summary = await summarize_messages(relevant_messages, llm_adapter)

    # 3. Construct the prompt for the LLM
    prompt = request.message
    if context_summary:
        prompt = f"""Based on the following context from past conversations, please answer the user's question.

        Context:
        ---
        {context_summary}
        ---

        User's question: {request.message}"""

    # 4. Get response from LLM
    llm_response_text = await llm_adapter.send_message(prompt)

    # 5. Save the new exchange to the database
    async with db_pool.acquire() as connection:
        async with connection.transaction():
            conv_id = request.conversation_id
            if not conv_id:
                new_conv = await connection.fetchrow('INSERT INTO conversations DEFAULT VALUES RETURNING id')
                conv_id = new_conv['id']

            user_embedding = await generate_embedding(request.message)
            await connection.execute(
                'INSERT INTO messages (conversation_id, role, content, embedding) VALUES ($1, $2, $3, $4)',
                conv_id, 'user', request.message, user_embedding
            )

            assistant_embedding = await generate_embedding(llm_response_text)
            await connection.execute(
                'INSERT INTO messages (conversation_id, role, content, embedding) VALUES ($1, $2, $3, $4)',
                conv_id, 'assistant', llm_response_text, assistant_embedding
            )

            return {"conversation_id": conv_id, "response": llm_response_text, "context_used": bool(context_summary)}

@app.post("/search")
async def search(request: SearchRequest):
    """Performs semantic search over past conversations."""
    relevant_messages = await find_relevant_messages(request.query)
    return {"results": [{"role": msg.role, "content": msg.content, "conversation_id": msg.conversation_id} for msg in relevant_messages]}

@app.get("/")
def read_root():
    """Root endpoint for the MCP Server."""
    return {"message": "MCP Server is running. Go to /docs for API documentation."}