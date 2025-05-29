# DDL事件服务
import datetime
import json
import re
from app.settings import MESSAGE_TYPES
from sqlalchemy import text
from app.db import db

# DDL字段映射配置

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

def generate_ddl_events():
    """从数据库获取5月20日发布的消息并提取DDL信息"""
    target_date = datetime.date(2025, 5, 20)
    ddl_events = []
    
    
    for message_type, config in MESSAGE_TYPES.items():
        table_name = config["table_name"]
        
        # 根据表结构设计不同查询字段
        ddl_fields = {
            '校园通知': ['截止时间'],
            '讲座或分享会信息': ['报名截止时间'],
            '社团消息': ['活动时间'],
            '实践培训活动': ['报名截止时间'],
            '作品征集': ['提交截止时间'],
            '其他活动': ['报名截止时间'],
            '其他类型': ['行动截止时间'],
            '比赛通知': ['报名截止时间'],
            '学业申请': ['申请截止时间'],
            '国际交流项目': ['项目时间_申请截止时间'],
            '志愿活动': ['报名截止时间'],
            '社会实践': ['报名截止时间'],
            '文体活动': ['报名截止时间'],
            '实习就业': ['申请截止日期']
        }

        if table_name not in ddl_fields :
            continue
        fields = ddl_fields[table_name]
        
        query = text(f"""
            SELECT 类型, 标题, 原文信息, 原文链接, {', '.join(fields)} 
            FROM {table_name} 
            WHERE 发布日期 = :target_date
            AND ({' OR '.join([f'{f} IS NOT NULL' for f in fields])})
        """)
        
        try:
            result = db.session.execute(query, {"target_date": target_date})
            for row in result:
                event = {
                    '类型': row[0],
                    '标题': row[1],
                    '原文信息': row[2],
                    '原文链接': row[3],
                    '截止时间': row[4]
                }
                ddl_events.append(event)
        except Exception as e:
                # print(f"查询{message_type}失败")
                continue

    # 构建符合要求的JSON列表
    formatted_events = [{
        'date': target_date.isoformat(),
        'summary': {
            '类型': event['类型'],
            '标题': event['标题'],
            '截止时间': event['截止时间'],
            '原文链接': event['原文链接']
        },
        # 'abstract': event['原文信息']
    } for event in ddl_events]

    return formatted_events