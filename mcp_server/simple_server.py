#!/usr/bin/env python3
"""
Simple MCP (Model Context Protocol) Server
A lightweight implementation without heavy dependencies
"""

import json
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class MCPRequest:
    """MCP Protocol Request Structure"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: str = ""
    params: Dict[str, Any] = None

    def __post_init__(self):
        if self.params is None:
            self.params = {}


@dataclass
class MCPResponse:
    """MCP Protocol Response Structure"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


class SimpleMCPServer:
    """Simple MCP Server Implementation"""

    def __init__(self):
        self.tools = {
            "echo": self._echo_tool,
            "get_time": self._get_time_tool,
            "health": self._health_tool
        }
        self.server_info = {
            "name": "simple-mcp-server",
            "version": "1.0.0",
            "protocol_version": "2024-11-05"
        }

    def _echo_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Echo tool - returns the input message"""
        message = params.get("message", "")
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Echo: {message}"
                }
            ]
        }

    def _get_time_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get current time tool"""
        current_time = datetime.now().isoformat()
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Current time: {current_time}"
                }
            ]
        }

    def _health_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Health check tool"""
        return {
            "content": [
                {
                    "type": "text",
                    "text": "Server is healthy and running"
                }
            ]
        }

    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "protocolVersion": self.server_info["protocol_version"],
            "capabilities": {
                "tools": {
                    "listChanged": False
                }
            },
            "serverInfo": self.server_info
        }

    def handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools = []
        for tool_name in self.tools.keys():
            if tool_name == "echo":
                tools.append({
                    "name": "echo",
                    "description": "Echo back the provided message",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Message to echo back"
                            }
                        },
                        "required": ["message"]
                    }
                })
            elif tool_name == "get_time":
                tools.append({
                    "name": "get_time",
                    "description": "Get the current server time",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                })
            elif tool_name == "health":
                tools.append({
                    "name": "health",
                    "description": "Check server health status",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                })

        return {"tools": tools}

    def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        tool_params = params.get("arguments", {})

        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        return self.tools[tool_name](tool_params)

    def process_request(self, request_data: str) -> str:
        """Process incoming MCP request"""
        try:
            request_json = json.loads(request_data)
            request = MCPRequest(**request_json)

            # Handle different method types
            if request.method == "initialize":
                result = self.handle_initialize(request.params)
            elif request.method == "tools/list":
                result = self.handle_tools_list(request.params)
            elif request.method == "tools/call":
                result = self.handle_tools_call(request.params)
            else:
                raise ValueError(f"Unknown method: {request.method}")

            response = MCPResponse(id=request.id, result=result)
            return json.dumps(asdict(response))

        except Exception as e:
            error_response = MCPResponse(
                id=request_json.get("id") if 'request_json' in locals() else None,
                error={
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            )
            return json.dumps(asdict(error_response))


def main():
    """Main server loop for stdio transport"""
    server = SimpleMCPServer()

    # Print server info to stderr for debugging
    print(f"Starting {server.server_info['name']} v{server.server_info['version']}", file=sys.stderr)
    print("Listening on stdin/stdout...", file=sys.stderr)

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            response = server.process_request(line)
            print(response, flush=True)

    except KeyboardInterrupt:
        print("Server shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()