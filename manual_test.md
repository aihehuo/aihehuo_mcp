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
   - `search_members(params)` - Search for 爱合伙 members using semantic vector search (query must be >5 characters, use coherent sentences)
   - `search_ideas(params)` - Search for 爱合伙 ideas/projects using semantic vector search (use coherent sentences)
   - `get_group_info(params)` - Get group information and member data
   - `update_bio(params)` - Update user profile bio
   - `update_goal(params)` - Update user profile goal
   - `get_current_user_profile()` - Get current user complete profile information
   - `get_current_user_ideas(params)` - Get current user's ideas/projects
   - `get_idea_details(params)` - Get detailed information about a specific idea/project
   - `fetch_new_users()` - Fetch new users list (10 pages, 200 per page, filtered fields)
   - `get_user_details(params)` - Get detailed information about a specific user
   - `submit_wechat_article_draft(params)` - Submit a WeChat article draft (title, digest, body as HTML)

3. The server will also provide these prompts:
   - `pitch` - Create a compelling 60-second elevator pitch based on your validated business model
   - `business_plan` - Create a comprehensive business plan for your startup

4. The server will also provide these resources:
   - `aihehuo://current_user/profile` - Get brief current user profile (id, name, industry, city, bio) with tool reference

## Method 3: Test with Environment Variables

Set up your API key and test:

```bash
export AIHEHUO_API_KEY="your_actual_api_key_here"
uvx --from . python -m aihehuo_mcp.server
```

Then use Method 1 to send test requests.

## API Request Headers

All API requests to the 爱合伙 backend include the following headers:
- `Authorization: Bearer {AIHEHUO_API_KEY}` - API authentication
- `Content-Type: application/json` - JSON request format
- `Accept: application/json` - JSON response format
- `User-Agent: LLM_AGENT` - Identifies requests from the LLM Agent (using standard HTTP User-Agent header)

## Expected Results

- **server_info()** should return server metadata
- **search_members()** should return search results (or error if API key is invalid)
- **search_ideas()** should return idea/project search results (or error if API key is invalid)
- **get_group_info()** should return group information and member data (or error if API key is invalid)
- **update_bio()** should update user bio and return success/error response
- **update_goal()** should update user goal and return success/error response
- **get_current_user_profile()** should return complete current user profile (or error if API key/CURRENT_USER_ID is invalid)
- **get_current_user_ideas()** should return current user's ideas (or error if API key/CURRENT_USER_ID is invalid)
- **get_idea_details()** should return detailed idea information (or error if API key/idea_id is invalid)
- **fetch_new_users()** should return concatenated list of new users with filtered fields (or error if API key is invalid)
- **get_user_details()** should return detailed user information (or error if API key/user_id is invalid)
- **submit_wechat_article_draft()** should submit article draft and return success response (or error if API key is invalid or fields are missing)
- **prompts/list** should return available prompts
- **prompts/get** should return prompt content from markdown files
- **resources/list** should return available resources
- **resources/read** should return brief current user profile (id, name, industry, city, bio) with tool reference
- All twelve tools, prompts, and resources should be listed in their respective list responses

## Semantic Search Best Practices

Since both `search_members` and `search_ideas` use vector semantic search, it's important to use coherent, descriptive sentences rather than simple keyword lists:

### ✅ Good Examples:
- **Members**: "寻找有AI技术背景的创业者，希望合作开发智能产品"
- **Ideas**: "寻找基于人工智能技术的创新创业项目，特别是医疗健康和教育领域的应用"

### ❌ Avoid These:
- **Members**: "AI 创业者 技术" (just keywords)
- **Ideas**: "AI 创业 投资" (just keywords)

### Tips:
- Use complete sentences that describe what you're looking for
- Include context and specific requirements
- Mention the purpose or goal of your search
- Be descriptive about the type of person or project you need

## Test Examples

### Search Members Examples
```bash
# Good semantic search (coherent sentence describing what you're looking for)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找有AI技术背景的创业者，希望合作开发智能产品"}}}' | uvx --from . python -m aihehuo_mcp.server

# Good semantic search with pagination
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "需要寻找有丰富经验的技术合伙人，擅长移动应用开发", "paginate": {"page": 1, "per": 5}}}}' | uvx --from . python -m aihehuo_mcp.server

# Another good semantic search example
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找对电商行业有深度理解的投资人，能够提供战略指导"}}}' | uvx --from . python -m aihehuo_mcp.server

# Bad example (too short) - will return error
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "AI"}}}' | uvx --from . python -m aihehuo_mcp.server
```

