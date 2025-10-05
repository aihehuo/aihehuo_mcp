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
   
   # Test 4: Search ideas (requires API key)
   echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "search_ideas", "arguments": {"query": "创业", "paginate": {"page": 1, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server
   
   # Test 5: Get group info (requires API key)
   echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "1233"}}}' | uvx --from . python -m aihehuo_mcp.server
   
   # Test 6: Update user bio (requires API key)
   echo '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "update_bio", "arguments": {"bio": "我是AI创业者，专注于人工智能技术研发"}}}' | uvx --from . python -m aihehuo_mcp.server
   
   # Test 7: Update user goal (requires API key)
   echo '{"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "update_goal", "arguments": {"goal": "寻找技术合伙人，共同开发AI产品"}}}' | uvx --from . python -m aihehuo_mcp.server
   
   # Test 8: Get current user profile (requires API key and CURRENT_USER_ID)
   echo '{"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "get_current_user", "arguments": {}}}' | uvx --from . python -m aihehuo_mcp.server
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
   - `search_ideas(params)` - Search for 爱合伙 ideas/projects
   - `get_group_info(params)` - Get group information and member data
   - `update_bio(params)` - Update user profile bio
   - `update_goal(params)` - Update user profile goal
   - `get_current_user_profile()` - Get current user profile information
   - `get_current_user_ideas(params)` - Get current user's ideas/projects
   - `get_idea_details(params)` - Get detailed information about a specific idea/project

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
- **search_ideas()** should return idea/project search results (or error if API key is invalid)
- **get_group_info()** should return group information and member data (or error if API key is invalid)
- **update_bio()** should update user bio and return success/error response
- **update_goal()** should update user goal and return success/error response
- **get_current_user_profile()** should return current user profile (or error if API key/CURRENT_USER_ID is invalid)
- **get_current_user_ideas()** should return current user's ideas (or error if API key/CURRENT_USER_ID is invalid)
- **get_idea_details()** should return detailed idea information (or error if API key/idea_id is invalid)
- All nine tools should be listed in `tools/list` response

## Test Examples

### Search Ideas Examples
```bash
# Search for startup ideas
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_ideas", "arguments": {"query": "AI创业", "paginate": {"page": 1, "per": 5}}}}' | uvx --from . python -m aihehuo_mcp.server

# Search for investment opportunities
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_ideas", "arguments": {"query": "投资", "paginate": {"page": 1, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server

# Search for business projects
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_ideas", "arguments": {"query": "电商", "paginate": {"page": 1, "per": 8}}}}' | uvx --from . python -m aihehuo_mcp.server
```

### Get Group Info Examples
```bash
# Get group information by ID
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "12345"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get another group's information
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "67890"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test with different group ID format
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "abc123"}}}' | uvx --from . python -m aihehuo_mcp.server
```

### Update Profile Examples
```bash
# Update user bio
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "update_bio", "arguments": {"bio": "我是AI创业者，专注于人工智能技术研发"}}}' | uvx --from . python -m aihehuo_mcp.server

# Update user goal
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "update_goal", "arguments": {"goal": "寻找技术合伙人，共同开发AI产品"}}}' | uvx --from . python -m aihehuo_mcp.server

# Update bio with different content
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "update_bio", "arguments": {"bio": "10年互联网经验，擅长产品设计和团队管理"}}}' | uvx --from . python -m aihehuo_mcp.server

# Update goal with different content
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "update_goal", "arguments": {"goal": "寻找投资机会，扩大业务规模"}}}' | uvx --from . python -m aihehuo_mcp.server
```

### Get Current User Examples
```bash
# Get current user profile (requires CURRENT_USER_ID env var)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_current_user_profile", "arguments": {}}}' | uvx --from . python -m aihehuo_mcp.server

# Get current user's ideas with default pagination (requires CURRENT_USER_ID env var)
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_current_user_ideas", "arguments": {}}}' | uvx --from . python -m aihehuo_mcp.server

# Get current user's ideas with custom pagination
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_current_user_ideas", "arguments": {"paginate": {"page": 1, "per": 5}}}}' | uvx --from . python -m aihehuo_mcp.server

# Test with environment variables set
export CURRENT_USER_ID="12345"
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_current_user_profile", "arguments": {}}}' | uvx --from . python -m aihehuo_mcp.server
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "get_current_user_ideas", "arguments": {"paginate": {"page": 1, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server
```

### Get Idea Details Examples
```bash
# Get details for a specific idea (requires API key)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_idea_details", "arguments": {"idea_id": "12345"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get details for another idea
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_idea_details", "arguments": {"idea_id": "67890"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test with different idea IDs
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_idea_details", "arguments": {"idea_id": "abc123"}}}' | uvx --from . python -m aihehuo_mcp.server
```
