# 应用程序工厂函数
from flask import Flask
from flask_cors import CORS
import sys
from pathlib import Path

def create_app():
    """应用程序工厂函数"""
    app = Flask(__name__)
    
    # 启用CORS以支持跨域请求
    CORS(app,resources={r"/*": {"origins": "http://47.115.222.10:80"}})
    
    # 设置JSON编码
    app.config['JSON_AS_ASCII'] = False
    # 设置一个密钥，用于会话管理和安全
    app.config['SECRET_KEY'] = 'your_secret_key_here' # 生产环境中请使用复杂且保密的密钥
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # 增加CSRF保护
    app.config['SESSION_COOKIE_SECURE'] = True # 仅通过HTTPS发送Cookie
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # 会话有效期为1小时
    # 加载配置
    from app.settings import SQLALCHEMY_DATABASE_URI, USER_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_BINDS'] = {
        'userinfo': USER_DATABASE_URI
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    # 初始化数据库
    from app.db import init_app as init_db
    init_db(app)
    
    # 注册路由
    from app.routes import init_app as init_routes
    init_routes(app)
    
    return app

# 创建应用实例供导入使用
# app = create_app() # 此行已注释，以避免循环导入，app实例由run.py或下面的__main__块创建


# 直接执行时运行
if __name__ == '__main__':
    app_instance = create_app() # 使用不同的变量名以避免与潜在的全局 'app' 混淆
    app_instance.run(host='0.0.0.0', port=5000, debug=True)