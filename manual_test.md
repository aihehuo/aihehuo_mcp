# Manual Testing Guide for aihehuo-mcp Server

## Method 1: Start Server and Test with Echo

1. **Start the server:**
   ```bash
   uvx --from . python -m aihehuo_mcp.server
   ```

2. **In another terminal, test with echo:**
   ```bash
   # Test 1: List tools
   echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uvx --from . python -m aihehuo_mcp.server
   
   # Test 2: Get server info
   echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "server_info", "arguments": {}}}' | uvx --from . python -m aihehuo_mcp.server
   
   # Test 3: Search members (requires API key)
   echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "测试", "paginate": {"page": 1, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server
   ```

## Method 2: Using MCP Client

If you have an MCP client (like in Cursor or other MCP-compatible tools), you can:

1. Configure the MCP server with:
   - **Command:** `uvx --from . python -m aihehuo_mcp.server`
   - **Working Directory:** `/Users/yc/workspace/aihehuo/aihehuo_mcp`
   - **Environment Variables:** 
     - `AIHEHUO_API_KEY=your_actual_api_key`
     - `AIHEHUO_API_BASE=https://new-api.aihehuo.com` (optional)

2. The server will provide these tools:
   - `server_info()` - Health check and server information
   - `search_members(params)` - Search for 爱合伙 members

## Method 3: Test with Environment Variables

Set up your API key and test:

```bash
export AIHEHUO_API_KEY="your_actual_api_key_here"
uvx --from . python -m aihehuo_mcp.server
```

Then use Method 1 to send test requests.

## Expected Results

- **server_info()** should return server metadata
- **search_members()** should return search results (or error if API key is invalid)
- Both tools should be listed in `tools/list` response
