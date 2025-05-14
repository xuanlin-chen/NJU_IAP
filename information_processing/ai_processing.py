import os
import requests
import json
import time
import re
from db_importer import save_to_database, is_url_exists # 数据库导入函数

# 每次调用 api 后休眠时间，避免短时间请求次数过多
SLEEP_TIME = 7
# 配置参数
API_KEY_FILTER = "sk-jkxiokcqdihbjfyeupkcfiobxflasxdgofzdtxgmuzkiynkz" # 数据清洗的大模型API密钥
API_KEY_STRUCTURING = "sk-jkxiokcqdihbjfyeupkcfiobxflasxdgofzdtxgmuzkiynkz" # 数据结构化的大模型API密钥
API_URL_FILTER = "https://api.siliconflow.cn/v1/chat/completions"
API_URL_STRUCTURING = "https://api.siliconflow.cn/v1/chat/completions"
MARKDOWN_PATH = "C:/Users/ASUS/Desktop/input"
# DESTINATION_PATH = "C:/Users/ASUS/Desktop/output" # 这是经清洗后的文章存放的地址，仅测试使用
# JSON_STORAGE_PATH = "C:/Users/ASUS/Desktop/JSON"  # JSON文件存入路径，仅用于保证代码完整性，整合到数据库导入部分时注释掉

# 数据库配置信息
DB_CONFIG = {
    'host': 'localhost',
    'user': 'user_test',
    'password': '241880484',
    'database': 'information_for_students',
    'charset': 'utf8mb4'
}

def extract_original_link(content):
    pattern = r'\|原文链接\|:\s*(https?://\S+)'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    else:
        return None
def safe_json_parse(raw_str, max_retries=3):
    # 安全解析JSON加自动修复
    for _ in range(max_retries):
        try:
            return json.loads(raw_str)
        except json.JSONDecodeError:
            # 去除代码块包裹
            repaired = re.sub(r'^.*?```(?:json)?\s*({.*?})\s*```.*$', r'\1', raw_str, flags=re.DOTALL)
            # 替换中文引号
            repaired = repaired.replace('“', '"').replace('”', '"')
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

    prompt = f"""你是一个高校信息过滤助手，你需要完成的任务是判断文章含有信息对本科生是否有用。请按照以下步骤进行判断：
1. 内容分析：提取关键要素（核心内容/时间/对象）
2. 有用性定义（这里的有用主要判断依据是学生参与度，是由本科生在阅读完这篇文章是否会产生明确的需要完成的任务来决定，即该文章是否能达到类似于行动指南的效果）：
  a. 具有行动指引功能（如报名、准备材料、参加活动等学生需要采取行动的内容）
  b. 影响学业进度或生活安排（如考试时间、课程调整、活动时间冲突等）
  c. 涉及生活必需（宿舍调整、校园活动、安全提醒等需要学生知晓并应对的内容）
  d. 提供发展机会或涉及资格/机会的获取条件（竞赛通知、实习机会、学术讲座等需要学生把握的机遇）
  e. 其他本科生可以参与的事件
3. 需排除的内容（直接判断为“无用”）：
  a. 对已经完成的活动的总结或者记录，且对本科生后续行程没有具体的安排（若总结内容能为本科生后续行动提供明确指引或参考，则不在此列）
  b. 纯工作部署类会议报道
  c. 未落地的规划方案讨论
  d. 无具体实施路径的政策宣导
  e. 无本科生参与机制的教研活动
4. 思考判断：根据上述规则判断文章是否有用。若将文章判断为“无用”，请再次谨慎思考是否真的“无用”，以保证不遗漏信息
5. 最终结论：仅输出“有用”或者“无用”
重要提醒：
除输出“有用”或者“无用”外不要输出其他任何文字

文章内容如下：
{content}"""

    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 10
    }

    try:
        response = requests.post(API_URL_FILTER, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip()
        time.sleep(SLEEP_TIME)
        return result.lower() == "有用"
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return True  # 失败时默认视为有用

def process_files_to_db():
    if not os.path.exists(MARKDOWN_PATH):
        print(f"处理失败\n路径有误")
        return

    # 测试用
    # os.makedirs(DESTINATION_PATH, exist_ok=True)
    # os.makedirs(JSON_STORAGE_PATH, exist_ok=True)

    base_temp = read_prompt_file()

    for filename in os.listdir(MARKDOWN_PATH):
        if not filename.endswith(".md"):
            print(f"处理失败\n文件格式需为markdown格式")
            return

        filepath = os.path.join(MARKDOWN_PATH, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                url = extract_original_link(content)
                if is_url_exists(url, DB_CONFIG):
                    continue


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
                    "model": "deepseek-ai/DeepSeek-V3",
                    "messages": [{"role": "user", "content": prompt_structuring}],
                    "temperature": 0.1,
                    "max_tokens": 2000
                }

                max_retries = 3
                valid_json = False
                json_data = None

                flag_api = False
                for attempt in range(max_retries):
                    try:
                        # 调用API获取原始文本
                        response_structuring = requests.post(API_URL_STRUCTURING, headers=headers, json=payload_structuring)
                        response_structuring.raise_for_status()
                        time.sleep(SLEEP_TIME)
                    except Exception as e:
                        print(f"API调用失败: {str(e)}")
                        flag_api = True
                        break
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
                    if not flag_api:
                        print(f"文件 {filename} 经过 {max_retries} 次重试仍无法生成有效JSON，跳过处理")
                    continue

                # 将原文信息和原文链接加到json中
                json_data["原文信息"] = content
                json_data["原文链接"] = url

                try:
                    if save_to_database(json_data, DB_CONFIG):
                        print(f"文件 {filename} 成功导入数据库")
                except Exception as e:
                    print(f"文件 {filename}导入数据库失败: {str(e)}")
                # 存储验证通过的JSON 这里是测试代码
                # json_filename = os.path.splitext(filename)[0] + ".json"
                # json_path = os.path.join(JSON_STORAGE_PATH, json_filename)

                # with open(json_path, 'w', encoding='utf-8') as json_file:
                #    json.dump(json_data, json_file, ensure_ascii=False, indent=4)
                # print(f"成功结构化并储存文件 {filename}")

        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")

if __name__ == "__main__":
    process_files_to_db()