### Search Ideas Examples
```bash
# Good semantic search for AI-related startup ideas
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_ideas", "arguments": {"query": "寻找基于人工智能技术的创新创业项目，特别是医疗健康和教育领域的应用", "paginate": {"page": 1, "per": 5}}}}' | uvx --from . python -m aihehuo_mcp.server

# Good semantic search for investment opportunities
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_ideas", "arguments": {"query": "寻找有潜力的早期创业项目，重点关注可持续发展和环保技术", "paginate": {"page": 1, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server

# Good semantic search for business projects
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_ideas", "arguments": {"query": "寻找电商平台相关的创业想法，特别是社交电商和新零售模式", "paginate": {"page": 1, "per": 8}}}}' | uvx --from . python -m aihehuo_mcp.server

# Another good semantic search example
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "search_ideas", "arguments": {"query": "寻找解决城市交通拥堵问题的创新解决方案，包括共享出行和智能交通"}}}' | uvx --from . python -m aihehuo_mcp.server
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
# Get complete current user profile (requires CURRENT_USER_ID env var)
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

### Resource Examples
```bash
# List available resources
echo '{"jsonrpc": "2.0", "id": 1, "method": "resources/list", "params": {}}' | uvx --from . python -m aihehuo_mcp.server

# Get brief current user profile (id, name, industry, city, bio) with tool reference
echo '{"jsonrpc": "2.0", "id": 2, "method": "resources/read", "params": {"uri": "aihehuo://current_user/profile"}}' | uvx --from . python -m aihehuo_mcp.server

# Test with environment variables set
export CURRENT_USER_ID="12345"
echo '{"jsonrpc": "2.0", "id": 3, "method": "resources/read", "params": {"uri": "aihehuo://current_user/profile"}}' | uvx --from . python -m aihehuo_mcp.server
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

### Fetch New Users Examples
```bash
# Fetch new users (10 pages, 200 per page, filtered fields)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "fetch_new_users", "arguments": {}}}' | uvx --from . python -m aihehuo_mcp.server
```

### Get User Details Examples
```bash
# Get details for a specific user by ID
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_user_details", "arguments": {"user_id": "1"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get details for another user
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_user_details", "arguments": {"user_id": "67890"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test with different user IDs
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_user_details", "arguments": {"user_id": "abc123"}}}' | uvx --from . python -m aihehuo_mcp.server
```

### Submit WeChat Article Draft Examples
```bash
# Submit a simple article draft
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "submit_wechat_article_draft", "arguments": {"title": "AI创业的新机遇", "digest": "探索人工智能在创业领域的最新应用", "body": "<h1>AI创业的新机遇</h1><p>人工智能正在改变创业生态...</p>"}}}' | uvx --from . python -m aihehuo_mcp.server

# Submit an article with rich HTML content
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "submit_wechat_article_draft", "arguments": {"title": "2024创业趋势报告", "digest": "深度分析2024年最值得关注的创业方向", "body": "<h1>2024创业趋势报告</h1><h2>市场分析</h2><p>根据最新数据...</p><ul><li>趋势一</li><li>趋势二</li></ul><p><strong>结论：</strong>创业者应该...</p>"}}}' | uvx --from . python -m aihehuo_mcp.server

# Note: Body should only contain HTML content (no <body> tags), title and digest are plain text
```

### Prompt Examples
```bash
# List available prompts
echo '{"jsonrpc": "2.0", "id": 1, "method": "prompts/list", "params": {}}' | uvx --from . python -m aihehuo_mcp.server

# Get the pitch prompt
echo '{"jsonrpc": "2.0", "id": 2, "method": "prompts/get", "params": {"name": "pitch"}}' | uvx --from . python -m aihehuo_mcp.server

# Get pitch prompt with arguments
echo '{"jsonrpc": "2.0", "id": 3, "method": "prompts/get", "params": {"name": "pitch", "arguments": {"target_audience": "investors", "context": "demo_day"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get business plan prompt
echo '{"jsonrpc": "2.0", "id": 4, "method": "prompts/get", "params": {"name": "business_plan"}}' | uvx --from . python -m aihehuo_mcp.server
```
