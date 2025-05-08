from wxauto import WeChat
import time
import csv
from datetime import datetime

wx = WeChat()

# 首先设置一个监听列表，列表元素为指定好友（或群聊）的昵称
listen_list = [

]

# 然后调用`AddListenChat`方法添加监听对象，其中可选参数`savepic`为是否保存新消息图片
for i in listen_list:
    wx.AddListenChat(who=i,
    savepic   = True,   # 保存图片
    savefile  = True,   # 保存文件
    savevoice = True    # 保存语音转文字内容
)

wait = 1

# 创建CSV文件并写入表头
with open('wechat_messages.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['发送人', '消息时间', '消息内容'])

while True:
    try:
        msgs = wx.GetListenMessage()
        for chat in msgs:
            one_msgs = msgs.get(chat)  # 获取消息内容

            # 回复收到
            for msg in one_msgs:
                if msg.type == 'sys':
                    print(f'【系统消息】{msg.content}')

                elif msg.type == 'friend':
                    sender = msg.sender_remark  # 这里可以将msg.sender改为msg.sender_remark，获取备注名
                    print(f'<{sender.center(10, "-")}>：{msg.content}')

                    # 获取当前时间
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # 写入CSV文件
                    with open('wechat_messages.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([sender, current_time, msg.content])
        time.sleep(wait)
    except KeyboardInterrupt:
        print('Bye~')
        break