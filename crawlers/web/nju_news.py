from curl_cffi import requests 
from bs4 import BeautifulSoup as bs
from html2text import HTML2Text

base_url = "https://jw.nju.edu.cn"
news = []
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
headers = {
    "User-Agent": user_agent,
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
}

def test():
    """
    测试函数
    """
    c = get_content("https://jw.nju.edu.cn/7d/b7/c26263a753079/page.psp")
    if c is not None:
        print(c)
    else:
        print("获取失败")


def get_content(url:str) -> None | str:
    if url == "":
        return None
    if url.find("http") == -1: 
        url = base_url + url
    try :
      r = requests.get(url, headers=headers, timeout=10) 
      print(r.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    if r.status_code == 200:
        soup = bs(r.text, "html.parser")
        div = soup.find("div", class_="read")
        if div is None:
            return None
        h = HTML2Text()
        content = h.handle(str(div))
        content = content.replace("\n", "")
        return content
    else:
        return None

class News:
    inited:bool = False
    
    def __init__(self, link):
        self.type = link.select("span")[0].text
        self.href = link.select("span")[1].select("a")[0].get("href")
        self.title = link.select("span")[1].select("a")[0].text
        self.time = link.select("span")[2].text
        self.content = get_content(str(self.href) if self.href is not None else "")
    
    def __str__(self):
        return f"title:{self.title}\ntype:{self.type}\ntime:{self.time}\nurl:{base_url + self.href}\n\n content:{self.content}\n\n\n"

def get_news(num:int=10) -> list[News]:
    """
    获取南大教务处的通知公告
    """
    news: list[News] = []
    for i in range(num):
      url = base_url + f"/ggtz/list{i}.htm"
      r = requests.get(url, headers=headers)
      soup = bs(r.text, "html.parser")
      link_list = soup.select("ul[class='news_list list2'] li")
      for link in link_list:
          news.append(News(link))
    return news


if __name__ == "__main__":
    test()