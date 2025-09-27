import pytest
from httpx import AsyncClient
from mcp_server.mcp.server import app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MCP Server is running. Go to /docs for API documentation."}
