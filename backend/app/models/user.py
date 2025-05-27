from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.db import db

class User(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'userinfo'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1024), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024), nullable=False)
    custom_ddls = db.Column(db.JSON, nullable=True)
    unsubscribed_accounts = db.Column(db.JSON, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'custom_ddls': list(self.custom_ddls) if self.custom_ddls else [],
            'unsubscribed_accounts': list(self.unsubscribed_accounts) if self.unsubscribed_accounts else []
        }

    def update_unsubscribed_accounts(self, accounts):
        """更新用户取消订阅的公众号列表"""
        if not isinstance(accounts, list):
            raise ValueError('订阅账号必须是列表格式')
        self.unsubscribed_accounts = accounts

    def add_custom_ddl(self, content):
        from datetime import date
        new_ddl = {
            'content': content,
            'date': date.today().isoformat()
        }
        if self.custom_ddls is None:
            self.custom_ddls = []
        self.custom_ddls=list(self.custom_ddls)+[new_ddl]

    def remove_custom_ddl(self, index):
        if self.custom_ddls and 0 <= index < len(self.custom_ddls):
            # 保持字典结构，只删除指定索引的元素
            ddl_list = list(self.custom_ddls)
            ddl_list.pop(index)
            self.custom_ddls = ddl_list
            # 创建新列表以确保SQLAlchemy检测到变化
