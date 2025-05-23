from curl_cffi import requests
from playwright.sync_api import sync_playwright

base_url: str = "https://ndwy.nju.edu.cn/dztml/#/"


def go_into():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(base_url)
        page.wait_for_timeout(10000)
        #print html
        html = page.content()
        print(html)


if __name__ == "__main__":
    go_into()
