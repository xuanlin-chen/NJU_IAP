import csv
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import random
import sys
import os

# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 导入信息处理模块
from information_processing.information_filter import process_single_article


def read_csv_links(csv_file):
    """从 CSV 文件中读取链接"""
    links = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            links.append(row['链接'])
    return links


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


def crawl_and_process(link):
    """爬取并处理内容"""
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
        
        # 使用信息处理模块处理文章内容
        if text_content:
            structured_data = process_single_article(text_content)
            if structured_data:
                print(f"文章处理成功，类型：{structured_data.get('type', '未知')}")
                return structured_data
            else:
                print("文章处理失败或被判定为无用信息")
                return None


    except Exception as e:
        print(f"处理链接 {link} 时出错：{e}")
        return None
    finally:
        driver.quit()


def crawl_all_articles(csv_file="articles.csv"):
    """爬取并处理所有文章，返回处理结果列表"""
    links = read_csv_links(csv_file)
    results = []

    for i, link in enumerate(links):
        print(f"处理链接 {i + 1}/{len(links)}: {link}")
        result = crawl_and_process(link)
        if result:
            results.append(result)
    
    return results

def main():
    csv_file = "articles.csv"  # CSV 文件路径
    results = crawl_all_articles(csv_file)
    print(f"成功处理")
    return results


if __name__ == "__main__":
    main()