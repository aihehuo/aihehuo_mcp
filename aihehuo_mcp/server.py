# server.py
import asyncio
import json
import os
import sys
import warnings
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

# Import prompts from separate file
from .prompts import PROMPTS

# Suppress the specific warning about module import order
warnings.filterwarnings("ignore", message=".*found in sys.modules after import.*")

# === 配置 ===
AIHEHUO_API_BASE = os.getenv("AIHEHUO_API_BASE", "https://new-api.aihehuo.com")
AIHEHUO_API_KEY  = os.getenv("AIHEHUO_API_KEY",  "REPLACE_ME")
CURRENT_USER_ID  = os.getenv("CURRENT_USER_ID",  "REPLACE_ME")

# === 定义请求/响应模型 ===
class SearchMembersParams(BaseModel):
    query: str = Field(..., description="搜索关键词")
    paginate: Dict[str, int] = Field(default_factory=lambda: {"page": 1, "per": 10}, description="分页参数")

class SearchIdeasParams(BaseModel):
    query: str = Field(..., description="搜索关键词")
    paginate: Dict[str, int] = Field(default_factory=lambda: {"page": 1, "per": 10}, description="分页参数")

class GetGroupInfoParams(BaseModel):
    group_id: str = Field(..., description="群组ID")

class UpdateBioParams(BaseModel):
    bio: str = Field(..., description="用户简介")

class UpdateGoalParams(BaseModel):
    goal: str = Field(..., description="用户目标")

class GetCurrentUserParams(BaseModel):
    pass  # No parameters needed, uses CURRENT_USER_ID from environment

class GetCurrentUserIdeasParams(BaseModel):
    paginate: Dict[str, int] = Field(default_factory=lambda: {"page": 1, "per": 10}, description="分页参数")

class GetIdeaDetailsParams(BaseModel):
    idea_id: str = Field(..., description="想法/项目ID")

class FetchNewUsersParams(BaseModel):
    pass  # No parameters needed, uses fixed pagination

class GetUserDetailsParams(BaseModel):
    user_id: str = Field(..., description="用户ID")

class SubmitWechatArticleDraftParams(BaseModel):
    title: str = Field(..., description="文章标题")
    digest: str = Field(..., description="文章摘要")
    body: str = Field(..., description="文章正文HTML内容（仅包含body标签内的内容，不能包含超链接<a>标签）")

class CreateAIReportParams(BaseModel):
    title: str = Field(..., description="报告标题")
    abstract: str = Field(..., description="报告摘要/简介")
    html_body: str = Field(..., description="报告正文HTML内容")
    mentioned_user_ids: List[str] = Field(default_factory=list, description="报告中提及的用户ID列表（注意是ID字符串，不是number）")
    mentioned_idea_ids: List[str] = Field(default_factory=list, description="报告中提及的项目/想法ID列表")

