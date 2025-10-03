#!/usr/bin/env python3
"""
Test script for the aihehuo-mcp server
"""
import json
import subprocess
import sys
from typing import Dict, Any

def send_mcp_request(method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Send an MCP request to the server via STDIO"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    
    # Start the server process
    process = subprocess.Popen(
        ["uvx", "--from", ".", "python", "-m", "aihehuo_mcp.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send the request
    request_json = json.dumps(request) + "\n"
    stdout, stderr = process.communicate(input=request_json, timeout=10)
    
    # Parse response
    try:
        response = json.loads(stdout.strip())
        return response
    except json.JSONDecodeError:
        return {"error": f"Failed to parse response: {stdout}", "stderr": stderr}

def test_server_info():
    """Test the server_info tool"""
    print("Testing server_info...")
    response = send_mcp_request("tools/call", {
        "name": "server_info",
        "arguments": {}
    })
    print(f"Response: {json.dumps(response, ensure_ascii=False, indent=2)}")
    return response

def test_search_members():
    """Test the search_members tool"""
    print("\nTesting search_members...")
    response = send_mcp_request("tools/call", {
        "name": "search_members",
        "arguments": {
            "query": "测试",
            "paginate": {"page": 1, "per": 10}
        }
    })
    print(f"Response: {json.dumps(response, ensure_ascii=False, indent=2)}")
    return response

def test_list_tools():
    """Test listing available tools"""
    print("\nTesting tools/list...")
    response = send_mcp_request("tools/list")
    print(f"Response: {json.dumps(response, ensure_ascii=False, indent=2)}")
    return response

if __name__ == "__main__":
    print("🧪 Testing aihehuo-mcp server...")
    print("=" * 50)
    
    # Test 1: List tools
    test_list_tools()
    
    # Test 2: Server info
    test_server_info()
    
    # Test 3: Search members (this will fail without proper API key)
    test_search_members()
    
    print("\n✅ Testing complete!")
