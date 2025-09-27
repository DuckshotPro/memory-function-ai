#!/bin/bash

# MCP Server Startup Script

echo "Starting MCP Server..."

# Check if we're in the right directory
if [ ! -f "simple_server.py" ]; then
    echo "Error: simple_server.py not found. Please run from mcp_server directory."
    exit 1
fi

# Run the simple MCP server
echo "Running Simple MCP Server (stdio transport)..."
echo "Server is ready for MCP client connections"
echo "Press Ctrl+C to stop"
python3 simple_server.py