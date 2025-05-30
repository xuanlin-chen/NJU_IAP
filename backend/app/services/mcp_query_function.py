from http import HTTPStatus
from dashscope import Application
from datetime import datetime
import json
import re
import os

# API_KEY_INTERACT = os.getenv("DASHSCOPE_API_KEY_INTERACT") # 将api_key添加至环境变量
# API_KEY_SEARCH = os.getenv("DASHSCOPE_API_KEY_SEARCH")
API_KEY_INTERACT = 'sk-842115343a2c4f928c445da9e1a7a5b9'
API_KEY_SEARCH = 'sk-f7d1df9afce849a5aad2c27a5a85c97d'
APP_ID_INTERACT = 'd983ba22ecd94a76b83e14f58aea3877'
APP_ID_SEARCH = '105936f2ac6949da98c4375b97fa082f'  # 五并发

# 安全解析JSON加自动修复
def safe_json_parse(raw_str):
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

def call_agent(api_key, app_id, query, is_stream=False):
    if query == '':
        return None
    try:
        response = Application.call(
            api_key=api_key,
            app_id=app_id,
            prompt=query,
            stream=is_stream
        )

        if response.status_code == HTTPStatus.OK:
            return response.output.text
        else:
            error_msg = {
                'request_id': response.request_id,
                'code': response.status_code,
                'message': response.message
            }
            print(f'API fail：{error_msg}')
            return None

    except Exception as e:
        print(f'Error：{str(e)}')
        return None

def is_to_db(json_data):
    to = json_data['to']
    content = json_data['content']
    if to == 'database' :
        return True, content
    else:
        return False, content

def query_mcp(query):
    query_json = {
    "from": "user",
    "content": ""
    }
    query_json['content'] = query
    query_json_str = json.dumps(query_json)

    try:
        response = call_agent(API_KEY_INTERACT, APP_ID_INTERACT, query_json_str)
    except Exception as e:
        print(f"智能助手响应失败：{e}")
        return None

    json_response = safe_json_parse(response)
    is_go_db, content = is_to_db(json_response)

    if is_go_db:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 实现AI优化用户需求的功能，现在还没做。主要是写提示词
        # if content != '':
        #     query_to_db = f"提问时间：{current_time}\n背景补充：{content}\n用户需求：{query}"
        # else:
        #     query_to_db = f"提问时间：{current_time}\n用户需求：{query}"
        query_to_db = f"提问时间：{current_time}\n用户需求：{query}"
        
        print(f"数据库检索助手正在检索...")
        print("耗时约 1 至 2 分钟，请耐心等待...")
        try:
            search_result = call_agent(API_KEY_SEARCH, APP_ID_SEARCH, query_to_db)
        except Exception as e:
            print(f"数据库检索助手检索失败：{e}")
            return None

        print("数据库检索助手检索完成，智能助手正在整理数据...")
        search_result_to_angent = f"用户需求：{query}\n数据库返回信息：{search_result}"

        try:
            raw_response = call_agent(API_KEY_INTERACT, APP_ID_INTERACT, search_result_to_angent)
        except Exception as e:
            print(f"智能助手整理数据失败：{e}")
            return None

        json_response = safe_json_parse(raw_response)
        return json_response['content']
    else:
        return content


if __name__ == "__main__":
    while True:
        query = input("在这里与智能助手对话：")
        if query == 'exit':
            break
        if query == '':
            print("输入不能为空，请重新输入")
            continue
        response = query_mcp(query)
        print(response)
