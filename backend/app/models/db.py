# 数据库模型和交互
from flask_sqlalchemy import SQLAlchemy

# 初始化SQLAlchemy，暂不绑定到应用
db = SQLAlchemy()

def init_app(app):
    """使用应用初始化数据库"""
    db.init_app(app)