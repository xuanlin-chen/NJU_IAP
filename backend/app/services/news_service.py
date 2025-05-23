# 新闻服务
import datetime
import json
import re
from app.settings import MESSAGE_TYPES
from sqlalchemy import text
from app.db import db

# API配置
# API_KEY = "sk-*****************************************"
# API_URL = "https://api.siliconflow.cn/v1/chat/completions"
# SLEEP_TIME = 7  # API调用间隔时间

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

def generate_daily_news():# -> dict[str, Any] | list[dict[str, Any]]:
    """从数据库获取2025年5月20日的所有消息并返回格式化的新闻摘要"""
    target_date = datetime.date(2025, 5, 20)
    
    # 收集所有类型的更新
    all_messages = []
    # 创建应用上下文
    
        # 遍历所有消息类型
    for message_type, config in MESSAGE_TYPES.items():
        table_name = config["table_name"]
        # 构建查询SQL，直接查询所需字段
        query = text(f"SELECT 类型, 标题, 关键词, 原文信息, 原文链接 FROM {table_name} WHERE 发布日期 = :target_date")
        try:
        # 执行查询
            result = db.session.execute(query, {"target_date": target_date})
            rows = result.fetchall()
    
    # 处理查询结果
            for row in rows:
                message = {
                    "类型": row[0],
                    "标题": row[1],
                    "关键词": row[2],
                    "原文信息": row[3],
                    "原文链接": row[4]
                }
                all_messages.append(message)
        except Exception as e:
            # print(f"查询{message_type}失败")
            continue
    
    # 如果没有数据，返回默认消息
    if not all_messages:
        return {
            'date': target_date.isoformat(),
            'summary': [],
            'abstract': []
        }
    
    # 格式化消息内容
    summary = [{
        '类型': msg['类型'],
        '标题': msg['标题'],
        '关键词': msg['关键词'],
        '原文链接': msg['原文链接']
    } for msg in all_messages]
    
    abstract = [msg['原文信息'] for msg in all_messages]
    
    # 为每条消息生成独立JSON对象
    news_list = [{
        'date': target_date.isoformat(),
        'summary': item,
        'abstract': abstract[i]
    } for i, item in enumerate(summary)]

    return news_list