#!/usr/bin/env python3
"""
Test script for the Simple MCP Server
"""

import json
import subprocess
import sys
import time
from typing import Dict, Any


def send_mcp_request(server_process, method: str, params: Dict[str, Any] = None, request_id: str = "1") -> Dict[str, Any]:
    """Send MCP request to server and get response"""
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params or {}
    }

    request_json = json.dumps(request) + '\n'
    server_process.stdin.write(request_json.encode())
    server_process.stdin.flush()

    response_line = server_process.stdout.readline()
    return json.loads(response_line.decode().strip())


def test_mcp_server():
    """Test the MCP server functionality"""
    print("Starting MCP Server test...")

    # Start the server process
    server_process = subprocess.Popen(
        [sys.executable, "simple_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="/data/data/com.termux/files/home/mcp_server"
    )

    try:
        # Give server a moment to start
        time.sleep(0.5)

        # Test 1: Initialize
        print("\n1. Testing initialize...")
        response = send_mcp_request(server_process, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        print(f"Initialize response: {json.dumps(response, indent=2)}")

        # Test 2: List tools
        print("\n2. Testing tools/list...")
        response = send_mcp_request(server_process, "tools/list")
        print(f"Tools list: {json.dumps(response, indent=2)}")

        # Test 3: Call echo tool
        print("\n3. Testing echo tool...")
        response = send_mcp_request(server_process, "tools/call", {
            "name": "echo",
            "arguments": {
                "message": "Hello, MCP Server!"
            }
        })
        print(f"Echo response: {json.dumps(response, indent=2)}")

        # Test 4: Call get_time tool
        print("\n4. Testing get_time tool...")
        response = send_mcp_request(server_process, "tools/call", {
            "name": "get_time",
            "arguments": {}
        })
        print(f"Get time response: {json.dumps(response, indent=2)}")

        # Test 5: Call health tool
        print("\n5. Testing health tool...")
        response = send_mcp_request(server_process, "tools/call", {
            "name": "health",
            "arguments": {}
        })
        print(f"Health response: {json.dumps(response, indent=2)}")

        print("\nAll tests completed successfully!")

    except Exception as e:
        print(f"Test failed: {e}")
        # Print any stderr output
        stderr_output = server_process.stderr.read().decode()
        if stderr_output:
            print(f"Server stderr: {stderr_output}")

    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    test_mcp_server()