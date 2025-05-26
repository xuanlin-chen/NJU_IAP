# API路由
from flask import Blueprint, request
from . import api_response
from http import HTTPStatus
from ..services.query_service import query_by_question, SearchModel
from ..services.news_service import generate_daily_news
from ..services.ddl_service import generate_ddl_events
from ..services.date_query_service import generate_date_data

# 为API路由创建Blueprint
api_bp = Blueprint('api', __name__)



@api_bp.route('/news/today', methods=['GET'])
def get_today_news():
    """获取每日新闻摘要"""
    try:
        # 调用生成每日新闻函数
        news_data = generate_daily_news()
        #example of news_data:
# [
#     {
#         'date': '2025-05-20',
#         'summary': {
#             '类型': '学术讲座',
#             '标题': '人工智能与未来教育发展论坛',
#             '关键词': 'AI, 教育创新, 未来发展',
#             '原文链接': 'https://www.nju.edu.cn/events/ai-forum-2025'
#         },
#         'abstract': '南京大学人工智能学院将于2025年5月20日举办"人工智能与未来教育发展论坛"，邀请国内外知名专家学者共同探讨AI技术在教育领域的创新应用...'
#     },
#     {
#         'date': '2025-05-20',
#         'summary': {
#             '类型': '校园通知',
#             '标题': '2025年春季学期期末考试安排',
#             '关键词': '考试安排, 期末考试, 教务通知',
#             '原文链接': 'https://www.nju.edu.cn/notice/exam-2025-spring'
#         },
#         'abstract': '2025年春季学期期末考试将于6月20日至7月5日进行，请各位同学注意查看具体考试时间安排，做好复习准备...'
#     }
# ]
        if not news_data:
            return api_response({
                'date': news_data['date'],
                'summary': '今日暂无更新',
                'raw_messages': []
            }, message='今日暂无新闻更新')
        return api_response(news_data, message='获取新闻成功')
    except Exception as e:
        print(f'获取每日新闻失败: {str(e)}')
        return api_response(message='获取新闻失败，请稍后重试', code=500)

@api_bp.route('/ddl-events', methods=['GET'])
def get_ddl_events():
    """获取近期重要截止日期事件列表"""
    try:
        # 调用生成DDL事件函数
        events_data = generate_ddl_events()
        #example of events_data:
# [
#     {
#         'date': '2025-05-20',
#         'summary': {
#             '类型': '讲座/分享会信息',
#             '标题': '2025春季校园招聘宣讲会',
#             '截止时间': '2025-05-25 18:00:00',
#             '原文链接': 'https://www.nju.edu.cn/events/career-talk-2025'
#         }
#     },
#     {
#         'date': '2025-05-20',
#         'summary': {
#             '类型': '学业申请',
#             '标题': '2025年秋季学期交换生项目申请',
#             '截止时间': '2025-06-01 23:59:59',
#             '原文链接': 'https://www.nju.edu.cn/exchange/fall-2025'
#         }
#     }
# ]
        if not events_data:
            return api_response({
                'date': events_data['date'],
                'summary': [],
                'raw_messages': []
            }, message='今日暂无DDL事件')
        return api_response(events_data, message='获取DDL事件成功')
    except Exception as e:
        print(f'获取DDL事件失败: {str(e)}')
        return api_response(message='获取DDL事件失败，请稍后重试', code=500)

@api_bp.route('/date-query', methods=['GET'])
def query_by_date():
    """根据日期获取新闻和DDL事件"""
    try:
        # 从请求参数中获取日期
        date_str = request.args.get('date')
        if not date_str:
            return api_response(message="日期参数不能为空", code=400)
            
        # 调用日期查询服务
        result_data = generate_date_data(date_str)
        
        # 检查是否有错误
        if 'error' in result_data:
            return api_response(result_data, message=result_data['error'], code=400)
            
        return api_response(result_data, message='查询成功')
    except Exception as e:
        print(f'日期查询失败: {str(e)}')
        return api_response(message='日期查询失败，请稍后重试', code=500)

@api_bp.route('/knowledge/query', methods=['POST'])
def query_knowledge():
    """知识库问答接口"""
#example of request:
#header添加 Content-Type: application/json
# - 设置请求体（Body）：
# - 选择 raw 选项
# - 格式选择 JSON
# {
#     'question': '最近有什么活动？',
#     'model': 'RAG'
# }
    #example of response:
