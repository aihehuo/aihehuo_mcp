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
   
   # Test 5: Get group info (requires API key, fetches all users at once)
   echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "818"}}}' | uvx --from . python -m aihehuo_mcp.server
   
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
   - `search_members(params)` - Search for 爱合伙 members using semantic vector search (query must be >5 characters, use coherent sentences, optional wechat_reachable_only, investor, excluded_ids to filter users)
   - `search_ideas(params)` - Search for 爱合伙 ideas/projects using semantic vector search (use coherent sentences)
   - `get_group_info(params)` - Get group information and all member data at once (saves as Markdown file to /tmp)
   - `update_bio(params)` - Update user profile bio
   - `update_goal(params)` - Update user profile goal
   - `get_current_user_profile()` - Get current user complete profile information
   - `get_current_user_ideas(params)` - Get current user's ideas/projects
   - `get_idea_details(params)` - Get detailed information about a specific idea/project
   - `fetch_new_users()` - Fetch new users list (3 pages, 50 per page, filtered fields)
   - `get_user_details(params)` - Get detailed information about a specific user
   - `get_wechat_data(params)` - Get user's WeChat related data (wechat remark, groups, nicknames)
   - `upload_file(params)` - Upload file to cloud storage (images, videos, documents) and get URL
   - `submit_wechat_article_draft(params)` - Submit a WeChat article draft (title, digest, body OR body_file for file upload, HTML without hyperlinks)
   - `create_ai_report(params)` - Create AI-generated report for official website display (title, abstract, html_body OR html_file_path for file upload, hyperlinks allowed, mentioned users/ideas)
   - `update_ai_report(params)` - Update existing AI-generated report (report_id, title, abstract, html_body OR html_file_path, mentioned users/ideas)
   - `get_ai_report(params)` - Get AI report information (report_id) - returns id, title, abstract, mentioned_user_ids, mentioned_idea_ids, confirmed_user_ids
   - `notify_mentioned_users(params)` - Notify users mentioned in AI report (report_id, intro_text, force re-notification, optional user_id to notify specific user)
   - `submit_confirmed_users(params)` - Submit confirmed users for AI report (report_id, user_ids array) - prevents future notifications
   - `convert_numbers_to_ids(params)` - Convert user numbers array to user IDs array (numbers array)
   - `get_latest_24h_ideas(params)` - Get latest ideas/projects published in the past 24 hours (LLM-optimized text format, automatic filtering, newest first)

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
- **search_members()** should return search results (or error if API key is invalid). Supports optional parameters: wechat_reachable_only (filter users reachable on WeChat), investor (filter only investors), excluded_ids (exclude specific user IDs)
- **search_ideas()** should return idea/project search results (or error if API key is invalid)
- **get_group_info()** should save group information and all member data as Markdown file to /tmp directory and return file path (or error if API key is invalid). The file contains formatted group info and complete user list. Use read_file to access the content.
- **update_bio()** should update user bio and return success/error response
- **update_goal()** should update user goal and return success/error response
- **get_current_user_profile()** should return complete current user profile (or error if API key/CURRENT_USER_ID is invalid)
- **get_current_user_ideas()** should return current user's ideas (or error if API key/CURRENT_USER_ID is invalid)
- **get_idea_details()** should return detailed idea information (or error if API key/idea_id is invalid)
- **fetch_new_users()** should return concatenated list of new users with filtered fields (or error if API key is invalid)
- **get_user_details()** should return detailed user information (or error if API key/user_id is invalid)
- **get_wechat_data()** should return user's WeChat data including wechat_remark, wechat_groups, and wechat_group_nicknames (or error if API key/user_id is invalid or user not found)
- **upload_file()** should upload file to cloud storage and return file URL (or error if API key is invalid, file not found, or upload failed). Supports images, videos, documents, etc.
- **submit_wechat_article_draft()** should submit article draft and return success response (or error if API key is invalid or fields are missing). Supports both inline HTML (`body`) and file upload (`body_file`)
- **create_ai_report()** should create AI report and return success response with report ID (or error if API key is invalid or fields are missing). Supports both inline HTML (`html_body`) and file upload (`html_file_path`)
- **update_ai_report()** should update existing AI report and return success response (or error if API key/report_id is invalid or fields are missing). Supports both inline HTML (`html_body`) and file upload (`html_file_path`)
- **get_ai_report()** should return AI report information including id, title, abstract, mentioned_user_ids, mentioned_idea_ids, and confirmed_user_ids (or error if API key/report_id is invalid or report not found)
- **notify_mentioned_users()** should notify users mentioned in AI report and return success response (or error if API key/report_id is invalid or fields are missing)
- **submit_confirmed_users()** should submit confirmed users and return success response (or error if API key/report_id is invalid or fields are missing)
- **convert_numbers_to_ids()** should convert user numbers array to user IDs array and return results with found status (or error if API key is invalid or numbers array is empty)
- **get_latest_24h_ideas()** should return latest ideas published in past 24 hours in LLM-optimized text format (or error if API key is invalid)
- **prompts/list** should return available prompts
- **prompts/get** should return prompt content from markdown files
- **resources/list** should return available resources
- **resources/read** should return brief current user profile (id, name, industry, city, bio) with tool reference
- All eighteen tools, prompts, and resources should be listed in their respective list responses

