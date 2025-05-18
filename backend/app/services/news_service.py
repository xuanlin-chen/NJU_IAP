# 新闻和事件服务
import datetime
import json
import openai
from ..config.settings import MESSAGE_TYPES
from ..services.query_service import query_messages

def generate_daily_news():
    """从数据库获取今日更新内容并生成每日新闻摘要"""
    # 获取今天的日期
    today = datetime.date.today()
    year, month, day = today.year, today.month, today.day
    
    # 构建查询条件 - 查询今天所有类型的消息
    query_conditions = {
        "tags": {
            "time": {
                "year": year,
                "month": month,
                "day": day
            }
        }
    }
    
    # 收集今天所有类型的更新
    all_messages = []
    for message_type in MESSAGE_TYPES.keys():
        messages = query_messages(message_type, query_conditions)
        if messages:
            all_messages.extend(messages)
    
    # 如果今天没有更新，返回默认消息
    if not all_messages:
        return {
            'date': today.isoformat(),
            'content': "今日暂无更新",
            'format': 'text'
        }
    
    # 准备AI摘要内容 - 按消息类型分组
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

def generate_ddl_events():
    """从数据库获取所有消息并生成截止日期事件列表"""
    # 获取今天的日期
    today = datetime.date.today()
    
    # 收集所有类型的数据
    all_messages = []
    for message_type in MESSAGE_TYPES.keys():
        # 这里不限制时间，获取所有消息
        # 在实际应用中可能需要时间范围限制
        messages = query_messages(message_type)
        if messages:
            all_messages.extend(messages)
    
    # 如果没有消息，返回空列表
    if not all_messages:
        return []
    
    # 准备AI内容
    content_for_ai = {
        'messages': all_messages,
        'today': today.isoformat()
    }
    
    # 调用AI提取截止日期事件
    prompt = f"请从以下消息中提取所有截止日期(DDL)事件，以JSON数组格式返回，每个事件包含名称和截止日期：\n{json.dumps(content_for_ai, ensure_ascii=False)}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        # 解析AI返回的JSON
        return json.loads(response.choices[0].message['content'])
    except:
        # 如果解析失败，返回空列表
        return []