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

# === 微信文章HTML模板 ===
WECHAT_ARTICLE_TEMPLATE = """<!-- 微信公众号文章HTML模板 - 爱合伙创业者推荐 -->

<div style="max-width: 677px; margin: 0 auto; background: white; overflow: hidden;">
    
    <!-- ========== 头部区域 ========== -->
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); color: white; padding: 30px 20px; text-align: center;">
        <h1 style="font-size: 1.6em; margin-bottom: 8px; font-weight: 600; line-height: 1.4;">🎯 【文章主标题】</h1>
        <div style="font-size: 0.95em; opacity: 0.95; margin-top: 5px;">【副标题，如：10月10日新增创业者精选】</div>
    </div>
    
    <div style="padding: 25px 18px;">
        
        <!-- ========== 数据概览区域 ========== -->
        <div style="margin-bottom: 35px;">
            <h2 style="font-size: 1.35em; color: #2c3e50; margin-bottom: 18px; padding-bottom: 8px; border-bottom: 2px solid #ff6b6b; font-weight: 600;">
                <span style="margin-right: 6px;">📊</span>【章节标题，如：10月10日新增创业者画像】
            </h2>
            
            <div style="background: #fafafa; padding: 20px; border-radius: 8px; margin-bottom: 25px; font-size: 0.95em;">
                <p style="margin-bottom: 12px; line-height: 1.8;">【开场介绍段落】</p>
                
                <h3 style="color: #2c3e50; margin-bottom: 12px; font-size: 1.1em; font-weight: 600;">【小标题】</h3>
                <p style="margin-bottom: 12px; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">【数据维度1】：</strong>【数据描述内容】
                </p>
                <p style="margin-bottom: 12px; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">【数据维度2】：</strong>【数据描述内容】
                </p>
                <p style="margin-bottom: 12px; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">【数据维度3】：</strong>【数据描述内容】
                </p>
                <p style="margin-bottom: 12px; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">【数据维度4】：</strong>【数据描述内容】
                </p>
            </div>
        </div>
        
        <!-- ========== 带项目创始人部分 ========== -->
        <div style="margin-bottom: 35px;">
            <h2 style="font-size: 1.35em; color: #2c3e50; margin-bottom: 18px; padding-bottom: 8px; border-bottom: 2px solid #ff6b6b; font-weight: 600;">
                <span style="margin-right: 6px;">🚀</span>【章节标题，如：带项目的典型创始人】
            </h2>
            
            <!-- === 创始人卡片模板 - 开始 === -->
            <div style="background: #fafafa; border-left: 3px solid #ff6b6b; border-radius: 6px; padding: 20px; margin-bottom: 20px;">
                
                <!-- 用户头部信息 -->
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 8px;">
                        <div style="font-size: 1.25em; font-weight: 600; color: #2c3e50;">【用户姓名】</div>
                        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); color: white; padding: 3px 12px; border-radius: 12px; font-size: 0.85em; font-weight: 500;">【创业号8位数字】</div>
                    </div>
                    <div style="background: #10b981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 500; display: inline-block;">带项目创始人</div>
                </div>
                
                <!-- 项目标题 -->
                <div style="font-size: 1.05em; color: #374151; margin-bottom: 12px; font-weight: 600; line-height: 1.6;">
                    【emoji】 【项目名称/方向描述】
                </div>
                
                <!-- 创业者背景 -->
                <div style="margin-bottom: 10px; font-size: 0.95em; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">创业者背景：</strong>【工作经历、教育背景、行业经验等】
                </div>
                
                <!-- 项目亮点 -->
                <div style="background: #fff9e6; border-left: 3px solid #fbbf24; padding: 12px; margin: 12px 0; border-radius: 4px; font-size: 0.95em; line-height: 1.8;">
                    <strong>💡 项目亮点：</strong>【项目的核心优势、商业模式、市场机会等】
                </div>
                
                <!-- 寻找资源 -->
                <div style="margin-bottom: 10px; font-size: 0.95em; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">🔍 寻找资源：</strong>【需要什么类型的合伙人或资源】
                </div>
                
                <!-- 联想点 -->
                <div style="background: #eff6ff; border-left: 3px solid #3b82f6; padding: 12px; margin: 12px 0; border-radius: 4px; font-size: 0.95em; line-height: 1.8;">
                    <strong>🎯 联想点：</strong>【适合什么样的合伙人、市场分析、合作建议等】
                </div>
            </div>
            <!-- === 创始人卡片模板 - 结束 === -->
            
            <!-- 复制上面的卡片结构，添加更多创始人 -->
            
        </div>
        
        <!-- ========== 找项目合伙人部分 ========== -->
        <div style="margin-bottom: 35px;">
            <h2 style="font-size: 1.35em; color: #2c3e50; margin-bottom: 18px; padding-bottom: 8px; border-bottom: 2px solid #ff6b6b; font-weight: 600;">
                <span style="margin-right: 6px;">🤝</span>【章节标题，如：寻找项目的优质合伙人】
            </h2>
            
            <!-- === 合伙人卡片模板 - 开始 === -->
            <div style="background: #fafafa; border-left: 3px solid #ff6b6b; border-radius: 6px; padding: 20px; margin-bottom: 20px;">
                
                <!-- 用户头部信息 -->
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 8px;">
                        <div style="font-size: 1.25em; font-weight: 600; color: #2c3e50;">【用户姓名】</div>
                        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); color: white; padding: 3px 12px; border-radius: 12px; font-size: 0.85em; font-weight: 500;">【创业号8位数字】</div>
                    </div>
                    <div style="background: #3b82f6; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 500; display: inline-block;">找项目合伙人</div>
                </div>
                
                <!-- 合伙人定位 -->
                <div style="font-size: 1.05em; color: #374151; margin-bottom: 12px; font-weight: 600; line-height: 1.6;">
                    【emoji】 【合伙人定位描述】
                </div>
                
                <!-- 背景介绍 -->
                <div style="margin-bottom: 10px; font-size: 0.95em; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">背景：</strong>【教育背景、工作经历、创业经历等】
                </div>
                
                <!-- 优势技能 -->
                <div style="margin-bottom: 10px; font-size: 0.95em; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">优势：</strong>【核心技能、资源、经验等】
                </div>
                
                <!-- 寻找诉求 -->
                <div style="margin-bottom: 10px; font-size: 0.95em; line-height: 1.8;">
                    <strong style="color: #ff6b6b; font-weight: 600;">诉求：</strong>【想找什么类型的项目或创始人】
                </div>
                
                <!-- 适配项目 -->
                <div style="background: #fff9e6; border-left: 3px solid #fbbf24; padding: 12px; margin: 12px 0; border-radius: 4px; font-size: 0.95em; line-height: 1.8;">
                    <strong>💡 适配项目：</strong>【适合加入哪些类型的项目】
                </div>
                
                <!-- 联想点 -->
                <div style="background: #eff6ff; border-left: 3px solid #3b82f6; padding: 12px; margin: 12px 0; border-radius: 4px; font-size: 0.95em; line-height: 1.8;">
                    <strong>🎯 联想点：</strong>【这位合伙人的特殊价值、适合的创始人类型等】
                </div>
            </div>
            <!-- === 合伙人卡片模板 - 结束 === -->
            
            <!-- 复制上面的卡片结构，添加更多合伙人 -->
            
        </div>
        
        <!-- ========== 数据观察/总结区域 ========== -->
        <div style="margin-bottom: 35px;">
            <div style="background: #f0fdf4; border-radius: 8px; padding: 20px; margin-top: 25px;">
                <h3 style="color: #059669; margin-bottom: 15px; font-size: 1.2em; font-weight: 600;">💡 【观察标题，如：数据观察】</h3>
                
                <ul style="list-style: none; padding-left: 0;">
                    <li style="padding: 8px 0 8px 20px; position: relative; line-height: 1.8; font-size: 0.95em;">
                        <span style="position: absolute; left: 0; color: #059669; font-weight: bold; font-size: 1.2em;">•</span>
                        <strong>【观察点标题】：</strong>【观察内容描述】
                    </li>
                    <li style="padding: 8px 0 8px 20px; position: relative; line-height: 1.8; font-size: 0.95em;">
                        <span style="position: absolute; left: 0; color: #059669; font-weight: bold; font-size: 1.2em;">•</span>
                        <strong>【观察点标题】：</strong>【观察内容描述】
                    </li>
                    <li style="padding: 8px 0 8px 20px; position: relative; line-height: 1.8; font-size: 0.95em;">
                        <span style="position: absolute; left: 0; color: #059669; font-weight: bold; font-size: 1.2em;">•</span>
                        <strong>【观察点标题】：</strong>【观察内容描述】
                    </li>
                    <li style="padding: 8px 0 8px 20px; position: relative; line-height: 1.8; font-size: 0.95em;">
                        <span style="position: absolute; left: 0; color: #059669; font-weight: bold; font-size: 1.2em;">•</span>
                        <strong>【观察点标题】：</strong>【观察内容描述】
                    </li>
                    <li style="padding: 8px 0 8px 20px; position: relative; line-height: 1.8; font-size: 0.95em;">
                        <span style="position: absolute; left: 0; color: #059669; font-weight: bold; font-size: 1.2em;">•</span>
                        <strong>【观察点标题】：</strong>【观察内容描述】
                    </li>
                </ul>
                
                <!-- 温馨提示框 -->
                <div style="margin-top: 20px; padding: 15px; background: white; border-radius: 6px; border-left: 3px solid #059669;">
                    <strong style="color: #059669; font-size: 1em;">📌 【提示标题】</strong>
                    <p style="margin-top: 8px; font-size: 0.95em; line-height: 1.8;">【提示内容描述】</p>
                </div>
            </div>
        </div>
        
    </div>
</div>"""

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
    body: Optional[str] = Field(None, description="文章正文HTML内容（仅包含body标签内的内容，不能包含超链接<a>标签）。与body_file二选一")
    body_file: Optional[str] = Field(None, description="HTML文件路径（与body二选一，用于大型HTML内容）")

