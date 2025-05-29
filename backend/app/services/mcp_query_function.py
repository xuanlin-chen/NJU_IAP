from http import HTTPStatus
from dashscope import Application
from datetime import datetime
import json

# API_KEY_INTERACT = os.getenv("DASHSCOPE_API_KEY_INTERACT") # 将api_key添加至环境变量
# API_KEY_SEARCH = os.getenv("DASHSCOPE_API_KEY_SEARCH")
API_KEY_INTERACT = 'sk-842115343a2c4f928c445da9e1a7a5b9'
API_KEY_SEARCH = 'sk-f7d1df9afce849a5aad2c27a5a85c97d'
APP_ID_INTERACT = 'd983ba22ecd94a76b83e14f58aea3877'
APP_ID_SEARCH = '105936f2ac6949da98c4375b97fa082f'  # 五并发

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

    json_response = json.loads(response)
    is_go_db, content = is_to_db(json_response)

    if is_go_db:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 实现AI优化用户需求的功能，现在还没做。主要是写提示词
        # if content != '':
        #     query_to_db = f"提问时间：{current_time}\n背景补充：{content}\n用户需求：{query}"
        # else:
        #     query_to_db = f"提问时间：{current_time}\n用户需求：{query}"
        query_to_db = f"提问时间：{current_time}\n用户需求：{query}"
        
        print(f"数据库检索助手正在检索...\n输入给数据库指令：\n{query_to_db}")
        try:
            search_result = call_agent(API_KEY_SEARCH, APP_ID_SEARCH, query_to_db)
        except Exception as e:
            print(f"数据库检索助手检索失败：{e}")
            return None

        print("数据库检索助手检索完成，智能助手正在整理数据...")

        try:
            raw_response = call_agent(API_KEY_INTERACT, APP_ID_INTERACT, search_result)
        except Exception as e:
            print(f"智能助手整理数据失败：{e}")
            return None

        json_response = json.loads(raw_response)
        return json_response['content']
    else:
        return content

'''
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
'''