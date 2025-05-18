# 数据库交互查询服务
import json
from ..models.db import db
from ..config.settings import MESSAGE_TYPES

def query_messages(message_type, query_conditions=None):
    """通用消息查询函数
    
    参数：
        message_type: 消息类型（如"通知"、"规章制度"等）
        query_conditions: 查询条件字典，包含标签和内容部分
        
    返回：
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
                print(f"处理消息{msg.id}时出错：{e}")
                continue
        
        return messages_data
    except Exception as e:
        print(f"数据库查询错误：{e}")
        return []

def _flatten_json_conditions(conditions, parent_path=''):
    """将嵌套的JSON查询条件展平为路径-值对
    
    参数：
        conditions: 嵌套的查询条件字典
        parent_path: 父路径前缀
        
    返回：
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

def query_by_question(question, extracted_tags):
    """基于用户问题查询相关信息
    
    参数：
        question: 用户问题
        extracted_tags: AI提取的标签
        
    返回：
        查询结果列表
    """
    # TODO: 实现基于提取标签的智能查询
    # 1. 分析提取的标签以确定消息类型
    # 2. 构建查询条件
    # 3. 调用query_messages函数执行查询
    
    # 示例实现（需要根据实际需求调整）
    results = []
    
    # 尝试查询所有消息类型
    for message_type in MESSAGE_TYPES.keys():
        # 构建查询条件 - 需要从AI标签进行智能映射
        query_conditions = {"tags": {}, "content": {}}
        
        # TODO: 根据extracted_tags填充query_conditions
        # 简单示例，实际实现需要更复杂的逻辑
        for tag in extracted_tags:
            # 假设tag是包含key和value的字典
            if isinstance(tag, dict) and "key" in tag and "value" in tag:
                # 检查标签是否属于当前消息类型的标签模式
                if tag["key"] in MESSAGE_TYPES[message_type]["tags_schema"]:
                    query_conditions["tags"][tag["key"]] = tag["value"]
                elif tag["key"] in MESSAGE_TYPES[message_type]["content_schema"]:
                    query_conditions["content"][tag["key"]] = tag["value"]
        
        # 如果存在条件则执行查询
        if query_conditions["tags"] or query_conditions["content"]:
            message_results = query_messages(message_type, query_conditions)
            results.extend(message_results)
    
    return results