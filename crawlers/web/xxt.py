import re
import os
import json
from base64 import b64encode as b64
from openai import OpenAI
from playwright.sync_api import sync_playwright, Playwright


def into_json(json_str) -> str:
    """删除JSON中的rtf_content字段及其内容"""
    # 正则表达式匹配rtf_content字段及其内容
    pattern_1 = r"(['\"])rtf_content\1\s*:\s*(['\"])(?:\\.|[^\\])*?\2,"
    pattern_2 = r"(['\"])attachment\1\s*:\s*(['\"])(?:\\.|[^\\])*?\2,"
    pattern_3 = r"(['\"])cparams\1\s*:\s*(['\"])(?:\\.|[^\\])*?\2,"

    # 替换为空字符串
    cleaned_content = re.sub(pattern_1, "", json_str)
    cleaned_content = re.sub(pattern_2, "", cleaned_content)
    cleaned_content = re.sub(pattern_3, "", cleaned_content)
    cleaned_content = (
        cleaned_content.replace("'", '"')  # 替换单引号为双引号
        .replace('"[', "[")  # 修复数组格式
        .replace(']"', "]")
        .replace('"{', "{")  # 修复对象格式
        .replace('}"', "}")
        .replace('\\"', '"')  # 替换双引号
        .replace("True", "true")  # 修复布尔值
        .replace("False", "false")
        .replace("None", "null")  # 修复None
    )
    return cleaned_content


def handle_verify_code(png: bytes) -> str:
    png_base64 = b64(png).decode("utf-8")
    client = OpenAI(
        api_key=os.getenv("aliyun_api_trans"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    config = {
        "model": "qwen-vl-max-latest",
        "messages": [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful assistant."}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{png_base64}"},
                    },
                    {"type": "text", "text": "识别图中验证码"},
                ],
            },
        ],
    }
    completion = client.chat.completions.create(**config)
    response = completion.choices[0].message.content
    pattern = r"[a-zA-Z0-9]{4}"
    v_code: str = ""
    try:
        v_code = re.findall(pattern, response)[0]
        return v_code
    except:
        exit("error")


class User:
    def __init__(self, phone: str, pwd: str):
        self.phone = phone
        self.pwd = pwd


def req(playwright: Playwright, user: User) -> dict:
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://v3.chaoxing.com/toJcLogin")
    page.wait_for_load_state("networkidle")
    verify = page.locator('xpath=//*[@id="verifyCanvas"]')
    phone = page.locator('xpath=//*[@id="phone"]')
    pwd = page.locator('xpath=//*[@id="pwd"]')
    log_code = page.locator('xpath=//*[@id="LogCode"]')
    login = page.locator('xpath=//*[@id="login"]')
    phone.fill(user.phone)
    pwd.fill(user.pwd)
    png = verify.screenshot()
    v_code = handle_verify_code(png)
    log_code.fill(v_code)
    login.click()
    page.wait_for_timeout(2000)
    jump = page.locator('xpath=//*[@id="showPrompt"]/a')
    if jump.is_visible():
        jump.click()

    else:
        return {}
    res = context.request.get(
        "https://notice.chaoxing.com/mobile/notice/getNoticeList?type=2"
    )
    if res.status != 200:
        return {}
    res = res.text()
    res = into_json(res)
    print(res)
    res = json.loads(res)
    browser.close()
    return res


def into_file(res: dict) -> bool:
    if res == {}:
        return False
    events = res["notices"]["list"]
    info = {}
    for event in events:
        if event["redDot"] != 1:
            continue
        ddl: str = event.get("completeTime", "Unknown")
        content: str = event.get("content", "No content")
        info[ddl] = content
    with open("./content/xxt.txt", "w") as f:
        for k, v in info.items():
            f.write(f"ddl:{k}\ncontent:\n{v}\n\n")
    return True


if __name__ == "__main__":
    with sync_playwright() as playwright:
        jyr = User("17805258668", "xiaohai20063015")
        while True:
            if into_file(req(playwright, jyr)):
                break
