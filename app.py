# ---------- 第一部分：基础配置 ----------
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 添加CORS支持
import openai
import json
import datetime


app = Flask(__name__)
# 启用CORS，支持跨域请求
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://crawler:*********@47.122.71.85:3306/information_for_students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# OpenAI配置（需替换为您的API密钥）
openai.api_key = "your-openai-key"

db = SQLAlchemy(app)

# ---------- 第二部分：数据库映射 ----------
# 数据表映射配置 - 灵活结构
# 每种消息类型都有两个部分：标签(tags)和内容(content)
# 标签用于检索和分类，内容是实际的消息数据
MESSAGE_TYPES = {
    # 示例消息类型配置
    "通知": {
        "table_name": "notifications",
        "tags_schema": {
            # 标签部分的JSON结构定义
        },
        "content_schema": {
            # 内容部分的JSON结构定义
        }
    },
    "规章制度": {
        "table_name": "regulations",
        "tags_schema": {
            # 标签部分的JSON结构定义
        },
        "content_schema": {
            # 内容部分的JSON结构定义
        }
    }
    # 可以根据需要添加更多消息类型
}

# ---------- 第三部分：数据库查询函数 ----------
# 通用查询函数 - 根据消息类型和查询条件查询数据
def query_messages(message_type, query_conditions=None):
    """通用消息查询函数
    
    Args:
        message_type: 消息类型（如"通知"、"规章制度"等）
        query_conditions: 查询条件字典，包含tags和content两部分的查询条件
        
    Returns:
        查询结果列表
    """
    if message_type not in MESSAGE_TYPES:
        return []
    
    table_name = MESSAGE_TYPES[message_type]["table_name"]
    query_conditions = query_conditions or {}
    
    # 构建基础SQL查询
    query = f"SELECT id, tags_json, content_json FROM {table_name} WHERE 1=1"
    params = []
    
    # 处理标签查询条件
    if "tags" in query_conditions:
        for path, value in _flatten_json_conditions(query_conditions["tags"]):
            query += f" AND JSON_EXTRACT(tags_json, '$.{path}') = %s"
            params.append(str(value))
    
    # 处理内容查询条件
    if "content" in query_conditions:
        for path, value in _flatten_json_conditions(query_conditions["content"]):
            query += f" AND JSON_EXTRACT(content_json, '$.{path}') = %s"
            params.append(str(value))
    
    try:
        # 使用SQLAlchemy执行查询
        result = db.session.execute(query, params)
        messages = result.fetchall()
        
        # 格式化结果
        messages_data = []
        for msg in messages:
            try:
                # 解析JSON字段
                tags = json.loads(msg.tags_json) if msg.tags_json else {}
                content = json.loads(msg.content_json) if msg.content_json else {}
                
                message_data = {
                    'id': msg.id,
                    'tags': tags,
                    'content': content,
                    'message_type': message_type
                }
                messages_data.append(message_data)
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"Error processing message {msg.id}: {e}")
                continue
        
        return messages_data
    except Exception as e:
        print(f"Database query error: {e}")
        return []

def _flatten_json_conditions(conditions, parent_path=''):
    """将嵌套的JSON查询条件展平为路径-值对
    
    Args:
        conditions: 嵌套的查询条件字典
        parent_path: 父路径前缀
        
    Returns:
        展平后的路径-值对列表
    """
    flattened = []
    for key, value in conditions.items():
        current_path = f"{parent_path}.{key}" if parent_path else key
        
        if isinstance(value, dict):
            # 递归处理嵌套字典
            flattened.extend(_flatten_json_conditions(value, current_path))
        else:
            flattened.append((current_path, value))
    
    return flattened



