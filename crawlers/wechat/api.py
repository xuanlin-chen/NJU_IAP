# -*- coding: utf-8 -*-
import requests
import time
import random
import csv
import os
headers = {
    "cookie":'appmsglist_action_3938956898=card; _qimei_uuid42=18a0b171a0510017b44bc6aaf91047ac4d0b93f86e; pac_uid=0_Sxdf68Qxzw6Yf; _qimei_q32=7e6b3461bd80f5cbb7d4a3fa2216a48f; _qimei_q36=4c68bcdf002ffce6deca54da30001d218806; _qimei_h38=19c52162b44bc6aaf91047ac02000009118a0b; suid=user_0_Sxdf68Qxzw6Yf; logTrackKey=9ef754235188487fa0dd84258b89ee20; RK=MbGwdPsnkb; ptcz=b2ff4a55c26c9f622fbe77dc1aca8ab73e73e86847f4b6db68939653925a2e3f; pgv_pvid=8723881191; ua_id=K7h2QIJ8yFFMNcTAAAAAABEPiNUQDoXPiw7Xump5wD8=; qq_domain_video_guid_verify=7377045afdff82ab; _qimei_fingerprint=d972d7a2666ab450f360b81c8c54f0dc; wxuin=43428532706510; eas_sid=z1c714935558j7W1S5g8A5C8Y6; omgid=0_Sxdf68Qxzw6Yf; mm_lang=zh_CN; poc_sid=HPieJGijcu5HqEAFA9HaxBr5B9Qg7X5Rm-KZi1Q8; uuid=9166b0ff3a26f4c3bb045266cb90a52f; _clck=1ezv27n|1|fw0|0; rand_info=CAESINhlzgCQfTFvnQr1gwMy+SBZ1GIZIy2sR3/Z9Zw+l8+V; slave_bizuin=3938956898; data_bizuin=3938956898; bizuin=3938956898; data_ticket=4ojhzFOTRZHrnWChmCqu6MoC163FCta+oy8eejWTH8jeof2rsuR8aWYZwkB8j+Z0; slave_sid=VVpKR29oYWV5WkhKdno3S2hVOTBuMDVEOWlmMWFDNV9VOE12VnV3MHVXYVRvdnFfN3NYYVpBZkJoblhPR0k3NlkxTFhWdXJRSW5YbnA2eTNqNUc2M3NhQTJNMDB0akZVX0FmVnZzMkROS2lsa1RYY0lqdmZWa3lDeUFBMmphcHNlc0V5WXQ4VDNsT2xIZ1Nq; slave_user=gh_78d74b62b2df; xid=76e87e06ddaab7bd17b45cdaa2b5d661; _clsk=qcmrb7|1747573654909|2|1|mp.weixin.qq.com/weheat-agent/payload/record',
    "user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
}
url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
# 公众号配置字典，key为公众号名称，value为对应的fakeid
accounts = {
    '南京大学健雄书院': 'MzkwODQwMDEzNg==',
    '南京大学新生学院': 'MzkwNDE4ODYyMg==',
    '南京大学': 'MzAxODAzMjQ1NQ==',
    '南京大学图书馆': 'MjM5NTE5Mjk1Mg==',
    '南大全球交流': 'MzAwMDYzNDc4MQ==',
    '南京大学安邦书院': 'MzkwNDE4ODYyMg==',
    '南京大学行知书院': 'Mzg5MjU1MjAyMA==',
    # 在这里添加更多公众号
    # '公众号名称': 'fakeid',
}

def page(account_name, num=3):                #要请求的文章页数
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
            'token': '1272874465',
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
        create_times, titles, links = page(account_name, 5)

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