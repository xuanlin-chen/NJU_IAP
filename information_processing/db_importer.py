# 导入数据库的几个函数
import pymysql
from datetime import datetime


def save_to_database(json_data, db_config):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    try:
        table_name = json_data['类型']
        processed = process_item(json_data)
        sql, values = generate_insert_sql(table_name, processed)
        cursor.execute(sql, values)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"数据库错误: {e}")
    finally:
        cursor.close()
        conn.close()

def process_item(item):
    # 处理单个数据项：类型转换和格式化
    processed = {}
    for key, value in item.items():
        # 处理数组类型
        if isinstance(value, list):
            processed[key] = ' '.join(map(str, value)) if value else None
        # 处理布尔类型
        elif isinstance(value, bool):
            processed[key] = int(value)
        # 处理日期时间字段
        elif '时间' in key or '日期' in key or '时间' in key:
            processed[key] = parse_datetime(value)
        else:
            processed[key] = value if value not in ['无', ''] else None
    return processed


def parse_datetime(time_str):
    # 解析时间字符串
    if not time_str or time_str.lower() == '无':
        return None
    try:
        if ':' in time_str:
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        return datetime.strptime(time_str, "%Y-%m-%d")
    except:
        return None


def generate_insert_sql(table_name, data):
    # 生成动态SQL语句
    columns = []
    placeholders = []
    values = []

    for col, val in data.items():
        # 处理包含/的情况
        column = f'`{col}`' if '/' in col else col
        columns.append(column)
        placeholders.append('%s')
        values.append(val)

    columns_str = ', '.join(columns)
    placeholders_str = ', '.join(placeholders)

    sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders_str})"
    return sql, values