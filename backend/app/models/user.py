from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    custom_ddls = db.Column(db.JSON, nullable=True)
    subscribed_accounts = db.Column(db.JSON, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'custom_ddls': self.custom_ddls if self.custom_ddls else [],
            'subscribed_accounts': self.subscribed_accounts if self.subscribed_accounts else []
        }

    def update_subscribed_accounts(self, accounts):
        """更新用户订阅的公众号列表"""
        if not isinstance(accounts, list):
            raise ValueError('订阅账号必须是列表格式')
        self.subscribed_accounts = accounts

    def add_custom_ddl(self, content):
        from datetime import date
        new_ddl = {
            'content': content,
            'date': date.today().isoformat()
        }
        if self.custom_ddls is None:
            self.custom_ddls = [new_ddl]
        else:
            self.custom_ddls.append(new_ddl)

    def remove_custom_ddl(self, index):
        if self.custom_ddls and 0 <= index < len(self.custom_ddls):
            self.custom_ddls.pop(index)