## Content Publishing Tools Comparison

### `submit_wechat_article_draft` vs `create_ai_report`

| Feature | WeChat Article Draft | AI Report |
|---------|---------------------|-----------|
| **Purpose** | Submit draft for WeChat publication | Create report for official website display |
| **Hyperlinks** | ❌ NOT allowed (`<a>` tags forbidden) | ✅ Allowed (can include `<a>` tags) |
| **User Mentions** | ❌ Not supported | ✅ Supported via `mentioned_user_ids` (ID strings) |
| **Idea Mentions** | ❌ Not supported | ✅ Supported via `mentioned_idea_ids` |
| **Field Names** | `title`, `digest`, `body` OR `body_file` | `title`, `abstract`, `html_body` OR `html_file_path` |
| **File Upload** | ✅ Supported via `body_file` (uploads complete HTML file) | ✅ Supported via `html_file_path` (uploads complete HTML file) |
| **API Endpoint** | `POST /articles/draft_wechat_article` | `POST /ai_reports` |
| **Content Type** | JSON (`body`) or Multipart (`body_file`) | JSON (`html_body`) or Multipart (`html_file_path`) |
| **Use Case** | WeChat social media content | In-depth analysis and reports on website |

**When to use `submit_wechat_article_draft`:**
- Publishing content to WeChat
- Content without external links
- Simple article format

**When to use `create_ai_report`:**
- Creating analytical reports for the website
- Content that references users or projects
- Reports with hyperlinks to external resources
- AI-generated insights and recommendations

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
- For `search_members`, use optional filters:
  - `wechat_reachable_only: true` - Only users who can be directly reached on WeChat
  - `investor: true` - Only search for investors
  - `excluded_ids: ["id1", "id2"]` - Exclude specific users from results

## Test Examples

