# -*- coding: utf-8 -*-
import requests
import time
import random
import csv
import os
headers = {
    "cookie":'appmsglist_action_3938956898=card; _qimei_uuid42=18a0b171a0510017b44bc6aaf91047ac4d0b93f86e; pac_uid=0_Sxdf68Qxzw6Yf; _qimei_q32=7e6b3461bd80f5cbb7d4a3fa2216a48f; _qimei_q36=4c68bcdf002ffce6deca54da30001d218806; _qimei_h38=19c52162b44bc6aaf91047ac02000009118a0b; suid=user_0_Sxdf68Qxzw6Yf; logTrackKey=9ef754235188487fa0dd84258b89ee20; RK=MbGwdPsnkb; ptcz=b2ff4a55c26c9f622fbe77dc1aca8ab73e73e86847f4b6db68939653925a2e3f; pgv_pvid=8723881191; ua_id=K7h2QIJ8yFFMNcTAAAAAABEPiNUQDoXPiw7Xump5wD8=; qq_domain_video_guid_verify=7377045afdff82ab; _qimei_fingerprint=d972d7a2666ab450f360b81c8c54f0dc; wxuin=43428532706510; eas_sid=z1c714935558j7W1S5g8A5C8Y6; omgid=0_Sxdf68Qxzw6Yf; rewardsn=; wxtokenkey=777; uuid=0a03d0d0463ce56474af03400b71b10e; _clck=1ezv27n|1|fvw|0; rand_info=CAESIGuT6L8Qp2KNegduvn4YLC3JWZ4lEAKefIjqiFWi6j4N; slave_bizuin=3938956898; data_bizuin=3938956898; bizuin=3938956898; data_ticket=XKpmBAz31aCseA3cJgTHNBOx1XPwmPuqTahjtxXY6ofiFAvoJYsq1t/0iAS+4WLv; slave_sid=VGJObWJKY0NtSWpKVHBKVFZZeWhpMVF6UGF6REQ2U2wwYTFTV0tmQ05qaDhab0xodFlGVk9iTlBnRHd6OF9iU0tvVFF6QUMxZHQ5RExydW8xdXUyWnZ1M0Z4bXdORWo4bjFmbFZYNFZjQ0ZnR3ljNUhiSUJMaVRNRXBibHAwSkd6dk9MZ1lnOXlFMDUyemFr; slave_user=gh_78d74b62b2df; xid=1debb0fda55571c5d3e050039da15741; mm_lang=zh_CN; _clsk=109hi53|1747200138081|4|1|mp.weixin.qq.com/weheat-agent/payload/record',
    "user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
}
url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
# 公众号配置字典，key为公众号名称，value为对应的fakeid
accounts = {
    '南京大学健雄书院': 'MzkwODQwMDEzNg==',
    # 在这里添加更多公众号
    # '公众号名称': 'fakeid',
}

def page(account_name, num=1):                #要请求的文章页数
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
            'token': '843770602',
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

if __name__ == '__main__':
    # 为每个公众号创建单独的存储目录
    os.makedirs('articles', exist_ok=True)
    
    for account_name in accounts.keys():
        print(f'正在爬取公众号：{account_name}')
        csv_file = f'articles/{account_name}.csv'
        
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