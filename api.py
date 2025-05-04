# -*- coding: utf-8 -*-
import requests
import time
import random
import csv
import os
headers = {
    "cookie":'',
    "user-agent":''
}
url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
fad = 'MzAxODAzMjQ1NQ=='                     #爬不同公众号只需要更改 fakeid

def page(num=1):                             #要请求的文章页数
    title = []
    link = []
    create_time = []
    for i in range(num):
        data = {
            'action': 'list_ex',
            'begin': i * 5,  # 页数
            'count': '5',
            'fakeid': fad,
            'type': '9',
            'query': '',
            'token': '1425605032',
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        r = requests.get(url,headers = headers,params=data)
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)
        dic = r.json()
        for i in dic['app_msg_list']:     #遍历dic['app_msg_list']中所有内容
            create_time.append(i['create_time'])
            title.append(i['title'])      #取 key键 为‘title’的 value值
            link.append(i['link'])        #去 key键 为‘link’的 value值
    return create_time,title,link

if __name__ == '__main__':
    existing_links = set()
    if os.path.exists('articles.csv'):
        with open('articles.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_links.add(row['链接'])

    # 获取最新文章数据
    create_times, titles, links = page(5)

    # 生成标签数据
    labels = [0 if link in existing_links else 1 for link in links]

    # 写入更新后的CSV文件
    with open('articles.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['时间', '标题', '链接', '标签'])
        for ct, tt, lk, lb in zip(create_times, titles, links, labels):
            writer.writerow([ct, tt, lk, lb])
    # 可选：保留原有打印输出
    for ct, tt, lk, lb in zip(create_times, titles, links, labels):
        print(ct, tt, lk, lb)