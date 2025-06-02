# API路由
from flask import Blueprint, request, session
from .__init__ import api_response
from http import HTTPStatus
from ..services.query_service import query_by_question
from ..services.date_query_service import generate_date_data
from ..models.user import User
from ..db import db
from typing import cast
from flask import jsonify
from ..services.mcp_query_function import get_query_progress

# 为API路由创建Blueprint
api_bp = Blueprint("api", __name__)


@api_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # 验证请求数据
    if not data or not data.get("username") or not data.get("password"):
        return api_response(message="用户名和密码不能为空", code=400)

    # 检查用户名是否已存在
    if User.query.filter_by(username=data["username"]).first():
        return api_response(message="用户名已存在", code=400)

    # 创建新用户
    user = User(username=data["username"])
    user.set_password(data["password"])

    try:
        db.session.add(user)
        db.session.commit()
        return api_response(data=user.to_dict(), message="注册成功")
    except Exception as e:
        db.session.rollback()
        return api_response(message="注册失败", code=500, errors=str(e))


@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # 验证请求数据
    if not data or not data.get("username") or not data.get("password"):
        return api_response(message="用户名和密码不能为空", code=400)

    # 查找用户
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return api_response(message="用户名或密码错误", code=401)

    try:
        session["user_id"] = user.id  # 在会话中设置用户ID
        session.permanent = True  # 设置会话为永久会话
        db.session.commit()
        return api_response(data=user.to_dict(), message="登录成功")
    except Exception as e:
        db.session.rollback()
        return api_response(message="登录失败", code=500, errors=str(e))


@api_bp.route("/custom-ddl", methods=["POST"])
def add_custom_ddl():
    """添加自定义DDL"""
    try:
        data: dict = request.get_json()
        if not data or not data.get("content"):
            return api_response(message="DDL内容不能为空", code=400)

        user_obj = User.query.get(session.get("user_id"))
        if not user_obj:
            return api_response(message="请先登录", code=401)
            
        current_user: User = cast(User, user_obj)
        # 检查是否有日期参数
        date_str = data.get("date")
        current_user.add_custom_ddl(data["content"], date_str)
        db.session.commit()

        # 重新加载用户数据以确保会话中的custom_ddls是最新的
        db.session.expunge(current_user)  # 分离对象
        user_obj = User.query.get(session.get("user_id"))  # 重新查询
        if user_obj:
            current_user = cast(User, user_obj)
            return api_response(data=current_user.to_dict(), message="添加自定义DDL成功")
        return api_response(message="获取更新后的用户数据失败", code=500)
    except Exception as e:
        db.session.rollback()
        return api_response(message="添加自定义DDL失败", code=500, errors=str(e))


@api_bp.route("/custom-ddl/<int:index>", methods=["DELETE"])
def remove_custom_ddl(index):
    """删除自定义DDL"""
    try:
        current_user = User.query.get(session.get("user_id"))
        if not current_user:
            return api_response(message="请先登录", code=401)

        current_user.remove_custom_ddl(index)
        db.session.commit()

        # 重新加载用户数据以确保会话中的custom_ddls是最新的
        db.session.expunge(current_user)  # 分离对象
        current_user = User.query.get(session.get("user_id"))  # 重新查询

        return api_response(data=current_user.to_dict(), message="删除自定义DDL成功")
    except Exception as e:
        db.session.rollback()
        return api_response(message="删除自定义DDL失败", code=500, errors=str(e))


@api_bp.route("/unsubscribed-accounts", methods=["PUT"])
def update_unsubscribed_accounts():
    """更新用户不想看的公众号列表"""
    try:
        data = request.get_json()
        if not data or not isinstance(data.get("accounts"), list):
            return api_response(message="公众号列表格式错误", code=400)

        current_user = User.query.get(session.get("user_id"))
        if not current_user:
            return api_response(message="请先登录", code=401)

        current_user.update_unsubscribed_accounts(data["accounts"])
        db.session.commit()

        return api_response(data=current_user.to_dict(), message="更新订阅公众号成功")
    except ValueError as e:
        return api_response(message=str(e), code=400)
    except Exception as e:
        db.session.rollback()
        return api_response(message="更新订阅公众号失败", code=500, errors=str(e))


@api_bp.route("/date-query", methods=["GET"])
def query_by_date():
    """根据日期获取新闻和DDL事件"""
    try:
        # 从请求参数中获取日期
        date_str = request.args.get("date")
        if not date_str:
            return api_response(message="日期参数不能为空", code=400)

        # 调用日期查询服务
        result_data = generate_date_data(date_str)

        # 检查是否有错误
        if "error" in result_data:
            return api_response(result_data, message=result_data["error"], code=400)

        return api_response(result_data, message="查询成功")
    except Exception as e:
        print(f"日期查询失败: {str(e)}")
        return api_response(message="日期查询失败，请稍后重试", code=500)


