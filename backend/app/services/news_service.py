# 新闻服务
import datetime
import json
import openai
from ..settings import MESSAGE_TYPES
from ..services.query_service import query_messages

def generate_daily_news():
    """从数据库获取今日更新内容并生成每日新闻摘要"""
    # 获取今天的日期
    today = datetime.date.today()
    
    # 构建查询条件 - 查询今天发布的消息
    query_conditions = {
        "发布日期": today.isoformat()
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
            'summary': "今日暂无更新",
            'raw_messages': []
        }
    
    # 调用AI生成摘要
    prompt = f"请根据以下今日({today.isoformat()})发布的内容，生成一个简洁的每日消息总结，以JSON格式返回，要求：\n1. 总结要包含'标题'和'内容'两个字段\n2. 内容要简明扼要地概括所有消息的重点\n3. 注意保持JSON格式的正确性\n\n原始消息：\n{json.dumps(all_messages, ensure_ascii=False)}"
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content
    if not content:
        return {
            'date': today.isoformat(),
            'summary': "今日暂无更新",
            'raw_messages': []
        }
    try:
        # 解析AI返回的JSON
        ai_summary = json.loads(content)
        return {
            'date': today.isoformat(),
            'summary': ai_summary,
            'raw_messages': all_messages
        }
    except:
        # 如果解析失败，直接返回AI的文本
        return {
            'date': today.isoformat(),
            'summary': content,
            'raw_messages': all_messages
        }