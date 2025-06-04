# -*- coding: utf-8 -*-
import requests
import time
import random
import csv
import os
headers = {
    "cookie":'',
    "user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
}
url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
# 公众号配置字典，key为公众号名称，value为对应的fakeid
accounts = {
    '南京大学新生学院': 'MzkwNDE4ODYyMg==',
    '南京大学': 'MzAxODAzMjQ1NQ==',
    '南京大学图书馆': 'MjM5NTE5Mjk1Mg==',
    '南大全球交流': 'MzAwMDYzNDc4MQ==',
    '南青科创': 'MzI4MjM3OTYyNw==',
    '南大社团': 'MzIxNTg4MjY0NA==',
    '南大体育': 'MzI2ODcyNTU2OQ==',
    '南大港澳台交流': 'MzA3NzczMTI5MA==',
    '南大高研院': 'MzI4MTY1MjkyOA==',
    '南商满天星': 'MzI2ODYyOTA5NQ==',
    '南京大学安邦书院': 'Mzk0NzE5NDkwOA==',
    '南京大学行知书院': 'Mzg5MjU1MjAyMA==',
    '南京大学健雄书院': 'MzkwODQwMDEzNg==',
    '南京大学有训书院': 'Mzk0MDE5MTk3Mw==',
    '南京大学开甲书院': 'Mzk0MjE5MDI5Nw==',
    '南京大学秉文书院': 'MzkzMTE5MDM1MA==',
    '南京大学毓琇书院': 'Mzg5MTU0NDIzOQ==',
    
    # 在这里添加更多公众号
    # '公众号名称': 'fakeid',
}

def page(account_name, num=6):                #要请求的文章页数
    title = []
    link = []
    create_time = []
    fad = accounts.get(account_name)
    if not fad:
        print(f'未找到公众号 {account_name} 的配置')
        return [], [], []
        
    for i in range(num):
        data = {
            'action': 'list_ex',
            'begin': i * 4,  # 页数
            'count': '4',
            'fakeid': fad,
            'type': '9',
            'query': '',
            'token': '196188915',
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        r = requests.get(url, headers=headers, params=data)
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)
        dic = r.json()
        for i in dic['app_msg_list']:     #遍历dic['app_msg_list']中所有内容
            create_time.append(i['create_time'])
            title.append(i['title'])      #取 key键 为'title'的 value值
            link.append(i['link'])        #去 key键 为'link'的 value值
    return create_time, title, link

def reset_all_labels():
    """重置所有CSV文件中的标签为0"""
    if not os.path.exists('article_link'):
        return
    
    for filename in os.listdir('article_link'):
        if not filename.endswith('.csv'):
            continue
            
        csv_file = os.path.join('article_link', filename)
        temp_rows = []
        
        # 读取现有数据
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            # 保存表头
            fieldnames = reader.fieldnames
            # 如果fieldnames为None，使用默认字段
            if fieldnames is None:
                fieldnames = ['时间', '标题', '链接', '标签', '公众号']
            # 读取所有行，将标签改为0
            for row in reader:
                row['标签'] = '0'
                temp_rows.append(row)
        
        # 写回文件
        with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(temp_rows)

if __name__ == '__main__':
    # 为每个公众号创建单独的存储目录
    os.makedirs('article_link', exist_ok=True)
    
    # 每日重置所有文章的标签为0
    reset_all_labels()
    print('已重置所有文章标签为0')
    
    for account_name in accounts.keys():
        print(f'正在爬取公众号：{account_name}')
        csv_file = f'article_link/{account_name}.csv'
        
        # 读取现有链接
        existing_links = set()
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_links.add(row['链接'])

        # 获取最新文章数据
        create_times, titles, links = page(account_name, 7)

        if not links:  # 如果没有获取到数据，继续下一个公众号
            continue

        # 生成标签数据
        labels = [0 if link in existing_links else 1 for link in links]

        # 写入更新后的CSV文件
        with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['时间', '标题', '链接', '标签', '公众号'])
            for ct, tt, lk, lb in zip(create_times, titles, links, labels):
                writer.writerow([ct, tt, lk, lb, account_name])
        
        print(f'{account_name} 爬取完成，共获取 {len(links)} 条数据')
        # 可选：打印详细信息
        for ct, tt, lk, lb in zip(create_times, titles, links, labels):
            print(f'[{account_name}] {ct} {tt} {lk} {lb}')