### Search Members Examples
```bash
# Good semantic search (coherent sentence describing what you're looking for)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找有AI技术背景的创业者，希望合作开发智能产品"}}}' | uvx --from . python -m aihehuo_mcp.server

# Good semantic search with pagination
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "需要寻找有丰富经验的技术合伙人，擅长移动应用开发", "paginate": {"page": 1, "per": 5}}}}' | uvx --from . python -m aihehuo_mcp.server

# Another good semantic search example
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找对电商行业有深度理解的投资人，能够提供战略指导"}}}' | uvx --from . python -m aihehuo_mcp.server

# Search with wechat_reachable_only=true (only return users reachable on WeChat)
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找有AI技术背景的创业者，希望合作开发智能产品", "wechat_reachable_only": true}}}' | uvx --from . python -m aihehuo_mcp.server

# Search with wechat_reachable_only and pagination
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "需要寻找有丰富经验的技术合伙人，擅长移动应用开发", "wechat_reachable_only": true, "paginate": {"page": 1, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server

# Search without wechat_reachable_only (default: false, returns all users)
echo '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找对教育科技有热情的创业者", "wechat_reachable_only": false}}}' | uvx --from . python -m aihehuo_mcp.server

# Search for investors only
echo '{"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找对AI领域感兴趣的投资人", "investor": true}}}' | uvx --from . python -m aihehuo_mcp.server

# Search for investors with wechat_reachable_only
echo '{"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找早期投资人，关注教育科技领域", "investor": true, "wechat_reachable_only": true}}}' | uvx --from . python -m aihehuo_mcp.server

# Search with excluded_ids (exclude specific users)
echo '{"jsonrpc": "2.0", "id": 9, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "寻找有技术背景的创业者", "excluded_ids": ["12345", "67890"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Search with multiple filters combined
echo '{"jsonrpc": "2.0", "id": 10, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "章宇辰爱合伙创始人", "investor": true, "wechat_reachable_only": true, "excluded_ids": ["1"], "paginate": {"page": 1, "per": 15}}}}' | uvx --from . python -m aihehuo_mcp.server

# Bad example (too short) - will return error
echo '{"jsonrpc": "2.0", "id": 11, "method": "tools/call", "params": {"name": "search_members", "arguments": {"query": "AI"}}}' | uvx --from . python -m aihehuo_mcp.server
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
# Get group information and all members by ID
# This will save all data as a Markdown file to /tmp/group_818.md
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "818"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get another group's complete information
# File will be saved to /tmp/group_12345.md
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "12345"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get yet another group
# File will be saved to /tmp/group_67890.md
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "67890"}}}' | uvx --from . python -m aihehuo_mcp.server

# Important Notes:
# - The tool fetches ALL users at once (no pagination needed)
# - Returns a JSON response with file_path, group_id, group_title, and total_users
# - The actual group data is saved as a Markdown file in /tmp directory
# - File naming pattern: /tmp/group_{group_id}.md
# - File includes: group intro, description, and complete user list
# - Use read_file tool to read the Markdown file and access the formatted group data
# - This approach prevents overwhelming the LLM with massive JSON data in the API response
# - Timeout increased to 30s to handle large groups

# Example: Read the saved file
cat /tmp/group_818.md
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
# Fetch new users (3 pages, 50 per page, filtered fields - max 150 users)
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

### Get WeChat Data Examples
```bash
# Get WeChat data for a specific user by ID
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_wechat_data", "arguments": {"user_id": "1"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get WeChat data for another user
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_wechat_data", "arguments": {"user_id": "123"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get WeChat data for yet another user
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_wechat_data", "arguments": {"user_id": "456"}}}' | uvx --from . python -m aihehuo_mcp.server

# Important Notes:
# - Returns user's WeChat related data including:
#   * user_id: User ID
#   * wechat_remark: WeChat remark name
#   * wechat_groups: List of WeChat groups the user has joined (with group titles)
#   * wechat_group_nicknames: List of nicknames used in groups
# - Returns 404 error if user not found
# - Requires valid API key for authentication
```

### Upload File Examples
```bash
# Upload an image file
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "upload_file", "arguments": {"file_path": "/tmp/test_image.jpg"}}}' | uvx --from . python -m aihehuo_mcp.server

# Upload a PDF document
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "upload_file", "arguments": {"file_path": "/tmp/document.pdf"}}}' | uvx --from . python -m aihehuo_mcp.server

# Upload a video file
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "upload_file", "arguments": {"file_path": "/tmp/video.mp4"}}}' | uvx --from . python -m aihehuo_mcp.server

# Upload any other file type
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "upload_file", "arguments": {"file_path": "/tmp/data.xlsx"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: file not found
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "upload_file", "arguments": {"file_path": "/tmp/nonexistent.jpg"}}}' | uvx --from . python -m aihehuo_mcp.server

# Important Notes:
# - Uploads file to cloud storage (OSS) via POST /micro/upload endpoint
# - Supports multiple file types: images (jpg, png, gif), videos (mp4, avi), documents (pdf, docx, xlsx), etc.
# - Returns file URL in format: https://oss-qd.aihehuo.com/{timestamp}_{filename}.{ext}
# - For images, may include ?r={random} query parameter
# - Requires valid API key (Bearer token) for authentication
# - File must exist at the specified path (absolute path required)
# - MIME type is automatically detected from file extension
# - Upload timeout is 60 seconds to handle large files
# - Maximum file size depends on server configuration

# Example: Create a test image file first
echo "Creating test image file..."
curl -o /tmp/test_image.jpg https://via.placeholder.com/150

