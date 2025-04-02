# -*- coding: utf-8 -*-
import requests
import time
import random
import csv
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
    (time,tle,lik) = page(5)
    with open('articles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['时间','标题', '链接'])  # 写入表头
        for x, y, z in zip(time, tle, lik):
            writer.writerow([x, y, z])  # 逐行写入数据

    # 可选：保留原有打印输出
    for x, y, z in zip(time, tle, lik):
        print(x, y, z)