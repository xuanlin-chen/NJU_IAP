import pymysql
from pymysql import Error
from crawler.crawlers.wechat.crawler import main
import json

# 导入数据库配置
from database_configuration import connection as db_connection


# 表名映射
TABLE_MAPPING = {
    "比赛通知": "比赛通知",
    "学习资源": "学习资源",
    "校园通知": "校园通知",
    "学业申请": "学业申请",
    "学业相关政策": "学业相关政策",
    "奖励_资助政策": "奖励_资助政策",
    "惩罚制度": "惩罚制度",
    "校园安全": "校园安全",
    "讲座_分享会信息": "讲座_分享会信息",
    "志愿活动": "志愿活动",
    "国际交流项目": "国际交流项目",
    "社团消息": "社团消息",
    "文体活动": "文体活动",
    "实践培训活动": "实践培训活动",
    "作品征集": "作品征集",
    "其他活动": "其他活动",
    "实习就业": "实习就业",
    "其他类型": "其他类型"
}

def connect_to_database():
    """连接数据库"""
    try:
        return db_connection
    except Error as e:
        print(f"数据库连接失败: {e}")
        return None

def insert_data(connection, table_name, data):
    """将数据插入到指定表中"""
    try:
        with connection.cursor() as cursor:
            # 动态生成SQL语句
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
        connection.commit()
        print(f"成功插入数据到{table_name}表")
    except Error as e:
        print(f"插入数据到{table_name}表失败: {e}")
        connection.rollback()

def process_and_import():
    """处理爬虫数据并导入数据库"""
    # 获取爬虫数据
    results = main()
    
    # 连接数据库
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        for data in results:
            if not data or 'type' not in data:
                continue
                
            # 根据类型获取表名
            data_type = data['type']
            table_name = TABLE_MAPPING.get(data_type)
            
            if not table_name:
                print(f"未知类型: {data_type}")
                continue
                
            # 插入数据
            insert_data(connection, table_name, data)
    finally:
        connection.close()

if __name__ == "__main__":
    process_and_import()