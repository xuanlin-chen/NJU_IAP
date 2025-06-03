from dashscope import Application
from http import HTTPStatus
import os

API_RAG = os.getenv("DASHSCOPE_API_KEY_RAG")

def query_rag(question: str):
    config = {
        'api_key': "sk-abf733f33ea64dcd9362d96bcfb77b6f",
        # 'api_key': API_RAG,
        'app_id': '7c8a24304e1f4f4e943d4472904294de'
    }
        
    response = Application.call(
    api_key=config['api_key'],  # 建议改为从环境变量获取
    app_id=config['app_id'],
    prompt=question,
    )
        
    if response.status_code != HTTPStatus.OK:
        return {
            "request_id": response.request_id,
            "code": response.status_code,
            "message": response.message,
            "documentation_url": "https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
        }
    else:
        return {"recommendation": response.output.text}