# 统一查询函数 - 根据用户问题查询相关信息
def query_by_question(question):
    """根据用户问题查询相关信息
    
    Args:
        question: 用户问题
        
    Returns:
        查询结果列表
    """
    # 使用AI提取查询标签
    extracted_tags = extract_tags_with_ai(question)
    
    # TODO: 实现基于提取标签的智能查询
    # 1. 分析提取的标签，确定查询的消息类型
    # 2. 构建查询条件
    # 3. 调用query_messages函数执行查询
    
    # 示例实现（需要根据实际情况调整）
    results = []
    
    # 尝试从所有消息类型中查询
    for message_type in MESSAGE_TYPES.keys():
        # 构建查询条件 - 这里需要根据AI提取的标签进行智能映射
        query_conditions = {"tags": {}, "content": {}}
        
        # TODO: 根据extracted_tags填充query_conditions
        # 这里只是一个简单示例，实际实现需要更复杂的逻辑
        for tag in extracted_tags:
            # 假设tag是一个包含key和value的字典
            if isinstance(tag, dict) and "key" in tag and "value" in tag:
                # 检查这个标签是否属于当前消息类型的标签模式
                if tag["key"] in MESSAGE_TYPES[message_type]["tags_schema"]:
                    query_conditions["tags"][tag["key"]] = tag["value"]
                elif tag["key"] in MESSAGE_TYPES[message_type]["content_schema"]:
                    query_conditions["content"][tag["key"]] = tag["value"]
        
        # 如果有查询条件，则执行查询
        if query_conditions["tags"] or query_conditions["content"]:
            message_results = query_messages(message_type, query_conditions)
            results.extend(message_results)
    
    return results

# ---------- 第四部分：AI处理函数 ----------
def extract_tags_with_ai(question):
    """使用AI提取查询标签"""
    prompt = f"请从以下问题中提取关键词和实体，以JSON数组格式返回，每个元素应包含'key'和'value'字段，例如[{{'key':'type', 'value':'会议通知'}}]：{question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        # 解析AI返回的JSON
        extracted_tags = json.loads(response.choices[0].message['content'])
        
        # 验证格式是否正确
        validated_tags = []
        for tag in extracted_tags:
            if isinstance(tag, dict) and 'key' in tag and 'value' in tag:
                validated_tags.append(tag)
            elif isinstance(tag, str):
                # 兼容旧格式，将字符串转换为key-value格式
                validated_tags.append({'key': 'keyword', 'value': tag})
        
        return validated_tags
    except:
        return []

def generate_answer_with_ai(question, results):
    """使用AI生成最终回答"""
    # 格式化结果数据，使其更易于AI理解
    formatted_results = []
    for res in results:
        # 提取标签和内容
        tags = res.get('tags', {})
        content = res.get('content', {})
        message_type = res.get('message_type', '未知类型')
        
        # 格式化时间信息
        time_info = ""
        if 'time' in tags and isinstance(tags['time'], dict):
            time = tags['time']
            if all(k in time for k in ['year', 'month', 'day']):
                time_info = f"{time.get('year', 0)}-{time.get('month', 0):02d}-{time.get('day', 0):02d}"
        
        # 构建格式化的结果
        formatted_result = {
            'id': res.get('id'),
            'type': message_type,
            'time': time_info,
            'tags': {k: v for k, v in tags.items() if k != 'time'},  # 排除time字段，因为已单独处理
            'content': content
        }
        formatted_results.append(formatted_result)
    
    # 将格式化的结果转换为JSON字符串
    context = json.dumps(formatted_results, ensure_ascii=False, indent=2)
    
    # 构建提示词
    prompt = f"根据以下数据回答问题：{question}\n\n数据：\n{context}\n\n请提供详细、准确的回答，并引用相关信息来源。"
    
    # 调用AI生成回答
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message['content']

# 生成每日消息摘要
def generate_daily_news():
    """从数据库获取今日更新的内容，并生成每日消息摘要"""
    # 获取今天的日期
    today = datetime.date.today()
    year, month, day = today.year, today.month, today.day
    
    # 构建查询条件 - 查询今日的所有消息类型
    query_conditions = {
        "tags": {
            "time": {
                "year": year,
                "month": month,
                "day": day
            }
        }
    }
    
    # 收集所有消息类型的今日更新
    all_messages = []
    for message_type in MESSAGE_TYPES.keys():
        messages = query_messages(message_type, query_conditions)
        if messages:
            all_messages.extend(messages)
    
    # 如果没有今日更新，返回默认消息
    if not all_messages:
        return {
            'date': today.isoformat(),
            'content': "今日暂无更新",
            'format': 'text'
        }
    
    # 准备AI摘要的内容 - 按消息类型分组
    content_for_ai = {}
    for message in all_messages:
        message_type = message.get("message_type")
        if message_type not in content_for_ai:
            content_for_ai[message_type] = []
        content_for_ai[message_type].append(message)
    
    # 调用AI生成摘要
    prompt = f"请根据以下今日({today.isoformat()})更新的内容，生成一个简洁的每日消息摘要，以JSON格式返回，包含标题和内容：\n{json.dumps(content_for_ai, ensure_ascii=False)}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        # 解析AI返回的JSON
        ai_summary = json.loads(response.choices[0].message['content'])
        return {
            'date': today.isoformat(),
            'content': ai_summary,
            'format': 'json'
        }
    except:
        # 如果解析失败，直接返回AI的文本
        return {
            'date': today.isoformat(),
            'content': response.choices[0].message['content'],
            'format': 'text'
        }

