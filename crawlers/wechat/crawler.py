import csv
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import random
from datetime import datetime
links = []
# 配置输出路径
MARKDOWN_PATH = "C:\\Users\\chenxuanlin\\Desktop\\njuIAP\\NJU_IAP\\input_example"
#改成你们自己的路径

def read_csv_links(account_name):
    """从 CSV 文件中读取标签为1的链接
    :param account_name: 公众号名称，用于构建文件路径
    """
    filtered_links = []
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "article_link", f"{account_name}.csv")
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '标签' in row and row['标签'] == '1':
                    filtered_links.append(row['链接'])
    except FileNotFoundError:
        print(f"警告: 未找到 {account_name} 的CSV文件")
    return filtered_links


def create_output_folders(account_name=None):
    """创建输出文件夹
    :param account_name: 公众号名称，用于创建子文件夹
    """
    if not os.path.exists(MARKDOWN_PATH):
        os.makedirs(MARKDOWN_PATH)
        
    if account_name:
        account_path = os.path.join(MARKDOWN_PATH, account_name)
        if not os.path.exists(account_path):
            os.makedirs(account_path)


def save_text_as_text(text_content, link_index, link, today_str):
    """将文字内容保存为 Markdown 文件，第二行写入日期"""
    file_path = os.path.join(MARKDOWN_PATH, f"article_{link_index}.md")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"原文链接: {link}\n")
        file.write(f"{today_str}\n\n")
        file.write(text_content)
    print(f"Markdown 内容已保存：{file_path}")


def process_text_content(html):
    """处理 HTML 内容，提取并格式化文字为 Markdown"""
    soup = BeautifulSoup(html, "html.parser")
    text_content = []
    for element in soup.find_all(True):
        if element.name == 'p':
            text = element.get_text(strip=True)
            if text:
                text_content.append(text)
        elif element.name == 'h1':
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"# {text}")
        elif element.name == 'h2':
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"## {text}")
        elif element.name == 'h3':
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"### {text}")
        elif element.name == 'img':
            continue
        elif element.name == 'ul' or element.name == 'ol':
            list_items = element.find_all('li')
            for item in list_items:
                text = item.get_text(strip=True)
                if text:
                    if element.name == 'ul':
                        text_content.append(f"- {text}")
                    else:
                        text_content.append(f"1. {text}")
        elif element.name == 'a':
            text = element.get_text(strip=True)
            href = element.get('href')
            if text and href:
                text_content.append(f"[{text}]({href})")
        elif element.name == 'strong':
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"**{text}**")
        elif element.name == 'em':
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"*{text}*")
    markdown_content = "\n\n".join(text_content)
    index = markdown_content.find("精彩荐读")
    if index != -1:
        return markdown_content[:index]
    else:
        return markdown_content

def crawl_and_save(link, link_index, today_str):
    """爬取并保存内容"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    try:
        driver.get(link)
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)
        html = driver.page_source
        text_content = process_text_content(html)
        save_text_as_text(text_content, link_index, link, today_str)
    except Exception as e:
        print(f"处理链接 {link} 时出错：{e}")
    finally:
        driver.quit()

def main():
    import os
    today_str = datetime.now().strftime("%Y-%m-%d")
    create_output_folders()
    
    # 遍历article_link文件夹中的所有CSV文件
    article_link_dir = os.path.join(os.path.dirname(__file__), "..", "..", "article_link")
    for csv_file in os.listdir(article_link_dir):
        if csv_file.endswith('.csv'):
            account_name = os.path.splitext(csv_file)[0]
            print(f"正在处理账号: {account_name}")
            create_output_folders(account_name)
            links = read_csv_links(account_name)
            for i, link in enumerate(links):
                print(f"处理链接 {i + 1}/{len(links)}: {link}")
                crawl_and_save(link, i + 1, today_str)

if __name__ == "__main__":
    main()