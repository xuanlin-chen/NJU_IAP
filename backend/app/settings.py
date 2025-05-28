# 应用程序配置设置

# Flask和数据库设置
# 主数据库连接
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user_w:241880484@47.122.71.85:3306/information_for_students?charset=utf8mb4'
# 用户数据库连接
USER_DATABASE_URI = 'mysql+pymysql://user_admin:usertable241880@47.122.71.85:3306/userinfo?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# OpenAI配置
OPENAI_API_KEY = "your-openai-key"

# 消息类型定义
MESSAGE_TYPES = {
    '比赛通知': {'table_name': '比赛通知'},
    '学习资源': {'table_name': '学习资源'},
    '校园通知': {'table_name': '校园通知'},
    '学业申请': {'table_name': '学业申请'},
    '学业相关政策': {'table_name': '学业相关政策'},
    '奖励、资助政策': {'table_name': '奖励、资助政策'},
    '惩罚制度': {'table_name': '惩罚制度'},
    '校园安全': {'table_name': '校园安全'},
    '讲座或分享会信息': {'table_name': '讲座或分享会信息'},
    '志愿活动': {'table_name': '志愿活动'},
    '社会实践': {'table_name': '社会实践'},
    '国际交流项目': {'table_name': '国际交流项目'},
    '社团消息': {'table_name': '社团消息'},
    '文体活动': {'table_name': '文体活动'},
    '实践培训活动': {'table_name': '实践培训活动'},
    '作品征集': {'table_name': '作品征集'},
    '其他活动': {'table_name': '其他活动'},
    '实习就业': {'table_name': '实习就业'},
    '其他类型': {'table_name': '其他类型'}
}