# Then upload it
echo '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "upload_file", "arguments": {"file_path": "/tmp/test_image.jpg"}}}' | uvx --from . python -m aihehuo_mcp.server
```

### Submit WeChat Article Draft Examples
```bash
# Submit a simple article draft (inline body)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "submit_wechat_article_draft", "arguments": {"title": "AI创业的新机遇", "digest": "探索人工智能在创业领域的最新应用", "body": "<h1>AI创业的新机遇</h1><p>人工智能正在改变创业生态...</p>"}}}' | uvx --from . python -m aihehuo_mcp.server

# Submit an article with rich HTML content (without hyperlinks)
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "submit_wechat_article_draft", "arguments": {"title": "2024创业趋势报告", "digest": "深度分析2024年最值得关注的创业方向", "body": "<h1>2024创业趋势报告</h1><h2>市场分析</h2><p>根据最新数据...</p><ul><li>趋势一</li><li>趋势二</li></ul><p><strong>结论：</strong>创业者应该...</p>"}}}' | uvx --from . python -m aihehuo_mcp.server

# ===== Testing with HTML File Upload =====

# First, create a test HTML file for WeChat article (NO hyperlinks!)
cat > /tmp/wechat_article.html << 'EOF'
<div style="max-width: 677px; margin: 0 auto; background: white; overflow: hidden;">
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); color: white; padding: 30px 20px; text-align: center;">
        <h1 style="font-size: 1.6em; margin-bottom: 8px; font-weight: 600; line-height: 1.4;">🎯 AI创业生态分析</h1>
        <div style="font-size: 0.95em; opacity: 0.95; margin-top: 5px;">探索人工智能创业的最新趋势</div>
    </div>
    
    <div style="padding: 25px 18px;">
        <h2 style="font-size: 1.35em; color: #2c3e50; margin-bottom: 18px;">市场概况</h2>
        <p style="line-height: 1.8; margin-bottom: 15px;">人工智能创业市场持续升温，各类创新应用不断涌现。</p>
        
        <h2 style="font-size: 1.35em; color: #2c3e50; margin-bottom: 18px;">主要趋势</h2>
        <ul style="line-height: 1.8;">
            <li>大模型应用落地</li>
            <li>垂直行业AI解决方案</li>
            <li>AI+传统产业深度融合</li>
        </ul>
        
        <div style="background: #f0fdf4; border-radius: 8px; padding: 20px; margin-top: 25px;">
            <p style="margin: 0; line-height: 1.8;"><strong>💡 结论：</strong>AI创业正处于黄金时期，机遇与挑战并存。</p>
        </div>
    </div>
</div>
EOF

