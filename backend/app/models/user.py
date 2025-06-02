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

    def add_custom_ddl(self, content, date_str=None):
        from datetime import date, datetime
        # 如果提供了日期，则使用提供的日期，否则使用今天的日期
        if date_str:
            # 确保日期格式正确
            try:
                # 尝试解析包含时间的日期字符串 (YYYY-MM-DD HH:MM:SS)
                if ' ' in date_str:
                    # 包含日期和时间
                    date_part, time_part = date_str.split(' ', 1)
                    year, month, day = map(int, date_part.split('-'))
                    
                    # 解析时间部分
                    hour, minute, second = 0, 0, 0
                    time_parts = time_part.split(':')
                    if len(time_parts) >= 1:
                        hour = int(time_parts[0])
                    if len(time_parts) >= 2:
                        minute = int(time_parts[1])
                    if len(time_parts) >= 3:
                        second = int(time_parts[2])
                    
                    # 创建包含日期和时间的字符串
                    custom_date = datetime(year, month, day, hour, minute, second).isoformat()
                else:
                    # 只有日期部分
                    year, month, day = map(int, date_str.split('-'))
                    custom_date = date(year, month, day).isoformat()
            except (ValueError, AttributeError):
                # 如果日期格式不正确，回退到使用今天的日期
                custom_date = datetime.now().isoformat()
        else:
            custom_date = datetime.now().isoformat()
            
        new_ddl = {
            'content': content,
            'date': custom_date
        }
        if self.custom_ddls is None:
            self.custom_ddls = []
        # 将新DDL添加到列表开头而不是末尾
        self.custom_ddls=[new_ddl]+list(self.custom_ddls)

    def remove_custom_ddl(self, index):
        if self.custom_ddls and 0 <= index < len(self.custom_ddls):
            # 保持字典结构，只删除指定索引的元素
            ddl_list = list(self.custom_ddls)
            ddl_list.pop(index)
            self.custom_ddls = ddl_list
            # 创建新列表以确保SQLAlchemy检测到变化
