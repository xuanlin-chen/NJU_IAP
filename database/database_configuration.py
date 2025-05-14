# 可使用如下代码配置数据库
import pymysql

connection = pymysql.connect(
    host='47.122.71.85',  # 阿里云ESC服务器的公有IP地址
    user='crawler',                   # 用户名（我们的项目数据库在crawler用户下）
    password='241880625',             # 数据库密码
    db='information_for_students',    # 数据库名称
    charset='utf8mb4',                # 字符集
    cursorclass=pymysql.cursors.DictCursor  # 使用字典游标
)
