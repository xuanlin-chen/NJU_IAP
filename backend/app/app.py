# 应用程序工厂函数
from flask import Flask
from flask_cors import CORS
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

def create_app():
    """应用程序工厂函数"""
    app = Flask(__name__)
    
    # 启用CORS以支持跨域请求
    CORS(app)
    
    # 加载配置
    from settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    # 初始化数据库
    from db import init_app as init_db
    init_db(app)
    
    # 注册路由
    # from routes import init_app as init_routes
    # init_routes(app)
    
    return app

# 创建应用实例供导入使用
app = create_app()


# 直接执行时运行
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)