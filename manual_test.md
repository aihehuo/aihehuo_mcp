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
   
   # Test 5: Get group info (requires API key, supports pagination)
   echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "818", "paginate": {"page": 1, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server
   
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
   - `get_group_info(params)` - Get group information and member data (supports pagination)
   - `update_bio(params)` - Update user profile bio
   - `update_goal(params)` - Update user profile goal
   - `get_current_user_profile()` - Get current user complete profile information
   - `get_current_user_ideas(params)` - Get current user's ideas/projects
   - `get_idea_details(params)` - Get detailed information about a specific idea/project
   - `fetch_new_users()` - Fetch new users list (3 pages, 50 per page, filtered fields)
   - `get_user_details(params)` - Get detailed information about a specific user
   - `submit_wechat_article_draft(params)` - Submit a WeChat article draft (title, digest, body OR body_file for file upload, HTML without hyperlinks)
   - `create_ai_report(params)` - Create AI-generated report for official website display (title, abstract, html_body OR html_file_path for file upload, hyperlinks allowed, mentioned users/ideas)
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
- **search_members()** should return search results (or error if API key is invalid)
- **search_ideas()** should return idea/project search results (or error if API key is invalid)
- **get_group_info()** should return group information and member data with pagination support (or error if API key is invalid)
- **update_bio()** should update user bio and return success/error response
- **update_goal()** should update user goal and return success/error response
- **get_current_user_profile()** should return complete current user profile (or error if API key/CURRENT_USER_ID is invalid)
- **get_current_user_ideas()** should return current user's ideas (or error if API key/CURRENT_USER_ID is invalid)
- **get_idea_details()** should return detailed idea information (or error if API key/idea_id is invalid)
- **fetch_new_users()** should return concatenated list of new users with filtered fields (or error if API key is invalid)
- **get_user_details()** should return detailed user information (or error if API key/user_id is invalid)
- **submit_wechat_article_draft()** should submit article draft and return success response (or error if API key is invalid or fields are missing). Supports both inline HTML (`body`) and file upload (`body_file`)
- **create_ai_report()** should create AI report and return success response with report ID (or error if API key is invalid or fields are missing). Supports both inline HTML (`html_body`) and file upload (`html_file_path`)
- **get_latest_24h_ideas()** should return latest ideas published in past 24 hours in LLM-optimized text format (or error if API key is invalid)
- **prompts/list** should return available prompts
- **prompts/get** should return prompt content from markdown files
- **resources/list** should return available resources
- **resources/read** should return brief current user profile (id, name, industry, city, bio) with tool reference
- All fourteen tools, prompts, and resources should be listed in their respective list responses

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
# Get group information by ID (default pagination)
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "12345"}}}' | uvx --from . python -m aihehuo_mcp.server

# Get group information with custom pagination
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "12345", "paginate": {"page": 1, "per": 20}}}}' | uvx --from . python -m aihehuo_mcp.server

# Get second page of group members
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "67890", "paginate": {"page": 2, "per": 10}}}}' | uvx --from . python -m aihehuo_mcp.server

# Get group info with larger page size
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_group_info", "arguments": {"group_id": "abc123", "paginate": {"page": 1, "per": 50}}}}' | uvx --from . python -m aihehuo_mcp.server
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
