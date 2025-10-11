# 爱合伙 MCP 服务器

Model Context Protocol (MCP) 服务器，用于访问爱合伙平台的创业者、项目和数据。

## 📦 安装配置（中国大陆）

### 方法 1: 配置 UV 使用国内镜像（推荐）

UV/UVX 有专门的配置文件。已为你创建 `~/.config/uv/uv.toml`:

```toml
[pip]
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
```

或者在命令行中使用环境变量：

```bash
# 设置 UV 使用清华镜像源
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 然后运行 uvx
uvx --from /Users/yc/workspace/aihehuo/aihehuo_mcp python -m aihehuo_mcp.server
```

### 方法 2: 全局配置 pip 镜像源

创建或编辑 `~/.pip/pip.conf` (Linux/macOS) 或 `%APPDATA%\pip\pip.ini` (Windows):

```bash
# macOS/Linux
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple

[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
```

### 方法 3: 临时使用镜像源

每次安装时指定镜像源：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple mcp requests pydantic
```

### 常用国内镜像源

| 镜像源 | URL | 说明 |
|--------|-----|------|
| 清华大学 | https://pypi.tuna.tsinghua.edu.cn/simple | 推荐，速度快，同步及时 |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple/ | 阿里云官方镜像 |
| 腾讯云 | https://mirrors.cloud.tencent.com/pypi/simple/ | 腾讯云官方镜像 |
| 华为云 | https://mirrors.huaweicloud.com/repository/pypi/simple/ | 华为云官方镜像 |
| 中科大 | https://pypi.mirrors.ustc.edu.cn/simple/ | 中国科技大学镜像 |
| 豆瓣 | https://pypi.douban.com/simple/ | 豆瓣镜像（较旧） |

## 🚀 快速开始

### 1. 配置环境变量

```bash
export AIHEHUO_API_KEY="your_api_key_here"
export AIHEHUO_API_BASE="https://new-api.aihehuo.com"
export CURRENT_USER_ID="your_user_id"
```

### 2. 在 Cursor 中配置 MCP

编辑 `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "aihehuo-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "/Users/yc/workspace/aihehuo/aihehuo_mcp",
        "python",
        "-m",
        "aihehuo_mcp.server"
      ],
      "cwd": "/Users/yc/workspace/aihehuo/aihehuo_mcp",
      "env": {
        "AIHEHUO_API_KEY": "your_api_key_here",
        "AIHEHUO_API_BASE": "https://new-api.aihehuo.com",
        "CURRENT_USER_ID": "your_user_id",
        "PIP_INDEX_URL": "https://pypi.tuna.tsinghua.edu.cn/simple",
        "PIP_TRUSTED_HOST": "pypi.tuna.tsinghua.edu.cn"
      }
    }
  }
}
```

### 3. 测试服务器

```bash
# 使用清华镜像源
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 测试工具列表
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | uvx --from . python -m aihehuo_mcp.server
```

## 🔧 可用工具

服务器提供 13 个工具：

1. **server_info()** - 健康检查
2. **search_members()** - 搜索创业者（向量语义搜索）
3. **search_ideas()** - 搜索项目（向量语义搜索）
4. **get_group_info()** - 获取群组信息
5. **update_bio()** - 更新个人简介
6. **update_goal()** - 更新创业目标
7. **get_current_user_profile()** - 获取当前用户完整资料
8. **get_current_user_ideas()** - 获取当前用户的项目
9. **get_idea_details()** - 获取项目详情
10. **fetch_new_users()** - 获取新用户列表（3页，每页50个）
11. **get_user_details()** - 获取用户详情
12. **submit_wechat_article_draft()** - 提交微信文章草稿（不允许超链接）
13. **create_ai_report()** - 创建AI报告（允许超链接和用户/项目提及）

## 📝 提示词

- **pitch** - 创建60秒电梯演讲
- **business_plan** - 创建商业计划书

## 🔗 资源

- **aihehuo://current_user/profile** - 当前用户简要资料

## 💡 使用技巧

### 语义搜索最佳实践

使用完整的语义连贯句子，而不是关键词罗列：

✅ 好的示例：
- "寻找有AI技术背景的创业者，希望合作开发智能产品"
- "寻找基于人工智能技术的创新创业项目，特别是医疗健康和教育领域的应用"

❌ 避免：
- "AI 创业者 技术"
- "AI 创业 投资"

## 🆘 故障排除

### 问题：安装依赖太慢

**解决方案**：使用国内镜像源，参考上面的配置方法。

### 问题：uvx 找不到模块

**解决方案**：确保使用 `--from` 参数指定正确的路径：

```bash
uvx --from /Users/yc/workspace/aihehuo/aihehuo_mcp python -m aihehuo_mcp.server
```

### 问题：API 请求失败

**解决方案**：检查环境变量是否正确设置：

```bash
echo $AIHEHUO_API_KEY
echo $AIHEHUO_API_BASE
echo $CURRENT_USER_ID
```

## 📚 更多信息

详细测试指南请参考 `manual_test.md`。

