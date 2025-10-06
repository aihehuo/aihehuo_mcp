# server.py
import asyncio
import json
import os
import sys
import warnings
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

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
                "description": "搜索爱合伙平台上的创业者/会员",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
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
                "description": "搜索爱合伙平台上的创业想法/项目",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
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
            }
        }
        
        # Initialize prompts
        self.prompts = {
            "pitch": {
                "name": "pitch",
                "description": "Create a compelling 60-second elevator pitch based on your validated business model and required artifacts",
                "arguments": [
                    {
                        "name": "arguments",
                        "description": "User input arguments for the pitch",
                        "required": False
                    }
                ]
            }
        }
        
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
                # Read the prompt content from the file
                try:
                    import os
                    
                    # Get current working directory for debugging
                    cwd = os.getcwd()
                    
                    # Try multiple possible paths for different deployment scenarios
                    possible_paths = [
                        f"aihehuo_mcp/prompts/{prompt_name}.md",  # Local development
                        f"prompts/{prompt_name}.md",  # Git repo deployment
                        f"./prompts/{prompt_name}.md",  # Relative path
                        f"../prompts/{prompt_name}.md",  # Parent directory
                        f"{cwd}/prompts/{prompt_name}.md",  # Absolute path
                        f"{cwd}/aihehuo_mcp/prompts/{prompt_name}.md"  # Absolute path with package
                    ]
                    
                    prompt_content = None
                    found_path = None
                    for path in possible_paths:
                        try:
                            with open(path, 'r', encoding='utf-8') as f:
                                prompt_content = f.read()
                                found_path = path
                                break
                        except FileNotFoundError:
                            continue
                    
                    if prompt_content is None:
                        # List directory contents for debugging
                        try:
                            dir_contents = os.listdir(cwd)
                        except:
                            dir_contents = "Unable to list directory"
                        
                        error_msg = f"Prompt file '{prompt_name}.md' not found. Current directory: {cwd}. Tried paths: {possible_paths}. Directory contents: {dir_contents}"
                        raise FileNotFoundError(error_msg)
                    
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
                except FileNotFoundError:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": f"Prompt file not found: {prompt_name}.md"
                        }
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": f"Error reading prompt: {str(e)}"
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
                    
                    payload = {
                        "query": params.query,
                        "paginate": params.paginate
                    }
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
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
                        "paginate": params.paginate
                    }
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
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