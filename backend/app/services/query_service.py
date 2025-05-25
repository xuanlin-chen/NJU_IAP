from fastapi import FastAPI
from sqlalchemy.orm import Session
from dashscope import Application
from http import HTTPStatus
from app.db import engine
from enum import Enum
from datetime import datetime

class SearchModel(Enum):
    RAG = "RAG"
    MCP = "MCP"

# 在query_by_question函数中添加model参数，在查询的时候用户可以选择查询方式
def query_by_question(question: str, model: SearchModel = SearchModel.RAG):
    with Session(engine) as session:
        model_configs = {
            SearchModel.RAG: {
                'api_key': "sk-abf733f33ea64dcd9362d96bcfb77b6f",
                'app_id': '7c8a24304e1f4f4e943d4472904294de',
            },
            SearchModel.MCP: {
                'api_key': "mcp-api-key",
                'app_id': 'mcp-app-id',
            }
        }
        
        # 获取选定模型的配置
        config = model_configs[model]
        
        # 如果是MCP模型，扩充问题格式
        if model == SearchModel.MCP:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_question = f"提问时间：{current_time}\n用户需求：{question}"
        else:
            formatted_question = question
        
        # 调用选定的模型
        response = Application.call(
            api_key=config['api_key'],  # 建议改为从环境变量获取
            app_id=config['app_id'],
            prompt=formatted_question,
        )
    
    # 处理大模型服务的响应
    if response.status_code != HTTPStatus.OK:
        return {
            "request_id": response.request_id,
            "code": response.status_code,
            "message": response.message,
            "documentation_url": "https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
        }
    else:
        return {"recommendation": response.output.text}
