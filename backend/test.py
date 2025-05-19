
from app.db import engine
from sqlalchemy import text

def test_database_connection():
    try:
        # 尝试连接数据库
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

if __name__ == '__main__':
    # 测试数据库连接
    if test_database_connection():
        # 如果连接成功，测试数据获取
        test_fetch_data()