class CreateAIReportParams(BaseModel):
    title: str = Field(..., description="报告标题")
    abstract: str = Field(..., description="报告摘要/简介")
    html_body: Optional[str] = Field(None, description="报告正文HTML内容（与html_file_path二选一）")
    html_file_path: Optional[str] = Field(None, description="HTML文件路径（与html_body二选一，用于大型HTML内容）")
    mentioned_user_ids: List[str] = Field(default_factory=list, description="报告中提及的用户ID列表（注意是ID字符串，不是number）")
    mentioned_idea_ids: List[str] = Field(default_factory=list, description="报告中提及的项目/想法ID列表")

class GetLatest24hIdeasParams(BaseModel):
    paginate: Dict[str, int] = Field(default_factory=lambda: {"page": 1, "per": 10}, description="分页参数")

# === 爱合伙 MCP 服务器实现 ===
class AihehuoMCPServer:
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
                "description": "获取群组基本情况和群内所有成员数据（一次性获取所有用户）。数据会自动保存为Markdown文件到/tmp目录，返回文件路径。使用read_file工具读取文件内容",
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
                "description": "获取新用户列表，分页获取3页数据并合并（每页50个用户）",
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
                "description": "提交微信文章草稿。注意：文章正文不能包含超链接（<a>标签）。支持直接提供HTML内容或提供HTML文件路径",
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
                            "description": "文章正文HTML内容（仅包含body标签内的内容，不包含<body>标签本身，不能包含超链接<a>标签）。与body_file二选一"
                        },
                        "body_file": {
                            "type": "string",
                            "description": "HTML文件的绝对路径。当HTML内容太大时使用此参数。与body二选一"
                        }
                    },
                    "required": ["title", "digest"]
                }
            },
            "create_ai_report": {
                "name": "create_ai_report",
                "description": "创建AI生成的报告并在官网展示。与微信文章不同，报告可以包含超链接，并可以关联提及的用户和项目。支持直接提供HTML内容或提供HTML文件路径",
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
                            "description": "报告正文HTML内容（可以包含超链接）。与html_file_path二选一"
                        },
                        "html_file_path": {
                            "type": "string",
                            "description": "HTML文件的绝对路径。当HTML内容太大时使用此参数。与html_body二选一"
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
                    "required": ["title", "abstract"]
                }
            },
            "get_latest_24h_ideas": {
                "name": "get_latest_24h_ideas",
                "description": "获取过去24小时内最新发布的创业项目/想法。返回LLM优化的纯文本格式，便于AI分析和处理。自动过滤已删除和待审核的项目",
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

                    url = f"{AIHEHUO_API_BASE}/users/e{params.group_id}?all_users=1"
                    
                    resp = requests.get(url, headers=headers, timeout=30)
                    resp.raise_for_status()
                    # Ensure response is decoded as UTF-8
                    resp.encoding = 'utf-8'
                    data = resp.json()
                    
                    # Extract group data from response
                    group_data = data.get("data", {}).get("group", {})
                    
                    # Format as Markdown
                    md_content = []
                    md_content.append(f"# {group_data.get('title', '群组信息')}\n")
                    md_content.append(f"**群组ID**: {group_data.get('id', 'N/A')}\n")
                    md_content.append(f"\n## 群组介绍\n")
                    md_content.append(f"{group_data.get('intro', 'N/A')}\n")
                    md_content.append(f"\n## 群组描述\n")
                    md_content.append(f"{group_data.get('description', 'N/A')}\n")
                    md_content.append(f"\n## 群友列表\n")
                    
                    users = group_data.get("users", [])
                    if users:
                        for i, user in enumerate(users, 1):
                            user_text = user.get("user_text", "")
                            md_content.append(f"\n### {i}. 群友信息\n")
                            md_content.append(f"{user_text}\n")
                    else:
                        md_content.append("\n暂无群友数据\n")
                    
                    # Save to /tmp directory
                    filename = f"/tmp/group_{params.group_id}.md"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(md_content))
                    
                    # Return success message with file path
                    result = {
                        "success": True,
                        "message": f"群组数据已保存为Markdown文件（包含所有{len(users)}位群友）",
                        "file_path": filename,
                        "group_id": group_data.get('id', 'N/A'),
                        "group_title": group_data.get('title', 'N/A'),
                        "total_users": len(users),
                        "note": "请使用read_file工具读取该文件以查看完整的群组和群友信息"
                    }
                    
                    result_text = json.dumps(result, ensure_ascii=False, indent=2)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": result_text}]
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

                    # Fetch 3 pages of data with per=50
                    all_users = []
                    for page in range(1, 4):
                        try:
                            url = f"{AIHEHUO_API_BASE}/users/new_users"
                            payload = {
                                "paginate": {
                                    "page": page,
                                    "per": 50
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
                                    filtered_users.append(user)
                                
                                all_users.extend(filtered_users)
                                
                                # If we get less than 50 users, we've reached the end
                                if len(data["data"]) < 50:
                                    break
                                    
                        except Exception as e:
                            # Log error but continue with other pages
                            print(f"Error fetching page {page}: {str(e)}")
                            continue
                    
                    # Create result with concatenated users
                    result = {
                        "total_users": len(all_users),
                        "pages_fetched": min(page, 10),
                        "users": all_users,
                        "html_body_template": WECHAT_ARTICLE_TEMPLATE
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

                    # Validate that either body or body_file is provided
                    if not params.body and not params.body_file:
                        error_result = {
                            "error": "Missing required parameter",
                            "message": "Either body or body_file must be provided"
                        }
                        error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [{"type": "text", "text": error_text}]
                            }
                        }

                    # If both are provided, return error
                    if params.body and params.body_file:
                        error_result = {
                            "error": "Conflicting parameters",
                            "message": "Only one of body or body_file should be provided, not both"
                        }
                        error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [{"type": "text", "text": error_text}]
                            }
                        }

                    # Build URL for submitting article draft: /articles/draft_wechat_article
                    url = f"{AIHEHUO_API_BASE}/articles/draft_wechat_article"

                    # Use different request methods based on whether file or body is provided
                    if params.body_file:
                        # Upload file using multipart/form-data
                        try:
                            # Verify file exists
                            if not os.path.exists(params.body_file):
                                error_result = {
                                    "error": "File not found",
                                    "message": f"HTML file not found at path: {params.body_file}"
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
                                "Accept": "application/json",
                                "User-Agent": "LLM_AGENT"
                            }

                            # Prepare multipart form data (no nested schema)
                            with open(params.body_file, 'rb') as f:
                                files = {
                                    'body_file': ('article.html', f, 'text/html')
                                }
                                data = [
                                    ('title', params.title),
                                    ('digest', params.digest)
                                ]

                                resp = requests.post(url, headers=headers, files=files, data=data, timeout=30)

                        except Exception as file_error:
                            error_result = {
                                "error": "File upload error",
                                "message": f"Failed to upload HTML file: {str(file_error)}"
                            }
                            error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                            return {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "result": {
                                    "content": [{"type": "text", "text": error_text}]
                                }
                            }
                    else:
                        # Use JSON request with body (no nested schema)
                        headers = {
                            "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "User-Agent": "LLM_AGENT"
                        }

                        payload = {
                            "title": params.title,
                            "digest": params.digest,
                            "body": params.body
                        }

                        resp = requests.post(url, json=payload, headers=headers, timeout=30)

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

                    # Validate that either html_body or html_file_path is provided
                    if not params.html_body and not params.html_file_path:
                        error_result = {
                            "error": "Missing required parameter",
                            "message": "Either html_body or html_file_path must be provided"
                        }
                        error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [{"type": "text", "text": error_text}]
                            }
                        }

                    # If both are provided, prefer html_body
                    if params.html_body and params.html_file_path:
                        error_result = {
                            "error": "Conflicting parameters",
                            "message": "Only one of html_body or html_file_path should be provided, not both"
                        }
                        error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [{"type": "text", "text": error_text}]
                            }
                        }

                    # Build URL for creating AI report: /ai_reports
                    url = f"{AIHEHUO_API_BASE}/ai_reports"

                    # Use different request methods based on whether file or body is provided
                    if params.html_file_path:
                        # Upload file using multipart/form-data
                        try:
                            # Verify file exists
                            if not os.path.exists(params.html_file_path):
                                error_result = {
                                    "error": "File not found",
                                    "message": f"HTML file not found at path: {params.html_file_path}"
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
                                "Accept": "application/json",
                                "User-Agent": "LLM_AGENT"
                            }

                            # Prepare multipart form data with ai_report schema
                            with open(params.html_file_path, 'rb') as f:
                                files = {
                                    'ai_report[html_file]': ('report.html', f, 'text/html')
                                }
                                
                                # Build form data with proper array handling for Rails
                                # Rails expects array fields as multiple 'field[]' entries
                                data = [
                                    ('ai_report[title]', params.title),
                                    ('ai_report[abstract]', params.abstract)
                                ]
                                
                                # Add array fields - each item as separate field with [] notation
                                for user_id in params.mentioned_user_ids:
                                    data.append(('ai_report[mentioned_user_ids][]', user_id))
                                
                                for idea_id in params.mentioned_idea_ids:
                                    data.append(('ai_report[mentioned_idea_ids][]', idea_id))

                                resp = requests.post(url, headers=headers, files=files, data=data, timeout=30)

                        except Exception as file_error:
                            error_result = {
                                "error": "File upload error",
                                "message": f"Failed to upload HTML file: {str(file_error)}"
                            }
                            error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
                            return {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "result": {
                                    "content": [{"type": "text", "text": error_text}]
                                }
                            }
                    else:
                        # Use JSON request with html_body
                        headers = {
                            "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "User-Agent": "LLM_AGENT"
                        }

                        payload = {
                            "ai_report": {
                                "title": params.title,
                                "abstract": params.abstract,
                                "html_body": params.html_body,
                                "mentioned_user_ids": params.mentioned_user_ids,
                                "mentioned_idea_ids": params.mentioned_idea_ids
                            }
                        }

                        resp = requests.post(url, json=payload, headers=headers, timeout=30)

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
            
            elif tool_name == "get_latest_24h_ideas":
                try:
                    params = GetLatest24hIdeasParams(**arguments)
                    
                    headers = {
                        "Authorization": f"Bearer {AIHEHUO_API_KEY}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "LLM_AGENT"  # Request LLM-optimized format
                    }

                    # Build URL for latest 24h ideas: /ideas/latest_24h
                    url = f"{AIHEHUO_API_BASE}/ideas/latest_24h"
                    
                    # Add pagination parameters to the request
                    request_params = {
                        "paginate[page]": params.paginate.get("page", 1),
                        "paginate[per]": params.paginate.get("per", 10)
                    }
                    
                    resp = requests.get(url, params=request_params, headers=headers, timeout=15)
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
                        "error": str(e),
                        "message": "Failed to fetch latest 24h ideas",
                        "paginate": arguments.get("paginate", {})
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
    server = AihehuoMCPServer()
    
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