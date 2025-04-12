from curl_cffi import requests
import bs4
import os
# -*- coding: utf-8 -*-

news = []
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
headers = {
    "User-Agent": user_agent,
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
}
parent_url = "https://jw.nju.edu.cn/"


class News:
    def __init__(self, title, type, time, href):
        self.title = title
        self.type = type
        self.time = time
        self.href = href


for i in range(1, 10):
    url = f"https://jw.nju.edu.cn/ggtz/list{i}.htm"
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    link_list = soup.select("ul[class='news_list list2'] li")
    for link in link_list:
        type = link.select("span")[0].text
        href = link.select("span")[1].select("a")[0].get("href")
        title = link.select("span")[1].select("a")[0].text
        time = link.select("span")[2].text
        news.append(News(title, type, time, href))

if not os.path.exists("./content"):
    os.makedirs("./content")

with open("./content/news.txt", "w", encoding="utf-8") as f:
    for i in news:
        f.write(
            f"title:{i.title}\ntype:{i.type}\ntime:{i.time}\nurl:{parent_url + i.href}\n"
        )
