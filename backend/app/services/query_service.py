from fastapi import FastAPI
from sqlalchemy.orm import Session
from dashscope import Application
from http import HTTPStatus
from app.db import engine


def query_by_question(question: str):
    with Session(engine) as session:
        # 实现问题查询逻辑
        response = Application.call(
        api_key="sk-abf733f33ea64dcd9362d96bcfb77b6f",  # 建议改为从环境变量获取
        app_id='7c8a24304e1f4f4e943d4472904294de',  # 替换为实际的应用 ID
        prompt=question  # 直接使用 question 作为 prompt
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
