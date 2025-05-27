# 数据库模型和交互
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from app.settings import SQLALCHEMY_DATABASE_URI, USER_DATABASE_URI

# 初始化主数据库SQLAlchemy实例
db = SQLAlchemy()

# 创建主数据库引擎供测试使用
engine = create_engine(SQLALCHEMY_DATABASE_URI)

def init_app(app):
    """使用应用初始化数据库"""
    db.init_app(app)