# Memory Function AI

This project is a context-aware, multi-purpose conversational platform (MCP) designed to give Large Language Models (LLMs) a persistent memory. It uses semantic search over a conversation history to provide relevant context to the LLM with each new prompt.

## Architecture Overview

The system consists of two main services:

1.  **`mcp_server`**: The main conversational server. It exposes a `/chat` API that takes a user's message, finds relevant past conversations from the database, summarizes them, injects them into a prompt, and returns a context-aware response from the LLM. It also provides a `/search` endpoint for semantic search.

2.  **`conversation_feeder`**: A lightweight microservice for ingesting conversation data into the database. It provides a simple web UI for manual entry and a secure REST API for programmatic ingestion.

### Tech Stack

*   **Backend**: Python, FastAPI
*   **Database**: PostgreSQL with `pgvector` for vector similarity search (designed for Neon.tech)
*   **LLM Integration**: Google Gemini (`gemini-pro` for chat, `embedding-001` for embeddings)
*   **Testing**: `pytest`
*   **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites

*   Python 3.10+
*   A PostgreSQL database with the `pgvector` extension enabled (e.g., a free tier from [Neon](https://neon.tech/))
*   A Google Gemini API Key.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DuckshotPro/memory-function-ai.git
    cd memory-function-ai
    ```

2.  **Install dependencies for both services:**
    ```bash
    pip install -r mcp_server/requirements.txt
    pip install -r conversation_feeder/requirements.txt
    ```

### Configuration

You need to configure environment variables for both services.

1.  **Main Server (`mcp_server`):**
    ```bash
    cp mcp_server/.env.example mcp_server/.env
    ```
    Now, edit `mcp_server/.env` and add your credentials:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    DATABASE_URL="YOUR_POSTGRESQL_CONNECTION_STRING"
    ```

2.  **Feeder Service (`conversation_feeder`):**
    ```bash
    cp conversation_feeder/.env.example conversation_feeder/.env
    ```
    Edit `conversation_feeder/.env` and add your credentials and a secret token:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    DATABASE_URL="YOUR_POSTGRESQL_CONNECTION_STRING"
    FEEDER_AUTH_TOKEN="CHOOSE_A_SECRET_TOKEN"
    ```

### Running the Application

1.  **Apply Database Migrations:**
    Before running either service, you need to create the tables in your database.
    ```bash
    alembic -c mcp_server/alembic.ini upgrade head
    ```

2.  **Run the Conversation Feeder (Optional):**
    If you want to manually add data, run the feeder service.
    ```bash
    uvicorn conversation_feeder.main:app --reload
    ```
    You can access the web UI at `http://127.0.0.1:8000`.

3.  **Run the Main MCP Server:**
    ```bash
    uvicorn mcp_server.main:app --reload
    ```
    The main API will be running at `http://127.0.0.1:8000`.

## API Usage

### Chat Endpoint

Send a message to the chat endpoint. The server will automatically handle context.

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{
  "message": "What did we talk about earlier regarding databases?"
}'
```

### Search Endpoint

Directly search for relevant messages from the history.

```bash
curl -X POST "http://127.0.0.1:8000/search" \
-H "Content-Type: application/json" \
-d '{
  "query": "AI for databases"
}'
```

