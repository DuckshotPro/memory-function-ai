import asyncio
import asyncpg
import google.generativeai as genai
from fastapi import FastAPI, Request, Depends, HTTPException, Security, Form
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
from typing import List

from config import settings

# --- Configuration & Globals ---
app = FastAPI(title="Conversation Feeder Service")
genai.configure(api_key=settings.gemini_api_key)

API_KEY_HEADER = APIKeyHeader(name="X-API-Token", auto_error=False)

# --- Pydantic Models ---
class Message(BaseModel):
    role: str
    content: str

class IngestionRequest(BaseModel):
    messages: List[Message]

# --- Authentication ---
async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header == settings.feeder_auth_token:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )

# --- Core Logic ---
async def generate_embedding(text: str) -> list[float]:
    try:
        result = await asyncio.to_thread(genai.embed_content, model='models/embedding-001', content=text)
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

async def save_conversation_to_db(messages: List[Message]):
    conn = await asyncpg.connect(dsn=settings.database_url)
    try:
        async with conn.transaction():
            # Create a new conversation record
            conv_id = await conn.fetchval('INSERT INTO conversations DEFAULT VALUES RETURNING id')

            # Generate embeddings and insert messages
            for msg in messages:
                embedding = await generate_embedding(msg.content)
                await conn.execute(
                    'INSERT INTO messages (conversation_id, role, content, embedding) VALUES ($1, $2, $3, $4)',
                    conv_id, msg.role, msg.content, embedding
                )
    finally:
        await conn.close()

# --- API Endpoints ---
@app.get("/")
async def read_root():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.post("/ingest-form")
async def ingest_from_form(transcript: str = Form(...)):
    messages = []
    try:
        for line in transcript.strip().split('\n'):
            role, content = line.split(':', 1)
            messages.append(Message(role=role.strip(), content=content.strip()))
    except ValueError:
        return HTMLResponse(content="<p class='error'>Failed to parse transcript. Ensure format is 'role: content'.</p>", status_code=400)
    
    await save_conversation_to_db(messages)
    return HTMLResponse(content="<p class='success'>Conversation ingested successfully!</p>")

@app.post("/api/ingest")
async def api_ingest(request: IngestionRequest, api_key: str = Depends(get_api_key)):
    """API endpoint to ingest a conversation with token-based authentication."""
    await save_conversation_to_db(request.messages)
    return {"status": "success", "message_count": len(request.messages)}
