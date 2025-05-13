# API路由
from flask import Blueprint, request
from . import api_response
import json

from app.services.query_service import query_messages, query_by_question
from app.services.ai_service import extract_tags_with_ai, generate_answer_with_ai
from app.services.news_service import generate_daily_news, generate_ddl_events

# 为API路由创建Blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/messages', methods=['GET'])
def get_messages():
    """直接查询消息（高级用户使用）"""
    try:
        # 获取查询参数
        message_type = request.args.get('message_type')
        query_conditions_str = request.args.get('query_conditions', '{}')
        
        # 验证消息类型
        if not message_type:
            return api_response(message="消息类型是必需的", code=400)
        
        # 解析查询条件
        try:
            query_conditions = json.loads(query_conditions_str)
        except json.JSONDecodeError:
            return api_response(message="查询条件必须是有效的JSON格式", code=400)
        
        # 执行查询
        results = query_messages(message_type, query_conditions)
        
        return api_response(results)
    except Exception as e:
        return api_response(message=str(e), code=500)

@api_bp.route('/news/today', methods=['GET'])
def get_today_news():
    """获取每日新闻摘要"""
    try:
        # 调用生成每日新闻函数
        news_data = generate_daily_news()
        return api_response(news_data)
    except Exception as e:
        return api_response(message=str(e), code=500)

@api_bp.route('/ddl-events', methods=['GET'])
def get_ddl_events():
    """获取近期重要截止日期事件列表"""
    try:
        # 调用生成DDL事件函数
        events_data = generate_ddl_events()
        return api_response(events_data)
    except Exception as e:
        return api_response(message=str(e), code=500)

@api_bp.route('/knowledge/query', methods=['POST'])
def ask_question():
    """处理用户问题的完整流程"""
    try:
        # 获取用户问题
        data = request.get_json()
        if not data or 'question' not in data:
            return api_response(message="问题不能为空", code=400)
            
        question = data.get('question', '')
        
        # 使用AI提取查询标签
        extracted_tags = extract_tags_with_ai(question)
        
        # 查询相关信息 - 使用灵活查询函数
        results = query_by_question(question, extracted_tags)
        
        # 生成答案
        answer = generate_answer_with_ai(question, results)
        
        # 构建响应数据 - 包含更多信息
        references = []
        for i, r in enumerate(results):
            # 提取标签和内容的摘要信息
            tags_summary = ", ".join([f"{k}: {v}" for k, v in r.get('tags', {}).items() if k != 'time'])
            content_preview = str(r.get('content', {}))[:50] + '...' if r.get('content') else ''
            
            reference = {
                'id': i+1,
                'type': r.get('message_type', '未知类型'),
                'tags': tags_summary,
                'content_preview': content_preview
            }
            references.append(reference)
        
        response_data = {
            'question': question,
            'extracted_tags': extracted_tags,  # 添加提取的标签
            'answer': answer,
            'references': references
        }
        
        return api_response(response_data)
    except Exception as e:
        return api_response(message=str(e), code=500)

@api_bp.route('/docs', methods=['GET'])
def api_docs():
    """返回API文档"""
    from ..config.settings import MESSAGE_TYPES
    
    docs = {
        "api_version": "1.0",
        "message_types": {
            "description": "系统支持的消息类型",
            "types": list(MESSAGE_TYPES.keys())
        },
        "endpoints": [
            {
                "path": "/api/news/today",
                "method": "GET",
                "description": "获取每日消息摘要",
                "parameters": [],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "date": "日期（ISO格式）",
                            "content": "消息内容（文本或JSON）",
                            "format": "内容格式（文本或json）"
                        }
                    }
                }
            },
            {
                "path": "/api/ddl-events",
                "method": "GET",
                "description": "获取即将到来的重要截止日期事件列表",
                "parameters": [],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "name": "事件名称",
                            "ddl": "截止日期（YYYY-MM-DD）"
                        }
                    }
                }
            },
            {
                "path": "/api/knowledge/query",
                "method": "POST",
                "description": "智能问答",
                "parameters": [
                    {
                        "name": "question",
                        "type": "string",
                        "required": True,
                        "description": "用户问题"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "question": "用户问题",
                            "extracted_tags": "AI提取的查询标签",
                            "answer": "AI生成的答案",
                            "references": "参考资料，包括消息类型、标签摘要和内容预览"
                        }
                    }
                }
            },
            {
                "path": "/api/messages",
                "method": "GET",
                "description": "直接消息查询（高级用户）",
                "parameters": [
                    {
                        "name": "message_type",
                        "type": "string",
                        "required": True,
                        "description": "消息类型，参考message_types字段"
                    },
                    {
                        "name": "query_conditions",
                        "type": "json",
                        "required": False,
                        "description": "查询条件，JSON格式，包括标签和内容部分"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "id": "消息ID",
                            "tags": "标签JSON对象",
                            "content": "内容JSON对象",
                            "message_type": "消息类型"
                        }
                    }
                }
            }
        ]
    }
    return api_response(docs)