# === 简单的 MCP 服务器实现 ===
class SimpleMCPServer:
    def __init__(self):
        self.tools = {
            "server_info": {
                "name": "server_info",
                "description": "获取 MCP 服务信息（健康检查）",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "search_members": {
                "name": "search_members", 
                "description": "搜索爱合伙平台上的创业者/会员。使用向量语义搜索，建议使用语义连贯的长句描述，避免简单关键词罗列",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "语义搜索查询（长度必须大于5个字符，建议使用完整句子描述需求）",
                            "minLength": 6
                        },
                        "paginate": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer", "default": 1},
                                "per": {"type": "integer", "default": 10}
                            },
                            "default": {"page": 1, "per": 10}
                        }
                    },
                    "required": ["query"]
                }
            },
            "search_ideas": {
                "name": "search_ideas", 
                "description": "搜索爱合伙平台上的创业想法/项目。使用向量语义搜索，建议使用语义连贯的长句描述，避免简单关键词罗列",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "语义搜索查询（建议使用完整句子描述需求）"
                        },
                        "paginate": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer", "default": 1},
                                "per": {"type": "integer", "default": 10}
                            },
                            "default": {"page": 1, "per": 10}
                        }
                    },
                    "required": ["query"]
                }
            },
            "get_group_info": {
                "name": "get_group_info",
                "description": "获取群组基本情况和群内所有成员数据",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "group_id": {
                            "type": "string",
                            "description": "群组ID"
                        }
                    },
                    "required": ["group_id"]
                }
            },
            "update_bio": {
                "name": "update_bio",
                "description": "更新用户简介",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "bio": {
                            "type": "string",
                            "description": "用户简介"
                        }
                    },
                    "required": ["bio"]
                }
            },
            "update_goal": {
                "name": "update_goal",
                "description": "更新用户目标",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "goal": {
                            "type": "string",
                            "description": "用户目标"
                        }
                    },
                    "required": ["goal"]
                }
            },
            "get_current_user_ideas": {
                "name": "get_current_user_ideas",
                "description": "获取当前用户的创业想法/项目",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "paginate": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer", "default": 1},
                                "per": {"type": "integer", "default": 10}
                            },
                            "default": {"page": 1, "per": 10}
                        }
                    },
                    "required": []
                }
            },
            "get_idea_details": {
                "name": "get_idea_details",
                "description": "获取指定想法/项目的详细信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "idea_id": {
                            "type": "string",
                            "description": "想法/项目ID"
                        }
                    },
                    "required": ["idea_id"]
                }
            },
            "get_current_user_profile": {
                "name": "get_current_user_profile",
                "description": "获取当前用户完整资料信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "fetch_new_users": {
                "name": "fetch_new_users",
                "description": "获取新用户列表，分页获取10页数据并合并",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "get_user_details": {
                "name": "get_user_details",
                "description": "获取指定用户的详细信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "用户ID"
                        }
                    },
                    "required": ["user_id"]
                }
            },
            "submit_wechat_article_draft": {
                "name": "submit_wechat_article_draft",
                "description": "提交微信文章草稿。注意：文章正文不能包含超链接（<a>标签）",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "文章标题"
                        },
                        "digest": {
                            "type": "string",
                            "description": "文章摘要"
                        },
                        "body": {
                            "type": "string",
                            "description": "文章正文HTML内容（仅包含body标签内的内容，不包含<body>标签本身，不能包含超链接<a>标签）"
                        }
                    },
                    "required": ["title", "digest", "body"]
                }
            },
            "create_ai_report": {
                "name": "create_ai_report",
                "description": "创建AI生成的报告并在官网展示。与微信文章不同，报告可以包含超链接，并可以关联提及的用户和项目",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "报告标题"
                        },
                        "abstract": {
                            "type": "string",
                            "description": "报告摘要/简介"
                        },
                        "html_body": {
                            "type": "string",
                            "description": "报告正文HTML内容（可以包含超链接）"
                        },
                        "mentioned_user_ids": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "报告中提及的用户ID列表（ID字符串，不是number）",
                            "default": []
                        },
                        "mentioned_idea_ids": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "报告中提及的项目/想法ID列表",
                            "default": []
                        }
                    },
                    "required": ["title", "abstract", "html_body"]
                }
            }
        }
        
        # Initialize prompts from separate file
        self.prompts = PROMPTS
        
        # Initialize resources
        self.resources = {
            "current_user_profile": {
                "uri": "aihehuo://current_user/profile",
                "name": "Current User Profile (Brief)",
                "description": "Get brief current user profile information with tool reference for complete data",
                "mimeType": "application/json"
            }
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理 MCP 请求"""
        method = request.get("method")
        request_id = request.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "prompts": {"listChanged": True},
                        "resources": {"listChanged": True}
                    },
                    "serverInfo": {
                        "name": "aihehuo-search-mcp",
                        "version": "0.1.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": list(self.tools.values())
                }
            }
        
        elif method == "prompts/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "prompts": list(self.prompts.values())
                }
            }
        
        elif method == "prompts/get":
            prompt_name = request.get("params", {}).get("name")
            if prompt_name in self.prompts:
                # Get the embedded prompt content
                try:
                    prompt_content = self.prompts[prompt_name]["content"]
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "description": self.prompts[prompt_name]["description"],
                            "messages": [
                                {
                                    "role": "user",
                                    "content": {
                                        "type": "text",
                                        "text": prompt_content
                                    }
                                }
                            ]
                        }
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": f"Error getting prompt content: {str(e)}"
                        }
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown prompt: {prompt_name}"
                    }
                }
        
        elif method == "resources/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "resources": list(self.resources.values())
                }
            }
        
        elif method == "resources/read":
            resource_uri = request.get("params", {}).get("uri")
            if resource_uri == "aihehuo://current_user/profile":
                try:
                    # Check if CURRENT_USER_ID is set
                    if CURRENT_USER_ID == "REPLACE_ME":
                        brief_info = {
                            "id": "not_configured",
                            "name": "Unknown",
                            "industry": "Unknown",
                            "city": "Unknown", 
                            "bio": "CURRENT_USER_ID not configured",
                            "status": "Please set CURRENT_USER_ID environment variable",
                            "available_tools": {
                                "get_current_user_profile": "Use this tool to get complete user profile information"
                            }
                        }
                    else:
                        # Fetch brief user information from API
                        headers = {
                            "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "User-Agent": "LLM_AGENT"
                        }

                        # Build URL with current user ID: /users/{CURRENT_USER_ID}
                        url = f"{AIHEHUO_API_BASE}/users/{CURRENT_USER_ID}"
                        
                        resp = requests.get(url, headers=headers, timeout=15)
                        resp.raise_for_status()
                        # Ensure response is decoded as UTF-8
                        resp.encoding = 'utf-8'
                        data = resp.json()["data"]
                        
                        # Extract brief information from the full profile
                        brief_info = {
                            "id": data.get("id", "unknown"),
                            "name": data.get("name", "Unknown"),
                            "industry": data.get("industry", "Unknown"),
                            "city": data.get("city", "Unknown"),
                            "bio": data.get("bio", "No bio available"),
                            "available_tools": {
                                "get_current_user_profile": "Use this tool to get complete user profile information"
                            },
                            "note": "This is a brief resource. Use the 'get_current_user_profile' tool for complete profile data."
                        }
                    
                    # Properly encode the brief info as UTF-8 string
                    json_text = json.dumps(brief_info, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "contents": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "id": "error",
                        "name": "Error",
                        "industry": "Unknown",
                        "city": "Unknown",
                        "bio": f"Failed to fetch user data: {str(e)}",
                        "error": str(e),
                        "message": "Failed to fetch current user profile brief info"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "contents": [{"type": "text", "text": error_text}]
                        }
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown resource: {resource_uri}"
                    }
                }
        
        elif method == "tools/call":
            tool_name = request.get("params", {}).get("name")
            arguments = request.get("params", {}).get("arguments", {})
            
            if tool_name == "server_info":
                result = {
                    "name": "aihehuo-search-mcp",
                    "version": "0.1.0",
                    "api_base": AIHEHUO_API_BASE,
                }
                # Properly encode result as UTF-8
                result_text = json.dumps(result, ensure_ascii=False, indent=2)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": result_text}]
                    }
                }
            
            elif tool_name == "search_members":
                try:
                    params = SearchMembersParams(**arguments)
                    
                    # Validate query length
                    if len(params.query.strip()) <= 5:
                        error_result = {
                            "error": "Query too short",
                            "message": "搜索关键词长度必须大于5个字符",
                            "query_length": len(params.query.strip()),
                            "minimum_length": 6
                        }
                        error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [{"type": "text", "text": error_text}]
                            }
                        }
                    
                    payload = {
                        "query": params.query,
                        "paginate": params.paginate,
                        "vector_search": True
                    }
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    url = f"{AIHEHUO_API_BASE}/users/search"
                    
                    resp = requests.get(url, json=payload, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "total": 0,
                        "page": arguments.get("paginate", {}).get("page", 1),
                        "page_size": arguments.get("paginate", {}).get("per", 10),
                        "hits": [],
                        "error": str(e)
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "search_ideas":
                try:
                    params = SearchIdeasParams(**arguments)
                    
                    payload = {
                        "query": params.query,
                        "paginate": params.paginate,
                        "vector_search": True
                    }
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    url = f"{AIHEHUO_API_BASE}/ideas/search"
                    
                    resp = requests.get(url, json=payload, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "total": 0,
                        "page": arguments.get("paginate", {}).get("page", 1),
                        "page_size": arguments.get("paginate", {}).get("per", 10),
                        "hits": [],
                        "error": str(e)
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "get_group_info":
                try:
                    params = GetGroupInfoParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    # Build URL with group ID and fixed parameters: /users/e{ID}?text_only=1&all_users=1
                    url = f"{AIHEHUO_API_BASE}/users/e{params.group_id}?text_only=1&all_users=1"
                    
                    resp = requests.get(url, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "group_id": arguments.get("group_id", "unknown"),
                        "error": str(e),
                        "message": "Failed to fetch group information"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "update_bio":
                try:
                    params = UpdateBioParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    url = f"{AIHEHUO_API_BASE}/users/update_bio"
                    payload = {"bio": params.bio}
                    
                    resp = requests.put(url, json=payload, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "bio": arguments.get("bio", ""),
                        "error": str(e),
                        "message": "Failed to update user bio"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "update_goal":
                try:
                    params = UpdateGoalParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    url = f"{AIHEHUO_API_BASE}/users/update_goal"
                    payload = {"goal": params.goal}
                    
                    resp = requests.put(url, json=payload, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "goal": arguments.get("goal", ""),
                        "error": str(e),
                        "message": "Failed to update user goal"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "get_current_user_profile":
                try:
                    # Check if CURRENT_USER_ID is set
                    if CURRENT_USER_ID == "REPLACE_ME":
                        error_result = {
                            "error": "CURRENT_USER_ID not configured",
                            "message": "Please set CURRENT_USER_ID environment variable"
                        }
                        error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [{"type": "text", "text": error_text}]
                            }
                        }
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    # Build URL with current user ID: /users/{CURRENT_USER_ID}
                    url = f"{AIHEHUO_API_BASE}/users/{CURRENT_USER_ID}"
                    
                    resp = requests.get(url, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "user_id": CURRENT_USER_ID,
                        "error": str(e),
                        "message": "Failed to fetch current user profile"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "get_current_user_ideas":
                try:
                    params = GetCurrentUserIdeasParams(**arguments)
                    
                    # Check if CURRENT_USER_ID is set
                    if CURRENT_USER_ID == "REPLACE_ME":
                        error_result = {
                            "error": "CURRENT_USER_ID not configured",
                            "message": "Please set CURRENT_USER_ID environment variable"
                        }
                        error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [{"type": "text", "text": error_text}]
                            }
                        }
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    # Build URL for current user's ideas with pagination: /ideas/my_ideas
                    url = f"{AIHEHUO_API_BASE}/ideas/my_ideas"
                    
                    # Add pagination parameters to the request
                    payload = {
                        "paginate": params.paginate
                    }
                    
                    resp = requests.get(url, json=payload, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "user_id": CURRENT_USER_ID,
                        "error": str(e),
                        "message": "Failed to fetch current user ideas"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "get_idea_details":
                try:
                    params = GetIdeaDetailsParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    # Build URL for idea details: /ideas/{idea_id}
                    url = f"{AIHEHUO_API_BASE}/ideas/{params.idea_id}"
                    
                    resp = requests.get(url, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "idea_id": arguments.get("idea_id", "unknown"),
                        "error": str(e),
                        "message": "Failed to fetch idea details"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "fetch_new_users":
                try:
                    params = FetchNewUsersParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    # Fetch 10 pages of data with per=200
                    all_users = []
                    for page in range(1, 11):
                        try:
                            url = f"{AIHEHUO_API_BASE}/users/new_users"
                            payload = {
                                "paginate": {
                                    "page": page,
                                    "per": 200
                                }
                            }
                            
                            resp = requests.get(url, json=payload, headers=headers, timeout=15)
                            resp.raise_for_status()
                            resp.encoding = 'utf-8'
                            data = resp.json()
                            
                            # Extract users from response.data
                            if "data" in data and isinstance(data["data"], list):
                                # Filter to only include specified fields
                                filtered_users = []
                                for user in data["data"]:
                                    filtered_user = {
                                        "created_at_actual": user.get("created_at_actual"),
                                        "last_accessed_at_actual": user.get("last_accessed_at_actual"),
                                        "id": user.get("id"),
                                        "name": user.get("name"),
                                        "description": user.get("description"),
                                        "page_url": user.get("page_url")
                                    }
                                    filtered_users.append(filtered_user)
                                
                                all_users.extend(filtered_users)
                                
                                # If we get less than 200 users, we've reached the end
                                if len(data["data"]) < 200:
                                    break
                                    
                        except Exception as e:
                            # Log error but continue with other pages
                            print(f"Error fetching page {page}: {str(e)}")
                            continue
                    
                    # Create result with concatenated users
                    result = {
                        "total_users": len(all_users),
                        "pages_fetched": min(page, 10),
                        "users": all_users
                    }
                    
                    # Properly encode the result as UTF-8 string
                    json_text = json.dumps(result, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "error": str(e),
                        "message": "Failed to fetch new users",
                        "total_users": 0,
                        "users": []
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "get_user_details":
                try:
                    params = GetUserDetailsParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    # Build URL for user details: /users/{user_id}
                    url = f"{AIHEHUO_API_BASE}/users/{params.user_id}"
                    
                    resp = requests.get(url, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "user_id": arguments.get("user_id", "unknown"),
                        "error": str(e),
                        "message": "Failed to fetch user details"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "submit_wechat_article_draft":
                try:
                    params = SubmitWechatArticleDraftParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    # Build URL for submitting article draft: /articles/draft_wechat_article
                    url = f"{AIHEHUO_API_BASE}/articles/draft_wechat_article"
                    
                    # Prepare payload
                    payload = {
                        "title": params.title,
                        "digest": params.digest,
                        "body": params.body
                    }
                    
                    resp = requests.post(url, json=payload, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "title": arguments.get("title", ""),
                        "error": str(e),
                        "message": "Failed to submit WeChat article draft"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            elif tool_name == "create_ai_report":
                try:
                    params = CreateAIReportParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"
                    }

                    # Build URL for creating AI report: /ai_reports
                    url = f"{AIHEHUO_API_BASE}/ai_reports"
                    
                    # Prepare payload
                    payload = {
                        "title": params.title,
                        "abstract": params.abstract,
                        "html_body": params.html_body,
                        "mentioned_user_ids": params.mentioned_user_ids,
                        "mentioned_idea_ids": params.mentioned_idea_ids
                    }
                    
                    resp = requests.post(url, json=payload, headers=headers, timeout=15)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Properly encode the JSON data as UTF-8 string
                    json_text = json.dumps(data, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": json_text}]
                        }
                    }
                    
                except Exception as e:
                    error_result = {
                        "title": arguments.get("title", ""),
                        "error": str(e),
                        "message": "Failed to create AI report"
                    }
                    # Properly encode error result as UTF-8
                    error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": error_text}]
                        }
                    }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }

# === 主入口（STDIO）===
async def main() -> None:
    server = SimpleMCPServer()
    
    # 从 stdin 读取请求，向 stdout 写入响应
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            # Ensure UTF-8 output
            response_json = json.dumps(response, ensure_ascii=False)
            print(response_json, flush=True)
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            # Ensure UTF-8 output for errors too
            error_json = json.dumps(error_response, ensure_ascii=False)
            print(error_json, flush=True)

if __name__ == "__main__":
    asyncio.run(main())