# Simple MCP Server

A lightweight Model Context Protocol (MCP) server implementation for Termux/Android environments.

## Features

- **Simple MCP Protocol**: Implements core MCP functionality without heavy dependencies
- **Built-in Tools**: Echo, time, and health check tools included
- **Stdio Transport**: Uses stdin/stdout for communication (standard MCP transport)
- **Termux Compatible**: Works reliably in Termux environment
- **Easy Testing**: Includes comprehensive test suite

## Quick Start

### 1. Test the Server

```bash
cd mcp_server
python3 test_simple_server.py
```

### 2. Run the Server

```bash
cd mcp_server
./run_server.sh
```

Or directly:

```bash
cd mcp_server
python3 simple_server.py
```

## Available Tools

### echo
- **Description**: Echo back the provided message
- **Parameters**:
  - `message` (string, required): Message to echo back

### get_time
- **Description**: Get the current server time
- **Parameters**: None

### health
- **Description**: Check server health status
- **Parameters**: None

## MCP Protocol Support

This server implements MCP protocol version `2024-11-05` with the following capabilities:

- `initialize`: Server initialization
- `tools/list`: List available tools
- `tools/call`: Execute tools

## Integration with Claude Code

To use this MCP server with Claude Code:

1. Add server configuration to your Claude Code settings
2. Use stdio transport with the server executable path
3. The server will handle MCP protocol communication automatically

Example configuration:
```json
{
  "mcpServers": {
    "simple-mcp": {
      "command": "python3",
      "args": ["/data/data/com.termux/files/home/mcp_server/simple_server.py"]
    }
  }
}
```

## Files

- `simple_server.py`: Main MCP server implementation
- `test_simple_server.py`: Test suite
- `run_server.sh`: Startup script
- `.env`: Environment configuration
- `README.md`: This documentation

## Development

To extend the server with new tools:

1. Add tool implementation to the `tools` dictionary in `SimpleMCPServer.__init__()`
2. Add tool definition to `handle_tools_list()`
3. Test with the included test suite

## Requirements

- Python 3.6+
- No external dependencies required for the simple server
- FastAPI/uvicorn available for future HTTP transport (optional)