# 生成DDL事件列表
def generate_ddl_events():
    """从数据库获取所有消息，并生成DDL事件列表"""
    # 获取今天的日期
    today = datetime.date.today()
    
    # 收集所有消息类型的数据
    all_messages = []
    for message_type in MESSAGE_TYPES.keys():
        # 这里不设置时间限制，获取所有消息
        # 实际应用中可能需要添加时间范围限制
        messages = query_messages(message_type)
        if messages:
            all_messages.extend(messages)
    
    # 如果没有消息，返回空列表
    if not all_messages:
        return []
    
    # 准备AI处理的内容
    content_for_ai = {
        'messages': all_messages,
        'today': today.isoformat()
    }
    
    # 调用AI提取DDL事件
    prompt = f"请从以下消息中提取所有截止日期(DDL)事件，以JSON数组格式返回，每个事件包含名称和截止日期：\n{json.dumps(content_for_ai, ensure_ascii=False)}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        # 解析AI返回的JSON
        ddl_events = json.loads(response.choices[0].message['content'])
        return ddl_events
    except:
        # 如果解析失败，返回空列表
        return []

# ---------- 第五部分：API路由 ----------
# 统一的API响应格式
def api_response(data=None, message="success", code=200, errors=None):
    response = {
        "code": code,
        "message": message,
        "data": data
    }
    if errors:
        response["errors"] = errors
    return jsonify(response)

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """直接查询消息（高级用户使用）"""
    try:
        # 获取查询参数
        message_type = request.args.get('message_type')
        query_conditions_str = request.args.get('query_conditions', '{}')
        
        # 验证消息类型
        if not message_type or message_type not in MESSAGE_TYPES:
            return api_response(message="无效的消息类型", code=400)
        
        # 解析查询条件
        try:
            query_conditions = json.loads(query_conditions_str)
        except json.JSONDecodeError:
            return api_response(message="查询条件格式错误，必须是有效的JSON", code=400)
        
        # 执行查询
        results = query_messages(message_type, query_conditions)
        
        return api_response(results)
    except Exception as e:
        return api_response(message=str(e), code=500)

@app.route('/api/news/today', methods=['GET'])
def get_today_news():
    """获取当日消息摘要"""
    try:
        # 调用生成每日消息的函数
        news_data = generate_daily_news()
        return api_response(news_data)
    except Exception as e:
        return api_response(message=str(e), code=500)

@app.route('/api/ddl-events', methods=['GET'])
def get_ddl_events():
    """获取近期重要事件DDL列表"""
    try:
        # 调用生成DDL事件的函数
        events_data = generate_ddl_events()
        return api_response(events_data)
    except Exception as e:
        return api_response(message=str(e), code=500)

@app.route('/api/knowledge/query', methods=['POST'])
def ask_question():
    """处理用户提问的完整流程"""
    try:
        # 获取用户问题
        data = request.get_json()
        if not data or 'question' not in data:
            return api_response(message="问题不能为空", code=400)
            
        question = data.get('question', '')
        
        # 使用AI提取查询标签
        extracted_tags = extract_tags_with_ai(question)
        
        # 查询相关信息 - 使用新的灵活查询函数
        results = query_by_question(question)
        
        # 生成回答
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

# ---------- 添加API文档路由 ----------
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """返回API文档"""
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
                "description": "获取当日消息摘要",
                "parameters": [],
                "responses": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "date": "日期 (ISO格式)",
                            "content": "消息内容（可能是文本或JSON）",
                            "format": "内容格式（text或json）"
                        }
                    }
                }
            },
            {
                "path": "/api/ddl-events",
                "method": "GET",
                "description": "获取近期重要事件DDL列表",
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
                            "answer": "AI生成的回答",
                            "references": "参考资料，包含消息类型、标签摘要和内容预览"
                        }
                    }
                }
            },
            {
                "path": "/api/messages",
                "method": "GET",
                "description": "直接查询消息（高级用户使用）",
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
                        "description": "查询条件，JSON格式，包含tags和content两部分"
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

# ---------- 启动应用 ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)