# Upload article with HTML file (no hyperlinks allowed!)
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "submit_wechat_article_draft", "arguments": {"title": "AI创业生态分析（文件上传）", "digest": "通过body_file参数上传完整HTML文件", "body_file": "/tmp/wechat_article.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: both body and body_file provided (should fail)
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "submit_wechat_article_draft", "arguments": {"title": "错误测试", "digest": "测试同时提供两个参数", "body": "<h1>Test</h1>", "body_file": "/tmp/wechat_article.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: file not found
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "submit_wechat_article_draft", "arguments": {"title": "文件不存在测试", "digest": "测试文件路径不存在", "body_file": "/tmp/nonexistent.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Important Notes:
# - Body should only contain HTML content (no <body> tags)
# - Title and digest are plain text
# - Body CANNOT contain hyperlinks (<a> tags) - they will be rejected
# - Allowed HTML tags: h1-h6, p, strong, em, ul, ol, li, blockquote, etc.
# - Forbidden HTML tags: <a> (hyperlinks)
# - NEW: Can upload complete HTML file via "body_file" parameter
# - Choose ONE: either "body" (for inline HTML) OR "body_file" (for file upload)
```

### Create AI Report Examples
```bash
# Create a simple AI report without mentions
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "create_ai_report", "arguments": {"title": "2024年AI创业生态分析报告", "abstract": "本报告深度分析了2024年人工智能创业领域的发展趋势、投资热点和创新方向", "html_body": "<h1>2024年AI创业生态分析报告</h1><h2>市场概况</h2><p>人工智能创业市场持续升温...</p><h2>主要趋势</h2><ul><li>大模型应用落地</li><li>垂直行业AI解决方案</li></ul>"}}}' | uvx --from . python -m aihehuo_mcp.server

# Create an AI report with user mentions
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "create_ai_report", "arguments": {"title": "爱合伙平台优秀创业者推荐", "abstract": "本报告推荐爱合伙平台上的优秀创业者，分析其创业方向和成功经验", "html_body": "<h1>优秀创业者推荐</h1><p>本期推荐以下创业者：</p><ul><li><a href=\"/users/12345\">张三</a> - AI教育领域</li><li><a href=\"/users/67890\">李四</a> - 智能硬件</li></ul>", "mentioned_user_ids": ["12345", "67890"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Create an AI report with idea mentions and hyperlinks
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "create_ai_report", "arguments": {"title": "本周热门创业项目精选", "abstract": "精选本周最具潜力的创业项目，涵盖AI、电商、教育等多个领域", "html_body": "<h1>本周热门项目</h1><h2>AI医疗项目</h2><p>推荐项目：<a href=\"/ideas/abc123\">AI辅助诊断系统</a></p><h2>教育科技</h2><p>推荐项目：<a href=\"/ideas/def456\">智能学习平台</a></p><p>更多信息请访问<a href=\"https://aihehuo.com\">爱合伙官网</a></p>", "mentioned_idea_ids": ["abc123", "def456"]}}}' | uvx --from . python -m aihehuo_mcp.server

# ===== Testing with HTML File Upload =====

# First, create a test HTML file
cat > /tmp/test_report.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Report</title>
</head>
<body>
    <h1>测试报告：AI创业生态分析</h1>
    <h2>概述</h2>
    <p>这是一个通过文件上传创建的测试报告。</p>
    <h2>重点内容</h2>
    <ul>
        <li>人工智能技术发展趋势</li>
        <li>创业者案例分析</li>
        <li>投资机会展望</li>
    </ul>
    <h2>相关链接</h2>
    <p>了解更多请访问 <a href="https://aihehuo.com">爱合伙官网</a></p>
</body>
</html>
EOF

# Upload AI report with HTML file (without mentions)
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "create_ai_report", "arguments": {"title": "AI创业生态分析（文件上传测试）", "abstract": "通过html_file_path参数上传完整HTML文件的测试报告", "html_file_path": "/tmp/test_report.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Upload AI report with HTML file and user mentions
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "create_ai_report", "arguments": {"title": "创业者推荐报告（文件上传）", "abstract": "包含创业者提及的完整HTML报告", "html_file_path": "/tmp/test_report.html", "mentioned_user_ids": ["12345", "67890"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Upload AI report with HTML file and both user/idea mentions
echo '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "create_ai_report", "arguments": {"title": "综合分析报告（文件上传）", "abstract": "包含用户和项目提及的完整HTML报告", "html_file_path": "/tmp/test_report.html", "mentioned_user_ids": ["12345", "67890"], "mentioned_idea_ids": ["abc123", "def456"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: both html_body and html_file_path provided (should fail)
echo '{"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "create_ai_report", "arguments": {"title": "错误测试", "abstract": "测试同时提供两个HTML参数", "html_body": "<h1>Test</h1>", "html_file_path": "/tmp/test_report.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: file not found
echo '{"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "create_ai_report", "arguments": {"title": "文件不存在测试", "abstract": "测试文件路径不存在的情况", "html_file_path": "/tmp/nonexistent_file.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Key Differences from WeChat Article:
# ✅ Hyperlinks ARE ALLOWED in AI reports (<a> tags)
# ✅ Can mention users via mentioned_user_ids (use ID strings, not numbers)
# ✅ Can mention projects via mentioned_idea_ids
# ✅ Reports are displayed on the official website
# ✅ Field name is "abstract" (not "digest")
# ✅ Field name is "html_body" (not "body")
# ✅ NEW: Can upload complete HTML file via "html_file_path" parameter
# ✅ Choose ONE: either "html_body" (for inline HTML) OR "html_file_path" (for file upload)
```

### Update AI Report Examples
```bash
# Update an existing AI report (inline HTML)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "update_ai_report", "arguments": {"report_id": "36", "title": "2024年AI创业生态分析报告（更新版）", "abstract": "本报告深度分析了2024年人工智能创业领域的最新发展趋势、投资热点和创新方向", "html_body": "<h1>2024年AI创业生态分析报告（更新版）</h1><h2>市场概况</h2><p>人工智能创业市场持续升温，出现新的增长点...</p><h2>主要趋势</h2><ul><li>大模型应用落地</li><li>垂直行业AI解决方案</li><li>AI与传统产业深度融合</li></ul>"}}}' | uvx --from . python -m aihehuo_mcp.server

# Update AI report with user mentions
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "update_ai_report", "arguments": {"report_id": "456", "title": "爱合伙平台优秀创业者推荐（2024Q2）", "abstract": "本报告推荐爱合伙平台上的优秀创业者，分析其创业方向和成功经验", "html_body": "<h1>优秀创业者推荐</h1><p>本期推荐以下创业者：</p><ul><li><a href=\"/users/12345\">张三</a> - AI教育领域</li><li><a href=\"/users/67890\">李四</a> - 智能硬件</li><li><a href=\"/users/11111\">王五</a> - 企业服务</li></ul>", "mentioned_user_ids": ["12345", "67890", "11111"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Update AI report with idea mentions and hyperlinks
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "update_ai_report", "arguments": {"report_id": "789", "title": "本周热门创业项目精选（更新）", "abstract": "精选本周最具潜力的创业项目，涵盖AI、电商、教育等多个领域", "html_body": "<h1>本周热门项目</h1><h2>AI医疗项目</h2><p>推荐项目：<a href=\"/ideas/abc123\">AI辅助诊断系统</a></p><h2>教育科技</h2><p>推荐项目：<a href=\"/ideas/def456\">智能学习平台</a></p><h2>新增项目</h2><p>推荐项目：<a href=\"/ideas/xyz999\">在线教育平台</a></p><p>更多信息请访问<a href=\"https://aihehuo.com\">爱合伙官网</a></p>", "mentioned_idea_ids": ["abc123", "def456", "xyz999"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Notify mentioned users about the AI report
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "36", "intro_text": "您好！您被提及在我们的最新AI创业生态分析报告中，请查看详细内容。"}}}' | uvx --from . python -m aihehuo_mcp.server

# Force re-notify mentioned users
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "456", "intro_text": "重要更新：我们的优秀创业者推荐报告已更新，您被重新推荐！", "force": true}}}' | uvx --from . python -m aihehuo_mcp.server

# ===== Testing with HTML File Upload =====

# Create an updated HTML file
cat > /tmp/updated_report.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Updated Report</title>
</head>
<body>
    <h1>更新的报告：AI创业生态分析</h1>
    <h2>概述</h2>
    <p>这是一个通过文件上传更新的测试报告，包含最新的市场分析。</p>
    <h2>重点内容</h2>
    <ul>
        <li>人工智能技术发展趋势（2024最新）</li>
        <li>创业者案例分析（新增案例）</li>
        <li>投资机会展望（市场预测）</li>
        <li>政策环境分析（新增）</li>
    </ul>
    <h2>相关链接</h2>
    <p>了解更多请访问 <a href="https://aihehuo.com">爱合伙官网</a></p>
</body>
</html>
EOF

# Update AI report with HTML file (without mentions)
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "update_ai_report", "arguments": {"report_id": "999", "title": "AI创业生态分析（文件更新测试）", "abstract": "通过html_file_path参数上传更新的完整HTML文件", "html_file_path": "/tmp/updated_report.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Update AI report with HTML file and user mentions
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "update_ai_report", "arguments": {"report_id": "888", "title": "创业者推荐报告（文件更新）", "abstract": "包含创业者提及的更新HTML报告", "html_file_path": "/tmp/updated_report.html", "mentioned_user_ids": ["12345", "67890", "11111"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Update AI report with HTML file and both user/idea mentions
echo '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "update_ai_report", "arguments": {"report_id": "777", "title": "综合分析报告（文件更新）", "abstract": "包含用户和项目提及的更新HTML报告", "html_file_path": "/tmp/updated_report.html", "mentioned_user_ids": ["12345", "67890"], "mentioned_idea_ids": ["abc123", "def456", "xyz999"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: both html_body and html_file_path provided (should fail)
echo '{"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "update_ai_report", "arguments": {"report_id": "666", "title": "错误测试", "abstract": "测试同时提供两个HTML参数", "html_body": "<h1>Test</h1>", "html_file_path": "/tmp/updated_report.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: file not found
echo '{"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "update_ai_report", "arguments": {"report_id": "555", "title": "文件不存在测试", "abstract": "测试文件路径不存在的情况", "html_file_path": "/tmp/nonexistent_update.html"}}}' | uvx --from . python -m aihehuo_mcp.server

# Key Points for Update:
# ✅ Must provide report_id (required parameter)
# ✅ All other parameters same as create_ai_report
# ✅ Uses PUT method to update existing report
```

### Get AI Report Examples
```bash
# Get AI report information by ID
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_ai_report", "arguments": {"report_id": "60"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get another report
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_ai_report", "arguments": {"report_id": "456"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: report not found
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_ai_report", "arguments": {"report_id": "999999"}}}' | uvx --from . python -m aihehuo_mcp.server

# Expected Response Format:
# {
#   "data": {
#     "id": 36,
#     "title": "报告标题",
#     "abstract": "报告摘要",
#     "mentioned_user_ids": [1, 2, 3],
#     "mentioned_idea_ids": [10, 20],
#     "confirmed_user_ids": [1, 5, 8]
#   }
# }

# Key Points:
# ✅ Only requires report_id parameter
# ✅ Returns basic report information: id, title, abstract, mentioned_user_ids, mentioned_idea_ids, confirmed_user_ids
# ✅ Does not return full HTML body to reduce response size
# ✅ confirmed_user_ids contains IDs of users who have confirmed/acknowledged the report
# ✅ Returns 404 error if report not found
```

### Notify Mentioned Users Examples
```bash
# IMPORTANT: Set your API key first (required for authentication)
export AIHEHUO_API_KEY="your_actual_api_key_here"

# Notify users mentioned in an AI report (basic notification)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "46", "intro_text": "您好！您被提及在我们的最新AI创业生态分析报告中，请查看详细内容。"}}}' | uvx --from . python -m aihehuo_mcp.server

# Force re-notify mentioned users (even if already notified)
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "46", "intro_text": "重要更新：我们的优秀创业者推荐报告已更新，您被重新推荐！", "force": true}}}' | uvx --from . python -m aihehuo_mcp.server

# Notify with detailed introduction text
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "46", "intro_text": "尊敬的用户，我们很高兴地通知您，您在我们的《本周热门创业项目精选》报告中被特别推荐。您的项目展现了卓越的创新性和市场潜力，我们相信这将为您带来更多合作机会。请点击查看完整报告内容。"}}}' | uvx --from . python -m aihehuo_mcp.server

