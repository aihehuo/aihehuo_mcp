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

# === 定义请求/响应模型 ===
class SearchMembersParams(BaseModel):
    query: str = Field(..., description="搜索关键词")
    paginate: Dict[str, int] = Field(default_factory=lambda: {"page": 1, "per": 10}, description="分页参数")

class SearchIdeasParams(BaseModel):
    query: str = Field(..., description="搜索关键词")
    paginate: Dict[str, int] = Field(default_factory=lambda: {"page": 1, "per": 10}, description="分页参数")

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
                        "tools": {"listChanged": True}
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