# {
#     'code': 200,
#     'message': '查询成功',
#     'data': {
#         'recommendation': '根据最新信息，近期有以下活动：\n1. 人工智能与未来教育发展论坛（2025年5月20日）\n2. 2025春季校园招聘宣讲会（截止时间：2025-05-25）\n3. 2025年秋季学期交换生项目申请（截止时间：2025-06-01）'
#     }
# }
    try:
        # 从请求体中获取问题和查询模型
        data = request.get_json()
        if not data or 'question' not in data:
            return api_response(message="问题不能为空", code=400)
            
        question = data['question']
        model = data.get('model', 'RAG')
        
        # 转换模型类型
        try:
            search_model = SearchModel[model]
        except KeyError:
            return api_response(message=f"不支持的查询模型类型: {model}", code=400)
        
        # 调用查询服务
        result = query_by_question(question, search_model)
        
        # 如果返回结果包含错误信息
        if 'code' in result and result['code'] != HTTPStatus.OK:
            return api_response(result, message=result['message'], code=result['code'])
            
        return api_response(result, message='查询成功')
    except Exception as e:
        print(f'知识查询失败: {str(e)}')
        return api_response(message='知识查询失败，请稍后重试', code=500)

@api_bp.route('/docs', methods=['GET'])
def api_docs():
    """返回API文档"""
    from ..settings import MESSAGE_TYPES
    
    docs = {
        "api_version": "1.0",
        "base_url": "/api",
        "description": "南京大学信息聚合平台API文档",
        "message_types": {
            "description": "系统支持的消息类型",
            "types": list(MESSAGE_TYPES.keys())
        },
        "response_format": {
            "description": "所有API响应都遵循以下统一格式",
            "schema": {
                "code": "状态码，200表示成功，其他值表示错误",
                "message": "响应消息，用于描述请求结果",
                "data": "响应数据，具体格式参见各接口说明",
                "errors": "错误详情，仅在发生错误时出现"
            }
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
                            "date": "日期（ISO格式，如：2024-01-20）",
                            "summary": "每日新闻摘要，包含标题，类型等",
                            "raw_messages": "原始消息数据，包含完整的新闻信息"
                        }
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {
                            "code": 500,
                            "message": "获取新闻失败，请稍后重试"
                        }
                    }
                },
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
                            "date": "日期（ISO格式，如：2024-01-20）",
                            "summary": "DDL事件列表",
                        }
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {
                            "code": 500,
                            "message": "获取DDL事件失败，请稍后重试"
                        }
                    }
                },
            },
            {
                "path": "/api/date-query",
                "method": "GET",
                "description": "根据日期获取新闻和DDL事件",
                "parameters": [
                    {
                        "name": "date",
                        "type": "string",
                        "required": True,
                        "description": "查询日期，格式为YYYY-MM-DD"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "date": "查询日期（ISO格式，如：2024-01-20）",
                            "news": "该日期的新闻列表",
                            "ddl_events": "该日期的DDL事件列表"
                        }
                    },
                    "400": {
                        "description": "请求参数错误",
                        "schema": {
                            "code": 400,
                            "message": "日期参数不能为空或日期格式错误"
                        }
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {
                            "code": 500,
                            "message": "日期查询失败，请稍后重试"
                        }
                    }
                },
            },
            {
                "path": "/api/knowledge/query",
                "method": "POST",
                "description": "知识库问答接口",
                "content_type": "application/json",
                "request_body": {
                    "type": "raw",
                    "format": "JSON"
                },
                "parameters": [
                    {
                        "name": "question",
                        "type": "string",
                        "required": True,
                        "description": "用户的问题"
                    },
                    {
                        "name": "model",
                        "type": "string",
                        "required": False,
                        "description": "查询模型类型，可选值：RAG（默认）、MCP"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "recommendation": "模型返回的回答内容"
                        }
                    },
                    "400": {
                        "description": "请求参数错误",
                        "schema": {
                            "code": 400,
                            "message": "问题不能为空或不支持的查询模型类型"
                        }
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {
                            "code": 500,
                            "message": "知识查询失败，请稍后重试"
                        }
                    }
                },
            }
        ]
    }
    return api_response(docs)