# Notify only a specific user (use user_id parameter)
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "46", "intro_text": "您好！您被特别提及在我们的报告中。", "user_id": 12345}}}' | uvx --from . python -m aihehuo_mcp.server

# Notify specific user with force re-notification
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "46", "intro_text": "重要更新：报告已更新，请查看。", "user_id": 67890, "force": true}}}' | uvx --from . python -m aihehuo_mcp.server

# Notify different specific user
echo '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "123", "intro_text": "您在我们的新报告中被提及，感谢您的贡献！", "user_id": 98765}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: missing required parameters
echo '{"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "123"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: invalid report_id
echo '{"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "notify_mentioned_users", "arguments": {"report_id": "invalid_id", "intro_text": "测试无效报告ID"}}}' | uvx --from . python -m aihehuo_mcp.server

# Key Points for Notify:
# ✅ Must provide report_id (required parameter)
# ✅ Must provide intro_text (required parameter)
# ✅ force parameter is optional (default: false)
# ✅ user_id parameter is optional (integer) - specify to notify only one user
# ✅ Uses POST method to /micro/ai_reports/{report_id}/notify_mentioned_users
# ✅ Without user_id: sends notification to all users mentioned in the report
# ✅ With user_id: sends notification to only the specified user
# ✅ force=true allows re-notification even if already notified
```

### Submit Confirmed Users Examples
```bash
# IMPORTANT: Set your API key first (required for authentication)
export AIHEHUO_API_KEY="your_actual_api_key_here"

