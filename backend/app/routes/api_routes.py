# API路由
from flask import Blueprint, request
from . import api_response
import json

# from services.query_service import query_by_question
from ..services.news_service import generate_daily_news
from ..services.ddl_service import generate_ddl_events

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

# @api_bp.route('/knowledge/query', methods=['POST'])
# def ask_question():
#     """处理用户问题的完整流程"""
#     try:
#         # 获取用户问题
#         data = request.get_json()
#         if not data or 'question' not in data:
#             return api_response(message="问题不能为空", code=400)
            
#         question = data.get('question', '')
        
#         # 使用AI提取查询标签
#         extracted_tags = extract_tags_with_ai(question)
        
#         # 查询相关信息 - 使用灵活查询函数
#         results = query_by_question(question, extracted_tags)
        
#         # 生成答案
#         answer = generate_answer_with_ai(question, results)
        
#         # 构建响应数据 - 包含更多信息
#         references = []
#         for i, r in enumerate(results):
#             # 提取标签和内容的摘要信息
#             tags_summary = ", ".join([f"{k}: {v}" for k, v in r.get('tags', {}).items() if k != 'time'])
#             content_preview = str(r.get('content', {}))[:50] + '...' if r.get('content') else ''
            
#             reference = {
#                 'id': i+1,
#                 'type': r.get('message_type', '未知类型'),
#                 'tags': tags_summary,
#                 'content_preview': content_preview
#             }
#             references.append(reference)
        
#         response_data = {
#             'question': question,
#             'extracted_tags': extracted_tags,  # 添加提取的标签
#             'answer': answer,
#             'references': references
#         }
        
#         return api_response(response_data)
#     except Exception as e:
#         return api_response(message=str(e), code=500)

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
                            "question": "用户提交的原始问题",
                            "extracted_tags": "AI系统提取的关键查询标签列表",
                            "answer": "AI生成的结构化答案",
                            "references": "参考资料列表，每条参考资料包含以下字段",
                            "reference_structure": {
                                "id": "参考资料ID",
                                "type": "消息类型",
                                "tags": "相关标签摘要",
                                "content_preview": "内容预览（限50字）"
                            }
                        }
                    },
                    "400": {
                        "description": "请求参数错误",
                        "schema": {
                            "code": 400,
                            "message": "问题不能为空"
                        }
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {
                            "code": 500,
                            "message": "处理问题失败，请稍后重试"
                        }
                    }
                },
                "example_response": {
                    "code": 200,
                    "message": "查询成功",
                    "data": {
                        "question": "如何申请成绩单？",
                        "extracted_tags": ["成绩单", "教务", "申请流程"],
                        "answer": "您可以通过以下方式申请成绩单：\n1. 教务系统自助打印\n2. 教务处人工服务窗口办理",
                        "references": [{
                            "id": 1,
                            "type": "学业相关政策",
                            "tags": "教务, 成绩单, 流程",
                            "content_preview": "成绩单申请流程说明：1.登录教务系统..."
                        }]
                    }
                }
            },
            
        ]
    }
    return api_response(docs)