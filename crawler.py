import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import os
# 读取CSV文件
file_path = 'articles.csv'  # 替换为你的CSV文件路径
df = pd.read_csv(file_path)

# 提取链接列
links = df['链接'].tolist()

folder_name = f"html_content"  # 根据时间戳命名文件夹
os.makedirs(folder_name, exist_ok=True)  # 如果文件夹已存在，不会报错

# 遍历链接并爬取内容
for i, link in enumerate(links):
    print(f"正在爬取第 {i + 1} 个链接: {link}")

    try:
        # 模拟人工访问，设置请求头
        headers = {
            'User-Agent': ''
        }
        # 发送请求
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 保存HTML内容到单独的文件
        file_name = f"page_{i + 1}.html"
        file_path = os.path.join(folder_name, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

        print(f"第 {i + 1} 个链接的HTML内容已保存到: {file_path}\n")

    except Exception as e:
        print(f"第 {i + 1} 个链接爬取失败: {e}\n")


print("爬取完成！HTML内容已保存到文件中。")