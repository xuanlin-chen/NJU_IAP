# 应用程序配置设置

# Flask和数据库设置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user_w:241880484@47.122.71.85:3306/information_for_students?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# OpenAI配置
OPENAI_API_KEY = "your-openai-key"

# 消息类型定义
MESSAGE_TYPES = {
    # 示例消息类型配置
    "通知": {
        "table_name": "notifications",
        "tags_schema": {
            # 标签结构定义
        },
        "content_schema": {
            # 内容结构定义
        }
    },
    "规章制度": {
        "table_name": "regulations",
        "tags_schema": {
            # 标签结构定义
        },
        "content_schema": {
            # 内容结构定义
        }
    }
    # 根据需要添加更多消息类型
}