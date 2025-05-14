import os
import requests
import json
import time
import re

# 配置参数
API_KEY_FILTER = "sk-f1197f3e182144aca44aa5b13a2ee46b" # 数据清洗的大模型API密钥
API_KEY_STRUCTURING = "sk-f1197f3e182144aca44aa5b13a2ee46b" # 数据结构化的大模型API密钥
API_URL_FILTER = "https://api.deepseek.com/v1/chat/completions"
API_URL_STRUCTURING = "https://api.deepseek.com/v1/chat/completions"
MARKDOWN_PATH = "C:/Users/chenxuanlin/Desktop/input"
JSON_STORAGE_PATH = "C:/Users/chenxuanlin/Desktop/JSON"  # JSON文件存入路径，仅用于保证代码完整性，整合到数据库导入部分时注释掉

# 创建必要的目录
os.makedirs(MARKDOWN_PATH, exist_ok=True)
os.makedirs(JSON_STORAGE_PATH, exist_ok=True)

def safe_json_parse(raw_str, max_retries=3):
    # 安全解析JSON加自动修复
    for _ in range(max_retries):
        try:
            return json.loads(raw_str)
        except json.JSONDecodeError as e:
            # 去除代码块包裹
            repaired = re.sub(r'^.*?```(?:json)?\s*({.*?})\s*```.*$', r'\1', raw_str, flags=re.DOTALL)
            # 替换中文引号
            repaired = repaired.replace('"', '"').replace('"', '"')
            # 处理尾随逗号
            repaired = re.sub(r',\s*([}\]])', r'\1', repaired)
            try:
                return json.loads(repaired)
            except:
                raw_str = repaired

    # 若上述手段都不行，暴力提取第一个完整JSON
    try:
        json_str = re.search(r'\{.*\}', raw_str, flags=re.DOTALL).group()
        return json.loads(json_str)
    except:
        raise ValueError("无法提取有效JSON内容")

# 读取提示词
def read_prompt_file():
    with open("prompt_structuring.txt", "r", encoding="utf-8") as f:
        return f.read()

def analyze_article(content):
    headers = {
        "Authorization": f"Bearer {API_KEY_FILTER}",
        "Content-Type": "application/json"
    }

    prompt_filter = f"""你是一个高校信息过滤助手，你需要完成的任务是判断文章含有信息对本科生是否有用。请按照以下步骤进行判断：
1. 内容分析：提取关键要素（核心内容/时间/对象）
2. 有用性判断：
  ○ 学业影响（课程通知、考试安排、选课信息等）
  ○ 生活必需（宿舍调整、校园活动、安全提醒等）
  ○ 发展机会（竞赛通知、实习机会、学术讲座等）
3. 学生参与度判断（若有且对象为本科生，直接判断为"有用"）：
  ○ 需要学生采取具体行动
  ○ 影响学业进度或生活安排
  ○ 涉及资格/机会的获取条件
4. 需排除的内容（直接判断为"无用"）：
  ○ 纯工作部署类会议报道
  ○ 未落地的规划方案讨论
  ○ 无具体实施路径的政策宣导
  ○ 无本科生参与机制的教研活动
5. 思考判断：若将文章判断为"无用"，请再次谨慎思考是否真的"无用"，以保证不遗漏信息
6. 最终结论：仅输出"有用"或者"无用"
重要提醒：
除输出"有用"或者"无用"外不要输出其他任何文字

文章内容如下：
{content}"""

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt_filter}],
        "temperature": 0.1,
        "max_tokens": 10,
        "stream": False
    }

    try:
        response = requests.post(API_URL_FILTER, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip()
        time.sleep(1)
        return result.lower() == "有用"
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return True  # 失败时默认视为有用

def process_files_to_db():
    if not os.path.exists(MARKDOWN_PATH):
        print(f"处理失败\n路径有误")
        return

    base_temp = read_prompt_file()

    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', s)]

    for filename in sorted(os.listdir(MARKDOWN_PATH), key=natural_sort_key):
        if not filename.endswith(".md"):
            print(f"处理失败\n文件格式需为markdown格式")
            return

        filepath = os.path.join(MARKDOWN_PATH, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if analyze_article(content):
                # 测试筛选模块的代码，和其他模块接入时注释掉
                # dest_path = os.path.join(DESTINATION_PATH, filename)
                # shutil.copy2(filepath, dest_path)

                # 数据结构化部分
                headers = {
                    "Authorization": f"Bearer {API_KEY_STRUCTURING}",
                    "Content-Type": "application/json"
                }

                prompt_structuring = base_temp + "/n" + content

                payload_structuring = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt_structuring}],
                    "temperature": 0.1,
                    "max_tokens": 2000,
                    "stream": False
                }

                max_retries = 3
                valid_json = False
                json_data = None

                for attempt in range(max_retries):
                    try:
                        # 调用API获取原始文本
                        response_structuring = requests.post(API_URL_STRUCTURING, headers=headers, json=payload_structuring)
                        response_structuring.raise_for_status()
                        time.sleep(1)
                    except Exception as e:
                        print(f"API调用失败: {str(e)}")
                        continue
                        # 提取模型原始输出文本
                    try:
                        raw_output = response_structuring.json()['choices'][0]['message']['content'].strip()

                        json_data = safe_json_parse(raw_output)
                        valid_json = True
                        break

                    except Exception as e:
                        print(f"文件 {filename} json格式处理时出错: {str(e)}")
                        continue

                if not valid_json:
                    print(f"文件 {filename} 经过 {max_retries} 次重试仍无法生成有效JSON，跳过处理")
                    continue

                # 将原文信息加到json中
                json_data["原文信息"] = content

                # 只保存到JSON文件夹
                json_filename = os.path.splitext(filename)[0] + ".json"
                json_path = os.path.join(JSON_STORAGE_PATH, json_filename)
                with open(json_path, 'w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, ensure_ascii=False, indent=4)
                print(f"成功结构化并储存文件 {filename} 到 JSON 文件夹")

        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")

if __name__ == "__main__":
    process_files_to_db()
