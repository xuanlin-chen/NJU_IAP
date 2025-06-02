
from flask import app
from app.db import db
from app.app import create_app
from sqlalchemy import text
from app.models.user import User



def test_database_connection():
    try:
            conn = db.engine.connect()
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
            with db.engine.connect() as conn:
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
from app.services.date_query_service import generate_date_data


def test_generate_ddl_events():
    try:
        result = generate_ddl_events()
        print("\nDDL事件生成结果：")
        print(f"共生成{len(result)}条DDL事件")
        
        # 验证数据结构
        if len(result) > 0:
            print(result)
            
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
        question = "EL报名什么时候截至"
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

def test_user_database_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("\nUser数据库连接成功！")
            return True
    except Exception as e:
        print(f"\nUser数据库连接测试失败：{str(e)}")
        return False

def test_user_model_methods():
    print("\n开始测试用户模型方法...")
    try:
        # 创建一个临时用户对象（不保存到数据库）
        user = User(username='test_user')

        # 测试 set_password 和 check_password
        password = 'secure_password'
        user.set_password(password)
        if user.check_password(password):
            print("set_password 和 check_password 测试通过")
        else:
            print("set_password 或 check_password 测试失败")
            return False

        # 测试 add_custom_ddl
        user.add_custom_ddl('完成项目报告')
        user.add_custom_ddl('准备演示文稿')
        if user.custom_ddls and len(user.custom_ddls) == 2:
            print("add_custom_ddl 测试通过")
        else:
            print("add_custom_ddl 测试失败")
            return False

        # 测试 remove_custom_ddl
        user.remove_custom_ddl(0) # 删除第一个
        if user.custom_ddls and len(user.custom_ddls) == 1 and user.custom_ddls[0]['content'] == '准备演示文稿':
             print("remove_custom_ddl 测试通过")
        else:
            print("remove_custom_ddl 测试失败")
            return False

        # 测试 update_unsubscribed_accounts
        accounts_to_unsubscribe = ['account1', 'account2']
        user.update_unsubscribed_accounts(accounts_to_unsubscribe)
        if user.unsubscribed_accounts == accounts_to_unsubscribe:
            print("update_unsubscribed_accounts 测试通过")
        else:
            print("update_unsubscribed_accounts 测试失败")
            return False

        print("用户模型方法测试全部通过！")
        return True
    except Exception as e:
        print(f"用户模型方法测试失败：{str(e)}")
        return False

def test_date_query_service():
    try:
        # 测试正确的日期格式
        date_str = "2025-05-20"
        result = generate_date_data(date_str)
        print("\n日期查询服务测试 - 正确日期格式：")
        print(f"日期：{date_str}")
        print(f"新闻数量：{len(result.get('news', []))}")
        print(f"DDL事件数量：{len(result.get('ddl_events', []))}")
        
        # 测试错误的日期格式
        invalid_date = "2025/05/20"
        error_result = generate_date_data(invalid_date)
        print("\n日期查询服务测试 - 错误日期格式：")
        print(f"日期：{invalid_date}")
        print(f"结果：{error_result}")
        
        print("日期查询服务测试通过！")
        return True
    except Exception as e:
        print(f"日期查询服务测试失败：{str(e)}")
        return False

if __name__ == "__main__":
    from app.app import create_app
    app = create_app()
    with app.app_context():
        # 调用需要上下文的函数
        # test_database_connection()
        # test_fetch_data()
        # test_generate_daily_news()
        test_generate_ddl_events()
        # test_date_query_service()
        # test_user_database_connection()
        # test_user_model_methods()
        # test_query_service()  # 添加查询服务测试
        