# News and events services
import datetime
import json
import openai
from ..config.settings import MESSAGE_TYPES
from ..services.query_service import query_messages

def generate_daily_news():
    """Get today's updated content from database and generate daily news summary"""
    # Get today's date
    today = datetime.date.today()
    year, month, day = today.year, today.month, today.day
    
    # Build query conditions - query all message types for today
    query_conditions = {
        "tags": {
            "time": {
                "year": year,
                "month": month,
                "day": day
            }
        }
    }
    
    # Collect today's updates for all message types
    all_messages = []
    for message_type in MESSAGE_TYPES.keys():
        messages = query_messages(message_type, query_conditions)
        if messages:
            all_messages.extend(messages)
    
    # If no updates today, return default message
    if not all_messages:
        return {
            'date': today.isoformat(),
            'content': "今日暂无更新",
            'format': 'text'
        }
    
    # Prepare content for AI summary - group by message type
    content_for_ai = {}
    for message in all_messages:
        message_type = message.get("message_type")
        if message_type not in content_for_ai:
            content_for_ai[message_type] = []
        content_for_ai[message_type].append(message)
    
    # Call AI to generate summary
    prompt = f"请根据以下今日({today.isoformat()})更新的内容，生成一个简洁的每日消息摘要，以JSON格式返回，包含标题和内容：\n{json.dumps(content_for_ai, ensure_ascii=False)}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        # Parse AI returned JSON
        ai_summary = json.loads(response.choices[0].message['content'])
        return {
            'date': today.isoformat(),
            'content': ai_summary,
            'format': 'json'
        }
    except:
        # If parsing fails, return AI's text directly
        return {
            'date': today.isoformat(),
            'content': response.choices[0].message['content'],
            'format': 'text'
        }

def generate_ddl_events():
    """Get all messages from database and generate DDL event list"""
    # Get today's date
    today = datetime.date.today()
    
    # Collect data from all message types
    all_messages = []
    for message_type in MESSAGE_TYPES.keys():
        # No time limit here, get all messages
        # May need time range limits in real application
        messages = query_messages(message_type)
        if messages:
            all_messages.extend(messages)
    
    # If no messages, return empty list
    if not all_messages:
        return []
    
    # Prepare content for AI
    content_for_ai = {
        'messages': all_messages,
        'today': today.isoformat()
    }
    
    # Call AI to extract DDL events
    prompt = f"请从以下消息中提取所有截止日期(DDL)事件，以JSON数组格式返回，每个事件包含名称和截止日期：\n{json.dumps(content_for_ai, ensure_ascii=False)}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        # Parse AI returned JSON
        ddl_events = json.loads(response.choices[0].message['content'])
        return ddl_events
    except:
        # If parsing fails, return empty list
        return []