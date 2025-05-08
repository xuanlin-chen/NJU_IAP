from app import app, db

def test_database_connection():
    with app.app_context():
        try:
            # 尝试连接数据库
            conn = db.engine.connect()
            print("数据库连接成功！")
            
            # 尝试执行一个简单的查询
            result = conn.execute("SELECT 1")
            print("查询测试成功！")
            
            # 关闭连接
            conn.close()
            print("数据库连接已正常关闭")
            return True
        except Exception as e:
            print(f"数据库连接测试失败：{str(e)}")
            return False

if __name__ == '__main__':
    test_database_connection()