# Submit confirmed users for an AI report (users who have read the report)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "submit_confirmed_users", "arguments": {"report_id": "46", "user_ids": ["12345", "67890"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Submit single confirmed user
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "submit_confirmed_users", "arguments": {"report_id": "46", "user_ids": ["12345"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Submit multiple confirmed users (larger batch)
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "submit_confirmed_users", "arguments": {"report_id": "46", "user_ids": ["12345", "67890", "11111", "22222", "33333"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Submit confirmed users for a different report
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "submit_confirmed_users", "arguments": {"report_id": "123", "user_ids": ["98765", "54321"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: missing required parameters
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "submit_confirmed_users", "arguments": {"report_id": "46"}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: empty user_ids array
echo '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "submit_confirmed_users", "arguments": {"report_id": "46", "user_ids": []}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: invalid report_id
echo '{"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "submit_confirmed_users", "arguments": {"report_id": "invalid_id", "user_ids": ["12345"]}}}' | uvx --from . python -m aihehuo_mcp.server

# Key Points for Submit Confirmed Users:
# ✅ Must provide report_id (required parameter)
# ✅ Must provide user_ids array (required parameter)
# ✅ User IDs should be strings (not numbers)
# ✅ Uses POST method to /micro/ai_reports/{report_id}/submit_confirmed_users
# ✅ Confirmed users will NEVER be notified again for this report
# ✅ Even force=true in notify_mentioned_users won't notify confirmed users
# ✅ Use this to mark users who have already read and acknowledged the report
# ✅ Helps prevent notification spam and respects user engagement
```

### Convert Numbers to IDs Examples
```bash
# IMPORTANT: Set your API key first (required for authentication)
export AIHEHUO_API_KEY="your_actual_api_key_here"

# Convert user numbers to IDs (basic example)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "convert_numbers_to_ids", "arguments": {"numbers": [9200001, 9200002, 123456]}}}' | uvx --from . python -m aihehuo_mcp.server

# Convert single user number
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "convert_numbers_to_ids", "arguments": {"numbers": [9200001]}}}' | uvx --from . python -m aihehuo_mcp.server

# Convert multiple user numbers (some may not exist)
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "convert_numbers_to_ids", "arguments": {"numbers": [9200001, 9200002, 9200003, 9999999, 123456]}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: empty numbers array
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "convert_numbers_to_ids", "arguments": {"numbers": []}}}' | uvx --from . python -m aihehuo_mcp.server

# Test error case: invalid numbers (non-integer)
echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "convert_numbers_to_ids", "arguments": {"numbers": ["invalid", 9200001]}}}' | uvx --from . python -m aihehuo_mcp.server

