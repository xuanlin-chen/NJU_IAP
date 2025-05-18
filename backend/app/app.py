# 应用程序工厂函数
from flask import Flask
from flask_cors import CORS

def create_app():
    """应用程序工厂函数"""
    app = Flask(__name__)
    
    # 启用CORS以支持跨域请求
    CORS(app)
    
    # 加载配置
    from .config.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    # 初始化数据库
    from .models.db import init_app as init_db
    init_db(app)
    
    # 注册路由
    from .routes import init_app as init_routes
    init_routes(app)
    
    return app


# 直接执行时运行
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)