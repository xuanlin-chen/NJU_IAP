import os
import json
import time
import re
from openai import OpenAI
from db_importer import save_to_database, is_url_exists # 数据库导入函数

# 每次调用 api 后休眠时间，避免短时间请求次数过多
SLEEP_TIME = 2
# 配置参数
API_KEY_FILTER = "sk-******************************" # 数据清洗的大模型API密钥
API_KEY_STRUCTURING = "sk-******************************" # 数据结构化的大模型API密钥
API_URL_FILTER = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_URL_STRUCTURING = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MARKDOWN_PATH = "C:/Users/ASUS/Desktop/input_example"
# DESTINATION_PATH = "C:/Users/ASUS/Desktop/output" # 这是经清洗后的文章存放的地址，仅测试使用
# JSON_STORAGE_PATH = "C:/Users/ASUS/Desktop/JSON"  # JSON文件存入路径，仅用于保证代码完整性，整合到数据库导入部分时注释掉

# 数据库配置信息
DB_CONFIG = {
    'host': '47.122.**.**',
    'user': 'user_w',
    'password': '**********',
    'database': 'information_for_students',
    'charset': 'utf8mb4'
}

def extract_and_remove_original_link(content):
    pattern = r'\|原文链接\|:\s*(https?://\S+)'
    match = re.search(pattern, content)
    if match:
        original_link = match.group(1)
        content = re.sub(r'\|原文链接\|:\s*https?://\S+\s*', '', content)
        return original_link, content.strip()
    else:
        print("缺少原文链接或原文链接格式错误。格式必须为：“|原文链接|: http://xxx”或“|原文链接|: https://xxx”")
        return None, content

def extract_and_remove_publish_date(content):
    pattern = r'\|发布日期\|:\s*\d{4}-\d{1,2}-\d{1,2}\s*'
    match = re.search(pattern, content)
    if match:
        date_str = re.search(r'\d{4}-\d{1,2}-\d{1,2}', match.group(0))
        if date_str is None:
            print("发布日期格式错误。格式必须为：“|发布日期|: YYYY-M-D”")
            return None, content
        date_str = date_str.group(0)
        content = re.sub(pattern, '', content)
        return date_str, content.strip()
    else:
        print("缺少发布日期或发布日期格式错误。格式必须为：“|发布日期|: YYYY-M-D”")
        return None, content

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
            except Exception as e:
                raw_str = repaired
                print(f"尝试修复JSON格式失败: {str(e)}")

    # 若上述手段都不行，暴力提取第一个完整JSON
    try:
        json_str = re.search(r'\{.*\}', raw_str, flags=re.DOTALL).group()
        return json.loads(json_str)
    except:
        raise ValueError("无法提取有效JSON内容")

# 读取提示词
def read_prompt_file(prompt_type = "structuring"):
    if prompt_type == "filter":
        with open("prompt_filter.txt", "r", encoding="utf-8") as f:
            return f.read()

    if prompt_type == "structuring":
        with open("prompt_structuring.txt", "r", encoding="utf-8") as f:
            return f.read()

    if prompt_type == "summary":
        with open("prompt_summary.txt", "r", encoding="utf-8") as f:
            return f.read()

def analyze_article(content):
    api_key = API_KEY_FILTER
    base_url = API_URL_FILTER

    prompt_filter = read_prompt_file("filter")

    messages = [
        {"role": "system", "content": prompt_filter},
        {"role": "user", "content": content}
    ]

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    try:
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            temperature=0,
            max_tokens=10
        )

        result = completion.choices[0].message.content.strip()
        time.sleep(SLEEP_TIME)
        return result.lower() == "有用"
    except Exception as e:
        print(f"API_FILTER调用失败: {str(e)}")
        return True  # 失败时默认视为有用

def process_files_to_db():
    if not os.path.exists(MARKDOWN_PATH):
        print(f"处理失败\n路径有误")
        return

    # 测试用
    # os.makedirs(DESTINATION_PATH, exist_ok=True)
    # os.makedirs(JSON_STORAGE_PATH, exist_ok=True)

    prompt_structuring = read_prompt_file("structuring")

    for filename in os.listdir(MARKDOWN_PATH):
        if not filename.endswith(".md"):
            print(f"处理失败\n文件格式需为markdown格式")
            return

        filepath = os.path.join(MARKDOWN_PATH, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
                url, content_temp = extract_and_remove_original_link(original_content)
                date, content = extract_and_remove_publish_date(content_temp)
                if is_url_exists(url, DB_CONFIG):
                    continue
                if url is None or date is None:
                    continue


            if analyze_article(content):
                # 测试筛选模块的代码，和其他模块接入时注释掉
                # dest_path = os.path.join(DESTINATION_PATH, filename)
                # shutil.copy2(filepath, dest_path)

                # 数据结构化部分
                api_key = API_KEY_STRUCTURING
                base_url = API_URL_STRUCTURING

                messages = [
                    {"role": "system", "content": prompt_structuring},
                    {"role": "user", "content": content}
                ]

                client = OpenAI(
                    api_key=api_key,
                    base_url=base_url,
                )

                max_retries = 3
                valid_json = False
                json_data = None

                flag_api = False
                for attempt in range(max_retries):
                    try:
                        # 调用API获取原始文本
                        completion = client.chat.completions.create(
                            model="qwen-plus",
                            messages=messages,
                            temperature=0.1,
                            max_tokens=4096
                        )
                        time.sleep(SLEEP_TIME)
                    except Exception as e:
                        print(f"API_STRUCTURING调用失败: {str(e)}")
                        flag_api = True
                        break
                        # 提取模型原始输出文本
                    try:
                        raw_output = completion.choices[0].message.content.strip()
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

                if json_data is None:
                    continue

                # 生成文章摘要
                prompt_summary = read_prompt_file("summary")
                messages_summary = [
                    {"role": "system", "content": prompt_summary},
                    {"role": "user", "content": content}
                ]

                try:
                    completion_summary = client.chat.completions.create(
                        model="qwen-plus",
                        messages=messages_summary,
                        temperature=0.1,
                        max_tokens=500
                    )
                    summary = completion_summary.choices[0].message.content.strip()
                    time.sleep(SLEEP_TIME)
                    
                    # 在文章头部添加摘要
                    content = f"|核心摘要: {summary}|\n\n{content}"
                except Exception as e:
                    print(f"生成摘要失败: {str(e)}")

                # 将原文信息、发布日期和原文链接加到json中
                json_data["原文信息"] = content
                json_data["发布日期"] = date
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
