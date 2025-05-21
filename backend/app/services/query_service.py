from sqlalchemy.orm import Session
from app.db import engine
def query_messages():
    with Session(engine) as session:
        # 实现消息查询逻辑
        return []

def query_by_question(question: str):
    with Session(engine) as session:
        # 实现问题查询逻辑
        return []