# 日期查询服务
import datetime
import json
import re
from app.settings import MESSAGE_TYPES
from sqlalchemy import text
from app.db import db
from .news_service import generate_daily_news
from .ddl_service import generate_ddl_events
from ..models.user import User
from flask import session
import pendulum

def generate_date_data(target_date_str):
    """
    根据指定日期生成新闻和DDL事件数据
    
    参数:
        target_date_str: 日期字符串，格式为'YYYY-MM-DD'
        
    返回:
        包含新闻和DDL事件的字典
    """
    # example of result_data:
    # {
    #     'date': '2025-05-20',
    #     'news': [
    #         {
    #             'date': '2025-05-20',
    #             'summary': {
    #                 '类型': '学术讲座',
    #                 '标题': '人工智能与未来教育发展论坛',
    #                 '关键词': 'AI, 教育创新, 未来发展',
    #                 '原文链接': 'https://www.nju.edu.cn/events/ai-forum-2025'
    #             },
    #             'abstract': '南京大学人工智能学院将于2025年5月20日举办"人工智能与未来教育发展论坛"...'
    #         }
    #     ],
    #     'ddl_events': [
    #         {
    #             'date': '2025-05-20',
    #             'summary': {
    #                 '类型': '讲座/分享会信息',
    #                 '标题': '2025春季校园招聘宣讲会',
    #                 '截止时间': '2025-05-25 18:00:00',
    #                 '原文链接': 'https://www.nju.edu.cn/events/career-talk-2025'
    #             }
    #         }
    #     ]
    # }
    try:
        # 解析日期字符串
        target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
        
        # 获取用户自定义DDL
        user_ddls = []
        user_id = session.get("user_id")
        print(f"[DEBUG] User ID from session: {user_id}") # 添加调试日志
        if user_id:
            user = User.query.get(user_id)
            if user and user.custom_ddls:
                for ddl in user.custom_ddls:
                    ddl_date = datetime.datetime.strptime(ddl['date'].split('T')[0], '%Y-%m-%d').date()
                    # 检查DDL日期是否在target_date及其后5天内
                    if target_date <= ddl_date <= target_date + datetime.timedelta(days=5):
                        # 将前端传入的日期时间字符串 'YYYY-MM-DDTHH:MM:SS' 转换为 'YYYY-MM-DD HH:MM:SS'
                        formatted_ddl_time = ddl['date'].replace('T', ' ')
                        user_ddls.append({
                            'date': ddl['date'].split('T')[0],
                            'summary': {
                                '类型': '用户自定义',
                                '标题': ddl['content'],
                                '截止时间': formatted_ddl_time # 使用转换后的日期时间字符串
                            }
                        })

        # 修改news_service和ddl_service中的函数调用，传入目标日期
        news_data = generate_news_by_date(target_date)
        
        # 获取未来5天的DDL事件
        ddl_data = []
        for i in range(6): # 包括目标日期和之后5天
            current_date = target_date + datetime.timedelta(days=i)
            ddl_data.extend(generate_ddl_by_date(current_date))

        # 将用户自定义DDL放在ddl_events的开头
        ddl_data = user_ddls + ddl_data

        # 构建返回数据
        return {
            'date': target_date.isoformat(),
            'news': news_data,
            'ddl_events': ddl_data
        }
    except ValueError:
        # 日期格式错误
        return {
            'date': target_date_str,
            'news': [],
            'ddl_events': [],
            'error': '日期格式错误，请使用YYYY-MM-DD格式'
        }
    except Exception as e:
        # 其他错误
        return {
            'date': target_date_str,
            'news': [],
            'ddl_events': [],
            'error': f'查询失败: {str(e)}'
        }

def generate_news_by_date(target_date):
    """
    根据指定日期生成新闻数据
    
    参数:
        target_date: datetime.date对象
        
    返回:
        新闻数据列表
    """
    # 收集所有类型的更新
    all_messages = []
    
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
    
    # 如果没有数据，返回空列表
    if not all_messages:
        return []
    
    # 格式化消息内容
    summary = [{
        '类型': msg['类型'],
        '标题': msg['标题'],
        '关键词': msg['关键词'],
        '原文链接': msg['原文链接']
    } for msg in all_messages]
    
    # 提取第一个||之间的内容作为摘要
    abstract = []
    for msg in all_messages:
        content = msg['原文信息']
        # 修改正则表达式以匹配单竖线 |
        match = re.search(r'\|([^|]*)\|', content)
        if match:
            extracted_content=match.group(1)
        else:
            extracted_content=content
        extracted_content = re.sub(r'(\*\*.*?\*\*)(?!\s)', r'\1 ', extracted_content)
        # 移除"核心摘要: "前缀
        if extracted_content.startswith("核心摘要: ##"):
            extracted_content = extracted_content[len("核心摘要: ##"):]
            # 检查并添加星号后的空格
            # extracted_content = re.sub(r'(\*+)(?!\s)', r'\1 ', extracted_content)
        abstract.append(extracted_content)
    
    # 为每条消息生成独立JSON对象
    news_list = [{
        'date': target_date.isoformat(),
        'summary': item,
        'abstract': abstract[i]
    } for i, item in enumerate(summary)]

    return news_list

def generate_ddl_by_date(target_date):
    """
    根据指定日期生成DDL事件数据
    
    参数:
        target_date: datetime.date对象
        
    返回:
        DDL事件数据列表
    """
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

        if table_name not in ddl_fields:
            continue
        fields = ddl_fields[table_name]
        
        query = text(f"""
            SELECT 类型, 标题, 原文信息, 原文链接, {', '.join(fields)} 
            FROM {table_name} 
            WHERE DATE({fields[0]}) = :target_date
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
                
                
                print(f"[DEBUG] 截止时间: {event['截止时间']}") # 添加调试日志
                
                if isinstance(event['截止时间'], datetime.datetime):
                    formatted_deadline = event['截止时间'].strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(event['截止时间'], str):
                    try:
                        # 尝试解析常见的日期时间格式，并转换为UTC时间再格式化
                        dt_obj = pendulum.parse(event['截止时间'])
                        formatted_deadline = dt_obj.in_utc().strftime('%Y-%m-%d %H:%M:%S')
                    except Exception:
                        formatted_deadline = event['截止时间'] # 如果解析失败，保留原始字符串
                else:
                    formatted_deadline = str(event['截止时间'])

                event['截止时间'] = formatted_deadline
                
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