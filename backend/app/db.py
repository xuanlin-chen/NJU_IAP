# 数据库模型和交互
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from .settings import SQLALCHEMY_DATABASE_URI

# 初始化SQLAlchemy，暂不绑定到应用
db = SQLAlchemy()

# 创建独立的数据库引擎供测试使用
engine = create_engine(SQLALCHEMY_DATABASE_URI)

def init_app(app):
    """使用应用初始化数据库"""
    db.init_app(app)