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


def read_csv_links(csv_file):
    """从 CSV 文件中读取链接"""
    links = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            links.append(row['链接'])
    return links


def create_output_folders():
    """创建输出文件夹"""
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists("output/text"):
        os.makedirs("output/text")
    if not os.path.exists("output/images"):
        os.makedirs("output/images")


def save_text_as_text(text_content, link_index):
    """将文字内容保存为普通文本文件"""
    file_path = f"output/text/text_{link_index}.txt"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text_content)
    print(f"文字内容已保存：{file_path}")


def save_images(img_urls, link_index):
    """保存图片到对应的文件夹"""
    img_folder = f"output/images/images_{link_index}"
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    for i, img_url in enumerate(img_urls):
        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                img_path = f"{img_folder}/image_{i}.jpg"
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                print(f"图片已保存：{img_path}")
        except Exception as e:
            print(f"保存图片失败：{e}")


def process_text_content(html):
    """处理 HTML 内容，提取并格式化文字"""
    soup = BeautifulSoup(html, "html.parser")

    # 提取文章标题
    title = soup.find("h1")
    if title:
        title_text = f"{title.get_text()}\n\n"
    else:
        title_text = ""

    # 提取文章内容
    content = ""
    for element in soup.find_all(["p", "h2", "h3", "ul", "ol", "li"]):
        if element.name == "p":
            content += f"{element.get_text()}\n\n"
        elif element.name == "h2":
            content += f"=== {element.get_text()} ===\n\n"
        elif element.name == "h3":
            content += f"--- {element.get_text()} ---\n\n"
        elif element.name in ["ul", "ol"]:
            list_items = element.find_all("li")
            for item in list_items:
                content += f"- {item.get_text()}\n"
            content += "\n"

    content = re.sub(r"\n{2,}", "\n\n", content)
    content = content.replace('\xa0', " ")

    return title_text + content


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
        time.sleep(3)
        html = driver.page_source

        # 处理文字内容
        text_content = process_text_content(html)
        save_text_as_text(text_content, link_index)

        # 提取图片 URL
        soup = BeautifulSoup(html, "html.parser")
        img_tags = soup.find_all("img")
        img_urls = []
        for img in img_tags:
            img_url = img.get("data-src") or img.get("src")
            if img_url:
                img_urls.append(img_url)
        save_images(img_urls, link_index)

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