@api_bp.route("/knowledge/query", methods=["POST"])
def knowledge_query():
    """知识库问答"""
    data = request.get_json()
    
    if not data or not data.get("question"):
        return api_response(message="问题不能为空", code=400)
    
    question = data.get("question")
    model = data.get("model", "RAG")  # 默认使用RAG模型
    
    try:
        result = query_by_question(question, model)
        # 如果返回结果包含错误信息
        if "code" in result and result["code"] != HTTPStatus.OK:
            return api_response(result, message=result["message"], code=result["code"])
            # 这里直接返回queryId，不等待处理完成
        return api_response(data=result)
    except Exception as e:
        print(f"知识查询失败: {str(e)}")
        return api_response(message="知识查询失败，请稍后重试", code=500)

@api_bp.route("/query-progress/<query_id>", methods=["GET"])
def query_progress(query_id):
    """获取查询进度"""
    progress_info = get_query_progress(query_id)
    return jsonify({
        "code": 200,
        "data": progress_info,
        "message": "Success"
    })

@api_bp.route("/check-login", methods=["GET"])
def check_login():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        if user:
            return api_response(data=user.to_dict(), message="已登录")
    return api_response(message="未登录", code=401)

@api_bp.route("/logout", methods=["POST"])
def logout():
    try:
        session.clear()  # 清除所有会话数据
        return api_response(message="登出成功")
    except Exception as e:
        return api_response(message="登出失败", code=500, errors=str(e))

@api_bp.route("/docs", methods=["GET"])
def api_docs():
    """返回API文档"""
    from ..settings import MESSAGE_TYPES

    docs = {
        "api_version": "1.0",
        "base_url": "/api",
        "description": "南京大学信息聚合平台API文档",
        "message_types": {
            "description": "系统支持的消息类型",
            "types": list(MESSAGE_TYPES.keys()),
        },
        "response_format": {
            "description": "所有API响应都遵循以下统一格式",
            "schema": {
                "code": "状态码，200表示成功，其他值表示错误",
                "message": "响应消息，用于描述请求结果",
                "data": "响应数据，具体格式参见各接口说明",
                "errors": "错误详情，仅在发生错误时出现",
            },
        },
        "endpoints": [
            {
                "path": "/api/auth/register",
                "method": "POST",
                "description": "用户注册",
                "content_type": "application/json",
                "request_body": {"username": "用户名", "password": "密码"},
                "responses": {
                    "200": {
                        "description": "注册成功",
                        "schema": {
                            "id": "用户ID",
                            "username": "用户名",
                        },
                    },
                    "400": {"description": "请求参数错误或用户名已存在"},
                    "500": {"description": "服务器错误"},
                },
            },
            {
                "path": "/api/auth/login",
                "method": "POST",
                "description": "用户登录",
                "content_type": "application/json",
                "request_body": {"username": "用户名", "password": "密码"},
                "responses": {
                    "200": {
                        "description": "登录成功",
                        "schema": {
                            "id": "用户ID",
                            "username": "用户名",
                        },
                    },
                    "400": {"description": "请求参数错误"},
                    "401": {"description": "用户名或密码错误"},
                    "500": {"description": "服务器错误"},
                },
            },
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
                            "raw_messages": "原始消息数据，包含完整的新闻信息",
                        },
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {"code": 500, "message": "获取新闻失败，请稍后重试"},
                    },
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
                        },
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {
                            "code": 500,
                            "message": "获取DDL事件失败，请稍后重试",
                        },
                    },
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
                        "required": true,
                        "description": "查询日期，格式为YYYY-MM-DD",
                    }
                ],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "date": "查询日期（ISO格式，如：2024-01-20）",
                            "news": "该日期的新闻列表",
                            "ddl_events": "该日期的DDL事件列表",
                        },
                    },
                    "400": {
                        "description": "请求参数错误",
                        "schema": {
                            "code": 400,
                            "message": "日期参数不能为空或日期格式错误",
                        },
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {"code": 500, "message": "日期查询失败，请稍后重试"},
                    },
                },
            },
            {
                "path": "/api/knowledge/query",
                "method": "POST",
                "description": "知识库问答接口",
                "content_type": "application/json",
                "request_body": {"type": "raw", "format": "JSON"},
                "parameters": [
                    {
                        "name": "question",
                        "type": "string",
                        "required": true,
                        "description": "用户的问题",
                    },
                    {
                        "name": "model",
                        "type": "string",
                        "required": false,
                        "description": "查询模型类型，可选值：RAG（默认）、MCP",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {"recommendation": "模型返回的回答内容"},
                    },
                    "400": {
                        "description": "请求参数错误",
                        "schema": {
                            "code": 400,
                            "message": "问题不能为空或不支持的查询模型类型",
                        },
                    },
                    "500": {
                        "description": "服务器错误",
                        "schema": {"code": 500, "message": "知识查询失败，请稍后重试"},
                    },
                },
            },
        ],
    }
    return api_response(docs)
