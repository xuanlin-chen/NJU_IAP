
from flask import app
from app.db import engine
from app.app import create_app
from sqlalchemy import text



def test_database_connection():
    try:
            conn = engine.connect()
            print("数据库连接成功！")
            
            # 关闭连接
            conn.close()
            print("数据库连接已正常关闭")
            return True
    except Exception as e:
        print(f"数据库连接测试失败：{str(e)}")
        return False

def test_fetch_data():
    try:
            # 连接数据库
            with engine.connect() as conn:
                # 测试查询比赛通知表
                result = conn.execute(text("SELECT 标题, 比赛名称, 发布日期 FROM 比赛通知 LIMIT 5"))
                print("\n比赛通知数据：")
                for row in result:
                    print(f"标题: {row[0]}, 比赛名称: {row[1]}, 发布日期: {row[2]}")
                
                # 测试查询学习资源表
                result = conn.execute(text("SELECT 标题, 资源类型, 发布日期 FROM 学习资源 LIMIT 5"))
                print("\n学习资源数据：")
                for row in result:
                    print(f"标题: {row[0]}, 资源类型: {row[1]}, 发布日期: {row[2]}")
                
                print("\n数据获取测试成功！")
                return True
    except Exception as e:
        print(f"数据获取测试失败：{str(e)}")
        return False

from app.services.news_service import generate_daily_news
from app.services.ddl_service import generate_ddl_events
from app.services.query_service import query_by_question


def test_generate_ddl_events():
    try:
        result = generate_ddl_events()
        print("\nDDL事件生成结果：")
        print(f"共生成{len(result)}条DDL事件")
        
        # 验证数据结构
        if len(result) > 0:
            print(result[0])
            
        print("DDL事件生成测试通过！")
        return True
    except Exception as e:
        print(f"DDL事件生成测试失败：{str(e)}")
        return False


def test_generate_daily_news():
    try:
        result = generate_daily_news()
        print("\n每日新闻生成结果：")
        print(f"共生成{len(result)}条每日新闻")
        
        # 验证数据结构
        if len(result) > 0:
            print(result[0])
        print("每日新闻生成测试通过！")
        return True
    except Exception as e:
        print(f"每日新闻生成测试失败：{str(e)}")
        return False


def test_query_service():
    try:
        # 测试正常查询
        question = ""
        result = query_by_question(question)
        print("\n查询服务测试 - 正常查询：")
        print(f"问题：{question}")
        print(f"回答：{result}")
        
        # 测试空字符串查询
        empty_result = query_by_question("")
        print("\n查询服务测试 - 空字符串查询：")
        print(f"结果：{empty_result}")
        
        print("查询服务测试通过！")
        return True
    except Exception as e:
        print(f"查询服务测试失败：{str(e)}")
        return False

if __name__ == "__main__":
    from app.app import create_app
    app = create_app()
    with app.app_context():
        # 调用需要上下文的函数
        test_database_connection()
        # test_fetch_data()
        # test_generate_daily_news()
        # test_generate_ddl_events()
        test_query_service()  # 添加查询服务测试
        