# DDL事件服务
import datetime
import json
import openai
from ..settings import MESSAGE_TYPES
from ..services.query_service import query_messages

def generate_ddl_events():
    """从数据库获取今日发布的消息并生成截止日期事件列表"""
    # 获取今天的日期
    today = datetime.date.today()
    
    # 收集所有类型的数据
    all_messages = []
    for message_type in MESSAGE_TYPES.keys():
        # 只获取今日发布的消息
        messages = query_messages(message_type, {"发布日期": today.isoformat()})
        if messages:
            all_messages.extend(messages)
    
    # 如果没有消息，返回默认结果
    if not all_messages:
        return {
            'date': today.isoformat(),
            'summary': [],
            'raw_messages': []
        }
    
    # 调用AI提取截止日期事件
    prompt = f"请从以下消息中提取所有截止日期(DDL)事件，生成一个JSON格式的今日DDL总结，要求：\n1. 每个事件必须包含'事件名称'、'截止日期'、'重要程度'（高、中、低）字段\n2. 按截止日期升序排序\n3. 注意保持JSON格式的正确性\n\n原始消息：\n{json.dumps(all_messages, ensure_ascii=False)}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        # 解析AI返回的JSON
        ai_summary = json.loads(response.choices[0].message['content'])
        return {
            'date': today.isoformat(),
            'summary': ai_summary,
            'raw_messages': all_messages
        }
    except:
        # 如果解析失败，返回空结果但保留原始数据
        return {
            'date': today.isoformat(),
            'summary': [],
            'raw_messages': all_messages
        }