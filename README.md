# Memory Function AI

This project is a context-aware, multi-purpose conversational platform (MCP) designed to give Large Language Models (LLMs) a persistent memory. It uses semantic search over a conversation history to provide relevant context to the LLM with each new prompt.

## Architecture Overview

The system consists of two main services:

1.  **`mcp_server`**: The main conversational server. It exposes a `/chat` API that takes a user's message, finds relevant past conversations from the database, summarizes them, injects them into a prompt, and returns a context-aware response from the LLM. It also provides a `/search` endpoint for semantic search.

2.  **`conversation_feeder`**: A lightweight microservice for ingesting conversation data into the database. It provides a simple web UI for manual entry and a secure REST API for programmatic ingestion.

### Tech Stack

*   **Backend**: Python, FastAPI
*   **Database**: PostgreSQL with `pgvector` for vector similarity search.
*   **LLM Integration**: Google Gemini (`gemini-pro` for chat, `embedding-001` for embeddings)
*   **Deployment**: Docker, Render

## Deployment

This project is designed to be deployed on the [Render](https://render.com/) cloud platform via the provided `render.yaml` configuration.

**For detailed, step-by-step deployment instructions, please see the [Deployment Guide](DEPLOYMENT.md).**

## API Usage

Once deployed, the API endpoints will be available at the URL provided by Render for the `mcp-server` service.

### Chat Endpoint

```bash
curl -X POST "https://your-mcp-server-url.onrender.com/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "What did we talk about earlier regarding databases?"
}'
```

### Search Endpoint

```bash
curl -X POST "https://your-mcp-server-url.onrender.com/search" \
-H "Content-Type: application/json" \
-d '{
  "query": "AI for databases"
}'
```