# Key Points for Convert:
# ✅ Must provide numbers array (required parameter)
# ✅ Each number should be an integer (user number)
# ✅ Uses POST method to /users/convert_numbers_to_ids
# ✅ Returns results array with number, user_id, and found status
# ✅ found=true means user exists, found=false means user not found
# ✅ user_id will be null if user not found
```

### Get Latest 24h Ideas Examples
```bash
# IMPORTANT: Set your API key first (required for authentication)
export AIHEHUO_API_KEY="your_actual_api_key_here"

# Get latest ideas published in the past 24 hours (default pagination)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_latest_24h_ideas", "arguments": {}}}' | uvx --from . python -m aihehuo_mcp.server

# Get latest ideas with custom pagination (page 1, 20 per page)
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_latest_24h_ideas", "arguments": {"paginate": {"page": 1, "per": 20}}}}' | uvx --from . python -m aihehuo_mcp.server

# Get second page of latest ideas
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_latest_24h_ideas", "arguments": {"paginate": {"page": 2, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server

# Get large batch (50 per page) - useful for comprehensive analysis
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_latest_24h_ideas", "arguments": {"paginate": {"page": 1, "per": 50}}}}' | uvx --from . python -m aihehuo_mcp.server

# Key Features:
# ✅ Returns LLM-optimized pure text format (not JSON)
# ✅ Automatically uses "User-Agent: LLM_AGENT" header
# ✅ Only returns accepted/published projects (filtered)
# ✅ Sorted by creation time (newest first)
# ✅ Includes full project details, links, and metadata
# ✅ Perfect for AI analysis and recommendations
# ✅ Response includes both data and meta information
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
