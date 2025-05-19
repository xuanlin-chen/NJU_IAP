# 新闻服务
import datetime
import json
import requests
import time
import re
from ..settings import MESSAGE_TYPES
from ..services.query_service import query_messages

# API配置
API_KEY = "sk-*****************************************"
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
SLEEP_TIME = 7  # API调用间隔时间

def safe_json_parse(raw_str, max_retries=3):
    # 安全解析JSON加自动修复
    for _ in range(max_retries):
        try:
            return json.loads(raw_str)
        except json.JSONDecodeError:
            # 去除代码块包裹
            repaired = re.sub(r'^.*?```(?:json)?\s*({.*?})\s*```.*$', r'\1', raw_str, flags=re.DOTALL)
            # 替换中文引号
            repaired = repaired.replace('"', '\"').replace('"', '\"')
            # 处理尾随逗号
            repaired = re.sub(r',\s*([}\]])', r'\1', repaired)
            try:
                return json.loads(repaired)
            except Exception as e:
                raw_str = repaired
                print(f"尝试修复JSON格式失败: {str(e)}")

    # 若上述手段都不行，暴力提取第一个完整JSON
    match = re.search(r'\{.*\}', raw_str, flags=re.DOTALL)
    if match is None:
        raise ValueError("找不到有效的JSON内容")
    json_str = match.group()
    return json.loads(json_str)

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
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"请根据以下今日({today.isoformat()})发布的内容，生成一个简洁的每日消息总结，以JSON格式返回，要求：\n1. 总结要包含'标题'和'内容'两个字段\n2. 内容要简明扼要地概括所有消息的重点\n3. 注意保持JSON格式的正确性\n\n原始消息：\n{json.dumps(all_messages, ensure_ascii=False)}"

    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 2000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        time.sleep(SLEEP_TIME)
        
        raw_output = response.json()['choices'][0]['message']['content'].strip()
        ai_summary = safe_json_parse(raw_output)
        
        return {
            'date': today.isoformat(),
            'summary': ai_summary,
            'raw_messages': all_messages
        }
    except Exception as e:
        print(f"API调用或解析失败: {str(e)}")
        return {
            'date': today.isoformat(),
            'summary': "今日暂无更新",
            'raw_messages': all_messages
        }