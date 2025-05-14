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
links = []
# 配置输出路径
MARKDOWN_PATH = "C:/Users/chenxuanlin/Desktop/input"

def read_csv_links(csv_file):
    """从 CSV 文件中读取链接"""

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            links.append(row['链接'])
    return links


def create_output_folders():
    """创建输出文件夹"""
    if not os.path.exists(MARKDOWN_PATH):
        os.makedirs(MARKDOWN_PATH)


def save_text_as_text(text_content, link_index):
    """将文字内容保存为 Markdown 文件"""
    file_path = os.path.join(MARKDOWN_PATH, f"article_{link_index}.md")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"原文链接: {links[link_index-1]}\n\n{text_content}")
    print(f"Markdown 内容已保存：{file_path}")


def process_text_content(html):
    """处理 HTML 内容，提取并格式化文字为 Markdown"""
    soup = BeautifulSoup(html, "html.parser")

    # 提取所有文本内容
    text_content = []

    # 遍历所有标签，提取文本并转换为 Markdown
    for element in soup.find_all(True):
        if element.name == 'p':
            # 段落文本
            text = element.get_text(strip=True)
            if text:
                text_content.append(text)
        elif element.name == 'h1':
            # 一级标题
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"# {text}")
        elif element.name == 'h2':
            # 二级标题
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"## {text}")
        elif element.name == 'h3':
            # 三级标题
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"### {text}")
        elif element.name == 'img':
            # 图片（图片的 URL 会在 save_images 中处理）
            continue
        elif element.name == 'ul' or element.name == 'ol':
            # 列表
            list_items = element.find_all('li')
            for item in list_items:
                text = item.get_text(strip=True)
                if text:
                    if element.name == 'ul':
                        text_content.append(f"- {text}")
                    else:
                        text_content.append(f"1. {text}")
        elif element.name == 'a':
            # 链接
            text = element.get_text(strip=True)
            href = element.get('href')
            if text and href:
                text_content.append(f"[{text}]({href})")
        elif element.name == 'strong':
            # 加粗
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"**{text}**")
        elif element.name == 'em':
            # 斜体
            text = element.get_text(strip=True)
            if text:
                text_content.append(f"*{text}*")

    # 将文本内容合并为一个字符串
    markdown_content = "\n\n".join(text_content)
    index = markdown_content.find("精彩荐读")
    if index != -1:
        return markdown_content[:index]
    else:
        return markdown_content


def crawl_and_save(link, link_index):
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

        # 处理文字内容
        text_content = process_text_content(html)
        save_text_as_text(text_content, link_index)

    except Exception as e:
        print(f"处理链接 {link} 时出错：{e}")
    finally:
        driver.quit()


def main():
    csv_file = "articles.csv"  # CSV 文件路径
    links = read_csv_links(csv_file)
    create_output_folders()

    for i, link in enumerate(links):
        print(f"处理链接 {i + 1}/{len(links)}: {link}")
        crawl_and_save(link, i + 1)


if __name__ == "__main__":
    main()